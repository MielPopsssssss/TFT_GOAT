"""Probabilites du shop et tailles de pool, versionnees par patch.

Hardcodees plutot que scrapees : ces tables sont quasi-stables d'un patch a l'autre et
les sources web (metatft) sont des SPA fragiles. Verifie contre esportstales + patch notes
le 2026-06-02 (Set 17, patch 17.1 a ajuste la ligne L7).

Format : `SHOP_ODDS[patch][level] = (p1, p2, p3, p4, p5)` en POURCENTS (somme = 100),
ou pK = chance qu'un slot du shop affiche un champion de cout K.
"""

from __future__ import annotations

from ..config import CURRENT_PATCH

# Copies de chaque champion dans le pool partage, par cout. Stable Set 12+.
POOL_SIZES: dict[int, int] = {1: 30, 2: 25, 3: 18, 4: 10, 5: 9}

# Odds par niveau (1..11). VERIFIE vs patch 17.4 le 2026-06-08 : op.gg + esportstales
# concordent EXACTEMENT (L7=19/30/40/10/1, L8=17/24/32/24/3, L9=15/18/25/30/12).
# tftactics divergeait (L7 sommait a 95 => stale) ; ecart tranche en faveur de la table ci-dessous.
# Pin de regression : tests/test_odds.py::test_disputed_levels_match_verified_patch_17_4.
SHOP_ODDS: dict[str, dict[int, tuple[int, int, int, int, int]]] = {
    "17.4": {
        1: (100, 0, 0, 0, 0),
        2: (100, 0, 0, 0, 0),
        3: (75, 25, 0, 0, 0),
        4: (55, 30, 15, 0, 0),
        5: (45, 33, 20, 2, 0),
        6: (30, 40, 25, 5, 0),
        7: (19, 30, 40, 10, 1),
        8: (17, 24, 32, 24, 3),
        9: (15, 18, 25, 30, 12),
        10: (5, 10, 20, 40, 25),
        11: (1, 2, 12, 50, 35),
    },
}


def roll_odds(level: int, patch: str = CURRENT_PATCH) -> dict[int, float]:
    """Probabilites (0..1) par cout pour un slot de shop a `level`.

    Raises:
        KeyError: patch inconnu.
        ValueError: niveau hors de 1..11.
    """
    table = SHOP_ODDS[patch]
    if level not in table:
        raise ValueError(f"Niveau {level} hors plage (1..{max(table)})")
    return {cost: pct / 100.0 for cost, pct in zip(range(1, 6), table[level])}


def pool_size(cost: int) -> int:
    """Nombre de copies d'un champion de cout donne dans le pool partage."""
    return POOL_SIZES[cost]
