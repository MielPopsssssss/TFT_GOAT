"""Calcul des traits actifs d'un board. Fonction pure.

TFT compte les *champions uniques* : poser deux copies du meme champion ne compte qu'une
fois pour les traits. Le palier (tier) est l'index du plus haut breakpoint atteint.
"""

from __future__ import annotations

from collections.abc import Iterable

from ..data.models import SetContent, Trait


def _traits_by_name(set_content: SetContent) -> dict[str, Trait]:
    """Index nom d'affichage -> Trait (les champions referencent les traits par nom)."""
    return {t.name: t for t in set_content.traits.values()}


def unit_trait_names(unit: str | object, set_content: SetContent) -> set[str]:
    """Traits d'affichage d'une unite : traits natifs, plus ceux d'un emblem equipe.

    CDragon n'a pas de champ « granted trait ». Sur un emblem, le trait accorde est
    `incompatibleTraits` (on ne peut pas l'equiper a un porteur natif de ce trait).
    """
    api = unit if isinstance(unit, str) else unit.champion_api
    champ = set_content.champions.get(api)
    names = set(champ.traits) if champ is not None else set()
    if isinstance(unit, str):
        return names
    for item_api in getattr(unit, "item_apis", ()) or ():
        item = set_content.items.get(item_api)
        if item is None or "Emblem" not in item.api_name:
            continue
        for trait_api in item.incompatible_traits:
            trait = set_content.traits.get(trait_api)
            if trait is not None and trait.name:
                names.add(trait.name)
    return names


def trait_counts(board_units: Iterable, set_content: SetContent) -> dict[str, int]:
    """Nombre de champions uniques par trait. Accepte des apiNames ou des unites (`item_apis`)."""
    per_champ: dict[str, set[str]] = {}
    for unit in board_units:
        api = unit if isinstance(unit, str) else unit.champion_api
        per_champ.setdefault(api, set()).update(unit_trait_names(unit, set_content))
    counts: dict[str, int] = {}
    for names in per_champ.values():
        for trait_name in names:
            counts[trait_name] = counts.get(trait_name, 0) + 1
    return counts


def active_traits(
    board_units: Iterable, set_content: SetContent, *, bonus_units: int = 0
) -> dict[str, int]:
    """Retourne {nom_trait: tier} pour les traits ayant atteint au moins leur 1er palier.

    `tier` = nombre de breakpoints atteints (1 = premier palier, 2 = deuxieme, ...).
    `bonus_units` ajoute des champions virtuels a chaque trait non-unique PRESENT sur le
    board (God Boon LargeQuest : « +1 to all non-unique traits ») ; les traits uniques
    (breakpoints == (1,)) ne sont jamais boostes, et aucun trait n'est cree ex nihilo.
    """
    by_name = _traits_by_name(set_content)
    result: dict[str, int] = {}
    for name, count in trait_counts(board_units, set_content).items():
        trait = by_name.get(name)
        if trait is None:
            continue
        bps = tuple(trait.breakpoints)
        n = count + (bonus_units if bps != (1,) else 0)
        tier = sum(1 for bp in bps if n >= bp)
        if tier > 0:
            result[name] = tier
    return result
