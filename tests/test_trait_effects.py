"""Tests des bonus de stats de traits (engine/trait_effects) — dont le fix heal vs health.

Bug corrigé : `heal` (substring) matchait `health` -> la branche health->hp était du code
mort et AUCUN bonus HP de trait n'était appliqué en combat (Brawler +25/45/65 %, Meeple
+100..500 flat). Découvert par l'audit des fiches (2026-06-10).
"""

from __future__ import annotations

import pytest

from tft_goat.data.content import load_set
from tft_goat.engine.trait_effects import apply_team_traits, attrs_for
from tft_goat.engine.unit import build_unit
from tft_goat.env.traits import active_traits


@pytest.fixture(scope="module")
def sc():
    return load_set()


def test_attrs_for_health_vs_heal_classification():
    """Table de vérité du fix : health -> hp ; heal/seuils/percent-health -> skip."""
    # HP réels (le cœur du bug : jamais appliqués avant le fix)
    assert attrs_for("HealthBonus") == ["hp"]  # Brawler +25/45/65 %
    assert attrs_for("BonusHealth") == ["hp"]  # Meeple +100..500 flat
    assert attrs_for("Wolf_Health") == ["hp"]  # aspect Stargazer (modèle aspects-en-bloc, P2)
    assert attrs_for("ShieldHP") == ["hp"]  # approximation v0 existante (shield -> hp)
    # Heals et mécaniques non-stat : toujours skippés
    assert attrs_for("Heal") == []  # N.O.V.A. (soin, pas une stat)
    assert attrs_for("Huntress_Heal") == []
    assert attrs_for("ModifiedHealAmount") == []
    assert attrs_for("HealthThreshold") == []  # seuil de déclenchement
    assert attrs_for("TransformedPercentHealth") == []  # mécanique Mecha
    assert attrs_for("Shield_CashoutHP") == []  # cashout (éco)
    # Clés *health* qui ne sont PAS des buffs HP vérifiés (jamais deviner) :
    assert attrs_for("PVEHP") == []  # flag PvE Fiora=1.0 — en fraction ça doublait ses HP
    assert attrs_for("HealthRatio") == []  # ratio d'ability (Commander)
    assert attrs_for("Shield_Health_Teamwide") == []  # paramètre de bouclier Stargazer


def test_fiora_unique_trait_does_not_double_hp(sc):
    """Régression PVEHP : le trait unique de Fiora (PVEHP=1.0) ne doit PAS doubler ses HP."""
    fiora = next((c for _, c in sorted(sc.champions.items()) if "Fiora" in c.api_name), None)
    if fiora is None:
        pytest.skip("pas de Fiora dans la data")
    unit = build_unit(fiora, 1, 0, sc)
    base = unit.max_hp
    apply_team_traits([unit], sc)
    assert unit.max_hp < base * 1.7, f"HP parasites : {base} -> {unit.max_hp}"


def test_multiple_hp_fractions_compound_multiplicatively():
    """Deux fractions hp se composent en (1+a)(1+b) — commutatif, donc déterministe."""
    from tft_goat.engine.trait_effects import _apply_stat
    from tft_goat.engine.unit import CombatUnit

    u = CombatUnit(champion_api="x", star=1, team=0, max_hp=1000.0, hp=1000.0,
                   ad=50.0, ap=100.0, attack_speed=0.6, armor=20.0, mr=20.0,
                   attack_range=1, crit_chance=0.25, crit_mult=1.4, max_mana=100.0, mana=0.0)
    _apply_stat(u, "hp", 0.25)
    _apply_stat(u, "hp", 0.45)
    assert u.max_hp == pytest.approx(1000.0 * 1.25 * 1.45)  # 1812.5, pas 1700


def _team_of(sc, trait_name: str, n: int):
    """n champions distincts porteurs du trait, dont SEUL ce trait est actif (sinon skip)."""
    holders = [c for _, c in sorted(sc.champions.items()) if trait_name in c.traits]
    if len(holders) < n:
        pytest.skip(f"moins de {n} porteurs de {trait_name} dans la data")
    from itertools import combinations

    for combo in combinations(holders, n):
        apis = [c.api_name for c in combo]
        if set(active_traits(apis, sc)) == {trait_name}:
            return list(combo)
    pytest.skip(f"pas de combinaison de {n} {trait_name} sans autre trait actif")


def test_brawler_health_bonus_is_applied_as_fraction(sc):
    """Brawler tier 1 : chaque porteur gagne +25 % de HP max (fraction, pas +0.25 flat)."""
    champs = _team_of(sc, "Brawler", 2)
    units = [build_unit(c, 1, 0, sc) for c in champs]
    base = [u.max_hp for u in units]
    apply_team_traits(units, sc)
    for u, b in zip(units, base):
        assert u.max_hp == pytest.approx(b * 1.25), f"{u.champion_api}: {b} -> {u.max_hp}"
        assert u.hp == pytest.approx(b * 1.25)


def test_meeple_bonus_health_is_applied_flat(sc):
    """Meeple tier 1 (3 porteurs) : chaque porteur gagne +100 HP flat."""
    champs = _team_of(sc, "Meeple", 3)
    units = [build_unit(c, 1, 0, sc) for c in champs]
    base = [u.max_hp for u in units]
    apply_team_traits(units, sc)
    for u, b in zip(units, base):
        assert u.max_hp == pytest.approx(b + 100.0), f"{u.champion_api}: {b} -> {u.max_hp}"


def test_nova_heal_variable_grants_no_hp(sc):
    """N.O.V.A. : la variable Heal (soin 12 %) ne doit PAS devenir un bonus de HP max."""
    champs = _team_of(sc, "N.O.V.A.", 2)
    units = [build_unit(c, 1, 0, sc) for c in champs]
    base = [u.max_hp for u in units]
    apply_team_traits(units, sc)
    for u, b in zip(units, base):
        # N.O.V.A. tier 1 peut donner d'autres stats, mais jamais un +0.12 hp parasite :
        # le max_hp reste soit inchangé, soit modifié par une VRAIE clé hp (aucune au tier 1).
        assert u.max_hp == pytest.approx(b), f"{u.champion_api}: {b} -> {u.max_hp}"
