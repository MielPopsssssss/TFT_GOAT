# Heart of the Swarm — fiche augment

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Augment_PrimordianPrismaticAugment`
- **Tier** : prismatic

All 3-star champions now count towards Swarmling power. At level @LevelRequirement@, while fielding @Num3StarUnits@ unique 3-star champions, Primordians summon the Apex Primordian. Gain 3 Primordian Champions and 2 Tiny Duplicators.Unique 3-Star Champions Fielded: @TFTUnitProperty.item:TFT17_Augment_PrimordianPrismaticAugment_TotalStarredUnits@ / @Num3StarUnits@Levels: @TFTUnitProperty.item:TFT17_Augment_PrimordianPrismaticAugment_TotalLevel@ / @LevelRequirement@

## Effets (data)

| Effet | Valeur |
|---|---|
| `LevelRequirement` | 9 |
| `Num3StarUnits` | 6 |

## Statut combat moteur

🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)
