"""Garde-fou de réalisme : l'EngineResolver doit rester directionnellement aligné sur datatft.

DIAGNOSTIC, pas une preuve : l'avg_place datatft est confondu par playrate/coût/utilité, donc on
ne vérifie que des invariants ROBUSTES (l'unité datatft-top domine ; pas d'anti-corrélation). Les
écarts connus (unités d'utilité/CC/summon sous-évaluées par le moteur) sont documentés au ledger.
"""

from __future__ import annotations

import numpy as np

from tft_goat.data.content import load_set
from tft_goat.data.datatft import load_meta_stats
from tft_goat.engine.simulate import run_combat
from tft_goat.env.state import BoardUnit

CORE = [
    "TFT17_Shen", "TFT17_TahmKench", "TFT17_Rammus",
    "TFT17_Morgana", "TFT17_Karma", "TFT17_Nami",
]
BASELINE = "TFT17_Vex"
N = 50


def _board(carry: str) -> list[BoardUnit]:
    return [BoardUnit(u, 2) for u in CORE] + [BoardUnit(carry, 2)]


def _win_rate(carry: str, content, rng) -> float:
    base = _board(BASELINE)
    test = _board(carry)
    return sum(run_combat(test, base, content, rng).winner == 0 for _ in range(N)) / N


def _spearman(xs, ys) -> float:
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for rank, i in enumerate(order):
            r[i] = rank
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def test_engine_is_directionally_aligned_with_datatft():
    """Corrélation de rang positive entre win rate moteur et force datatft (5-cost).

    Seuil LÂCHE (rho > 0.2) : on garantit que le moteur n'est pas décorrélé/inversé, pas
    qu'il est parfait. Une régression qui casserait la fidélité (sorts inversés, etc.) ferait
    chuter rho sous 0.
    """
    content = load_set()
    meta = load_meta_stats()
    rng = np.random.default_rng(42)
    carries = [
        api for api, c in content.champions.items()
        if api.startswith("TFT17_") and c.cost == 5 and api != BASELINE and api in meta.units
    ]
    wrs = [_win_rate(c, content, rng) for c in carries]
    neg_places = [-meta.units[c].avg_place for c in carries]
    rho = _spearman(wrs, neg_places)
    assert rho > 0.2, f"moteur décorrélé de datatft (rho={rho:.2f}) -> régression de fidélité ?"


def test_datatft_top_carry_dominates_baseline():
    """Jhin (meilleur avg_place datatft du tier) gagne nettement contre le board baseline."""
    content = load_set()
    rng = np.random.default_rng(7)
    assert _win_rate("TFT17_Jhin", content, rng) >= 0.6
