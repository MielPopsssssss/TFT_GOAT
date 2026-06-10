# Veigar — fiche champion

> Fiche GÉNÉRÉE depuis CommunityDragon patch 17.4 — **NE PAS ÉDITER À LA MAIN**.
> Régénérer : `.venv/bin/python -m scripts.generate_fiches`

- **apiName** : `TFT17_Veigar`
- **Coût** : 1
- **Traits** : [Meeple](../traits/TFT17_Astronaut.md), [Replicator](../traits/TFT17_APTrait.md)
- **Rôle** : APCaster
- **Jouable (pool boutique)** : oui

## Stats

| Stat | 1★ | 2★ | 3★ |
|---|---|---|---|
| HP | 500 | 900 | 1620 |
| Dégâts d'attaque | 30 | 54 | 97.2 |
| Vitesse d'attaque | 0.7 | = | = |
| Armure | 15 | = | = |
| Résistance magique | 15 | = | = |
| Mana (initial/max) | 10 / 50 | = | = |
| Portée | 4 | = | = |
| Crit (chance × multi) | 0.25 × 1.4 | = | = |

## Sort — Meepteor Shower

**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)

Call down a Meepteor on the target that deals @ModifiedDamage@ magic damage.Meep Bonus: An additional @ModifiedMiniMeeps@ mini Meepteor are called down on nearby targets dealing @ModifiedMiniDamage@ magic damage each.

### Variables (valeurs data par niveau)

| Variable | Valeurs |
|---|---|
| `Damage` | 250 / 310 / 465 / 700 / 1190 / 825 / 825 |
| `MiniDamage` | 40 / 31 / 47 / 70 / 130 / 120 / 120 |
| `MiniMeepsPerAstro` | 2 / 2 / 2 / 2 / 2 / 2 / 2 |

