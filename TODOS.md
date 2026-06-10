# TODOS

Backlog technique fin (le [ROADMAP.md](ROADMAP.md) public porte les grands axes).
Format : groupé par composant, priorité P0 (urgent) → P4 (un jour), complétés en bas.

## Env / Rounds

- **Coupler le champion offert et le dieu du vote**
  **Priority:** P2
  `_offer_gods()` (rounds.py) assigne les dieux indépendamment de `_sample_gods()` : le vote
  ne porte aucun sens en jeu pour le choix du champion. Le vrai TFT lie chaque Minor Blessing
  à son dieu. Renforce l'item ROADMAP « Realm of the Gods (full) ».

## Engine / Traits

- **Clarifier les 8 variantes homonymes « Stargazer »**
  **Priority:** P2
  8 apiNames partagent le nom « Stargazer » (Wolf/Medallion/Huntress/Serpent/Shield/
  Fountain/Mountain + base). Le moteur résout par nom -> seule `TFT17_Stargazer` est
  utilisée. Hypothèse : variantes liées au dieu aligné (Realm of the Gods) — vérifier en
  jeu laquelle s'active et selon quoi, puis modéliser. Les fiches marquent les variantes
  masquées ⛔ en attendant.

## Engine / Abilities

- **Multiplicateur d'autos dédié (passives auto-only : Graves, Jhin)**
  **Priority:** P3
  Les passives « par auto-attaque » (Graves 5 projectiles ×33% AD, Jhin ADConversionRate)
  sont modélisées en buff d'AD global, ce qui gonfle AUSSI leurs sorts (qui scalent AD)
  — divergence vs vrai jeu où seules les autos sont touchées. Ajouter un champ
  multiplicateur d'autos sur CombatUnit, appliqué dans la formule d'attaque uniquement,
  et migrer les deux champions + pins. (Trouvé par red team, décision D3, 2026-06-10.)

## Surrogate

- **Encoder les augments dans les features du CombatNet**
  **Priority:** P2
  Le NeuralResolver reçoit `augments_a/b` mais les ignore (prédiction boards-only), alors
  que Heuristic (augment_power) et Engine (registre) sont désormais augment-aware. C'est
  le resolver PRIMAIRE d'entraînement RL : les God Boons y sont inertes. Ajouter les
  augments aux features du surrogate (et au dataset), ou documenter/gater l'entraînement
  boon-sensible sur Heuristic/Engine en attendant. (Trouvé par red team, 2026-06-10.)

## Data

- **Scraper les stats d'augments metatft (pick-rate/placement)**
  **Priority:** P3
  Riot a RETIRÉ les augments de match-v1 (champ absent des participants, vérifié sur
  matches_17.4.jsonl — 1200 joueurs, 0 augments) : aucun proxy d'usage challenger possible
  en interne. Un scrape metatft (même infra que scrape_datatft) donnerait pick-rate +
  avg place par augment → prioriser la long tail par usage réel et ancrer
  `AUGMENT_TIER_WEIGHT` (env/combat.py) dans la vraie data. En attendant, priorisation
  par tier (exposition uniforme → prismatic combat d'abord, cf. batch_7).

## Tests

- **Extraire un helper partagé de boucle de jeu aléatoire**
  **Priority:** P3
  La boucle `reset → while env.agents → actions masquées → step` est copiée ~5× :
  `test_game_length.py` (×3), `test_coherence.py`, `scripts/{check_coherence,simulate_games}.py`.
  Un helper `tests/_helpers.py::play_random_game(...)` évite 5 mises à jour synchrones.

## Completed

- **Décider du sort du God Boon hors moteur réel**
  Décision : impact heuristique dédié. `env/combat.py::augment_power` — multiplicateur de
  force pour les augments à effet COMBAT uniquement (présents dans `AUGMENT_REGISTRY` ;
  les augments éco payent déjà via l'économie : pas de double-comptage). Poids par tier
  assumés (documentés comme heuristiques, pas de la data). Pins : `tests/test_combat.py`.
  **Completed:** v0.5.0.0 (2026-06-10)

- **Câbler les 11 God Boons absents du registre d'augments moteur**
  17/17 God Boons dans `AUGMENT_REGISTRY` (`augments_set17/batch_6.py`) : 8 effets combat
  (dont LargeQuest fidèle via `active_traits(bonus_units=1)` au build, Thresh d6 réel,
  Ekko Anomaly par rôle) + 3 no-ops FIDÈLES (boons purement éco/joueur). `ctx.content`
  ajouté à `CombatContext` (lecture data cross-augment). Approximations détaillées dans
  `docs/COMBAT_COVERAGE.md` ; pins `tests/test_god_boons_engine.py`. **Completed:** v0.5.0.0 (2026-06-10)

- **Enquête équité des sièges**
  Root cause double : (1) tie-break déterministe des morts simultanées à HP égaux
  (`assign_eliminations`, tri stable -> siège bas pénalisé ; corrigé en départage rng) ;
  (2) bande fixe de `check_coherence` statistiquement naïve à petit N (corrigée N-aware).
  L'hypothèse premier-acteur est écartée (signe inversé) ; l'appariement est sain
  (permutation rng). Magnitude : aucun biais réel à N=400 (max |z|=1.9) — les FAIL à
  N=15/40 étaient du bruit. **Completed:** v0.4.1.0 (2026-06-10)

- **Encoder les features Realm of the Gods dans l'observation**
  Vecteur `gods` 31 dims (lobby, slots d'offre, votes, aligné, boon) + réseau adapté.
  Checkpoints antérieurs invalidés (réentraîner).
  **Completed:** v0.4.0.0 (2026-06-10)

- **Variables `*_Health` de traits jamais appliquées (`"heal"` matche `"health"`)**
  Tri par variable effectué : `HealthBonus` (Brawler %) et `BonusHealth` (Meeple flat)
  appliqués en hp (fraction/flat) ; heals/seuils/percent-health toujours skippés.
  **Completed:** v0.3.1.0 (2026-06-10)
