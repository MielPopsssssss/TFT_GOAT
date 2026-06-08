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


def trait_counts(board_champions: Iterable[str], set_content: SetContent) -> dict[str, int]:
    """Nombre de champions uniques par trait sur le board."""
    counts: dict[str, int] = {}
    seen: set[str] = set()
    for api in board_champions:
        if api in seen:
            continue
        seen.add(api)
        champ = set_content.champions.get(api)
        if champ is None:
            continue
        for trait_name in champ.traits:
            counts[trait_name] = counts.get(trait_name, 0) + 1
    return counts


def active_traits(
    board_champions: Iterable[str], set_content: SetContent
) -> dict[str, int]:
    """Retourne {nom_trait: tier} pour les traits ayant atteint au moins leur 1er palier.

    `tier` = nombre de breakpoints atteints (1 = premier palier, 2 = deuxieme, ...).
    """
    by_name = _traits_by_name(set_content)
    result: dict[str, int] = {}
    for name, count in trait_counts(board_champions, set_content).items():
        trait = by_name.get(name)
        if trait is None:
            continue
        tier = sum(1 for bp in trait.breakpoints if count >= bp)
        if tier > 0:
            result[name] = tier
    return result
