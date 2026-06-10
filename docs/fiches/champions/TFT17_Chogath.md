# Cho'Gath — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Chogath`
- **Coût** : 1
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Brawler](../traits/TFT17_HPTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 45 | 81 | 145.8 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 30 / 70 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Accretion

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Deal @TotalDamage@  magic damage to the lowest Health enemy in range and permanently gain @BonusHealthPerCast@ maximum Health. If this kills them, permanently gain @BonusHealthOnKill@ maximum Health instead.(Current Bonus: +@TFTUnitProperty.:TFT17_ChoGathBonusHealth@ Health)

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BonusDamage` | 140 / 210 / 290 / 420 / 715 / 450 / 450 |
| `BonusHealthOnKill` | 35 / 30 / 40 / 70 / 115 / 35 / 35 |
| `BonusHealthPerCast` | 0 / 12 / 18 / 33 / 50 / 0 / 0 |
| `HPToTier2` | 1000 / 1000 / 1000 / 1000 / 1000 / 1000 / 1000 |
| `HPToTier3` | 2000 / 2000 / 2000 / 2000 / 2000 / 2000 / 2000 |
| `PercentMaximumHealthDamage` | 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 |

