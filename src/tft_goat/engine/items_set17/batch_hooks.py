"""Items utilisant les hooks moteur (on-damaged / on-tick / hp-threshold / revive / durability).

Valeurs tirees de la vraie data Set 17 (effects). apiNames verifies presents dans le contenu.
Les approximations (ICD, untargetable, invuln) sont notees `# approx:`.
"""

from __future__ import annotations

from ..unit import CombatUnit


# --- ON_DAMAGED : reflet quand l'unite SUBIT une attaque --------------------
def _bramble_reflect(unit: CombatUnit, attacker: CombatUnit, ctx) -> None:
    # Bramble Vest : "When struck by any attack, deal 100 magic AoE" (1StarAoEDamage=100, ICD 2s).
    ctx.deal_magic(unit, attacker, 100.0)  # approx: ICD 2s ignore, cible l'attaquant


ON_DAMAGED = {
    "TFT_Item_BrambleVest": _bramble_reflect,
}


# --- ON_TICK : effets periodiques (~1/s) ------------------------------------
def _dragons_claw(unit: CombatUnit, ctx) -> None:
    # Dragon's Claw : heal 2.5% PV max toutes les 2s -> ~1.25%/s.
    ctx.heal(unit, unit.max_hp * (2.5 / 100.0) / 2.0)


def _spirit_visage(unit: CombatUnit, ctx) -> None:
    # Spirit Visage (Redemption) : regen 2% des PV manquants/s (cap MaxHeal=250).
    ctx.heal(unit, min(250.0, (unit.max_hp - unit.hp) * 0.02))


ON_TICK = {
    "TFT_Item_DragonsClaw": _dragons_claw,
    "TFT_Item_Redemption": _spirit_visage,
}


# --- HP_THRESHOLD : proc unique sous un seuil de PV -------------------------
def _steraks(unit: CombatUnit, ctx) -> None:
    # Sterak's Gage : a 60% PV, bouclier = 40% PV max.
    ctx.shield_unit(unit, unit.max_hp * 0.40)


def _edge_of_night(unit: CombatUnit, ctx) -> None:
    # Edge of Night : a 60% PV, soigne 20% des PV manquants (+ intargetable 1s approx -> bouclier).
    ctx.heal(unit, (unit.max_hp - unit.hp) * 0.20)
    ctx.shield_unit(unit, unit.max_hp * 0.15)  # approx: intargetabilite 1s


def _protectors_vow_shield(unit: CombatUnit, ctx) -> None:
    # Protector's Vow : a 40% PV, bouclier = 20% PV max (+ mana, donne au combat start).
    ctx.shield_unit(unit, unit.max_hp * 0.20)


def _zhonyas(unit: CombatUnit, ctx) -> None:
    # Zhonya's Paradox (Ornn, in-set) : a 40% PV, invulnerable 3s -> approx gros bouclier.
    ctx.shield_unit(unit, unit.max_hp * 0.40)  # approx: invulnerabilite 3s


HP_THRESHOLD = {
    "TFT_Item_SteraksGage": (0.60, _steraks),
    "TFT_Item_GuardianAngel": (0.60, _edge_of_night),
    "TFT_Item_FrozenHeart": (0.40, _protectors_vow_shield),
    "TFT4_Item_OrnnZhonyasParadox": (0.40, _zhonyas),
}


# --- COMBAT_START : mana / durability --------------------------------------
def _protectors_vow_mana(unit: CombatUnit, ctx) -> None:
    # Protector's Vow : +20 mana au debut du combat (CombatStartMana=20).
    unit.mana = min(unit.max_mana, unit.mana + 20.0)


def _steadfast_heart(unit: CombatUnit, ctx) -> None:
    # Steadfast Heart : durability 15% au-dessus de 50% PV (approx constant ; base 5%).
    unit.incoming_reduction = max(unit.incoming_reduction, 0.15)


COMBAT_START = {
    "TFT_Item_FrozenHeart": _protectors_vow_mana,
    "TFT_Item_NightHarvester": _steadfast_heart,
}


# --- REVIVE : aucun item standard Set 17 ne ressuscite (GA -> Edge of Night).
# Le mecanisme moteur existe (ITEM_REVIVE) ; vide pour Set 17, pret pour items hors-set/artefacts.
REVIVE: dict[str, callable] = {}
