# Bard — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Bard`
- **Coût** : 5
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Conduit](../traits/TFT17_ManaTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 0 / 65 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Ultra Friendly Object

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Summon a flying saucer over the current target that lasts @AugmentedDuration@@Duration@ seconds. Each second it deals @ModifiedDamagePerSecond@ magic damage to the target, plus @ModifiedSplitDamagePerSecond@ magic damage split between all enemies within @SecondaryHexRange@ hex. The saucer deals @TankDamageIncrease*100@% increased damage to Tanks.If an enemy under the UFO dies, Bard has a @AbductChance*100@% chance to abduct them and create a 1-star copy on your bench.Meep bonus: On combat start, grant the nearest @ModifiedNumAllies@ Meeple allies an additional Meep.Friends abducted: @TFTUnitProperty.:TFT17_Bard_FriendsAbducted@

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AbductChance` | 0.4 / 0.15 / 0.2 / 1 / 0.4 / 0.4 / 0.4 |
| `AugmentedDuration` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `CanAbductSecondaryTargets` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `DamagePerSecond` | 2 / 220 / 330 / 3000 / 5000 / 2 / 2 |
| `Duration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `MeepsPerMeep` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `PVEAbductionChanceModifier` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `SecondaryHexRange` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `SplitDamagePerSecond` | 0 / 135 / 205 / 1500 / 2500 / 0 / 0 |
| `TankDamageIncrease` | 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 |

