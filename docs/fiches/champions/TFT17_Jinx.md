# Jinx — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Jinx`
- **Coût** : 2
- **Traits** : [Anima](../traits/TFT17_AnimaSquad.md), [Challenger](../traits/TFT17_ASTrait.md)
- **Rôle** : ADCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 550 | 990 | 1782 |
| Dégâts d'attaque | 55 | 99 | 178.2 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 20 | = | = |
| Résistance magique | 20 | = | = |
| Mana (initial/max) | 20 / 80 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Explosive Attitude

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Fire a barrage of @ModifiedNumRockets@ rockets in a cone, each dealing @TotalDamage@ physical damage to the first target hit.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 3 / 29 / 44 / 70 / 110 / 3 / 3 |
| `APDamage` | 0 / 3 / 5 / 7 / 12 / 0 / 0 |
| `ASPerBullet` | 0.35 / 0.35 / 0.35 / 0.35 / 0.35 / 0.35 / 0.35 |
| `BaseBullets` | 16 / 16 / 16 / 16 / 16 / 16 / 16 |
| `BulletTravelDistance` | 1500 / 1500 / 1500 / 1500 / 1500 / 1500 / 1500 |
| `MinimumNumTargets` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `RocketsPerLaunchAttack` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |
| `TotalSpellTime` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

