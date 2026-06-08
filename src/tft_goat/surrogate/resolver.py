"""NeuralResolver : combat resolu par le CombatNet appris. Implemente CombatResolver."""

from __future__ import annotations

import numpy as np
import torch

from ..data.models import SetContent
from ..env.combat import CombatResult
from ..env.encoding import Encoder
from ..env.state import BoardUnit
from .featurize import batch_boards
from .net import CombatNet


class NeuralResolver:
    """Drop-in pour HeuristicResolver : meme interface, combat predit par le reseau."""

    def __init__(self, net: CombatNet, encoder: Encoder, device: str = "cpu"):
        self.net = net.to(device).eval()
        self.encoder = encoder
        self.device = device

    @torch.no_grad()
    def resolve(
        self,
        board_a: list[BoardUnit],
        board_b: list[BoardUnit],
        set_content: SetContent,
        rng: np.random.Generator,
        augments_a: tuple[str, ...] = (),
        augments_b: tuple[str, ...] = (),
    ) -> CombatResult:
        a = batch_boards([board_a], self.encoder, self.device)
        b = batch_boards([board_b], self.encoder, self.device)
        p_a = float(self.net.win_prob(a, b).item())
        winner = 0 if rng.random() < p_a else 1
        win_board = board_a if winner == 0 else board_b
        margin = abs(p_a - 0.5) * 2  # 0 (serre) .. 1 (ecrasant)
        survivors = max(1, round(len(win_board) * margin)) if win_board else 0
        return CombatResult(winner=winner, survivors=survivors)
