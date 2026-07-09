#!/usr/bin/env python3
"""Build static redirect pages for the historical GitHub Pages URL."""

from __future__ import annotations

import shutil
from html import escape
from pathlib import Path


SITE_DIR = Path("_site")
OUT_DIR = Path(".redirect_build")
OLD_PROJECT_PREFIX = "/3cucharadas"
NEW_BASE = "https://3cucharadas.cl"

REDIRECT_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirección a 3 Cucharadas</title>
  <link rel="canonical" href="{target}">
  <meta http-equiv="refresh" content="0; url={target}">
  <meta name="robots" content="index, follow">
  <script>
    window.location.replace({target_js});
  </script>
</head>
<body>
  <p>El sitio se trasladó a <a href="{target}">{target}</a>.</p>
</body>
</html>
"""

FOUR_O_FOUR = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirección a 3 Cucharadas</title>
  <link rel="canonical" href="https://3cucharadas.cl/">
  <meta name="robots" content="index, follow">
  <script>
    (function () {
      var path = window.location.pathname || "/";
      if (path.indexOf("/3cucharadas") === 0) {
        path = path.slice("/3cucharadas".length) || "/";
      }
      var target = "https://3cucharadas.cl" + path + window.location.search + window.location.hash;
      window.location.replace(target);
    }());
  </script>
</head>
<body>
  <p>El sitio se trasladó a <a href="https://3cucharadas.cl/">https://3cucharadas.cl/</a>.</p>
</body>
</html>
"""


def html_target_for(site_file: Path) -> tuple[Path, str]:
    rel = site_file.relative_to(SITE_DIR)
    rel_posix = rel.as_posix()

    if rel_posix == "404.html":
        raise ValueError("404.html is generated separately")

    if rel.name == "index.html":
        parent = rel.parent.as_posix()
        rel_url = "/" if parent == "." else f"/{parent.strip('/')}/"
        out_rel = rel
    else:
        stem_rel = rel.with_suffix("")
        rel_url = f"/{stem_rel.as_posix().strip('/')}/"
        out_rel = stem_rel / "index.html"

    target = NEW_BASE.rstrip("/") + rel_url
    return out_rel, target


def write_redirect(out_file: Path, target: str) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    html = REDIRECT_TEMPLATE.format(
        target=escape(target, quote=True),
        target_js=repr(target),
    )
    out_file.write_text(html, encoding="utf-8")


def main() -> None:
    if not SITE_DIR.exists():
        raise SystemExit(
            "No existe _site. Ejecuta primero: JEKYLL_ENV=production bundle exec jekyll build"
        )

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    html_files = sorted(p for p in SITE_DIR.rglob("*.html") if p.is_file())
    written = 0
    for html_file in html_files:
        try:
            out_rel, target = html_target_for(html_file)
        except ValueError:
            continue
        write_redirect(OUT_DIR / out_rel, target)
        written += 1

    (OUT_DIR / "404.html").write_text(FOUR_O_FOUR, encoding="utf-8")
    (OUT_DIR / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://3cucharadas.cl/sitemap.xml\n",
        encoding="utf-8",
    )
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    if (OUT_DIR / "CNAME").exists():
        raise SystemExit("No se debe generar CNAME para GitHub Pages.")

    print(f"Redirector generado en {OUT_DIR} con {written} paginas.")


if __name__ == "__main__":
    main()
