# Woven Magic — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_TheVidalion`
- **Tier** : prismatic

Gain a random item component. Every @ManaPerComponent@ Mana your team spends grants an additional component (max @TFTUnitProperty.trait:TFT_Augment_TheVidalion_NumComponents@/@ComponentMax@).Mana spent: @TFTUnitProperty.trait:TFT_Augment_TheVidalion_TrackedMana@/@ManaPerComponent@

## Effets (data)

| Effet | Valeur |
|---|---|
| `ComponentMax` | 3 |
| `ManaPerComponent` | 2200 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
