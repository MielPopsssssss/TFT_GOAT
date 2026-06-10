"""Tests du pool partage et du tirage de shop."""

from __future__ import annotations

import numpy as np

from tft_goat.data.odds import pool_size
from tft_goat.env.shop import Pool, roll_shop


def test_pool_init_counts(sample_content):
    pool = Pool(sample_content)
    # c1 est un 1-cost -> pool_size(1) copies
    assert pool.remaining("c1") == pool_size(1)
    assert pool.remaining("c8") == pool_size(5)


def test_take_and_give_back_conserves(sample_content):
    pool = Pool(sample_content)
    total0 = pool.total_remaining()
    assert pool.take("c1") is True
    assert pool.remaining("c1") == pool_size(1) - 1
    assert pool.total_remaining() == total0 - 1
    pool.give_back("c1")
    assert pool.total_remaining() == total0  # conservation


def test_take_depleted_returns_false(sample_content):
    pool = Pool(sample_content)
    for _ in range(pool_size(1)):
        assert pool.take("c1") is True
    assert pool.take("c1") is False


def test_roll_shop_respects_tiers_at_level_1(sample_content):
    pool = Pool(sample_content)
    rng = np.random.default_rng(42)
    # Niveau 1 : 100% 1-cost -> uniquement des 1-cost (c1, c2)
    for _ in range(20):
        slots = roll_shop(1, pool, rng)
        assert len(slots) == 5
        for s in slots:
            if s is not None:
                assert sample_content.champions[s].cost == 1


def test_roll_shop_only_available_units(sample_content):
    pool = Pool(sample_content)
    rng = np.random.default_rng(0)
    # vider tous les 1-cost
    for c in ("c1", "c2"):
        while pool.take(c):
            pass
    slots = roll_shop(1, pool, rng)
    # plus aucun 1-cost dispo -> tous les slots None au niveau 1
    assert all(s is None for s in slots)


def test_real_pool_roster_matches_verified_set17():
    """Le pool achetable = roster jouable Set 17 vérifié (15/13/13/14/10), PvE exclus.

    Vérifié 2026-06-08 : les unités PvE/evergreen (Golem, Rift Scuttler, Training Dummy)
    ont cost=1 dans setData mais ne sont PAS en boutique → exclues par le préfixe TFT17_.
    """
    from tft_goat.data.content import load_set

    pool = Pool(load_set())
    expected = {1: 15, 2: 13, 3: 13, 4: 14, 5: 10}
    for cost, n in expected.items():
        assert len(pool.champions_of_cost(cost)) == n, (
            f"{cost}-cost: {len(pool.champions_of_cost(cost))} != {n} attendu"
        )
    # aucune unité PvE/evergreen dans le pool
    for cost in range(1, 6):
        for api in pool.champions_of_cost(cost):
            assert api.startswith("TFT17_"), f"unité non-Set17 dans le pool: {api}"
    # nommément : ces PvE ne sont jamais achetables
    for pve in ("TFT_BlueGolem", "TFT9_SLIME_Crab", "TFT_TrainingDummy"):
        assert pool.remaining(pve) == 0
