"""Constantes du moteur de combat (versionnees).

AUDIT 2026-06-08 vs patch 17.4 :
  - VERIFIE (web + skill unanimes) : crit 25% / x1.4, ATTACK_SPEED_CAP 5.0, star scaling x1.8,
    MANA_LOCK_DURATION ~1.0s.
  - MODELE MANA (code = ref skill) : 10/attaque tous, 1% pre-mit + 7% post-mit, cap 42.5. La page
    wiki LoL decrit un modele par ROLE (10/7/5) + mana-sur-degats tanks-only 1%+3% = modele
    HISTORIQUE des premiers sets ; non flippe sans confirmation officielle Set 17.
  Pins : tests/test_combat_constants.py.
"""

from __future__ import annotations

# Star scaling : HP et AD multiplies par etoile (standard TFT ~1.8).
STAR_SCALE = {1: 1.0, 2: 1.8, 3: 1.8 * 1.8}

# Mana
MANA_PER_ATTACK = 10.0
MANA_ON_HIT_PREMIT = 0.01   # +1% des degats PRE-mitigation
MANA_ON_HIT_POSTMIT = 0.07  # +7% des degats POST-mitigation
MANA_ON_HIT_CAP = 42.5      # plafond de mana gagne par instance de degats
MANA_LOCK_DURATION = 1.0    # apres un cast : ~1s sans aucun gain de mana

# Attack speed plafonnee (TFT cap a 5.0 attaques/s)
ATTACK_SPEED_CAP = 5.0
ATTACK_WINDUP = 0.25        # delai (s) avant la 1re auto-attaque (windup)
SHIELD_DEFAULT_DURATION = 8.0  # duree par defaut d'un bouclier (s)

# Temps
TICK_DT = 0.1  # secondes par tick
MOVE_INTERVAL = 0.5  # secondes/hex (= 5 ticks, multiple exact de TICK_DT ; ~2 hex/s, realiste TFT)
MAX_COMBAT_TICKS = 400  # garde-fou (~40s) -> au-dela, depart aux degats restants

# Grille (combinee) : 8 rangees x 7 colonnes, 4 rangees par joueur.
GRID_ROWS = 8
GRID_COLS = 7
ROWS_PER_TEAM = 4

# AP de base d'une unite (les sorts scalent via leurs variables data + AP/100).
BASE_AP = 100.0
