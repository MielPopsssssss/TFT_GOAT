# Savings Account — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_SavingsAccount`
- **Tier** : gold

After you earn @GoldRequired@ gold in interest, gain @GoldToGain@ gold. Your max interest is increased to @InterestCap@. Gain @GoldNow@ gold now.Gold earned: @TFTUnitProperty.item:TFT_Augment_SavingsAccount_Tracker@

## Effets (data)

| Effet | Valeur |
|---|---|
| `GoldNow` | 4 |
| `GoldToGain` | 25 |
| `InterestCap` | 7 |
| `goldrequired` | 50 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
