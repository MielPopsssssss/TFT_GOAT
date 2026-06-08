"""Constantes globales du Data & Knowledge Layer.

Toutes les valeurs liees au set/patch sont centralisees ici pour qu'un nouveau set
soit un simple changement de constantes + refresh de donnees (cf. docs/ARCHITECTURE.md).
"""

from __future__ import annotations

import os
from pathlib import Path

# --- Set / patch courant ---------------------------------------------------
# Set 17 « Space Gods », patch 17.4 (confirme 2026-06-02).
CURRENT_PATCH = "17.4"
SET_NUMBER = 17
SET_MUTATOR = "TFTSet17"  # filtre l'entree setData du set live dans CDragon

# --- CommunityDragon -------------------------------------------------------
# Seule source viable pour stats / breakpoints de traits / augments.
# `latest` pointe toujours sur le patch courant ; on fige une copie locale par patch.
CDRAGON_LATEST_URL = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"

# --- Chemins ---------------------------------------------------------------
# Racine du projet = deux niveaux au-dessus de ce fichier (src/tft_goat/config.py).
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
CDRAGON_DIR = DATA_DIR / "cdragon"
FIXTURES_DIR = DATA_DIR / "fixtures"


def cdragon_snapshot_path(patch: str = CURRENT_PATCH) -> Path:
    """Chemin du snapshot CDragon pine pour un patch donne."""
    return CDRAGON_DIR / f"cdragon_{patch}.json"


def riot_api_key() -> str:
    """Cle API Riot, lue depuis l'environnement (jamais hardcodee).

    Raises:
        RuntimeError: si la variable RIOT_API_KEY est absente.
    """
    key = os.environ.get("RIOT_API_KEY")
    if not key:
        raise RuntimeError(
            "RIOT_API_KEY absente de l'environnement. "
            "Genere une cle dev sur https://developer.riotgames.com puis "
            "export RIOT_API_KEY=..."
        )
    return key
