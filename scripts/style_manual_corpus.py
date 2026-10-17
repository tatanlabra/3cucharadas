#!/usr/bin/env python3
"""Build and query a private, local corpus from editorial-style manuals.

The builder prefers Docling when it is installed and falls back explicitly to
pdftotext.  Extracted manual text is written only to the caller's output
directory; it must not be committed to the public site.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable


WORD_RE = re.compile(r"[\wáéíóúüñÁÉÍÓÚÜÑ'-]+", re.UNICODE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalise(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def chunk_pages(
    pages: Iterable[str], target_words: int = 1_200, overlap_words: int = 120
) -> list[dict[str, object]]:
    if target_words < 100 or overlap_words < 0 or overlap_words >= target_words:
        raise ValueError("invalid chunk or overlap size")

    chunks: list[dict[str, object]] = []
    pending: list[str] = []
    page_start = 1
    page_end = 1

    for page_number, page in enumerate(pages, start=1):
        words = normalise(page).split()
        if not words:
            continue
        if not pending:
            page_start = page_number
        pending.extend(words)
        page_end = page_number
        while len(pending) >= target_words:
            body = pending[:target_words]
            chunks.append(
                {
                    "page_start": page_start,
                    "page_end": page_end,
                    "text": " ".join(body),
                }
            )
            pending = pending[target_words - overlap_words :]
            page_start = page_number

    if pending:
        chunks.append(
            {
                "page_start": page_start,
                "page_end": page_end,
                "text": " ".join(pending),
            }
        )
    return chunks


def extract_docling(pdf: Path) -> list[str]:
    from docling.document_converter import DocumentConverter  # type: ignore

    result = DocumentConverter().convert(str(pdf))
    return [result.document.export_to_markdown()]


def extract_pdftotext(pdf: Path) -> list[str]:
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("pdftotext is not installed")
    with tempfile.TemporaryDirectory(prefix="style-manual-") as directory:
        output = Path(directory) / "manual.txt"
        completed = subprocess.run(
            [executable, "-layout", "-enc", "UTF-8", str(pdf), str(output)],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "pdftotext failed")
        return output.read_text(encoding="utf-8", errors="replace").split("\f")


def choose_backend(requested: str) -> str:
    if requested == "pdftotext":
        if not shutil.which("pdftotext"):
            raise RuntimeError("pdftotext is not installed")
        return requested
    try:
        __import__("docling.document_converter")
        return "docling"
    except ImportError:
        if requested == "docling":
            raise RuntimeError("Docling was requested but is not installed")
        if shutil.which("pdftotext"):
            return "pdftotext"
        raise RuntimeError("neither Docling nor pdftotext is available")


def repository_root(path: Path) -> Path | None:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    return Path(completed.stdout.strip()).resolve() if completed.returncode == 0 else None


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def build(args: argparse.Namespace) -> int:
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()
    project_root = repository_root(Path(__file__).resolve().parent)
    if project_root and path_is_within(output_dir, project_root):
        print(f"refusing to write copyrighted corpus inside repository: {output_dir}", file=sys.stderr)
        return 2
    pdfs = sorted(source_dir.glob("*.pdf"), key=lambda path: path.name.casefold())
    if not pdfs:
        print(f"no PDF manuals found in {source_dir}", file=sys.stderr)
        return 2
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        print(f"output directory is not empty: {output_dir}", file=sys.stderr)
        return 2

    backend = choose_backend(args.backend)
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "chunks.jsonl"
    manuals: list[dict[str, object]] = []
    chunk_count = 0

    with chunks_path.open("w", encoding="utf-8") as stream:
        for manual_index, pdf in enumerate(pdfs, start=1):
            pages = extract_docling(pdf) if backend == "docling" else extract_pdftotext(pdf)
            chunks = chunk_pages(pages, args.chunk_words, args.overlap_words)
            if backend == "docling":
                for chunk in chunks:
                    chunk["page_start"] = None
                    chunk["page_end"] = None
            source_id = f"manual-{manual_index:02d}"
            for sequence, chunk in enumerate(chunks, start=1):
                record = {
                    "id": f"{source_id}-chunk-{sequence:04d}",
                    "source_id": source_id,
                    "source_file": pdf.name,
                    **chunk,
                }
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            chunk_count += len(chunks)
            manuals.append(
                {
                    "source_id": source_id,
                    "source_file": pdf.name,
                    "sha256": sha256(pdf),
                    "chunks": len(chunks),
                }
            )

    manifest = {
        "schema": "style-manual-corpus-v1",
        "backend": backend,
        "backend_requested": args.backend,
        "docling_preferred": True,
        "fallback_used": args.backend == "auto" and backend != "docling",
        "chunk_words": args.chunk_words,
        "overlap_words": args.overlap_words,
        "manuals": manuals,
        "chunks": chunk_count,
        "copyright_boundary": "local private corpus; extracted text is not a public-site asset",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


def tokens(text: str) -> list[str]:
    return [token.casefold() for token in WORD_RE.findall(text) if len(token) > 2]


def search(args: argparse.Namespace) -> int:
    records = [json.loads(line) for line in args.corpus.read_text(encoding="utf-8").splitlines()]
    if not records:
        print("corpus has no records", file=sys.stderr)
        return 2
    documents = [Counter(tokens(record["text"])) for record in records]
    query = Counter(tokens(args.query))
    if not query:
        print("query has no searchable terms", file=sys.stderr)
        return 2
    document_frequency = Counter(
        token for document in documents for token in document if token in query
    )
    scored: list[tuple[float, dict[str, object]]] = []
    for record, document in zip(records, documents):
        score = 0.0
        for token, query_count in query.items():
            if document[token]:
                inverse_frequency = math.log((len(records) + 1) / (document_frequency[token] + 1)) + 1
                score += (1 + math.log(document[token])) * inverse_frequency * query_count
        if score:
            scored.append((score, record))
    for score, record in sorted(scored, key=lambda item: item[0], reverse=True)[: args.limit]:
        result = {key: record[key] for key in ("id", "source_file", "page_start", "page_end")}
        result["score"] = round(score, 4)
        result["excerpt"] = " ".join(str(record["text"]).split()[:80])
        print(json.dumps(result, ensure_ascii=False))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="extract manuals into a local JSONL corpus")
    build_parser.add_argument("--source-dir", type=Path, required=True)
    build_parser.add_argument("--output-dir", type=Path, required=True)
    build_parser.add_argument("--backend", choices=("auto", "docling", "pdftotext"), default="auto")
    build_parser.add_argument("--chunk-words", type=int, default=1_200)
    build_parser.add_argument("--overlap-words", type=int, default=120)
    build_parser.add_argument("--force", action="store_true")
    build_parser.set_defaults(handler=build)

    search_parser = commands.add_parser("search", help="rank corpus chunks for a plain-text query")
    search_parser.add_argument("--corpus", type=Path, required=True)
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--limit", type=int, default=5)
    search_parser.set_defaults(handler=search)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, RuntimeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
