"""Edge cases : moteur (boards vides, intargetable, pool) + env (partie reelle, invariants)."""

from __future__ import annotations

import numpy as np

from tft_goat.data.content import load_set
from tft_goat.data.sample import build_sample_content
from tft_goat.engine.resolver import EngineResolver
from tft_goat.engine.simulate import CombatContext, run_combat
from tft_goat.engine.unit import build_unit
from tft_goat.env.economy import BENCH_CAP
from tft_goat.env.state import BoardUnit
from tft_goat.env.tft_env import TftEnv


def test_engine_empty_boards():
    c = build_sample_content()
    rng = np.random.default_rng(0)
    assert run_combat([], [], c, rng).winner == 0  # double vide -> pas de crash
    assert run_combat([], [BoardUnit("c1", 1)], c, rng).winner == 1
    assert run_combat([BoardUnit("c1", 1)], [], c, rng).winner == 0


def test_engine_all_untargetable_terminates():
    c = load_set()
    rng = np.random.default_rng(0)
    a = build_unit(c.champions["TFT17_Shen"], 2, 0, c)
    b = build_unit(c.champions["TFT17_Shen"], 2, 1, c)
    ctx = CombatContext([a, b], rng)
    ctx.make_untargetable(b, 999.0)  # b intargetable -> a n'a pas de cible
    assert ctx.target_of(a) is None  # ne plante pas, pas de cible


def test_engine_combat_terminates_on_real_content():
    """Combat moteur entre 2 vrais boards pleins se termine (garde de ticks)."""
    c = load_set()
    champs = [a for a in c.champions if a.startswith("TFT17_")][:8]
    A = [BoardUnit(champs[i], 2) for i in range(4)]
    B = [BoardUnit(champs[i + 4], 2) for i in range(4)]
    res = run_combat(A, B, c, np.random.default_rng(0))
    assert res.winner in (0, 1)
    assert res.survivors >= 0


def test_full_real_game_invariants():
    """Une partie complete sur le VRAI Set 17 (moteur) respecte les invariants."""
    env = TftEnv(set_content=load_set(), resolver=EngineResolver())
    obs, infos = env.reset(seed=0)
    rng = np.random.default_rng(0)
    steps = 0
    while env.agents and steps < 30000:
        acts = {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
        obs, r, t, tr, infos = env.step(acts)
        for p in env._state.players.values():
            assert p.gold >= 0
            assert len(p.board) <= p.board_cap
            assert len(p.bench) <= BENCH_CAP
        steps += 1
    assert env.agents == []
    assert sorted(p.placement for p in env._state.players.values()) == list(range(1, 9))


def test_pool_conserved_with_eliminations():
    """Pool conserve meme apres eliminations (unites des morts rendues au pool)."""
    from tft_goat.data.odds import pool_size

    content = build_sample_content()
    env = TftEnv(set_content=content)
    obs, infos = env.reset(seed=1)
    rng = np.random.default_rng(1)
    while env.agents:
        acts = {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
        obs, r, t, tr, infos = env.step(acts)
    state = env._state
    in_play = sum(u.copies for p in state.players.values() for u in p.all_units())
    initial = sum(pool_size(c.cost) for c in content.champions.values() if 1 <= c.cost <= 5)
    assert state.pool.total_remaining() + in_play == initial
