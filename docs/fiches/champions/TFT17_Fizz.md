# Fizz — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Fizz`
- **Coût** : 3
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : APReaper
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 55 | = | = |
| Résistance magique | 55 | = | = |
| Mana (initial/max) | 0 / 20 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Meep Bait

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Dash through the current target, dealing @ModifiedDamage@ magic damage. Every third cast also summons a Mega Meep after a delay, briefly knocking the target up and dealing @ModifiedChompDamage@ magic damage. Adjacent enemies take @SecondaryDamage*100@% damage.Meep Bonus: Add @ModifiedNumMeeps@ Meep to the bait, increasing Mega Meep damage by @ModifiedMeepBonusDamage@.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BiteDamageAP` | 100 / 185 / 280 / 445 / 785 / 660 / 660 |
| `BiteDamageMeep` | 70 / 75 / 115 / 180 / 320 / 400 / 400 |
| `DashDamage` | 80 / 120 / 180 / 290 / 470 / 250 / 250 |
| `MeepsPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `MegaMeepStunDuration` | 1.25 / 1.25 / 1.25 / 1.25 / 1.25 / 1.25 / 1.25 |
| `SecondaryDamage` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |

