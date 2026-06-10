"""Tests des items & augments dans l'env."""

from __future__ import annotations

import numpy as np

from tft_goat.env.actions import (
    EQUIP,
    PASS,
    PICK_AUGMENT_START,
    apply_action,
    legal_mask,
)
from tft_goat.env.combat import board_strength
from tft_goat.env.economy import COMPONENTS_PER_ITEM, ITEMS_MAX
from tft_goat.env.rounds import _apply_damage
from tft_goat.env.shop import Pool
from tft_goat.env.state import BoardUnit, GameState, PlayerState


def _state(content, **kw):
    p = PlayerState(agent_id="p0", **kw)
    return GameState(players={"p0": p}, pool=Pool(content),
                     set_content=content, rng=np.random.default_rng(0)), p


def test_equip_consumes_components(sample_content):
    state, p = _state(sample_content, components=["cmp_bf", "cmp_bow"])
    p.board = [BoardUnit("c7", 1, on_board=True)]
    assert legal_mask(state, p)[EQUIP]
    apply_action(state, p, EQUIP)
    assert p.board[0].items == 1
    assert "it_combined" in p.board[0].item_apis  # recette reelle appliquee
    assert p.components == []


def test_equip_illegal_without_components(sample_content):
    state, p = _state(sample_content, components=["cmp_bf"])  # un seul composant
    p.board = [BoardUnit("c7", 1, on_board=True)]
    assert not legal_mask(state, p)[EQUIP]


def test_equip_caps_at_max(sample_content):
    state, p = _state(sample_content, components=["cmp_bf", "cmp_bow"])
    p.board = [BoardUnit("c7", 1, on_board=True, items=ITEMS_MAX)]
    assert not legal_mask(state, p)[EQUIP]  # unite deja pleine


def test_items_increase_board_strength(sample_content):
    bare = board_strength([BoardUnit("c7", 2)], sample_content)
    armed = board_strength([BoardUnit("c7", 2, items=2)], sample_content)
    assert armed > bare


def test_augment_offer_forces_pick(sample_content):
    state, p = _state(sample_content)
    p.augment_offer = ["a", "b", "c"]
    mask = legal_mask(state, p)
    assert not mask[PASS]  # PASS interdit tant qu'un augment est propose
    assert mask[PICK_AUGMENT_START] and mask[PICK_AUGMENT_START + 2]
    apply_action(state, p, PICK_AUGMENT_START)
    assert p.augment_offer == []
    assert p.augment_power > 0.0


def test_god_offer_forces_champion_pick(sample_content):
    from tft_goat.env.actions import PICK_GOD_START

    state, p = _state(sample_content)
    p.god_offer = ["c1", "c3", "c7"]  # Realm of the Gods : 3 champions
    mask = legal_mask(state, p)
    assert not mask[PASS]  # choix force
    assert mask[PICK_GOD_START] and mask[PICK_GOD_START + 2]
    n0 = len(p.bench)
    apply_action(state, p, PICK_GOD_START + 1)  # choisit c3
    assert p.god_offer == []
    assert len(p.bench) == n0 + 1
    assert p.bench[-1].champion_api == "c3"


def test_augment_tier_detection():
    """Le tier (silver/gold/prismatic) est lu depuis l'icone CDragon ; les God Augments -> 'god'."""
    from tft_goat.data.augment_tiers import detect_tier

    assert detect_tier("TFT17_Augment_X", "x/Crown_Bruiser_III.TFT_Set17.tex") == "prismatic"
    assert detect_tier("TFT17_Augment_X", "x/AnimaCommander_II.TFT_Set17.tex") == "gold"
    assert detect_tier("TFT17_Augment_X", "x/AatroxHero_I.TFT_Set17.tex") == "silver"
    assert detect_tier("TFT17_Augment_X", "x/BandThieves3.tex") == "prismatic"
    assert detect_tier("TFT17_Augment_AurelionSolGodAugment_SmallQuest", "x/y.tex") == "god"


def test_real_augments_all_have_a_tier():
    """Sur la vraie data Set 17, chaque augment recoit un tier valide (jamais '?')."""
    from tft_goat.data.content import load_set

    sc = load_set()
    valid = {"silver", "gold", "prismatic", "god"}
    assert all(a.tier in valid for a in sc.augments.values())
    # le pool regulier (hors god) est non vide pour chaque tier
    regular = [a for a in sc.augments.values() if a.tier != "god"]
    tiers = {a.tier for a in regular}
    assert {"silver", "gold", "prismatic"} <= tiers


def test_augment_offer_respects_tier_odds_and_excludes_gods(sample_content):
    """L'offre d'augment tire selon les odds du round et n'inclut jamais un God Augment."""
    import numpy as np

    from tft_goat.env.rounds import sample_augments
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState

    state = GameState(players={}, pool=Pool(sample_content), set_content=sample_content,
                      rng=np.random.default_rng(0))
    p = PlayerState(agent_id="p0")
    offer = sample_augments(state, p, 3)
    assert len(offer) == 3
    assert len(set(offer)) == 3  # pas de doublon dans une meme offre
    for api in offer:
        assert sample_content.augments[api].tier != "god"


def test_augment_reroll_costs_2_gold_and_changes_offer(sample_content):
    """Le reroll d'augment coûte 2 gold, est légal si gold suffisant, et re-tire l'offre."""
    from tft_goat.env.actions import REROLL_AUGMENT
    from tft_goat.env.economy import REROLL_COST

    state, p = _state(sample_content, gold=5)
    p.augment_offer = list(sample_content.augments)[:3]
    mask = legal_mask(state, p)
    assert mask[REROLL_AUGMENT]  # reroll possible (gold >= 2)
    apply_action(state, p, REROLL_AUGMENT)
    assert p.gold == 5 - REROLL_COST  # 2 gold dépensés
    assert len(p.augment_offer) == 3  # toujours 3 augments proposés
    assert all(sample_content.augments[a].tier != "god" for a in p.augment_offer)


def test_augment_reroll_illegal_without_gold(sample_content):
    from tft_goat.env.actions import REROLL_AUGMENT

    state, p = _state(sample_content, gold=1)  # < 2 gold
    p.augment_offer = list(sample_content.augments)[:3]
    assert not legal_mask(state, p)[REROLL_AUGMENT]


def test_player_damage_is_not_mitigated_by_augments(sample_content):
    """Correction 2026-06-08 : les dégâts JOUEUR ne sont plus réduits par augment_power.

    Un augment renforce le board (proba de victoire via le resolver), il ne réduit pas les
    dégâts subis à la défaite. L'ancienne mitigation gonflait la durée des parties (stage 7.8→6.9).
    """
    _, p = _state(sample_content)
    p.hp = 100
    p.augment_power = 0.5  # ne doit plus avoir d'effet sur les dégâts joueur
    _apply_damage(p, 20)
    assert p.hp == 80  # dégâts pleins (20), sans mitigation
