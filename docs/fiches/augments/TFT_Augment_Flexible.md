# Flexible — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_Flexible`
- **Tier** : gold

Gain @StartingEmblems@ random Emblem. At the start of every Stage, gain a random Emblem. Your team gains @HPPerEmblem@ Health for each Emblem they are holding.

## Effets (data)

| Effet | Valeur |
|---|---|
| `BonusStages` | 99 |
| `HPPerEmblem` | 30 |
| `StartingEmblems` | 1 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
