# Illaoi — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Illaoi`
- **Coût** : 3
- **Traits** : [Anima](../traits/TFT17_AnimaSquad.md), [Vanguard](../traits/TFT17_ShieldTank.md), [Shepherd](../traits/TFT17_SummonTrait.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1100 | 1980 | 3564 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 50 | = | = |
| Résistance magique | 50 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Test of Spirit

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ Shield for @Duration@ seconds. Over the duration, drain @ModifiedHealthDrain@ Health from the nearest @NumEnemies@ enemies. Then slam down, dealing @ModifiedDamage@ magic damage to all enemies within 2 hexes.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 80 / 80 / 120 / 180 / 240 / 240 / 240 |
| `Duration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `HealthDrain` | 40 / 55 / 85 / 130 / 175 / 240 / 240 |
| `NumEnemies` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `Shield` | 250 / 450 / 525 / 650 / 775 / 400 / 400 |

