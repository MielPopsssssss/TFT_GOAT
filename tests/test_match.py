"""Test du parsing match-v1 sur un fixture offline (format Riot reel)."""

from __future__ import annotations

import json

import pytest

from tft_goat.config import FIXTURES_DIR
from tft_goat.data.content import build_set_content
from tft_goat.data.riot.match import parse_match


@pytest.fixture(scope="module")
def match():
    raw = json.loads((FIXTURES_DIR / "match_sample.json").read_text(encoding="utf-8"))
    return parse_match(raw)


def test_eight_participants(match):
    assert len(match.participants) == 8


def test_placements_are_1_to_8(match):
    assert sorted(p.placement for p in match.participants) == list(range(1, 9))


def test_set_and_version(match):
    assert match.set_number == 17
    assert match.game_version.startswith("Version 17")


def test_winner_board_parsed(match):
    winner = next(p for p in match.participants if p.placement == 1)
    assert winner.level == 9
    assert len(winner.augments) == 3
    unit = winner.units[0]
    assert unit.character_id == "TFT17_Rammus"
    assert unit.tier == 2
    assert "TFT_Item_InfinityEdge" in unit.items


def test_units_map_to_content(match):
    """Les character_id des parties doivent correspondre aux apiNames du contenu."""
    raw = json.loads((FIXTURES_DIR / "cdragon_sample.json").read_text(encoding="utf-8"))
    content = build_set_content(raw, patch="17.4")
    winner = next(p for p in match.participants if p.placement == 1)
    mapped = [u.character_id for u in winner.units if u.character_id in content.champions]
    assert "TFT17_Rammus" in mapped
