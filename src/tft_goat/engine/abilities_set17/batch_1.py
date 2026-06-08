"""Set 17 champion ability logic — batch 1 (12 champions)."""

from __future__ import annotations


def _aatrox(caster, allies, enemies, ctx) -> None:
    # Stellar Slash: heal (%maxHP + AP), then physical damage to target (AD + %armor).
    heal = caster.max_hp * caster.ability_value("HealHP") + caster.ability_value("HealAP") * (caster.ap / 100.0)
    ctx.heal(caster, heal)
    target = ctx.target_of(caster)
    if target is None:
        return
    amount = caster.ability_value("DamageAD") * (caster.ad / 100.0 + 1.0) \
        + caster.ability_value("DamagePercentArmor") * caster.armor
    ctx.deal_physical(caster, target, amount)


def _blitzcrank(caster, allies, enemies, ctx) -> None:
    # Marked for Death-style: uppercut highest-HP target + AoE explosion (magic, AP scaled).
    target = ctx.highest_hp_enemy(caster) or ctx.target_of(caster)
    if target is None:
        return
    uppercut = caster.ability_value("UppercutDamage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, uppercut)
    explosion = caster.ability_value("ExplosionDamage") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(target, 1):  # approx: disco-ball crash AoE around target
        ctx.deal_magic(caster, e, explosion)


def _diana(caster, allies, enemies, ctx) -> None:
    # Active: gain shield, then orbiting orbs deal magic damage to nearby enemies.
    shield = caster.ability_value("Shield") + caster.ability_value("ShieldPercent") * caster.max_hp
    if shield <= 0:
        shield = caster.ability_value("ShieldAP", 0.0) * (caster.ap / 100.0)
    ctx.shield_unit(caster, shield)
    orb = caster.ability_value("BaseDamage") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(caster, 2):  # approx: 3 encircling orbs hitting passing enemies
        ctx.deal_magic(caster, e, orb)


def _gnar(caster, allies, enemies, ctx) -> None:
    # Boomerang: physical damage (AD + AP) to target, piercing two hexes past first hit.
    target = ctx.target_of(caster)
    if target is None:
        return
    amount = caster.ability_value("DamageAD") * (caster.ad / 100.0) \
        + caster.ability_value("DamageAP") * (caster.ap / 100.0)
    ctx.deal_physical(caster, target, amount)
    # approx: boomerang travels through line; hit one extra enemy at reduced damage
    reduced = amount * (1.0 - caster.ability_value("DamageReductionPerHit"))
    for e in ctx.enemies_in_radius(target, 1):
        if e is not target:
            ctx.deal_physical(caster, e, reduced)
            break


def _jax(caster, allies, enemies, ctx) -> None:
    # Defensive stance: shield self, then strike + stun nearby enemies (magic, armor+MR scaled).
    ctx.shield_unit(caster, caster.ability_value("ShieldAP") * (caster.ap / 100.0))
    scale = caster.ability_value("ArmorMRScale")
    amount = scale * (caster.armor + caster.mr)
    stun = caster.ability_value("StunDuration")
    radius = int(caster.ability_value("AttackRadius", 1)) or 1
    for e in ctx.enemies_in_radius(caster, radius):
        ctx.deal_magic(caster, e, amount)
        ctx.stun(e, stun)


def _leblanc(caster, allies, enemies, ctx) -> None:
    # Active: clones attack alongside; their final bolt deals magic damage to target.
    target = ctx.target_of(caster)
    if target is None:
        return
    clones = max(1, int(caster.ability_value("NumClones", 1)))
    bolt = caster.ability_value("BoltDamage") * (caster.ap / 100.0)
    # approx: clones' bolt volley collapsed into one nuke scaled by clone count
    ctx.deal_magic(caster, target, bolt * clones)


def _milio(caster, allies, enemies, ctx) -> None:
    # Kick a ball: magic damage to target, then bounce to a second enemy.
    target = ctx.target_of(caster)
    if target is None:
        return
    ctx.deal_magic(caster, target, caster.ability_value("Damage") * (caster.ap / 100.0))
    bounce = caster.ability_value("BounceDamage") * (caster.ap / 100.0)
    for e in ctx.living_enemies(caster):  # approx: ball bounces to a new target
        if e is not target:
            ctx.deal_magic(caster, e, bounce)
            break


def _nunu(caster, allies, enemies, ctx) -> None:
    # Shield self, astrolabe crashes (AoE magic) + followup, knocking up enemies hit.
    ctx.shield_unit(caster, caster.ability_value("Shield") * (caster.ap / 100.0))
    initial = caster.ability_value("InitialDamage") * (caster.ap / 100.0)
    followup = caster.ability_value("FollowupDamage") * (caster.ap / 100.0)
    stun = caster.ability_value("StunDuration")
    target = ctx.target_of(caster)
    center = target if target is not None else caster
    for e in ctx.enemies_in_radius(center, 2):
        ctx.deal_magic(caster, e, initial + followup)  # approx: astrolabe sweep merged
        ctx.stun(e, stun)


def _reksai(caster, allies, enemies, ctx) -> None:
    # Heal (%maxHP + AP), then knock up adjacent enemies and deal magic damage.
    heal = caster.max_hp * caster.ability_value("PercentMaximumHealthHealing") \
        + caster.ability_value("APHealing") * (caster.ap / 100.0)
    ctx.heal(caster, heal)
    amount = caster.ability_value("Damage") * (caster.ap / 100.0)
    stun = caster.ability_value("StunDuration")
    for e in ctx.enemies_in_radius(caster, 1):
        ctx.deal_magic(caster, e, amount)
        ctx.stun(e, stun)  # approx: brief knock-up


def _tahmkench(caster, allies, enemies, ctx) -> None:
    # Heal (%maxHP + AP), then tongue-lash all enemies within 2 hexes (magic, AP+HP scaled).
    heal = caster.max_hp * caster.ability_value("HealHP") + caster.ability_value("HealAP") * (caster.ap / 100.0)
    ctx.heal(caster, heal)
    amount = caster.ability_value("DamageAP") * (caster.ap / 100.0) \
        + caster.ability_value("DamageHP") * caster.max_hp
    for e in ctx.enemies_in_radius(caster, 2):
        ctx.deal_magic(caster, e, amount)


def _vex(caster, allies, enemies, ctx) -> None:
    # Active: Shadow launches N empowered strikes (magic, AP scaled) at nearby enemies.
    strikes = max(1, int(caster.ability_value("NumActiveStrikes", 1)))
    amount = caster.ability_value("ShadowHandMagicDamage") * (caster.ap / 100.0)
    living = ctx.living_enemies(caster)
    if not living:
        return
    # approx: distribute the empowered strikes, focusing the primary target
    target = ctx.target_of(caster) or living[0]
    for i in range(strikes):
        victim = target if i == 0 else living[i % len(living)]
        ctx.deal_magic(caster, victim, amount)


def _blue_golem(caster, allies, enemies, ctx) -> None:
    # PvE monster (Golem Smash) — not a player champion ability; no-op.
    pass


REGISTRY = {
    "TFT17_Aatrox": _aatrox,
    "TFT17_Blitzcrank": _blitzcrank,
    "TFT17_Diana": _diana,
    "TFT17_Gnar": _gnar,
    "TFT17_Jax": _jax,
    "TFT17_Leblanc": _leblanc,
    "TFT17_Milio": _milio,
    "TFT17_Nunu": _nunu,
    "TFT17_RekSai": _reksai,
    "TFT17_TahmKench": _tahmkench,
    "TFT17_Vex": _vex,
    "TFT_BlueGolem": _blue_golem,
}
