"""Set 17 champion ability logic — batch 3 (11 champions)."""

from __future__ import annotations


def _aurelionsol(caster, allies, enemies, ctx) -> None:
    # Deathbeam: channeled line toward target dealing magic damage/sec, falling off per enemy passed.
    target = ctx.target_of(caster)
    if target is None:
        return
    dps = caster.ability_value("DamagePerSecond") * (caster.ap / 100.0)
    duration = caster.ability_value("Duration")
    total = dps * max(duration, 1.0)
    ctx.deal_magic(caster, target, total)  # approx: full-channel damage on primary target
    falloff = 1.0 - caster.ability_value("DamageReductionPerTarget")
    amount = total * falloff
    for e in ctx.enemies_in_radius(target, 1):  # approx: beam pierces enemies behind target
        if e is not target:
            ctx.deal_magic(caster, e, amount)


def _caitlyn(caster, allies, enemies, ctx) -> None:
    # Aim For The Head: empowered Headshot — big single-target physical (AD + AP).
    target = ctx.target_of(caster)
    if target is None:
        return
    amount = caster.ability_value("Damage") * (caster.ad / 100.0) \
        + caster.ability_value("BonusDamage") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, amount)


def _ezreal(caster, allies, enemies, ctx) -> None:
    # Temporal Shot: fire a blast at target (AD + AP physical), plus drone follow-up.
    target = ctx.target_of(caster)
    if target is None:
        return
    amount = caster.ability_value("ADDamage") * (caster.ad / 100.0) \
        + caster.ability_value("APDamage") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, amount)
    # approx: periodic drone fires an extra physical bolt at the current target
    drone = caster.ability_value("DroneDamage") * (caster.ad / 100.0)
    if drone > 0:
        ctx.deal_physical(caster, target, drone)


def _graves(caster, allies, enemies, ctx) -> None:
    # Collateral Damage: explosive shell — physical to target + AoE to adjacent enemies.
    target = ctx.target_of(caster)
    if target is None:
        return
    primary = caster.ability_value("Damage") * (caster.ad / 100.0)
    ctx.deal_physical(caster, target, primary)
    secondary = caster.ability_value("SecondaryDamageAD") * (caster.ad / 100.0) \
        + caster.ability_value("SecondaryDamageAP") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(target, 1):
        if e is not target:
            ctx.deal_physical(caster, e, secondary)


def _jinx(caster, allies, enemies, ctx) -> None:
    # Explosive Attitude: barrage of rockets in a cone, each hitting first target (AD physical).
    target = ctx.target_of(caster)
    if target is None:
        return
    per_rocket = caster.ability_value("ADDamage") * (caster.ad / 100.0) \
        + caster.ability_value("APDamage") * (caster.ap / 100.0)
    rockets = max(1, int(caster.ability_value("RocketsPerLaunchAttack", 1)))
    ctx.deal_physical(caster, target, per_rocket * rockets)  # approx: cone of rockets onto target
    for e in ctx.enemies_in_radius(target, 1):  # approx: spillover onto nearby cone targets
        if e is not target:
            ctx.deal_physical(caster, e, per_rocket)


def _lissandra(caster, allies, enemies, ctx) -> None:
    # Dark Matter: shard to first target (AP magic), then explodes hitting nearby enemies.
    target = ctx.target_of(caster)
    if target is None:
        return
    primary = caster.ability_value("Damage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, primary)
    secondary = caster.ability_value("SecondaryDamage") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(target, 1):
        if e is not target:
            ctx.deal_magic(caster, e, secondary)


def _mordekaiser(caster, allies, enemies, ctx) -> None:
    # Indestructible: gain shield, then each second add shield + AoE magic to adjacent enemies.
    duration = max(1.0, caster.ability_value("Duration"))
    shield = caster.ability_value("InitialShield") * (caster.ap / 100.0) \
        + caster.ability_value("ShieldPerProc") * (caster.ap / 100.0) * duration
    ctx.shield_unit(caster, shield)  # approx: initial + per-second shield summed
    per_proc = caster.ability_value("DamagePerProc") * (caster.ap / 100.0)
    total = per_proc * duration
    for e in ctx.enemies_in_radius(caster, 1):
        ctx.deal_magic(caster, e, total)


def _pantheon(caster, allies, enemies, ctx) -> None:
    # Advanced Defences: gain shield (%maxHP + AP), then deal physical/sec to a cone of enemies.
    shield = caster.ability_value("PercentHealthShield") * caster.max_hp \
        + caster.ability_value("APShield") * (caster.ap / 100.0)
    ctx.shield_unit(caster, shield)
    duration = max(1.0, caster.ability_value("Duration"))
    per_sec = caster.ability_value("TrueDamagePerSecond")
    total = per_sec * duration
    for e in ctx.enemies_in_radius(caster, 2):  # approx: damage-over-time cone collapsed
        ctx.deal_true(caster, e, total)


def _riven(caster, allies, enemies, ctx) -> None:
    # Time Warp: dash + gain shield, then slash adjacent enemies (adaptive AD/AP physical).
    ctx.shield_unit(caster, caster.ability_value("Shield"))
    amount = caster.ability_value("Damage") * (caster.ad / 100.0 + caster.ap / 100.0)
    for e in ctx.enemies_in_radius(caster, 1):  # approx: dash slash around landing hex
        ctx.deal_physical(caster, e, amount)
    # approx: third cast launches a damaging wave in a cone
    wave = caster.ability_value("WaveDamage") * (caster.ad / 100.0)
    if wave > 0:
        target = ctx.target_of(caster)
        if target is not None:
            ctx.deal_physical(caster, target, wave)


def _teemo(caster, allies, enemies, ctx) -> None:
    # Double Time: gain attack speed steroid, and hit target with bonus + poison magic damage.
    ctx.buff_attack_speed(caster, caster.ability_value("AttackSpeed"))
    target = ctx.target_of(caster)
    if target is None:
        return
    amount = caster.ability_value("HitDamage") * (caster.ap / 100.0) \
        + caster.ability_value("MagicDamage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, amount)  # approx: hit + stacking poison damage merged


def _xayah(caster, allies, enemies, ctx) -> None:
    # Stellar Ricochet: gain attack speed, then recall feathers for physical damage to closest enemies.
    ctx.buff_attack_speed(caster, caster.ability_value("AttackSpeed"))
    amount = caster.ability_value("ADDamage") * (caster.ad / 100.0) \
        + caster.ability_value("APDamage") * (caster.ap / 100.0)
    target = ctx.target_of(caster)
    targets = max(1, int(caster.ability_value("RecallFeatherTargets", 1)))
    bonus = caster.ability_value("PrimaryTargetBonusDamage") * (caster.ad / 100.0)
    living = ctx.living_enemies(caster)
    if not living:
        return
    # approx: feathers recalled split across the closest enemies
    for e in living[:targets]:
        dmg = amount + (bonus if e is target else 0.0)
        ctx.deal_physical(caster, e, dmg)


REGISTRY = {
    "TFT17_AurelionSol": _aurelionsol,
    "TFT17_Caitlyn": _caitlyn,
    "TFT17_Ezreal": _ezreal,
    "TFT17_Graves": _graves,
    "TFT17_Jinx": _jinx,
    "TFT17_Lissandra": _lissandra,
    "TFT17_Mordekaiser": _mordekaiser,
    "TFT17_Pantheon": _pantheon,
    "TFT17_Riven": _riven,
    "TFT17_Teemo": _teemo,
    "TFT17_Xayah": _xayah,
}
