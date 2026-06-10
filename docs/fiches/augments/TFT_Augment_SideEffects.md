# Side Effects — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_SideEffects`
- **Tier** : gold

When an ally is healed, they deal @HealConversionPct*100@% of the healing to their target as magic damage. Every @HealInterval@ seconds, allies heal for @HealPct*100@% of their max Health.

## Effets (data)

| Effet | Valeur |
|---|---|
| `HealConversionPct` | 0.5 |
| `HealInterval` | 5 |
| `HealPct` | 0.04 |

## Statut combat moteur

✅ effet combat codé (`engine/augments_set17`)
