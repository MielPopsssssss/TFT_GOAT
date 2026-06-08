"""Telechargement et cache du JSON CommunityDragon (contenu TFT brut).

Le fichier `latest` (~24,5 MB) pointe sur le patch courant. On en fige une copie locale
par patch (`data/cdragon/cdragon_<patch>.json`) pour la reproductibilite : un re-fetch
plus tard ne doit pas changer silencieusement les donnees d'un patch deja fige.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx

from ..config import CDRAGON_DIR, CDRAGON_LATEST_URL, CURRENT_PATCH, cdragon_snapshot_path


def download_snapshot(patch: str = CURRENT_PATCH, *, force: bool = False) -> Path:
    """Telecharge (en streaming) le JSON CDragon `latest` et le fige pour `patch`.

    Args:
        patch: etiquette de patch sous laquelle figer le fichier.
        force: re-telecharge meme si le snapshot existe deja.

    Returns:
        Le chemin du snapshot pine.
    """
    dest = cdragon_snapshot_path(patch)
    if dest.exists() and not force:
        return dest

    CDRAGON_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".json.part")
    with httpx.stream("GET", CDRAGON_LATEST_URL, timeout=120.0, follow_redirects=True) as resp:
        resp.raise_for_status()
        with tmp.open("wb") as fh:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                fh.write(chunk)
    tmp.replace(dest)  # ecriture atomique
    return dest


def load_raw(patch: str = CURRENT_PATCH) -> dict:
    """Charge le dict CDragon brut pour `patch` (le telecharge s'il manque)."""
    path = cdragon_snapshot_path(patch)
    if not path.exists():
        download_snapshot(patch)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
