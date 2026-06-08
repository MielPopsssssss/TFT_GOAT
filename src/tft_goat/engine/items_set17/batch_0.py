"""Procs des objets completes (lot 0) pour le moteur de combat Set 17.

Les bonus de STATS (AD/AP/Armor/HP/MR/AS/Crit/Mana) sont deja appliques
automatiquement depuis item.effects (cf. unit.build_unit). On code ici UNIQUEMENT
la logique active des procs. Magnitudes lues dans 'effects' du JSON et codees en dur.

Hooks:
  COMBAT_START = {item_api: fn(unit, ctx)}
  ON_ATTACK    = {item_api: fn(unit, target, ctx)}
  ON_CAST      = {item_api: fn(unit, ctx)}
"""

from __future__ import annotations

from ..unit import CombatUnit


# ---------------------------------------------------------------------------
# COMBAT_START
# ---------------------------------------------------------------------------

def _gargoyle_combat_start(unit: CombatUnit, ctx) -> None:
    # Gargoyle Stoneplate: "+10 Armor and +10 MR per enemy targeting holder"
    # (ArmorPerEnemy=10, MRPerEnemy=10). approx: applique une fois au debut en
    # supposant que tous les ennemis vivants ciblent le porteur (pas de tracking).
    if unit is None:
        return
    enemies = ctx.living_enemies(unit) or []
    n = len(enemies)
    if n <= 0:
        return
    unit.armor += 10.0 * n  # ArmorPerEnemy = 10.0
    unit.mr += 10.0 * n      # MRPerEnemy = 10.0


def _steraks_combat_start(unit: CombatUnit, ctx) -> None:
    # Sterak's Gage: "At 60% HP, gain a shield = 40% max Health" (decroit en 4s).
    # approx: applique le bouclier au debut du combat (pas de tracking du seuil HP).
    if unit is None:
        return
    ctx.shield_unit(unit, unit.max_hp * 0.40)  # PercentHealthShield = 0.40


def _bloodthirster_combat_start(unit: CombatUnit, ctx) -> None:
    # Bloodthirster: omnivol via le nouveau mecanisme moteur (auto-heal sur CHAQUE
    # instance de degats = omnivamp x degats, autos + sorts, cumul additif).
    # StatOmnivamp = 0.20. On retire l'ancien heal ON_ATTACK pour eviter le double.
    # Shield: "Once per combat at 40% HP, gain 25% max HP Shield up to 5s."
    # approx: applique le bouclier au debut (pas de tracking du seuil/once-per-combat).
    if unit is None:
        return
    unit.omnivamp += 0.20  # StatOmnivamp = 0.20
    ctx.shield_unit(unit, unit.max_hp * 0.25, duration=5.0)  # ShieldHealthPercent=25 ->0.25, ShieldDuration=5.0


def _voyager_combat_start(unit: CombatUnit, ctx) -> None:
    # Voyager Emblem (TFT17 FlexTraitEmblem): "Combat Start: holder + allies in
    # same row gain a bonus by role -> Tanks: +10 Armor/MR; Fighters/Assassins:
    # 10% Omnivamp; Other: 10% Attack Speed." approx: role n'est pas exposé sur
    # CombatUnit et il n'y a pas d'API alliés -> on applique la branche "Other"
    # (BonusAttackSpeed=0.10) au seul porteur, modeste.
    if unit is None:
        return
    ctx.buff_attack_speed(unit, 0.10)  # BonusAttackSpeed = 0.10


def _morello_combat_start(unit: CombatUnit, ctx) -> None:
    # Morellonomicon: regen de mana passive (ManaRegen=1.0 mana/sec). Le moteur
    # l'ajoute chaque seconde en respectant le mana-lock.
    if unit is None:
        return
    unit.mana_regen += 1.0  # ManaRegen = 1.0


COMBAT_START = {
    "TFT_Item_GargoyleStoneplate": _gargoyle_combat_start,
    "TFT_Item_Bloodthirster": _bloodthirster_combat_start,
    "TFT17_Item_FlexTraitEmblemItem": _voyager_combat_start,
    "TFT_Item_Morellonomicon": _morello_combat_start,
}


# ---------------------------------------------------------------------------
# ON_ATTACK
# ---------------------------------------------------------------------------

def _guinsoos_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Guinsoo's Rageblade: "AttackSpeedPerStack = 7% stacking AS par seconde".
    # approx: ajoute le gain d'AS a chaque attaque (pas de timer 1s precis).
    if unit is None:
        return
    ctx.buff_attack_speed(unit, 0.07)  # AttackSpeedPerStack = 7 -> 0.07


def _kraken_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Kraken's Fury: "ADOnAttack = 3.5% stacking AD par attaque" (cap 15 stacks).
    # approx: gain d'AD a chaque attaque, sans capter le cap ni le capstone AS.
    if unit is None:
        return
    ctx.buff_ad(unit, 0.035)  # ADOnAttack = 0.035


def _titans_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Titan's Resolve: "StackingAD = 2% AD + StackingSP = 2 AP en attaquant/subissant"
    # (cap 25 stacks). approx: gain d'AD + AP a chaque attaque, sans capter le cap.
    if unit is None:
        return
    ctx.buff_ad(unit, 0.02)  # StackingAD = 0.02
    unit.ap += 2.0           # StackingSP = 2.0 (AP)


def _morello_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Morellonomicon: Burn = 1% max HP true dmg / sec pendant 10s + Wound (reduction
    # de soin) sur l'ennemi. approx: burn DoT applique comme degats vrais a chaque
    # attaque (1% max HP); Grievous via le mecanisme moteur (max actif).
    if unit is None or target is None:
        return
    ctx.deal_true(unit, target, target.max_hp * 0.01)  # BurnPercent = 1 -> 0.01
    ctx.apply_grievous(target, 0.33)  # GrievousWoundsPercent = 33 -> 0.33


def _sunfire_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Sunfire Cape (RedBuff): Burn = 1% max HP true dmg toutes les 2s (ICD), 10s,
    # + Wound (reduction de soin). approx: burn DoT applique comme degats vrais a
    # chaque attaque (1% max HP); Grievous via le mecanisme moteur (max actif).
    if unit is None or target is None:
        return
    ctx.deal_true(unit, target, target.max_hp * 0.01)  # BurnPercent = 1 -> 0.01
    ctx.apply_grievous(target, 0.33)  # GrievousWoundsPercent = 33 -> 0.33


def _nashor_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Nashor's Tooth (Leviathan): "BaseManaOnHit = 2 mana par attaque".
    # approx: pas de distinction crit (ManaOnCrit=4), on prend le cas de base.
    if unit is None:
        return
    unit.mana = min(unit.max_mana, unit.mana + 2.0)  # BaseManaOnHit = 2.0


def _strikers_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Striker's Flail (PowerGauntlet): "crit -> +5% Damage Amp (max 4 stacks, 5s)".
    # approx: on n'a pas le hook crit ni le tracking d'amp -> on traduit en petit
    # gain d'AD a chaque attaque, plafonne par la frequence de combat.
    if unit is None:
        return
    ctx.buff_ad(unit, 0.05 * unit.crit_chance)  # BuffDamageAmp=0.05, pondere par crit


def _evenshroud_on_attack(unit: CombatUnit, target: CombatUnit, ctx) -> None:
    # Evenshroud (SpectralGauntlet): Sunder = -30% Armor sur l'ennemi (max actif,
    # pas de mutation permanente) via le mecanisme moteur.
    if unit is None or target is None:
        return
    ctx.sunder_armor(target, 0.30)  # ARReductionAmount = 30 -> 0.30


ON_ATTACK = {
    # Bloodthirster: omnivol migre vers unit.omnivamp (cf. COMBAT_START) -> plus
    # de heal ON_ATTACK ici (evite le double-dip).
    "TFT_Item_GuinsoosRageblade": _guinsoos_on_attack,
    "TFT_Item_RunaansHurricane": _kraken_on_attack,
    "TFT_Item_TitansResolve": _titans_on_attack,
    "TFT_Item_Morellonomicon": _morello_on_attack,
    "TFT_Item_RedBuff": _sunfire_on_attack,
    "TFT_Item_Leviathan": _nashor_on_attack,
    "TFT_Item_PowerGauntlet": _strikers_on_attack,
    "TFT_Item_SpectralGauntlet": _evenshroud_on_attack,
}
