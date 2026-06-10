# Blitzcrank — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Blitzcrank`
- **Coût** : 5
- **Traits** : [Party Animal](../traits/TFT17_BlitzcrankUniqueTrait.md), [Space Groove](../traits/TFT17_SpaceGroove.md), [Vanguard](../traits/TFT17_ShieldTank.md)
- **Rôle** : APFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1000 | 1800 | 3240 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 50 | = | = |
| Résistance magique | 50 | = | = |
| Mana (initial/max) | 20 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Party Crasher

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Every @BoltCooldown@ seconds, call down a bolt on the highest Health nearby enemy that deals @ModifiedBoltDamage@ magic damage.Active: Summon a disco ball at the largest clump of enemies, then knock up the current target into it, dealing @ModifiedUppercutDamage@ magic damage. They crash down into the disco ball, dealing @ModifiedExplosionDamage@ magic damage in a three hex radius. Enter {{TFT17_SpaceGroove_TheGroove}} for @GrooveDurationPerTarget@ second per enemy hit.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BoltCooldown` | 2 / 2 / 2 / 0.5 / 1 / 1 / 1 |
| `BoltDamage` | 90 / 60 / 90 / 150 / 150 / 150 / 150 |
| `ExplosionDamage` | 200 / 175 / 265 / 5000 / 5000 / 5000 / 5000 |
| `GrooveDurationPerTarget` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `UppercutDamage` | 170 / 150 / 225 / 999 / 2000 / 789 / 5000 |

