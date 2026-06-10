# Lulu — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Lulu`
- **Coût** : 3
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Replicator](../traits/TFT17_APTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 25 | = | = |
| Résistance magique | 25 | = | = |
| Mana (initial/max) | 0 / 55 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — It's Raining Stars

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Gain a different secondary effect each game based on the Stargazer constellation.Active: Call down something from the sky, dealing @ModifiedDamage@ magic damage to @NumEnemies@ nearby enemies and do some special effect based on this game's Stargazer Constellation.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 2 / 150 / 225 / 360 / 495 / 2 / 2 |
| `NumEnemies` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |

