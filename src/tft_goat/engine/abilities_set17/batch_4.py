"""Set 17 champion abilities - batch 4 (11 champions)."""

from __future__ import annotations


def _aurora(caster, allies, enemies, ctx) -> None:
    # Rift: nuke target + split AoE magic damage to enemies in radius.
    target = ctx.target_of(caster)
    if target is not None:
        ctx.deal_magic(caster, target, caster.ability_value("Damage") * (caster.ap / 100.0))
    r = max(1, int(caster.ability_value("SpellHexRadius", 2.0)))
    hit = ctx.enemies_in_radius(caster, r)
    if hit:
        split = caster.ability_value("SplitDamage") * (caster.ap / 100.0) / len(hit)
        for e in hit:
            ctx.deal_magic(caster, e, split)


def _chogath(caster, allies, enemies, ctx) -> None:
    # Tank: magic nuke (% max hp + AP) on lowest-hp enemy; grow own max hp.
    target = ctx.lowest_hp_enemy(caster)
    if target is None:
        return
    dmg = target.max_hp * caster.ability_value("PercentMaximumHealthDamage") + \
        caster.ability_value("BonusDamage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, dmg)
    # approx: permanent max-hp growth -> heal as durability gain
    ctx.heal(caster, caster.ability_value("BonusHealthPerCast"))


def _fiora(caster, allies, enemies, ctx) -> None:
    # Carry: reveal vitals and quick-attack -> single bigger true-damage nuke + self heal.
    target = ctx.target_of(caster)
    if target is None:
        return
    hits = max(1, int(caster.ability_value("NumVitals", 3.0)))
    dmg = caster.ability_value("VitalDamage") * (caster.ad / 100.0) * hits  # approx: multi-vital strike
    ctx.deal_true(caster, target, dmg)
    ctx.heal(caster, dmg * caster.ability_value("PercentHealing"))


def _gwen(caster, allies, enemies, ctx) -> None:
    # Carry: snip lowest %hp enemy (single nuke) + AoE to nearby enemies.
    target = ctx.lowest_hp_enemy(caster)
    if target is not None:
        ctx.deal_magic(caster, target, caster.ability_value("Damage") * (caster.ap / 100.0))
    for e in ctx.enemies_in_radius(caster, 1):
        ctx.deal_magic(caster, e, caster.ability_value("AreaDamage") * (caster.ap / 100.0))


def _kaisa(caster, allies, enemies, ctx) -> None:
    # Carry: fire missiles in radius around target -> AoE physical (per-missile dmg x count).
    n = max(1, int(caster.ability_value("BaseNumMissiles", 1.0)))
    per = caster.ability_value("ADDamage") * (caster.ad / 100.0) + caster.ability_value("APDamage") * (caster.ap / 100.0)
    r = max(1, int(caster.ability_value("HexRange", 2.0)))
    hit = ctx.enemies_in_radius(caster, r)
    target = ctx.target_of(caster)
    if target is not None and target not in hit:
        hit = hit + [target]
    if not hit:
        return
    # approx: distribute n missiles across enemies in radius
    for i in range(n):
        ctx.deal_physical(caster, hit[i % len(hit)], per)


def _lulu(caster, allies, enemies, ctx) -> None:
    # Utility: call down magic damage to several nearby enemies.
    n = max(1, int(caster.ability_value("NumEnemies", 1.0)))
    dmg = caster.ability_value("Damage") * (caster.ap / 100.0)
    for e in ctx.living_enemies(caster)[:n]:
        ctx.deal_magic(caster, e, dmg)


def _morgana(caster, allies, enemies, ctx) -> None:
    # Tank/AoE DoT: gain health, AoE magic to closest enemies, heal nearby allies.
    ctx.shield_unit(caster, caster.ability_value("APHealthGain") * (caster.ap / 100.0))  # approx: transform hp gain
    n = max(1, int(caster.ability_value("NumEnemies", 1.0)))
    dmg = caster.ability_value("APDamage") * (caster.ap / 100.0)
    for e in ctx.living_enemies(caster)[:n]:
        ctx.deal_magic(caster, e, dmg)
    na = max(1, int(caster.ability_value("NumAllies", 1.0)))
    heal = caster.ability_value("APHealing") * (caster.ap / 100.0)
    for a in ctx.allies_of(caster)[:na]:
        ctx.heal(a, heal)


def _poppy(caster, allies, enemies, ctx) -> None:
    # Tank: shield self + grant armor/MR (approx as shield) to allies within two hexes.
    ctx.shield_unit(caster, caster.ability_value("Shield") * (caster.ap / 100.0))
    bonus = caster.ability_value("Resists") * (caster.ap / 100.0)
    for a in ctx.allies_of(caster):  # approx: armor/MR buff -> shield
        ctx.shield_unit(a, bonus)


def _samira(caster, allies, enemies, ctx) -> None:
    # Carry: volley of bullets at target -> burst physical + stun.
    target = ctx.target_of(caster)
    if target is None:
        return
    ctx.deal_physical(caster, target, caster.ability_value("Damage") * (caster.ad / 100.0))  # approx: volley as one nuke
    ctx.stun(target, caster.ability_value("StunDuration"))


def _twistedfate(caster, allies, enemies, ctx) -> None:
    # Utility: throw a card for magic damage (use average of min/max range).
    target = ctx.target_of(caster)
    if target is None:
        return
    avg = (caster.ability_value("DamageMin") + caster.ability_value("DamageMax")) / 2.0
    ctx.deal_magic(caster, target, avg * (caster.ap / 100.0))


def _zed(caster, allies, enemies, ctx) -> None:
    # Carry: create a clone -> approx as a burst physical strike on the target.
    target = ctx.target_of(caster)
    if target is None:
        return
    # approx: clone inheriting stats casting -> extra AD-based hit
    ctx.deal_physical(caster, target, caster.ad * (1.0 - caster.ability_value("HPPenalty", 0.5)))


REGISTRY = {
    "TFT17_Aurora": _aurora,
    "TFT17_Chogath": _chogath,
    "TFT17_Fiora": _fiora,
    "TFT17_Gwen": _gwen,
    "TFT17_Kaisa": _kaisa,
    "TFT17_Lulu": _lulu,
    "TFT17_Morgana": _morgana,
    "TFT17_Poppy": _poppy,
    "TFT17_Samira": _samira,
    "TFT17_TwistedFate": _twistedfate,
    "TFT17_Zed": _zed,
}
