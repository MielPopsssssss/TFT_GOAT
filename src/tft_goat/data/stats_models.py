"""Modeles immuables des vraies stats meta (datatft) + facteur de force.

Le placement moyen d'une unite/trait sert de proxy de « force reelle » pour le combat v0
(meilleur placement = plus fort), borne pour rester stable. Caveat : le placement reflete la
compo entiere, pas la seule puissance de combat -> proxy raisonnable, remplace par le surrogate
appris a l'etape 4.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

BASELINE_PLACE = 4.5  # placement moyen neutre (8 joueurs)
POWER_MIN = 0.5
POWER_MAX = 2.0


def place_to_power(place: float, baseline: float = BASELINE_PLACE) -> float:
    """Facteur de force a partir d'un placement moyen, borne [POWER_MIN, POWER_MAX]."""
    if place <= 0:
        return 1.0
    return max(POWER_MIN, min(POWER_MAX, baseline / place))


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)


class UnitStat(_Frozen):
    key: str  # apiName, ex. TFT17_Nunu
    avg_place: float
    top4: float
    win: float
    count: int
    place3: float = 0.0
    rate3: float = 0.0
    best_items: tuple[str, ...] = ()


class TraitStat(_Frozen):
    key: str  # apiName du trait
    tier: int  # palier (1..)
    avg_place: float
    top4: float
    win: float
    count: int


class ItemStat(_Frozen):
    key: str  # apiName de l'objet complet
    avg_place: float
    top4: float
    win: float
    count: int
    best_units: tuple[str, ...] = ()  # unites portant le mieux cet objet (heros)


class MetaStats(_Frozen):
    patch: str
    units: dict[str, UnitStat] = Field(default_factory=dict)
    # cle = "<trait_api>|<tier>"
    traits: dict[str, TraitStat] = Field(default_factory=dict)
    items: dict[str, ItemStat] = Field(default_factory=dict)

    @staticmethod
    def trait_key(api: str, tier: int) -> str:
        return f"{api}|{tier}"

    def unit_power(self, key: str) -> float:
        """Force relative d'une unite (1.0 neutre si stat absente)."""
        stat = self.units.get(key)
        return place_to_power(stat.avg_place) if stat else 1.0

    def trait_power(self, api: str, tier: int) -> float:
        """Force relative d'un palier de trait (1.0 neutre si stat absente)."""
        stat = self.traits.get(self.trait_key(api, tier))
        return place_to_power(stat.avg_place) if stat else 1.0
