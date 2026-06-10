# Nunu & Willump — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Nunu`
- **Coût** : 4
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Vanguard](../traits/TFT17_ShieldTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 40 / 145 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Calamity

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds. Summon an astrolabe to crash down on a nearby hex, dealing @ModifiedInitialDamage@ magic damage to enemies within 2 hexes. Then, push the astrolabe towards the end of the board, dealing @ModifiedFollowupDamage@ magic damage. All enemies hit by the astrolabe are knocked up for @StunDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `FollowupDamage` | 0 / 100 / 150 / 2000 / 3000 / 0 / 0 |
| `InitialDamage` | 0 / 120 / 180 / 2000 / 4000 / 0 / 0 |
| `LockoutTime` | 2.5 / 2.5 / 2.5 / 2.5 / 2.5 / 2.5 / 2.5 |
| `Shield` | 0 / 475 / 575 / 2000 / 4000 / 0 / 0 |
| `ShieldDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `StunDuration` | 0 / 1.5 / 1.75 / 8 / 16 / 0 / 0 |

