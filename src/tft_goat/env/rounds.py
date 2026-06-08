"""Deroulement des rounds : schedule PvE/PvP, revenu, appariement, degats, eliminations.

Faithful-lite : 3 rounds PvE au depart (stage 1), puis PvP avec un round PvE periodique
(round minions). Carousel abstrait. Le combat lui-meme passe par le CombatResolver injecte.
"""

from __future__ import annotations

from .combat import CombatResolver
from .economy import ROUND_XP, apply_xp, round_income
from .items import components_and_recipes
from .shop import roll_shop
from .state import GameState, PlayerState

PVE_OPENING = 3  # STAGE 1 = 3 rounds PvE (1-1, 1-2, 1-3) — pas de PvP, comme le vrai TFT
ROUNDS_PER_STAGE = 7  # stages 2+ = 7 rounds chacun

# Vraie formule TFT : degats joueur = base_stage + 1 x (nb d'unites ennemies survivantes).
# Table de base reelle Set 17 (source TFT Ninja). Le par-unite est PLAT (1), pas pondere etoile.
STAGE_BASE_DAMAGE = {1: 0, 2: 2, 3: 5, 4: 8, 5: 10, 6: 12, 7: 17}

# Augments aux vrais rounds 2-1, 3-2, 4-2 (indices : 3, 3+7+1=11, 3+14+1=18).
AUGMENT_ROUNDS = {3, 11, 18}
N_AUGMENT_CHOICES = 3
# Reroll d'augment : chaque joueur recoit une offre aleatoire (differente par joueur) qu'il peut
# reroll. Le reroll COUTE 2 gold (= REROLL_COST), re-tire toute la ligne selon les odds du round.
MAX_AUGMENT_MITIGATION = 0.8  # plafond de reduction de degats cumulee

# Vraies probabilites de tier (Silver/Gold/Prismatic) par round d'augment (Set 17, patch 17.4).
# Chacun des 3 augments proposes est tire independamment selon ces odds (les tiers d'une meme
# ligne peuvent etre mixtes, comme dans le vrai TFT). Sources : metatft / tftodds augment-distributions.
AUGMENT_TIER_ODDS = {
    3:  {"silver": 0.28, "gold": 0.62, "prismatic": 0.10},  # 1er choix — Stage 2-1
    11: {"silver": 0.35, "gold": 0.45, "prismatic": 0.20},  # 2e choix  — Stage 3-2
    18: {"silver": 0.06, "gold": 0.74, "prismatic": 0.20},  # 3e choix  — Stage 4-2
}
_AUGMENT_TIERS = ("silver", "gold", "prismatic")


def stage_of(round_index: int) -> int:
    """Stage TFT : stage 1 = 3 rounds, puis stages de 7 rounds."""
    if round_index < PVE_OPENING:
        return 1
    return 2 + (round_index - PVE_OPENING) // ROUNDS_PER_STAGE


def round_in_stage(round_index: int) -> int:
    if round_index < PVE_OPENING:
        return round_index + 1
    return (round_index - PVE_OPENING) % ROUNDS_PER_STAGE + 1


def is_pvp(round_index: int) -> bool:
    """PvP sauf stage 1 (tout PvE) et, dans les stages 2+, le carrousel (x-4) et les monstres (x-7)."""
    if round_index < PVE_OPENING:
        return False
    return round_in_stage(round_index) not in (4, 7)


def stage_base_damage(round_index: int) -> int:
    return STAGE_BASE_DAMAGE.get(stage_of(round_index), 17)  # stage 7+ = 17


# --- debut de round --------------------------------------------------------
GOD_CHOICES = 3  # Realm of the Gods : choix d'1 champion parmi 3 (remplace le carrousel Set 17)

# Realm of the Gods : les Minor Blessings (= offrandes/votes) n'ont lieu qu'aux rounds
# 2-4, 3-4 et 4-4 (trois votes), apres quoi la majorite fixe le dieu aligne ; le God Boon
# arrive en 4-7 et le dieu droppe ensuite du loot. VERIFIE vs patch 17.4 le 2026-06-08
# (eloboost24 + mobalytics + bunnymuffins concordants : "during each carousel round 2-4,
# 3-4, 4-4 you choose a minor blessing"). Les x-4 des stages 5+ sont du loot, PAS un vote.
GOD_VOTE_STAGES = (2, 3, 4)


def is_god_round(round_index: int) -> bool:
    """Round d'offrande Realm of the Gods (Minor Blessing + vote) : 2-4, 3-4, 4-4 uniquement."""
    return stage_of(round_index) in GOD_VOTE_STAGES and round_in_stage(round_index) == 4


def _augments_by_tier(state: GameState) -> dict[str, list[str]]:
    """Augments du pool regulier groupes par tier (exclut les God Augments)."""
    groups: dict[str, list[str]] = {t: [] for t in _AUGMENT_TIERS}
    for api, aug in state.set_content.augments.items():
        if aug.tier in groups:
            groups[aug.tier].append(api)
    return groups


def sample_augments(state: GameState, player: PlayerState, round_index: int) -> list[str]:
    """Propose 3 augments : tire un tier par slot selon les vraies odds du round, puis un
    augment aleatoire de ce tier (distinct, jamais deja choisi par le joueur)."""
    groups = _augments_by_tier(state)
    odds = AUGMENT_TIER_ODDS.get(round_index, AUGMENT_TIER_ODDS[3])
    weights = [odds[t] for t in _AUGMENT_TIERS]
    taken = set(player.chosen_augments)
    offer: list[str] = []
    for _ in range(N_AUGMENT_CHOICES):
        # tente le tier tire, puis n'importe quel tier ayant encore un augment dispo
        tier = str(state.rng.choice(_AUGMENT_TIERS, p=weights))
        order = [tier] + [t for t in _AUGMENT_TIERS if t != tier]
        for t in order:
            pool = [a for a in groups[t] if a not in taken and a not in offer]
            if pool:
                offer.append(str(state.rng.choice(pool)))
                break
    if len(offer) < N_AUGMENT_CHOICES:  # filet : data degeneree
        offer += [f"AUG{i}" for i in range(N_AUGMENT_CHOICES - len(offer))]
    return offer


def _sample_gods(state: GameState) -> list[str]:
    champs = [a for a, c in state.set_content.champions.items() if 1 <= c.cost <= 5]
    if len(champs) >= GOD_CHOICES:
        return [str(k) for k in state.rng.choice(champs, size=GOD_CHOICES, replace=False)]
    return champs


def start_round(state: GameState) -> None:
    """Revenu + XP + shop gratuit + composant (PvE) + offre d'augment + reset planification."""
    pve = not is_pvp(state.round_index)
    augment_round = state.round_index in AUGMENT_ROUNDS
    components, _ = components_and_recipes(state.set_content)
    for p in state.alive_players():
        p.gold += round_income(p.gold, p.streak)
        p.level, p.xp = apply_xp(p.level, p.xp, ROUND_XP)
        p.shop = roll_shop(p.level, state.pool, state.rng)
        p.passed = False
        if pve and components:  # round PvE -> 1 composant aleatoire reel
            p.components.append(str(state.rng.choice(components)))
        if augment_round:
            p.augment_offer = sample_augments(state, p, state.round_index)
        if is_god_round(state.round_index):  # Realm of the Gods : 1 champion parmi 3
            p.god_offer = _sample_gods(state)


# --- combat ----------------------------------------------------------------
def _apply_damage(player: PlayerState, raw_damage: int) -> None:
    """Degats reduits par les augments (mitigation plafonnee)."""
    mitig = min(player.augment_power, MAX_AUGMENT_MITIGATION)
    player.hp -= max(0, round(raw_damage * (1.0 - mitig)))


def _fight(state: GameState, resolver: CombatResolver, p: PlayerState, q: PlayerState) -> None:
    res = resolver.resolve(
        p.board, q.board, state.set_content, state.rng,
        augments_a=tuple(p.chosen_augments), augments_b=tuple(q.chosen_augments),
    )
    winner, loser = (p, q) if res.winner == 0 else (q, p)
    _apply_damage(loser, stage_base_damage(state.round_index) + res.survivors)
    winner.streak = max(1, winner.streak + 1)
    loser.streak = min(-1, loser.streak - 1)


def resolve_combat(state: GameState, resolver: CombatResolver) -> None:
    """Resout le round courant. PvE = pas de combat ; PvP = appariement aleatoire."""
    if not is_pvp(state.round_index):
        return
    alive = state.alive_players()
    order = list(state.rng.permutation(len(alive)))
    shuffled = [alive[i] for i in order]
    for i in range(0, len(shuffled) - 1, 2):
        _fight(state, resolver, shuffled[i], shuffled[i + 1])
    if len(shuffled) % 2 == 1:  # joueur impair -> combat « fantome » (adversaire clone)
        lone = shuffled[-1]
        ghost = state.rng.choice([p for p in alive if p is not lone])
        res = resolver.resolve(
            lone.board, ghost.board, state.set_content, state.rng,
            augments_a=tuple(lone.chosen_augments), augments_b=tuple(ghost.chosen_augments),
        )
        if res.winner == 1:  # seul le joueur reel prend des degats
            _apply_damage(lone, stage_base_damage(state.round_index) + res.survivors)
            lone.streak = min(-1, lone.streak - 1)
        else:
            lone.streak = max(1, lone.streak + 1)


# --- eliminations ----------------------------------------------------------
def _free_units(state: GameState, player: PlayerState) -> None:
    """Rend les copies des unites d'un joueur elimine au pool partage (comme le vrai TFT)."""
    for unit in player.all_units():
        state.pool.give_back(unit.champion_api, unit.copies)
    player.bench.clear()
    player.board.clear()


def assign_eliminations(state: GameState) -> None:
    """Marque les joueurs a PV<=0 comme elimines ; place = nb de vivants restants + 1."""
    dead_now = [p for p in state.players.values() if p.alive and p.hp <= 0]
    # les PV les plus bas meurent en premier (placement le plus eleve)
    for p in sorted(dead_now, key=lambda x: x.hp):
        remaining = len([q for q in state.players.values() if q.alive])
        p.alive = False
        p.placement = remaining  # remaining inclut p lui-meme -> il prend cette place
        _free_units(state, p)  # ses unites retournent au pool


def finalize_if_over(state: GameState) -> bool:
    """Si <=1 vivant, attribue la 1re place au survivant. Retourne True si fini."""
    alive = state.alive_players()
    if len(alive) <= 1:
        for p in alive:
            p.placement = 1
            p.alive = False
        return True
    return False
