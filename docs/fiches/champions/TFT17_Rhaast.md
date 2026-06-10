# Rhaast — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Rhaast`
- **Coût** : 3
- **Traits** : [Redeemer](../traits/TFT17_RhaastUniqueTrait.md)
- **Rôle** : ADTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1200 | 2160 | 3888 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 30 / 90 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Divine Scythe

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Gain @Durability*100@% Durability for @Duration@ seconds, healing @ModifiedHeal@ over the duration. Afterwards, slash forward in a line, dealing @ModifiedDamage@ physical damage to enemies hit and knocking them up for @KnockupDuration@ second.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 0.2 / 120 / 180 / 300 / 510 / 0.2 / 0.2 |
| `Durability` | 0.2 / 0.2 / 0.2 / 0.2 / 0.2 / 0.2 / 0.2 |
| `Duration` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `HealAmount` | 1 / 500 / 550 / 650 / 850 / 0 / 0 |
| `KnockupDuration` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

