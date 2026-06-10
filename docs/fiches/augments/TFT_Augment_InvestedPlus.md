# Invested+ — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_InvestedPlus`
- **Tier** : prismatic

Gain @Gold@ gold. After every combat, gain 1 Shop reroll for every @GoldPerReroll@ gold above @GoldThreshold@ (max @MaxGold@ gold).

## Effets (data)

| Effet | Valeur |
|---|---|
| `Gold` | 26 |
| `GoldPerReroll` | 10 |
| `GoldThreshold` | 50 |
| `MaxGold` | 80 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
