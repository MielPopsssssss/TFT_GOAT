"""Scrape + fige les vraies stats meta datatft pour un patch.

Usage : .venv/bin/python -m tft_goat.scripts.scrape_datatft [--patch 17.4] [--force]
"""

from __future__ import annotations

import argparse

from ..config import CURRENT_PATCH
from ..data.datatft import download_snapshot, load_meta_stats


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--patch", default=CURRENT_PATCH)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    path = download_snapshot(args.patch, force=args.force)
    meta = load_meta_stats(args.patch)
    print(f"Snapshot ecrit : {path}")
    print(f"  {len(meta.units)} units, {len(meta.traits)} lignes de traits (patch {meta.patch})")
    best = sorted(meta.units.values(), key=lambda u: u.avg_place)[:5]
    print("  Top 5 unites par placement moyen :")
    for u in best:
        print(f"    {u.key:<22} place={u.avg_place:.3f}  top4={u.top4:.1f}%  count={u.count}")


if __name__ == "__main__":
    main()
