# Miss Fortune — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_MissFortune`
- **Coût** : 3
- **Traits** : [Gun Goddess](../traits/TFT17_MissFortuneUniqueTrait.md), [Choose Trait](../traits/TFT17_MissFortuneUndeterminedTrait.md)
- **Rôle** : —
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.75 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 0 / 100 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Gun Goddess Arsenal

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Field Miss Fortune to choose whether she activates Conduit Mode, Challenger Mode, or Replicator Mode. The chosen mode determines her ability and her trait.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Tier1Damage` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `Tier2Damage` | 2.5 / 2.5 / 2.5 / 2.5 / 2.5 / 2.5 / 2.5 |
| `Tier3Damage` | 3.3 / 3.3 / 3.3 / 3.3 / 3.3 / 3.3 / 3.3 |
| `Tier4Damage` | 0 / 4.5 / 4.5 / 9 / 0 / 0 / 0 |
| `Tier5Damage` | 0 / 6 / 6 / 60 / 0 / 0 / 0 |

