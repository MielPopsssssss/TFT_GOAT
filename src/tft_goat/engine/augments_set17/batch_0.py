"""Augment combat logic, batch 0 (slice keys[0::6]).

Only augments with a direct combat effect on the holder's own units are registered.
Economy / loot / item-grant / emblem augments are intentionally omitted (no-op).
Each function is applied once at combat start with the augment's real numeric values.
"""

from __future__ import annotations

# Approximation note: TFT has no level/board context here, so per-level and
# per-item augments use a conservative fixed multiplier (documented inline).


def _ahri_boon(team, enemies, ctx, variables) -> None:
    # "team gains @ADAPPerLevel@% AD and AP per level" (effects ADAPPerLevel=2 => 2%/level)
    if not team:
        return
    per = variables.get("ADAPPerLevel", 0.0) / 100.0
    frac = per * 9  # approx: assume max level 9
    for u in team:
        ctx.buff_ad(u, frac)
        u.ap *= 1.0 + frac


def _evelynn_boon(team, enemies, ctx, variables) -> None:
    # "team gains @Durability*100@% Durability" -> approx as effective-HP gain
    if not team:
        return
    dur = variables.get("Durability", 0.0)  # 0.10 fraction
    for u in team:  # approx: durability ~= proportional max HP increase
        gain = u.max_hp * dur
        u.max_hp += gain
        u.hp += gain


def _kayle_boon(team, enemies, ctx, variables) -> None:
    # "for each unique completed item: team gains @Health@ HP, @AD*100@% AD, @AP@% AP"
    # effects: Health=10 (flat), AD=0.01 (fraction), AP=1.0 (PERCENT, not flat)
    if not team:
        return
    items = 3  # approx: typical mid-game completed unique item count
    hp = variables.get("Health", 0.0) * items
    ad = variables.get("AD", 0.0) * items  # fraction (0.01 = +1% per item)
    ap_frac = variables.get("AP", 0.0) / 100.0 * items  # @AP@% -> percent AP
    for u in team:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_ad(u, ad)
        u.ap *= 1.0 + ap_frac


def _varus_boon(team, enemies, ctx, variables) -> None:
    # "team gains @Health@ health for each total star level in your army"
    if not team:
        return
    total_stars = sum(u.star for u in team)  # approx: living team star levels
    hp = variables.get("Health", 0.0) * total_stars
    for u in team:
        u.max_hp += hp
        u.hp += hp


def _exiles_ii(team, enemies, ctx, variables) -> None:
    # "champions with no adjacent ally gain @MaxHealthShield@% max HP shield"
    if not team:
        return
    pct = variables.get("MaxHealthShield", 0.0) / 100.0
    # approx: shield the most isolated units (corners) -> here, backline + any solo
    iso = [u for u in team if u.attack_range > 1] or team
    for u in iso:
        ctx.shield_unit(u, u.max_hp * pct)


def _second_wind_ii(team, enemies, ctx, variables) -> None:
    # "after delay, team heals @HealPercent@% of their missing Health"
    if not team:
        return
    pct = variables.get("HealPercent", 0.0) / 100.0
    for u in team:  # approx: applied at start on current missing HP
        ctx.heal(u, max(0.0, u.max_hp - u.hp) * pct)


def _ascension(team, enemies, ctx, variables) -> None:
    # "after delay, team gains @DamageAmp@% Damage Amp" -> approx as AD buff
    if not team:
        return
    amp = variables.get("DamageAmp", 0.0) / 100.0
    for u in team:  # approx: damage amp ~= offensive (AD + AP) increase
        ctx.buff_ad(u, amp)
        u.ap *= 1.0 + amp


def _charge_transfer_i(team, enemies, ctx, variables) -> None:
    # "team gains @DamageAmp@% Damage Amp" -> approx as AD/AP buff
    if not team:
        return
    amp = variables.get("DamageAmp", 0.0) / 100.0
    for u in team:  # approx: damage amp ~= offensive increase
        ctx.buff_ad(u, amp)
        u.ap *= 1.0 + amp


def _kahunahuna(team, enemies, ctx, variables) -> None:
    # "every Nth attack deals @PercentAD*100@% bonus true damage" -> approx steady AD%
    if not team:
        return
    n = variables.get("NumAttacks", 5.0) or 5.0
    pct = variables.get("PercentAD", 0.0)  # fraction of AD
    frac = pct / n  # approx: amortize the burst over the attack cycle
    for u in team:
        ctx.buff_ad(u, frac)


def _retribution(team, enemies, ctx, variables) -> None:
    # "allies with Hand of Justice gain @CritChance*100@% Crit Chance" -> approx team-wide
    if not team:
        return
    crit = variables.get("CritChance", 0.0)  # 0.15 fraction
    for u in team:  # approx: granted team-wide (item holders unknown here)
        u.crit_chance += crit


def _blood_offering(team, enemies, ctx, variables) -> None:
    # combat start: Bloodthirster holders lose HP%, gain HP% shield and @BonusAD*100@% AD
    if not team:
        return
    loss = variables.get("HPLossPercent", 0.0)
    shield = variables.get("HPShieldPercent", 0.0)
    ad = variables.get("BonusAD", 0.0)
    for u in team:  # approx: applied team-wide (item holders unknown here)
        u.hp = max(1.0, u.hp - u.max_hp * loss)
        ctx.shield_unit(u, u.max_hp * shield)
        ctx.buff_ad(u, ad)


def _misfits(team, enemies, ctx, variables) -> None:
    # "team gains @Health@ Health for each active Unique trait" -> approx a couple uniques
    if not team:
        return
    uniques = 2  # approx: typical unique-trait count on a board
    hp = variables.get("Health", 0.0) * uniques
    for u in team:
        u.max_hp += hp
        u.hp += hp


def _crash_test_dummies(team, enemies, ctx, variables) -> None:
    # "Combat start: Training Dummies launch at a group of enemies and Stun them"
    # effects: NumDummies=2, SearchRange=4, Stun=1.0s. approx: each dummy stuns the
    # enemies clustered around an anchor enemy (the dummies are summoned, not in team).
    if not team or not enemies:
        return
    num = int(variables.get("NumDummies", 0.0))
    dur = variables.get("Stun", 0.0)
    if num <= 0 or dur <= 0.0:
        return
    src = team[0]  # any ally as a reference point for the enemy query
    foes = ctx.living_enemies(src) or enemies
    # approx: each of the NumDummies dummies stuns the closest enemy to the
    # holder's frontline; with small boards this covers a front cluster.
    foes = sorted(foes, key=lambda e: e.pos)
    for e in foes[:num]:
        ctx.stun(e, dur)


def _two_tanky(team, enemies, ctx, variables) -> None:
    # "field exactly 2 copies of a champion -> both gain @BonusHealth@ Health"
    if not team:
        return
    hp = variables.get("BonusHealth", 0.0)
    counts: dict[str, int] = {}
    for u in team:
        counts[u.champion_api] = counts.get(u.champion_api, 0) + 1
    for u in team:  # only the exact-pair champions get the health
        if counts.get(u.champion_api) == 2:
            u.max_hp += hp
            u.hp += hp


REGISTRY = {
    "TFT10_Augment_CrashTestDummies": _crash_test_dummies,
    "TFT17_Augment_AhriGodAugment": _ahri_boon,
    "TFT17_Augment_EvelynnGodAugment": _evelynn_boon,
    "TFT17_Augment_KayleGodAugment": _kayle_boon,
    "TFT17_Augment_VarusGodAugment_BoonOfStars": _varus_boon,
    "TFT6_Augment_Distancing2": _exiles_ii,
    "TFT6_Augment_SecondWind2": _second_wind_ii,
    "TFT9_Augment_Commander_Ascension": _ascension,
    "TFT_Augment_ChargeTransfer1": _charge_transfer_i,
    "TFT_Augment_FuriousBlows": _kahunahuna,
    "TFT_Augment_Retribution": _retribution,
    "TFT_Augment_TheDarkinBlade": _blood_offering,
    "TFT_Augment_Misfits": _misfits,
    "TFT_Augment_TwoTanky": _two_tanky,
}
