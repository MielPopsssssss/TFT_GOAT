"""Mise a jour PPO (clip-surrogate + value + entropy) sur un Batch collecte."""

from __future__ import annotations

import numpy as np
import torch

from .config import PPOConfig
from .network import ActorCritic
from .obs import batch_masks, batch_obs
from .rollout import Batch


def ppo_update(
    policy: ActorCritic, optimizer: torch.optim.Optimizer, batch: Batch, cfg: PPOConfig
) -> dict[str, float]:
    device = cfg.device
    n = len(batch)
    actions = torch.as_tensor(batch.actions, device=device)
    old_logp = torch.as_tensor(batch.logprobs, device=device)
    returns = torch.as_tensor(batch.returns, device=device)
    advantages = torch.as_tensor(batch.advantages, device=device)
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    metrics = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0}
    n_updates = 0
    idx = np.arange(n)
    for _ in range(cfg.update_epochs):
        np.random.shuffle(idx)
        for start in range(0, n, cfg.minibatch_size):
            mb = idx[start : start + cfg.minibatch_size]
            mb_obs = batch_obs([batch.obs[i] for i in mb], device)
            mb_mask = batch_masks([batch.masks[i] for i in mb], device)
            new_logp, entropy, value = policy.evaluate_actions(mb_obs, mb_mask, actions[mb])

            ratio = (new_logp - old_logp[mb]).exp()
            adv_mb = advantages[mb]
            l_unclipped = ratio * adv_mb
            l_clipped = torch.clamp(ratio, 1 - cfg.clip_coef, 1 + cfg.clip_coef) * adv_mb
            policy_loss = -torch.min(l_unclipped, l_clipped).mean()
            value_loss = ((value - returns[mb]) ** 2).mean()
            ent = entropy.mean()
            loss = policy_loss + cfg.value_coef * value_loss - cfg.entropy_coef * ent

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), cfg.max_grad_norm)
            optimizer.step()

            metrics["policy_loss"] += float(policy_loss.item())
            metrics["value_loss"] += float(value_loss.item())
            metrics["entropy"] += float(ent.item())
            n_updates += 1

    for k in metrics:
        metrics[k] /= max(n_updates, 1)
    return metrics
