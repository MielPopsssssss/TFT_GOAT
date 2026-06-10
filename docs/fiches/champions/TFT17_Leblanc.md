# LeBlanc — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Leblanc`
- **Coût** : 4
- **Traits** : [Arbiter](../traits/TFT17_ADMIN.md), [Shepherd](../traits/TFT17_SummonTrait.md)
- **Rôle** : APCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 0 | 0 | 0 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 0 / 40 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Fracture Reality

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks deal @ModifiedBaseAttackDamage@ magic damage instead.Active: Summon @NumClones@ clones that attack alongside for @NumAttacks@ attacks, dealing @CloneDamageMultiplier*100@% damage. For their final attack, clones fire a bolt that deals @ModifiedBoltDamage@ magic damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BasicAttackDamage` | 0 / 62 / 93 / 250 / 450 / 0 / 0 |
| `BoltDamage` | 0 / 80 / 120 / 750 / 540 / 0 / 0 |
| `CloneDamageMultiplier` | 0 / 0.25 / 0.25 / 1.5 / 1 / 0 / 0 |
| `NumAttacks` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `NumClones` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |

