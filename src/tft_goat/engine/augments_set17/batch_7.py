"""Batch 7 — prismatic combat prioritaires (2026-06-10).

Priorisation : Riot a RETIRÉ les augments de match-v1 (aucun proxy d'usage challenger) ;
sous exposition uniforme par tier dans l'env, la distorsion = ampleur de l'effet non
modélisé -> les prismatic combat d'abord. Valeurs lues dans la data (augment.effects +
composants via ctx.content) ; approximations commentées. Pins :
tests/test_augments_prismatic_batch.py.
"""

from __future__ import annotations

from .batch_6 import ASSUMED_MISSING_TAC_HP


def _component_fx(ctx, api: str) -> dict:
    """Effets data d'un composant (via ctx.content) — jamais de chiffre en dur."""
    if ctx.content is None:
        return {}
    item = ctx.content.items.get(api)
    return dict(item.effects) if item else {}


def _belt_overflow(team, enemies, ctx, variables) -> None:
    # "Gain @NumItems@ Giant's Belts. Your Giant's Belts grant +@BonusHealth@ bonus Health."
    # approx : les @NumItems@ ceintures finissent équipées -> les N plus costauds gagnent
    # (HP de la ceinture data + bonus). Les ceintures DÉJÀ équipées ne sont pas re-bostées
    # (l'env compte les items en générique : porteurs réels inconnus).
    n = int(variables.get("NumItems", 0.0))
    hp = _component_fx(ctx, "TFT_Item_GiantsBelt").get("Health", 0.0) + variables.get("BonusHealth", 0.0)
    for u in sorted(team, key=lambda x: -x.max_hp)[:n]:
        u.max_hp += hp
        u.hp += hp


def _comeback_story(team, enemies, ctx, variables) -> None:
    # "team gains @HPPerMissingHP@ Health and @ASPerMissingHP@% AS per missing player Health"
    # même approx que Soraka : ~30 PV joueur manquants (cf. batch_6.ASSUMED_MISSING_TAC_HP).
    hp = variables.get("HPPerMissingHP", 0.0) * ASSUMED_MISSING_TAC_HP
    as_frac = variables.get("ASPerMissingHP", 0.0) / 100.0 * ASSUMED_MISSING_TAC_HP
    for u in team:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_attack_speed(u, as_frac)


def _sweet_treats(team, enemies, ctx, variables) -> None:
    # "team gains @HealthPerItem@ Health for each item equipped" (l'anvil d'artifact = éco).
    # Items réels si visibles (item_apis) ; sinon ~6 items team-wide (mid-game typique).
    n_items = sum(len(u.item_apis) for u in team) or 6
    hp = variables.get("HealthPerItem", 0.0) * n_items
    for u in team:
        u.max_hp += hp
        u.hp += hp


def _wand_overflow(team, enemies, ctx, variables) -> None:
    # "Gain @NumItems@ Rods. Your Rods grant +@BonusStat*100@% Attack Speed."
    # approx : les @NumItems@ rods finissent équipées -> AP du rod (data) + l'AS bonus.
    n = int(variables.get("NumItems", 0.0))
    ap = _component_fx(ctx, "TFT_Item_NeedlesslyLargeRod").get("AP", 0.0)
    as_frac = variables.get("BonusStat", 0.0)
    for u in sorted(team, key=lambda x: -x.max_hp)[:n]:
        u.ap += ap
        ctx.buff_attack_speed(u, as_frac)


REGISTRY = {
    "TFT_Augment_BeltOverflow": _belt_overflow,
    "TFT_Augment_ComebackStory": _comeback_story,
    "TFT_Augment_SweetTreats": _sweet_treats,
    "TFT_Augment_WandOverflow": _wand_overflow,
}
