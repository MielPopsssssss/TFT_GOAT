# Xayah — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Xayah`
- **Coût** : 4
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Sniper](../traits/TFT17_RangedTrait.md)
- **Rôle** : ADCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 52 | 93.6 | 168.48 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Stellar Ricochet

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks bounce to strike @AttackNumEnemies@ times, dealing @PassivePercentReducedDamage*100@% reduced damage per target hit and leaving a Feather behind the final target.Active: Gain @AttackSpeed*100@% Attack Speed for the next @NumAttacks@ attacks. At the end, recall all Feathers split between the closest @RecallFeatherTargets@ enemies, dealing @TotalDamage@ physical damage each. Xayah's current target takes @ModifiedPrimaryTargetBonusDamage@ additional physical damage per feather.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 40 / 45 / 68 / 900 / 375 / 300 / 300 |
| `APDamage` | 10 / 6 / 9 / 60 / 75 / 75 / 75 |
| `ActivePercentReducedDamage` | 0.2 / 0.2 / 0.2 / 0.2 / 0.2 / 0.2 / 0.2 |
| `AttackNumEnemies` | 3 / 3 / 3 / 5 / 5 / 5 / 5 |
| `AttackSpeed` | 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 |
| `Duration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `NumAttacks` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |
| `PassivePercentReducedDamage` | 0.6 / 0.6 / 0.6 / 0.3 / 0.3 / 0.3 / 0.3 |
| `PrimaryTargetBonusDamage` | 10 / 25 / 40 / 200 / 10 / 10 / 10 |
| `RecallFeatherTargets` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |

