"""Smoke test de l'environnement : une partie complete en actions aleatoires legales.

Utilise le contenu synthetique (rapide, deterministe, CI-safe) et verifie les invariants.
"""

from __future__ import annotations

import numpy as np

from tft_goat.data.odds import pool_size
from tft_goat.env.combat import CombatResult
from tft_goat.env.economy import BENCH_CAP
from tft_goat.env.tft_env import TftEnv

MAX_SAFETY_STEPS = 20000


def _initial_pool_total(set_content) -> int:
    return sum(pool_size(c.cost) for c in set_content.champions.values() if 1 <= c.cost <= 5)


def _units_in_play(state) -> int:
    return sum(u.copies for p in state.players.values() for u in p.all_units())


def _play_random_game(env: TftEnv, seed: int):
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)
    steps = 0
    while env.agents and steps < MAX_SAFETY_STEPS:
        actions = {
            a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents
        }
        obs, rewards, terminations, truncations, infos = env.step(actions)
        # invariants a chaque step
        for p in env._state.players.values():
            assert p.gold >= 0
            assert len(p.board) <= p.board_cap
            assert len(p.bench) <= BENCH_CAP
        steps += 1
    return steps


def test_full_game_terminates_and_ranks(sample_content):
    env = TftEnv(set_content=sample_content)
    steps = _play_random_game(env, seed=0)
    assert env.agents == []  # tous termines
    assert steps < MAX_SAFETY_STEPS
    placements = sorted(p.placement for p in env._state.players.values())
    assert placements == list(range(1, 9))  # permutation 1..8, distincts


def test_pool_is_conserved(sample_content):
    env = TftEnv(set_content=sample_content)
    _play_random_game(env, seed=3)
    state = env._state
    total = state.pool.total_remaining() + _units_in_play(state)
    assert total == _initial_pool_total(sample_content)


def test_resolver_substitution_runs(sample_content):
    """L'env tourne avec un CombatResolver factice (prouve la couture etape 4)."""

    class FirstWins:
        def resolve(self, board_a, board_b, set_content, rng, augments_a=(), augments_b=()):
            return CombatResult(winner=0, survivors=1)

    env = TftEnv(set_content=sample_content, resolver=FirstWins())
    steps = _play_random_game(env, seed=1)
    assert env.agents == []
    assert steps < MAX_SAFETY_STEPS
