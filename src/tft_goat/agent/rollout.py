"""Collecte de trajectoires par self-play (parties completes) + calcul GAE.

Les 8 sieges sont controles par la meme policy ; leurs transitions sont poolees. On joue des
parties entieres : chaque trajectoire de siege se termine (done=True, reward = placement),
donc le GAE n'a pas besoin de bootstrap a la troncature.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch

from .network import ActorCritic
from .obs import batch_masks, batch_obs


@dataclass
class Batch:
    obs: list[dict[str, np.ndarray]]
    masks: list[np.ndarray]
    actions: np.ndarray
    logprobs: np.ndarray
    advantages: np.ndarray
    returns: np.ndarray
    values: np.ndarray
    # metriques
    mean_game_reward: float
    mean_game_len: float
    n_games: int

    def __len__(self) -> int:
        return len(self.actions)


def compute_gae(
    rewards: list[float], values: list[float], dones: list[bool], gamma: float, lam: float
) -> tuple[list[float], list[float]]:
    """GAE pour une trajectoire (terminale). Retourne (advantages, returns)."""
    n = len(rewards)
    adv = [0.0] * n
    last = 0.0
    for t in reversed(range(n)):
        next_value = values[t + 1] if t + 1 < n else 0.0
        nonterminal = 0.0 if dones[t] else 1.0
        delta = rewards[t] + gamma * next_value * nonterminal - values[t]
        last = delta + gamma * lam * nonterminal * last
        adv[t] = last
    returns = [adv[t] + values[t] for t in range(n)]
    return adv, returns


@torch.no_grad()
def collect_games(
    env, policy: ActorCritic, min_steps: int, gamma: float, lam: float, device: str = "cpu"
) -> Batch:
    obs_buf: list[dict[str, np.ndarray]] = []
    mask_buf: list[np.ndarray] = []
    act_buf: list[int] = []
    logp_buf: list[float] = []
    val_buf: list[float] = []
    adv_buf: list[float] = []
    ret_buf: list[float] = []

    game_rewards: list[float] = []
    game_lens: list[int] = []
    seed = 0

    while len(act_buf) < min_steps:
        obs, infos = env.reset(seed=seed)
        seed += 1
        # par siege : listes paralleles de transitions
        traj: dict[str, dict[str, list]] = {
            a: {"obs": [], "mask": [], "act": [], "logp": [], "val": [], "rew": [], "done": []}
            for a in env.possible_agents
        }
        steps = 0
        while env.agents:
            agents = list(env.agents)
            ob_list = [obs[a] for a in agents]
            mk_list = [infos[a]["action_mask"] for a in agents]
            b_obs = batch_obs(ob_list, device)
            b_mask = batch_masks(mk_list, device)
            actions, logps, values = policy.act(b_obs, b_mask)
            actions_np = actions.cpu().numpy()
            logps_np = logps.cpu().numpy()
            values_np = values.cpu().numpy()

            act_dict = {a: int(actions_np[i]) for i, a in enumerate(agents)}
            for i, a in enumerate(agents):
                t = traj[a]
                t["obs"].append(ob_list[i])
                t["mask"].append(mk_list[i])
                t["act"].append(int(actions_np[i]))
                t["logp"].append(float(logps_np[i]))
                t["val"].append(float(values_np[i]))

            obs, rewards, terms, truncs, infos = env.step(act_dict)
            for a in agents:
                traj[a]["rew"].append(float(rewards[a]))
                traj[a]["done"].append(bool(terms[a] or truncs[a]))
            steps += 1

        # fin de partie : GAE par siege et accumulation
        for a in env.possible_agents:
            t = traj[a]
            if not t["act"]:
                continue
            adv, ret = compute_gae(t["rew"], t["val"], t["done"], gamma, lam)
            obs_buf.extend(t["obs"])
            mask_buf.extend(t["mask"])
            act_buf.extend(t["act"])
            logp_buf.extend(t["logp"])
            val_buf.extend(t["val"])
            adv_buf.extend(adv)
            ret_buf.extend(ret)
            game_rewards.append(t["rew"][-1])  # reward terminal (placement)
        game_lens.append(steps)

    return Batch(
        obs=obs_buf,
        masks=mask_buf,
        actions=np.array(act_buf, dtype=np.int64),
        logprobs=np.array(logp_buf, dtype=np.float32),
        advantages=np.array(adv_buf, dtype=np.float32),
        returns=np.array(ret_buf, dtype=np.float32),
        values=np.array(val_buf, dtype=np.float32),
        mean_game_reward=float(np.mean(game_rewards)) if game_rewards else 0.0,
        mean_game_len=float(np.mean(game_lens)) if game_lens else 0.0,
        n_games=len(game_lens),
    )
