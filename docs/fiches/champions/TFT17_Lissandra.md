# Lissandra — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Lissandra`
- **Coût** : 1
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Shepherd](../traits/TFT17_SummonTrait.md), [Replicator](../traits/TFT17_APTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 450 | 810 | 1458 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Dark Matter

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Hurl a shard towards the current target, dealing @ModifiedDamage@ magic damage to the first target it hits. After hitting its initial target or at its final destination, the dagger explodes dealing @ModifiedSecondaryDamage@ magic damage to nearby targets.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 200 / 250 / 375 / 600 / 1020 / 660 / 660 |
| `SecondaryDamage` | 100 / 50 / 75 / 115 / 195 / 300 / 300 |

