# Pantheon — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Pantheon`
- **Coût** : 2
- **Traits** : [Timebreaker](../traits/TFT17_Timebreaker.md), [Brawler](../traits/TFT17_HPTank.md), [Replicator](../traits/TFT17_APTrait.md)
- **Rôle** : ADTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 20 / 80 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Advanced Defences

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @ModifiedShield@ Shield and @Durability*100@% Durability for @Duration@ seconds. Over the duration, deal @ModifiedDamage@ physical damage each second to enemies in a cone.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `APShield` | 0 / 275 / 300 / 500 / 700 / 0 / 0 |
| `Durability` | 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 |
| `Duration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `PercentHealthShield` | 0.06 / 0.06 / 0.06 / 0.06 / 0.06 / 0.06 / 0.06 |
| `TrueDamagePerSecond` | 0 / 30 / 45 / 70 / 120 / 0 / 0 |

