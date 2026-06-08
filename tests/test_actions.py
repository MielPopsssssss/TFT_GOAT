"""Tests des actions : achat, vente, combine, deplacements, masque de legalite."""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.data.odds import pool_size
from tft_goat.env.actions import (
    BUY_SHOP_START,
    FIELD_BENCH_START,
    PASS,
    SELL_BENCH_START,
    apply_action,
    combine,
    legal_mask,
)
from tft_goat.env.shop import Pool
from tft_goat.env.state import BoardUnit, GameState, PlayerState


def make_state(sample_content, **player_kwargs) -> tuple[GameState, PlayerState]:
    pool = Pool(sample_content)
    player = PlayerState(agent_id="p0", **player_kwargs)
    state = GameState(
        players={"p0": player},
        pool=pool,
        set_content=sample_content,
        rng=np.random.default_rng(0),
    )
    return state, player


def test_buy_from_shop(sample_content):
    state, p = make_state(sample_content, gold=10)
    p.shop = ["c7", None, None, None, None]  # c7 = 4-cost
    apply_action(state, p, BUY_SHOP_START)
    assert p.gold == 6
    assert len(p.bench) == 1 and p.bench[0].champion_api == "c7"
    assert p.shop[0] is None
    assert state.pool.remaining("c7") == pool_size(4) - 1


def test_sell_returns_gold_and_pool(sample_content):
    state, p = make_state(sample_content, gold=0)
    state.pool.take("c7")  # simule un achat prealable
    p.bench = [BoardUnit("c7", 1)]
    apply_action(state, p, SELL_BENCH_START)
    assert p.gold == 4  # 4-cost 1-star
    assert state.pool.remaining("c7") == pool_size(4)  # copie rendue
    assert p.bench == []


def test_combine_three_to_two_star(sample_content):
    _, p = make_state(sample_content)
    p.bench = [BoardUnit("c1", 1), BoardUnit("c1", 1), BoardUnit("c1", 1)]
    combine(p)
    assert len(p.bench) == 1
    assert p.bench[0].star == 2


def test_combine_cascade_to_three_star(sample_content):
    _, p = make_state(sample_content)
    # 9 copies 1-star -> 3 deux-etoiles -> 1 trois-etoiles
    p.bench = [BoardUnit("c1", 1) for _ in range(9)]
    combine(p)
    stars = sorted(u.star for u in p.bench)
    assert stars == [3]


def test_field_unit_to_board(sample_content):
    _, p = make_state(sample_content, level=2)
    p.bench = [BoardUnit("c1", 1)]
    apply_action(state=GameState(players={"p0": p}, pool=Pool(sample_content),
                                 set_content=sample_content, rng=np.random.default_rng(0)),
                 player=p, action=FIELD_BENCH_START)
    assert len(p.board) == 1 and len(p.bench) == 0
    assert p.board[0].on_board is True


def test_field_blocked_when_board_full(sample_content):
    _, p = make_state(sample_content, level=1)
    p.board = [BoardUnit("c1", 1, on_board=True)]
    p.bench = [BoardUnit("c2", 1)]
    mask = legal_mask(
        GameState(players={"p0": p}, pool=Pool(sample_content),
                  set_content=sample_content, rng=np.random.default_rng(0)),
        p,
    )
    assert mask[FIELD_BENCH_START] == False  # board plein (cap = level = 1)


def test_pass_always_legal(sample_content):
    state, p = make_state(sample_content)
    assert legal_mask(state, p)[PASS] == True


def test_buy_xp_blocked_without_gold(sample_content):
    state, p = make_state(sample_content, gold=0)
    from tft_goat.env.actions import BUY_XP

    assert legal_mask(state, p)[BUY_XP] == False
