# Jhin — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Jhin`
- **Coût** : 5
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Eradicator](../traits/TFT17_JhinUniqueTrait.md), [Sniper](../traits/TFT17_RangedTrait.md)
- **Rôle** : ADCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 80 | 144 | 259.2 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 0 / 44 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Space Opera

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Jhin has a fixed attack speed of @FixedAS@ and converts every @PercentBonusASToConvert*100@% of bonus Attack Speed into @ADConversionRate@ bonus Attack Damage.Active: Summon @NumHands@ spectral hands that fire alongside Jhin for the next @NumAttacks@ attacks. Each hand deals @TotalDamage@ physical damage per shot. The final shots deal @FinalShotPercentDamageIncrease*100@% more damage and pierce through the most enemies in a line, dealing @PercentDamageReductionPerTargetHit*100@% reduced damage per target hit.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADConversionRate` | 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 |
| `ADDamage` | 0 / 41 / 62 / 644 / 444 / 0 / 0 |
| `APDamage` | 0 / 4 / 6 / 44 / 0 / 0 / 0 |
| `ArmorReduction` |  |
| `FinalShotPercentDamageIncrease` | 2.44 / 2.44 / 2.44 / 2.44 / 2.44 / 2.44 / 2.44 |
| `FixedAS` | 0 / 0.9 / 0.9 / 1.4 / 0 / 0 / 0 |
| `NumAttacks` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `NumHands` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `PercentBonusASToConvert` | 0.01 / 0.01 / 0.01 / 0.01 / 0.01 / 0.01 / 0.01 |
| `PercentDamageReductionPerTargetHit` | 0.44 / 0.44 / 0.44 / 0.44 / 0.44 / 0.44 / 0.44 |

