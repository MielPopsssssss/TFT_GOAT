# Twisted Fate — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_TwistedFate`
- **Coût** : 1
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Fateweaver](../traits/TFT17_Fateweaver.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 500 | 900 | 1620 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Fate's Gambit

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Draw a card with a value between 1 and 9 by Lucky chance, then throw it at the target. Based on the card drawn, deal between @ModifiedDamageMin@ and @ModifiedDamageMax@ magic damage. Overkill damage bounces to the nearest enemy. 3-Star Bonus: If a 9 is thrown, generate 1 gold.Lucky: Check twice and take the better outcome.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DamageMax` | 330 / 380 / 570 / 860 / 1460 / 1000 / 1000 |
| `DamageMin` | 180 / 190 / 285 / 430 / 730 / 500 / 500 |

