"""Featurisation d'un board pour le surrogate de combat.

Reutilise les index champion/trait de `env.encoding.Encoder` pour garantir la coherence
avec le reste du projet.
"""

from __future__ import annotations

import numpy as np
import torch

from ..env.encoding import Encoder
from ..env.state import BoardUnit
from ..env.traits import active_traits

MAX_UNITS = 10


def encode_board(board: list[BoardUnit], encoder: Encoder) -> dict[str, np.ndarray]:
    """Board -> {champ_idx, star, items (MAX_UNITS,), trait_vec (n_trait,)}."""
    champ_idx = np.zeros(MAX_UNITS, dtype=np.int64)
    star = np.zeros(MAX_UNITS, dtype=np.float32)
    items = np.zeros(MAX_UNITS, dtype=np.float32)
    for i, u in enumerate(board[:MAX_UNITS]):
        champ_idx[i] = encoder.champ_index.get(u.champion_api, 0)
        star[i] = u.star
        items[i] = getattr(u, "items", 0)
    trait_vec = np.zeros(encoder.n_trait, dtype=np.float32)
    for name, tier in active_traits([u.champion_api for u in board], encoder._set_content).items():
        idx = encoder.trait_index.get(name)
        if idx is not None:
            trait_vec[idx] = tier
    return {"champ_idx": champ_idx, "star": star, "items": items, "trait_vec": trait_vec}


def batch_boards(
    boards: list[list[BoardUnit]], encoder: Encoder, device: str = "cpu"
) -> dict[str, torch.Tensor]:
    """Empile une liste de boards en tenseurs (B, ...)."""
    feats = [encode_board(b, encoder) for b in boards]
    return {
        "champ_idx": torch.as_tensor(np.stack([f["champ_idx"] for f in feats]), device=device),
        "star": torch.as_tensor(np.stack([f["star"] for f in feats]), device=device),
        "items": torch.as_tensor(np.stack([f["items"] for f in feats]), device=device),
        "trait_vec": torch.as_tensor(np.stack([f["trait_vec"] for f in feats]), device=device),
    }
