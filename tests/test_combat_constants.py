"""Pins des constantes du moteur de combat, avec statut d'audit vs patch 17.4 (2026-06-08)."""

from __future__ import annotations

from tft_goat.engine.config import (
    ATTACK_SPEED_CAP,
    MANA_LOCK_DURATION,
    MANA_ON_HIT_CAP,
    MANA_ON_HIT_POSTMIT,
    MANA_ON_HIT_PREMIT,
    MANA_PER_ATTACK,
    STAR_SCALE,
)
from tft_goat.data.models import Champion, SetContent
from tft_goat.engine.unit import build_unit


def test_crit_and_attack_speed_verified_patch_17_4():
    """VÉRIFIÉ vs patch live : crit de base 25% pour ×1.4 dégâts, cap d'attack speed 5.0.

    Sources unanimes : wiki LoL Critical strike + skill tft-knowledge (combat.md).
    """
    assert ATTACK_SPEED_CAP == 5.0
    # défaut data (stats=None) appliqué aux unités sans stats CDragon
    champ = Champion(api_name="X", name="X", cost=1)
    content = SetContent(
        patch="17.4", set_number=17, champions={}, traits={}, items={}, augments={}
    )
    u = build_unit(champ, star=1, team=0, content=content)
    assert u.crit_chance == 0.25
    assert u.crit_mult == 1.4


def test_star_scaling_verified():
    """Star scaling ×1.8 HP/AD par étoile (standard TFT, confirmé skill)."""
    assert STAR_SCALE[1] == 1.0
    assert STAR_SCALE[2] == 1.8
    assert round(STAR_SCALE[3], 4) == round(1.8 * 1.8, 4)


def test_mana_lock_verified():
    """Mana-lock ~1s post-cast — confirmé skill tft-knowledge."""
    assert MANA_LOCK_DURATION == 1.0


def test_mana_gain_matches_skill_reference_but_wiki_disputes():
    """Modèle de mana MODERNE (code == skill) : 10/attaque tous, 1% pré-mit + 7% post-mit, cap 42.5.

    🟡 DISPUTE : la page wiki LoL décrit un modèle par RÔLE (10/7/5 par attaque) + mana-sur-dégâts
    TANKS seulement (1% pré + 3% post) — c'est le modèle HISTORIQUE des premiers sets. Le code suit
    le modèle moderne (= référence skill, sourcée patch notes + in-game testing). NE PAS flipper sans
    confirmation officielle Set 17 ; pin des valeurs courantes pour rendre tout changement explicite.
    """
    assert MANA_PER_ATTACK == 10.0
    assert MANA_ON_HIT_PREMIT == 0.01
    assert MANA_ON_HIT_POSTMIT == 0.07
    assert MANA_ON_HIT_CAP == 42.5
