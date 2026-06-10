# Urgot — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Urgot`
- **Coût** : 3
- **Traits** : [Mecha](../traits/TFT17_Mecha.md), [Brawler](../traits/TFT17_HPTank.md), [Marauder](../traits/TFT17_MeleeTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 600 | 1080 | 1944 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 2 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Unstoppable Dreadnought

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive - Proximity Blast: Whenever an enemy enters a @ShotgunRange@ hex radius, fire a blast in a cone towards the closest adjacent hex that deals @ModifiedShotgunDamage@ physical damage with @FalloffPerHex*100@% falloff per hex. Each adjacent hex has a @ShotgunCooldown@ second cooldown, and starts combat on cooldown.Active: Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds and reposition up to one hex to maximize the number of targets within Proximity Blast's radius. Reset Proximity Blast's cooldowns.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `FalloffPerHex` | 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 |
| `ShieldAmount` | 200 / 150 / 175 / 200 / 225 / 420 / 420 |
| `ShieldDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `ShotgunCooldown` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `ShotgunDamage` | 90 / 85 / 125 / 200 / 275 / 1.8 / 1.8 |

