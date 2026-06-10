# Ornn — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Ornn`
- **Coût** : 3
- **Traits** : [Space Groove](../traits/TFT17_SpaceGroove.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 950 | 1710 | 3078 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 40 | = | = |
| Résistance magique | 40 | = | = |
| Mana (initial/max) | 40 / 100 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Disco Inferno

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: On combat start, forge a temporary completed item. If 3 items are already equipped, a random completed item becomes Radiant this combat instead.Active: Gain @ModifiedShield@ Shield for @ShieldDuration@ seconds, then breath fire in a cone dealing @ModifiedDamage@ magic damage. After any Shield on Ornn expires, Ornn enters {{TFT17_SpaceGroove_TheGroove}} for @GrooveDuration@ seconds.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 200 / 180 / 270 / 430 / 590 / 600 / 600 |
| `GrooveDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `Shield` | 100 / 125 / 200 / 500 / 1050 / 300 / 300 |
| `ShieldDuration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |

