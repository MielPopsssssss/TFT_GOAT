"""Tests du combat heuristique et de l'interface CombatResolver."""

from __future__ import annotations

import numpy as np

from tft_goat.env.combat import CombatResult, HeuristicResolver, board_strength
from tft_goat.env.state import BoardUnit


def test_board_strength_scales_with_star(sample_content):
    one = [BoardUnit("c7", 1)]  # 4-cost 1-star
    three = [BoardUnit("c7", 3)]  # 4-cost 3-star
    assert board_strength(three, sample_content) > board_strength(one, sample_content)


def test_stronger_board_wins_majority(sample_content):
    rng = np.random.default_rng(7)
    strong = [BoardUnit("c7", 3), BoardUnit("c8", 2), BoardUnit("c5", 2)]
    weak = [BoardUnit("c1", 1)]
    resolver = HeuristicResolver()
    wins_a = sum(
        resolver.resolve(strong, weak, sample_content, rng).winner == 0
        for _ in range(200)
    )
    assert wins_a > 170  # board nettement plus fort gagne >85%


def test_empty_vs_nonempty(sample_content):
    rng = np.random.default_rng(1)
    res = HeuristicResolver().resolve([], [BoardUnit("c1", 1)], sample_content, rng)
    assert res.winner == 1


def test_datatft_meta_coherently_affects_board_strength():
    """Cohérence sim : à coût/étoile égaux, une unité méta-forte (datatft) donne plus de force.

    Valide que l'ancrage datatft est réellement câblé dans board_strength (pas décoratif).
    Jhin (avg_place ~3.95, top) vs Zed (~4.31), deux 5-cost : board(Jhin) > board(Zed).
    """
    from tft_goat.data.content import load_set
    from tft_goat.data.datatft import load_meta_stats

    sc = load_set()
    meta = load_meta_stats()
    jhin = [BoardUnit("TFT17_Jhin", 2)]
    zed = [BoardUnit("TFT17_Zed", 2)]
    # sanity : Jhin est bien méta-supérieur dans la data
    assert meta.unit_power("TFT17_Jhin") > meta.unit_power("TFT17_Zed")
    assert board_strength(jhin, sc, meta) > board_strength(zed, sc, meta)
    # sans meta_stats, les deux 5-cost 2★ sont équivalents (cost×star seul)
    assert board_strength(jhin, sc, None) == board_strength(zed, sc, None)


def test_survivors_bounded_by_winning_board_with_variance(sample_content):
    """Survivants (→ dégâts joueur) bornés [1, taille board] et VARIÉS selon la marge du matchup.

    survivors = round(board × marge) : déterministe pour un matchup donné, mais varie d'un
    adversaire à l'autre (marge écrasante → bcp de survivants ; serré → 1). Vérifié en partie :
    distribution 1→7, moyenne ~1.7. Garde-fou de la formule de dégâts.
    """
    rng = np.random.default_rng(0)
    win_board = [BoardUnit("c7", 3), BoardUnit("c8", 2), BoardUnit("c5", 2)]
    opponents = [  # adversaires de force croissante => marge décroissante
        [BoardUnit("c1", 1)],
        [BoardUnit("c1", 2), BoardUnit("c4", 1)],
        [BoardUnit("c7", 2), BoardUnit("c8", 1), BoardUnit("c5", 1)],
    ]
    seen = set()
    for opp in opponents:
        for _ in range(50):
            res = HeuristicResolver().resolve(win_board, opp, sample_content, rng)
            if res.winner == 0:
                assert 1 <= res.survivors <= len(win_board)
                seen.add(res.survivors)
    assert len(seen) >= 2, f"survivants sans variance entre matchups: {seen}"


def test_resolver_substitution(sample_content):
    """Un resolver factice deterministe satisfait l'interface (couture etape 4)."""

    class AlwaysB:
        def resolve(self, board_a, board_b, set_content, rng):
            return CombatResult(winner=1, survivors=2)

    res = AlwaysB().resolve([BoardUnit("c8", 3)], [], sample_content, None)
    assert res.winner == 1 and res.survivors == 2


def test_augment_power_counts_only_combat_augments():
    """`augment_power` : seuls les augments à effet COMBAT (registre moteur) boostent.

    Les augments éco/utilitaires payent déjà leur valeur via l'économie de l'env —
    les compter ici serait du double-comptage (investigation 2026-06-10, backlog
    « Décider du sort du God Boon hors moteur réel »)."""
    from tft_goat.data.content import load_set
    from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
    from tft_goat.env.combat import augment_power

    c = load_set()
    god = "TFT17_Augment_SorakaGodAugment"  # God Boon câblé au moteur
    assert god in AUGMENT_REGISTRY
    assert augment_power((god,), c) > 1.0
    eco = next(api for api, a in sorted(c.augments.items())
               if a.tier == "gold" and api not in AUGMENT_REGISTRY)
    assert augment_power((eco,), c) == 1.0
    assert augment_power((), c) == 1.0
    # cumul : god + un augment combat régulier > god seul
    reg = next(api for api in sorted(AUGMENT_REGISTRY)
               if api in c.augments and c.augments[api].tier != "god")
    assert augment_power((god, reg), c) > augment_power((god,), c)


def test_heuristic_resolver_favors_god_boon_side():
    """Boards identiques, un côté a un God Boon -> il gagne > 50% des résolutions."""
    from tft_goat.data.content import load_set
    from tft_goat.env.combat import HeuristicResolver

    c = load_set()
    board = [BoardUnit("TFT17_Aatrox", 2, on_board=True),
             BoardUnit("TFT17_Graves", 2, on_board=True)]
    resolver = HeuristicResolver()
    rng = np.random.default_rng(0)
    god = ("TFT17_Augment_SorakaGodAugment",)
    n = 4000
    wins = sum(
        resolver.resolve(board, board, c, rng, augments_a=god).winner == 0
        for _ in range(n)
    )
    assert wins / n > 0.51  # le boon pèse dans la proba (0.5 sans lui)
