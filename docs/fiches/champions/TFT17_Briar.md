# Briar — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Briar`
- **Coût** : 1
- **Traits** : [Anima](../traits/TFT17_AnimaSquad.md), [Primordian](../traits/TFT17_Primordian.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 35 | 63 | 113.4 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 35 | = | = |
| Résistance magique | 35 | = | = |
| Mana (initial/max) | 0 / 40 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Fish Frenzy

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: For every @PercentMissingHealth@% missing Health, gain @ModifiedAS@% Attack SpeedActive: Deal @ModifiedDamage@ physical damage to the target, increased by @PercentBonusDamage*100@% if they're a tank.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 3.3 / 120 / 180 / 285 / 485 / 3.3 / 3.3 |
| `APDamage` | 0 / 10 / 15 / 25 / 45 / 0 / 0 |
| `AS` | 2 / 2 / 2 / 2.5 / 2.5 / 2 / 2 |
| `PercentBonusDamage` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `PercentMissingHealth` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

