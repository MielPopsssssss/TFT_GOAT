"""Statut d'implémentation moteur d'une entité (introspection des registres réels).

Aucune donnée inventée ici : on lit les registres du moteur (`engine/`) pour dire,
fiche par fiche, ce qui est réellement codé vs ce qui retombe sur un défaut/no-op.
"""

from __future__ import annotations

from ..data.gods import SET17_GODS
from ..data.models import Augment, SetContent, Trait
from ..engine.abilities import IMPLEMENTED
from ..engine.augments_set17 import AUGMENT_REGISTRY
from ..engine.items_set17 import (
    ITEM_COMBAT_START,
    ITEM_HP_THRESHOLD,
    ITEM_ON_ATTACK,
    ITEM_ON_CAST,
    ITEM_ON_DAMAGED,
    ITEM_ON_TICK,
    ITEM_REVIVE,
)
from ..engine.trait_effects import attrs_for

# Hooks de proc spéciaux du moteur, par nom lisible (l'ordre est celui de l'affichage).
_ITEM_HOOKS: dict[str, dict] = {
    "combat_start": ITEM_COMBAT_START,
    "on_attack": ITEM_ON_ATTACK,
    "on_cast": ITEM_ON_CAST,
    "on_damaged": ITEM_ON_DAMAGED,
    "on_tick": ITEM_ON_TICK,
    "hp_threshold": ITEM_HP_THRESHOLD,
    "revive": ITEM_REVIVE,
}


def ability_implemented(champion_api: str) -> bool:
    """Le sort du champion est-il codé dans `engine/abilities_set17` (sinon défaut générique) ?"""
    return champion_api in IMPLEMENTED


def item_proc_hooks(item_api: str) -> list[str]:
    """Hooks de proc spéciaux codés pour cet item ([] = stats uniquement)."""
    return [name for name, registry in _ITEM_HOOKS.items() if item_api in registry]


def augment_in_engine(augment_api: str) -> bool:
    """L'augment a-t-il un effet combat codé dans `engine/augments_set17` (sinon no-op) ?"""
    return augment_api in AUGMENT_REGISTRY


def trait_var_attrs(key: str) -> list[str]:
    """Stats auto-appliquées par le moteur pour une variable de trait ([] = non-stat)."""
    return attrs_for(key)


def god_of_augment(aug: Augment) -> str | None:
    """Dieu du Realm of the Gods dont cet augment est le God Boon (None si pas un boon).

    Même politique que `data/gods.py::god_boons` : un apiName matchant PLUSIEURS dieux est
    une donnée ambiguë -> erreur explicite, jamais devinée.
    """
    if aug.tier != "god":
        return None
    matched = [god for god, token in SET17_GODS.items() if token in aug.api_name]
    if len(matched) > 1:
        raise ValueError(f"God augment ambigu : {aug.api_name} matche plusieurs dieux {matched}")
    return matched[0] if matched else None


def trait_name_winner(content: SetContent) -> dict[str, str]:
    """Nom d'affichage -> apiName du trait que le moteur résout RÉELLEMENT.

    Le moteur joint les traits par nom d'affichage (`{t.name: t}` dans
    `engine/trait_effects.apply_team_traits` et `env/traits._traits_by_name`) : en cas
    d'homonymes (ex. 8 apiNames « Stargazer »), le dernier inséré gagne. Cette fonction
    réplique exactement cette construction pour que les fiches disent la vérité moteur.
    """
    return {t.name: api for api, t in content.traits.items()}


def shadowed_by(trait: Trait, content: SetContent) -> str | None:
    """apiName du trait homonyme que le moteur résout À LA PLACE (None si ce trait gagne)."""
    winner = trait_name_winner(content).get(trait.name)
    return winner if winner is not None and winner != trait.api_name else None
