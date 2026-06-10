# Aurelion Sol — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_AurelionSol`
- **Coût** : 4
- **Traits** : [Mecha](../traits/TFT17_Mecha.md), [Conduit](../traits/TFT17_ManaTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 15 / 75 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Deathbeam

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Channel a deathbeam in a line towards the current target for @AugmentedDuration@@Duration@ seconds. It deals @ModifiedDamage@ magic damage per second, reduced by @DamageReductionPerTarget*100@% per enemy it passes through. Deathbeam ignores @MagicPen*100@% of the enemy's Magic Resist.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AugmentedDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `DamagePerSecond` | 250 / 320 / 480 / 2000 / 2000 / 1650 / 1650 |
| `DamageReductionPerTarget` | 0.8 / 0.8 / 0.8 / 0.8 / 0.8 / 0.8 / 0.8 |
| `Duration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `MagicPen` | 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 |

