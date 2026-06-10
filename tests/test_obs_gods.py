"""Tests de l'encodage des dieux dans l'observation (l'agent doit VOIR pour qui il vote).

Avant ce changement, l'observation n'encodait AUCUNE info dieu : l'agent votait à l'aveugle
(choix = bruit). Vecteur `gods` (31 dims) : lobby (9 one-hot), slots d'offre (3 : 0=vide,
1=dieu A du lobby, 2=dieu B), votes par dieu (9, /3), dieu aligné (9 one-hot), boon (1).
"""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.data.content import load_set
from tft_goat.data.gods import SET17_GODS
from tft_goat.env.encoding import GOD_FEATS, Encoder
from tft_goat.env.shop import Pool
from tft_goat.env.state import GameState, PlayerState

GOD_ORDER = tuple(SET17_GODS)


@pytest.fixture(scope="module")
def sc():
    return load_set()


def _state(sc, p, **kw):
    return GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(0), lobby_gods=("Ahri", "Kayle"), **kw,
    )


def test_observation_space_has_gods_vector(sc):
    enc = Encoder(sc)
    space = enc.observation_space()
    assert "gods" in space.spaces
    assert space.spaces["gods"].shape == (GOD_FEATS,)
    assert GOD_FEATS == 31  # 9 lobby + 3 slots + 9 votes + 9 aligné + 1 boon


def test_gods_vector_encodes_lobby_offer_votes_alignment(sc):
    enc = Encoder(sc)
    p = PlayerState(agent_id="p0")
    p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
    p.god_votes = {"Ahri": 2, "Kayle": 1}
    p.aligned_god = "Ahri"
    p.god_boon = "TFT17_Augment_AhriGodAugment"
    state = _state(sc, p)

    g = enc.encode(state, "p0")["gods"]
    ia, ik = GOD_ORDER.index("Ahri"), GOD_ORDER.index("Kayle")
    lobby, slots, votes, aligned, boon = g[:9], g[9:12], g[12:21], g[21:30], g[30]
    # lobby : exactement Ahri et Kayle
    assert lobby[ia] == 1.0 and lobby[ik] == 1.0 and lobby.sum() == 2.0
    # slots d'offre : [A, B, A] -> [1, 2, 1]
    assert slots.tolist() == [1.0, 2.0, 1.0]
    # votes normalisés /3
    assert votes[ia] == pytest.approx(2 / 3) and votes[ik] == pytest.approx(1 / 3)
    assert votes.sum() == pytest.approx(1.0)
    # aligné : one-hot Ahri ; boon présent
    assert aligned[ia] == 1.0 and aligned.sum() == 1.0
    assert boon == 1.0


def test_gods_vector_is_zero_without_god_state(sc):
    enc = Encoder(sc)
    p = PlayerState(agent_id="p0")
    state = _state(sc, p)
    g = enc.encode(state, "p0")["gods"]
    assert g[9:].sum() == 0.0  # pas d'offre/votes/alignement/boon
    assert g[:9].sum() == 2.0  # le lobby, lui, est toujours visible


def test_gods_vector_stays_within_observation_space(sc):
    """Saturation des votes (3/3) : valeurs bornées, et le vecteur reste dans l'espace gym."""
    enc = Encoder(sc)
    p = PlayerState(agent_id="p0")
    p.god_votes = {"Ahri": 3}  # maximum possible (3 votes au total)
    p.aligned_god = "Ahri"
    p.god_boon = "TFT17_Augment_AhriGodAugment"
    p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
    state = _state(sc, p)
    obs = enc.encode(state, "p0")
    assert obs["gods"][12 + GOD_ORDER.index("Ahri")] == pytest.approx(1.0)  # 3/3, jamais > 1
    assert enc.observation_space()["gods"].contains(obs["gods"])


def test_network_forward_with_gods(sc):
    """Le réseau consomme le nouveau vecteur : forward OK, logits de la bonne taille."""
    import torch

    from tft_goat.agent.network import ActorCritic
    from tft_goat.agent.obs import batch_obs
    from tft_goat.env.actions import NUM_ACTIONS

    enc = Encoder(sc)
    p = PlayerState(agent_id="p0")
    p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
    state = _state(sc, p)
    obs = enc.encode(state, "p0")

    net = ActorCritic(n_champ=enc.n_champ, n_trait=enc.n_trait)
    batched = batch_obs([obs], device=torch.device("cpu"))
    mask = torch.ones((1, NUM_ACTIONS), dtype=torch.bool)
    logits, value = net.forward(batched, mask)
    assert logits.shape == (1, NUM_ACTIONS)
    assert value.shape[0] == 1
