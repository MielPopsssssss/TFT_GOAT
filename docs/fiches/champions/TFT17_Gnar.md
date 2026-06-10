# Gnar — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Gnar`
- **Coût** : 2
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Sniper](../traits/TFT17_RangedTrait.md)
- **Rôle** : ADSpecialist
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 550 | 990 | 1782 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 20 | = | = |
| Résistance magique | 20 | = | = |
| Mana (initial/max) | 0 / 5 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Slingshot Maneuver

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Every 5th attack, launch a returning boomerang at the target that travels two hexes past the first enemy it hits. It deals @ModifiedDamage@ physical damage, reduced by @DamageReductionPerHit*100@% per hit.Meep Bonus: @ModifiedNumMeeps@ Meeps attack alongside Gnar, dealing @ModifiedMeepDPS@ physical damage per second.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DamageAD` | 200 / 225 / 340 / 560 / 860 / 600 / 600 |
| `DamageAP` | 30 / 20 / 30 / 45 / 75 / 95 / 95 |
| `DamageReductionPerHit` | 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 / 0.75 |
| `MeepASScaling` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |
| `MeepPercentBAD` | 0.23 / 0.23 / 0.23 / 0.23 / 0.23 / 0.23 / 0.23 |
| `NumMeepsPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

