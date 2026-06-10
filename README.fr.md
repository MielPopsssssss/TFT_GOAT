# TFT_GOAT

IA pour jouer à Teamfight Tactics (TFT) à très haut niveau, entraînée par **reinforcement
learning / self-play**.

## Idée directrice

Deux approches du combat cohabitent derrière une même interface `CombatResolver` :
- un **vrai moteur tick-par-tick** (grille hex, vraies stats champions/items/traits, sorts, CC,
  omnivamp/grievous/durability/boucliers, crit de sort) — la **source de vérité**, fidèle ;
- un **surrogate neuronal** `P(victoire | board A, board B)` **entraîné sur ce moteur** — une
  approximation **rapide** pour le débit du self-play RL (approche Riot, GDC 2024).

Le RL apprend la *macro* (économie, roll, level, compo, items, augments, positionnement). Tout le
contenu est data-driven (CommunityDragon + datatft) → un nouveau set = un refresh de données.

## État

Architecture figée (→ **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**). Pipeline complet : data →
env (éco/shop/traits/items/augments) → combat (heuristique / moteur / surrogate) → agent RL +
adversaires scriptés. Couverture combat : **[docs/COMBAT_COVERAGE.md](docs/COMBAT_COVERAGE.md)** ;
support moteur par entité (chaque champion / trait / item / augment, ✅ implémenté vs 🟡 partiel vs
⛔ masqué) audité dans **[docs/fiches/INDEX.md](docs/fiches/INDEX.md)**.

```
.venv/bin/python -m pytest -q                          # 215 tests
.venv/bin/python -m tft_goat.scripts.scrape_datatft    # fige les vraies stats meta (datatft)
.venv/bin/python -m tft_goat.scripts.random_rollout    # partie 8 joueurs complete (Set 17)
.venv/bin/python -m tft_goat.scripts.train --content real --resolver neural \
    --surrogate runs/surrogate_engine/combatnet.pt --iterations 30
#   -> agent PPO ; eval vs random ET vs adversaire scripte (baseline de skill credible)
```

Les vraies stats (placement moyen par champion/trait, scrapées depuis l'API datatft) ancrent la
force de board du combat heuristique v0 (`TftEnv(..., meta_stats=load_meta_stats())`).

Le combat appris (étape 4) :
```
RIOT_API_KEY=... .venv/bin/python -m tft_goat.scripts.collect_matches --matches 150
.venv/bin/python -m tft_goat.scripts.train_surrogate --source riot --matches data/matches/matches_17.4.jsonl
#   -> CombatNet ~85% d'accuracy pour predire quel board finit mieux ; charge via NeuralResolver
```

Surrogate régénéré sur le **vrai moteur** (vérité terrain combat, le plus fidèle) :
```
.venv/bin/python -m tft_goat.scripts.train_surrogate --source engine --pairs 8000 --engine-samples 3
#   -> CombatNet ~83% d'accord avec le moteur tick-par-tick ; approximation RAPIDE du moteur pour le RL
```
Étape 5 — surrogate **hybride** (vraies paires + bootstrap multi-stades) + RL sur le vrai Set 17 :
```
.venv/bin/python -m tft_goat.scripts.train_surrogate --source hybrid --matches data/matches/matches_17.4.jsonl
.venv/bin/python -m tft_goat.scripts.train --content real --resolver neural --surrogate runs/surrogate/combatnet.pt --iterations 20
#   -> surrogate val ~0.88, P(fort bat faible) 0.99 (anomalie corrigee) ; agent place ~1.5-2 vs random 4.5
```

## Roadmap (chaque étape a son propre spec + plan)

1. ✅ **Data & Knowledge Layer** — contenu CommunityDragon (Set 17), shop odds, collecteur Riot match-v1
2. ✅ **Macro Environment + combat placeholder** — env PettingZoo 8 joueurs jouable de bout en bout
3. ✅ **Agent RL (PPO self-play)** — PPO custom (masquage + self-play) + adversaire scripté pour
   l'éval. ⚠️ L'agent écrase le random mais **perd encore contre le scripté** (top4 ~40%) : le
   pipeline est complet, l'agent demande un **entraînement à l'échelle** (gros rollouts, tuning,
   éventuellement curriculum vs scripté) — c'est le prochain gros chantier RL.
4. ✅ **Combat surrogate** — `CombatNet` entraîné sur 150 vraies parties challenger (val_acc ~0.85), enfiché via `NeuralResolver`
5. ✅ **Montée en puissance** — items & augments dans l'env ; surrogate **hybride** robuste (val réel ~0.88, anomalie petit-board corrigée) ; agent PPO entraîné sur le vrai Set 17 contre le combat appris (placement ~1.5-2 vs random 4.5)
6. 🔧 **Vrai moteur de combat tick-par-tick** — cœur livré (grille hex, vraies stats champions/items/traits, attaques/mana/cast/morts) ; logique des sorts/augments = remplissage en cours → voir **[docs/COMBAT_COVERAGE.md](docs/COMBAT_COVERAGE.md)**
7. *(optionnel, ⚠️ ToS)* Perception (computer vision) + Actuation (jouer sur le vrai client)

### Trois moteurs de combat enfichables (même interface `CombatResolver`)
- `HeuristicResolver` — force de board ancrée datatft (rapide)
- `NeuralResolver` — surrogate appris sur vraies parties (rapide, pour le RL)
- `EngineResolver` — **vrai** combat tick-par-tick sur les stats réelles (fidèle, source de vérité)

### Différé / en cours
Logique exacte des 83 sorts + procs items + 276 augments (PARTIE B) ; identités d'objets dans l'env ;
déroulé exact (tables XP/stages) ; positionnement joueur ; MuZero ; vectorisation.

## ⚠️ Avertissement

Le cœur (RL/self-play) est **offline** et ne touche pas au client → aucun risque ToS.
L'actuation in-game (étape 6) viole le ToS Riot → à n'utiliser que sur un compte de test,
aux risques de l'utilisateur.
