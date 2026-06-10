"""Tests du Realm of the Gods : 9 dieux, God Boons réels, flux vote -> dieu aligné."""

from __future__ import annotations

import numpy as np

from tft_goat.data.content import load_set
from tft_goat.data.gods import (
    SET17_GODS,
    aligned_god,
    choose_lobby_gods,
    god_boons,
)


def test_nine_gods_each_have_real_boons():
    """Les 9 dieux Set 17 ont chacun >= 1 God Boon réel ; 17 god augments au total (CDragon)."""
    sc = load_set()
    boons = god_boons(sc)
    assert set(boons) == set(SET17_GODS)
    assert len(SET17_GODS) == 9
    for god, apis in boons.items():
        assert apis, f"{god} n'a aucun God Boon dans la data"
        assert all(sc.augments[a].tier == "god" for a in apis)
    assert sum(len(v) for v in boons.values()) == 17  # vérifié vs cdragon_17.4


def test_choose_lobby_gods_returns_two_distinct():
    rng = np.random.default_rng(0)
    a, b = choose_lobby_gods(rng)
    assert a != b
    assert a in SET17_GODS and b in SET17_GODS


def test_aligned_god_majority_and_tiebreak():
    assert aligned_god({}) is None
    assert aligned_god({"Ahri": 0}) is None
    assert aligned_god({"Ahri": 2, "Kayle": 1}) == "Ahri"  # majorité 2-1
    # égalité -> départage stable par l'ordre des dieux (Soraka avant Yasuo dans SET17_GODS)
    assert aligned_god({"Yasuo": 1, "Soraka": 1}) == "Soraka"


def test_vote_flow_sets_aligned_god_and_boon_at_4_4():
    """Bout en bout : 3 votes (2-4/3-4/4-4) -> dieu aligné majoritaire + boon réel posé."""
    from tft_goat.env.actions import _record_god_vote
    from tft_goat.env.rounds import PVE_OPENING, ROUNDS_PER_STAGE
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    rng = np.random.default_rng(1)
    p = PlayerState(agent_id="p0")
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc, rng=rng,
        lobby_gods=("Ahri", "Kayle"),
    )

    def god_round_index(stage: int) -> int:
        return PVE_OPENING + (stage - 2) * ROUNDS_PER_STAGE + 3  # x-4

    # 2-4 et 3-4 : vote pour Ahri (idx 0 -> lobby_gods[0]) ; pas encore d'alignement
    for stage in (2, 3):
        state.round_index = god_round_index(stage)
        p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
        _record_god_vote(state, p, 0)
        assert p.aligned_god is None

    # 4-4 : 3e vote pour Ahri -> majorité 3-0 -> aligné Ahri + boon Ahri réel
    state.round_index = god_round_index(4)
    p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
    _record_god_vote(state, p, 0)
    assert p.god_votes["Ahri"] == 3
    assert p.aligned_god == "Ahri"
    assert p.god_boon is not None
    assert "Ahri" in p.god_boon and sc.augments[p.god_boon].tier == "god"


def test_offer_gods_alternates_lobby_gods_via_start_round():
    """start_round peuple god_offer_gods depuis les 2 dieux du lobby, en alternance [A, B, A]."""
    from tft_goat.env.rounds import PVE_OPENING, start_round
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    p = PlayerState(agent_id="p0", gold=10, level=5)
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(3), lobby_gods=("Ahri", "Kayle"),
        round_index=PVE_OPENING + 3,  # 2-4 : premier round de dieu
    )
    start_round(state)
    assert p.god_offer_gods == ["Ahri", "Kayle", "Ahri"]  # alternance des 2 dieux du lobby
    assert set(p.god_offer_gods) == {"Ahri", "Kayle"}  # les 2 dieux representes
    assert len(p.god_offer) == 3  # 3 champions offerts en face des 3 votes


def test_split_vote_majority_end_to_end():
    """Vote partagé 2-1 à travers start_round + _record_god_vote -> majorité alignée au 4-4."""
    from tft_goat.env.actions import _record_god_vote
    from tft_goat.env.rounds import PVE_OPENING, ROUNDS_PER_STAGE, start_round
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    p = PlayerState(agent_id="p0", gold=10, level=5)
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(4), lobby_gods=("Ahri", "Kayle"),
    )
    # stage 2 : idx 0 -> Ahri ; stages 3 et 4 : idx 1 -> Kayle (offre réelle via start_round)
    for stage, idx in ((2, 0), (3, 1), (4, 1)):
        state.round_index = PVE_OPENING + (stage - 2) * ROUNDS_PER_STAGE + 3  # x-4
        start_round(state)
        _record_god_vote(state, p, idx)
    assert p.god_votes == {"Ahri": 1, "Kayle": 2}
    assert p.aligned_god == "Kayle"  # majorité 2-1
    assert p.god_boon is not None and "Kayle" in p.god_boon
    assert sc.augments[p.god_boon].tier == "god"


def test_illegal_action_during_god_offer_is_coerced_to_pick_not_pass():
    """Régression : une action illégale pendant une offre forcée ne doit JAMAIS devenir PASS.

    Avant le fix, tft_env coerçait toute action illégale vers PASS même quand mask[PASS]=False
    (offre de dieu en cours) -> le vote sautait silencieusement.
    """
    from tft_goat.env.rounds import PVE_OPENING, start_round
    from tft_goat.env.tft_env import TftEnv

    env = TftEnv()
    env.reset(seed=7)
    state = env._state
    state.round_index = PVE_OPENING + 3  # 2-4 : round de dieu
    start_round(state)
    for p in state.players.values():
        assert p.god_offer and p.god_offer_gods  # offre forcée en place

    # chaque agent envoie PASS (illégal pendant l'offre) -> doit être coercé vers un pick
    env.step({a: 0 for a in env.agents})
    for p in state.players.values():
        assert not p.god_offer_gods  # le vote a bien eu lieu (offre consommée)
        assert sum(p.god_votes.values()) == 1
        assert not p.passed  # pas de PASS fantôme


def test_stale_god_offer_is_purged_at_next_round():
    """Régression : une offre de dieu non consommée ne fuit pas vers le round suivant."""
    from tft_goat.env.rounds import PVE_OPENING, start_round
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    p = PlayerState(agent_id="p0", gold=10, level=5)
    p.god_offer = ["TFT17_Ahri", "TFT17_Kayle", "TFT17_Yasuo"]  # offre périmée (round raté)
    p.god_offer_gods = ["Ahri", "Kayle", "Ahri"]
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(5), lobby_gods=("Ahri", "Kayle"),
        round_index=PVE_OPENING + 4,  # 2-5 : PAS un round de dieu
    )
    start_round(state)
    assert p.god_offer == [] and p.god_offer_gods == []  # purgée, pas de vote fantôme


def test_god_offer_only_contains_playable_pool_units():
    """Régression : l'offre des dieux est tirée du roster jouable du pool (jamais de PvE).

    Avant le fix, _sample_gods tirait dans content.champions non filtré : TFT_BlueGolem &co
    (cost 1-5 dans setData) pouvaient être offerts, puis pool.take() échouait silencieusement.
    """
    from tft_goat.env.rounds import _sample_gods
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    pool = Pool(sc)
    state = GameState(
        players={"p0": PlayerState(agent_id="p0")}, pool=pool, set_content=sc,
        rng=np.random.default_rng(8), lobby_gods=("Ahri", "Kayle"),
    )
    for _ in range(50):
        for champ in _sample_gods(state):
            assert pool.remaining(champ) > 0, f"{champ} offert mais absent du pool jouable"


def test_missed_final_vote_still_aligns_at_4_7():
    """Filet : 2 votes seulement (3e manqué) -> l'alignement est résolu au 4-7 et le boon délivré."""
    from tft_goat.env.rounds import PVE_OPENING, ROUNDS_PER_STAGE, start_round
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    p = PlayerState(agent_id="p0", gold=10, level=5)
    p.god_votes = {"Ahri": 2}  # 2 votes exprimés, jamais alignés
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(6), lobby_gods=("Ahri", "Kayle"),
        round_index=PVE_OPENING + (4 - 2) * ROUNDS_PER_STAGE + 6,  # 4-7
    )
    start_round(state)
    assert p.aligned_god == "Ahri"
    assert p.god_boon is not None and "Ahri" in p.god_boon
    assert p.god_boon in p.chosen_augments  # boon bien délivré dans la foulée


def test_god_boon_round_is_only_4_7():
    from tft_goat.env.rounds import (
        PVE_OPENING,
        ROUNDS_PER_STAGE,
        is_god_boon_round,
    )

    def idx(stage: int, rnd: int) -> int:
        return PVE_OPENING + (stage - 2) * ROUNDS_PER_STAGE + (rnd - 1)

    assert is_god_boon_round(idx(4, 7))  # 4-7
    for s, r in [(4, 4), (4, 6), (3, 7), (5, 7), (2, 7)]:
        assert not is_god_boon_round(idx(s, r))


def test_god_boon_delivered_to_augments_at_4_7():
    """Au 4-7, le God Boon réel du dieu aligné entre dans le pipeline d'augments du combat."""
    from tft_goat.env.rounds import (
        PVE_OPENING,
        ROUNDS_PER_STAGE,
        start_round,
    )
    from tft_goat.env.shop import Pool
    from tft_goat.env.state import GameState, PlayerState

    sc = load_set()
    p = PlayerState(agent_id="p0", gold=10, level=5)
    boon = god_boons(sc)["Kayle"][0]
    p.aligned_god = "Kayle"
    p.god_boon = boon
    state = GameState(
        players={"p0": p}, pool=Pool(sc), set_content=sc,
        rng=np.random.default_rng(2), lobby_gods=("Ahri", "Kayle"),
        round_index=PVE_OPENING + (4 - 2) * ROUNDS_PER_STAGE + 6,  # 4-7
    )
    assert boon not in p.chosen_augments
    start_round(state)
    assert boon in p.chosen_augments  # délivré
    # idempotent : un second start_round (même round) ne le duplique pas
    start_round(state)
    assert p.chosen_augments.count(boon) == 1
