#!/usr/bin/env python3
"""Comprobaciones de markup sobre el artefacto construido.

Cubre la barra de navegación propia (Fase 1) y los soft-404 (Fase 2).

Contexto de la barra: el greedy-nav del tema calculaba el espacio disponible sin
restar los dos controles que el sitio le inyectaba dentro (`lang-switcher` y
`theme-toggle`). Sobrestimaba ~71 px, no movía nada a `.hidden-links`, dejaba la
hamburguesa oculta, y `.visible-links { overflow: hidden }` recortaba en
silencio: «Acerca de» aparecía cortado y «Publicaciones» desaparecía.

Estos comprobadores fijan la corrección para que no pueda revertirse sin aviso.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_html, load_pages, report, require_artifact  # noqa: E402

NAV_OPEN = re.compile(r"<nav\b[^>]*\bid=[\"']site-nav[\"'][^>]*>", re.I)
NAV_BLOCK = re.compile(r"<nav\b[^>]*\bid=[\"']site-nav[\"'].*?</nav>", re.I | re.S)
BANNER = re.compile(r"Minimal Mistakes Jekyll Theme\s+([0-9.]+)")


def _pages_with_masthead(root: Path) -> list[Path]:
    return [p for p in iter_html(root) if NAV_OPEN.search(p.read_text("utf-8", errors="replace"))]


def check_no_greedy_nav(root: Path) -> int:
    problems = []
    files = list(iter_html(root))
    for path in files:
        text = path.read_text("utf-8", errors="replace")
        for token in ("greedy-nav", "visible-links", "hidden-links"):
            if token in text:
                problems.append(f"{path.relative_to(root)} todavía contiene '{token}'")
    return report("HTML sin restos de greedy-nav", problems, len(files))


def check_site_nav(root: Path) -> int:
    problems = []
    files = _pages_with_masthead(root)
    if not files:
        print("FAIL barra propia: ninguna página emite <nav id=\"site-nav\">")
        return 1

    for path in files:
        rel = path.relative_to(root)
        text = path.read_text("utf-8", errors="replace")
        block = NAV_BLOCK.search(text)
        if not block:
            problems.append(f"{rel}: <nav id=site-nav> sin cierre </nav>")
            continue
        nav = block.group(0)

        if 'class="masthead__nav"' not in nav and "class='site-nav'" not in nav:
            problems.append(f"{rel}: <nav id=site-nav> sin class=\"site-nav\"")
        if "aria-label" not in nav:
            problems.append(f"{rel}: <nav id=site-nav> sin aria-label")
        if 'id="site-nav-menu"' not in nav:
            problems.append(f"{rel}: falta <ul id=\"site-nav-menu\">")
        if "masthead__nav-toggle" not in nav:
            problems.append(f"{rel}: falta el botón .masthead__nav-toggle")
        if 'aria-expanded="false"' not in nav:
            problems.append(f"{rel}: el botón no arranca con aria-expanded=\"false\"")
        if 'aria-controls="site-nav-menu"' not in nav:
            problems.append(f"{rel}: el botón no declara aria-controls=\"site-nav-menu\"")
        if nav.count("<li") < 2:
            problems.append(f"{rel}: la barra emite {nav.count('<li')} enlace(s), se esperaban 2")

    return report("barra propia accesible", problems, len(files))


def check_controls_outside_nav(root: Path) -> int:
    """Los controles deben ser hermanos del <nav>, no hijos.

    Ésta es la corrección estructural: mientras vivieran dentro del <nav>,
    cualquier algoritmo de medición del tema los ignoraría al repartir el ancho.
    """
    problems = []
    files = _pages_with_masthead(root)
    for path in files:
        rel = path.relative_to(root)
        text = path.read_text("utf-8", errors="replace")
        block = NAV_BLOCK.search(text)
        if not block:
            continue
        nav = block.group(0)
        for control in ("theme-toggle", "lang-switcher"):
            if control in nav:
                problems.append(f"{rel}: '{control}' sigue DENTRO de <nav id=site-nav>")
        if "masthead__controls" not in text:
            problems.append(f"{rel}: no existe el contenedor .masthead__controls")
    return report("controles fuera del <nav>", problems, len(files))


def check_theme_bundle(root: Path, expected: str) -> int:
    bundle = root / "assets" / "js" / "main.min.js"
    if not bundle.exists():
        print(f"FAIL bundle del tema: no existe {bundle.relative_to(root)}")
        return 1
    head = bundle.read_text("utf-8", errors="replace")[:400]
    match = BANNER.search(head)
    if not match:
        print("FAIL bundle del tema: no se pudo leer la versión del banner")
        return 1
    if match.group(1) != expected:
        print(f"FAIL bundle del tema: es {match.group(1)}, se esperaba {expected}")
        print("     Probablemente reapareció una copia vendorizada en assets/js/.")
        return 1
    print(f"OK   bundle del tema: {match.group(1)} (servido desde la gema)")
    return 0


def check_soft_404(root: Path) -> int:
    """`/404.html` responde 200 al pedirse directamente: sin noindex es un soft-404.

    Además estaba enlazada desde `/sitemap/`, que iteraba `site.pages` sin filtro
    y por tanto le daba a Googlebot una ruta de descubrimiento.

    Se miran los enlaces del contenido (`content_links`), no todos los del
    documento: el pie del tema enlaza `/feed.xml` en las 30 páginas del sitio, y
    contarlo aquí acusaba al bucle del sitemap de un enlace que no escribe. Lo
    que este comprobador vigila es lo que emite la plantilla de `/sitemap/`.
    """
    problems = []
    pages = load_pages(root)
    error_pages = [p for p in pages if p.path.name == "404.html"]

    if not error_pages:
        print("FAIL soft-404: no se encontró ninguna página 404 en el artefacto")
        return 1

    for page in error_pages:
        if not page.noindex:
            problems.append(f"{page.url} no lleva <meta name=robots content=noindex>")

    error_urls = {p.url for p in error_pages}
    for page in pages:
        if not page.url.rstrip("/").endswith("/sitemap"):
            continue
        for href in page.content_links:
            target = href.removeprefix("https://3cucharadas.cl")
            if target in error_urls:
                problems.append(f"{page.url} enlaza a {target}")
            if target.rsplit("/", 1)[-1] in {"robots.txt", "sitemap.xml"} or target.endswith(
                (".css", ".js", ".xml")
            ):
                problems.append(f"{page.url} enlaza al recurso no-página {target}")

    return report("soft-404 cerrados", problems, len(error_pages))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact")
    parser.add_argument("--no-greedy-nav", action="store_true")
    parser.add_argument("--site-nav", action="store_true")
    parser.add_argument("--controls-outside-nav", action="store_true")
    parser.add_argument("--theme-bundle-version", metavar="X.Y.Z")
    parser.add_argument("--soft-404", action="store_true")
    args = parser.parse_args()

    root = require_artifact(args.artifact)
    codes = []
    if args.no_greedy_nav:
        codes.append(check_no_greedy_nav(root))
    if args.site_nav:
        codes.append(check_site_nav(root))
    if args.controls_outside_nav:
        codes.append(check_controls_outside_nav(root))
    if args.theme_bundle_version:
        codes.append(check_theme_bundle(root, args.theme_bundle_version))
    if args.soft_404:
        codes.append(check_soft_404(root))

    if not codes:
        codes = [
            check_no_greedy_nav(root),
            check_site_nav(root),
            check_controls_outside_nav(root),
            check_soft_404(root),
        ]
    return max(codes)


if __name__ == "__main__":
    sys.exit(main())
