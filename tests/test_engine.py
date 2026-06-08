"""Tests du vrai moteur de combat (vraies stats / etoiles / items / traits)."""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.data.models import Champion, SetContent, Stats, Trait, TraitEffect
from tft_goat.engine.config import STAR_SCALE
from tft_goat.engine.grid import distance, step_toward
from tft_goat.engine.resolver import EngineResolver
from tft_goat.engine.simulate import run_combat
from tft_goat.engine.trait_effects import apply_team_traits
from tft_goat.engine.unit import build_unit
from tft_goat.env.state import BoardUnit
from tft_goat.env.tft_env import TftEnv


def _stats(**kw):
    base = dict(hp=500.0, armor=20.0, magic_resist=20.0, damage=50.0, attack_speed=0.7,
                mana=50.0, initial_mana=0.0, crit_chance=0.25, crit_multiplier=1.4,
                attack_range=1.0)
    base.update(kw)
    return Stats(**base)


@pytest.fixture()
def content() -> SetContent:
    champs = {
        "melee": Champion(api_name="melee", name="melee", cost=2, traits=("Brawler",),
                          stats=_stats()),
        "ranged": Champion(api_name="ranged", name="ranged", cost=3, traits=(),
                           stats=_stats(attack_range=4.0)),
    }
    traits = {
        "T_Brawler": Trait(api_name="T_Brawler", name="Brawler",
                           effects=(TraitEffect(min_units=1, max_units=99,
                                                variables={"BonusArmor": 30.0}),)),
    }
    from tft_goat.data.models import Item
    items = {
        "itAD": Item(api_name="itAD", name="AD", effects={"AD": 0.5}),
        "itHP": Item(api_name="itHP", name="HP", effects={"Health": 300.0}),
    }
    return SetContent(patch="t", set_number=0, champions=champs, traits=traits,
                      items=items, augments={})


def test_star_scaling(content):
    u1 = build_unit(content.champions["melee"], 1, 0, content)
    u2 = build_unit(content.champions["melee"], 2, 0, content)
    assert u2.max_hp == pytest.approx(u1.max_hp * STAR_SCALE[2])
    assert u2.ad == pytest.approx(u1.ad * STAR_SCALE[2])


def test_item_raises_ad(content):
    bare = build_unit(content.champions["melee"], 1, 0, content)
    armed = build_unit(content.champions["melee"], 1, 0, content, item_apis=("itAD",))
    assert armed.ad == pytest.approx(bare.ad * 1.5)


def test_generic_items_raise_hp(content):
    bare = build_unit(content.champions["melee"], 1, 0, content)
    armed = build_unit(content.champions["melee"], 1, 0, content, generic_items=2)
    assert armed.max_hp > bare.max_hp


def test_trait_bonus_armor(content):
    units = [build_unit(content.champions["melee"], 1, 0, content)]
    base_armor = units[0].armor
    apply_team_traits(units, content)  # 1 Brawler -> +30 armure
    assert units[0].armor == pytest.approx(base_armor + 30.0)


def test_grid_distance_and_step():
    assert distance((0, 0), (0, 0)) == 0
    far = (7, 6)
    d0 = distance((0, 0), far)
    assert d0 > 0
    nxt = step_toward((0, 0), far, occupied=set())
    assert distance(nxt, far) < d0


def test_run_combat_stronger_board_wins(content):
    rng = np.random.default_rng(0)
    strong = [BoardUnit("melee", 2), BoardUnit("melee", 2), BoardUnit("ranged", 2)]
    weak = [BoardUnit("melee", 1)]
    wins = sum(run_combat(strong, weak, content, rng).winner == 0 for _ in range(20))
    assert wins >= 18


def test_run_combat_empty_board(content):
    res = run_combat([], [BoardUnit("melee", 1)], content, np.random.default_rng(0))
    assert res.winner == 1


def test_all_set17_abilities_execute():
    """Chaque sort Set 17 implemente s'execute sans erreur dans un contexte de combat."""
    from tft_goat.data.content import load_set
    from tft_goat.engine.abilities import get_ability
    from tft_goat.engine.abilities_set17 import SET17_ABILITIES
    from tft_goat.engine.simulate import CombatContext
    from tft_goat.engine.unit import build_unit

    content = load_set()
    rng = np.random.default_rng(0)
    assert len(SET17_ABILITIES) >= 68
    for api in SET17_ABILITIES:
        champ = content.champions.get(api)
        if champ is None:
            continue
        caster = build_unit(champ, 2, 0, content)
        caster.pos = (3, 3)
        enemy = build_unit(content.champions["TFT17_Briar"], 1, 1, content)
        enemy.pos = (4, 3)
        ally = build_unit(content.champions["TFT17_Shen"], 1, 0, content)
        ally.pos = (2, 3)
        ctx = CombatContext([caster, enemy, ally], rng)
        get_ability(api)(caster, [ally], [enemy], ctx)  # ne doit pas lever


def test_ie_enables_ability_crit(content):
    bare = build_unit(content.champions["melee"], 1, 0, content)
    with_ie = build_unit(content.champions["melee"], 1, 0, content,
                         item_apis=("TFT_Item_InfinityEdge",))
    assert with_ie.can_ability_crit is True
    assert bare.can_ability_crit is False


def test_damage_amp_increases_damage(content):
    import numpy as np
    from tft_goat.engine.simulate import CombatContext

    rng = np.random.default_rng(0)
    src = build_unit(content.champions["melee"], 1, 0, content)
    src.crit_chance = 0.0  # isole l'effet du damage amp
    tgt1 = build_unit(content.champions["melee"], 1, 1, content)
    tgt2 = build_unit(content.champions["melee"], 1, 1, content)
    CombatContext([src, tgt1], rng).deal_magic(src, tgt1, 100)
    src.damage_amp = 1.0  # +100%
    CombatContext([src, tgt2], rng).deal_magic(src, tgt2, 100)
    assert (tgt1.hp - tgt2.hp) > 1.0  # tgt2 a pris plus de degats


def test_new_item_hooks_real_content():
    """on-damaged (Bramble), on-tick (Dragon's Claw), hp-threshold (Sterak)."""
    import numpy as np
    from tft_goat.data.content import load_set
    from tft_goat.engine.items_set17 import ITEM_ON_TICK
    from tft_goat.engine.simulate import CombatContext

    c = load_set()
    rng = np.random.default_rng(0)
    atk = build_unit(c.champions["TFT17_Briar"], 2, 0, c)
    bram = build_unit(c.champions["TFT17_Shen"], 2, 1, c, item_apis=("TFT_Item_BrambleVest",))
    ctx = CombatContext([atk, bram], rng)
    hp0 = atk.hp
    ctx.deal_physical(atk, bram, 100)
    assert atk.hp < hp0  # reflect

    dc = build_unit(c.champions["TFT17_Shen"], 2, 0, c, item_apis=("TFT_Item_DragonsClaw",))
    dc.hp = dc.max_hp * 0.5
    ITEM_ON_TICK["TFT_Item_DragonsClaw"](dc, ctx)
    assert dc.hp > dc.max_hp * 0.5  # regen

    st = build_unit(c.champions["TFT17_Shen"], 2, 1, c, item_apis=("TFT_Item_SteraksGage",))
    st.hp = st.max_hp * 0.5
    CombatContext([atk, st], rng).deal_magic(atk, st, 1)
    assert st.shield > 0  # bouclier de seuil declenche


def test_all_registry_apis_exist_in_content():
    """Garde : chaque item/augment reference dans un registre EXISTE dans la vraie data."""
    from tft_goat.data.content import load_set
    from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
    from tft_goat.engine.items_set17 import (
        ITEM_COMBAT_START,
        ITEM_HP_THRESHOLD,
        ITEM_ON_ATTACK,
        ITEM_ON_CAST,
        ITEM_ON_DAMAGED,
        ITEM_ON_TICK,
        ITEM_REVIVE,
    )

    c = load_set()
    item_apis = set().union(
        ITEM_COMBAT_START, ITEM_ON_ATTACK, ITEM_ON_CAST,
        ITEM_ON_DAMAGED, ITEM_ON_TICK, ITEM_HP_THRESHOLD, ITEM_REVIVE,
    )
    assert [a for a in item_apis if a not in c.items] == []
    assert [a for a in AUGMENT_REGISTRY if a not in c.augments] == []


def test_durability_reduces_incoming_damage():
    import numpy as np
    from tft_goat.data.content import load_set
    from tft_goat.engine.simulate import CombatContext

    c = load_set()
    rng = np.random.default_rng(0)
    atk = build_unit(c.champions["TFT17_Briar"], 2, 0, c)
    normal = build_unit(c.champions["TFT17_Shen"], 2, 1, c)
    tanky = build_unit(c.champions["TFT17_Shen"], 2, 1, c)
    tanky.incoming_reduction = 0.5
    CombatContext([atk, normal], rng).deal_true(atk, normal, 200)
    CombatContext([atk, tanky], rng).deal_true(atk, tanky, 200)
    assert tanky.hp > normal.hp  # le durable prend moins de degats


def test_revive_mechanism():
    import numpy as np
    from tft_goat.data.content import load_set
    from tft_goat.engine.items_set17 import ITEM_REVIVE
    from tft_goat.engine.simulate import CombatContext

    c = load_set()
    ITEM_REVIVE["__TEST_REVIVE__"] = lambda u, ctx: setattr(u, "hp", u.max_hp * 0.3)
    try:
        u = build_unit(c.champions["TFT17_Shen"], 2, 1, c)
        u.item_apis = ("__TEST_REVIVE__",)
        atk = build_unit(c.champions["TFT17_Briar"], 2, 0, c)
        ctx = CombatContext([atk, u], np.random.default_rng(0))
        ctx.deal_true(atk, u, u.hp + 9999)  # letal
        assert u.alive is True and u.hp > 0  # ressuscite une fois
        ctx.deal_true(atk, u, u.hp + 9999)  # 2e mort
        assert u.alive is False  # definitive
    finally:
        del ITEM_REVIVE["__TEST_REVIVE__"]


def test_mirror_matchup_is_fair():
    """Un matchup miroir doit etre ~50/50 (pas de biais 'equipe 0 agit en premier')."""
    from tft_goat.data.content import load_set
    from tft_goat.engine.simulate import run_combat

    content = load_set()
    b = [BoardUnit("TFT17_Jhin", 2), BoardUnit("TFT17_Shen", 2),
         BoardUnit("TFT17_Leona", 2), BoardUnit("TFT17_Caitlyn", 2)]
    a = [BoardUnit(u.champion_api, u.star) for u in b]
    wins = sum(run_combat(a, b, content, np.random.default_rng(i)).winner == 0 for i in range(80))
    assert 24 <= wins <= 56  # ~50/80, large bande anti-flake


def test_all_augments_and_item_procs_execute():
    """Tous les augments de combat + procs d'items s'executent sans erreur."""
    from tft_goat.data.content import load_set
    from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
    from tft_goat.engine.items_set17 import (
        ITEM_COMBAT_START,
        ITEM_ON_ATTACK,
        ITEM_ON_CAST,
    )
    from tft_goat.engine.simulate import CombatContext
    from tft_goat.engine.unit import build_unit

    content = load_set()
    rng = np.random.default_rng(0)

    def mk(api, team):
        u = build_unit(content.champions[api], 2, team, content)
        u.pos = (team, 0)
        return u

    team = [mk("TFT17_Jhin", 0), mk("TFT17_Shen", 0)]
    enemies = [mk("TFT17_Briar", 1), mk("TFT17_Leona", 1)]
    units = team + enemies

    for api, fn in AUGMENT_REGISTRY.items():
        fn(list(team), list(enemies), CombatContext(list(units), rng), content.augments[api].effects)
    for api, fn in ITEM_COMBAT_START.items():
        fn(mk("TFT17_Jhin", 0), CombatContext(list(units), rng))
    for api, fn in ITEM_ON_ATTACK.items():
        fn(mk("TFT17_Jhin", 0), mk("TFT17_Briar", 1), CombatContext(list(units), rng))
    for api, fn in ITEM_ON_CAST.items():
        fn(mk("TFT17_Jhin", 0), CombatContext(list(units), rng))
    assert len(AUGMENT_REGISTRY) >= 40


def test_engine_resolver_in_env(sample_content):
    """EngineResolver enfiche dans l'env -> partie complete (contenu synthetique, rapide)."""
    env = TftEnv(set_content=sample_content, resolver=EngineResolver())
    obs, infos = env.reset(seed=0)
    rng = np.random.default_rng(0)
    steps = 0
    while env.agents and steps < 20000:
        acts = {a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"]))) for a in env.agents}
        obs, r, t, tr, infos = env.step(acts)
        steps += 1
    assert env.agents == []
    assert sorted(p.placement for p in env._state.players.values()) == list(range(1, 9))
