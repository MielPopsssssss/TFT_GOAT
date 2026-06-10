"""Batch 2 des sorts du Set 17 : 12 champions (apiName -> fonction de sort)."""

from __future__ import annotations

from ..unit import CombatUnit  # noqa: F401  (type hint only)


def _akali(caster, allies, enemies, ctx) -> None:
    # Throw piercing kunai at target + nearby enemies, dealing physical AD damage and shredding armor.
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("DamageAD", 2.0) * (caster.ad / 100.0) + caster.ability_value("DamageAP") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, dmg)
    # approx: piercing line + armor shred -> hit a couple nearby enemies for reduced damage
    secondary = dmg * caster.ability_value("SecondaryDamageModifier", 0.5)
    for e in ctx.enemies_in_radius(caster, 2):
        if e is not target:
            ctx.deal_physical(caster, e, secondary)


def _briar(caster, allies, enemies, ctx) -> None:
    # Active: physical AD damage to target (bonus vs tanks). Passive AS approximated as a steroid.
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("ADDamage", 2.0) * (caster.ad / 100.0) + caster.ability_value("APDamage") * (caster.ap / 100.0)
    # approx: bonus damage if target is a tank -> proxy via high max_hp
    if target.max_hp >= 1500:
        dmg *= 1.0 + caster.ability_value("PercentBonusDamage", 0.0)
    ctx.deal_physical(caster, target, dmg)
    ctx.buff_attack_speed(caster, caster.ability_value("AS", 0.0))  # approx: passive missing-HP AS scaling


def _enemy_aatrox(caster, allies, enemies, ctx) -> None:
    pass  # PvE boss unit -> no-op


def _gragas(caster, allies, enemies, ctx) -> None:
    # Heal self, then magic AoE damage + chill (slow approximated as stun) target and adjacent enemies.
    ctx.heal(caster, caster.ability_value("HEALING") * (caster.ap / 100.0))
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("Damage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, dmg)
    for e in ctx.enemies_around(caster, target, 1):
        if e is not target:
            ctx.deal_magic(caster, e, dmg)
    ctx.stun(target, caster.ability_value("CCDuration", 0.0))  # approx: Chill (AS slow)


def _jhin(caster, allies, enemies, ctx) -> None:
    # Active: spectral hands fire alongside Jhin -> burst of physical AD damage to target.
    target = ctx.target_of(caster)
    if target is None:
        return
    hands = caster.ability_value("NumHands", 1.0)
    per = caster.ability_value("ADDamage", 1.0) * (caster.ad / 100.0) + caster.ability_value("APDamage") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, per * hands)  # approx: hands firing over next attacks
    ctx.buff_ad(caster, caster.ability_value("ADConversionRate", 0.0))  # approx: passive AS->AD conversion


def _leona(caster, allies, enemies, ctx) -> None:
    # Shield self, bash target for magic damage and stun.
    ctx.shield_unit(caster, caster.ability_value("ShieldAmount") * (caster.ap / 100.0))
    target = ctx.target_of(caster)
    if target is None:
        return
    # approx: scales with armor+MR -> add a flat fraction of defenses
    dmg = caster.ability_value("Damage") + (caster.armor + caster.mr) * caster.ability_value("DefenseToDamageRatio", 0.0)
    ctx.deal_magic(caster, target, dmg)
    ctx.stun(target, caster.ability_value("StunDuration", 0.0))


def _missfortune(caster, allies, enemies, ctx) -> None:
    # Mode-select unit; approximate the default damage mode as a magic nuke on the nearest enemy.
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("Tier1Damage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, dmg)  # approx: Conduit/Challenger/Replicator mode choice


def _ornn(caster, allies, enemies, ctx) -> None:
    # Shield self, then breathe fire in a cone dealing magic damage.
    ctx.shield_unit(caster, caster.ability_value("Shield") * (caster.ap / 100.0))
    dmg = caster.ability_value("Damage") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(caster, 2):  # approx: cone in front
        ctx.deal_magic(caster, e, dmg)


def _rhaast(caster, allies, enemies, ctx) -> None:
    # Gain durability + heal, then slash forward dealing physical AD damage and knocking up (approx: stun).
    ctx.heal(caster, caster.ability_value("HealAmount") * (caster.ap / 100.0))
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("Damage", 2.0) * (caster.ad / 100.0)
    for e in ctx.enemies_in_radius(caster, 2):  # approx: line slash
        ctx.deal_physical(caster, e, dmg)
    ctx.stun(target, caster.ability_value("KnockupDuration", 0.0))  # approx: knockup


def _talon(caster, allies, enemies, ctx) -> None:
    # Stab target causing a bleed (physical AD damage over time, approximated as upfront), then leap.
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("ADBleedDamage", 2.0) * (caster.ad / 100.0) + caster.ability_value("APBleedDamage") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, dmg)  # approx: bleed DoT applied upfront + leap to high-HP enemy


def _viktor(caster, allies, enemies, ctx) -> None:
    # Channel a psionic storm dealing magic damage each second to enemies within (approx: AoE nuke).
    target = ctx.target_of(caster)
    if target is None:
        return
    dmg = caster.ability_value("Damage") * (caster.ap / 100.0)
    for e in ctx.enemies_around(caster, target, 1):  # approx: growing storm with per-hex falloff
        ctx.deal_magic(caster, e, dmg)


def _training_dummy(caster, allies, enemies, ctx) -> None:
    pass  # Training Dummy cannot act -> no-op


REGISTRY = {
    "TFT17_Akali": _akali,
    "TFT17_Briar": _briar,
    "TFT17_Enemy_Aatrox": _enemy_aatrox,
    "TFT17_Gragas": _gragas,
    "TFT17_Jhin": _jhin,
    "TFT17_Leona": _leona,
    "TFT17_MissFortune": _missfortune,
    "TFT17_Ornn": _ornn,
    "TFT17_Rhaast": _rhaast,
    "TFT17_Talon": _talon,
    "TFT17_Viktor": _viktor,
    "TFT_TrainingDummy": _training_dummy,
}
