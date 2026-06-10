"""Benchmark de fidélité ULTIME : le moteur prédit-il les placements de VRAIES parties ?

Pour chaque vraie partie challenger (data/matches/matches_17.4.jsonl) : reconstruit les
8 boards finaux (champion/étoiles/items réels), joue un round-robin EngineResolver entre
les 8, et corrèle le classement prédit (victoires) au placement réel.

C'est la vérité terrain de « fidélité d'abord » : contrairement à realism_vs_datatft
(avg_place méta, confondu par playrate/itemisation), ici chaque comparaison est interne
à une vraie partie — même lobby, mêmes conditions.

Limites assumées : boards finaux = au moment de l'élimination (les éliminés tôt ont des
boards plus petits — c'est un VRAI signal de force) ; pas d'augments (Riot les a retirés
de match-v1) ; pas de positionnement réel (placement auto du moteur).

Usage : .venv/bin/python -m scripts.realism_vs_matches [n_matches] [fights_par_paire]
"""

from __future__ import annotations

import json
import sys
from itertools import combinations

import numpy as np

from scripts.realism_vs_datatft import spearman
from tft_goat.data.content import load_set
from tft_goat.engine.simulate import run_combat
from tft_goat.env.state import BoardUnit

MATCHES_PATH = "data/matches/matches_17.4.jsonl"


def board_of(participant, content) -> list[BoardUnit]:
    """Board final réel -> BoardUnits (champions/étoiles/items connus du contenu)."""
    board = []
    for u in participant.get("units", []):
        api = u.get("character_id", "")
        if api not in content.champions:
            continue  # unités hors set (PvE/cosmétiques) — ignorées
        items = tuple(i for i in u.get("itemNames", []) if i in content.items)
        board.append(BoardUnit(api, int(u.get("tier", 1)), on_board=True,
                               items=len(items), item_apis=items))
    return board


def predict_scores(boards: list[list[BoardUnit]], content, rng,
                   fights_per_pair: int) -> list[float]:
    """Round-robin moteur : score = victoires (camps alternés, cf. test_pathing_symmetry)."""
    wins = [0.0] * len(boards)
    for i, j in combinations(range(len(boards)), 2):
        for k in range(fights_per_pair):
            if k % 2 == 0:
                r = run_combat(boards[i], boards[j], content, rng)
                wins[i if r.winner == 0 else j] += 1
            else:
                r = run_combat(boards[j], boards[i], content, rng)
                wins[j if r.winner == 0 else i] += 1
    return wins


def main() -> None:
    n_matches = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    fights = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    content = load_set()
    rng = np.random.default_rng(42)

    rhos, top1_hits, n_used = [], 0, 0
    with open(MATCHES_PATH) as f:
        for line in f:
            if n_used >= n_matches:
                break
            match = json.loads(line)
            parts = match.get("info", {}).get("participants", [])
            if len(parts) != 8:
                continue
            boards = [board_of(p, content) for p in parts]
            placements = [int(p.get("placement", 0)) for p in parts]
            if any(not b for b in boards) or any(pl < 1 for pl in placements):
                continue  # board vide ou placement manquant (data incomplète) — ignorée
            scores = predict_scores(boards, content, rng, fights)
            rhos.append(spearman(scores, [-pl for pl in placements]))
            predicted_winner = int(np.argmax(scores))
            top1_hits += placements[predicted_winner] <= 2  # le « gagnant moteur » a fini top2
            n_used += 1

    if not rhos:
        print("Aucune partie exploitable (data incomplète ou n_matches=0).")
        return
    rho_mean = float(np.mean(rhos))
    rho_se = float(np.std(rhos) / max(1, len(rhos)) ** 0.5)
    print(f"Moteur vs {n_used} vraies parties challenger "
          f"({fights} combats/paire, {28 * fights} combats/partie)\n")
    print(f"  Spearman(classement moteur, placement réel) = {rho_mean:+.3f} ± {rho_se:.3f}")
    print(f"  « gagnant moteur » finit top2 réel           = {top1_hits}/{n_used} "
          f"({100 * top1_hits / max(1, n_used):.0f}%)")
    print(f"  distribution rho : min {min(rhos):+.2f} | "
          f"p25 {np.percentile(rhos, 25):+.2f} | médiane {np.median(rhos):+.2f} | "
          f"p75 {np.percentile(rhos, 75):+.2f} | max {max(rhos):+.2f}")
    print("\n(+1 = le moteur reproduit parfaitement l'ordre réel ; 0 = décorrélé.")
    print(" Référence : les placements réels intègrent éco/augments/pilotage —")
    print(" un moteur de combat parfait ne ferait PAS +1.0, mais doit être nettement > 0.)")


if __name__ == "__main__":
    main()
