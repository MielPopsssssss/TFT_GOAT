# Vex — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Vex`
- **Coût** : 5
- **Traits** : [Doomer](../traits/TFT17_VexUniqueTrait.md)
- **Rôle** : APCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 15 | 27 | 48.6 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 0 / 60 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Lend Me a Hand, Shadow!

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Every time Vex attacks, Shadow strikes a nearby enemy, dealing @ModifiedShadowHandDamage@ magic damage. Whenever an enemy is struck @NumStrikesForPassive@ times by Shadow, Shadow strikes them again.Active: Shadow launches @NumActiveStrikes@ empowered strikes, dealing @ModifiedShadowHandMagicDamage@ magic damage instead.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `NumActiveStrikes` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `NumStrikesForPassive` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `ShadowHandDamage` | 2.5 / 30 / 45 / 250 / 1000 / 2.5 / 2.5 |
| `ShadowHandMagicDamage` | 200 / 130 / 195 / 1000 / 9999 / 200 / 200 |

