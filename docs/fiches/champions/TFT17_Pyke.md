# Pyke — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Pyke`
- **Coût** : 2
- **Traits** : [Psionic](../traits/TFT17_PsyOps.md), [Voyager](../traits/TFT17_FlexTrait.md)
- **Rôle** : ADReaper
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 45 | 81 | 145.8 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 0 / 40 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Marked for Death

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Reposition up to one hex to throw a harpoon at the furthest enemy. The harpoon pulls the first enemy hit one hex forward and deals @ModifiedDamage@ physical damage. Then, teleport behind them and cleave, dealing @ModifiedTargetDamage@ physical damage to them and @ModifiedAreaDamage@ physical damage to nearby enemies.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AoEDamage` | 150 / 120 / 180 / 360 / 615 / 475 / 475 |
| `SpearDamage` | 60 / 60 / 90 / 135 / 180 / 180 / 180 |
| `TargetDamage` | 0 / 210 / 315 / 720 / 1225 / 0 / 0 |

