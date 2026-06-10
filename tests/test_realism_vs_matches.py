"""Smoke tests du benchmark realism_vs_matches (vérité terrain de fidélité).

Les scripts sont hors couverture par convention, mais celui-ci est LA métrique de
référence (baseline +0.44, cf. COMBAT_COVERAGE.md) : ses fonctions pures sont pinnées.
"""

from __future__ import annotations

import numpy as np
import pytest

from scripts.realism_vs_matches import board_of, predict_scores


@pytest.fixture(scope="module")
def rc():
    from tft_goat.data.content import load_set

    return load_set()


def test_board_of_filters_and_maps_real_units(rc):
    """character_id connu -> BoardUnit (star=tier, items réels) ; inconnus filtrés."""
    participant = {"units": [
        {"character_id": "TFT17_Aatrox", "tier": 2,
         "itemNames": ["TFT_Item_InfinityEdge", "PAS_UN_ITEM"]},
        {"character_id": "PAS_UN_CHAMPION", "tier": 3, "itemNames": []},
    ]}
    board = board_of(participant, rc)
    assert len(board) == 1
    u = board[0]
    assert u.champion_api == "TFT17_Aatrox" and u.star == 2
    assert u.item_apis == ("TFT_Item_InfinityEdge",)  # l'item inconnu est filtré
    assert u.items == 1


def test_predict_scores_round_robin_total_and_ordering(rc):
    """Round-robin : somme des scores == nb total de combats ; board vide ne gagne rien."""
    from tft_goat.env.state import BoardUnit

    strong = [BoardUnit("TFT17_Aatrox", 3, on_board=True),
              BoardUnit("TFT17_Graves", 3, on_board=True)]
    weak = [BoardUnit("TFT17_Aatrox", 1, on_board=True)]
    fights = 4
    scores = predict_scores([strong, weak], rc, np.random.default_rng(0), fights)
    assert sum(scores) == fights  # 1 paire x 4 combats, chaque combat a 1 gagnant
    assert scores[0] > scores[1]  # le board fort domine le board faible
