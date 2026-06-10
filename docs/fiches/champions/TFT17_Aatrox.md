# Aatrox — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Aatrox`
- **Coût** : 1
- **Traits** : [N.O.V.A.](../traits/TFT17_DRX.md), [Bastion](../traits/TFT17_ResistTank.md)
- **Rôle** : ADTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 700 | 1260 | 2268 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 30 / 90 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Stellar Slash

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Heal @ModifiedHeal@, then deal @ModifiedDamage@ physical damage to the current target.N.O.V.A. Strike: Cleave the battlefield, briefly knocking up all enemies and dealing @ModifiedNovaDamage@ physical damage.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `DamageAD` | 200 / 80 / 120 / 180 / 300 / 600 / 600 |
| `DamagePercentArmor` | 1 / 1.8 / 2.7 / 4.05 / 6.9 / 3 / 3 |
| `HealAP` | 150 / 325 / 400 / 650 / 900 / 180 / 180 |
| `HealHP` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `NOVAModifier` | 0.65 / 0.65 / 0.65 / 0.65 / 0.65 / 0.65 / 0.65 |

