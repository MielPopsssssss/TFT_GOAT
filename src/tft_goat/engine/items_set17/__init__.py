"""Effets (procs) des objets completes, par lots (batch_*.py). Auto-agreges.

Les bonus de STATS des objets sont deja appliques automatiquement (data) dans unit.build_unit.
Ici on code seulement la LOGIQUE des procs. Chaque batch expose des dicts optionnels :
  COMBAT_START = {item_api: fn(unit, ctx)}            # auras/boucliers/regen au debut du combat
  ON_ATTACK    = {item_api: fn(unit, target, ctx)}    # proc a chaque auto-attaque
  ON_CAST      = {item_api: fn(unit, ctx)}            # proc quand l'unite lance son sort
  ON_DAMAGED   = {item_api: fn(unit, attacker, ctx)}  # proc quand l'unite SUBIT des degats (reflect)
  ON_TICK      = {item_api: fn(unit, ctx)}            # proc periodique (~1/s) : regen, etc.
  HP_THRESHOLD = {item_api: (frac, fn(unit, ctx))}    # proc unique sous frac% de PV (bouclier...)
  REVIVE       = {item_api: fn(unit, ctx)}            # a la mort : ressuscite l'unite (une fois)
"""

from __future__ import annotations

import importlib
import pkgutil
import warnings

ITEM_COMBAT_START: dict[str, callable] = {}
ITEM_ON_ATTACK: dict[str, callable] = {}
ITEM_ON_CAST: dict[str, callable] = {}
ITEM_ON_DAMAGED: dict[str, callable] = {}
ITEM_ON_TICK: dict[str, callable] = {}
ITEM_HP_THRESHOLD: dict[str, tuple] = {}
ITEM_REVIVE: dict[str, callable] = {}

for _mod in pkgutil.iter_modules(__path__):
    if not _mod.name.startswith("batch_"):
        continue
    try:
        _m = importlib.import_module(f"{__name__}.{_mod.name}")
        ITEM_COMBAT_START.update(getattr(_m, "COMBAT_START", {}))
        ITEM_ON_ATTACK.update(getattr(_m, "ON_ATTACK", {}))
        ITEM_ON_CAST.update(getattr(_m, "ON_CAST", {}))
        ITEM_ON_DAMAGED.update(getattr(_m, "ON_DAMAGED", {}))
        ITEM_ON_TICK.update(getattr(_m, "ON_TICK", {}))
        ITEM_HP_THRESHOLD.update(getattr(_m, "HP_THRESHOLD", {}))
        ITEM_REVIVE.update(getattr(_m, "REVIVE", {}))
    except Exception as exc:  # noqa: BLE001
        warnings.warn(f"item batch '{_mod.name}' non charge : {exc}")
