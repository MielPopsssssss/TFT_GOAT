"""Tests de l'agent PPO : reseau, masquage, GAE, eval, smoke d'entrainement."""

from __future__ import annotations

import numpy as np
import pytest
import torch

from tft_goat.agent.config import PPOConfig
from tft_goat.agent.evaluate import eval_vs_random
from tft_goat.agent.network import ActorCritic
from tft_goat.agent.obs import batch_masks, batch_obs
from tft_goat.agent.ppo import ppo_update
from tft_goat.agent.rollout import collect_games, compute_gae
from tft_goat.env.actions import NUM_ACTIONS, PASS
from tft_goat.env.tft_env import TftEnv


@pytest.fixture()
def env(sample_content):
    return TftEnv(set_content=sample_content)


@pytest.fixture()
def policy(env):
    torch.manual_seed(0)
    return ActorCritic(n_champ=env.encoder.n_champ, n_trait=env.encoder.n_trait,
                       embed_dim=8, hidden_dim=32)


def test_network_forward_shapes(env, policy):
    obs, infos = env.reset(seed=0)
    agents = list(env.agents)
    b_obs = batch_obs([obs[a] for a in agents])
    b_mask = batch_masks([infos[a]["action_mask"] for a in agents])
    logits, value = policy.forward(b_obs, b_mask)
    assert logits.shape == (len(agents), NUM_ACTIONS)
    assert value.shape == (len(agents),)
    assert torch.isfinite(value).all()


def test_masking_never_samples_illegal(env, policy):
    obs, infos = env.reset(seed=0)
    a = env.agents[0]
    # masque artificiel : seul PASS est legal
    mask = np.zeros(NUM_ACTIONS, dtype=bool)
    mask[PASS] = True
    b_obs = batch_obs([obs[a]])
    b_mask = batch_masks([mask])
    for _ in range(50):
        action, _, _ = policy.act(b_obs, b_mask)
        assert int(action.item()) == PASS


def test_batch_obs_shapes(env):
    obs, _ = env.reset(seed=0)
    b = batch_obs([obs[a] for a in env.agents])
    assert b["scalars"].shape[0] == len(env.agents)
    assert b["board"].shape[1:] == (10, 3)


def test_compute_gae_toy():
    adv, ret = compute_gae([0.0, 0.0, 1.0], [0.0, 0.0, 0.0],
                           [False, False, True], gamma=1.0, lam=1.0)
    assert adv == pytest.approx([1.0, 1.0, 1.0])
    assert ret == pytest.approx([1.0, 1.0, 1.0])


def test_eval_runs(env, policy):
    res = eval_vs_random(policy, env, n_games=3)
    assert 1.0 <= res["mean_placement"] <= 8.0
    assert 0.0 <= res["win_rate"] <= 1.0


def test_smoke_train_changes_params(env, policy):
    cfg = PPOConfig(rollout_steps=300, minibatch_size=64, update_epochs=2)
    optim = torch.optim.Adam(policy.parameters(), lr=1e-3)
    before = policy.policy_head.weight.detach().clone()
    for _ in range(2):
        batch = collect_games(env, policy, cfg.rollout_steps, cfg.gamma, cfg.gae_lambda)
        metrics = ppo_update(policy, optim, batch, cfg)
        assert np.isfinite(metrics["policy_loss"])
        assert np.isfinite(metrics["value_loss"])
    after = policy.policy_head.weight.detach()
    assert not torch.allclose(before, after)  # apprentissage effectif
