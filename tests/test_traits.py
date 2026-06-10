"""Tests du calcul des traits actifs."""

from __future__ import annotations

from tft_goat.env.traits import active_traits, trait_counts

# Breakpoints Set 17 VÉRIFIÉS le 2026-06-08 : la data CDragon (source statique du jeu)
# concorde EXACTEMENT avec la table du skill tft-knowledge (sourcée officiel/mobalytics)
# pour ces 23 traits — double source indépendante. Pin anti-drift de patch/parsing.
# Stargazer est EXCLU : trait spécial à breakpoints variables par "constellation"
# (ex: Boar=3/4/5/6), le trait de base agrège (3,5,7,8,9,10) — voir test dédié.
SET17_TRAIT_BREAKPOINTS = {
    "Anima": (3, 6),
    "Arbiter": (2, 3),
    "Bastion": (2, 4, 6),
    "Brawler": (2, 4, 6),
    "Challenger": (2, 3, 4, 5),
    "Conduit": (2, 3, 4, 5),
    "Dark Star": (2, 4, 6, 9),
    "Fateweaver": (2, 4),
    "Marauder": (2, 4, 6),
    "Mecha": (3, 4, 6),
    "Meeple": (3, 5, 7, 10),
    "N.O.V.A.": (2, 5),
    "Primordian": (2, 3),
    "Psionic": (2, 4),
    "Replicator": (2, 4),
    "Rogue": (2, 3, 4, 5),
    "Shepherd": (3, 5, 7),
    "Sniper": (2, 3, 4),
    "Space Groove": (1, 3, 5, 7, 10),
    "Timebreaker": (2, 3, 4),
    "Vanguard": (2, 4, 6),
    "Voyager": (2, 3, 4, 5, 6),
}


def test_unique_champion_counting(sample_content):
    # deux copies du meme champion ne comptent qu'une fois
    counts = trait_counts(["c1", "c1", "c1"], sample_content)
    assert counts["Brawler"] == 1


def test_active_traits_breakpoints(sample_content):
    # c1,c4,c5 = 3 Brawler -> tier 1 (breakpoints 2/4/6 : 3>=2 seulement)
    active = active_traits(["c1", "c4", "c5"], sample_content)
    assert active["Brawler"] == 1


def test_active_traits_higher_tier(sample_content):
    # c1,c4,c5,c7 = 4 Brawler -> tier 2
    active = active_traits(["c1", "c4", "c5", "c7"], sample_content)
    assert active["Brawler"] == 2


def test_trait_below_breakpoint_inactive(sample_content):
    # c3 seul = 1 Mage -> pas de palier (Mage commence a 3)
    active = active_traits(["c3"], sample_content)
    assert "Mage" not in active


def test_multi_trait_champion(sample_content):
    # c2 porte Brawler + Mage ; avec c1 (Brawler) -> Brawler=2 actif, Mage=1 inactif
    active = active_traits(["c1", "c2"], sample_content)
    assert active.get("Brawler") == 1
    assert "Mage" not in active


def test_set17_trait_breakpoints_match_real_data():
    """Les breakpoints réels (CDragon) == table vérifiée pour les 23 traits standard."""
    from tft_goat.data.content import load_set

    sc = load_set()
    by_name = {t.name: t.breakpoints for t in sc.traits.values()}
    for name, expected in SET17_TRAIT_BREAKPOINTS.items():
        assert name in by_name, f"Trait {name} absent de la data Set 17"
        assert by_name[name] == expected, (
            f"{name} : data CDragon {by_name[name]} != vérifié {expected} "
            f"— re-vérifier vs patch live (breakpoints changés ?)"
        )


def test_every_trait_first_breakpoint_reachable_from_roster():
    """Invariant data : le 1er palier de chaque trait est atteignable avec le roster Set 17 seul.

    Sinon le trait ne s'activerait JAMAIS (bug). Les hauts paliers (Dark Star 9, Space Groove 10…)
    nécessitent des emblèmes = design TFT correct, hors scope ici. Vérifié 2026-06-08.
    """
    from collections import defaultdict

    from tft_goat.data.content import load_set

    sc = load_set()
    members: dict[str, int] = defaultdict(int)
    for api, c in sc.champions.items():
        if not api.startswith("TFT17_"):
            continue
        for t in c.traits:
            members[t] += 1

    for trait in sc.traits.values():
        positive = [b for b in trait.breakpoints if b > 0]
        if not positive:
            continue
        first = min(positive)
        n = members.get(trait.name, 0)
        assert first <= max(n, 1), (
            f"{trait.name}: 1er palier {first} > {n} membres -> trait inactivable"
        )


def test_stargazer_is_constellation_variable():
    """Stargazer = trait spécial : breakpoints variables par constellation.

    Vérifié vs patch 17.4 : chaque constellation a ses propres paliers (ex: Boar 3/4/5/6).
    Le trait de base agrège plusieurs paliers ; on documente qu'il N'est PAS un 3/5/7 fixe.
    Le moteur utilise les breakpoints du trait de base (approximation documentée).
    """
    from tft_goat.data.content import load_set

    sc = load_set()
    by_name = {t.name: t.breakpoints for t in sc.traits.values()}
    assert "Stargazer" in by_name
    # commence à 3 (toujours 3 unités pour activer) et a >3 paliers (constellation-variable)
    assert by_name["Stargazer"][0] == 3
    assert len(by_name["Stargazer"]) > 3
