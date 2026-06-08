"""Set 17 combat augments — batch 4 (slice keys[4::6]).

Only combat-relevant augments are registered (stat buffs / shields / heals at combat start);
economy, item-grant, champion-grant, reroll/XP and pure trait-emblem augments are omitted.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unit import CombatUnit  # noqa: F401


def _jeweled_lotus(team, enemies, ctx, variables) -> None:
    # Team gains flat Critical Strike Chance (CritChance is a percent, e.g. 10 -> +0.10).
    crit = variables.get("CritChance", 0.0) / 100.0
    for u in team:
        u.crit_chance += crit


def _greater_jeweled_lotus(team, enemies, ctx, variables) -> None:
    # Team gains Crit Chance (% value) and Crit Damage (fraction added to crit multiplier).
    crit = variables.get("CritChance", 0.0) / 100.0
    crit_dmg = variables.get("CritDamage", 0.0)
    for u in team:
        u.crit_chance += crit
        u.crit_mult += crit_dmg


def _tons_of_stats(team, enemies, ctx, variables) -> None:
    # Team gains flat HP, %AD, %AP, flat Armor, flat MR, %Attack Speed (Mana ignored: not a combat attr).
    hp = variables.get("Health", 0.0)
    ad = variables.get("AttackDamage", 0.0) / 100.0
    ap = variables.get("AbilityPower", 0.0) / 100.0
    armor = variables.get("Armor", 0.0)
    mr = variables.get("MR", 0.0)
    as_ = variables.get("AttackSpeed", 0.0) / 100.0
    for u in team:
        u.max_hp += hp
        u.hp += hp
        u.ad *= 1.0 + ad
        u.ap *= 1.0 + ap
        u.armor += armor
        u.mr += mr
        u.attack_speed *= 1.0 + as_


def _best_friends(team, enemies, ctx, variables) -> None:
    # approx: isolated-pair allies gain %Attack Speed and flat Armor; applied team-wide.
    as_ = variables.get("AS", 0.0)
    armor = variables.get("Armor", 0.0)
    for u in team:
        u.attack_speed *= 1.0 + as_
        u.armor += armor


def _glass_cannon(team, enemies, ctx, variables) -> None:
    # approx: back-row allies start at Health% HP but gain DamageAmp (modeled as +AD/+AP).
    hp_frac = variables.get("Health", 1.0)
    amp = variables.get("DamageAmp", 0.0)
    front = {id(u) for u in team if u.attack_range <= 1}
    for u in team:
        if id(u) in front:
            continue
        u.hp = u.max_hp * hp_frac
        u.ad *= 1.0 + amp
        u.ap *= 1.0 + amp


def _group_hug(team, enemies, ctx, variables) -> None:
    # approx: adjacent allies grant Armor and MR (stacking); applied once per ally team-wide.
    resists = variables.get("Resists", 0.0)
    for u in team:
        u.armor += resists
        u.mr += resists


def _lineup(team, enemies, ctx, variables) -> None:
    # Team gains Armor and MR for each ally starting in the front two rows (approx: frontline count).
    per = variables.get("Resistances", 0.0)
    n = len([u for u in team if u.attack_range <= 1])
    bonus = per * n
    for u in team:
        u.armor += bonus
        u.mr += bonus


def _clockwork_accelerator(team, enemies, ctx, variables) -> None:
    # approx: periodic team Attack Speed gain modeled as a single combat-start application.
    as_ = variables.get("AttackSpeed", 0.0)
    for u in team:
        u.attack_speed *= 1.0 + as_


def _twin_guardians(team, enemies, ctx, variables) -> None:
    # approx: if exactly NumUnits front-row allies, grant them bonus HP, Armor, MR.
    front = [u for u in team if u.attack_range <= 1]
    if len(front) != int(variables.get("NumUnits", 0)):
        return
    hp = variables.get("BonusHealth", 0.0)
    ar = variables.get("BonusAR", 0.0)
    mr = variables.get("BonusMR", 0.0)
    for u in front:
        u.max_hp += hp
        u.hp += hp
        u.armor += ar
        u.mr += mr


def _gargoyle_stoneplate(team, enemies, ctx, variables) -> None:
    # approx: allies alone in their row gain %max HP; modeled as a frontline %max-HP bonus.
    frac = variables.get("HealthIncrease", 0.0)
    for u in team:
        if u.attack_range <= 1:
            bonus = u.max_hp * frac
            u.max_hp += bonus
            u.hp += bonus


def _makeshift_armor(team, enemies, ctx, variables) -> None:
    # approx: allies without items gain Armor and MR; applied to item-less units.
    resists = variables.get("Resists", 0.0)
    for u in team:
        if not u.item_apis:
            u.armor += resists
            u.mr += resists


def _bronze_for_life(team, enemies, ctx, variables) -> None:
    # approx: team gains Armor and MR per bronze trait; one bronze tier assumed (Resists, damage amp ignored).
    resists = variables.get("Resists", 0.0)
    for u in team:
        u.armor += resists
        u.mr += resists


def _no_scout_no_pivot(team, enemies, ctx, variables) -> None:
    # approx: team gains %max HP and %AD/%AP (one post-combat stack applied at start).
    hp = variables.get("HPScale", 0.0)
    ad = variables.get("ADScale", 0.0)
    ap = variables.get("APScale", 0.0) / 100.0
    for u in team:
        bonus = u.max_hp * hp
        u.max_hp += bonus
        u.hp += bonus
        u.ad *= 1.0 + ad
        u.ap *= 1.0 + ap


def _cybernetic_uplink(team, enemies, ctx, variables) -> None:
    # approx: allies holding an item gain flat HP (Mana Regen ignored: not a combat attr).
    hp = variables.get("Health", 0.0)
    for u in team:
        if u.item_apis:
            u.max_hp += hp
            u.hp += hp


def _little_buddies(team, enemies, ctx, variables) -> None:
    # approx: 4/5-cost allies gain flat Health and %Attack Speed per 1/2-cost ally on board;
    # no cost attr available, so applied team-wide (count of low-cost allies unknown).
    hp = variables.get("Health", 0.0)
    as_ = variables.get("AttackSpeed", 0.0)
    for u in team:
        u.max_hp += hp
        u.hp += hp
        u.attack_speed *= 1.0 + as_


def _side_effects(team, enemies, ctx, variables) -> None:
    # approx: periodic %max-HP team heal modeled as a single combat-start heal
    # (heal->magic-damage conversion proc omitted).
    pct = variables.get("HealPct", 0.0)
    for u in team:
        ctx.heal(u, u.max_hp * pct)


REGISTRY = {
    "TFT9_Augment_JeweledLotus": _jeweled_lotus,
    "TFT9_Augment_GreaterJeweledLotus": _greater_jeweled_lotus,
    "TFT9_Augment_TonsOfStats": _tons_of_stats,
    "TFT7_Augment_BestFriends2": _best_friends,
    "TFT_Augment_GlassCannonI": _glass_cannon,
    "TFT_Augment_GroupHug2": _group_hug,
    "TFT_Augment_Lineup": _lineup,
    "TFT_Augment_ClockworkAccelerator": _clockwork_accelerator,
    "TFT_Augment_TwinGuardians": _twin_guardians,
    "TFT_Augment_ItemGargoyleStoneplate": _gargoyle_stoneplate,
    "TFT6_Augment_MakeshiftArmor2": _makeshift_armor,
    "TFT_Augment_BronzeForLife2": _bronze_for_life,
    "TFT_Augment_NoScoutNoPivot": _no_scout_no_pivot,
    "TFT6_Augment_CyberneticUplink2": _cybernetic_uplink,
    "TFT10_Augment_LittleBuddies": _little_buddies,
    "TFT_Augment_SideEffects": _side_effects,
}
