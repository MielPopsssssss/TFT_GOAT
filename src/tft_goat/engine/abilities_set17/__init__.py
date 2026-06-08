"""Sorts du Set 17, remplis par lots (batch_*.py). Auto-agreges ici.

Chaque module `batch_*.py` expose `REGISTRY: dict[str, callable]` (apiName -> fn de sort).
On les fusionne dans SET17_ABILITIES. Un batch defaillant est ignore (avec warning) pour ne pas
casser tout le moteur.
"""

from __future__ import annotations

import importlib
import pkgutil
import warnings

SET17_ABILITIES: dict[str, callable] = {}

for _mod in pkgutil.iter_modules(__path__):
    if not _mod.name.startswith("batch_"):
        continue
    try:
        _m = importlib.import_module(f"{__name__}.{_mod.name}")
        SET17_ABILITIES.update(getattr(_m, "REGISTRY", {}))
    except Exception as exc:  # noqa: BLE001
        warnings.warn(f"batch '{_mod.name}' non charge : {exc}")
