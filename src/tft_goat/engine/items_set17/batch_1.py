"""Item procs (batch_1). Stats deja appliquees ; ici uniquement la LOGIQUE des procs.

Magnitudes lues dans data/items_completed_set17.json 'effects' et codees en dur.

Mecaniques moteur utilisees (au lieu d'approximations crues) :
  - omnivamp : unit.omnivamp += <frac> au COMBAT_START ; le moteur soigne
    automatiquement omnivamp x degats sur autos ET sorts (cumul additif).
  - sunder armure : ctx.sunder_armor(target, frac) en ON_ATTACK (max actif).
  - shred RM     : ctx.shred_mr(target, frac) en ON_ATTACK ou aura COMBAT_START.
  - grievous     : ctx.apply_grievous(target, frac) en ON_ATTACK (max actif).
  - mana regen   : unit.mana_regen += <par seconde> au COMBAT_START (respecte le mana-lock).
  - durability   : ctx.add_durability(unit, frac) au COMBAT_START (cumul multiplicatif).
  - boucliers    : ctx.shield_unit(unit, amount, duration) (expirent + s'empilent).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unit import CombatUnit  # noqa: F401  (type hint only)


# ----------------------------------------------------------------------------
# COMBAT_START : boucliers / auras / setups (omnivamp, mana regen) au debut du combat
# ----------------------------------------------------------------------------

def _crownguard(unit, ctx):
    # Crownguard: bouclier = 25% PV max pendant 8s au debut du combat
    # (ShieldSize=25, ShieldDuration=8). Le bonus d'AP a l'expiration n'est pas modelise.
    if unit is None:
        return
    ctx.shield_unit(unit, unit.max_hp * 0.25, duration=8.0)  # ShieldSize=25, ShieldDuration=8


def _ionic_spark(unit, ctx):
    # Ionic Spark: Shred 30% RM des ennemis dans 2 hexes (MRShred=30, HexRange=2).
    # Aura appliquee au start via ctx.shred_mr (max actif). Les degats sur cast
    # ennemi (ManaRatio) ne sont pas representables (pas de hook on-enemy-cast).
    if unit is None:
        return
    for e in ctx.enemies_in_radius(unit, 2):  # HexRange=2
        ctx.shred_mr(e, 0.30)  # MRShred=30


def _hextech_gunblade(unit, ctx):
    # Hextech Gunblade (Set 17): omnivamp 15% des degats infliges (StatOmnivamp=0.15).
    # Le moteur soigne omnivamp x degats sur autos+sorts (cumul additif).
    # En jeu le soin va a l'allie le plus bas PV ; ici on l'attribue au porteur (approx).
    if unit is None:
        return
    unit.omnivamp += 0.15      # StatOmnivamp=0.15
    unit.mana_regen += 1.0     # ManaRegen=1 (par seconde)


def _hand_of_justice(unit, ctx):
    # Hand of Justice (UnstableConcoction): omnivamp 12% (StatOmnivamp_NotStatBar=0.12).
    # Le bonus conditionnel (x2 au-dessus/en-dessous de 50% PV) n'est pas modelise ;
    # on applique la valeur de base via le moteur d'omnivamp.
    if unit is None:
        return
    unit.omnivamp += 0.12      # StatOmnivamp_NotStatBar=0.12
    unit.mana_regen += 1.0     # ManaRegen=1 (par seconde)


def _spear_of_shojin_cs(unit, ctx):
    # Spear of Shojin: mana regen passif (ManaRegen=1 par seconde). Le +5 mana
    # par attaque (FlatManaRestore) reste gere en ON_ATTACK.
    if unit is None:
        return
    unit.mana_regen += 1.0     # ManaRegen=1 (par seconde)


def _archangels_cs(unit, ctx):
    # Archangel's Staff: mana regen passif (ManaRegen=1 par seconde). Le gain d'AP
    # periodique (APPerInterval) reste gere en ON_CAST.
    if unit is None:
        return
    unit.mana_regen += 1.0     # ManaRegen=1 (par seconde)


COMBAT_START = {
    "TFT_Item_Crownguard": _crownguard,
    "TFT_Item_IonicSpark": _ionic_spark,
    "TFT_Item_HextechGunblade": _hextech_gunblade,
    "TFT_Item_UnstableConcoction": _hand_of_justice,
    "TFT_Item_SpearOfShojin": _spear_of_shojin_cs,
    "TFT_Item_ArchangelsStaff": _archangels_cs,
    # FrozenHeart/Protector's Vow + GuardianAngel/Edge of Night -> HP_THRESHOLD (batch_hooks.py).
}


# ----------------------------------------------------------------------------
# ON_ATTACK : procs a chaque auto-attaque
# ----------------------------------------------------------------------------

def _red_buff(unit, target, ctx):
    # Red Buff (RapidFireCannon): Burn 1% PV max en degats vrais (BurnPercent=1)
    # + Wound 33% (HealingReductionPct=33) via Grievous.
    if unit is None or target is None:
        return
    ctx.deal_true(unit, target, target.max_hp * 0.01)  # BurnPercent=1 (DoT par tick, approx)
    ctx.apply_grievous(target, 0.33)                    # HealingReductionPct=33


def _last_whisper(unit, target, ctx):
    # Last Whisper: Sunder 30% armure (ArmorReductionPercent=30). N'empile pas.
    if unit is None or target is None:
        return
    ctx.sunder_armor(target, 0.30)  # ArmorReductionPercent=30 (max actif)


def _void_staff(unit, target, ctx):
    # Void Staff (StatikkShiv): Shred 30% RM (MRShred=30). N'empile pas.
    if unit is None or target is None:
        return
    ctx.shred_mr(target, 0.30)  # MRShred=30 (max actif)


def _spear_of_shojin(unit, target, ctx):
    # Spear of Shojin: +5 mana par attaque (FlatManaRestore=5)
    if unit is None:
        return
    unit.mana = min(getattr(unit, "max_mana", unit.mana + 5.0), unit.mana + 5.0)


def _quicksilver(unit, target, ctx):
    # Quicksilver: +3% AS cumulatif (ProcAttackSpeed=0.03)
    # approx: applique par attaque au lieu de chaque seconde
    if unit is None:
        return
    ctx.buff_attack_speed(unit, 0.03)


def _brawler_emblem(unit, target, ctx):
    # Brawler Emblem (HPTankEmblem): attaques infligent 3% des PV max du porteur
    # en degats magiques (PercentHPAttack=0.03)
    if unit is None or target is None:
        return
    ctx.deal_magic(unit, target, unit.max_hp * 0.03)


ON_ATTACK = {
    "TFT_Item_RapidFireCannon": _red_buff,
    "TFT17_Item_HPTankEmblemItem": _brawler_emblem,
    "TFT_Item_LastWhisper": _last_whisper,
    "TFT_Item_StatikkShiv": _void_staff,
    "TFT_Item_SpearOfShojin": _spear_of_shojin,
    "TFT_Item_Quicksilver": _quicksilver,
    # HextechGunblade + UnstableConcoction (Hand of Justice) : migres vers omnivamp
    # (COMBAT_START). Plus de ctx.heal en ON_ATTACK pour eviter le double-dipping.
}


# ----------------------------------------------------------------------------
# ON_CAST : procs au lancer de sort
# ----------------------------------------------------------------------------

def _archangels(unit, ctx):
    # Archangel's Staff: +20% AP par intervalle (APPerInterval=20 = pourcentage)
    # approx: applique a chaque cast au lieu de toutes les 5s
    if unit is None:
        return
    unit.ap += unit.ap * 0.20


ON_CAST = {
    "TFT_Item_ArchangelsStaff": _archangels,
}
