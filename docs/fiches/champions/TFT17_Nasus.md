# Nasus — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Nasus`
- **Coût** : 1
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Vanguard](../traits/TFT17_ShieldTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 40 | 72 | 129.6 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 60 / 120 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Groovin' Susan

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Transform for @Duration@ seconds, temporarily gaining @MaxHealth@ max Health, entering {{TFT17_SpaceGroove_TheGroove}}, and dealing @ModifiedDamage@ magic damage to adjacent enemies each second.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DamageAP` | 18 / 30 / 45 / 70 / 120 / 48 / 48 |
| `DamageHealth` | 0.02 / 0.02 / 0.02 / 0.02 / 0.02 / 0.02 / 0.02 |
| `Duration` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |
| `MaxHealth` | 400 / 250 / 350 / 550 / 750 / 700 / 700 |

