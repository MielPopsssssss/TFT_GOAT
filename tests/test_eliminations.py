"""Équité des départages d'élimination (enquête sièges, 2026-06-10).

Bug : `assign_eliminations` triait les morts simultanées par HP avec un tri STABLE ->
à HP exactement égaux, l'ordre du dict (player_0..7) attribuait déterministiquement la
PIRE place au siège le plus bas. Même classe de bug dans `_truncate_by_hp` (sens inverse).
L'égalité exacte de HP est un artefact du modèle discret (le vrai TFT résout en temps réel,
jamais d'ex æquo parfait — cf. skill tft-knowledge, game-flow) : pas de règle officielle ->
départage ALÉATOIRE UNIFORME via state.rng, zéro biais de siège.
"""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.data.content import load_set
from tft_goat.env.rounds import assign_eliminations
from tft_goat.env.shop import Pool
from tft_goat.env.state import GameState, PlayerState
from tft_goat.env.tft_env import TftEnv


@pytest.fixture(scope="module")
def sc():
    return load_set()


def _players(hps: list[int]) -> dict[str, PlayerState]:
    players = {}
    for i, hp in enumerate(hps):
        p = PlayerState(agent_id=f"player_{i}")
        p.hp = hp
        players[f"player_{i}"] = p
    return players


def test_simultaneous_equal_hp_deaths_are_not_seat_biased(sc):
    """À HP égaux, le départage des morts simultanées ne doit PAS être déterministe."""
    outcomes = set()
    for seed in range(30):
        players = _players([-3, 50, -3, 50])  # p0 et p2 morts, HP identiques
        state = GameState(
            players=players, pool=Pool(sc), set_content=sc,
            rng=np.random.default_rng(seed), lobby_gods=("Ahri", "Kayle"),
        )
        assign_eliminations(state)
        assert {players["player_0"].placement, players["player_2"].placement} == {3, 4}
        outcomes.add(players["player_0"].placement)
    # sur 30 seeds, les DEUX ordres doivent apparaître (sinon départage déterministe biaisé)
    assert outcomes == {3, 4}, f"départage toujours identique : {outcomes}"


def test_lower_hp_still_dies_first_when_not_tied(sc):
    """La règle réelle reste intacte : HP plus bas = mort « en premier » = pire place."""
    for seed in range(5):
        players = _players([-10, 50, -2, 50])  # p0 plus bas que p2
        state = GameState(
            players=players, pool=Pool(sc), set_content=sc,
            rng=np.random.default_rng(seed), lobby_gods=("Ahri", "Kayle"),
        )
        assign_eliminations(state)
        assert players["player_0"].placement == 4  # toujours pire que p2
        assert players["player_2"].placement == 3


def test_truncate_by_hp_equal_ties_are_not_seat_biased(sc):
    """Fin forcée à MAX_ROUNDS : HP égaux -> ordre non déterministe ; HP réels respectés."""
    env = TftEnv(set_content=sc)
    outcomes = set()
    for seed in range(30):
        players = _players([40, 40, 40])  # égalité parfaite à 3
        state = GameState(
            players=players, pool=Pool(sc), set_content=sc,
            rng=np.random.default_rng(seed), lobby_gods=("Ahri", "Kayle"),
        )
        env._truncate_by_hp(state)
        assert sorted(p.placement for p in players.values()) == [1, 2, 3]
        outcomes.add(players["player_0"].placement)
    assert len(outcomes) > 1, f"départage toujours identique : {outcomes}"

    # et sans égalité, le classement par HP décroissant reste exact
    players = _players([80, 40, 60])
    state = GameState(
        players=players, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(0), lobby_gods=("Ahri", "Kayle"),
    )
    env._truncate_by_hp(state)
    assert players["player_0"].placement == 1
    assert players["player_2"].placement == 2
    assert players["player_1"].placement == 3
