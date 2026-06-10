# The Mighty Mech — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Galio`
- **Coût** : 4
- **Traits** : [Mecha](../traits/TFT17_Mecha.md), [Voyager](../traits/TFT17_FlexTrait.md)
- **Rôle** : ADTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 70 | 126 | 226.8 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Gravity Matrix

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Enter a defensive stance for @DurabilityDuration@ seconds gaining @Durability*100@% Durability. While in the defensive stance, attract nearby enemy projectiles and heal @ModifiedHeal@ over the duration. When this ends, release a shockwave that deals @ModifiedDamage@ as physical damage in a @HexRange@-hex range.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ARMARScaling` | 0 / 0.8 / 1.2 / 30 / 25 / 0 / 0 |
| `Durability` | 0 / 0.2 / 0.2 / 0.6 / 0.6 / 0 / 0 |
| `DurabilityDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `Heal` | 0 / 900 / 1300 / 3000 / 5000 / 0 / 0 |
| `HexRange` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |

