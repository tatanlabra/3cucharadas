#!/usr/bin/env python3
"""Coherencia de URLs canónicas y del sitemap sobre el artefacto construido.

Motivo: Google Search Console reportaba «Duplicada: Google ha elegido una versión
canónica diferente a la del usuario». La causa mecánica es que dos o más URLs
emitían la misma canónica, o que una URL indexable declaraba canónica otra
distinta de sí misma.

Una página con `noindex` o con meta-refresh SÍ puede apuntar su canónica a otra
URL: es exactamente lo que debe hacer un stub de redirección. Por eso los tres
modos ignoran las páginas no indexables.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    load_pages,
    normalize,
    report,
    require_artifact,
    sitemap_locs,
    url_to_path,
)

PAGINATOR = re.compile(r"/page/?\d+/?$")


def check_no_duplicates(root: Path) -> int:
    pages = [p for p in load_pages(root) if p.indexable]
    by_canonical: dict[str, list[str]] = defaultdict(list)
    for page in pages:
        if page.canonical:
            by_canonical[normalize(page.canonical)].append(page.url)

    problems = [
        f"{canonical} lo declaran {len(urls)} URLs indexables: {', '.join(sorted(urls))}"
        for canonical, urls in sorted(by_canonical.items())
        if len(urls) > 1
    ]
    return report("canonicals sin duplicar", problems, len(pages))


def check_self_referential(root: Path) -> int:
    pages = [p for p in load_pages(root) if p.indexable]
    problems = []
    for page in pages:
        if not page.canonical:
            problems.append(f"{page.url} no emite <link rel=canonical>")
            continue
        if normalize(page.canonical) != normalize(page.url):
            problems.append(f"{page.url} declara canónica {page.canonical}")
    return report("canonicals autorreferentes", problems, len(pages))


def check_sitemap_clean(root: Path) -> int:
    locs = sitemap_locs(root)
    if not locs:
        print("FAIL sitemap: no se encontró sitemap.xml en el artefacto")
        return 1

    problems = []
    for loc in locs:
        if PAGINATOR.search(loc):
            problems.append(f"{loc} es una página del paginador y no debe estar en el sitemap")
            continue

        path = url_to_path(loc, root)
        if not path.exists():
            problems.append(f"{loc} no corresponde a ninguna página generada (404)")
            continue

        from _common import read_page  # import diferido: solo se usa aquí

        page = read_page(path, root)
        if page.refresh_to:
            problems.append(f"{loc} es una redirección (meta-refresh hacia {page.refresh_to})")
        elif page.noindex:
            problems.append(f"{loc} lleva noindex y no debe declararse en el sitemap")
        elif page.canonical and normalize(page.canonical) != normalize(loc):
            problems.append(f"{loc} declara canónica {page.canonical}")

    return report("sitemap sin URLs muertas", problems, len(locs))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", help="directorio del artefacto construido")
    parser.add_argument("--no-duplicates", action="store_true")
    parser.add_argument("--self-referential", action="store_true")
    parser.add_argument("--sitemap-clean", action="store_true")
    args = parser.parse_args()

    root = require_artifact(args.artifact)
    modes = [
        (args.no_duplicates, check_no_duplicates),
        (args.self_referential, check_self_referential),
        (args.sitemap_clean, check_sitemap_clean),
    ]
    selected = [fn for flag, fn in modes if flag] or [fn for _, fn in modes]
    return max(fn(root) for fn in selected)


if __name__ == "__main__":
    sys.exit(main())
