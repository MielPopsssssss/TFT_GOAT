"""Régénère docs/fiches/ : une fiche d'audit markdown par champion/trait/item/augment.

Usage : .venv/bin/python -m scripts.generate_fiches [out_dir]
(défaut : docs/fiches — les fiches sont versionnées ; un diff = un vrai changement
de data ou de couverture moteur, jamais une édition manuelle)
"""

from __future__ import annotations

import sys
from pathlib import Path

from tft_goat.data.content import load_set
from tft_goat.fiches import generate_all


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/fiches")
    content = load_set()
    paths = generate_all(content, out)
    total = sum(len(group) for group in paths.values())
    print(f"{total} fiches générées dans {out}/ (patch {content.patch})")
    for group, files in paths.items():
        print(f"  {group}: {len(files)}")


if __name__ == "__main__":
    main()
