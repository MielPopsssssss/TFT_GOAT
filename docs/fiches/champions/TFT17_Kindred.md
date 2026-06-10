# Kindred — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Kindred`
- **Coût** : 4
- **Traits** : [N.O.V.A.](../traits/TFT17_DRX.md), [Challenger](../traits/TFT17_ASTrait.md)
- **Rôle** : ADCarry
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 850 | 1530 | 2754 |
| Dégâts d'attaque | 55 | 99 | 178.2 |
| Vitesse d'attaque | 0.8 | = | = |
| Armure | 30 | = | = |
| Résistance magique | 30 | = | = |
| Mana (initial/max) | 0 / 40 | = | = |
| Portée | 6 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Cosmic Pursuit

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Passive: Attacks and Abilities mark the target. When an enemy reaches @MaxMarks@ marks, Wolf consumes the marks, dealing @TotalDamage@ physical damage. Active: Jump up to @HexDistance@ hex away and fire arrows at the nearest @NumTargets@ targets, each dealing @ModifiedDamage@ physical damage. N.O.V.A. Strike: Gain @NovaDamageAmp*100@% Damage Amp. Now and every @NovaRepeatTimer@ seconds after, add a mark to all enemies.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ADDamage` | 0 / 115 / 175 / 900 / 1050 / 0 / 0 |
| `APDamage` | 0 / 10 / 15 / 100 / 75 / 0 / 0 |
| `HexDistance` | 1 / 1 / 1 / 1 / 1 / 1 / 1 |
| `MaxMarks` | 3 / 3 / 3 / 3 / 3 / 3 / 3 |
| `NovaDamageAmp` | 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 / 0.1 |
| `NovaRepeatTimer` | 4.5 / 4.5 / 4.5 / 4.5 / 4.5 / 4.5 / 4.5 |
| `NumTargets` | 3 / 3 / 3 / 5 / 5 / 5 / 5 |
| `SpellDamage` | 0 / 75 / 115 / 600 / 810 / 0 / 0 |

