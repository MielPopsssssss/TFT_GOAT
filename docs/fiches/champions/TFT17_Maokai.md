# Maokai — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Maokai`
- **Coût** : 3
- **Traits** : [N.O.V.A.](../traits/TFT17_DRX.md), [Brawler](../traits/TFT17_HPTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1100 | 1980 | 3564 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 30 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Grasp of Convergence

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Gain @PassiveRatio*100@% more max Health from all sources.Active: Converge an X-shape of vines on the target, dealing @DamageTotal@ magic damage to each enemy hit and Stunning them for @StunDuration@ seconds. N.O.V.A. Strike: Send forth a wave of dragons that stun all enemies for @NovaStunDuration@ seconds. For the rest of combat, Maokai's attacks deal @ModifiedNovaDamage@ bonus physical damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 100 / 100 / 150 / 225 / 300 / 0 / 0 |
| `NovaHealthDamage` | 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 / 0.08 |
| `NovaStunDuration` | 1.5 / 1.5 / 1.5 / 1.75 / 2 / 2 / 2 |
| `PassiveRatio` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `StunDuration` | 1.5 / 1.5 / 1.5 / 1.75 / 2 / 2 / 0 |

