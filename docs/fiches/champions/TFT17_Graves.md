# Graves — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Graves`
- **Coût** : 5
- **Traits** : [Factory New](../traits/TFT17_GravesTrait.md)
- **Rôle** : ADCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 0 / 60 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Collateral Damage

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks fire @NumProjectiles@ projectiles in a cone that deal @ModifiedPassiveDamage@ physical damage each.Active: Fire an explosive shell that deals @ModifiedDamage@ physical damage to the target, and @ModifiedSecondaryDamage@ physical damage to adjacent enemies.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 400 / 390 / 585 / 5555 / 5555 / 5555 / 5555 |
| `NumProjectiles` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `PassivePercentBAD` | 0.33 / 0.33 / 0.33 / 0.33 / 0.33 / 0.33 / 0.33 |
| `SecondaryDamageAD` | 120 / 135 / 200 / 3333 / 3333 / 3333 / 3333 |
| `SecondaryDamageAP` | 30 / 30 / 45 / 777 / 777 / 777 / 777 |

