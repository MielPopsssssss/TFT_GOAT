# Corki — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Corki`
- **Coût** : 4
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Fateweaver](../traits/TFT17_Fateweaver.md)
- **Rôle** : ADCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 45 | 81 | 145.8 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 0 / 60 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Asteroid Blaster

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Strafe to a nearby position, unleashing @BaseMissiles@ missiles split between the target and all enemies within two hexes. Missiles deal @ModifiedDamage@ physical damage with a @ProcChance@% Lucky chance of firing a mega missile that deals @ModifiedProcDamage@ instead.Meep Bonus: Every @ModifiedMeepCooldown@ seconds, launch an Explosive Meep at the target, dealing @ModifiedMeepDamage@ physical damage in a one hex radius on impact.Lucky: Check twice and take the better outcome.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BaseMeepCooldown` | 8 / 8 / 8 / 8 / 8 / 8 / 8 |
| `BaseMissiles` | 21 / 21 / 21 / 21 / 21 / 21 / 21 |
| `CDRPerMeep` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `CooldownReductionPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `MeepDamage` | 150 / 110 / 165 / 900 / 1200 / 1200 / 1200 |
| `MissileAD` | 25 / 28 / 42 / 280 / 200 / 25 / 25 |
| `MissileAP` | 6 / 5 / 7 / 24 / 30 / 25 / 25 |
| `MissilesPerLaunchAttack` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `ProcChance` | 20 / 20 / 20 / 20 / 20 / 20 / 20 |
| `ProcDamageMult` | 3.5 / 3.5 / 3.5 / 3.5 / 3.5 / 3.5 / 3.5 |

