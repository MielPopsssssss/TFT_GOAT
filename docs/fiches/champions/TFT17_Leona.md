# Leona — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Leona`
- **Coût** : 1
- **Traits** : [Arbiter](../traits/TFT17_ADMIN.md), [Vanguard](../traits/TFT17_ShieldTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 50 / 110 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Shield of Daybreak

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds. Bash the current target, dealing @ModifiedDamage@ magic damage and stunning them for @StunDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 0 / 100 / 150 / 225 / 385 / 0 / 0 |
| `DefenseToDamageRatio` | 0 / 1.2 / 1.8 / 2.7 / 4.6 / 0 / 0 |
| `ShieldAmount` | 0 / 420 / 480 / 620 / 760 / 0 / 0 |
| `ShieldDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `StunDuration` | 0 / 1.75 / 1.75 / 2 / 2.25 / 0 / 0 |

