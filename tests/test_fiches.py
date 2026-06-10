"""Tests du générateur de fiches d'audit (docs/fiches/).

Les fiches sont des vues markdown GÉNÉRÉES depuis la data CDragon + les registres moteur :
une par champion/trait/item/augment, avec le statut d'implémentation moteur. Jamais éditées
à la main — la source de vérité reste cdragon ; régénérer = `python -m scripts.generate_fiches`.
"""

from __future__ import annotations

import pytest

from tft_goat.data.content import load_set
from tft_goat.data.gods import god_boons
from tft_goat.engine.abilities import IMPLEMENTED
from tft_goat.engine.config import STAR_SCALE
from tft_goat.fiches import fmt, generate_all
from tft_goat.fiches.render import (
    render_augment,
    render_champion,
    render_item,
    render_trait,
)


@pytest.fixture(scope="module")
def sc():
    return load_set()


def test_generate_all_covers_every_entity(sc, tmp_path):
    """Chaque champion/trait/item/augment du contenu a sa fiche + un INDEX."""
    paths = generate_all(sc, tmp_path)
    assert len(paths["champions"]) == len(sc.champions)
    assert len(paths["traits"]) == len(sc.traits)
    assert len(paths["items"]) == len(sc.items)
    assert len(paths["augments"]) == len(sc.augments)
    for group in ("champions", "traits", "items", "augments"):
        for p in paths[group].values():
            assert p.is_file(), f"fiche manquante : {p}"
    assert (tmp_path / "INDEX.md").is_file()


def test_champion_fiche_has_real_stats_and_star_scaling(sc):
    """La fiche d'Ahri contient ses vraies stats CDragon et le scaling ×1.8 par étoile."""
    champ = sc.champions["TFT17_Aatrox"]
    md = render_champion(champ, sc)
    assert champ.name in md and champ.api_name in md
    assert fmt(champ.stats.hp) in md  # HP 1 étoile
    assert fmt(champ.stats.hp * STAR_SCALE[2]) in md  # HP 2 étoiles
    assert fmt(champ.stats.damage * STAR_SCALE[3]) in md  # AD 3 étoiles
    assert champ.ability is not None and champ.ability.name in md
    for trait_name in champ.traits:  # noms d'affichage, liés vers les fiches trait
        assert trait_name in md


def test_champion_ability_engine_status(sc):
    """Le statut moteur reflète le registre : ✅ si implémenté, 🟡 défaut sinon."""
    implemented = next(a for a in sorted(sc.champions) if a in IMPLEMENTED)
    md_ok = render_champion(sc.champions[implemented], sc)
    assert "✅" in md_ok

    missing = [a for a in sorted(sc.champions) if a not in IMPLEMENTED]
    if not missing:
        pytest.skip("toutes les abilities du contenu sont implémentées")
    md_default = render_champion(sc.champions[missing[0]], sc)
    assert "🟡" in md_default


def test_augment_fiche_god_boon(sc):
    """La fiche d'un God Boon nomme son dieu et son statut combat moteur."""
    boon = god_boons(sc)["Ahri"][0]
    md = render_augment(sc.augments[boon], sc)
    assert "Ahri" in md  # dieu identifié
    assert "god" in md  # tier
    assert ("✅" in md) or ("🟡" in md)  # statut moteur explicite


def test_item_fiche_recipe_and_hooks(sc):
    """Une fiche d'item complet liste ses 2 composants ; un item à proc liste ses hooks."""
    from tft_goat.engine.items_set17 import ITEM_COMBAT_START, ITEM_ON_ATTACK

    completed = next(
        i for _, i in sorted(sc.items.items())
        if len(i.composition) == 2 and all(c in sc.items for c in i.composition)
    )
    md = render_item(completed, sc)
    for comp in completed.composition:
        assert sc.items[comp].name in md

    procced = [a for a in sorted(sc.items) if a in ITEM_ON_ATTACK or a in ITEM_COMBAT_START]
    if not procced:
        pytest.skip("aucun item à proc dans le contenu")
    md_proc = render_item(sc.items[procced[0]], sc)
    assert "proc" in md_proc.lower()


def test_trait_fiche_breakpoints(sc):
    """Une fiche de trait affiche tous ses paliers d'activation."""
    trait = next(t for _, t in sorted(sc.traits.items()) if len(t.breakpoints) >= 2)
    md = render_trait(trait, sc)
    for bp in trait.breakpoints:
        assert f"{bp}" in md
    assert "Statut moteur" in md


def test_index_links_every_fiche(sc, tmp_path):
    """L'INDEX référence chaque fiche générée (lien relatif)."""
    paths = generate_all(sc, tmp_path)
    index = (tmp_path / "INDEX.md").read_text(encoding="utf-8")
    for group in ("champions", "traits", "items", "augments"):
        for p in paths[group].values():
            assert f"{group}/{p.name}" in index, f"{p.name} absent de l'INDEX"


def test_generation_is_deterministic(sc, tmp_path):
    """Deux générations -> exactement les mêmes octets (diff git propre)."""
    d1, d2 = tmp_path / "a", tmp_path / "b"
    p1 = generate_all(sc, d1)
    generate_all(sc, d2)
    assert (d1 / "INDEX.md").read_bytes() == (d2 / "INDEX.md").read_bytes()
    sample = sorted(p1["champions"])[0]
    rel = p1["champions"][sample].relative_to(d1)
    assert (d1 / rel).read_bytes() == (d2 / rel).read_bytes()


def test_fiches_never_handwritten_marker(sc):
    """Chaque fiche porte l'avertissement « générée — ne pas éditer »."""
    md = render_champion(sc.champions["TFT17_Aatrox"], sc)
    assert "NE PAS ÉDITER" in md
