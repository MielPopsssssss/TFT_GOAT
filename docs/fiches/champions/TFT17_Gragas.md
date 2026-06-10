# Gragas — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Gragas`
- **Coût** : 2
- **Traits** : [Psionic](../traits/TFT17_PsyOps.md), [Brawler](../traits/TFT17_HPTank.md)
- **Rôle** : APTank
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 950 | 1710 | 3078 |
| Dégâts d'attaque | 50 | 90 | 162 |
| Vitesse d'attaque | 0.6 | = | = |
| Armure | 45 | = | = |
| Résistance magique | 45 | = | = |
| Mana (initial/max) | 30 / 80 | = | = |
| Portée | 1 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Chemical Rage

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Heal @ModifiedHeal@ over @Duration@ seconds. Then, deal @DamageTotal@ magic damage to target and enemies adjacent to them and @ASSlow*100@% Chill them for @CCDuration@ seconds.{{TFT_Keyword_Chill}}

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `ASSlow` | 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 / 0.3 |
| `CCDuration` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `DURATION` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |
| `Damage` | 0 / 200 / 300 / 450 / 765 / 0 / 0 |
| `HEALING` | 0 / 415 / 470 / 630 / 790 / 0 / 0 |
| `HealingPercentHealth` | 0.085 / 0.085 / 0.085 / 0.085 / 0.085 / 0.085 / 0.085 |

