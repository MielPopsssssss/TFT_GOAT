"""Hyperparametres PPO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PPOConfig:
    # collecte
    rollout_steps: int = 4096  # nb minimal de transitions (agent-steps) par iteration
    gamma: float = 0.997  # horizon long (reward quasi terminal)
    gae_lambda: float = 0.95

    # optimisation
    lr: float = 3e-4
    clip_coef: float = 0.2
    value_coef: float = 0.5
    entropy_coef: float = 0.01
    max_grad_norm: float = 0.5
    update_epochs: int = 4
    minibatch_size: int = 512

    # reseau
    embed_dim: int = 16
    hidden_dim: int = 256

    # divers
    device: str = "cpu"  # MPS opportuniste possible, CPU sur par defaut
    seed: int = 0
