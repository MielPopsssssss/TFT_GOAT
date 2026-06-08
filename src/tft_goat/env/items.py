"""Composants de base + recettes d'objets complets, dérivés de la vraie data.

Un objet complet a une `composition` de 2 composants de base. La combinaison de 2 composants
donne l'objet complet correspondant (recette réelle). Mis en cache par patch.
"""

from __future__ import annotations

from ..data.models import SetContent

_CACHE: dict[str, tuple[list[str], dict[tuple[str, str], str]]] = {}


def _is_component(api: str, content: SetContent) -> bool:
    it = content.items.get(api)
    return it is not None and len(it.composition) == 0


def _build(content: SetContent) -> tuple[list[str], dict[tuple[str, str], str]]:
    completed = [
        (api, it) for api, it in content.items.items()
        if len(it.composition) == 2 and "_Augment_" not in api
    ]
    refs: set[str] = set()
    for _, it in completed:
        refs.update(it.composition)
    components = sorted(c for c in refs if _is_component(c, content))
    recipes: dict[tuple[str, str], str] = {}
    for api, it in completed:
        if all(_is_component(c, content) for c in it.composition):
            recipes[tuple(sorted(it.composition))] = api
    return components, recipes


def components_and_recipes(content: SetContent) -> tuple[list[str], dict[tuple[str, str], str]]:
    key = content.patch
    if key not in _CACHE:
        _CACHE[key] = _build(content)
    return _CACHE[key]


def combine(c1: str, c2: str, content: SetContent) -> str | None:
    """Objet complet obtenu en combinant 2 composants (None si paire invalide)."""
    _, recipes = components_and_recipes(content)
    return recipes.get(tuple(sorted([c1, c2])))
