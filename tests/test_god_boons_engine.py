"""Tests pin des God Boons du Realm of the Gods câblés au moteur (`augments_set17/batch_6`).

Chaque chiffre est pinné sur sa source : augments setData via `load_set()`, item Anomaly
global (hors setData) via `load_raw()`. Mécanique vérifiée : skill tft-knowledge (le boon
du dieu aligné est octroyé au 4-7). Approximations documentées : docs/COMBAT_COVERAGE.md.
"""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
from tft_goat.engine.simulate import CombatContext
from tft_goat.engine.unit import _GENERIC_ITEM, build_unit


@pytest.fixture(scope="module")
def rc():
    """Contenu Set 17 réel (chargé une fois pour le module)."""
    from tft_goat.data.content import load_set

    return load_set()


# Champs de stats combat observés par les tests de no-op (tout effet doit s'y refléter).
_STATS = (
    "max_hp", "hp", "ad", "ap", "attack_speed", "armor", "mr", "crit_chance",
    "shield", "damage_amp", "incoming_reduction", "omnivamp", "mana_regen",
)


def _snap(team) -> list[tuple]:
    return [tuple(getattr(u, f) for f in _STATS) for u in team]


def _unit(rc, api: str, team: int = 0):
    return build_unit(rc.champions[api], 2, team, rc)


def _apply(rc, aug_api: str, team, seed: int = 0) -> None:
    """Applique le boon comme `simulate._apply_combat_start` : variables réelles de la data."""
    ctx = CombatContext(list(team), np.random.default_rng(seed), content=rc)
    AUGMENT_REGISTRY[aug_api](team, [], ctx, rc.augments[aug_api].effects)


def test_all_17_god_boons_registered(rc):
    """Garde : les 17 GodAugments (tier="god") ont tous une entrée moteur (plus de skip muet)."""
    gods = sorted(api for api, a in rc.augments.items() if a.tier == "god")
    assert len(gods) == 17  # pin : 17 God Boons dans cdragon_17.4
    assert [api for api in gods if api not in AUGMENT_REGISTRY] == []


def test_aurelion_sol_parent_grants_small_quest(rc):
    """Parent « choisis 1 de 3 quêtes » ≈ quête Small (seule à effet combat immédiat)."""
    api = "TFT17_Augment_AurelionSolGodAugment"
    assert rc.augments[api].effects["SmallQuestADAP"] == 15.0  # pin CDragon
    team = [_unit(rc, "TFT17_Aatrox")]
    ad0, ap0 = team[0].ad, team[0].ap
    _apply(rc, api, team)
    assert team[0].ad == pytest.approx(ad0 + 15.0)
    assert team[0].ap == pytest.approx(ap0 + 15.0)


def test_soraka_boon_scales_with_missing_tactician_hp(rc):
    """Soraka : +@HealthPerTacHealth@ HP team par PV tacticien manquant (manque supposé fixe)."""
    from tft_goat.engine.augments_set17.batch_6 import ASSUMED_MISSING_TAC_HP

    api = "TFT17_Augment_SorakaGodAugment"
    assert rc.augments[api].effects["HealthPerTacHealth"] == 2.5  # pin CDragon
    team = [_unit(rc, "TFT17_Aatrox"), _unit(rc, "TFT17_Graves")]
    hp0 = [u.max_hp for u in team]
    _apply(rc, api, team)
    for u, h in zip(team, hp0):
        assert u.max_hp == pytest.approx(h + 2.5 * ASSUMED_MISSING_TAC_HP)


def test_thresh_boon_d6_health_and_as_faces(rc):
    """Thresh : un d6 par combat ; faces Health (+75 HP) et AS (+6%) en combat, le reste éco."""
    api = "TFT17_Augment_ThreshGodAugment"
    fx = rc.augments[api].effects
    # pin CDragon — clés hashées stables du snapshot 17.4 (cf. desc : Health / Attack Speed)
    assert fx["{b386f143}"] == 75.0
    assert fx["{7eafa4c6}"] == pytest.approx(0.06, abs=1e-3)
    seen: set[str] = set()
    for seed in range(120):
        team = [_unit(rc, "TFT17_Aatrox")]
        hp0, as0 = team[0].max_hp, team[0].attack_speed
        _apply(rc, api, team, seed=seed)
        if team[0].max_hp == pytest.approx(hp0 + 75.0):
            seen.add("health")
        elif team[0].attack_speed == pytest.approx(as0 * 1.06):
            seen.add("as")
        elif team[0].max_hp == hp0 and team[0].attack_speed == as0:
            seen.add("eco")
        else:  # pragma: no cover - garde
            raise AssertionError("face de dé inattendue")
    assert seen == {"health", "as", "eco"}  # les 3 issues du dé apparaissent


def test_ekko_anomaly_constants_pinned_to_cdragon_raw():
    """Les constantes Anomaly du moteur == item global CDragon (hors setData, donc en dur+pin)."""
    from tft_goat.data.cdragon import load_raw
    from tft_goat.engine.augments_set17.batch_6 import (
        ANOMALY_FIGHTER_ADAP,
        ANOMALY_MARKSMAN_AS,
        ANOMALY_TANK_HP,
    )

    raw = load_raw()
    item = next(i for i in raw["items"] if i.get("apiName") == "TFT17_EkkoOffering_AnomalyItem")
    fx = item["effects"]
    assert ANOMALY_TANK_HP == fx["TankHP_TOOLTIPONLY"] == 1100
    assert ANOMALY_MARKSMAN_AS == fx["MarksmanBonusAS_TOOLTIPONLY"] == 0.75
    assert ANOMALY_FIGHTER_ADAP == fx["FighterAD_TOOLTIPONLY"] == fx["FighterAP_TOOLTIPONLY"] == 35


def test_ekko_anomaly_evolves_by_role(rc):
    """Ekko : l'Anomaly évolue l'unité selon son rôle data (Tank / Carry / autres≈Fighter)."""
    api = "TFT17_Augment_EkkoGodAugment"
    tank = [_unit(rc, "TFT17_Aatrox")]  # role *Tank
    hp0 = tank[0].max_hp
    _apply(rc, api, tank)
    assert tank[0].max_hp == pytest.approx(hp0 + 1100.0)

    carry = [_unit(rc, "TFT17_Graves")]  # role *Carry -> Marksman
    as0 = carry[0].attack_speed
    _apply(rc, api, carry)
    assert carry[0].attack_speed == pytest.approx(as0 * 1.75)

    fighter = [_unit(rc, "TFT17_Akali")]  # role *Fighter
    ad0, ap0 = fighter[0].ad, fighter[0].ap
    _apply(rc, api, fighter)
    assert fighter[0].ad == pytest.approx(ad0 + 35.0)
    assert fighter[0].ap == pytest.approx(ap0 + 35.0)


def test_ekko_anomaly_evolves_only_strongest(rc):
    """Une seule unité reçoit l'Anomaly : la plus costaud (même approx que Golden Hex)."""
    api = "TFT17_Augment_EkkoGodAugment"
    team = [_unit(rc, "TFT17_Aatrox"), _unit(rc, "TFT17_Graves")]
    strongest = max(team, key=lambda u: u.max_hp)
    weakest = min(team, key=lambda u: u.max_hp)
    before_s, before_w = _snap([strongest]), _snap([weakest])
    _apply(rc, api, team)
    assert _snap([strongest]) != before_s  # la plus costaud a bien évolué
    assert _snap([weakest]) == before_w  # l'autre est intouchée


def test_kayle_scrapper_three_temp_completed_items(rc):
    """Scrapper : @NumComponents@ composants -> items complets temporaires ≈ 3 items génériques."""
    api = "TFT17_Augment_KayleGodAugment_Scrapper"
    assert rc.augments[api].effects["NumComponents"] == 3.0  # pin CDragon
    team = [_unit(rc, a) for a in ("TFT17_Aatrox", "TFT17_Graves", "TFT17_Akali", "TFT17_Briar")]
    hp0 = [u.max_hp for u in team]
    _apply(rc, api, team)
    gained = sorted(u.max_hp - h for u, h in zip(team, hp0))
    assert gained == [0.0] + [_GENERIC_ITEM["Health"]] * 3  # exactement 3 porteurs


def test_yasuo_more_hexes_extends_golden_hex_to_adjacents(rc):
    """MoreHexes : le hex (≈1 modélisé, valeurs Golden Hex) touche aussi 2 adjacents à 100%."""
    api = "TFT17_Augment_YasuoGodAugment_MoreHexes"
    golden = rc.augments["TFT17_Augment_YasuoGodAugment_GoldenHex"].effects
    assert golden["BonusHealth"] == 250.0 and golden["AttackSpeed"] == 0.25  # pin CDragon
    assert rc.augments[api].effects["Effectiveness"] == 1.0  # pin CDragon
    team = [_unit(rc, a) for a in ("TFT17_Aatrox", "TFT17_Graves", "TFT17_Akali", "TFT17_Briar")]
    hp0 = [u.max_hp for u in team]
    _apply(rc, api, team)
    gained = sorted(u.max_hp - h for u, h in zip(team, hp0))
    assert gained == [0.0, 250.0, 250.0, 250.0]  # hex + 2 adjacents (100% d'efficacité)


def test_yasuo_painted_power_amplifies_hex(rc):
    """PaintedPower : puissance des hexes +@Effectiveness@% (l'or-si-2-hexes est de l'éco)."""
    api = "TFT17_Augment_YasuoGodAugment_PaintedPower"
    assert rc.augments[api].effects["Effectiveness"] == 0.5  # pin CDragon
    team = [_unit(rc, "TFT17_Aatrox"), _unit(rc, "TFT17_Graves")]
    strongest = max(team, key=lambda u: u.max_hp)
    hp0, as0 = strongest.max_hp, strongest.attack_speed
    _apply(rc, api, team)
    assert strongest.max_hp == pytest.approx(hp0 + 250.0 * 1.5)
    assert strongest.attack_speed == pytest.approx(as0 * (1.0 + 0.25 * 1.5))


@pytest.mark.parametrize("api", [
    "TFT17_Augment_AurelionSolGodAugment_BoonOfResurrection",  # survie joueur (env)
    "TFT17_Augment_AurelionSolGodAugment_MediumQuest",  # anvil + or (éco)
    "TFT17_Augment_EvelynnGodAugment_BloodPrice",  # shop contre PV (éco)
])
def test_eco_boons_are_faithful_combat_noops(rc, api):
    """Ces boons n'ont AUCUN effet combat dans le vrai jeu : le no-op enregistré est
    l'implémentation combat FIDÈLE (l'effet éco/joueur côté env reste un backlog dédié)."""
    assert api in AUGMENT_REGISTRY
    team = [_unit(rc, "TFT17_Aatrox"), _unit(rc, "TFT17_Graves")]
    before = _snap(team)
    _apply(rc, api, team)
    assert _snap(team) == before


def test_large_quest_grants_plus_one_to_nonunique_traits(rc):
    """LargeQuest : +1 champion virtuel sur chaque trait non-unique PRÉSENT (jamais ex nihilo)."""
    from tft_goat.env.traits import active_traits

    anima2 = ["TFT17_Aurora", "TFT17_Briar"]  # 2 Anima (breakpoints 3/6) : inactif sans bonus
    assert "Anima" not in active_traits(anima2, rc)
    assert active_traits(anima2, rc, bonus_units=1).get("Anima") == 1
    assert active_traits([], rc, bonus_units=1) == {}


def test_large_quest_constant_matches_registry():
    """Anti-drift : la constante de simulate.py et la clé du registre batch_6 doivent rester
    identiques — sinon le bonus de trait s'éteint silencieusement (aucun import ne casse)."""
    from tft_goat.engine.simulate import _LARGE_QUEST_API

    assert _LARGE_QUEST_API in AUGMENT_REGISTRY


def test_large_quest_registry_fn_is_buildtime_noop(rc):
    """Le fn du registre est no-op : l'effet réel vit au build des équipes (trait_bonus)."""
    api = "TFT17_Augment_AurelionSolGodAugment_LargeQuest"
    assert api in AUGMENT_REGISTRY
    team = [_unit(rc, "TFT17_Aatrox")]
    before = _snap(team)
    _apply(rc, api, team)
    assert _snap(team) == before


def _stat_trait_members(rc, needed_minus_one: bool = True) -> list[str]:
    """Membres d'un trait non-unique dont le palier 1 applique de vraies stats moteur,
    en nombre (breakpoint1 - 1) : inactif tel quel, actif avec +1 virtuel."""
    from tft_goat.engine.trait_effects import attrs_for

    for trait in rc.traits.values():
        bps = sorted(trait.breakpoints)
        if bps == [1] or not trait.effects or bps[0] < 2:
            continue
        eff = sorted(trait.effects, key=lambda e: e.min_units)[0]
        has_stat = any(
            attrs_for(k)
            for k, v in eff.variables.items()
            if isinstance(v, (int, float)) and v
        )
        if not has_stat:
            continue
        members = [a for a, ch in sorted(rc.champions.items()) if trait.name in ch.traits]
        if len(members) >= bps[0] - 1:
            return members[: bps[0] - 1]
    pytest.skip("aucun trait non-unique à stats de palier 1 trouvé")


def test_build_team_applies_large_quest_trait_bonus(rc):
    """Intégration : run_combat avec LargeQuest -> traits +1 appliqués au build de l'équipe."""
    from tft_goat.engine.simulate import _build_team
    from tft_goat.env.state import BoardUnit

    apis = _stat_trait_members(rc)
    board = [BoardUnit(champion_api=a, star=2) for a in apis]
    plain = _build_team(board, 0, rc)
    boosted = _build_team(board, 0, rc, trait_bonus=1)
    assert _snap(plain) != _snap(boosted)  # le palier 1 du trait s'applique avec le bonus
