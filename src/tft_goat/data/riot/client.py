"""Clients riotwatcher (cle via environnement).

On ne reecrit pas de client HTTP Riot : riotwatcher gere le header X-Riot-Token, le
rate-limiting et la deserialisation. `RiotWatcher` porte account-v1 (lookup PUUID),
`TftWatcher` porte tft-match-v1.
"""

from __future__ import annotations

from functools import lru_cache

from riotwatcher import RiotWatcher, TftWatcher

from ...config import riot_api_key


@lru_cache(maxsize=1)
def tft_watcher() -> TftWatcher:
    """Client TFT (match-v1, league, summoner). Cle lue depuis RIOT_API_KEY."""
    return TftWatcher(riot_api_key())


@lru_cache(maxsize=1)
def riot_watcher() -> RiotWatcher:
    """Client Riot generique (account-v1 : lookup PUUID par Riot ID)."""
    return RiotWatcher(riot_api_key())
