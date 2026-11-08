#!/usr/bin/env python3
"""Registro de enlaces para referencias científicas de los posts.

Decisión editorial del 2026-10-31: el título de cada referencia científica enlaza a
un PDF legal verificado o, si no lo hay, a su DOI (o al PDF de arXiv), y Google
Scholar queda como enlace secundario. Scholar no se valida en automático: sus
condiciones prohíben las consultas automatizadas y su página de bloqueo responde
200, así que un 200 no prueba nada. Lo que sí se valida aquí:

- que el DOI corresponda al título citado (OpenAlex o arXiv), y
- que el PDF sea el artículo: 200, firma %PDF y, extraído con pdftotext, que sus
  primeras páginas contengan al menos el 70 % de las palabras del título oficial.
  Un PDF que abre pero es otro documento (portada de repositorio, otro artículo
  del mismo número) no pasa.

Uso:
  scripts/build_reference_links.py [--posts _posts] [--out _data/referencias_enlaces.yml]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import tempfile
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

DOI_RE = re.compile(r"doi\.org/(10\.\d{4,9}/(?:[^\s()>\]{}\"'<]|\([^\s()>\]{}\"'<]*\))+)", re.I)
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
UA = "3cucharadas-reference-links/1.0 (+https://3cucharadas.cl)"


def clean_doi(doi: str) -> str:
    return doi.rstrip(".,;:").strip()


REF_HEAD = re.compile(
    r"^#{2,4}\s+(Referencias|References|Fuentes|Sources|Lectura complementaria|Further reading|"
    r"Software y documentaci|Software and (technical )?documentation|Bibliograf|Bibliography)",
    re.I,
)
ANY_HEAD = re.compile(r"^#{1,4}\s")


def entry_lines(text: str) -> list[str]:
    """Líneas de referencias: bajo un encabezado de referencias (y sus subencabezados)
    o definiciones de nota `[^x]:`. Misma regla que scripts/verify_reference_links.rb:
    el registro solo cuenta identificadores de entradas, no citas del cuerpo."""

    ref_level = 0
    lines = []
    for line in text.splitlines():
        if ANY_HEAD.match(line):
            level = len(line) - len(line.lstrip("#"))
            if REF_HEAD.match(line):
                ref_level = ref_level if ref_level and level > ref_level else level
            elif not ref_level or level <= ref_level:
                ref_level = 0
        if line.startswith("|"):
            continue
        if ref_level or line.startswith("[^"):
            lines.append(line)
    return lines


def collect_identifiers(posts_dir: Path) -> dict[str, dict]:
    """Identificadores por post, con las líneas que los citan (texto, no número de línea:
    los números cambian con cada edición y el registro no debe depender de ellos)."""

    found: dict[str, dict] = {}
    annexes = [posts_dir.parent / "_pages" / f"tesis-post{part}-anexo-metodologico{lang}.md"
               for part in (3, 4) for lang in ("", "-en")]
    for path in sorted([*posts_dir.glob("*.md"), *(p for p in annexes if p.is_file())]):
        for line in entry_lines(path.read_text(encoding="utf-8")):
            dois = [clean_doi(match.group(1)) for match in DOI_RE.finditer(line)]
            for doi in dois:
                key = "doi:" + doi.lower()
                found.setdefault(key, {"kind": "doi", "id": doi, "seen": set(), "lines": []})
                found[key]["seen"].add(path.name)
                found[key]["lines"].append(line)
            for match in ARXIV_RE.finditer(line):
                # Un PDF de arXiv al lado de un DOI es la versión abierta de ese DOI,
                # no otra referencia.
                if dois and "/pdf/" in match.group(0):
                    continue
                key = "arxiv:" + match.group(1)
                found.setdefault(key, {"kind": "arxiv", "id": match.group(1), "seen": set(), "lines": []})
                found[key]["seen"].add(path.name)
                found[key]["lines"].append(line)
    return found


def http_json(url: str) -> dict | None:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def http_text(url: str) -> str | None:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError):
        return None


PDF_MAX_BYTES = 60 * 1024 * 1024
PDF_TITLE_MIN = 0.7


def fetch_url(url: str) -> str:
    """URL desde la que se descarga para verificar. arXiv pide usar su espejo export."""

    return re.sub(r"^https://arxiv\.org/pdf/", "https://export.arxiv.org/pdf/", url)


def pdf_title_ratio(url: str, title: str) -> float:
    """Proporción de palabras del título presentes en las dos primeras páginas del PDF.

    0.0 si no responde 200, si no es un PDF o si pdftotext no extrae texto.
    """

    request = urllib.request.Request(fetch_url(url), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status != 200:
                return 0.0
            body = response.read(PDF_MAX_BYTES + 1)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return 0.0
    if b"%PDF" not in body[:1024] or len(body) > PDF_MAX_BYTES:
        return 0.0
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "doc.pdf"
        pdf.write_bytes(body)
        result = subprocess.run(
            ["pdftotext", "-q", "-l", "2", str(pdf), "-"],
            capture_output=True, text=True, timeout=60, check=False,
        )
    wanted = normalize(title)
    if not wanted or not result.stdout:
        return 0.0
    tokens = normalize(result.stdout)
    # Los títulos en versalitas salen partidos de pdftotext («H INDSIGHT»): una palabra
    # de 5+ letras también cuenta si aparece en el texto sin espacios.
    compact = re.sub(r"[^a-z0-9]", "", " ".join(sorted(tokens)) + " " + _flat(result.stdout))
    hits = sum(1 for word in wanted if word in tokens or (len(word) >= 5 and word in compact))
    return round(hits / len(wanted), 2)


def _flat(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower())


def openalex(doi: str) -> dict:
    data = http_json("https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe="/"))
    if not data:
        return {"source": "openalex", "found": False}
    candidates: list[str] = []
    best = data.get("best_oa_location") or {}
    if best.get("pdf_url"):
        candidates.append(best["pdf_url"])
    for location in data.get("locations") or []:
        if location.get("is_oa") and location.get("pdf_url") and location["pdf_url"] not in candidates:
            candidates.append(location["pdf_url"])
    return {
        "source": "openalex",
        "found": True,
        "title": data.get("display_name") or "",
        "year": data.get("publication_year"),
        "pdf_candidates": candidates,
    }


def arxiv(identifier: str) -> dict:
    text = http_text("https://export.arxiv.org/api/query?id_list=" + identifier)
    title = ""
    if text:
        match = re.search(r"<entry>.*?<title>(.*?)</title>", text, flags=re.S)
        if match:
            title = " ".join(match.group(1).split())
    return {
        "source": "arxiv",
        "found": bool(title),
        "title": title,
        "year": int("20" + identifier[:2]) if identifier[:2].isdigit() else None,
        "pdf_candidates": [f"https://arxiv.org/pdf/{identifier}"],
    }


def scholar_url(title: str, doi: str | None) -> str:
    params = {"title": title}
    if doi:
        params["doi"] = doi
    return "https://scholar.google.com/scholar_lookup?" + urllib.parse.urlencode(params)


def normalize(text: str) -> set[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return {token for token in re.findall(r"[a-z0-9]+", text) if len(token) > 2}


def title_in_lines(title: str, lines: list[str]) -> float:
    """Proporción de palabras del título oficial presentes en la línea que lo cita."""

    wanted = normalize(title)
    if not wanted:
        return 0.0
    return round(max(len(wanted & normalize(line)) / len(wanted) for line in lines), 2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts", type=Path, default=Path("_posts"))
    parser.add_argument("--out", type=Path, default=Path("_data/referencias_enlaces.yml"))
    parser.add_argument("--refresh", action="store_true", help="Re-query all identifiers instead of reusing existing entries")
    args = parser.parse_args()

    existing: dict[str, dict] = {}
    if not args.refresh and args.out.exists():
        loaded = yaml.safe_load(args.out.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            existing = loaded

    identifiers = collect_identifiers(args.posts)
    registry: dict[str, dict] = {}
    for key, item in sorted(identifiers.items()):
        if key in existing and existing[key].get("metadata_found"):
            cached = dict(existing[key])
            title = cached.get("title") or ""
            cached["seen"] = sorted(item["seen"])
            cached["title_match"] = title_in_lines(title, item["lines"]) if title else 0.0
            registry[key] = cached
            continue
        meta = openalex(item["id"]) if item["kind"] == "doi" else arxiv(item["id"])
        title = meta.get("title", "")
        pdf_url, pdf_match, rejected = None, 0.0, []
        for candidate in meta.get("pdf_candidates", []):
            ratio = pdf_title_ratio(candidate, title) if title else 0.0
            time.sleep(1.0)
            if ratio >= PDF_TITLE_MIN:
                pdf_url, pdf_match = candidate, ratio
                break
            rejected.append({"url": candidate, "title_match": ratio})
        match = title_in_lines(title, item["lines"]) if title else 0.0
        registry[key] = {
            "kind": item["kind"],
            "id": item["id"],
            "doi_url": f"https://doi.org/{item['id']}" if item["kind"] == "doi" else None,
            "arxiv_abs": f"https://arxiv.org/abs/{item['id']}" if item["kind"] == "arxiv" else None,
            "metadata_source": meta["source"],
            "metadata_found": meta["found"],
            "title": title,
            "year": meta.get("year"),
            "title_match": match,
            "pdf_url": pdf_url,
            "pdf_verified": bool(pdf_url),
            "pdf_title_match": pdf_match,
            "pdf_rejected": rejected,
            "scholar_url": scholar_url(title, item["id"] if item["kind"] == "doi" else None) if title else None,
            "seen": sorted(item["seen"]),
            "checked_at": dt.date.today().isoformat(),
        }
        time.sleep(0.2)
    args.out.write_text(
        "# Generado por scripts/build_reference_links.py. No editar a mano: volver a correr.\n"
        + yaml.safe_dump(registry, allow_unicode=True, sort_keys=True, width=1000),
        encoding="utf-8",
    )
    total = len(registry)
    pdfs = sum(1 for value in registry.values() if value["pdf_verified"])
    weak = [key for key, value in registry.items() if value["title_match"] < 0.6]
    print(f"OK {total} identificadores; {pdfs} con PDF verificado; {len(weak)} con título a revisar")
    for key in weak:
        print("REVISAR", key, registry[key]["title_match"], registry[key]["title"][:80])
    return 0


if __name__ == "__main__":
    sys.exit(main())
