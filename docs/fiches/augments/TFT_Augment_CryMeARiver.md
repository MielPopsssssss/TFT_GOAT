# Cry Me A River — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT_Augment_CryMeARiver`
- **Tier** : gold

Gain a Tear of the Goddess. Your team gains @RegenBonus@ Mana Regen. After @DelayTime@ seconds in combat, increase this to @UpgradedRegenBonus@.

## Effets (data)

| Effet | Valeur |
|---|---|
| `DelayTime` | 12 |
| `RegenBonus` | 1 |
| `UpgradedRegenBonus` | 3 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
