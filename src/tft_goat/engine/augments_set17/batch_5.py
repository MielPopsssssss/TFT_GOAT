"""Set 17 combat augments - batch 5 (keys[5::6]).

Only combat-affecting augments are registered (stat buffs / shields / heals at combat start).
Economy / loot / XP / item-grant / unit-grant / pure-emblem augments are omitted (no-op).
"""

from __future__ import annotations

from ..unit import CombatUnit  # noqa: F401  (type hint only)


def _tour_of_the_galaxy(team, enemies, ctx, variables) -> None:
    # approx: Voyagers gain HP/AD/AP; applied to whole team (trait membership unknown here).
    hp = variables.get("HP", 0.0)
    ad = variables.get("AD", 0.0)  # fraction (desc: @AD*100@%)
    ap = variables.get("AP", 0.0) / 100.0  # percent (desc: @AP@%)
    for u in team:
        u.max_hp += hp
        u.hp += hp
        u.ad *= 1.0 + ad
        u.ap += u.ap * ap


def _distancing(team, enemies, ctx, variables) -> None:
    # approx: units with no adjacent ally get a % max-HP shield (treat frontline as adjacent-clustered).
    frac = variables.get("MaxHealthShield", 0.0) / 100.0
    backline = [u for u in team if u.attack_range > 1]
    for u in (backline or team):
        ctx.shield_unit(u, u.max_hp * frac)


def _second_wind(team, enemies, ctx, variables) -> None:
    # approx: after a delay the team heals % of missing HP (applied once at combat start).
    pct = variables.get("HealPercent", 0.0) / 100.0
    for u in team:
        ctx.heal(u, (u.max_hp - u.hp) * pct)


def _you_have_my_bow(team, enemies, ctx, variables) -> None:
    # Team gains AS%.
    frac = variables.get("AS", 0.0) / 100.0
    for u in team:
        ctx.buff_attack_speed(u, frac)


def _awakened_soul(team, enemies, ctx, variables) -> None:
    # approx: AD/AP per second for MaxStacks seconds, applied as the full stacked total at start.
    per = variables.get("StatsPerSecond", 0.0) / 100.0
    stacks = variables.get("MaxStacks", 0.0)
    total = per * stacks
    for u in team:
        u.ad *= 1.0 + total
        u.ap += u.ap * total


def _early_learning(team, enemies, ctx, variables) -> None:
    # Team gains AD & AP %.
    frac = variables.get("NumADAP", 0.0) / 100.0
    for u in team:
        u.ad *= 1.0 + frac
        u.ap += u.ap * frac


def _glass_cannon(team, enemies, ctx, variables) -> None:
    # approx: back-row allies start at Health% HP (damage-amp portion unmodeled).
    frac = variables.get("Health", 1.0)
    backline = [u for u in team if u.attack_range > 1]
    for u in (backline or team):
        u.hp = u.max_hp * frac


def _guardbreaker_spirit(team, enemies, ctx, variables) -> None:
    # Team gains crit strike chance (fraction).
    crit = variables.get("CritChance", 0.0)
    for u in team:
        u.crit_chance += crit


def _hold_the_line(team, enemies, ctx, variables) -> None:
    # approx: back-2-rows gain AP/AD per front-row ally; use frontline count for whole backline.
    front = [u for u in team if u.attack_range <= 1]
    back = [u for u in team if u.attack_range > 1]
    ap = variables.get("AP", 0.0) / 100.0 * len(front)  # percent per front ally (desc: @AP@%)
    ad = variables.get("AD", 0.0) * len(front)  # fraction per front ally (desc: @AD*100@%)
    for u in back:
        u.ap += u.ap * ap
        u.ad *= 1.0 + ad


def _item_spirit_visage(team, enemies, ctx, variables) -> None:
    # approx: periodic missing-HP heal modeled as a single combat-start heal.
    pct = variables.get("Missinghealth", variables.get("MissingHealth", 0.0)) / 100.0
    for u in team:
        ctx.heal(u, (u.max_hp - u.hp) * pct)


def _barons_lair(team, enemies, ctx, variables) -> None:
    # approx: ramping AD/AP per second after StartSeconds, applied as one early-game tick.
    frac = variables.get("Stats", 0.0) / 100.0
    for u in team:
        u.ad *= 1.0 + frac
        u.ap += u.ap * frac


def _healing_orbs(team, enemies, ctx, variables) -> None:
    # approx: on enemy death the nearest ally is healed a flat amount; on-death trigger
    # modeled as a single combat-start heal to the lowest-HP ally.
    heal = variables.get("Heal", 0.0)
    if heal <= 0.0 or not team:
        return
    target = min(team, key=lambda u: u.hp)
    ctx.heal(target, heal)


REGISTRY = {
    "TFT17_Augment_TourOfTheGalaxy": _tour_of_the_galaxy,
    "TFT6_Augment_Distancing": _distancing,
    "TFT6_Augment_SecondWind1": _second_wind,
    "TFT9_Augment_YouHaveMyBow": _you_have_my_bow,
    "TFT_Augment_AwakenedSoul": _awakened_soul,
    "TFT_Augment_EarlyLearning": _early_learning,
    "TFT_Augment_GlassCannonII": _glass_cannon,
    "TFT_Augment_GuardbreakerSpirit": _guardbreaker_spirit,
    "TFT_Augment_HoldTheLine": _hold_the_line,
    "TFT_Augment_ItemSpiritVisage": _item_spirit_visage,
    "TFT_Augment_TheBaronsLair": _barons_lair,
    "TFT9_Augment_HealingOrbsI": _healing_orbs,
}
