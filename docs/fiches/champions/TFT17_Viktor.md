# Viktor — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Viktor`
- **Coût** : 3
- **Traits** : [Psionic](../traits/TFT17_PsyOps.md), [Conduit](../traits/TFT17_ManaTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 25 | = | = |
| Résistance magique | 25 | = | = |
| Mana (initial/max) | 20 / 80 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Psionic Storm

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Channel a one-hex psionic storm that follows enemies for @AugmentedDuration@@Duration@ seconds. Each second, it grows larger and deals @ModifiedDamage@ magic damage to enemies within, reduced by @FalloffPerHex*100@% per hex from the epicenter.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AugmentedDuration` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `Damage` | 200 / 190 / 290 / 500 / 850 / 505 / 505 |
| `Duration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `FalloffPerHex` | 0.6 / 0.6 / 0.6 / 0.6 / 0.6 / 0.6 / 0.6 |
| `RadiusIncreasePerSecond` | 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 |

