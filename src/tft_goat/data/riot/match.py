"""Recuperation et parsing de parties TFT (squelette match-v1).

Squelette : quelques appels unitaires + parsing en modeles immuables, pour valider le
format. Le pipeline d'ingestion massif (stockage, reprise, batch) viendra a l'etape 4.

Routing regional : match-v1 et account-v1 sont routes par grande region
(`americas` | `asia` | `europe`), pas par plateforme.
"""

from __future__ import annotations

from .client import riot_watcher, tft_watcher
from .models import BoardUnit, Match, Participant, ParsedTrait

DEFAULT_REGION = "europe"


def puuid_by_riot_id(game_name: str, tag_line: str, region: str = DEFAULT_REGION) -> str:
    """Resout un Riot ID (gameName#tagLine) en PUUID via account-v1."""
    account = riot_watcher().account.by_riot_id(region, game_name, tag_line)
    return account["puuid"]


def recent_match_ids(
    puuid: str, count: int = 20, region: str = DEFAULT_REGION
) -> list[str]:
    """IDs des parties recentes d'un PUUID (max 20 par defaut sur cle dev)."""
    return tft_watcher().match.by_puuid(region, puuid, count=count)


def match_detail(match_id: str, region: str = DEFAULT_REGION) -> dict:
    """JSON brut d'une partie."""
    return tft_watcher().match.by_id(region, match_id)


def _parse_unit(raw: dict) -> BoardUnit:
    return BoardUnit(
        character_id=raw.get("character_id", ""),
        tier=int(raw.get("tier") or 0),
        rarity=int(raw.get("rarity") or 0),
        items=tuple(raw.get("itemNames") or []),
    )


def _parse_trait(raw: dict) -> ParsedTrait:
    return ParsedTrait(
        name=raw.get("name", ""),
        num_units=int(raw.get("num_units") or 0),
        style=int(raw.get("style") or 0),
        tier_current=int(raw.get("tier_current") or 0),
        tier_total=int(raw.get("tier_total") or 0),
    )


def _parse_participant(raw: dict) -> Participant:
    return Participant(
        puuid=raw.get("puuid", ""),
        placement=int(raw.get("placement") or 0),
        level=int(raw.get("level") or 0),
        gold_left=int(raw.get("gold_left") or 0),
        last_round=int(raw.get("last_round") or 0),
        units=tuple(_parse_unit(u) for u in raw.get("units", [])),
        traits=tuple(_parse_trait(t) for t in raw.get("traits", [])),
        augments=tuple(raw.get("augments") or []),
    )


def parse_match(raw: dict) -> Match:
    """Parse le JSON brut d'une partie en `Match` immuable."""
    info = raw.get("info", {})
    metadata = raw.get("metadata", {})
    participants = tuple(_parse_participant(p) for p in info.get("participants", []))
    return Match(
        match_id=metadata.get("match_id", ""),
        set_number=int(info.get("tft_set_number") or 0),
        game_version=info.get("game_version", ""),
        queue_id=int(info.get("queue_id") or 0),
        participants=participants,
    )
