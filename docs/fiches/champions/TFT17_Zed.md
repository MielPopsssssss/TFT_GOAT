# Zed — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Zed`
- **Coût** : 5
- **Traits** : [Galaxy Hunter](../traits/TFT17_ZedUniqueTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 85 | 153 | 275.4 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Quantum Clone

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Create a clone behind the target with @HPPenalty*100@% reduced max Health and @ManaCostIncrease@ increased Mana cost. The clone inherits its creator's items, stats, and current Health, and can cast Quantum Clone.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `HPPenalty` | 0.33 / 0.33 / 0.45 / 0.45 / 0.33 / 0.33 / 0.33 |
| `ManaCostIncrease` | 30 / 30 / 30 / 30 / 30 / 30 / 30 |

