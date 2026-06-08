"""Tests de l'adversaire scripté et de l'éval vs opponents."""

from __future__ import annotations

import numpy as np

from tft_goat.agent.scripted import scripted_action
from tft_goat.env.actions import legal_mask
from tft_goat.env.tft_env import TftEnv


def test_scripted_action_always_legal(sample_content):
    env = TftEnv(set_content=sample_content)
    obs, infos = env.reset(seed=0)
    rng = np.random.default_rng(0)
    steps = 0
    while env.agents and steps < 20000:
        acts = {}
        for a in env.agents:
            act = scripted_action(env._state, env._state.players[a])
            assert legal_mask(env._state, env._state.players[a])[act]  # toujours legal
            acts[a] = act
        obs, r, t, tr, infos = env.step(acts)
        steps += 1
    # partie scripté-vs-scripté se termine proprement
    assert env.agents == []
    assert sorted(p.placement for p in env._state.players.values()) == list(range(1, 9))


def test_scripted_beats_random(sample_content):
    """1 siège scripté vs 7 aléatoires : placement moyen nettement < 4.5."""
    env = TftEnv(set_content=sample_content)
    seat = "player_0"
    places = []
    for g in range(20):
        rng = np.random.default_rng(g)
        obs, infos = env.reset(seed=g)
        while env.agents:
            acts = {}
            for a in env.agents:
                if a == seat:
                    acts[a] = scripted_action(env._state, env._state.players[a])
                else:
                    acts[a] = int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
            obs, r, t, tr, infos = env.step(acts)
        places.append(env._state.players[seat].placement)
    assert float(np.mean(places)) < 3.8  # bat clairement le random (4.5)


def test_eval_vs_opponents_runs(sample_content):
    from tft_goat.agent.evaluate import eval_vs_opponents
    from tft_goat.env.encoding import Encoder
    from tft_goat.agent.network import ActorCritic
    import torch

    torch.manual_seed(0)
    env = TftEnv(set_content=sample_content)
    enc = Encoder(sample_content)
    policy = ActorCritic(enc.n_champ, enc.n_trait, embed_dim=8, hidden_dim=32)
    res = eval_vs_opponents(policy, env, "scripted", n_games=3)
    assert 1.0 <= res["mean_placement"] <= 8.0
