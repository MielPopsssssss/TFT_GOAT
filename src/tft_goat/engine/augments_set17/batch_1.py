"""Set 17 combat augments — batch 1 (slice keys[1::6] of augments_set17.json).

Only augments with a DIRECT combat effect on the holder's own units (or combat-start
damage to enemies) are registered. Economy / gold / XP / item-grant / scouting / pure
trait-emblem augments are intentionally omitted -> implicit no-op.

Each fn is applied once at combat start: fn(team, enemies, ctx, variables) -> None
  team    : living friendly CombatUnit list
  enemies : living enemy CombatUnit list
  ctx     : CombatContext (shield_unit/heal/buff_ad/buff_attack_speed/deal_* helpers)
  variables : dict of REAL numeric values for this augment tier.
"""

from __future__ import annotations

# Assumed active non-unique traits when the real count is unavailable (approximation).
_ASSUMED_TRAITS = 6


def _golden_hex(team, enemies, ctx, variables) -> None:
    # Yasuo's Golden Hex: one unit gains BonusHealth + AttackSpeed% (gold-on-kill ignored).
    if not team:
        return
    hp = variables.get("BonusHealth", 0.0)
    as_ = variables.get("AttackSpeed", 0.0)
    u = max(team, key=lambda x: x.max_hp)  # approx: place the hex under the strongest unit
    u.max_hp += hp
    u.hp += hp
    ctx.buff_attack_speed(u, as_)


def _stand_united(team, enemies, ctx, variables) -> None:
    # Stand United: team gains @AD*100@% AD and @AP@% AP per non-unique active trait.
    # desc: AD is a fraction (0.015 -> 1.5%/trait); AP is a PERCENT number (1.5 -> 1.5%/trait).
    if not team:
        return
    ad = variables.get("AD", 0.0) * _ASSUMED_TRAITS  # fraction per trait (trait count approximated)
    ap_frac = (variables.get("AP", 0.0) / 100.0) * _ASSUMED_TRAITS  # percent AP -> fraction
    for u in team:
        ctx.buff_ad(u, ad)
        u.ap *= 1.0 + ap_frac


def _partial_ascension(team, enemies, ctx, variables) -> None:
    # Partial Ascension: team gains DamageAmp% after a delay; approx as AD+AP buff at start.
    if not team:
        return
    amp = variables.get("DamageAmp", 0.0) / 100.0  # percent -> fraction
    for u in team:  # approx: damage amp modeled as equivalent offensive buff
        ctx.buff_ad(u, amp)
        u.ap *= 1.0 + amp


def _charge_transfer(team, enemies, ctx, variables) -> None:
    # Charge Transfer II: team gains DamageAmp% (overkill redirection ignored); approx as AD+AP.
    if not team:
        return
    amp = variables.get("DamageAmp", 0.0) / 100.0  # percent -> fraction
    for u in team:  # approx: damage amp modeled as equivalent offensive buff
        ctx.buff_ad(u, amp)
        u.ap *= 1.0 + amp


def _warlords_honor(team, enemies, ctx, variables) -> None:
    # Warlord's Honor: team gains Stats% AD and AP per stack; start with StartingStacks.
    if not team:
        return
    stacks = variables.get("StartingStacks", 1.0)
    frac = (variables.get("Stats", 0.0) / 100.0) * stacks  # percent per stack -> fraction
    for u in team:
        ctx.buff_ad(u, frac)
        u.ap *= 1.0 + frac


def _boxing_lessons(team, enemies, ctx, variables) -> None:
    # Boxing Lessons: team gains flat Health for each ally starting in the front row.
    if not team:
        return
    frontline = [u for u in team if u.attack_range <= 1]
    bonus = variables.get("Health", 0.0) * len(frontline)
    for u in team:
        u.max_hp += bonus
        u.hp += bonus


def _sunfire_board(team, enemies, ctx, variables) -> None:
    # Sunfire Board: combat start, burn all enemies for TotalBurnPercent% of their max HP.
    if not enemies:
        return
    pct = variables.get("TotalBurnPercent", 0.0) / 100.0  # percent of max HP over duration
    for e in enemies:  # approx: total burn applied as up-front magic damage
        ctx.deal_magic(team[0] if team else e, e, e.max_hp * pct)


def _cursed_crown(team, enemies, ctx, variables) -> None:
    # Cursed Crown: team gains @DurabilityBonus*100@% Durability (also +max team size,
    # double player damage on loss -- not combat-stat relevant here).
    if not team:
        return
    dur = variables.get("DurabilityBonus", 0.0)  # 0.04 fraction
    for u in team:  # approx: durability ~= proportional max HP increase (matches batch_0 convention)
        gain = u.max_hp * dur
        u.max_hp += gain
        u.hp += gain


REGISTRY = {
    "TFT17_Augment_YasuoGodAugment_GoldenHex": _golden_hex,
    "TFT6_Augment_Diversify1": _stand_united,
    "TFT9_Augment_Commander_PartialAscension": _partial_ascension,
    "TFT_Augment_ChargeTransfer2": _charge_transfer,
    "TFT_Augment_Unforgotten": _warlords_honor,
    "TFT_Augment_BoxingLessons": _boxing_lessons,
    "TFT6_Augment_SunfireBoard": _sunfire_board,
    "TFT7_Augment_CursedCrown": _cursed_crown,
}
