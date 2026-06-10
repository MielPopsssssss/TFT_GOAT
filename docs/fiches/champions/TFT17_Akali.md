# Akali — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Akali`
- **Coût** : 2
- **Traits** : [N.O.V.A.](../traits/TFT17_DRX.md), [Marauder](../traits/TFT17_MeleeTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 750 | 1350 | 2430 |
| Dégâts d'attaque | 45 | 81 | 145.8 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Star Strike

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Reposition next to the target to strike the most enemies. Then throw @NumShurikens@ piercing kunai, each dealing @ModifiedDamage@ physical damage to the first enemy hit, reduced to @ModifiedSecondaryDamage@ for each subsequent target. Kunai remove @ArmorShred@ Armor, @ArmorShredCrit@ if they crit.N.O.V.A. Strike: Slice all enemies, applying Wound and a bleed that deals @ModifiedNovaDamage@ physical damage each second. Kunai increase the damage of the bleed by @NovaShurikenBonusDamage*100@%.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ArmorShred` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `ArmorShredCrit` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `DamageAD` | 27 / 37 / 56 / 84 / 140 / 72 / 72 |
| `DamageAP` | 6 / 4 / 6 / 9 / 15 / 6 / 6 |
| `NovaDamagePerSecond` | 12 / 12 / 18 / 24 / 30 / 22 / 22 |
| `NovaShurikenBonusDamage` | 0.12 / 0.12 / 0.12 / 0.12 / 0.12 / 0.12 / 0.12 |
| `NumShurikens` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `SecondaryDamageModifier` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |

