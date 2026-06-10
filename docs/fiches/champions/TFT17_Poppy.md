# Poppy — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Poppy`
- **Coût** : 1
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 30 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Huddle Up!

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds. For the duration, allies within two hexes gain @ModifiedResists@ Armor and Magic Resistance.Meep Bonus: Meeps grant @ModifiedMeepShield@ Shield to the nearest @ModifiedNumMeeps@ allies for @ShieldDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `MeepShield` | 100 / 125 / 160 / 210 / 260 / 300 / 300 |
| `MeepsPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `Resists` | 36 / 15 / 25 / 60 / 100 / 36 / 36 |
| `Shield` | 300 / 400 / 475 / 575 / 675 / 390 / 390 |
| `ShieldDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |

