# Worth the Wait II — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_WorthTheWaitPrismatic`
- **Tier** : prismatic

Gain @InitialCopies@ copies of a random @unittier@-cost champion. Gain another copy of them at the start of each round for the rest of the game.Champion: @TFTUnitProperty.item:TFT_Augment_WorthTheWait@

## Effets (data)

| Effet | Valeur |
|---|---|
| `AdditionalCopies` | 99 |
| `InitialCopies` | 2 |
| `UnitTier` | 2 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
