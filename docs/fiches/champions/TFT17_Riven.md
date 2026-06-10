# Riven — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Riven`
- **Coût** : 4
- **Traits** : [Timebreaker](../traits/TFT17_Timebreaker.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : HFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1100 | 1980 | 3564 |
| Dégâts d'attaque | 0 | 0 | 0 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 0 / 20 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Time Warp

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: This Ability adapts to Attack Damage or Ability Power, whichever is higher. Attacks deal @ModifiedPassiveAPDamage@ magic@ModifiedPassiveADDamage@ physical damage.Active: Dash to a nearby hex, gaining @Shield@ Shield for @ShieldDuration@ seconds and slashing adjacent enemies for @ModifiedAPDamage@ magic@ModifiedADDamage@ physical damage. Every third cast, leap into the air and launch a wave of energy that deals @ModifiedAPWaveDamage@ magic@ModifiedADWaveDamage@ physical damage to enemies in a line.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 180 / 90 / 135 / 1000 / 1250 / 0 / 0 |
| `DashRange` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `PassiveDamage` | 50 / 75 / 115 / 300 / 400 / 170 / 170 |
| `Shield` | 160 / 100 / 150 / 1200 / 900 / 0 / 0 |
| `ShieldDuration` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `SpecialCastCount` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `ThirdCastConeHexRange` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `WaveDamage` | 300 / 160 / 240 / 2000 / 1350 / 0 / 0 |

