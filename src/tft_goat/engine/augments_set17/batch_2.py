"""Logique de COMBAT pour le lot 2 des augments Set 17 (combat-start buffs sur ses propres unites).

Seuls les augments a effet de combat verifiable sur les stats des unites sont enregistres.
Les augments d'economie/loot/XP/reroll/emblem pur/spawn d'unite sont omis (no-op implicite).
"""

from __future__ import annotations

from ..unit import CombatUnit


def _aurelion_sol_small_quest(team, enemies, ctx, variables) -> None:
    # Toute l'equipe gagne SmallQuestADAP en AD plat et en AP plat.
    v = variables.get("SmallQuestADAP", 0.0)
    for u in team:
        u.ad += v
        u.ap += v


def _giant_and_mighty(team, enemies, ctx, variables) -> None:
    # L'equipe gagne FlatHealth PV plats + PercentHealth% des PV max.
    flat = variables.get("FlatHealth", 0.0)
    pct = variables.get("PercentHealth", 0.0)
    for u in team:
        bonus = flat + u.max_hp * pct
        u.max_hp += bonus
        u.hp += bonus


def _late_game_scaling(team, enemies, ctx, variables) -> None:
    # approx: cible les 5-couts, identite de cout indisponible -> applique a toute l'equipe.
    hp = variables.get("BonusHealth", 0.0)
    asp = variables.get("AttackSpeed", 0.0)
    for u in team:
        bonus = u.max_hp * hp
        u.max_hp += bonus
        u.hp += bonus
        ctx.buff_attack_speed(u, asp)


def _marksman(team, enemies, ctx, variables) -> None:
    # approx: gain d'AD de base (BaselineAD) au start; les procs periodiques sont ignores.
    frac = variables.get("BaselineAD", 0.0)
    for u in team:
        ctx.buff_ad(u, frac)


def _plot_armor(team, enemies, ctx, variables) -> None:
    # L'equipe gagne BaseResists en Armure et RM (palier renforce conditionnel ignore).
    r = variables.get("BaseResists", 0.0)
    for u in team:
        u.armor += r
        u.mr += r


def _trifecta(team, enemies, ctx, variables) -> None:
    # approx: BuffedNumber unites Tier-cost gagnent PV + AS au start; cout inconnu -> N premieres.
    n = int(variables.get("BuffedNumber", 0.0))
    hp = variables.get("Health", 0.0)
    asp = variables.get("AttackSpeed", 0.0)
    for u in team[:n]:
        u.max_hp += hp
        u.hp += hp
        ctx.buff_attack_speed(u, asp)


def _we_stick_together(team, enemies, ctx, variables) -> None:
    # approx: bonus d'AS aux allies partageant le trait d'emblem; traits indisponibles -> equipe.
    asp = variables.get("ASPercent", 0.0) / 100.0
    for u in team:
        ctx.buff_attack_speed(u, asp)


def _climb_the_ladder(team, enemies, ctx, variables) -> None:
    # approx: buff trait-partage a la mort d'un allie, modelise en un seul grant AP/AD/Armure/RM a l'equipe.
    # BonusAP/BonusArmor/BonusMR sont plats; BonusAD est une fraction (@BonusAD*100@%).
    ap = variables.get("BonusAP", 0.0)
    ad = variables.get("BonusAD", 0.0)
    armor = variables.get("BonusArmor", 0.0)
    mr = variables.get("BonusMR", 0.0)
    for u in team:
        u.ap += ap
        ctx.buff_ad(u, ad)
        u.armor += armor
        u.mr += mr


def _electrocharge(team, enemies, ctx, variables) -> None:
    # approx: proc AoE magique sur attaque recue, modelise en une rafale unique de degats magiques a tous les ennemis.
    dmg = variables.get("Damage2", 0.0) or variables.get("Damage1", 0.0)
    if dmg <= 0 or not team:
        return
    src = team[0]
    for e in enemies:
        ctx.deal_magic(src, e, dmg)


REGISTRY = {
    "TFT17_Augment_AurelionSolGodAugment_SmallQuest": _aurelion_sol_small_quest,
    "TFT_Augment_GiantAndMighty": _giant_and_mighty,
    "TFT_Augment_LateGameScaling": _late_game_scaling,
    "TFT_Augment_MarksMan": _marksman,
    "TFT_Augment_PlotArmor": _plot_armor,
    "TFT_Augment_Trifecta1": _trifecta,
    "TFT_Augment_WeStickTogether": _we_stick_together,
    "TFT_Augment_ClimbTheLadder1": _climb_the_ladder,
    "TFT6_Augment_Electrocharge1": _electrocharge,
}
