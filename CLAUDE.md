# TFT_GOAT

## But du projet

Construire un **agent autonome capable de battre de vrais joueurs humains** à Teamfight
Tactics (Set 17 « Space Gods »), par RL/self-play — l'approche décrite par Riot à la GDC 2024 :
le macro-jeu appris par RL, le combat résolu par un surrogate neuronal entraîné sur un moteur
tick-by-tick fidèle.

**Principe directeur : fidélité d'abord.** Pas de RL sérieux tant que la simulation n'est pas
prouvée fidèle au vrai jeu (data exacte, mécaniques exactes, déroulé de partie réaliste).
Un simulateur faux produit un agent qui apprend à exploiter les bugs du simulateur.
La fidélité est documentée honnêtement dans `docs/COMBAT_COVERAGE.md`.

## Connaissance TFT — TOUJOURS vérifier, jamais inventer

- **Skill `tft-knowledge`** (`.claude/skills/tft-knowledge/`) : règles et chiffres vérifiés du
  Set 17 (économie, odds de shop/augments, mécanique des dieux, combat). **Invoquer ce skill
  pour toute question de mécanique ou de chiffre TFT.**
- Aucun chiffre de jeu ne doit être écrit en dur sans source : la vérité primaire est la data
  CommunityDragon, secondairement le wiki / les sites de patch (metatft, tftodds, mobalytics).

## Où est la data (couche 1)

| Source | Fichier | Contenu | Comment rafraîchir |
|---|---|---|---|
| CommunityDragon | `data/cdragon/cdragon_17.4.json` | Contenu statique : 83 champions, traits, items, augments (stats/effets réels) | `src/tft_goat/data/cdragon.py` |
| datatft | `data/datatft/datatft_17.4.json` | Méta/perf UNIQUEMENT (winrates, placements) — pas de data statique | `src/tft_goat/scripts/scrape_datatft.py` + `verify_datatft.py` |
| Riot match-v1 | `data/matches/matches_17.4.jsonl` | Vraies parties challenger (dataset du surrogate) | `collect_matches.py` (RIOT_API_KEY) |
| Data dérivée | `data/{augments,items_completed,abilities}_set17.json` | Vues extraites pour l'audit | — |

Le chargement passe par `src/tft_goat/data/content.py::load_set()` (filtre l'entrée setData
TFTSet17 ; les préfixes non-TFT17 restants sont du contenu evergreen/PvE légitime).

**Fiches d'audit** : `docs/fiches/` — une vue markdown GÉNÉRÉE par champion/trait/item/augment
(data CDragon + statut d'implémentation moteur ✅/🟡), liées par `docs/fiches/INDEX.md`.
Jamais éditées à la main ; régénérer après tout refresh de data ou ajout moteur :
`.venv/bin/python -m scripts.generate_fiches`. C'est la surface d'audit humaine : ouvrir une
fiche, comparer au vrai jeu, transformer chaque écart en test pin.

## Architecture (résumé)

- `src/tft_goat/data/` — couche data (modèles pydantic immuables, gods, odds)
- `src/tft_goat/env/` — env macro PettingZoo 8 joueurs (éco, shop, items, augments, dieux, rounds)
- `src/tft_goat/engine/` — moteur de combat tick-by-tick réel (vérité terrain)
- `src/tft_goat/surrogate/` — CombatNet P(win|A,B), approximation rapide pour le RL
- `src/tft_goat/agent/` — PPO self-play + adversaire scripté (éval)
- Trois resolvers interchangeables derrière `CombatResolver` : Heuristic / Neural / Engine

Doc complète : `docs/ARCHITECTURE.md`. Backlog fin : `TODOS.md`. Axes publics : `ROADMAP.md`.

## Commandes

```bash
.venv/bin/python -m pytest -q                      # suite complète (~75 s)
.venv/bin/python -m scripts.check_coherence 20     # invariants de cohérence sur 20 parties
.venv/bin/python -m scripts.realism_vs_datatft     # réalisme vs méta datatft
.venv/bin/python -m scripts.realism_vs_matches     # vérité terrain : moteur vs vraies parties (Spearman +0.44)
.venv/bin/python -m tft_goat.scripts.random_rollout  # une partie aléatoire complète
```

## Conventions

- Tests obligatoires pour toute mécanique de jeu : chaque chiffre/règle vérifié = un test « pin »
  qui référence sa source (voir `tests/test_champion_data.py`, `tests/test_gods.py`).
- Docstrings/commentaires en français, code en anglais (idiome existant du repo).
- Toute approximation assumée vs le vrai TFT doit être notée dans `docs/COMBAT_COVERAGE.md`.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Question de mécanique/chiffre TFT → invoke /tft-knowledge (skill projet)
- Product ideas/brainstorming → invoke /gstack-office-hours
- Strategy/scope → invoke /gstack-plan-ceo-review
- Architecture → invoke /gstack-plan-eng-review
- Full review pipeline → invoke /gstack-autoplan
- Bugs/errors → invoke /gstack-investigate
- Code review/diff check → invoke /gstack-review
- Ship/deploy/PR → invoke /gstack-ship or /gstack-land-and-deploy
- Save progress → invoke /gstack-context-save
- Resume context → invoke /gstack-context-restore
- Author a backlog-ready spec/issue → invoke /gstack-spec
