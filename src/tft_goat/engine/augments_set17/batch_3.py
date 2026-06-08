"""Set 17 combat augments — batch_3 (apiName slice keys[3::6]).

Only combat-relevant augments are registered (team buffs / enemy debuffs at combat start);
economy / XP / reroll / loot / item-grant / champion-grant / emblem augments are omitted.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unit import CombatUnit  # noqa: F401


def _tiny_but_deadly(team, enemies, ctx, variables) -> None:
    # Whole team becomes small: gain % Attack Speed.
    frac = variables.get("AttackSpeed", 0.0)
    for u in team:
        ctx.buff_attack_speed(u, frac)


def _cybernetic_implants(team, enemies, ctx, variables) -> None:
    # Allies holding an item gain flat Health and % Attack Damage (approx: all allies).
    hp = variables.get("HP", 0.0)
    ad = variables.get("AD", 0.0)
    for u in team:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_ad(u, ad)


def _makeshift_armor(team, enemies, ctx, variables) -> None:
    # Allies without items gain flat Armor and Magic Resist (approx: all allies).
    r = variables.get("Resists", 0.0)
    for u in team:
        u.armor += r
        u.mr += r


def _best_friends(team, enemies, ctx, variables) -> None:
    # approx: isolated-pair allies gain % Attack Speed and flat Armor (apply to all).
    as_ = variables.get("AS", 0.0)
    armor = variables.get("Armor", 0.0)
    for u in team:
        ctx.buff_attack_speed(u, as_)
        u.armor += armor


def _arcane_viktory(team, enemies, ctx, variables) -> None:
    # approx: timed team-wide stun -> apply one stun to all enemies at combat start.
    dur = variables.get("StunDuration", 0.0)
    if dur <= 0:
        return
    for e in enemies:
        ctx.stun(e, dur)


def _bodyguard_training(team, enemies, ctx, variables) -> None:
    # Allies gain flat Armor and Magic Resist (base; per-level scaling omitted, no level ctx).
    r = variables.get("BaseResistGained", 0.0)
    for u in team:
        u.armor += r
        u.mr += r


def _climb_the_ladder(team, enemies, ctx, variables) -> None:
    # approx: on-death trait-shared buff modeled as a single small AP/AD/Armor/MR grant to team.
    # BonusAP is a percent value (@BonusAP@% Ability Power); BonusAD is already a fraction.
    ap_frac = variables.get("BonusAP", 0.0) / 100.0
    ad = variables.get("BonusAD", 0.0)
    armor = variables.get("BonusArmor", 0.0)
    mr = variables.get("BonusMR", 0.0)
    for u in team:
        u.ap *= 1.0 + ap_frac
        ctx.buff_ad(u, ad)
        u.armor += armor
        u.mr += mr


def _corrosion(team, enemies, ctx, variables) -> None:
    # approx: front-two-rows enemies lose Armor and Magic Resist (apply one tick to all enemies).
    loss = variables.get("ResistLoss", 0.0)
    for e in enemies:
        e.armor = max(0.0, e.armor - loss)
        e.mr = max(0.0, e.mr - loss)


def _find_your_center(team, enemies, ctx, variables) -> None:
    # approx: center-front ally gains % max Health (damage-amp portion omitted).
    if not team:
        return
    frontline = [u for u in team if u.attack_range <= 1]
    target = (frontline or team)[0]  # approx: front-row representative
    bonus = variables.get("BonusHealth", 0.0)
    extra = target.max_hp * bonus
    target.max_hp += extra
    target.hp += extra


def _group_hug(team, enemies, ctx, variables) -> None:
    # approx: adjacency-stacked Armor/MR grant -> flat Armor/MR to all allies.
    r = variables.get("Resists", 0.0)
    for u in team:
        u.armor += r
        u.mr += r


def _legion_of_threes(team, enemies, ctx, variables) -> None:
    # approx: 3-cost/emblem allies gain flat Health and % Attack Speed (apply to all).
    hp = variables.get("HealthAmount", 0.0)
    as_ = variables.get("AS", 0.0)
    for u in team:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_attack_speed(u, as_)


def _may_the_fours(team, enemies, ctx, variables) -> None:
    # approx: 4-cost allies (+Jhin) gain flat Health and % Attack Speed (apply to all).
    hp = variables.get("Health", 0.0)
    as_ = variables.get("AttackSpeed", 0.0)
    for u in team:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_attack_speed(u, as_)


def _trifecta(team, enemies, ctx, variables) -> None:
    # Team-wide % Attack Speed; approx: tier-cost buffed units' HP/AS spread across all allies.
    team_as = variables.get("TeamAttackSpeed", 0.0)
    hp = variables.get("Health", 0.0)
    as_ = variables.get("AttackSpeed", 0.0)
    for u in team:
        ctx.buff_attack_speed(u, team_as)
    for u in team[: int(variables.get("BuffedNumber", 0.0))]:  # approx: first N allies
        u.max_hp += hp
        u.hp += hp
        ctx.buff_attack_speed(u, as_)


def _sword_overflow(team, enemies, ctx, variables) -> None:
    # approx: B.F. Sword bonus % Attack Speed granted to all allies.
    as_ = variables.get("BonusStat", 0.0)
    for u in team:
        ctx.buff_attack_speed(u, as_)


def _electrocharge(team, enemies, ctx, variables) -> None:
    # approx: on-attack AoE magic proc modeled as one burst of magic damage to all enemies.
    dmg = variables.get("Damage2", 0.0) or variables.get("Damage1", 0.0)
    if dmg <= 0 or not team:
        return
    src = team[0]
    for e in enemies:
        ctx.deal_magic(src, e, dmg)


REGISTRY = {
    "TFT11_Augment_TinyButDeadly": _tiny_but_deadly,
    "TFT6_Augment_CyberneticImplants2": _cybernetic_implants,
    "TFT6_Augment_MakeshiftArmor1": _makeshift_armor,
    "TFT7_Augment_BestFriends1": _best_friends,
    "TFT_Augment_ArcaneViktory": _arcane_viktory,
    "TFT_Augment_BodyguardTraining": _bodyguard_training,
    "TFT_Augment_ClimbTheLadder2": _climb_the_ladder,
    "TFT_Augment_Corrosion": _corrosion,
    "TFT_Augment_FindYourCenter": _find_your_center,
    "TFT_Augment_GroupHug1": _group_hug,
    "TFT_Augment_LegionOfThrees": _legion_of_threes,
    "TFT_Augment_MayTheFoursBeWithYou": _may_the_fours,
    "TFT_Augment_Trifecta2": _trifecta,
    "TFT_Augment_SwordOverflow": _sword_overflow,
    "TFT6_Augment_Electrocharge2": _electrocharge,
}
