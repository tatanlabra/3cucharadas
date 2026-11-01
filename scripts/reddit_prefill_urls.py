#!/usr/bin/env python3
"""Arma el formulario de envío de Reddit ya lleno para cada hilo de un paquete de difusión.

Reddit bloquea su API y los navegadores automatizados ("blocked by network security"),
así que este script no publica: genera la URL de old.reddit con título y texto
prellenados (`/r/<sub>/submit?selftext=true&title=…&text=…`) y, con --open, la abre en
el navegador habitual de la persona, donde ya tiene su sesión. La persona revisa las
reglas de la barra lateral y aprieta Submit. Verificado el 2026-11-01 con r/PublicPolicy
y r/latinoamerica (Post III de la tesis).

Lee `difusion/paquetes/<ref>/reddit-hilos.md`: cada sección `## r/<sub>` con
`**Título:**` y `**Texto:**` en una línea cada uno. Una sección sin `**Texto:**` (por
ejemplo r/dataisbeautiful, que va como envío de enlace con primer comentario de fuentes)
se informa y se omite: este script solo prellena posts de texto.

Uso:
  scripts/reddit_prefill_urls.py <ref> [--sub NOMBRE ...] [--open]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTION = re.compile(r"^## r/([A-Za-z0-9_]+)[^\n]*\n(.*?)(?=^## |\Z)", re.M | re.S)
TITLE = re.compile(r"^\*\*T[ií]tulo:\*\* (.+)$", re.M)
BODY = re.compile(r"^\*\*Texto:\*\* (.+)$", re.M)


def threads(path: Path) -> list[tuple[str, str | None, str | None]]:
    text = path.read_text(encoding="utf-8")
    out = []
    for sub, block in SECTION.findall(text):
        title, body = TITLE.search(block), BODY.search(block)
        out.append((sub, title.group(1).strip() if title else None, body.group(1).strip() if body else None))
    return out


def submit_url(sub: str, title: str, body: str) -> str:
    query = urllib.parse.urlencode({"selftext": "true", "title": title, "text": body}, quote_via=urllib.parse.quote)
    return f"https://old.reddit.com/r/{sub}/submit?{query}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref")
    ap.add_argument("--sub", action="append", default=[], help="limitar a estos subreddits (sin r/)")
    ap.add_argument("--open", action="store_true", help="abrir cada formulario con xdg-open")
    args = ap.parse_args(argv)

    path = ROOT / "difusion" / "paquetes" / args.ref / "reddit-hilos.md"
    if not path.is_file():
        print(f"No existe {path.relative_to(ROOT)}", file=sys.stderr)
        return 2
    wanted = {s.lower().removeprefix("r/") for s in args.sub}
    found = [t for t in threads(path) if not wanted or t[0].lower() in wanted]
    if wanted and {t[0].lower() for t in found} != wanted:
        print(f"Subreddits sin sección en el paquete: {sorted(wanted - {t[0].lower() for t in found})}", file=sys.stderr)
        return 1
    urls = 0
    for sub, title, body in found:
        if not title or not body:
            print(f"OMITIDO r/{sub}: sin **Título:** y **Texto:** de una línea (envío de enlace o imagen: va a mano)")
            continue
        if len(title) > 300:
            print(f"ERROR r/{sub}: el título tiene {len(title)} caracteres y Reddit admite 300", file=sys.stderr)
            return 1
        url = submit_url(sub, title, body)
        print(f"r/{sub}\t{url}")
        urls += 1
        if args.open:
            subprocess.run(["xdg-open", url], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
    return 0 if urls else 1


if __name__ == "__main__":
    raise SystemExit(main())
