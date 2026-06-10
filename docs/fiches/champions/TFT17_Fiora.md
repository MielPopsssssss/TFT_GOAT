# Fiora — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Fiora`
- **Coût** : 5
- **Traits** : [Divine Duelist](../traits/TFT17_FioraUniqueTrait.md), [Anima](../traits/TFT17_AnimaSquad.md), [Marauder](../traits/TFT17_MeleeTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1200 | 2160 | 3888 |
| Dégâts d'attaque | 80 | 144 | 259.2 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 65 | = | = |
| Résistance magique | 65 | = | = |
| Mana (initial/max) | 0 / 70 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Perfect Bladework

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Every @NumAttacks@ attacks, reveal a Vital on the target. If a Vital exists, dash to attack it dealing @ModifiedVitalDamage@ bonus true damage and heal for @PercentHealing*100@% of the damage dealt.Active: Reveal @NumVitals@ Vitals on the target and quickly attack them all. If the target dies, remaining Vitals transfer to the nearest enemy. Upon striking the final Vital, create a two hex aura that heals allies within for @ModifiedHealing@ over @AuraDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AuraDuration` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `AuraHealing` | 250 / 200 / 250 / 999 / 999 / 999 / 999 |
| `NumAttacks` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `NumVitals` | 6 / 6 / 6 / 6 / 6 / 6 / 6 |
| `PercentHealing` | 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 / 0.15 |
| `VitalDamage` | 50 / 37 / 56 / 777 / 777 / 777 / 777 |

