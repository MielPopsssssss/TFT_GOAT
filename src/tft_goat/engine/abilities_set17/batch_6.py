"""Set 17 champion ability logic — batch 6 (11 entries)."""

from __future__ import annotations


def _belveth(caster, allies, enemies, ctx) -> None:
    # Flurry of slashes at current target: BaseNumSlashes hits, each AD + AP physical damage.
    target = ctx.target_of(caster)
    if target is None:
        return
    per_hit = caster.ability_value("ADDamage") * (caster.ad / 100.0) \
        + caster.ability_value("APDamage") * (caster.ap / 100.0)
    slashes = int(caster.ability_value("BaseNumSlashes", 12.0)) or 12
    for _ in range(slashes):
        if not getattr(target, "hp", 0) > 0:
            break
        ctx.deal_physical(caster, target, per_hit)


def _darkstar_fakeunit(caster, allies, enemies, ctx) -> None:
    # No-op: PvE/fake unit (miniature black hole), no offensive ability.
    pass


def _galio(caster, allies, enemies, ctx) -> None:
    # Defensive stance: heal over time, then shockwave physical damage (armor+MR) in HexRange.
    ctx.heal(caster, caster.ability_value("Heal") * (caster.ap / 100.0))
    scale = caster.ability_value("ARMARScaling")
    amount = scale * (caster.armor + caster.mr)
    radius = int(caster.ability_value("HexRange", 2.0)) or 2
    for e in ctx.enemies_in_radius(caster, radius):  # approx: shockwave AoE on stance end
        ctx.deal_physical(caster, e, amount)


def _ivernminion(caster, allies, enemies, ctx) -> None:
    # No-op: PvE/minion summon (Ivern's Daisy meep), no standalone cast here.
    pass


def _kindred(caster, allies, enemies, ctx) -> None:
    # Active: fire arrows at nearest NumTargets enemies, each AD + AP physical damage.
    if not enemies:
        return
    per_hit = caster.ability_value("ADDamage") * (caster.ad / 100.0) \
        + caster.ability_value("APDamage") * (caster.ap / 100.0)
    num = int(caster.ability_value("NumTargets", 3.0)) or 3
    primary = ctx.target_of(caster)
    targets = []
    if primary is not None:
        targets.append(primary)
    for e in enemies:
        if e not in targets:
            targets.append(e)
        if len(targets) >= num:
            break
    for e in targets[:num]:
        ctx.deal_physical(caster, e, per_hit)


def _masteryi(caster, allies, enemies, ctx) -> None:
    # Active: Psi-State steroid (attack speed + AD), then psychic strikes (AD + AP) on nearby enemies.
    ctx.buff_attack_speed(caster, caster.ability_value("AttackSpeed"))
    ctx.buff_ad(caster, caster.ability_value("Omnivamp"))  # approx: omnivamp -> AD steroid
    strike = caster.ability_value("DamageAD") * (caster.ad / 100.0) \
        + caster.ability_value("DamageAP") * (caster.ap / 100.0)
    target = ctx.target_of(caster)
    if target is not None:
        ctx.deal_physical(caster, target, strike)
    for e in ctx.enemies_in_radius(caster, 2):  # approx: projections at random nearby enemies
        if e is not target:
            ctx.deal_physical(caster, e, strike)


def _nasus(caster, allies, enemies, ctx) -> None:
    # Transform: gain max-HP shield, then magic damage (%maxHP + AP) to adjacent enemies.
    ctx.shield_unit(caster, caster.ability_value("MaxHealth"))  # approx: temp max-HP gain as shield
    amount = caster.ability_value("DamageHealth") * caster.max_hp \
        + caster.ability_value("DamageAP") * (caster.ap / 100.0)
    for e in ctx.enemies_in_radius(caster, 1):  # adjacent enemies, damage each second
        ctx.deal_magic(caster, e, amount)


def _rammus(caster, allies, enemies, ctx) -> None:
    # Gain shield, then strike a 3-hex line dealing magic damage (AP + armor).
    ctx.shield_unit(caster, caster.ability_value("ShieldAP") * (caster.ap / 100.0))
    amount = caster.ability_value("DamageAP") * (caster.ap / 100.0) \
        + caster.ability_value("DamageArmor") * caster.armor
    target = ctx.target_of(caster)
    if target is not None:
        ctx.deal_magic(caster, target, amount)
    for e in ctx.enemies_in_radius(caster, 1):  # approx: three-hex line strike
        if e is not target:
            ctx.deal_magic(caster, e, amount)


def _sona(caster, allies, enemies, ctx) -> None:
    # Hurl magnetic debris at nearest target for magic damage. Le slam (rip de TOUS les
    # debris + stun) n'arrive que « every @NumCasts@ casts » -> AMORTI : slam/NumCasts de
    # dégâts par cast, stun rng-gaté à 1/NumCasts (avant : slam entier + stun à CHAQUE
    # cast = ~3-4x sur-tunée, win rate saturé à 1.00 dans realism_vs_datatft).
    target = ctx.target_of(caster) or ctx.lowest_hp_enemy(caster)
    if target is None:
        return
    ap = caster.ap / 100.0
    ctx.deal_magic(caster, target, caster.ability_value("DebrisDamage") * ap)
    n = max(1.0, caster.ability_value("NumCasts", 5.0))
    slam = caster.ability_value("SlamDamage") * ap / n
    if slam > 0:
        ctx.deal_magic(caster, target, slam)
        if ctx.rng.random() < 1.0 / n:  # le vrai slam ne tombe qu'un cast sur NumCasts
            ctx.stun(target, caster.ability_value("StunDuration", 1.0))


def _veigar(caster, allies, enemies, ctx) -> None:
    # Meepteor: big single-target magic nuke (AP), plus mini meteors on nearby enemies.
    target = ctx.target_of(caster) or ctx.highest_hp_enemy(caster)
    if target is None:
        return
    main = caster.ability_value("Damage") * (caster.ap / 100.0)
    ctx.deal_magic(caster, target, main)
    mini = caster.ability_value("MiniDamage") * (caster.ap / 100.0)  # approx: mini meepteors on nearby
    for e in ctx.enemies_around(caster, target, 1):
        if e is not target:
            ctx.deal_magic(caster, e, mini)


def _slime_crab(caster, allies, enemies, ctx) -> None:
    # No-op: PvE monster (slime crab), only passively dashes around the board.
    pass


REGISTRY = {
    "TFT17_Belveth": _belveth,
    "TFT17_DarkStar_FakeUnit": _darkstar_fakeunit,
    "TFT17_Galio": _galio,
    "TFT17_IvernMinion": _ivernminion,
    "TFT17_Kindred": _kindred,
    "TFT17_MasterYi": _masteryi,
    "TFT17_Nasus": _nasus,
    "TFT17_Rammus": _rammus,
    "TFT17_Sona": _sona,
    "TFT17_Veigar": _veigar,
    "TFT9_SLIME_Crab": _slime_crab,
}
