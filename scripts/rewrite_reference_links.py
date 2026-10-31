#!/usr/bin/env python3
"""Reescribe los enlaces de las referencias científicas según _data/referencias_enlaces.yml.

Regla editorial (2026-10-31): el título de la referencia enlaza al PDF legal cuyo
contenido se verificó (scripts/build_reference_links.py) o, si no lo hay, al DOI. La
entrada termina con los enlaces secundarios: [DOI] o [arXiv] cuando el título apunta al
PDF, y siempre [Scholar]. Si la entrada no tiene un título enlazable, todos van al final:
[PDF] · [DOI] · [Scholar].

Solo toca entradas de referencias: líneas bajo un encabezado de referencias o
definiciones de nota `[^x]:`. Las citas del cuerpo quedan para la conversión a notas.
Una entrada con más de un identificador distinto no se toca y se informa.

Uso:
  scripts/rewrite_reference_links.py [--write] [archivo.md ...]
Sin --write muestra el diff y no escribe. Sin archivos, recorre _posts/*.md.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

import yaml

REF_HEAD = re.compile(
    r"^#{2,4}\s+(Referencias|References|Fuentes|Sources|Lectura complementaria|Further reading|"
    r"Software y documentaci|Software and (technical )?documentation|Bibliograf|Bibliography)",
    re.I,
)
ANY_HEAD = re.compile(r"^#{1,4}\s")
DOI_URL = r"https?://(?:dx\.)?doi\.org/(10\.\d{4,9}/[^\s)>\]\"'<]+)"
ARXIV_URL = r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?"
ID_RE = re.compile(f"{DOI_URL}|{ARXIV_URL}", re.I)
SCHOLAR = "scholar.google.com/scholar_lookup"
QUOTED = re.compile(r"(“[^”]{12,}”|«[^»]{12,}»|\"[^\"]{12,}\")")


def clean_doi(doi: str) -> str:
    return doi.rstrip(".,;:").strip()


def identifiers(line: str) -> set[str]:
    """DOI y arXiv de la línea. Un PDF de arXiv junto a un DOI es la versión abierta
    de ese DOI, no otra referencia (misma regla que build_reference_links.py)."""

    found = set()
    matches = list(ID_RE.finditer(line))
    has_doi = any(match.group(1) for match in matches)
    for match in matches:
        if match.group(1):
            found.add("doi:" + clean_doi(match.group(1)).lower())
        elif not (has_doi and "/pdf/" in match.group(0)):
            found.add("arxiv:" + match.group(2))
    return found


def url_pattern(entry: dict) -> str:
    if entry["kind"] == "doi":
        return r"https?://(?:dx\.)?doi\.org/" + re.escape(entry["id"]) + r"(?=[\s)>\].,;:]|$)"
    return r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/" + re.escape(entry["id"]) + r"(?:v\d+)?"


ID_TEXT = re.compile(r"^\s*(?:doi:?\s*)?10\.\d|^\s*https?:|^\s*(?:DOI|arXiv)\s*$|^\s*arXiv:", re.I)
ITALIC = re.compile(r"(?<![\[\w*])\*([^*\n]{12,}?)\*(?!\*)")


def rewrite_entry(line: str, entry: dict) -> str:
    pattern = url_pattern(entry)
    canonical = entry["doi_url"] if entry["kind"] == "doi" else entry["arxiv_abs"]
    label = "DOI" if entry["kind"] == "doi" else "arXiv"
    pdf = entry["pdf_url"] if entry.get("pdf_verified") else None
    primary = pdf or canonical

    text = line
    # Autoenlaces y URL desnudas del identificador: se reemplazan por los enlaces
    # finales. Solo se borran cuando cierran la entrada o van solos entre paréntesis;
    # dentro de la prosa («verificable en <https://doi.org/…>») el borrado dejaría
    # la frase trunca, así que ahí se convierten en un enlace [DOI] en su lugar.
    text = re.sub(r"\s*\(\s*<" + pattern + r">\s*\)", "", text, flags=re.I)
    inline = re.compile(r"(?<=\w)\s+<" + pattern + r">(?=\s*[),;:]|\s+\w)", re.I)
    text = inline.sub(lambda m: f" [{label}]({canonical})", text)
    text = re.sub(r"\s*<" + pattern + r">", "", text, flags=re.I)
    text = re.sub(r"(?<![(<\[])\s*\b" + pattern, "", text, flags=re.I)

    # Enlaces Markdown al identificador. Si su texto es el propio DOI («10.4067/…»,
    # «DOI», una URL), es el enlace canónico y conserva su destino; si es un título,
    # pasa a apuntar al destino primario (PDF verificado o DOI).
    titled = 0
    canonical_kept = False

    def retarget(match: re.Match) -> str:
        nonlocal titled, canonical_kept
        if ID_TEXT.search(match.group(1)):
            canonical_kept = True
            return f"[{match.group(1)}]({canonical})"
        titled += 1
        return f"[{match.group(1)}]({primary})"

    text = re.sub(r"\[([^\]]+)\]\(" + pattern + r"\)", retarget, text, flags=re.I)
    if not titled:
        for finder in (QUOTED, ITALIC):
            match = finder.search(text)
            if match:
                text = text[: match.start()] + f"[{match.group(0)}]({primary})" + text[match.end():]
                titled = 1
                break
    text = re.sub(r"\.\s*\.(\s|$)", r".\1", text).rstrip()
    text = re.sub(r"\s+\.$", ".", text)

    extras: list[str] = []
    if not titled and pdf:
        extras.append(f"[PDF]({pdf})")
    if not canonical_kept and (primary != canonical or not titled):
        extras.append(f"[{label}]({canonical})")
    if entry.get("scholar_url"):
        extras.append(f"[Scholar]({entry['scholar_url']})")
    if not text.endswith((".", ")")):
        text += "."
    return text + " " + " · ".join(extras)


def process(path: Path, registry: dict, report: list[str]) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    ref_level = 0  # nivel del encabezado de referencias vigente; 0 = fuera
    out: list[str] = []
    for number, raw in enumerate(lines, 1):
        body = raw.rstrip("\n")
        head = ANY_HEAD.match(body)
        if head:
            level = len(body) - len(body.lstrip("#"))
            if REF_HEAD.match(body):
                ref_level = ref_level if ref_level and level > ref_level else level
            elif not ref_level or level <= ref_level:
                ref_level = 0
        in_refs = bool(ref_level)
        is_entry = in_refs or body.startswith("[^")
        ids = identifiers(body)
        if not ids or not is_entry or body.startswith("|"):
            out.append(raw)
            continue
        if SCHOLAR in body:
            out.append(raw)
            continue
        if len(ids) > 1:
            report.append(f"OMITIDA {path.name}:{number}: {len(ids)} identificadores {sorted(ids)}")
            out.append(raw)
            continue
        key = next(iter(ids))
        entry = registry.get(key)
        if not entry:
            report.append(f"SIN_REGISTRO {path.name}:{number}: {key}")
            out.append(raw)
            continue
        out.append(rewrite_entry(body, entry) + ("\n" if raw.endswith("\n") else ""))
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--registry", type=Path, default=Path("_data/referencias_enlaces.yml"))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    registry = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    files = args.files or sorted(Path("_posts").glob("*.md"))
    report: list[str] = []
    changed = 0
    for path in files:
        before = path.read_text(encoding="utf-8")
        after = process(path, registry, report)
        if after == before:
            continue
        changed += 1
        if args.write:
            path.write_text(after, encoding="utf-8")
        else:
            sys.stdout.writelines(
                difflib.unified_diff(
                    before.splitlines(keepends=True), after.splitlines(keepends=True),
                    fromfile=str(path), tofile=str(path), n=0,
                )
            )
    for line in report:
        print(line, file=sys.stderr)
    print(f"{'ESCRITOS' if args.write else 'CAMBIARÍAN'} {changed} archivos; {len(report)} avisos", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
