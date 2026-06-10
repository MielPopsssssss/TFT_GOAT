# Zoe — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Zoe`
- **Coût** : 2
- **Traits** : [Arbiter](../traits/TFT17_ADMIN.md), [Conduit](../traits/TFT17_ManaTrait.md)
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
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Paddle Star

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Fire a paddle star at the current target, dealing @ModifiedDamage@ magic damage to the first target hit and @ModifiedSecondaryDamage@ to others it passes through. When the missile reaches its destination, redirect it to a distant enemy, increasing its speed and repeating the damage. This redirect can occur @AugmentedNumRedirects@@NumRedirects@ times.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AugmentedNumRedirects` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `BaseSpeed` | 1600 / 1600 / 1600 / 1600 / 1600 / 1600 / 1600 |
| `Damage` | 50 / 73 / 110 / 180 / 300 / 210 / 155 |
| `NumRedirects` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `SecondaryDamage` | 20 / 34 / 51 / 77 / 130 / 105 / 60 |
| `SpeedPerBounce` | 800 / 800 / 800 / 800 / 800 / 800 / 800 |

