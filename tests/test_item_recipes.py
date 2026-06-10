"""Vérifie la table de recettes composants -> objet complété contre la vraie data CDragon."""

from __future__ import annotations

from tft_goat.data.content import load_set
from tft_goat.env.items import components_and_recipes


def test_ten_components_and_55_recipes():
    """10 composants -> C(10,2)+10 = 55 recettes (combinatoire TFT complète)."""
    sc = load_set()
    comps, recipes = components_and_recipes(sc)
    assert len(comps) == 10
    assert len(recipes) == 55


def test_every_recipe_output_is_a_real_distinct_item():
    """Chaque recette produit un vrai objet complété existant ; les 55 sont distincts."""
    sc = load_set()
    _, recipes = components_and_recipes(sc)
    outputs = list(recipes.values())
    assert all(o in sc.items for o in outputs), "une recette pointe un objet inexistant"
    assert len(set(outputs)) == 55, "des recettes produisent le même objet"


def test_canonical_combos_verified_patch_17_4():
    """Combos canoniques vérifiés vs patch 17.4 (data CDragon, 2026-06-08)."""
    sc = load_set()
    _, recipes = components_and_recipes(sc)

    def combine(c1: str, c2: str) -> str:
        for key, out in recipes.items():
            if set(key) == {c1, c2}:
                return sc.items[out].name
        return "??"

    bf, rod = "TFT_Item_BFSword", "TFT_Item_NeedlesslyLargeRod"
    tear, belt = "TFT_Item_TearOfTheGoddess", "TFT_Item_GiantsBelt"
    assert combine(bf, bf) == "Deathblade"
    assert combine(rod, rod) == "Rabadon's Deathcap"
    assert combine(tear, tear) == "Blue Buff"
    assert combine(belt, belt) == "Warmog's Armor"
