# Forward Thinking — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_ForwardThinking`
- **Tier** : gold

Lose all your gold. After @Rounds@ player combats, gain back the original amount and another @BaseGold@ gold.Incoming Gold: @TFTUnitProperty.item:TFT_Augment_ForwardThinkingGold@

## Effets (data)

| Effet | Valeur |
|---|---|
| `BaseGold` | 70 |
| `rounds` | 5 |
| `{8f9a1368}` | 1 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
