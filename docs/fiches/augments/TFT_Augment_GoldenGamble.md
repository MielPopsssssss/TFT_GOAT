# Golden Gamble — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_GoldenGamble`
- **Tier** : prismatic

Gain @gold@ gold and flip a coin. If heads, gain a Radiant Lucky Item Chest. If tails, gain @CompletedAnvils@ Completed item anvils.@TFTUnitProperty.item:TFT_Augment_GoldenGamble_Tooltip@

## Effets (data)

| Effet | Valeur |
|---|---|
| `CompletedAnvils` | 2 |
| `Gold` | 1 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
