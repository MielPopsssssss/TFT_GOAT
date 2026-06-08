"""Golden tests du parsing de contenu, sur un fixture CDragon trime (deterministe)."""

from __future__ import annotations

import json

import pytest

from tft_goat.config import FIXTURES_DIR
from tft_goat.data.content import build_set_content
from tft_goat.data.models import SetContent


@pytest.fixture(scope="module")
def content() -> SetContent:
    raw = json.loads((FIXTURES_DIR / "cdragon_sample.json").read_text(encoding="utf-8"))
    return build_set_content(raw, patch="17.4")


def test_champion_parsed(content: SetContent):
    rammus = content.champions["TFT17_Rammus"]
    assert rammus.cost == 4
    assert "Bastion" in rammus.traits
    assert rammus.stats.hp == 1300.0
    assert rammus.ability.name == "Gravitational Spin"


def test_trait_breakpoints(content: SetContent):
    bastion = content.traits["TFT17_ResistTank"]
    assert bastion.name == "Bastion"
    assert bastion.breakpoints == (2, 4, 6)


def test_item_composition(content: SetContent):
    ie = content.items["TFT_Item_InfinityEdge"]
    assert ie.composition == ("TFT_Item_BFSword", "TFT_Item_SparringGloves")
    assert "CritChance" in ie.effects


def test_augment_resolved(content: SetContent):
    aug = content.augments["TFT10_Augment_CrashTestDummies"]
    assert "_Augment_" in aug.api_name
    assert aug.name


def test_set_metadata(content: SetContent):
    assert content.patch == "17.4"
    assert content.set_number == 17


def test_models_are_immutable(content: SetContent):
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        content.champions["TFT17_Rammus"].cost = 5
