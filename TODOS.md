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

## Env / Équité

- **Enquêter l'équité des sièges en self-play (et rendre la bande de check_coherence N-aware)**
  **Priority:** P2
  Sur policy entraînée (v0.4.0, it250) : 2 runs de `check_coherence` (15 et 40 parties) sortent
  de la bande fixe [3.8, 5.2] avec des sièges différents — sauf le siège 5, bas (3.00 puis 3.62)
  les deux fois (avantage répété ?). Le sim 10k pré-fixes donnait 4.49-4.52 partout. Hypothèse
  à tester : avantage du premier acteur (`for a in acting` itère player_0..7, pool partagé —
  les achats du siège 0 dépètent le pool avant le siège 7 au même step). Plan : run 500+
  parties offline, et adapter la bande du check à N (±k·2.29/√N) au lieu d'une bande fixe.

## Tests

- **Extraire un helper partagé de boucle de jeu aléatoire**
  **Priority:** P3
  La boucle `reset → while env.agents → actions masquées → step` est copiée ~5× :
  `test_game_length.py` (×3), `test_coherence.py`, `scripts/{check_coherence,simulate_games}.py`.
  Un helper `tests/_helpers.py::play_random_game(...)` évite 5 mises à jour synchrones.

## Completed

- **Encoder les features Realm of the Gods dans l'observation**
  Vecteur `gods` 31 dims (lobby, slots d'offre, votes, aligné, boon) + réseau adapté.
  Checkpoints antérieurs invalidés (réentraîner).
  **Completed:** v0.4.0.0 (2026-06-10)

- **Variables `*_Health` de traits jamais appliquées (`"heal"` matche `"health"`)**
  Tri par variable effectué : `HealthBonus` (Brawler %) et `BonusHealth` (Meeple flat)
  appliqués en hp (fraction/flat) ; heals/seuils/percent-health toujours skippés.
  **Completed:** v0.3.1.0 (2026-06-10)
