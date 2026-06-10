# Ezreal — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Ezreal`
- **Coût** : 1
- **Traits** : [Timebreaker](../traits/TFT17_Timebreaker.md), [Sniper](../traits/TFT17_RangedTrait.md)
- **Rôle** : ADCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 450 | 810 | 1458 |
| Dégâts d'attaque | 40 | 72 | 129.6 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Temporal Shot

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Active: Fire a blast at the current target that deals @TotalDamage@ physical damage. Every @TakedownsToDrone@ takedowns, gain a drone that deals @ModifiedDroneDamage@ physical damage to the current target on cast. (Total Takedowns: @TFTUnitProperty.:TFT17_Ezreal_Takedowns@)

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 0 / 160 / 240 / 365 / 620 / 0 / 0 |
| `APDamage` | 0 / 14 / 21 / 32 / 54 / 0 / 0 |
| `DroneDamage` | 0 / 8 / 12 / 18 / 30 / 0 / 0 |
| `TakedownTimerThreshold` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `TakedownsToDrone` | 8 / 8 / 8 / 8 / 8 / 8 / 8 |
| `TakedownsToForm3` | 60 / 60 / 60 / 60 / 60 / 60 / 60 |

