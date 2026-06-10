# Meepsie — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_IvernMinion`
- **Coût** : 2
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Shepherd](../traits/TFT17_SummonTrait.md), [Voyager](../traits/TFT17_FlexTrait.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 950 | 1710 | 3078 |
| Dégâts d'attaque | 65 | 117 | 210.6 |
| Vitesse d'attaque | 0.55 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 50 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Meep Impact

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Heal @ModifiedHeal@ Health over @HealDuration@ seconds. Slam the target, dealing @ModifiedDamage@ magic damage and knocking up for @StunDuration@ seconds. The impact creates meepwaves that deal @PercentEffects*100@% of these effects in the target's row.Meep Bonus: Meeps water Meepsie's flower, increasing all incoming Healing and Shielding by @ModifiedHealingAndShielding@.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 200 / 160 / 240 / 360 / 600 / 450 / 450 |
| `HealDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `HealingAP` | 80 / 380 / 430 / 600 / 770 / 80 / 80 |
| `HealingAndShieldingPerAstro` | 0.12 / 0.12 / 0.12 / 0.12 / 0.12 / 0.12 / 0.12 |
| `HealingPercentHealth` | 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 |
| `MeepsPerAstro` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `PercentEffects` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `StunDuration` | 1.5 / 1.5 / 1.75 / 2 / 2.25 / 1.5 / 1.5 |

