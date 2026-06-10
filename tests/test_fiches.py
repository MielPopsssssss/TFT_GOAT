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
    """La fiche d'un God Boon identifie son dieu (ligne dédiée) et son vrai statut moteur."""
    from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY

    boon = god_boons(sc)["Ahri"][0]
    md = render_augment(sc.augments[boon], sc)
    # ligne d'identification du dieu — PAS le nom de l'augment (qui contient déjà « Ahri »)
    assert "boon du dieu **Ahri**" in md
    assert "Realm of the Gods" in md
    # statut moteur lié au VRAI registre (pas une assertion vide ✅-ou-🟡)
    status_section = md.split("## Statut combat moteur")[1]
    expected = "✅" if boon in AUGMENT_REGISTRY else "🟡"
    assert expected in status_section


def test_augment_fiche_non_god_has_no_boon_line(sc):
    """Un augment non-god n'a JAMAIS de ligne God Boon, et son statut reflète le registre."""
    from tft_goat.engine.augments_set17 import AUGMENT_REGISTRY
    from tft_goat.fiches.status import god_of_augment

    api, aug = next((a, x) for a, x in sorted(sc.augments.items()) if x.tier != "god")
    assert god_of_augment(aug) is None
    md = render_augment(aug, sc)
    assert "boon du dieu" not in md
    status_section = md.split("## Statut combat moteur")[1]
    expected = "✅" if api in AUGMENT_REGISTRY else "🟡"
    assert expected in status_section


def test_god_boons_raises_on_ambiguous_api_name():
    """Data ambiguë (apiName matchant 2 dieux) -> erreur explicite, jamais devinée."""
    from tft_goat.data.models import Augment, SetContent

    ambiguous = Augment(
        api_name="TFT17_Augment_AhriYasuoGodAugment", name="Chimère", tier="god"
    )
    content = SetContent(
        patch="test", set_number=17, champions={}, traits={}, items={},
        augments={ambiguous.api_name: ambiguous},
    )
    with pytest.raises(ValueError, match="ambigu"):
        god_boons(content)


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
    """Deux générations -> exactement les mêmes octets pour CHAQUE fiche (diff git propre)."""
    d1, d2 = tmp_path / "a", tmp_path / "b"
    p1 = generate_all(sc, d1)
    generate_all(sc, d2)
    assert (d1 / "INDEX.md").read_bytes() == (d2 / "INDEX.md").read_bytes()
    for group, files in p1.items():
        for api, path1 in files.items():
            path2 = d2 / group / path1.name
            assert path1.read_bytes() == path2.read_bytes(), f"non déterministe : {group}/{api}"


def test_fiches_never_handwritten_marker(sc):
    """Chaque fiche porte l'avertissement « générée — ne pas éditer »."""
    md = render_champion(sc.champions["TFT17_Aatrox"], sc)
    assert "NE PAS ÉDITER" in md


def test_item_fiche_base_component_is_stats_only(sc):
    """Un composant de base (sans recette ni proc) : type explicite + 🟡 stats uniquement."""
    from tft_goat.fiches.status import item_proc_hooks

    item = next(
        i for _, i in sorted(sc.items.items())
        if not i.composition and not item_proc_hooks(i.api_name)
    )
    md = render_item(item, sc)
    assert "composant de base" in md
    assert "🟡 stats uniquement" in md


def test_item_fiche_odd_composition_renders_generic_line(sc):
    """Une composition atypique (≠ 0 et ≠ 2 composants) passe par la ligne générique."""
    from tft_goat.data.models import Item

    odd = Item(api_name="TFT_Test_Odd", name="Triple", composition=("a", "b", "c"))
    md = render_item(odd, sc)
    assert "**Composition**" in md
    assert "Recette" not in md


def test_trait_fiche_without_stat_variables(sc):
    """Un trait sans variable numérique affiche le message dédié (pas de table vide)."""
    trait = next(
        (t for _, t in sorted(sc.traits.items()) if not {k for e in t.effects for k in e.variables}),
        None,
    )
    if trait is None:
        pytest.skip("tous les traits du contenu ont des variables")
    md = render_trait(trait, sc)
    assert "Aucune variable" in md


def test_trait_name_collision_is_explicit(sc):
    """8 traits « Stargazer » : seule la variante résolue par le moteur revendique ✅/porteurs.

    Le moteur joint les traits par nom d'affichage (dernier homonyme gagnant). Une fiche de
    variante masquée ne doit JAMAIS revendiquer d'application moteur ni lister de porteurs.
    """
    from tft_goat.fiches.status import shadowed_by, trait_name_winner

    stargazers = [a for a, t in sorted(sc.traits.items()) if t.name == "Stargazer"]
    assert len(stargazers) == 8  # pin data : 8 variantes homonymes (patch 17.4)
    winner_api = trait_name_winner(sc)["Stargazer"]
    shadowed_api = next(a for a in stargazers if a != winner_api)

    md_shadow = render_trait(sc.traits[shadowed_api], sc)
    assert "Collision de nom" in md_shadow
    assert winner_api in md_shadow  # pointe vers le trait réellement résolu
    assert "✅" not in md_shadow  # aucune fausse revendication d'application
    assert "Champions avec ce trait" not in md_shadow  # porteurs non attribuables

    md_winner = render_trait(sc.traits[winner_api], sc)
    assert "Collision de nom" not in md_winner
    assert shadowed_by(sc.traits[winner_api], sc) is None


def test_god_of_augment_raises_on_ambiguous_api_name():
    """Même politique que god_boons : apiName matchant 2 dieux -> erreur, jamais deviné."""
    from tft_goat.data.models import Augment
    from tft_goat.fiches.status import god_of_augment

    ambiguous = Augment(
        api_name="TFT17_Augment_AhriYasuoGodAugment", name="Chimère", tier="god"
    )
    with pytest.raises(ValueError, match="ambigu"):
        god_of_augment(ambiguous)


def test_strip_html_cleans_cdragon_noise():
    """_strip_html : tags, icônes %i:...%, &nbsp;, parenthèses vidées ; @Var@ conservés."""
    from tft_goat.fiches.render import _strip_html

    raw = "Deal <magicDamage>@Damage@&nbsp;(%i:scaleAP%)</magicDamage> damage"
    assert _strip_html(raw) == "Deal @Damage@ damage"
