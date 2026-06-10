# Teemo — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Teemo`
- **Coût** : 1
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Shepherd](../traits/TFT17_SummonTrait.md)
- **Rôle** : APCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 450 | 810 | 1458 |
| Dégâts d'attaque | 15 | 27 | 48.6 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Double Time

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks deal @ModifiedHitDamage@ bonus magic damage and an additional @ModifiedMagicDamage@ stacking magic damage over @PoisonDuration@ seconds. While an enemy has @GrooveStacks@ or more stacks, Teemo is in {{TFT17_SpaceGroove_TheGroove}}.Active: Gain @AttackSpeed*100@% Attack Speed for @ActiveAttacks@ attacks.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ActiveAttacks` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `AttackSpeed` | 1.5 / 1.5 / 1.5 / 1.5 / 1.5 / 1.5 / 1.5 |
| `GrooveStacks` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `HitDamage` | 100 / 30 / 45 / 100 / 170 / 95 / 95 |
| `MagicDamage` | 60 / 65 / 95 / 170 / 300 / 180 / 180 |
| `PoisonDuration` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |

