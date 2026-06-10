"""Espace d'action factorise + masque de legalite + application des actions.

Layout (Discrete(35)) :
  0        PASS
  1        REROLL          (2 or)
  2        BUY_XP          (4 or)
  3..7     BUY_SHOP[0..4]
  8..16    SELL_BENCH[0..8]
  17..25   FIELD_BENCH[0..8]   (banc -> board si place)
  26..34   BENCH_BOARD[0..8]   (board -> banc si place au banc)

Simplification v0 : un achat exige une place au banc (pas d'achat « combine direct » banc
plein). La vente ne se fait que depuis le banc (bench d'abord une unite du board pour la vendre).
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from .economy import (
    AUGMENT_BONUS_RANGE,
    COMPONENTS_PER_ITEM,
    ITEMS_MAX,
    MAX_LEVEL,
    REROLL_COST,
    SHOP_SIZE,
    XP_BUY_COST,
    XP_PER_BUY,
    apply_xp,
    sell_value,
)
from .items import combine as combine_components
from .rounds import GOD_CHOICES, GOD_VOTE_STAGES, finalize_god_alignment
from .shop import roll_shop
from .state import BoardUnit, GameState, PlayerState

PASS = 0
REROLL = 1
BUY_XP = 2
BUY_SHOP_START = 3
SELL_BENCH_START = 8
FIELD_BENCH_START = 17
BENCH_BOARD_START = 26
EQUIP = 35
PICK_AUGMENT_START = 36
N_AUGMENT_CHOICES = 3
PICK_GOD_START = 39
N_GOD_CHOICES = GOD_CHOICES  # single-sourcé avec rounds.py (offre = 3 choix)
REROLL_AUGMENT = 42  # reroll de l'offre d'augment (vrai TFT) — change les 3 augments proposes
NUM_ACTIONS = 43

_BENCH_SLOTS = 9


# --- combine (star-up automatique) ----------------------------------------
def _try_combine_once(player: PlayerState) -> bool:
    groups: dict[tuple[str, int], list[tuple[str, BoardUnit]]] = defaultdict(list)
    for u in player.bench:
        groups[(u.champion_api, u.star)].append(("bench", u))
    for u in player.board:
        groups[(u.champion_api, u.star)].append(("board", u))
    for (champ, star), lst in groups.items():
        if star >= 3 or len(lst) < 3:
            continue
        chosen = lst[:3]
        was_on_board = any(loc == "board" for loc, _ in chosen)
        for loc, u in chosen:
            (player.board if loc == "board" else player.bench).remove(u)
        upgraded = BoardUnit(champ, star + 1, on_board=False)
        if was_on_board and len(player.board) < player.board_cap:
            upgraded.on_board = True
            player.board.append(upgraded)
        else:
            player.bench.append(upgraded)
        return True
    return False


def combine(player: PlayerState) -> None:
    while _try_combine_once(player):
        pass


# --- legalite --------------------------------------------------------------
def _champ_cost(state: GameState, champ: str) -> int:
    c = state.set_content.champions.get(champ)
    return c.cost if c else 0


def legal_mask(state: GameState, player: PlayerState) -> np.ndarray:
    mask = np.zeros(NUM_ACTIONS, dtype=bool)
    mask[PASS] = True
    if player.passed:
        return mask  # une fois passe, seul PASS reste legal ce round
    if player.augment_offer:
        # un augment est propose -> choix force avant toute autre action (+ reroll possible)
        mask[PASS] = False
        for i in range(min(N_AUGMENT_CHOICES, len(player.augment_offer))):
            mask[PICK_AUGMENT_START + i] = True
        mask[REROLL_AUGMENT] = player.gold >= REROLL_COST  # reroll d'augment = 2 gold
        return mask
    if player.god_offer:
        # Realm of the Gods : choix d'un champion force avant toute autre action
        mask[PASS] = False
        for i in range(min(N_GOD_CHOICES, len(player.god_offer))):
            mask[PICK_GOD_START + i] = True
        return mask
    mask[REROLL] = player.gold >= REROLL_COST
    mask[BUY_XP] = player.gold >= XP_BUY_COST and player.level < MAX_LEVEL
    bench_room = player.bench_has_room()
    for i in range(SHOP_SIZE):
        champ = player.shop[i]
        ok = (
            champ is not None
            and bench_room
            and player.gold >= _champ_cost(state, champ)
            and state.pool.remaining(champ) > 0
        )
        mask[BUY_SHOP_START + i] = ok
    for i in range(_BENCH_SLOTS):
        mask[SELL_BENCH_START + i] = i < len(player.bench)
        mask[FIELD_BENCH_START + i] = i < len(player.bench) and len(player.board) < player.board_cap
    for i in range(_BENCH_SLOTS):
        mask[BENCH_BOARD_START + i] = i < len(player.board) and player.bench_has_room()
    mask[EQUIP] = len(player.components) >= COMPONENTS_PER_ITEM and any(
        u.items < ITEMS_MAX for u in player.board
    )
    return mask


# --- application -----------------------------------------------------------
def apply_action(state: GameState, player: PlayerState, action: int) -> None:
    if action == PASS:
        player.passed = True
        return
    if action == REROLL:
        if player.gold >= REROLL_COST:
            player.gold -= REROLL_COST
            player.shop = roll_shop(player.level, state.pool, state.rng)
        return
    if action == BUY_XP:
        if player.gold >= XP_BUY_COST and player.level < MAX_LEVEL:
            player.gold -= XP_BUY_COST
            player.level, player.xp = apply_xp(player.level, player.xp, XP_PER_BUY)
        return
    if BUY_SHOP_START <= action < BUY_SHOP_START + SHOP_SIZE:
        _buy_shop(state, player, action - BUY_SHOP_START)
        return
    if SELL_BENCH_START <= action < SELL_BENCH_START + _BENCH_SLOTS:
        _sell_bench(state, player, action - SELL_BENCH_START)
        return
    if FIELD_BENCH_START <= action < FIELD_BENCH_START + _BENCH_SLOTS:
        _field_bench(player, action - FIELD_BENCH_START)
        return
    if BENCH_BOARD_START <= action < BENCH_BOARD_START + _BENCH_SLOTS:
        _bench_board(player, action - BENCH_BOARD_START)
        return
    if action == EQUIP:
        _equip(state, player)
        return
    if action == REROLL_AUGMENT:
        _reroll_augment(state, player)
        return
    if PICK_AUGMENT_START <= action < PICK_AUGMENT_START + N_AUGMENT_CHOICES:
        _pick_augment(state, player, action - PICK_AUGMENT_START)
        return
    if PICK_GOD_START <= action < PICK_GOD_START + N_GOD_CHOICES:
        _pick_god(state, player, action - PICK_GOD_START)
        return


def _buy_shop(state: GameState, player: PlayerState, slot: int) -> None:
    champ = player.shop[slot]
    if champ is None or not player.bench_has_room():
        return
    cost = _champ_cost(state, champ)
    if player.gold < cost or not state.pool.take(champ):
        return
    player.gold -= cost
    player.shop[slot] = None
    player.bench.append(BoardUnit(champ, 1, on_board=False))
    combine(player)


def _sell_bench(state: GameState, player: PlayerState, idx: int) -> None:
    if idx >= len(player.bench):
        return
    unit = player.bench.pop(idx)
    cost = _champ_cost(state, unit.champion_api)
    player.gold += sell_value(cost, unit.star)
    state.pool.give_back(unit.champion_api, unit.copies)


def _field_bench(player: PlayerState, idx: int) -> None:
    if idx >= len(player.bench) or len(player.board) >= player.board_cap:
        return
    unit = player.bench.pop(idx)
    unit.on_board = True
    player.board.append(unit)


def _bench_board(player: PlayerState, idx: int) -> None:
    if idx >= len(player.board) or not player.bench_has_room():
        return
    unit = player.board.pop(idx)
    unit.on_board = False
    player.bench.append(unit)


def _equip(state: GameState, player: PlayerState) -> None:
    """Combine les 2 premiers composants -> objet complet REEL (recette) sur l'unite de plus haut cout."""
    if len(player.components) < COMPONENTS_PER_ITEM:
        return
    candidates = [u for u in player.board if u.items < ITEMS_MAX]
    if not candidates:
        return
    item_api = combine_components(player.components[0], player.components[1], state.set_content)
    if item_api is None:  # paire sans recette (ne devrait pas arriver avec 2 composants valides)
        return
    target = max(candidates, key=lambda u: _champ_cost(state, u.champion_api))
    target.item_apis = tuple(target.item_apis) + (item_api,)
    target.items += 1
    del player.components[0:COMPONENTS_PER_ITEM]


# Le tier d'augment module la puissance (abstraction resolvers non-moteur) : un prismatic
# est nettement plus fort qu'un silver. (Le moteur, lui, applique l'effet reel via chosen_augments.)
_TIER_POWER = {"silver": 0.7, "gold": 1.0, "prismatic": 1.4}


def _reroll_augment(state: GameState, player: PlayerState) -> None:
    """Reroll l'offre d'augment pour 2 gold : 3 nouveaux augments (tirés selon les odds du round)."""
    if not player.augment_offer or player.gold < REROLL_COST:
        return
    from .rounds import sample_augments  # import local : evite tout cycle

    player.gold -= REROLL_COST
    player.augment_offer = sample_augments(state, player, state.round_index)


def _pick_augment(state: GameState, player: PlayerState, idx: int) -> None:
    if idx >= len(player.augment_offer):
        return
    chosen = player.augment_offer[idx]
    player.chosen_augments.append(chosen)  # identite reelle -> effet de combat applique
    lo, hi = AUGMENT_BONUS_RANGE
    aug = state.set_content.augments.get(chosen)
    mult = _TIER_POWER.get(aug.tier, 1.0) if aug else 1.0
    player.augment_power += float(state.rng.uniform(lo, hi)) * mult  # abstraction ponderee par tier
    player.augment_offer = []


def _record_god_vote(state: GameState, player: PlayerState, idx: int) -> None:
    """Minor Blessing = un vote pour le dieu lié au choix `idx`.

    Au round 4-4 (3e vote), la majorité fixe le **dieu aligné** et tire son **God Boon** réel
    (apiName d'un augment tier="god" du dieu — data CDragon). La consommation du boon en combat
    est une sous-étape suivante (le champ god_boon est posé avec la vraie data).
    """
    if idx >= len(player.god_offer_gods):
        return
    god = player.god_offer_gods[idx]
    player.god_votes[god] = player.god_votes.get(god, 0) + 1
    player.god_offer_gods = []
    # 3e et dernier vote -> alignement. Déclenché par le COMPTE de votes (pas le numéro de
    # round) : robuste même si un vote a lieu hors du chemin nominal 2-4/3-4/4-4.
    if sum(player.god_votes.values()) >= len(GOD_VOTE_STAGES):
        finalize_god_alignment(state, player)


def _pick_god(state: GameState, player: PlayerState, idx: int) -> None:
    """Realm of the Gods : Minor Blessing = vote pour un dieu + champion offert (banc, sinon board)."""
    _record_god_vote(state, player, idx)
    if idx >= len(player.god_offer):
        return
    champ = player.god_offer[idx]
    player.god_offer = []
    if not state.pool.take(champ):  # plus de copie dispo -> champion non octroye (conservation pool)
        return
    unit = BoardUnit(champ, 1, on_board=False)
    if player.bench_has_room():
        player.bench.append(unit)
    elif len(player.board) < player.board_cap:
        unit.on_board = True
        player.board.append(unit)
    else:  # ni banc ni board -> rendre la copie
        state.pool.give_back(champ)
        return
    combine(player)  # peut declencher un star-up
