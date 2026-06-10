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

## Engine / Resolvers

- **Câbler les 11 God Boons absents du registre d'augments moteur**
  **Priority:** P2
  Seuls 6/17 God Boons ont un effet implémenté dans `AUGMENT_REGISTRY`
  (`engine/simulate.py` skippe silencieusement les non-enregistrés). Les 11 autres entrent
  dans `chosen_augments` mais n'ont AUCUN effet combat — gap de fidélité silencieux.
  À tracer aussi dans `docs/COMBAT_COVERAGE.md`.

- **Décider du sort du God Boon hors moteur réel**
  **Priority:** P2
  Le God Boon entre dans `chosen_augments` (consommé par l'EngineResolver) mais est inerte
  sous le HeuristicResolver v0 (qui ignore les augments) et n'alimente pas `augment_power`.
  Décider : impact heuristique dédié, ou documenter+tester « engine-only ».

## Tests

- **Extraire un helper partagé de boucle de jeu aléatoire**
  **Priority:** P3
  La boucle `reset → while env.agents → actions masquées → step` est copiée ~5× :
  `test_game_length.py` (×3), `test_coherence.py`, `scripts/{check_coherence,simulate_games}.py`.
  Un helper `tests/_helpers.py::play_random_game(...)` évite 5 mises à jour synchrones.

## Completed

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
