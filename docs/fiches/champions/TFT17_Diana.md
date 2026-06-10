# Diana — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Diana`
- **Coût** : 3
- **Traits** : [Arbiter](../traits/TFT17_ADMIN.md), [Challenger](../traits/TFT17_ASTrait.md)
- **Rôle** : APFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 0 | 0 | 0 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 50 | = | = |
| Résistance magique | 50 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Pale Cascade

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks deal @ModifiedBonusDamageToAttacks@ bonus magic damage.Active: Gain @ModifiedShield@ Shield and summon 3 encircling orbs for @ShieldDuration@ seconds. Orbs deal @ModifiedDamage@ magic damage to enemies they pass through, and rotate faster based on Attack Speed.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ASDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `AttackSpeed` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `BaseAttackDamagePercent` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `BaseDamage` | 50 / 60 / 90 / 145 / 250 / 240 / 330 |
| `BonusDamageToAttacks` | 0 / 52 / 78 / 135 / 230 / 0 / 0 |
| `CleaveDamage` | 100 / 100 / 150 / 240 / 330 / 330 / 330 |
| `NumAttacks` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `Shield` | 100 / 275 / 325 / 475 / 460 / 100 / 100 |
| `ShieldDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `ShieldPercent` | 0.05 / 0.05 / 0.07 / 0.1 / 0.13 / 0.05 / 0.05 |

