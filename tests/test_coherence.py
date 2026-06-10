"""Invariants de cohérence du déroulé de partie (vérifiés sur parties complètes).

Verrouille les invariants STRUCTURELS (indépendants de l'agent) confirmés sur 500 parties :
placements = permutation 1..8, board ≤ cap de niveau, valeurs saines, équité des sièges.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from tft_goat.env.economy import MAX_LEVEL
from tft_goat.env.tft_env import TftEnv

N_GAMES = 40


def _run(seed):
    env = TftEnv()
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)
    viol = []
    while env.agents:
        for p in env._state.players.values():
            if p.alive:
                if len(p.board) > p.level:
                    viol.append(f"board {len(p.board)} > niveau {p.level}")
                if p.hp < 0 or p.gold < 0 or not (1 <= p.level <= MAX_LEVEL):
                    viol.append(f"absurde hp={p.hp} gold={p.gold} lvl={p.level}")
        acts = {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
        obs, r, term, trunc, infos = env.step(acts)
    placements = {a: p.placement for a, p in env._state.players.items()}
    return placements, viol


def test_coherence_invariants_over_games():
    """Sur N parties : permutation 1..8 valide, board≤cap, valeurs saines, sièges équitables."""
    seat = defaultdict(list)
    for seed in range(N_GAMES):
        placements, viol = _run(seed)
        assert not viol, f"partie {seed}: violation {viol[0]}"
        assert sorted(placements.values()) == list(range(1, 9)), (
            f"partie {seed}: placements != permutation 1..8 ({sorted(placements.values())})"
        )
        for a, pl in placements.items():
            seat[a].append(pl)
    # équité des sièges (bande large pour N modéré ; à 500 parties tous ≈ 4.5)
    for a, places in seat.items():
        m = sum(places) / len(places)
        assert 3.5 <= m <= 5.5, f"siège {a} place moyenne {m:.2f} hors bande (biais positionnel ?)"


def test_sim_supports_realistic_economy_and_starring_via_scripted_agent():
    """Le SIM permet une éco + des étoiles réalistes — prouvé par l'agent scripté compétent.

    Découplé de la qualité du PPO : l'agent scripté atteint or moyen ~52 (réaliste, pas la
    thésaurisation à 250+ du jeu non-optimisé) et max-star moyen ~1.9 (il 2-star). Une régression
    sim cassant la dépense (buy/reroll) ou la combinaison (2-star) ferait sauter ce test.
    """
    from tft_goat.agent.scripted import scripted_action

    golds, stars, boards, items = [], [], [], []
    for seed in range(25):
        env = TftEnv()
        obs, infos = env.reset(seed=seed)
        last = {a: {"g": 0, "s": 1, "b": 0, "i": 0} for a in env.possible_agents}
        while env.agents:
            for a in env.possible_agents:
                p = env._state.players[a]
                if p.alive:
                    last[a] = {"g": p.gold, "s": max((u.star for u in p.board), default=1),
                               "b": len(p.board), "i": sum(u.items for u in p.board)}
            acts = {a: scripted_action(env._state, env._state.players[a]) for a in env.agents}
            obs, r, term, trunc, infos = env.step(acts)
        for a in env.possible_agents:
            golds.append(last[a]["g"])
            stars.append(last[a]["s"])
            boards.append(last[a]["b"])
            items.append(last[a]["i"])

    avg_gold = sum(golds) / len(golds)
    avg_star = sum(stars) / len(stars)
    avg_board = sum(boards) / len(boards)
    avg_items = sum(items) / len(items)
    assert avg_gold < 90, f"agent scripté thésaurise ({avg_gold:.0f}) -> dépense cassée ?"
    assert avg_star > 1.5, f"agent scripté ne 2-star pas ({avg_star:.2f}) -> combinaison cassée ?"
    # Capacités sim prouvées par un agent sensé (les FAILs random étaient un faux signal,
    # cf. scripts/check_coherence.py batch scripté, investigation 2026-06-10) :
    assert avg_board > 4.0, f"agent scripté ne remplit pas son board ({avg_board:.2f})"
    assert avg_items > 0.5, f"agent scripté n'équipe pas d'items ({avg_items:.2f})"
