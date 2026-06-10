"""Mise en batch des observations Dict et des masques d'actions pour PyTorch."""

from __future__ import annotations

import numpy as np
import torch

OBS_KEYS = ("scalars", "shop", "bench", "board", "traits", "opponents", "gods")


def batch_obs(obs_list: list[dict[str, np.ndarray]], device: str = "cpu") -> dict[str, torch.Tensor]:
    """Empile une liste d'observations Dict en tenseurs (B, ...)."""
    batched: dict[str, torch.Tensor] = {}
    for key in OBS_KEYS:
        stacked = np.stack([o[key] for o in obs_list]).astype(np.float32)
        batched[key] = torch.from_numpy(stacked).to(device)
    return batched


def batch_masks(mask_list: list[np.ndarray], device: str = "cpu") -> torch.Tensor:
    """Empile les masques de legalite en BoolTensor (B, NUM_ACTIONS)."""
    stacked = np.stack(mask_list).astype(bool)
    return torch.from_numpy(stacked).to(device)
