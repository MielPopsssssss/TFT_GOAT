"""Modeles immuables des donnees post-game (match-v1).

Sous-ensemble des champs utiles pour entrainer le combat surrogate (etape 4) :
board final, traits, augments, placement de chaque joueur.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)


class BoardUnit(_Frozen):
    """Une unite sur le board final d'un joueur."""

    character_id: str  # -> mappe sur SetContent.champions[apiName]
    tier: int  # niveau d'etoile 1..3
    rarity: int = 0
    items: tuple[str, ...] = ()  # apiNames d'items (itemNames)


class ParsedTrait(_Frozen):
    name: str
    num_units: int
    style: int = 0
    tier_current: int = 0
    tier_total: int = 0


class Participant(_Frozen):
    """Un des 8 joueurs d'une partie."""

    puuid: str
    placement: int
    level: int
    gold_left: int
    last_round: int
    units: tuple[BoardUnit, ...] = ()
    traits: tuple[ParsedTrait, ...] = ()
    augments: tuple[str, ...] = ()


class Match(_Frozen):
    """Une partie parsee : metadonnees + 8 participants."""

    match_id: str
    set_number: int
    game_version: str
    queue_id: int = Field(default=0)
    participants: tuple[Participant, ...] = ()
