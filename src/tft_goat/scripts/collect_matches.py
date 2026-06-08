"""Collecte de parties TFT match-v1 (cle dev RIOT_API_KEY) -> dataset jsonl.

Part du ladder challenger, remonte les PUUID, recupere leurs parties recentes, filtre le set
courant, et ecrit une partie brute par ligne. Throttle pour respecter le rate-limit dev
(20 req/s ET 100 req / 2 min).

Usage : RIOT_API_KEY=... .venv/bin/python -m tft_goat.scripts.collect_matches --matches 150
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from riotwatcher import ApiError

from ..config import DATA_DIR, SET_NUMBER, CURRENT_PATCH
from ..data.riot.client import tft_watcher

THROTTLE_S = 1.3  # ~46 req/min, sous la limite 100/2min


def _call(fn, *a, **k):
    """Appel API avec throttle + un retry sur 429."""
    for attempt in range(2):
        try:
            time.sleep(THROTTLE_S)
            return fn(*a, **k)
        except ApiError as e:
            if e.response.status_code == 429 and attempt == 0:
                print("  429 -> pause 15s")
                time.sleep(15)
                continue
            raise


def collect(args) -> None:
    w = tft_watcher()
    platform, region = args.platform, args.region

    print(f"ladder challenger {platform}...")
    ladder = _call(w.league.challenger, platform)
    puuids = [e["puuid"] for e in ladder["entries"] if e.get("puuid")]
    print(f"  {len(puuids)} joueurs challenger")

    seen_ids: set[str] = set()
    out_path = Path(args.out or DATA_DIR / "matches" / f"matches_{args.patch}.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for pi, puuid in enumerate(puuids):
            if kept >= args.matches:
                break
            try:
                ids = _call(w.match.by_puuid, region, puuid, count=args.per_player)
            except ApiError as e:
                print(f"  skip joueur ({e.response.status_code})")
                continue
            for mid in ids:
                if kept >= args.matches or mid in seen_ids:
                    continue
                seen_ids.add(mid)
                try:
                    detail = _call(w.match.by_id, region, mid)
                except ApiError as e:
                    print(f"  skip match ({e.response.status_code})")
                    continue
                if detail["info"].get("tft_set_number") != SET_NUMBER:
                    continue
                fh.write(json.dumps(detail) + "\n")
                kept += 1
                if kept % 20 == 0:
                    print(f"  {kept}/{args.matches} parties (joueur {pi+1})")
    print(f"{kept} parties ecrites -> {out_path}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--matches", type=int, default=150)
    p.add_argument("--per-player", type=int, default=15)
    p.add_argument("--platform", default="euw1")
    p.add_argument("--region", default="europe")
    p.add_argument("--patch", default=CURRENT_PATCH)
    p.add_argument("--out", default="")
    collect(p.parse_args())


if __name__ == "__main__":
    main()
