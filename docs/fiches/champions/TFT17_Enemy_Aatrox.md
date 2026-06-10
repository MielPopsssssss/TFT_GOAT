# Apex Primordian — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Enemy_Aatrox`
- **Coût** : 5
- **Traits** : —
- **Rôle** : ADTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 8452 | 15213.6 | 27384.5 |
| Dégâts d'attaque | 90 | 162 | 291.6 |
| Vitesse d'attaque | 0.9 | = | = |
| Armure | 60 | = | = |
| Résistance magique | 60 | = | = |
| Mana (initial/max) | 30 / 90 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Harbinger of The End

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Swords fly out in a grid dealing @TotalGridDamage@ physical damage to enemies they hit. Active: Launch @NumSwords@ swords into the air and gain @Durability*100@% Durability. When they land, they deal @TotalSwordAoEDamage@ physical damage to enemies they hit in a @HexRange@-hex range.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Durability` | 0.25 / 0.25 / 0.25 / 0.25 / 0.25 / 0.25 / 0.25 |
| `GridADDamage` | 50 / 50 / 50 / 50 / 50 / 50 / 50 |
| `GridAPDamage` | 50 / 50 / 50 / 50 / 50 / 50 / 50 |
| `HexRange` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `NumSwords` | 20 / 20 / 20 / 20 / 20 / 20 / 20 |
| `SwordAoEADDamage` | 200 / 200 / 200 / 200 / 200 / 200 / 200 |
| `SwordAoEAPDamage` | 200 / 200 / 200 / 200 / 200 / 200 / 200 |

