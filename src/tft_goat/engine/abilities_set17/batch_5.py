"""Set 17 champion abilities - batch 5 (11 champions)."""

from __future__ import annotations

from ..unit import CombatUnit


def _ap(caster: CombatUnit, var: str) -> float:
    return caster.ability_value(var) * (caster.ap / 100.0)


def _bard(caster, allies, enemies, ctx) -> None:
    # Flying saucer over target deals magic damage per second (apply burst on target + nearby).
    tgt = ctx.target_of(caster)
    if tgt is None:
        return
    dur = caster.ability_value("Duration", default=4.0)
    ctx.deal_magic(caster, tgt, _ap(caster, "DamagePerSecond") * dur)
    for e in ctx.enemies_in_radius(caster, 1):
        if e is not tgt:
            ctx.deal_magic(caster, e, _ap(caster, "SplitDamagePerSecond") * dur)


def _corki(caster, allies, enemies, ctx) -> None:
    # Strafe: missiles split between target and enemies within 2 hexes (AD+AP per missile).
    per = caster.ad * (caster.ability_value("MissileAD") / 100.0) + _ap(caster, "MissileAP")
    targets = ctx.enemies_in_radius(caster, 2)
    if not targets:
        return
    for e in targets:
        ctx.deal_physical(caster, e, per * caster.ability_value("BaseMissiles") / len(targets))


def _fizz(caster, allies, enemies, ctx) -> None:
    # Assassin dash through target for magic burst; adjacent enemies take 50%.
    tgt = ctx.target_of(caster) or ctx.lowest_hp_enemy(caster)
    if tgt is None:
        return
    dmg = _ap(caster, "DashDamage") + _ap(caster, "BiteDamageAP")
    ctx.deal_magic(caster, tgt, dmg)
    sec = caster.ability_value("SecondaryDamage", default=0.5)
    for e in ctx.enemies_in_radius(caster, 1):
        if e is not tgt:
            ctx.deal_magic(caster, e, dmg * sec)


def _illaoi(caster, allies, enemies, ctx) -> None:
    # Tank: gain shield, true-drain nearest enemies, then magic slam in 2 hexes.
    ctx.shield_unit(caster, _ap(caster, "Shield"))
    drain = _ap(caster, "HealthDrain")
    num = int(caster.ability_value("NumEnemies", default=3.0))
    near = sorted(ctx.living_enemies(caster), key=lambda e: e.hp)[:num]
    for e in near:
        ctx.deal_true(caster, e, drain)
    ctx.heal(caster, drain * len(near))
    for e in ctx.enemies_in_radius(caster, 2):
        ctx.deal_magic(caster, e, _ap(caster, "Damage"))


def _karma(caster, allies, enemies, ctx) -> None:
    # Black hole: magic damage split among target + closest enemies, extra on target.
    tgt = ctx.target_of(caster)
    if tgt is None:
        return
    num = int(caster.ability_value("NumEnemies", default=2.0))
    group = sorted(ctx.living_enemies(caster), key=lambda e: e.hp)[:num]
    if tgt not in group:
        group = [tgt] + group[: max(0, num - 1)]
    split = _ap(caster, "Damage") / max(1, len(group))
    for e in group:
        ctx.deal_magic(caster, e, split)
    ctx.deal_magic(caster, tgt, _ap(caster, "SecondaryDamage"))


def _maokai(caster, allies, enemies, ctx) -> None:
    # Tank: X of vines on target deals magic damage and stuns (line approx via radius 1).
    tgt = ctx.target_of(caster)
    if tgt is None:
        return
    dmg = _ap(caster, "Damage")
    dur = caster.ability_value("StunDuration", default=1.5)
    ctx.deal_magic(caster, tgt, dmg)
    ctx.stun(tgt, dur)
    for e in ctx.enemies_in_radius(caster, 1):
        if e is not tgt:
            ctx.deal_magic(caster, e, dmg)
            ctx.stun(e, dur)


def _nami(caster, allies, enemies, ctx) -> None:
    # Disco bubble: magic split in 1 hex radius, plus bounce globs to nearby enemies.
    tgt = ctx.target_of(caster)
    if tgt is None:
        return
    in_r = ctx.enemies_in_radius(caster, 1) or [tgt]
    for e in in_r:
        ctx.deal_magic(caster, e, _ap(caster, "Damage") / len(in_r))
    num = int(caster.ability_value("NumProjectiles", default=3.0))
    for e in ctx.living_enemies(caster)[:num]:
        ctx.deal_magic(caster, e, _ap(caster, "FirstBounceDamage"))


def _pyke(caster, allies, enemies, ctx) -> None:
    # Assassin: harpoon furthest enemy then cleave - physical burst on target + AoE.
    tgt = ctx.highest_hp_enemy(caster) or ctx.target_of(caster)
    if tgt is None:
        return
    ctx.deal_physical(caster, tgt, _ap(caster, "SpearDamage"))
    ctx.deal_physical(caster, tgt, caster.ad * (caster.ability_value("TargetDamage") / 100.0))
    aoe = _ap(caster, "AoEDamage")
    for e in ctx.enemies_in_radius(caster, 1):
        if e is not tgt:
            ctx.deal_physical(caster, e, aoe)


def _shen(caster, allies, enemies, ctx) -> None:
    # Tank: gain shield (HP+AP), buff attack speed, slow nearest enemy (approx via stun).
    ctx.shield_unit(caster, caster.max_hp * caster.ability_value("ShieldHP") + _ap(caster, "ShieldAP"))
    ctx.buff_attack_speed(caster, caster.ability_value("BonusAS", default=0.8))
    tgt = ctx.target_of(caster)
    if tgt is not None:
        ctx.stun(tgt, caster.ability_value("BuffDebuffDuration", default=3.0) * 0.3)  # approx: attack speed slow


def _urgot(caster, allies, enemies, ctx) -> None:
    # Ranged: shotgun blast cone (AD scaled) + self shield.
    ctx.shield_unit(caster, caster.ability_value("ShieldAmount"))
    dmg = caster.ad * (caster.ability_value("ShotgunDamage") / 100.0)
    targets = ctx.enemies_in_radius(caster, 2)
    if not targets:
        tgt = ctx.target_of(caster)
        targets = [tgt] if tgt else []
    falloff = caster.ability_value("FalloffPerHex", default=0.3)
    for i, e in enumerate(targets):
        ctx.deal_physical(caster, e, dmg * max(0.0, 1.0 - falloff * i))


def _zoe(caster, allies, enemies, ctx) -> None:
    # Paddle star: magic to first target, secondary to others it passes through, redirects.
    tgt = ctx.target_of(caster)
    if tgt is None:
        return
    redirects = int(caster.ability_value("NumRedirects", default=4.0))
    others = [e for e in ctx.living_enemies(caster) if e is not tgt]
    for _ in range(redirects):
        ctx.deal_magic(caster, tgt, _ap(caster, "Damage"))
        for e in others:
            ctx.deal_magic(caster, e, _ap(caster, "SecondaryDamage"))


REGISTRY = {
    "TFT17_Bard": _bard,
    "TFT17_Corki": _corki,
    "TFT17_Fizz": _fizz,
    "TFT17_Illaoi": _illaoi,
    "TFT17_Karma": _karma,
    "TFT17_Maokai": _maokai,
    "TFT17_Nami": _nami,
    "TFT17_Pyke": _pyke,
    "TFT17_Shen": _shen,
    "TFT17_Urgot": _urgot,
    "TFT17_Zoe": _zoe,
}
