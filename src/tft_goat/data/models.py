"""Modeles immuables du contenu d'un set TFT.

Tous les modeles sont `frozen` (immuabilite — cf. coding-style global). Ils sont remplis
par `content.load_set()` a partir du JSON CommunityDragon, qui sert de frontiere de
validation (Pydantic v2).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Frozen(BaseModel):
    """Base immuable commune."""

    model_config = ConfigDict(frozen=True)


class Stats(_Frozen):
    """Stats de base d'un champion (niveau 1 etoile)."""

    hp: float
    armor: float
    magic_resist: float
    damage: float
    attack_speed: float
    mana: float
    initial_mana: float
    crit_chance: float
    crit_multiplier: float
    attack_range: float


class Ability(_Frozen):
    """Sort d'un champion. `variables` mappe un nom -> valeur par niveau d'etoile."""

    name: str
    desc: str = ""
    variables: dict[str, tuple[float, ...]] = Field(default_factory=dict)


class Champion(_Frozen):
    api_name: str
    name: str
    cost: int
    traits: tuple[str, ...] = ()
    role: str = ""
    stats: Stats | None = None
    ability: Ability | None = None


class TraitEffect(_Frozen):
    """Un palier de trait. Le breakpoint est `min_units` (jamais `style`, qui bouge)."""

    min_units: int
    max_units: int
    style: int = 0
    variables: dict[str, float] = Field(default_factory=dict)


class Trait(_Frozen):
    api_name: str
    name: str
    effects: tuple[TraitEffect, ...] = ()

    @property
    def breakpoints(self) -> tuple[int, ...]:
        """Paliers d'activation, tries (ex. Bastion -> (2, 4, 6))."""
        return tuple(sorted(e.min_units for e in self.effects))


class Item(_Frozen):
    api_name: str
    name: str
    composition: tuple[str, ...] = ()  # apiNames des composants (vide si composant de base)
    effects: dict[str, float] = Field(default_factory=dict)
    tags: tuple[str, ...] = ()
    unique: bool = False
    associated_traits: tuple[str, ...] = ()
    incompatible_traits: tuple[str, ...] = ()


class Augment(_Frozen):
    api_name: str
    name: str
    desc: str = ""
    tier: str = "gold"  # silver / gold / prismatic (qualite TFT), ou "god" (boon Realm of the Gods)
    composition: tuple[str, ...] = ()
    effects: dict[str, float] = Field(default_factory=dict)
    tags: tuple[str, ...] = ()
    associated_traits: tuple[str, ...] = ()


class SetContent(_Frozen):
    """Contenu complet d'un set, indexe par apiName."""

    patch: str
    set_number: int
    champions: dict[str, Champion]
    traits: dict[str, Trait]
    items: dict[str, Item]
    augments: dict[str, Augment]
