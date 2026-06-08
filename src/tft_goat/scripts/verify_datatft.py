"""Vérifie que les données meta datatft sont cohérentes avec notre contenu CDragon.

datatft = couche META (place/top4/win/count/best items) ; notre contenu = data STATIQUE
(CommunityDragon). La vérification = cohérence des rosters : chaque champion/objet/trait suivi
par datatft doit exister dans notre contenu. Toute clé manquante est un signal (data manquante
chez nous, OU item hors-pool comme les artefacts de dieu).

Usage : .venv/bin/python -m tft_goat.scripts.verify_datatft [--refresh]
"""

from __future__ import annotations

import sys

from ..data.content import load_set
from ..data.datatft import download_snapshot, load_meta_stats


def _section(title: str, datatft_keys: set[str], content_keys: set[str]) -> int:
    missing = sorted(k for k in datatft_keys if k not in content_keys)
    extra = len(content_keys) - (len(datatft_keys) - len(missing))
    status = "✅" if not missing else "⚠️"
    print(f"\n[{title}] {status}  datatft suit {len(datatft_keys)} | "
          f"manquants chez nous: {len(missing)} | nous en avons ~{extra} de plus (non-meta)")
    for k in missing:
        print(f"   ⚠️  ABSENT de notre contenu : {k}")
    return len(missing)


def main(refresh: bool = False) -> int:
    if refresh:
        download_snapshot(force=True)
    meta = load_meta_stats()
    sc = load_set()
    print(f"=== Vérification datatft ↔ contenu (patch {meta.patch}) ===")
    print(f"datatft meta : {len(meta.units)} champions, {len(meta.items)} objets, "
          f"{len({k.split('|')[0] for k in meta.traits})} traits")

    miss = 0
    miss += _section("CHAMPIONS", set(meta.units), set(sc.champions))
    miss += _section("OBJETS", set(meta.items), set(sc.items))
    miss += _section("TRAITS", {k.split("|")[0] for k in meta.traits}, set(sc.traits))

    print("\n" + ("✅ Cohérence totale : tout ce que datatft suit existe dans notre contenu."
                  if miss == 0 else
                  f"⚠️ {miss} clé(s) suivie(s) par datatft absente(s) de notre contenu "
                  "(voir détail ci-dessus — souvent des items hors-pool, ex. artefacts de dieu)."))
    return miss


if __name__ == "__main__":
    sys.exit(0 if main("--refresh" in sys.argv) == 0 else 0)  # rapport, pas d'echec CI
