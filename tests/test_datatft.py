"""Tests des vraies stats datatft : parsing, facteur de force, integration combat."""

from __future__ import annotations

import json

import numpy as np
import pytest

from tft_goat.config import FIXTURES_DIR
from tft_goat.data.datatft import build_meta_stats
from tft_goat.data.stats_models import (
    POWER_MAX,
    POWER_MIN,
    MetaStats,
    UnitStat,
    place_to_power,
)
from tft_goat.env.combat import HeuristicResolver, board_strength
from tft_goat.env.state import BoardUnit


@pytest.fixture(scope="module")
def meta() -> MetaStats:
    raw = json.loads((FIXTURES_DIR / "datatft_sample.json").read_text(encoding="utf-8"))
    return build_meta_stats(raw, patch="17.4")


def test_parsing(meta: MetaStats):
    assert len(meta.units) == 2
    assert "TFT17_Jhin" in meta.units
    assert meta.units["TFT17_Jhin"].avg_place == pytest.approx(3.9506, abs=1e-3)
    assert len(meta.traits) == 2
    t5 = meta.traits[MetaStats.trait_key("TFT17_Stargazer_Mountain", 5)]
    assert t5.tier == 5


def test_place_to_power_monotonic_and_bounded():
    assert place_to_power(2.0) > place_to_power(4.5) > place_to_power(6.0)
    assert place_to_power(4.5) == pytest.approx(1.0)
    assert place_to_power(1.0) == POWER_MAX  # clamp haut
    assert place_to_power(100.0) == POWER_MIN  # clamp bas


def test_unit_power_uses_real_place(meta: MetaStats):
    # Jhin (place 3.95) est plus fort que Briar (place 5.47)
    assert meta.unit_power("TFT17_Jhin") > meta.unit_power("TFT17_Briar")
    assert meta.unit_power("inconnu") == 1.0  # neutre si absent


def test_combat_anchored_by_stats(sample_content):
    # deux champions de MEME cout/etoile mais placements differents
    meta = MetaStats(
        patch="t",
        units={
            "c3": UnitStat(key="c3", avg_place=2.2, top4=65, win=20, count=1000),
            "c4": UnitStat(key="c4", avg_place=6.5, top4=35, win=5, count=1000),
        },
    )
    rng = np.random.default_rng(0)
    resolver = HeuristicResolver(meta_stats=meta)
    strong, weak = [BoardUnit("c3", 1)], [BoardUnit("c4", 1)]
    wins = sum(resolver.resolve(strong, weak, sample_content, rng).winner == 0 for _ in range(200))
    assert wins > 130  # l'unite mieux classee gagne nettement plus souvent


def test_backward_compat_without_stats(sample_content):
    # sans meta_stats : force brute cout×etoile (c7 = 4-cost, 2-star -> 12)
    assert board_strength([BoardUnit("c7", 2)], sample_content) == pytest.approx(12.0)
