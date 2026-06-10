"""Pins de fidélité des abilities outliers identifiés par realism_vs_datatft (2026-06-10).

Root causes confirmées vs data CDragon (chaque chiffre référence `champion.ability.variables`) :
- Sona : le slam (SlamDamage) est « every @NumCasts@ casts » — il était appliqué à CHAQUE
  cast avec stun systématique (~3-4x sur-tunée, premier win rate saturé à 1.00).
- Blitzcrank : passive bolt (BoltDamage toutes les @BoltCooldown@s) et knockup du clump
  (GrooveDurationPerTarget) absents — il ne faisait que les dégâts de l'active.
- Graves : passive « attacks fire @NumProjectiles@ projectiles à @PassivePercentBAD@ AD »
  absente (165% AD par auto au lieu de 100%).
"""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.engine.abilities import get_ability
from tft_goat.engine.simulate import CombatContext
from tft_goat.engine.unit import build_unit


@pytest.fixture(scope="module")
def rc():
    from tft_goat.data.content import load_set

    return load_set()


def _setup(rc, caster_api: str, n_enemies: int = 2):
    """Caster 2 étoiles + ennemis adjacents, ctx réel avec probes deal_magic/physical/stun."""
    caster = build_unit(rc.champions[caster_api], 2, 0, rc)
    caster.pos = (3, 3)
    enemies = [build_unit(rc.champions["TFT17_Shen"], 2, 1, rc) for _ in range(n_enemies)]
    for e, pos in zip(enemies, [(4, 3), (4, 4), (5, 3)]):
        e.pos = pos
    ctx = CombatContext([caster] + enemies, np.random.default_rng(0), content=rc)
    log = {"magic": [], "physical": [], "true": [], "stun": []}
    ctx.deal_magic = lambda src, tgt, raw: log["magic"].append((tgt, raw))
    ctx.deal_physical = lambda src, tgt, raw: log["physical"].append((tgt, raw))
    ctx.deal_true = lambda src, tgt, raw: log["true"].append((tgt, raw))
    ctx.stun = lambda tgt, dur: log["stun"].append((tgt, dur))
    return caster, enemies, ctx, log


def test_sona_slam_amortized_over_numcasts(rc):
    """Un cast Sona = debris + slam/NumCasts (amorti), jamais le slam entier à chaque cast."""
    v = rc.champions["TFT17_Sona"].ability.variables
    assert v["NumCasts"][2] == 5.0  # pin CDragon
    assert v["DebrisDamage"][2] == 450.0 and v["SlamDamage"][2] == 1100.0  # pin 2 étoiles
    caster, enemies, ctx, log = _setup(rc, "TFT17_Sona")
    get_ability("TFT17_Sona")(caster, [], [e for e in enemies], ctx)
    total = sum(raw for _, raw in log["magic"])
    expected = (450.0 + 1100.0 / 5.0) * (caster.ap / 100.0)
    assert total == pytest.approx(expected)


def test_sona_stun_gated_not_every_cast(rc):
    """Le stun du slam arrive ~1 cast sur NumCasts (rng), pas à chaque cast."""
    stuns = 0
    n = 200
    caster, enemies, ctx, log = _setup(rc, "TFT17_Sona")
    for _ in range(n):
        log["stun"].clear()
        get_ability("TFT17_Sona")(caster, [], [e for e in enemies], ctx)
        stuns += bool(log["stun"])
    assert 0.08 <= stuns / n <= 0.35  # ~1/5, bande large (rng)


def test_blitzcrank_active_knocks_up_the_clump(rc):
    """L'active stun (knockup) les ennemis autour de la cible — le CC réel du disco ball."""
    v = rc.champions["TFT17_Blitzcrank"].ability.variables
    assert v["GrooveDurationPerTarget"][2] == 1.0  # pin CDragon
    caster, enemies, ctx, log = _setup(rc, "TFT17_Blitzcrank")
    get_ability("TFT17_Blitzcrank")(caster, [], [e for e in enemies], ctx)
    assert len(log["stun"]) >= 2  # cible + adjacents knockup
    assert all(dur == pytest.approx(1.0) for _, dur in log["stun"])


def test_blitzcrank_passive_bolts_included(rc):
    """La passive (bolt/2s) est amortie dans le cast : dégâts > uppercut + explosions seuls."""
    from tft_goat.engine.abilities_set17.batch_1 import _BLITZ_BOLTS_PER_CAST

    v = rc.champions["TFT17_Blitzcrank"].ability.variables
    assert v["BoltDamage"][2] == 90.0 and v["BoltCooldown"][2] == 2.0  # pin CDragon
    caster, enemies, ctx, log = _setup(rc, "TFT17_Blitzcrank")
    get_ability("TFT17_Blitzcrank")(caster, [], [e for e in enemies], ctx)
    total = sum(raw for _, raw in log["magic"])
    ap = caster.ap / 100.0
    base_active = (225.0 + 265.0 * len(enemies)) * ap  # uppercut + explosion par ennemi touché
    assert total > base_active  # les bolts passifs s'ajoutent
    bolts = total - (225.0 * ap + sum(
        raw for tgt, raw in log["magic"] if raw == pytest.approx(265.0 * ap)
    ))
    # la constante est une approximation assumée (PAS un chiffre pinné CDragon) :
    # on vérifie la cohérence avec la source, pas une valeur magique dupliquée.
    assert bolts == pytest.approx(_BLITZ_BOLTS_PER_CAST * 90.0 * ap)


def test_no_ability_friendly_fire(rc):
    """Garde systémique : AUCUNE ability ne doit infliger de dégâts à sa propre équipe.

    Root cause historique : `enemies_in_radius(target, r)` = ennemis DE la cible = alliés
    du caster — 10 AoE nukaient leur propre frontline (Vex, le baseline de la métrique de
    réalisme, incluse). Corrigé via `enemies_around(caster, target, r)`."""
    from tft_goat.engine.abilities_set17 import SET17_ABILITIES

    offenders = []
    for api in sorted(SET17_ABILITIES):
        if api not in rc.champions:
            continue
        caster, enemies, ctx, log = _setup(rc, api, n_enemies=3)
        ally = build_unit(rc.champions["TFT17_Shen"], 2, 0, rc)
        ally.pos = (3, 2)  # collé au caster ET adjacent à la cible (4,3)
        ctx.units.append(ally)
        SET17_ABILITIES[api](caster, [ally], list(enemies), ctx)
        for kind in ("magic", "physical", "true"):
            if any(tgt.team == 0 for tgt, _ in log[kind]):
                offenders.append(api)
                break
    assert offenders == []


def test_graves_passive_projectiles_buff_autos_once(rc):
    """Passive : 5 projectiles x 33% AD = 165% AD par auto -> buff +65% AD une seule fois."""
    v = rc.champions["TFT17_Graves"].ability.variables
    assert v["NumProjectiles"][2] == 5.0  # pin CDragon
    assert v["PassivePercentBAD"][2] == pytest.approx(0.33, abs=0.01)
    caster, enemies, ctx, log = _setup(rc, "TFT17_Graves")
    ad0 = caster.ad
    get_ability("TFT17_Graves")(caster, [], [e for e in enemies], ctx)
    factor = 5.0 * v["PassivePercentBAD"][2]
    assert caster.ad == pytest.approx(ad0 * factor)
    get_ability("TFT17_Graves")(caster, [], [e for e in enemies], ctx)
    assert caster.ad == pytest.approx(ad0 * factor)  # ne re-stack PAS au 2e cast
