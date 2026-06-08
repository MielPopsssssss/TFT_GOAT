"""Construction du `SetContent` immuable a partir du JSON CommunityDragon.

C'est la frontiere de validation : le JSON brut (heterogene, avec des `null` et des cles
variables) entre ici, des modeles Pydantic types et immuables en sortent.
"""

from __future__ import annotations

from ..config import CURRENT_PATCH, SET_MUTATOR, SET_NUMBER
from .augment_tiers import detect_tier
from .cdragon import load_raw
from .models import (
    Ability,
    Augment,
    Champion,
    Item,
    SetContent,
    Stats,
    Trait,
    TraitEffect,
)


def _numeric(d: dict | None) -> dict[str, float]:
    """Ne garde que les valeurs numeriques d'un dict d'effets (filtre les `null`)."""
    if not d:
        return {}
    return {k: float(v) for k, v in d.items() if isinstance(v, (int, float))}


def _f(value) -> float:
    """Coerce une valeur potentiellement `null` en float (0.0 par defaut)."""
    return float(value) if isinstance(value, (int, float)) else 0.0


def _parse_stats(raw: dict | None) -> Stats | None:
    if not raw:
        return None
    return Stats(
        hp=_f(raw.get("hp")),
        armor=_f(raw.get("armor")),
        magic_resist=_f(raw.get("magicResist")),
        damage=_f(raw.get("damage")),
        attack_speed=_f(raw.get("attackSpeed")),
        mana=_f(raw.get("mana")),
        initial_mana=_f(raw.get("initialMana")),
        crit_chance=_f(raw.get("critChance")),
        crit_multiplier=_f(raw.get("critMultiplier")),
        attack_range=_f(raw.get("range")),
    )


def _parse_ability(raw: dict | None) -> Ability | None:
    if not raw:
        return None
    variables = {
        v["name"]: tuple(float(x) for x in (v.get("value") or []) if isinstance(x, (int, float)))
        for v in raw.get("variables", [])
        if v.get("name")
    }
    return Ability(name=raw.get("name") or "", desc=raw.get("desc") or "", variables=variables)


def _parse_champion(raw: dict) -> Champion:
    return Champion(
        api_name=raw["apiName"],
        name=raw.get("name") or "",
        cost=int(raw.get("cost") or 0),
        traits=tuple(raw.get("traits") or []),
        role=raw.get("role") or "",
        stats=_parse_stats(raw.get("stats")),
        ability=_parse_ability(raw.get("ability")),
    )


def _parse_trait(raw: dict) -> Trait:
    effects = tuple(
        TraitEffect(
            min_units=int(e.get("minUnits") or 0),
            max_units=int(e.get("maxUnits") or e.get("minUnits") or 0),
            style=int(e.get("style") or 0),
            variables=_numeric(e.get("variables")),
        )
        for e in raw.get("effects", [])
    )
    return Trait(api_name=raw["apiName"], name=raw.get("name") or "", effects=effects)


def _parse_item(raw: dict) -> Item:
    return Item(
        api_name=raw["apiName"],
        name=raw.get("name") or "",
        composition=tuple(raw.get("composition") or []),
        effects=_numeric(raw.get("effects")),
        tags=tuple(raw.get("tags", [])),
        unique=bool(raw.get("unique", False)),
        associated_traits=tuple(raw.get("associatedTraits", [])),
        incompatible_traits=tuple(raw.get("incompatibleTraits", [])),
    )


def _parse_augment(raw: dict) -> Augment:
    return Augment(
        api_name=raw["apiName"],
        name=raw.get("name") or "",
        desc=raw.get("desc") or "",
        tier=detect_tier(raw["apiName"], raw.get("icon")),  # silver/gold/prismatic (vrai tier TFT)
        composition=tuple(raw.get("composition") or []),
        effects=_numeric(raw.get("effects")),
        tags=tuple(raw.get("tags", [])),
        associated_traits=tuple(raw.get("associatedTraits", [])),
    )


def build_set_content(raw: dict, patch: str = CURRENT_PATCH) -> SetContent:
    """Construit un `SetContent` depuis un dict CDragon deja charge.

    Separe du chargement disque pour permettre les tests sur un fixture en memoire.
    """
    set_data = next(
        (s for s in raw["setData"] if s.get("mutator") == SET_MUTATOR), None
    )
    if set_data is None:
        raise ValueError(f"Set {SET_MUTATOR} introuvable dans le JSON CDragon")

    items_by_api = {it["apiName"]: it for it in raw.get("items", [])}

    champions = {c["apiName"]: _parse_champion(c) for c in set_data.get("champions", [])}
    traits = {t["apiName"]: _parse_trait(t) for t in set_data.get("traits", [])}

    items = {
        api: _parse_item(items_by_api[api])
        for api in set_data.get("items", [])
        if api in items_by_api
    }
    augments = {
        api: _parse_augment(items_by_api[api])
        for api in set_data.get("augments", [])
        if api in items_by_api
    }

    return SetContent(
        patch=patch,
        set_number=SET_NUMBER,
        champions=champions,
        traits=traits,
        items=items,
        augments=augments,
    )


def load_set(patch: str = CURRENT_PATCH) -> SetContent:
    """Charge le contenu complet du set pour `patch` (telecharge le snapshot si besoin)."""
    return build_set_content(load_raw(patch), patch)
