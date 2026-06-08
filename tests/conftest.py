"""Fixtures partagees pour les tests de l'environnement.

`sample_content` reutilise le builder synthetique de production (data.sample) : deterministe,
independant du snapshot CDragon (gitignored), donc sur pour la CI.
"""

from __future__ import annotations

import pytest

from tft_goat.data.models import SetContent
from tft_goat.data.sample import build_sample_content


@pytest.fixture(scope="session")
def sample_content() -> SetContent:
    return build_sample_content()
