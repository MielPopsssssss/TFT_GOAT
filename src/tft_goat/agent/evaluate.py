"""Evaluation : la policy (1 siege) contre 7 joueurs aleatoires.

Baseline random = placement moyen ~4.5. Un placement moyen < 4.5 prouve que l'agent apprend.
"""

from __future__ import annotations

import numpy as np
import torch

from .network import ActorCritic
from .obs import batch_masks, batch_obs
from .scripted import scripted_action


def _placement_stats(placements: list[int]) -> dict[str, float]:
    arr = np.array(placements, dtype=float)
    return {
        "mean_placement": float(arr.mean()),
        "win_rate": float((arr == 1).mean()),
        "top4_rate": float((arr <= 4).mean()),
    }


@torch.no_grad()
def eval_vs_opponents(
    policy: ActorCritic,
    env,
    opponent: str = "random",  # "random" ou "scripted"
    n_games: int = 30,
    seat: str = "player_0",
    device: str = "cpu",
    seed: int = 1000,
) -> dict[str, float]:
    """Place la policy sur un siège ; les 7 autres jouent `opponent` (aléatoire ou scripté)."""
    placements: list[int] = []
    for g in range(n_games):
        rng = np.random.default_rng(seed + g)
        obs, infos = env.reset(seed=seed + g)
        while env.agents:
            act_dict = {}
            for a in env.agents:
                if a == seat:
                    mask = infos[a]["action_mask"]
                    b_obs = batch_obs([obs[a]], device)
                    b_mask = batch_masks([mask], device)
                    act_dict[a] = int(policy.act_greedy(b_obs, b_mask).item())
                elif opponent == "scripted":
                    act_dict[a] = scripted_action(env._state, env._state.players[a])
                else:
                    act_dict[a] = int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
            obs, rewards, terms, truncs, infos = env.step(act_dict)
        placements.append(env._state.players[seat].placement)
    return _placement_stats(placements)


@torch.no_grad()
def eval_vs_random(
    policy: ActorCritic,
    env,
    n_games: int = 30,
    seat: str = "player_0",
    device: str = "cpu",
    seed: int = 1000,
) -> dict[str, float]:
    return eval_vs_opponents(policy, env, "random", n_games, seat, device, seed)
