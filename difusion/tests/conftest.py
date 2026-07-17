from __future__ import annotations

from pathlib import Path

import pytest

from cucharadas_difusion.posts import create_draft, find_pair

REPO = Path(__file__).resolve().parents[2]
CASEN_ES = REPO / "_posts" / "2026-03-15-casen2024-julia-waffles-politica-publica.md"


@pytest.fixture
def repo() -> Path:
    return REPO


@pytest.fixture
def posts(repo: Path):
    return find_pair(repo, CASEN_ES)


@pytest.fixture
def valid_payload(posts):
    return {
        "es": "CASEN 2024 en una lectura territorial reproducible con Julia. #CASEN2024 #Julia",
        "en": "A reproducible territorial reading of CASEN 2024 with Julia. #CASEN2024 #Julia",
    }


@pytest.fixture
def draft(posts, valid_payload):
    return create_draft(posts, "test", valid_payload, [])
