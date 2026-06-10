"""Intégrité de la data champion réelle (mana de cast), vérifiée vs patch 17.4."""

from __future__ import annotations

from tft_goat.data.content import load_set


def _playable(sc):
    return [
        c for api, c in sc.champions.items()
        if api.startswith("TFT17_") and 1 <= c.cost <= 5
    ]


def test_most_playable_champions_have_real_cast_mana():
    """Garde-fou anti-panne de chargement : la grande majorité a un mana de cast réel (1..300).

    Vérifié 2026-06-08 : 63/65 jouables ont un mana réel ; les 2 exceptions (mana=0) sont des
    casters PASSIFS légitimes (voir test dédié), pas un échec de parsing.
    """
    sc = load_set()
    champs = _playable(sc)
    with_mana = [
        c for c in champs
        if c.stats and c.stats.mana and 1 <= c.stats.mana <= 300
    ]
    # tolérance : au plus quelques casters passifs (mana=0)
    assert len(with_mana) >= len(champs) - 3, (
        f"seulement {len(with_mana)}/{len(champs)} ont un mana réel -> panne de parsing ?"
    )


def test_attack_ranges_are_real_and_sane():
    """Ranges d'attaque réels (1..6), mélange mêlée/distance — vérifié vs patch 17.4 (2026-06-08).

    Buckets réels Set 17 : 1=mêlée (33), 2 (3), 4 (19), 6=carries longue portée (9, ex Jhin/Ezreal).
    Seule exception range=0 = Mini Black Hole (unité spéciale/fake). Garde-fou anti-régression data.
    """
    sc = load_set()
    champs = _playable(sc)
    melee = ranged = 0
    for c in champs:
        r = c.stats.attack_range if c.stats else None
        if c.api_name == "TFT17_DarkStar_FakeUnit":
            continue  # unité spéciale, range 0
        assert r is not None and 1 <= r <= 6, f"{c.name}: range absurde {r}"
        if r == 1:
            melee += 1
        else:
            ranged += 1
    assert melee >= 20, "trop peu d'unités mêlée -> parsing range cassé ?"
    assert ranged >= 20, "trop peu d'unités à distance -> parsing range cassé ?"


def test_caitlyn_is_a_passive_zero_mana_caster():
    """Caitlyn = ability PASSIVE (0 mana, headshot 15% sur auto-attaque) — vérifié vs patch 17.4.

    `mana=0` est de la VRAIE data (pas un bug) ; le moteur ne la mana-caste donc jamais
    (max_mana=1e9), comportement correct. Empêche un « fix » erroné qui lui mettrait du mana.
    """
    sc = load_set()
    cait = sc.champions.get("TFT17_Caitlyn")
    assert cait is not None
    assert cait.stats is not None
    assert cait.stats.mana == 0  # passif, pas de cast au mana
    assert cait.ability is not None  # a bien une ability (passive)
