# Jax — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Jax`
- **Coût** : 2
- **Traits** : [Stargazer](../traits/TFT17_Stargazer.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 950 | 1710 | 3078 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.65 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 20 / 80 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Counter Star-ike

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Enter a defensive stance for @Duration@ seconds, reducing incoming damage by @ModifiedFlatDR@ and gaining @ModifiedShield@ Shield. When the stance ends, strike all nearby enemies, dealing @ModifiedDamage@ magic damage and Stunning them for @StunDuration@ second(s).

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ArmorMRScale` | 50 / 0.75 / 1.15 / 1.7 / 2.9 / 500 / 500 |
| `AttackRadius` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `Duration` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `FlatDR` | 0 / 20 / 25 / 30 / 35 / 0 / 0 |
| `ShieldAP` | 0 / 400 / 450 / 500 / 600 / 0 / 0 |
| `StunDuration` | 1.5 / 1 / 1.25 / 1.5 / 1.75 / 1.5 / 1.5 |

