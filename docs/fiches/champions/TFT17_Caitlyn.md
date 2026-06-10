# Caitlyn — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Caitlyn`
- **Coût** : 1
- **Traits** : [N.O.V.A.](../traits/TFT17_DRX.md), [Fateweaver](../traits/TFT17_Fateweaver.md)
- **Rôle** : ADSpecialist
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 500 | 900 | 1620 |
| Dégâts d'attaque | 65 | 117 | 210.6 |
| Vitesse d'attaque | 0.55 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 0 / 0 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Aim For The Head

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks have a @ProcChance@% Lucky chance to fire an empowered Headshot, dealing @ModifiedHeadshotDamage@ physical damage.N.O.V.A. Strike: Mark all enemies, increasing damage taken by @NovaMarkDamageAmp*100@%. The first time marked targets drop below @NovaMarkThreshold*100@% Health, Headshot them for @ModifiedNovaHeadshotDamage@ physical damage.Lucky: Check twice and take the better outcome.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `BonusDamage` | 20 / 20 / 30 / 45 / 77 / 60 / 60 |
| `Damage` | 145 / 170 / 255 / 510 / 875 / 455 / 455 |
| `NovaHeadshotModifier` | 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 / 0.4 |
| `NovaMarkDamageAmp` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `NovaMarkThreshold` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `ProcChance` | 15 / 15 / 15 / 15 / 15 / 15 / 15 |

