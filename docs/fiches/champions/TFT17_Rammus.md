# Rammus — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Rammus`
- **Coût** : 4
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 20 / 90 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Gravitational Spin

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ shield for @ShieldDuration@ seconds. Then, strike enemies in a three hex line, dealing @ModifiedDamage@ magic damage.Meep Bonus: Reduce the damage of incoming attacks by @ModifiedFlatDR@. After being attacked @AttacksPerPassiveTrigger@ times, deal @ModifiedPassiveDamage@ magic damage in a two hex radius.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AttacksPerPassiveTrigger` | 20 / 20 / 20 / 20 / 20 / 20 / 20 |
| `DamageAP` | 100 / 50 / 75 / 700 / 600 / 800 / 800 |
| `DamageArmor` | 3 / 0.5 / 0.75 / 11 / 12 / 12 / 12 |
| `FlatDRPerMeep` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `MeepsPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `PassivePercentArmor` | 0.5 / 0.2 / 0.3 / 5 / 10 / 10 / 10 |
| `ShieldAP` | 300 / 675 / 825 / 2000 / 2500 / 300 / 300 |
| `ShieldDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |

