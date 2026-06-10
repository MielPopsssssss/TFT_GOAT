# Pilfer — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_Pilfer`
- **Tier** : gold

Each round, gain a 1-star copy of the first champion you killed last combat. The first time you gain @GoldRequired@ gold worth of champions in this way, gain a Thief's Gloves. @TFTUnitProperty.item:TFT_Augment_Pilfer_Tooltip@

## Effets (data)

| Effet | Valeur |
|---|---|
| `goldrequired` | 21 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
