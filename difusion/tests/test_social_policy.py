from types import SimpleNamespace

from cucharadas_difusion.destinations import _evaluar, cargar_catalogo, destination_checklist


def test_social_catalog_respects_opt_out():
    pair = {"es": SimpleNamespace(distribution={"social": False})}
    for destination in cargar_catalogo():
        if destination["id"] in {"mastodon-es", "bluesky-es"}:
            status, reason = _evaluar(destination, pair, [])
            assert status == "bloqueado"
            assert "social" in reason


def test_eligibility_is_not_a_completed_task(repo):
    result = destination_checklist(repo, "casen2024-julia-waffles")
    assert "[x]" not in result
    assert "no acredita publicación" in result
