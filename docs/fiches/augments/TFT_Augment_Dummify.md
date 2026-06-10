# Dummify — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_Dummify`
- **Tier** : silver

Lose all champions on your board and bench. Gain a Training Dummy with @HealthPercent@% of their combined Health. The Training Dummy gains @HPPerStage@ Health per stage. Gain a non-Tank 2-star @ChampCost@-cost champion.

## Effets (data)

| Effet | Valeur |
|---|---|
| `ChampCost` | 2 |
| `HPPerStage` | 1000 |
| `HealthPercent` | 60 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
