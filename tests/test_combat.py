"""Tests du combat heuristique et de l'interface CombatResolver."""

from __future__ import annotations

import numpy as np

from tft_goat.env.combat import CombatResult, HeuristicResolver, board_strength
from tft_goat.env.state import BoardUnit


def test_board_strength_scales_with_star(sample_content):
    one = [BoardUnit("c7", 1)]  # 4-cost 1-star
    three = [BoardUnit("c7", 3)]  # 4-cost 3-star
    assert board_strength(three, sample_content) > board_strength(one, sample_content)


def test_stronger_board_wins_majority(sample_content):
    rng = np.random.default_rng(7)
    strong = [BoardUnit("c7", 3), BoardUnit("c8", 2), BoardUnit("c5", 2)]
    weak = [BoardUnit("c1", 1)]
    resolver = HeuristicResolver()
    wins_a = sum(
        resolver.resolve(strong, weak, sample_content, rng).winner == 0
        for _ in range(200)
    )
    assert wins_a > 170  # board nettement plus fort gagne >85%


def test_empty_vs_nonempty(sample_content):
    rng = np.random.default_rng(1)
    res = HeuristicResolver().resolve([], [BoardUnit("c1", 1)], sample_content, rng)
    assert res.winner == 1


def test_resolver_substitution(sample_content):
    """Un resolver factice deterministe satisfait l'interface (couture etape 4)."""

    class AlwaysB:
        def resolve(self, board_a, board_b, set_content, rng):
            return CombatResult(winner=1, survivors=2)

    res = AlwaysB().resolve([BoardUnit("c8", 3)], [], sample_content, None)
    assert res.winner == 1 and res.survivors == 2
