"""Recuperation des vraies stats meta depuis l'API datatft + snapshot pin par patch.

API non officielle (reverse-engineered) :
  POST https://api.datatft.com/data/explore/list
  body {"version": "<patch>", "tier": "all", "filterTargetType": "hero"|"trait"|"equip"}
Nomenclature datatft : hero = champion, equip = objet, trait = trait, hex = augment.
NB verifie (2026-06) : datatft n'expose QUE des stats META (place/top4/win/count/best items).
Aucune donnee statique (HP/AD/sorts/recettes/tiers) ; le champ augments (`hex`/`hexs`) est vide
cote API. La donnee statique reste CommunityDragon. On fige une copie locale par patch.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx

from ..config import CURRENT_PATCH, DATA_DIR
from .stats_models import ItemStat, MetaStats, TraitStat, UnitStat

DATATFT_URL = "https://api.datatft.com/data/explore/list"
_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Origin": "https://www.datatft.com",
    "Referer": "https://www.datatft.com/",
}
DATATFT_DIR = DATA_DIR / "datatft"


def snapshot_path(patch: str = CURRENT_PATCH) -> Path:
    return DATATFT_DIR / f"datatft_{patch}.json"


# Cle de la liste retournee selon le type demande (les autres champs sont des agregats).
_LIST_KEY = {"hero": "units", "trait": "traits", "equip": "equips"}


def fetch_explore(filter_target_type: str, version: str = CURRENT_PATCH, tier: str = "all") -> list[dict]:
    """POST explore/list ; retourne la liste brute (units/traits/equips). Leve si code != 1."""
    body = {"version": version, "tier": tier, "filterTargetType": filter_target_type}
    resp = httpx.post(DATATFT_URL, json=body, headers=_HEADERS, timeout=30.0)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code") != 1:
        raise RuntimeError(f"datatft a renvoye code={payload.get('code')} pour {filter_target_type}")
    data = payload["data"]
    key = _LIST_KEY.get(filter_target_type)
    if key:
        return data.get(key) or []
    return data.get("units") or data.get("traits") or data.get("equips") or []


def download_snapshot(patch: str = CURRENT_PATCH, *, force: bool = False) -> Path:
    """Fige hero + trait + equip (toute la base meta datatft) pour `patch` dans un seul JSON."""
    dest = snapshot_path(patch)
    if dest.exists() and not force:
        return dest
    DATATFT_DIR.mkdir(parents=True, exist_ok=True)
    raw = {
        "patch": patch,
        "units": fetch_explore("hero", patch),
        "traits": fetch_explore("trait", patch),
        "items": fetch_explore("equip", patch),
    }
    tmp = dest.with_suffix(".json.part")
    tmp.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    tmp.replace(dest)
    return dest


def _parse_unit(r: dict) -> UnitStat:
    return UnitStat(
        key=r["key"],
        avg_place=float(r.get("place") or 0.0),
        top4=float(r.get("top4") or 0.0),
        win=float(r.get("won") or 0.0),
        count=int(r.get("count") or 0),
        place3=float(r.get("place3") or 0.0),
        rate3=float(r.get("rate3") or 0.0),
        best_items=tuple(str(x) for x in (r.get("equips") or [])),
    )


def _parse_trait(r: dict) -> TraitStat:
    return TraitStat(
        key=r["key"],
        tier=int(r.get("tier") or 0),
        avg_place=float(r.get("place") or 0.0),
        top4=float(r.get("top4") or 0.0),
        win=float(r.get("won") or 0.0),
        count=int(r.get("count") or 0),
    )


def _parse_item(r: dict) -> ItemStat:
    return ItemStat(
        key=r["key"],
        avg_place=float(r.get("place") or 0.0),
        top4=float(r.get("top4") or 0.0),
        win=float(r.get("won") or 0.0),
        count=int(r.get("count") or 0),
        best_units=tuple(str(x) for x in (r.get("heros") or [])),
    )


def build_meta_stats(raw: dict, patch: str = CURRENT_PATCH) -> MetaStats:
    """Construit un MetaStats depuis un dict {units, traits, items} deja charge."""
    units = {u["key"]: _parse_unit(u) for u in raw.get("units", [])}
    traits = {}
    for t in raw.get("traits", []):
        ts = _parse_trait(t)
        traits[MetaStats.trait_key(ts.key, ts.tier)] = ts
    items = {i["key"]: _parse_item(i) for i in raw.get("items", [])}
    return MetaStats(patch=patch, units=units, traits=traits, items=items)


def load_meta_stats(patch: str = CURRENT_PATCH) -> MetaStats:
    """Charge les stats meta pour `patch` (telecharge le snapshot s'il manque)."""
    path = snapshot_path(patch)
    if not path.exists():
        download_snapshot(patch)
    raw = json.loads(path.read_text(encoding="utf-8"))
    return build_meta_stats(raw, patch)
