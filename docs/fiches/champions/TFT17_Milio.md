# Milio — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Milio`
- **Coût** : 2
- **Traits** : [Timebreaker](../traits/TFT17_Timebreaker.md), [Fateweaver](../traits/TFT17_Fateweaver.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 550 | 990 | 1782 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 20 | = | = |
| Résistance magique | 20 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Mega Time Kick

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Kick a ball at the current target that deals @ModifiedDamage@ magic damage. On impact, the ball has a 100% Lucky chance to bounce to a new target dealing @ModifiedBounceDamage@ magic damage. These bounces can trigger additional bounces, but the odds halve with each bounce.Lucky: Check twice and take the better outcome.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BounceDamage` | 80 / 85 / 130 / 190 / 325 / 330 / 330 |
| `Damage` | 200 / 255 / 380 / 575 / 975 / 900 / 700 |

