"""Tests des probabilites de shop et tailles de pool."""

from __future__ import annotations

import pytest

from tft_goat.data.odds import POOL_SIZES, SHOP_ODDS, pool_size, roll_odds


def test_each_level_row_sums_to_100():
    for patch, table in SHOP_ODDS.items():
        for level, row in table.items():
            assert sum(row) == 100, f"{patch} L{level} ne somme pas a 100: {row}"
            assert len(row) == 5


def test_pool_sizes():
    assert POOL_SIZES == {1: 30, 2: 25, 3: 18, 4: 10, 5: 9}
    assert pool_size(1) == 30
    assert pool_size(5) == 9


def test_roll_odds_returns_probabilities():
    odds = roll_odds(8)
    assert set(odds) == {1, 2, 3, 4, 5}
    assert odds[4] == pytest.approx(0.24)  # L8 4-cost confirme = 24%
    assert sum(odds.values()) == pytest.approx(1.0)


def test_roll_odds_low_levels_only_cheap_units():
    assert roll_odds(1)[1] == pytest.approx(1.0)
    assert roll_odds(2)[5] == pytest.approx(0.0)


def test_disputed_levels_match_verified_patch_17_4():
    """Pin les lignes L7/L8/L9 qui etaient le point de desaccord entre sources.

    Verifie 2026-06-08 contre op.gg ET esportstales (concordants). tftactics donnait
    L7=19/30/35/10/1 (somme 95 => stale/invalide) ; on garde la valeur a somme 100.
    Re-verifier si les patch notes officiels publient une table differente.
    """
    table = SHOP_ODDS["17.4"]
    assert table[7] == (19, 30, 40, 10, 1)
    assert table[8] == (17, 24, 32, 24, 3)
    assert table[9] == (15, 18, 25, 30, 12)


def test_roll_odds_invalid_level():
    with pytest.raises(ValueError):
        roll_odds(99)
