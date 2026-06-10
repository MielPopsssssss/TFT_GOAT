# Morgana — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Morgana`
- **Coût** : 4
- **Traits** : [Dark Lady](../traits/TFT17_MorganaUniqueTrait.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 70 | = | = |
| Résistance magique | 70 | = | = |
| Mana (initial/max) | 30 / 90 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Dark Form

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Transform for @HealthGainDuration@ seconds, gaining @ModifiedHealthGain@ Health and tethering to nearby champions. Over the duration, deal @ModifiedDamage@ magic damage to the closest @NumEnemies@ enemies and restore @ModifiedHeal@ health to the closest @NumAllies@ injured allies.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `APDamage` | 0 / 100 / 150 / 3000 / 0 / 0 / 0 |
| `APHealing` | 0 / 100 / 150 / 3000 / 0 / 0 / 0 |
| `APHealthGain` | 0 / 525 / 625 / 2500 / 2500 / 2500 / 2500 |
| `HealthGainDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `NumAllies` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `NumEnemies` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `PercentHPHealthGain` | 0 / 0.15 / 0.15 / 0.5 / 3000 / 0 / 0 |

