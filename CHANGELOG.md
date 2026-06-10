# Changelog

Toutes les évolutions notables du projet. Format inspiré de
[Keep a Changelog](https://keepachangelog.com/) ; versions `MAJOR.MINOR.PATCH.MICRO`.

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
