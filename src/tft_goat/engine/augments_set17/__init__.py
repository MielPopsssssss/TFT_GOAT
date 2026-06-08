"""Logique des augments de COMBAT, par lots (batch_*.py). Auto-agreges.

Seuls les augments ayant un effet de combat sont enregistres ; les augments d'economie/utilite
sont omis (no-op implicite). Chaque batch expose :
  REGISTRY = {augment_api: fn(team, enemies, ctx, variables)}
ou `team`/`enemies` sont des listes de CombatUnit vivants, `ctx` le CombatContext, et
`variables` = dict des valeurs numeriques reelles de l'augment (depuis la data, deja au bon tier
bronze/silver/gold/prismatic puisque chaque apiName est un tier specifique).
"""

from __future__ import annotations

import importlib
import pkgutil
import warnings

AUGMENT_REGISTRY: dict[str, callable] = {}

for _mod in pkgutil.iter_modules(__path__):
    if not _mod.name.startswith("batch_"):
        continue
    try:
        _m = importlib.import_module(f"{__name__}.{_mod.name}")
        AUGMENT_REGISTRY.update(getattr(_m, "REGISTRY", {}))
    except Exception as exc:  # noqa: BLE001
        warnings.warn(f"augment batch '{_mod.name}' non charge : {exc}")
