"""Tests du combat surrogate : featurize, net, dataset, distillation, riot pairs, swap env."""

from __future__ import annotations

import json

import numpy as np
import pytest
import torch

from tft_goat.config import FIXTURES_DIR
from tft_goat.data.riot.match import parse_match
from tft_goat.env.encoding import Encoder
from tft_goat.env.state import BoardUnit
from tft_goat.env.tft_env import TftEnv
from tft_goat.surrogate.dataset import (
    make_bootstrap_dataset,
    pairs_from_matches,
    sample_board,
)
from tft_goat.surrogate.featurize import MAX_UNITS, batch_boards, encode_board
from tft_goat.surrogate.net import CombatNet
from tft_goat.surrogate.resolver import NeuralResolver


@pytest.fixture()
def encoder(sample_content):
    return Encoder(sample_content)


@pytest.fixture()
def net(encoder):
    torch.manual_seed(0)
    return CombatNet(encoder.n_champ, encoder.n_trait)


def test_encode_board_shapes(encoder):
    feat = encode_board([BoardUnit("c1", 2), BoardUnit("c7", 1)], encoder)
    assert feat["champ_idx"].shape == (MAX_UNITS,)
    assert feat["star"].shape == (MAX_UNITS,)
    assert feat["trait_vec"].shape == (encoder.n_trait,)


def test_net_win_prob_range(encoder, net):
    a = batch_boards([[BoardUnit("c7", 2)]], encoder)
    b = batch_boards([[BoardUnit("c1", 1)]], encoder)
    p = net.win_prob(a, b)
    assert p.shape == (1,)
    assert 0.0 <= float(p.item()) <= 1.0


def test_bootstrap_dataset(sample_content):
    rng = np.random.default_rng(0)
    a, b, y = make_bootstrap_dataset(sample_content, None, 100, rng)
    assert len(a) == len(b) == len(y) == 100
    assert y.min() >= 0.0 and y.max() <= 1.0


def test_engine_dataset(sample_content):
    from tft_goat.surrogate.dataset import make_engine_dataset

    rng = np.random.default_rng(0)
    a, b, y = make_engine_dataset(sample_content, 30, rng, samples=1)
    assert len(a) == len(b) == len(y) == 30
    assert set(np.unique(y)).issubset({0.0, 1.0})  # label binaire (verite terrain moteur)


def test_distillation_learns_heuristic(sample_content, encoder):
    """Apres un court entrainement, le reseau predit le vainqueur de l'heuristique > 80%."""
    rng = np.random.default_rng(1)
    a, b, y = make_bootstrap_dataset(sample_content, None, 6000, rng)
    fa, fb = batch_boards(a, encoder), batch_boards(b, encoder)
    yt = torch.as_tensor(y)
    torch.manual_seed(0)
    net = CombatNet(encoder.n_champ, encoder.n_trait)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    for _ in range(20):
        opt.zero_grad()
        loss = loss_fn(net.logit(fa, fb), yt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = (net.win_prob(fa, fb) > 0.5).float()
        target = (yt > 0.5).float()
        acc = float((pred == target).float().mean())
    assert acc > 0.8


def test_pairs_from_matches_labels():
    raw = json.loads((FIXTURES_DIR / "match_sample.json").read_text())
    match = parse_match(raw)
    a, b, y = pairs_from_matches([match])
    assert len(y) == 28  # C(8,2), placements 1..8 distincts
    assert set(np.unique(y)).issubset({0.0, 1.0})
    # 1er participant (placement 1) vs 2e (placement 2) -> label 1
    assert y[0] == 1.0


def test_neural_resolver_in_env(sample_content, encoder, net):
    """NeuralResolver enfiche dans l'env -> partie complete (couture, reseau reel)."""
    resolver = NeuralResolver(net, encoder)
    env = TftEnv(set_content=sample_content, resolver=resolver)
    obs, infos = env.reset(seed=0)
    rng = np.random.default_rng(0)
    steps = 0
    while env.agents and steps < 20000:
        acts = {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
        obs, r, t, tr, infos = env.step(acts)
        steps += 1
    assert env.agents == []
    placements = sorted(p.placement for p in env._state.players.values())
    assert placements == list(range(1, 9))
