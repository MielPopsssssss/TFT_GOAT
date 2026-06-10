# Mordekaiser — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Mordekaiser`
- **Coût** : 2
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Conduit](../traits/TFT17_ManaTrait.md), [Vanguard](../traits/TFT17_ShieldTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 950 | 1710 | 3078 |
| Dégâts d'attaque | 40 | 72 | 129.6 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Indestructible

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedInitialShield@ Shield. Each second for the next @AugmentedDuration@@Duration@ seconds, gain @ModifiedShieldPerProc@ more Shield and deal @ModifiedDamagePerProc@ magic damage to adjacent enemies. When this ability ends, consume the remaining Shield and heal for @HealRefund*100@% of its value.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AugmentedDuration` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |
| `DamagePerProc` | 0 / 45 / 70 / 100 / 170 / 0 / 0 |
| `Duration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `HealRefund` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |
| `InitialShield` | 0 / 300 / 375 / 500 / 650 / 200 / 240 |
| `ShieldPerProc` | 0 / 75 / 90 / 105 / 120 / 0 / 0 |

