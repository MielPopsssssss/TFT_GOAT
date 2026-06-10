# Aurora — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Aurora`
- **Coût** : 3
- **Traits** : [Anima](../traits/TFT17_AnimaSquad.md), [Voyager](../traits/TFT17_FlexTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 25 | = | = |
| Résistance magique | 25 | = | = |
| Mana (initial/max) | 20 / 80 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Hopped-Up Hacks

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Open a @SpellHexRadius@ hex rift containing the target, Hacking enemies within for @HexDuration@ seconds and dealing @ModifiedDamage@ magic damage to each, plus @ModifiedSplitDamage@ magic damage split between all enemies hit.Hacked enemies store @HexPercent*100@% of all damage they take. When the Hack ends, they take true damage equal to the stored damage. The Hack ends early if it would kill the target.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 2.5 / 80 / 120 / 190 / 340 / 2.5 / 2.5 |
| `HexDuration` | 4 / 4 / 4 / 4 / 4 / 4 / 4 |
| `HexPercent` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `SpellHexRadius` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `SplitDamage` | 3 / 400 / 600 / 960 / 1650 / 3 / 3 |

