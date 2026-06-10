"""Fiches d'audit générées : une vue markdown par champion/trait/item/augment.

Source de vérité = data CommunityDragon (`load_set()`) + registres moteur (statut
d'implémentation). Les fiches ne sont JAMAIS éditées à la main : régénérer via
`.venv/bin/python -m scripts.generate_fiches`. Objectif : donner une surface auditable
humaine — ouvrir une fiche, comparer au vrai jeu, transformer chaque écart en test pin.
"""

from __future__ import annotations

from .generate import generate_all
from .render import fmt

__all__ = ["fmt", "generate_all"]
