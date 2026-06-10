# Flowing Tears — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_ComponentQuestTear`
- **Tier** : silver

Gain a Tear of the Goddess. After your team spends @StacksForReward@ Mana, gain @NumDelayed@ more.Mana spent: @TFTUnitProperty.item:TFT_Augment_ComponentQuest_Tracker@

## Effets (data)

| Effet | Valeur |
|---|---|
| `NumDelayed` | 2 |
| `StacksForReward` | 6500 |
| `{1ed24481}` | 1 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
