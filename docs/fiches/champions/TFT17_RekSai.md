# Rek'Sai — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_RekSai`
- **Coût** : 1
- **Traits** : [Primordian](../traits/TFT17_Primordian.md), [Brawler](../traits/TFT17_HPTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Upheaval

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Heal @TotalHealing@, then briefly knock up adjacent enemies and deal @ModifiedDamage@ magic damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `APHealing` | 90 / 200 / 220 / 260 / 300 / 90 / 90 |
| `Damage` | 0 / 80 / 120 / 180 / 315 / 0 / 0 |
| `PercentMaximumHealthHealing` | 0.065 / 0.065 / 0.065 / 0.065 / 0.065 / 0.065 / 0.065 |
| `StunDuration` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

