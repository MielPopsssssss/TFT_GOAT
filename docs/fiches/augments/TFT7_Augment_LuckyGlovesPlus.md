# Lucky Gloves+ — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT7_Augment_LuckyGlovesPlus`
- **Tier** : prismatic

Thief's Gloves will always give your champions recommended items. Gain @NumGloves@ Sparring Gloves now, then another after @DelayTurns@ player combats.

## Effets (data)

| Effet | Valeur |
|---|---|
| `DelayTurns` | 4 |
| `NumGloves` | 2 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
