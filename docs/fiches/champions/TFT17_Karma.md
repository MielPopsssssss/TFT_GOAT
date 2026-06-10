# Karma — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Karma`
- **Coût** : 4
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Voyager](../traits/TFT17_FlexTrait.md)
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
| Mana (initial/max) | 10 / 55 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Singularity

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gather the force of a black hole, dealing @ModifiedDamage@ magic damage split between the target and the @NumEnemies@ closest enemies to them. The target takes an additional @ModifiedSecondaryDamage@ magic damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BaseHexRange` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `Damage` | 0 / 570 / 855 / 5000 / 6000 / 0 / 0 |
| `HexPerExpansion` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `MaximumHexes` | 8 / 8 / 8 / 8 / 8 / 8 / 8 |
| `NumCastsToExpand` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `NumEnemies` | 2 / 2 / 2 / 4 / 4 / 4 / 4 |
| `SecondaryDamage` | 0 / 180 / 270 / 1000 / 1320 / 0 / 0 |

