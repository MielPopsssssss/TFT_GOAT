"""Diagnostic rho par partie du benchmark realism_vs_matches : bruit vs signal.

Pass 1 : réplique exacte de scripts.realism_vs_matches (rng(42) séquentiel, 4 fights)
         -> rho4 par partie, pour retrouver les parties « négatives » de la baseline.
Pass 2 : pour CHAQUE partie, rho à 16 fights/paire x 3 seeds indépendants
         -> rho stable ; un négatif persistant est un signal moteur, pas du bruit.

Sortie : table triée par rho16 croissant + détail par board (score moteur vs
placement réel, composition) des parties rho16 < 0.05 — la surface d'attaque
pour transformer chaque inversion en root cause (cf. investigation 2026-06-11 :
Riven passive absente, trait Meeple sans meeps).

Usage : .venv/bin/python -m scripts.diagnose_rho [n_matches]
"""

from __future__ import annotations

import json
import sys

import numpy as np

from scripts.realism_vs_datatft import spearman
from scripts.realism_vs_matches import MATCHES_PATH, board_of, predict_scores
from tft_goat.data.content import load_set

RHO_DETAIL_THRESHOLD = 0.05  # en dessous : breakdown par board


def load_matches(content, n_matches: int) -> list[tuple]:
    """Charge les parties exploitables (mêmes filtres que la baseline)."""
    matches = []
    with open(MATCHES_PATH) as f:
        for line in f:
            if len(matches) >= n_matches:
                break
            match = json.loads(line)
            parts = match.get("info", {}).get("participants", [])
            if len(parts) != 8:
                continue
            boards = [board_of(p, content) for p in parts]
            placements = [int(p.get("placement", 0)) for p in parts]
            if any(not b for b in boards) or any(pl < 1 for pl in placements):
                continue
            mid = match.get("metadata", {}).get("match_id", f"line{len(matches)}")
            matches.append((mid, boards, placements, parts))
    return matches


def main() -> None:
    n_matches = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    content = load_set()
    matches = load_matches(content, n_matches)
    print(f"{len(matches)} parties chargées")

    # pass 1 : réplique baseline (rng partagé séquentiel, comme realism_vs_matches)
    rng = np.random.default_rng(42)
    rho4s = []
    for _, boards, placements, _ in matches:
        scores = predict_scores(boards, content, rng, 4)
        rho4s.append(spearman(scores, [-pl for pl in placements]))

    # pass 2 : haute précision, seeds indépendants par partie (reproductible)
    results = []
    for idx, (mid, boards, placements, parts) in enumerate(matches):
        rhos, all_scores = [], []
        for s in range(3):
            rng2 = np.random.default_rng(10_000 + idx * 10 + s)
            sc = predict_scores(boards, content, rng2, 16)
            rhos.append(spearman(sc, [-pl for pl in placements]))
            all_scores.append(sc)
        results.append({
            "idx": idx, "mid": mid, "rho4": rho4s[idx],
            "rho16": float(np.mean(rhos)),
            "rho16_spread": [round(r, 2) for r in rhos],
            "scores": np.mean(all_scores, axis=0),
            "placements": placements, "parts": parts,
        })

    results.sort(key=lambda r: r["rho16"])
    print(f"\n{'idx':>3} {'rho4':>6} {'rho16':>6}  spread(3 seeds)        match_id")
    for r in results:
        print(f"{r['idx']:>3} {r['rho4']:+.2f} {r['rho16']:+.2f}  "
              f"{str(r['rho16_spread']):<22} {r['mid']}")

    agg16 = float(np.mean([r["rho16"] for r in results]))
    print(f"\nrho moyen baseline(4f)={float(np.mean(rho4s)):+.3f}  "
          f"haute précision(16f x3)={agg16:+.3f}")

    for r in results:
        if r["rho16"] >= RHO_DETAIL_THRESHOLD:
            continue
        print(f"\n=== idx {r['idx']} {r['mid']} rho4={r['rho4']:+.2f} "
              f"rho16={r['rho16']:+.2f} {r['rho16_spread']} ===")
        order = np.argsort(-r["scores"])  # mieux classé moteur d'abord
        for rank, i in enumerate(order, 1):
            p = r["parts"][i]
            units = " ".join(
                f"{u['character_id'].removeprefix('TFT17_')}*{u.get('tier', 1)}"
                + (f"({len([x for x in u.get('itemNames', []) if x in content.items])}i)"
                   if u.get("itemNames") else "")
                for u in p.get("units", []) if u.get("character_id") in content.champions
            )
            print(f"  moteur#{rank} (wins {r['scores'][i]:5.1f}) "
                  f"réel#{r['placements'][i]} lvl{p.get('level', '?')} | {units}")


if __name__ == "__main__":
    main()
