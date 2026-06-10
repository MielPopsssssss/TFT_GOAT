# Gwen — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Gwen`
- **Coût** : 2
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : APReaper
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 750 | 1350 | 2430 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 50 | = | = |
| Résistance magique | 50 | = | = |
| Mana (initial/max) | 0 / 30 | = | = |
| Portée | 2 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Dance n' Dice

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks deal magic damage. Gwen is in {{TFT17_SpaceGroove_TheGroove}} while targeting an enemy below @GrooveThreshold*100@% Health.Active: Dash to a nearby hex to snip the lowest percent Health enemy, dealing @ModifiedDamage@ magic damage to the target and @ModifiedAreaDamage@ magic damage to enemies in a cone. If this kills, dash and snip again at @ResetDamage*100@% damage!

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AreaDamage` | 120 / 75 / 110 / 190 / 325 / 420 / 420 |
| `BonusDashRange` |  |
| `Damage` | 180 / 145 / 220 / 410 / 700 / 840 / 840 |
| `GrooveThreshold` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |
| `ResetDamage` | 0.65 / 0.65 / 0.65 / 0.65 / 0.65 / 0.65 / 0.65 |

