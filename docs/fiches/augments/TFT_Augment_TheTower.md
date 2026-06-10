# The Tower — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_TheTower`
- **Tier** : silver

Gain a giant Training Dummy with increased Health (increases with Stage). Every @ZapInterval@ seconds, it zaps the @ZapCount@ nearest enemies dealing @MaxHealthPct*100@% max Health true damage.

## Effets (data)

| Effet | Valeur |
|---|---|
| `MaxHealthPct` | 0.05 |
| `ZapCount` | 3 |
| `ZapInterval` | 4 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
