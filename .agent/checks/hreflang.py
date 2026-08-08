#!/usr/bin/env python3
"""Reciprocidad de hreflang entre los pares ES/EN del artefacto.

Motivo: 12 de las 30 URLs del sitemap eran pares ES/EN que no emitían ninguna
señal hreflang en el HTML, mientras el sitemap XML sí la declaraba. Señales
contradictorias entre sitemap y página son la causa mecánica de que Google
descarte la canónica declarada y elija otra.

La causa de raíz estaba en el guard de `_includes/head/custom.html`, que exigía
`page.permalink` — algo que la portada no tiene por diseño y que las páginas de
archivo tampoco declaran.

Regla comprobada: si existen la variante ES y la EN de una URL, y ambas son
indexables, las DOS deben emitir hreflang es, hreflang en y x-default, y esos
valores deben apuntar a las URLs reales.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SITE_URL, load_pages, normalize, report, require_artifact  # noqa: E402

DEFAULT_LANG = "es"
ALT_LANG = "en"


def es_url(url: str) -> str:
    """`/en/about/` -> `/about/`; `/en/` -> `/`."""
    if url == f"/{ALT_LANG}/":
        return "/"
    if url.startswith(f"/{ALT_LANG}/"):
        return url[len(f"/{ALT_LANG}") :]
    return url


def en_url(url: str) -> str:
    """`/about/` -> `/en/about/`; `/` -> `/en/`."""
    return f"/{ALT_LANG}{url}" if url != "/" else f"/{ALT_LANG}/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", help="directorio del artefacto construido")
    args = parser.parse_args()

    root = require_artifact(args.artifact)
    pages = {p.url: p for p in load_pages(root)}

    # Pares canónicos ES/EN en los que AMBAS variantes existen y son indexables.
    pairs: list[tuple[str, str]] = []
    for url, page in sorted(pages.items()):
        if url.startswith(f"/{ALT_LANG}/"):
            continue  # el par se registra desde el lado ES
        twin = en_url(url)
        if twin in pages and page.indexable and pages[twin].indexable:
            pairs.append((url, twin))

    problems: list[str] = []
    for spanish, english in pairs:
        expected = {
            DEFAULT_LANG: normalize(SITE_URL + spanish),
            ALT_LANG: normalize(SITE_URL + english),
            "x-default": normalize(SITE_URL + spanish),
        }
        for url in (spanish, english):
            emitted = {k: normalize(v) for k, v in pages[url].hreflang.items()}
            if not emitted:
                problems.append(f"{url} no emite ningún hreflang (par: {spanish} / {english})")
                continue
            for lang, want in expected.items():
                got = emitted.get(lang)
                if got is None:
                    problems.append(f"{url} no emite hreflang=\"{lang}\"")
                elif got != want:
                    problems.append(f"{url} emite hreflang=\"{lang}\" -> {got}, se esperaba {want}")

    if not pairs:
        print("FAIL hreflang: no se detectó ningún par ES/EN indexable; revisar el artefacto")
        return 1

    return report(f"hreflang recíproco en {len(pairs)} pares ES/EN", problems, len(pairs) * 2)


if __name__ == "__main__":
    sys.exit(main())
