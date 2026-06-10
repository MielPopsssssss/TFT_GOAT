# Tahm Kench — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_TahmKench`
- **Coût** : 4
- **Traits** : [Oracle](../traits/TFT17_TahmKenchUniqueTrait.md), [Brawler](../traits/TFT17_HPTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1300 | 2340 | 4212 |
| Dégâts d'attaque | 75 | 135 | 243 |
| Vitesse d'attaque | 0.5 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 50 / 110 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Tounge Lash

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Once per combat after dropping below @HPThreshold*100@% Health, gain Shield for @ShieldDuration@ seconds equal to @PercentHealingToShield*100@% of healing received this combat.Active: Heal @ModifiedHeal@, then tongue lash all enemies within two hexes dealing @ModifiedDamage@ magic damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DamageAP` | 120 / 45 / 60 / 1500 / 1500 / 870 / 870 |
| `DamageHP` | 0.02 / 0.02 / 0.02 / 0.02 / 0.02 / 0.02 / 0.02 |
| `HPThreshold` | 0.35 / 0.35 / 0.35 / 0.35 / 0.35 / 0.35 / 0.35 |
| `HealAP` | 0 / 300 / 360 / 1500 / 2500 / 0 / 0 |
| `HealHP` | 0.085 / 0.085 / 0.085 / 0.085 / 0.085 / 0.085 / 0.085 |
| `PercentHealingToShield` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |
| `ShieldDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |

