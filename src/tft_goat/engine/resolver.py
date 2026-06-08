"""EngineResolver : le vrai moteur de combat expose comme CombatResolver."""

from __future__ import annotations

import numpy as np

from ..data.models import SetContent
from ..env.combat import CombatResult
from ..env.state import BoardUnit
from .simulate import run_combat


class EngineResolver:
    """Drop-in pour HeuristicResolver/NeuralResolver : combat simule tick-par-tick."""

    def resolve(
        self,
        board_a: list[BoardUnit],
        board_b: list[BoardUnit],
        set_content: SetContent,
        rng: np.random.Generator,
        augments_a: tuple[str, ...] = (),
        augments_b: tuple[str, ...] = (),
    ) -> CombatResult:
        return run_combat(board_a, board_b, set_content, rng, augments_a, augments_b)
