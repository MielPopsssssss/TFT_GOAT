# Samira — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Samira`
- **Coût** : 3
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Sniper](../traits/TFT17_RangedTrait.md)
- **Rôle** : ADCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 25 | = | = |
| Résistance magique | 25 | = | = |
| Mana (initial/max) | 0 / 60 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Jump and Jive

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Whenever an enemy is knocked up, shoot them, dealing @ModifiedPassiveDamage@ physical damage and entering {{TFT17_SpaceGroove_TheGroove}} for @GrooveDuration@ seconds.Active: Unleash a volley of bullets at the target, dealing @ModifiedDamage@ physical damage and knocking up for @StunDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 260 / 375 / 560 / 900 / 1555 / 810 / 810 |
| `GrooveDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `PassiveAD` | 60 / 55 / 80 / 130 / 220 / 210 / 210 |
| `PassiveAP` | 20 / 10 / 15 / 25 / 35 / 70 / 70 |
| `StunDuration` | 1.25 / 1.25 / 1.25 / 1.25 / 1.25 / 1.25 / 1.25 |

