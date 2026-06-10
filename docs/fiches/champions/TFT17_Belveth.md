# Bel'Veth — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Belveth`
- **Coût** : 2
- **Traits** : [Primordian](../traits/TFT17_Primordian.md), [Challenger](../traits/TFT17_ASTrait.md), [Marauder](../traits/TFT17_MeleeTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 750 | 1350 | 2430 |
| Dégâts d'attaque | 47 | 84.6 | 152.28 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 2 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Tidal Slashes

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Unleash a flurry of @TotalNumSlashes@ slashes at the current target over @SlashDuration@ seconds, dealing @TotalDamage@ physical damage each.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 50 / 20 / 30 / 45 / 77 / 0 / 0 |
| `APDamage` | 0 / 3 / 5 / 7 / 12 / 0 / 0 |
| `BaseNumSlashes` | 12 / 12 / 12 / 12 / 12 / 12 / 12 |
| `BonusASBreakpoint` | 25 / 25 / 25 / 25 / 25 / 25 / 25 |
| `NumProcsPerSimulatedAttack` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `SlashDuration` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |

