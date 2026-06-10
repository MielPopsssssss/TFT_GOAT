# Kai'Sa — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Kaisa`
- **Coût** : 3
- **Traits** : [Dark Star](../traits/TFT17_DarkStar.md), [Rogue](../traits/TFT17_AssassinTrait.md)
- **Rôle** : ADCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 650 | 1170 | 2106 |
| Dégâts d'attaque | 45 | 81 | 145.8 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 25 | = | = |
| Résistance magique | 25 | = | = |
| Mana (initial/max) | 0 / 50 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Bullet Cluster

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: On takedown, gain @ManaPerKill@ mana.Active: Fire @BaseNumMissiles@ missiles in a @HexRange@-hex radius around the current target, dealing @TotalDamage@ physical damage each.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 0 / 30 / 45 / 72 / 136 / 0 / 0 |
| `APDamage` | 0 / 3 / 5 / 7 / 13 / 0 / 0 |
| `BaseNumMissiles` | 16 / 16 / 16 / 16 / 16 / 16 / 16 |
| `HexRange` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `ManaPerKill` | 10 / 10 / 10 / 10 / 10 / 10 / 10 |
| `PercentTargetedMissiles` | 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 / 0.5 |
| `SpellDuration` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |

