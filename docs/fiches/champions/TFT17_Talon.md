# Talon — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Talon`
- **Coût** : 1
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : ADReaper
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 35 | 63 | 113.4 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 35 | = | = |
| Résistance magique | 35 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Diviner's Judgment

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Stab the target, causing them to bleed for @ModifiedBleedDamage@ physical damage over @BleedDuration@ seconds. After the attack, leap to the highest percent Health enemy within @HexDistance@ hexes.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADBleedDamage` | 2.5 / 430 / 645 / 1000 / 1700 / 2.5 / 2.5 |
| `APBleedDamage` | 0 / 60 / 90 / 135 / 230 / 0 / 0 |
| `BleedDuration` | 18 / 18 / 18 / 18 / 18 / 18 / 18 |
| `HexDistance` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |

