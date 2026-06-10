# Shen — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Shen`
- **Coût** : 5
- **Traits** : [Bulwark](../traits/TFT17_ShenUniqueTrait.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : APFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 65 | = | = |
| Résistance magique | 65 | = | = |
| Mana (initial/max) | 20 / 70 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Reality Tear

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: On cast, attacks gain @ModifiedBonusDamage@ stacking bonus magic damage. Starting from the third cast, gain true damage instead.Active: Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds, then slice open a rift on the largest group of champions dealing the Passive's bonus damage to all enemies within. Enemies have their Attack Speed slowed by @ASSlow*100@% while allies within gain @BonusAS*100@% Attack Speed, both rapidly decaying over @BuffDebuffDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ASSlow` | 0.5 / 0.5 / 0.5 / 0.99 / 0.99 / 0.99 / 0.99 |
| `BonusAS` | 0.8 / 0.8 / 0.8 / 9.99 / 99 / 99 / 99 |
| `BonusDamageOnAttack` | 50 / 25 / 40 / 777 / 777 / 777 / 777 |
| `BuffDebuffDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `DamageHP` | 0.01 / 0.01 / 0.01 / 0.01 / 0.01 / 0.01 / 0.01 |
| `ShieldAP` | 0 / 200 / 250 / 3456 / 3456 / 3456 / 3456 |
| `ShieldDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `ShieldHP` | 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 |

