# Malicious Monetization — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_MirroredMonetization`
- **Tier** : gold

Gain @GoldContained@ gold. For the next @Rounds@ rounds, enemy champions drop @PercCost@ gold when killed.@TFTUnitProperty.item:TFT_Augment_MirroredMonetization_TotalGoldTooltip@

## Effets (data)

| Effet | Valeur |
|---|---|
| `GoldContained` | 4 |
| `PercCost` | 2 |
| `rounds` | 2 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
