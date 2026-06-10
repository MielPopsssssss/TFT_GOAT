# Master Yi — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_MasterYi`
- **Coût** : 4
- **Traits** : [Psionic](../traits/TFT17_PsyOps.md), [Marauder](../traits/TFT17_MeleeTrait.md)
- **Rôle** : ADFighter
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 1100 | 1980 | 3564 |
| Dégâts d'attaque | 60 | 108 | 194.4 |
| Vitesse d'attaque | 0.85 | = | = |
| Armure | 65 | = | = |
| Résistance magique | 65 | = | = |
| Mana (initial/max) | 30 / 70 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Psi Strikes

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Every third attack is a doubleslash that deals @ModifiedPassiveDamage@ bonus physical damage.Active: After brief meditation, enter a Psi-State for @Duration@ seconds, gaining @Omnivamp*100@% Omnivamp, @AttackSpeed*100@% Attack Speed, and increased movement speed. Twice a second, fire a psychic projection at a random nearby enemy that deals @ModifiedDamage@ physical damage

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `AttackSpeed` | 0.7 / 0.7 / 0.7 / 0.7 / 0.7 / 0.7 / 0.7 |
| `DamageAD` | 60 / 50 / 75 / 600 / 720 / 450 / 450 |
| `DamageAP` | 30 / 20 / 30 / 200 / 360 / 360 / 360 |
| `Duration` | 5 / 5 / 5 / 5 / 5 / 5 / 5 |
| `Omnivamp` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `PassiveDamage` | 60 / 70 / 105 / 550 / 720 / 720 / 720 |

