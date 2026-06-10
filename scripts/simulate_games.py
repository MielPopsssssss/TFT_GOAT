"""Lance N parties 8 joueurs (actions aléatoires légales) et agrège les résultats.

NB : jeu ALÉATOIRE (pas de stratégie) — ceci caractérise les dynamiques moteur/économie de l'env,
pas le skill. Resolver par défaut = HeuristicProb (ancré meta datatft).

Usage : .venv/bin/python -m scripts.simulate_games [n_games] [seed0]
"""

from __future__ import annotations

import sys

import numpy as np

from tft_goat.env.rounds import round_in_stage, stage_of
from tft_goat.env.tft_env import TftEnv

_POLICY = None  # ActorCritic chargée si --policy fourni (sinon jeu aléatoire)
_SCRIPTED = False  # si True, tous les agents jouent l'heuristique scriptée


def _load_policy(path: str, env):
    import torch

    from tft_goat.agent.network import ActorCritic

    policy = ActorCritic(n_champ=env.encoder.n_champ, n_trait=env.encoder.n_trait)
    policy.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
    policy.eval()
    return policy


def _policy_actions(env, obs, infos):
    """Tous les agents jouent la policy entraînée (greedy)."""
    from tft_goat.agent.obs import batch_masks, batch_obs

    acts = {}
    for a in env.agents:
        b_obs = batch_obs([obs[a]], "cpu")
        b_mask = batch_masks([infos[a]["action_mask"]], "cpu")
        acts[a] = int(_POLICY.act_greedy(b_obs, b_mask).item())
    return acts


def run_one(seed: int):
    env = TftEnv()
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)
    elim_round = {a: None for a in env.possible_agents}
    # dernier état "vivant" connu (board/level) — snapshot avant que la mort vide le board
    last_board = {a: 0 for a in env.possible_agents}
    last_level = {a: 1 for a in env.possible_agents}
    steps = 0
    while env.agents:
        prev_alive = {a: env._state.players[a].alive for a in env.possible_agents}
        for a in env.possible_agents:
            p = env._state.players[a]
            if p.alive:
                last_board[a] = len(p.board)
                last_level[a] = p.level
        if _SCRIPTED:
            from tft_goat.agent.scripted import scripted_action
            acts = {a: scripted_action(env._state, env._state.players[a]) for a in env.agents}
        elif _POLICY is not None:
            acts = _policy_actions(env, obs, infos)
        else:
            acts = {
                a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
                for a in env.agents
            }
        obs, r, term, trunc, infos = env.step(acts)
        steps += 1
        for a in env.possible_agents:  # qui vient de mourir ce round
            if prev_alive[a] and not env._state.players[a].alive and elim_round[a] is None:
                elim_round[a] = env._state.round_index
    st = env._state
    rows = []
    for a, p in st.players.items():
        alive = p.alive or p.placement == 1
        rows.append({
            "placement": p.placement,
            "level": p.level if alive else last_level[a],
            "board": len(p.board) if alive else last_board[a],
            "elim_round": elim_round[a] if elim_round[a] is not None else st.round_index,
            "seat": a,
        })
    return {"rounds": st.round_index, "steps": steps, "players": rows}


def main():
    global _POLICY, _SCRIPTED
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    policy_path = sys.argv[3] if len(sys.argv) > 3 else None
    mode = "ALÉATOIRE"
    if policy_path == "scripted":
        _SCRIPTED = True
        mode = "SCRIPTÉ (heuristique)"
    elif policy_path:
        _POLICY = _load_policy(policy_path, TftEnv())
        mode = f"POLICY entraînée ({policy_path})"

    games = [run_one(seed0 + i) for i in range(n)]

    # --- agrégats partie ---
    rounds = [g["rounds"] for g in games]
    last_stages = [stage_of(g["rounds"]) for g in games]
    avg_rounds = sum(rounds) / n
    avg_stage = sum(last_stages) / n

    # winner final stage en notation x-y
    def xy(ri):
        return f"{stage_of(ri)}-{round_in_stage(ri)}"

    # --- table par placement ---
    by_place = {k: [] for k in range(1, 9)}
    seat_place = {}
    for g in games:
        for r in g["players"]:
            by_place[r["placement"]].append(r)
            seat_place.setdefault(r["seat"], []).append(r["placement"])

    def avg(rows, key):
        vals = [r[key] for r in rows]
        return sum(vals) / len(vals) if vals else 0.0

    print(f"=== {n} parties (jeu {mode}, resolver HeuristicProb ancré datatft) ===\n")
    print("LONGUEUR DE PARTIE")
    print(f"  rounds moyens      : {avg_rounds:.1f}  (min {min(rounds)}, max {max(rounds)})")
    print(f"  stage final moyen  : {avg_stage:.1f}")
    print(f"  fin médiane        : {xy(sorted(rounds)[n // 2])}")
    # distribution du stage de fin
    from collections import Counter
    dist = Counter(last_stages)
    print("  fin par stage      : " + "  ".join(
        f"S{s}:{100*dist[s]/n:.0f}%" for s in sorted(dist)))

    print("\nTABLE PAR PLACEMENT (moyennes ; board/niveau au moment de l'élimination)")
    print(f"  {'place':<6}{'niveau':>8}{'board':>8}{'round élim (x-y)':>18}")
    for k in range(1, 9):
        rows = by_place[k]
        er = avg(rows, "elim_round")
        print(f"  {k:<6}{avg(rows,'level'):>8.2f}{avg(rows,'board'):>8.2f}"
              f"{xy(round(er)):>18}")

    print("\nÉQUITÉ DES SIÈGES (place moyenne, attendu 4.5)")
    seats = sorted(seat_place)
    print("  " + "  ".join(
        f"{s.split('_')[-1]}:{sum(seat_place[s])/len(seat_place[s]):.2f}" for s in seats))


if __name__ == "__main__":
    main()
