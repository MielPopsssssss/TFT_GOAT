"""Joue une partie 8 joueurs complete en actions aleatoires legales (smoke manuel).

Usage : .venv/bin/python -m tft_goat.scripts.random_rollout [seed]
"""

from __future__ import annotations

import sys

import numpy as np

from ..env.tft_env import TftEnv


def run(seed: int = 0) -> None:
    env = TftEnv()  # contenu reel (load_set)
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)

    steps = 0
    while env.agents:
        actions = {}
        for a in env.agents:
            legal = np.flatnonzero(infos[a]["action_mask"])
            actions[a] = int(rng.choice(legal))
        obs, rewards, terminations, truncations, infos = env.step(actions)
        steps += 1

    ranking = sorted(env._state.players.values(), key=lambda p: p.placement)
    print(f"Partie terminee en {steps} steps, {env._state.round_index} rounds.\n")
    print("Classement final :")
    for p in ranking:
        print(f"  {p.placement}. {p.agent_id}  hp={p.hp:>4}  niveau={p.level}  "
              f"board={len(p.board)}")


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    run(seed)
