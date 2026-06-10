"""Pins du batch prismatic 7 (priorisation 2026-06-10 : exposition uniforme par tier ->
les prismatic combat non modélisés sont la plus grosse distorsion ; Riot a retiré les
augments de match-v1 donc pas de proxy d'usage challenger possible).

Chaque chiffre référence la data CDragon (`augments.effects`, composants `items`)."""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
from tft_goat.engine.simulate import CombatContext
from tft_goat.engine.unit import build_unit


@pytest.fixture(scope="module")
def rc():
    from tft_goat.data.content import load_set

    return load_set()


def _team(rc, n=5):
    apis = ("TFT17_Aatrox", "TFT17_Graves", "TFT17_Akali", "TFT17_Briar", "TFT17_Shen")
    return [build_unit(rc.champions[a], 2, 0, rc) for a in apis[:n]]


def _apply(rc, api, team, seed=0):
    ctx = CombatContext(list(team), np.random.default_rng(seed), content=rc)
    AUGMENT_REGISTRY[api](team, [], ctx, rc.augments[api].effects)


def test_belt_overflow_grants_boosted_belts(rc):
    """4 Giant's Belts (+150 HP base data) boostées à +@BonusHealth@ -> 4 porteurs."""
    api = "TFT_Augment_BeltOverflow"
    fx = rc.augments[api].effects
    assert fx["NumItems"] == 4.0 and fx["BonusHealth"] == 85.0  # pin CDragon
    belt = rc.items["TFT_Item_GiantsBelt"].effects.get("Health", 0.0)
    assert belt == 150.0  # pin composant
    team = _team(rc)
    hp0 = [u.max_hp for u in team]
    _apply(rc, api, team)
    gained = sorted(u.max_hp - h for u, h in zip(team, hp0))
    assert gained == [0.0] + [belt + 85.0] * 4  # 4 porteurs, +235 HP chacun


def test_comeback_story_scales_with_missing_tac_hp(rc):
    """Team +@HPPerMissingHP@ HP et +@ASPerMissingHP@% AS par PV joueur manquant."""
    from tft_goat.engine.augments_set17.batch_6 import ASSUMED_MISSING_TAC_HP

    api = "TFT_Augment_ComebackStory"
    fx = rc.augments[api].effects
    assert fx["HPPerMissingHP"] == 4.0
    assert fx["ASPerMissingHP"] == pytest.approx(0.4, abs=0.01)
    team = _team(rc, n=2)
    hp0, as0 = team[0].max_hp, team[0].attack_speed
    _apply(rc, api, team)
    assert team[0].max_hp == pytest.approx(hp0 + 4.0 * ASSUMED_MISSING_TAC_HP)
    assert team[0].attack_speed == pytest.approx(
        as0 * (1.0 + 0.4 / 100.0 * ASSUMED_MISSING_TAC_HP)
    )


def test_sweet_treats_health_per_equipped_item(rc):
    """Team +@HealthPerItem@ HP par item équipé (items réels si visibles, sinon ~6)."""
    api = "TFT_Augment_SweetTreats"
    assert rc.augments[api].effects["HealthPerItem"] == 16.0  # pin CDragon
    team = _team(rc, n=2)
    team[0].item_apis = ("TFT_Item_InfinityEdge", "TFT_Item_GiantsBelt")
    team[1].item_apis = ("TFT_Item_RunaansHurricane",)
    hp0 = [u.max_hp for u in team]
    _apply(rc, api, team)
    for u, h in zip(team, hp0):
        assert u.max_hp == pytest.approx(h + 16.0 * 3)  # 3 items équipés visibles


def test_wand_overflow_grants_boosted_rods(rc):
    """4 Rods (+@AP@ base data) qui donnent aussi +@BonusStat*100@% AS -> 4 porteurs."""
    api = "TFT_Augment_WandOverflow"
    fx = rc.augments[api].effects
    assert fx["NumItems"] == 4.0
    assert fx["BonusStat"] == pytest.approx(0.05, abs=0.001)  # pin CDragon
    rod_ap = rc.items["TFT_Item_NeedlesslyLargeRod"].effects.get("AP", 0.0)
    assert rod_ap > 0  # pin composant (AP non nul)
    team = _team(rc)
    snap = [(u.ap, u.attack_speed) for u in team]
    _apply(rc, api, team)
    boosted = [
        u for u, (ap0, as0) in zip(team, snap)
        if u.ap == pytest.approx(ap0 + rod_ap) and u.attack_speed == pytest.approx(as0 * 1.05)
    ]
    assert len(boosted) == 4  # exactement 4 porteurs
