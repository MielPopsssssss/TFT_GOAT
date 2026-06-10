"""Fait tourner N parties (agent entraîné) et vérifie une batterie d'INVARIANTS de cohérence.

Chaque invariant -> PASS/FAIL. Sortie structurée pour piloter une boucle d'audit :
  - si tout PASS : le déroulé est cohérent à ce niveau de jeu.
  - si un FAIL : incohérence à investiguer/corriger (vrai bug, pas artefact).

Usage : .venv/bin/python -m scripts.check_coherence [n_games] [policy.pt] [seed0]
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict

import numpy as np

from tft_goat.env.economy import MAX_LEVEL
from tft_goat.env.rounds import stage_of
from tft_goat.env.tft_env import TftEnv

_POLICY = None


def _load_policy(path, env):
    import torch

    from tft_goat.agent.network import ActorCritic

    pol = ActorCritic(n_champ=env.encoder.n_champ, n_trait=env.encoder.n_trait)
    pol.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
    pol.eval()
    return pol


def _actions(env, obs, infos, rng):
    if _POLICY is None:
        return {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
    from tft_goat.agent.obs import batch_masks, batch_obs

    acts = {}
    for a in env.agents:
        b_obs = batch_obs([obs[a]], "cpu")
        b_mask = batch_masks([infos[a]["action_mask"]], "cpu")
        acts[a] = int(_POLICY.act_greedy(b_obs, b_mask).item())
    return acts


def run_one(seed):
    env = TftEnv()
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)
    last = {a: {"board": 0, "level": 1, "champs": ()} for a in env.possible_agents}
    violations = []
    while env.agents:
        for a in env.possible_agents:
            p = env._state.players[a]
            if p.alive:
                last[a] = {"board": len(p.board), "level": p.level,
                           "champs": tuple(u.champion_api for u in p.board),
                           "gold": p.gold,
                           "max_star": max((u.star for u in p.board), default=1),
                           "items": sum(u.items for u in p.board)}
                if len(p.board) > p.level:
                    violations.append(f"board {len(p.board)} > niveau {p.level}")
                if p.hp < 0 or p.gold < 0 or not (1 <= p.level <= MAX_LEVEL):
                    violations.append(f"valeur absurde hp={p.hp} gold={p.gold} lvl={p.level}")
        obs, r, term, trunc, infos = env.step(_actions(env, obs, infos, rng))
    st = env._state
    placements = [p.placement for p in st.players.values()]
    rows = [{"seat": a, "placement": p.placement, **last[a]} for a, p in st.players.items()]
    return {"final_stage": stage_of(st.round_index), "placements": placements,
            "rows": rows, "violations": violations, "content": st.set_content}


def check(results):
    n = len(results)
    checks = []

    def add(name, ok, detail):
        checks.append((name, ok, detail))

    # 1. longueur réaliste
    stages = [g["final_stage"] for g in results]
    avg_stage = sum(stages) / n
    add("longueur (stage final moyen ∈ [6.0,7.5])", 6.0 <= avg_stage <= 7.5, f"{avg_stage:.2f}")

    # 2. placements valides : chaque partie = permutation 1..8, exactement un 1er
    bad_perm = sum(1 for g in results if sorted(g["placements"]) != list(range(1, 9)))
    add("placements = permutation 1..8 par partie", bad_perm == 0, f"{bad_perm} parties invalides")

    # 3. équité des sièges (toutes ~4.5)
    seat = defaultdict(list)
    for g in results:
        for r in g["rows"]:
            seat[r["seat"]].append(r["placement"])
    means = {s: sum(v) / len(v) for s, v in seat.items()}
    add("équité sièges (tous ∈ [3.8,5.2])", all(3.8 <= m <= 5.2 for m in means.values()),
        " ".join(f"{s.split('_')[-1]}:{m:.2f}" for s, m in sorted(means.items())))

    # 4. gradient placement->board (top2 > bottom2)
    by_place = defaultdict(list)
    for g in results:
        for r in g["rows"]:
            by_place[r["placement"]].append(r["board"])
    top = (np.mean(by_place[1]) + np.mean(by_place[2])) / 2
    bottom = (np.mean(by_place[7]) + np.mean(by_place[8])) / 2
    add("gradient board (top2 > bottom2)", top > bottom, f"top {top:.2f} vs bottom {bottom:.2f}")

    # 5. board rempli par l'agent (survivants top4 board moyen > 4)
    top4_board = np.mean([b for pl in (1, 2, 3, 4) for b in by_place[pl]])
    add("agent fielde (board top4 > 4.0)", top4_board > 4.0, f"{top4_board:.2f}")

    # 6. aucune violation d'invariant live (board<=cap, valeurs saines)
    nviol = sum(len(g["violations"]) for g in results)
    sample = next((g["violations"][0] for g in results if g["violations"]), "")
    add("invariants live (board<=cap, valeurs saines)", nviol == 0, f"{nviol} violations {sample}")

    # --- cohérence des comps (itération 2) ---
    from tft_goat.data.datatft import load_meta_stats
    from tft_goat.env.traits import active_traits
    content = results[0]["content"]
    meta = load_meta_stats()

    by_place_champs = defaultdict(list)
    for g in results:
        for r in g["rows"]:
            if r["champs"]:
                by_place_champs[r["placement"]].append(r["champs"])

    # 7. synergies de traits : les boards gagnants ont des traits ACTIFS (≥2 en moyenne)
    def avg_active_traits(places):
        vals = [len(active_traits(list(c), content)) for pl in places for c in by_place_champs[pl]]
        return np.mean(vals) if vals else 0.0
    top_traits = avg_active_traits((1, 2))
    add("synergies de traits (top2 boards ≥ 2 traits actifs)", top_traits >= 2.0, f"{top_traits:.2f}")

    # 8. (INFORMATIF, pas PASS/FAIL) force méta moyenne des unités jouées par l'agent vs roster.
    # Mesure la QUALITÉ d'agent (a-t-il appris la méta), PAS la cohérence du simulateur :
    # board_strength récompense coût×étoile×traits, donc 3-star d'unités cheap gagne sans
    # viser la haute méta. En self-play, comparer top/bottom est mal posé (comps homogènes).
    played = [meta.unit_power(api) for g in results for r in g["rows"] for api in r["champs"]]
    pop_mean = np.mean([meta.unit_power(a) for a in content.champions if a.startswith("TFT17_")])
    agent_mean = np.mean(played) if played else 0.0
    print(f"  ℹ️  INFO   méta moyenne unités jouées (qualité agent) | "
          f"agent {agent_mean:.3f} vs roster {pop_mean:.3f}")

    # 9. distribution des coûts : les boards tardifs ne sont pas QUE du 1-cost (coût moyen > 1.5)
    def avg_cost(places):
        vals = [content.champions[api].cost for pl in places for c in by_place_champs[pl]
                for api in c if api in content.champions]
        return np.mean(vals) if vals else 0.0
    top_cost = avg_cost((1, 2))
    add("distribution coûts (coût moyen top2 > 1.5)", top_cost > 1.5, f"{top_cost:.2f}")

    # --- cohérence objets + INFO qualité d'agent (itération 3) ---
    rows_all = [r for g in results for r in g["rows"] if r["champs"]]
    # 10. items : l'agent équipe des objets => le mécanisme d'items fonctionne en jeu (PASS/FAIL).
    top4_items = np.mean([r["items"] for r in rows_all if r["placement"] <= 4]) if rows_all else 0.0
    add("équipement d'items (items top4 > 0.5)", top4_items > 0.5, f"{top4_items:.2f}")
    # INFO (qualité d'agent, PAS cohérence sim) : économie + étoiles. Le sim PERMET une éco/étoiles
    # réalistes — prouvé par l'agent scripté (or ~52, star ~1.90, cf. tests/test_coherence.py).
    # Un PPO sous-entraîné thésaurise et sous-star ; c'est de l'entraînement, pas un bug sim.
    avg_gold = np.mean([r["gold"] for r in rows_all]) if rows_all else 0.0
    avg_star = np.mean([r["max_star"] for r in rows_all]) if rows_all else 0.0
    print(f"  ℹ️  INFO   éco/étoiles (qualité agent) | or moyen {avg_gold:.0f}, max-star {avg_star:.2f} "
          f"(scripté: or 52, star 1.90)")

    return checks, avg_stage


def main():
    global _POLICY
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    policy = sys.argv[2] if len(sys.argv) > 2 else None
    seed0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    if policy:
        _POLICY = _load_policy(policy, TftEnv())

    results = [run_one(seed0 + i) for i in range(n)]
    checks, avg_stage = check(results)

    print(f"=== COHÉRENCE sur {n} parties ({'policy '+policy if policy else 'aléatoire'}) ===\n")
    all_ok = True
    for name, ok, detail in checks:
        flag = "✅ PASS" if ok else "❌ FAIL"
        if not ok:
            all_ok = False
        print(f"  {flag}  {name:42} | {detail}")
    print(f"\n  VERDICT : {'TOUT COHÉRENT ✅' if all_ok else 'INCOHÉRENCE(S) DÉTECTÉE(S) ❌'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
