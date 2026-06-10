# Solo Leveling — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_SoloLeveling`
- **Tier** : gold

For the next @NumCombats@ combats, your team size is 1 but the champion you field has massively increased stats. Gain @XPPerKill@ XP for every kill they get. Afterwards, gain @NumComponents@ item components.

## Effets (data)

| Effet | Valeur |
|---|---|
| `ADBonus` | 0.5 |
| `APBonus` | 50 |
| `ASBonus` | 0.5 |
| `DamageAmpBonus` | 0.3 |
| `DurabilityBonus` | 0.2 |
| `FlatHealthBonus` | 525 |
| `NumCombats` | 5 |
| `NumComponents` | 2 |
| `OmnivampBonus` | 0.2 |
| `XPPerKill` | 1 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
