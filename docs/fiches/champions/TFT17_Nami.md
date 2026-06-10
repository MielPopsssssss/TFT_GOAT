# Nami — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Nami`
- **Coût** : 4
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Replicator](../traits/TFT17_APTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 40 | 72 | 129.6 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 20 / 65 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Bubble Pop

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Toss a disco bubble at the target that deals @ModifiedDamage@ split between enemies in a one hex radius. The explosion sends @NumProjectiles@ globs towards nearby enemies that deal @ModifiedFirstBounceDamage@ magic damage. On cast, Nami enters {{TFT17_SpaceGroove_TheGroove}} for @GrooveDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 260 / 440 / 660 / 5000 / 3600 / 4000 / 4000 |
| `FirstBounceDamage` | 120 / 110 / 165 / 1000 / 2000 / 1200 / 1200 |
| `GrooveDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `NumProjectiles` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |

