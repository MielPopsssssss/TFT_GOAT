# Sona — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Sona`
- **Coût** : 5
- **Traits** : [Commander](../traits/TFT17_SonaUniqueTrait.md), [Psionic](../traits/TFT17_PsyOps.md), [Shepherd](../traits/TFT17_SummonTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 900 | 1620 | 2916 |
| Dégâts d'attaque | 35 | 63 | 113.4 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 0 / 25 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Psionic Crush

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Hurl a chunk of magnetic debris at the nearest target without one, dealing @ModifiedDebrisDamage@ magic damage and sticking it to them. If an enemy with debris dies, it passes to the nearest enemy without one.Every @NumCasts@ casts, instead rip off all debris dealing @ModifiedDebrisRipDamage@ magic damage, then crush all the debris onto the target, dealing @ModifiedSlamDamage@ magic damage and briefly stunning them.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DebrisDamage` | 300 / 300 / 450 / 999 / 999 / 2 / 2 |
| `DebrisRipDamage` | 160 / 120 / 180 / 999 / 2000 / 0 / 0 |
| `NumCasts` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `SlamDamage` | 2.5 / 720 / 1100 / 9999 / 9999 / 2.5 / 2.5 |
| `StunDuration` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

