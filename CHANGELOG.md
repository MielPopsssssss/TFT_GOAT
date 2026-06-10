# Changelog

Toutes les évolutions notables du projet. Format inspiré de
[Keep a Changelog](https://keepachangelog.com/) ; versions `MAJOR.MINOR.PATCH.MICRO`.

## [0.4.0.0] - 2026-06-10

### Added
- **L'agent voit enfin les dieux** : nouveau vecteur d'observation `gods` (31 dims) —
  dieux du lobby, dieu associé à chaque choix d'offrande, votes cumulés, dieu aligné,
  God Boon. L'agent peut maintenant APPRENDRE la mécanique du Realm of the Gods au lieu
  de voter au hasard.

### Breaking
- Les dimensions d'entrée du réseau changent : les checkpoints antérieurs
  (`runs/ppo*/policy*.pt`) ne sont plus chargeables — réentraîner.

## [0.3.1.0] - 2026-06-10

### Fixed
- **Les bonus de HP de traits atteignent enfin le combat** : `heal` (substring) matchait
  `health` dans le filtre des variables de traits, rendant la branche HP morte — **Brawler**
  (+25/45/65 % HP max) et **Meeple** (+100..500 HP flat) n'avaient AUCUN effet en combat
  moteur. Corrigé (`heal(?!th)` + heuristique fraction/flat) ; les soins (`Heal`,
  `Huntress_Heal`), seuils et mécaniques percent-health restent correctement ignorés.
  Découvert par l'audit des fiches v0.3.0.0.

## [0.3.0.0] - 2026-06-10

### Added
- **Fiches d'audit générées** (`docs/fiches/`, 1090 fichiers) : une vue markdown par
  champion (stats réelles 1★/2★/3★, sort + statut moteur ✅/🟡), trait (paliers, variables
  auto-appliquées), item (recette, procs) et augment (tier, dieu du God Boon, statut
  combat) — liées par `docs/fiches/INDEX.md`. On peut maintenant auditer chaque entité
  du jeu en ouvrant un fichier lisible et comparer au vrai TFT.
- Générateur : module `src/tft_goat/fiches/` + CLI `scripts/generate_fiches.py`
  (déterministe : régénérer après un refresh de data donne un diff git propre) ; 17 tests.

### Fixed
- Les 8 traits homonymes « Stargazer » sont rendus honnêtement : seule la variante que le
  moteur résout réellement revendique des effets ; les 7 variantes masquées sont marquées
  ⛔ (collision de nom explicite) au lieu d'afficher de fausses applications.

### Changed
- `engine/trait_effects.attrs_for` devient une API publique (consommée par les fiches).

### Known gaps (tracés TODOS.md / COMBAT_COVERAGE)
- Les variables `*_Health` de traits ne sont jamais auto-appliquées en combat (`heal`
  matche `health` en substring) — découvert par l'audit des fiches, correctif à trier
  variable par variable.

## [0.2.0.0] - 2026-06-10

### Added
- **Realm of the Gods (Set 17)** : les parties simulées jouent maintenant la vraie mécanique
  des dieux — 2 dieux tirés par lobby, un vote par Minor Blessing aux rounds 2-4/3-4/4-4,
  alignement à la majorité des 3 votes, God Boon réel (augment tier "god" CDragon) octroyé
  au 4-7 et injecté dans le pipeline de combat (`src/tft_goat/data/gods.py`).
- **Scripts d'audit de cohérence** : `scripts/check_coherence.py` (invariants PASS/FAIL sur
  N parties), `scripts/realism_vs_datatft.py` (réalisme vs méta) et
  `scripts/simulate_games.py` (stats agrégées de déroulé).
- 13 nouveaux tests « pin » : intégrité de la data champions (mana/ranges), recettes
  d'items (10 composants, 55 recettes), flux de vote des dieux (8 tests dont 4 régressions),
  longueur de partie, cohérence et réalisme.

### Changed
- **Dégâts joueur fidèles** : la formule applique désormais base_stage + survivants SANS
  mitigation par augment (le stage final moyen passe de 7.8 à 6.9, médiane 8-2 → 7-2,
  conforme au vrai TFT).
- **Pool de boutique filtré** : seules les unités jouables `TFT17_` entrent dans le pool
  (les unités PvE/evergreen comme Training Dummy n'apparaissent plus en boutique) ; l'offre
  des dieux est tirée du même roster jouable.
- Durcissement sécurité : chargement des checkpoints via `torch.load(..., weights_only=True)`.

### Fixed
- Une action illégale pendant une offre forcée (dieu/augment) ne se transforme plus en PASS
  silencieux : elle est coercée vers la première action légale — le vote n'est plus sauté.
- Une offre de dieu non consommée ne fuit plus vers les rounds suivants (votes fantômes).
- L'alignement du dieu se déclenche au 3e vote (compte de votes) avec filet au 4-7 si un
  vote a été manqué — plus de dépendance fragile au numéro de round.
