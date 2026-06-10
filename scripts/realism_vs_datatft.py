"""Diagnostic de réalisme : corrélation de rang EngineResolver <-> datatft (par coût).

ATTENTION méthodologique : l'avg_place datatft n'est PAS une mesure pure de force de combat
(confondue par playrate, coût, contexte de comp). Ce diagnostic compare donc des RANGS au sein
d'un même coût, sur un board contrôlé (même support + items, seul le carry change), contre un
board baseline fixe. Objectif : (1) vérifier une corrélation positive globale, (2) surtout
repérer les OUTLIERS — unités que le moteur juge très différemment de datatft = candidats à un
bug de fidélité d'ability.
"""

from __future__ import annotations

import numpy as np

from tft_goat.data.content import load_set
from tft_goat.data.datatft import load_meta_stats
from tft_goat.engine.simulate import run_combat
from tft_goat.env.state import BoardUnit

N_FIGHTS = 300
# Core partagé de 6 unités (tanks + carries + support) => l'unité variée n'a qu'un impact
# MARGINAL, ce qui étale les win rates (moins de blowouts 0/100) et isole sa valeur de combat.
CORE = [
    "TFT17_Shen", "TFT17_TahmKench", "TFT17_Rammus",  # frontline
    "TFT17_Morgana", "TFT17_Karma", "TFT17_Nami",      # backline / support
]
BASELINE_CARRY = "TFT17_Vex"  # 7e unité de référence pour le board adverse fixe


def _board(carry: str, star: int = 2) -> list[BoardUnit]:
    return [BoardUnit(u, 2) for u in CORE] + [BoardUnit(carry, star)]


def win_rate(carry: str, content, rng) -> float:
    baseline = _board(BASELINE_CARRY)
    test = _board(carry)
    # Camps alternés : tout biais résiduel team0/team1 du moteur s'annule en espérance
    # (le pathing est désormais rng-équitable, mais on ne mesure jamais à travers un
    # biais de camp — cf. tests/test_pathing_symmetry.py).
    wins = 0
    for i in range(N_FIGHTS):
        if i % 2 == 0:
            wins += run_combat(test, baseline, content, rng).winner == 0
        else:
            wins += run_combat(baseline, test, content, rng).winner == 1
    return wins / N_FIGHTS


def spearman(xs: list[float], ys: list[float]) -> float:
    """Corrélation de rang de Spearman (sans scipy)."""
    def ranks(v: list[float]) -> list[float]:
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for rank, i in enumerate(order):
            r[i] = rank
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def main() -> None:
    content = load_set()
    meta = load_meta_stats()
    rng = np.random.default_rng(42)

    carries = [
        api for api, c in content.champions.items()
        if api.startswith("TFT17_") and c.cost == 5 and api != BASELINE_CARRY
        and api in meta.units
    ]
    rows = []
    for c in carries:
        wr = win_rate(c, content, rng)
        avg_place = meta.units[c].avg_place
        rows.append((content.champions[c].name, wr, avg_place))

    wrs = [r[1] for r in rows]
    places = [r[2] for r in rows]
    # datatft : place BASSE = meilleur ; on corrèle win_rate avec (-avg_place)
    rho = spearman(wrs, [-p for p in places])

    print(f"5-cost carries (vs board baseline {BASELINE_CARRY}), {N_FIGHTS} combats chacun\n")
    print(f"{'Carry':16} {'win_rate':>9} {'datatft place':>14}")
    for name, wr, pl in sorted(rows, key=lambda r: -r[1]):
        print(f"{name:16} {wr:>9.2f} {pl:>14.2f}")
    print(f"\nSpearman(win_rate, -avg_place) = {rho:+.2f}")
    print("(+1 = moteur parfaitement aligné sur le rang datatft ; ~0 = décorrélé)")


if __name__ == "__main__":
    main()
