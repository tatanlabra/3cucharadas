#!/usr/bin/env python3
"""One-time script: builds assets/feed_descriptions.json from OPML.

PASADA 1 — Fetches channel-level <description>/<subtitle> from each RSS feed (parallel).
PASADA 2 — Calls Gemini CLI in batch for feeds still empty after pasada 1.

Re-runnable: feeds already in the output file are skipped (incremental).
Output: assets/feed_descriptions.json  {xmlUrl: description, ...}
"""

import json
import re
import shutil
import socket
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import feedparser
except ImportError:
    sys.exit("Missing: pip install feedparser")

ROOT = Path(__file__).resolve().parents[1]
OPML_FILE = ROOT / "assets" / "feedly-subscriptions.opml"
OUTPUT_FILE = ROOT / "assets" / "feed_descriptions.json"
FETCH_WORKERS = 12
FETCH_TIMEOUT = 8
GEMINI_BATCH_SIZE = 50  # feeds per Gemini call to stay within context


# ── OPML ─────────────────────────────────────────────────────────────────────

def parse_opml_flat(path: Path) -> list[dict]:
    """Return flat list of {url, title, htmlUrl, category} for all RSS outlines."""
    tree = ET.parse(path)
    body = tree.getroot().find("body")
    if body is None:
        return []
    feeds = []
    for cat_node in body.findall("outline"):
        cat = cat_node.get("title") or cat_node.get("text") or "sin categoría"
        for feed_node in cat_node.findall("outline"):
            xml_url = feed_node.get("xmlUrl", "").strip()
            if xml_url and feed_node.get("type") == "rss":
                feeds.append({
                    "url": xml_url,
                    "title": feed_node.get("title") or feed_node.get("text") or xml_url,
                    "htmlUrl": feed_node.get("htmlUrl", ""),
                    "category": cat,
                })
    return feeds


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean(text: str, max_len: int = 150) -> str:
    clean = re.sub(r"<[^>]+>", "", text or "")
    return " ".join(clean.split())[:max_len].rstrip()


# ── Pasada 1: RSS channel metadata ────────────────────────────────────────────

def _fetch_channel_desc(feed: dict) -> tuple[str, str]:
    """Return (url, description). Description may be empty string on failure."""
    url = feed["url"]
    try:
        parsed = feedparser.parse(
            url,
            request_headers={"User-Agent": "3cucharadas-bot/1.0 (+https://tatanlabra.gitlab.io/3cucharadas)"},
        )
        f = parsed.get("feed", {})
        desc = _clean(f.get("description", "") or f.get("subtitle", ""))
        return url, desc
    except Exception:
        return url, ""


def fetch_all_channel_descs(feeds: list[dict]) -> dict[str, str]:
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
        futures = {pool.submit(_fetch_channel_desc, f): f for f in feeds}
        done = 0
        for future in as_completed(futures):
            url, desc = future.result()
            results[url] = desc
            done += 1
            status = "OK" if desc else "--"
            title = futures[future]["title"]
            print(f"  [{status}] ({done:3}/{len(feeds)}) {title[:55]}")
    return results


# ── Pasada 2: Gemini CLI ──────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> str:
    result = subprocess.run(
        ["gemini", "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    return result.stdout.strip()


def enrich_with_gemini(empty_feeds: list[dict]) -> dict[str, str]:
    """Call Gemini CLI in batch for feeds without description. Returns {url: desc}."""
    if not shutil.which("gemini"):
        print("  [Gemini] CLI no disponible — saltando pasada 2", file=sys.stderr)
        return {}

    all_results: dict[str, str] = {}
    for i in range(0, len(empty_feeds), GEMINI_BATCH_SIZE):
        chunk = empty_feeds[i:i + GEMINI_BATCH_SIZE]
        batch_num = i // GEMINI_BATCH_SIZE + 1
        print(f"  [Gemini] Lote {batch_num}: {len(chunk)} feeds…")

        payload = json.dumps(
            [{"url": f["url"], "title": f["title"], "site": f["htmlUrl"]} for f in chunk],
            ensure_ascii=False,
        )
        prompt = (
            "Para cada feed RSS de la siguiente lista, escribe UNA descripción breve "
            "en español (máximo 120 caracteres) sobre qué tipo de contenido publica. "
            "Responde ÚNICAMENTE con un objeto JSON válido donde las claves son los "
            "valores de \"url\" y los valores son las descripciones. "
            "Sin texto adicional, sin bloques markdown, solo el JSON puro.\n\n"
            + payload
        )

        try:
            output = _call_gemini(prompt)
            json_match = re.search(r"\{.*\}", output, re.DOTALL)
            if not json_match:
                print(f"  [Gemini] No se encontró JSON en la respuesta del lote {batch_num}", file=sys.stderr)
                continue
            parsed = json.loads(json_match.group())
            batch_results = {k: _clean(v) for k, v in parsed.items() if isinstance(v, str) and v.strip()}
            all_results.update(batch_results)
            print(f"  [Gemini] Lote {batch_num}: {len(batch_results)} descripciones obtenidas")
        except subprocess.TimeoutExpired:
            print(f"  [Gemini] Timeout en lote {batch_num}", file=sys.stderr)
        except json.JSONDecodeError as exc:
            print(f"  [Gemini] JSON inválido en lote {batch_num}: {exc}", file=sys.stderr)
        except Exception as exc:
            print(f"  [Gemini] Error en lote {batch_num}: {exc}", file=sys.stderr)

    return all_results


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not OPML_FILE.exists():
        sys.exit(f"OPML no encontrado: {OPML_FILE}")

    feeds = parse_opml_flat(OPML_FILE)
    print(f"OPML: {len(feeds)} feeds en total")

    # Reutilizar tabla existente (incremental)
    existing: dict[str, str] = {}
    if OUTPUT_FILE.exists():
        existing = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        print(f"Tabla existente: {len(existing)} entradas reutilizadas")

    to_fetch = [f for f in feeds if f["url"] not in existing]
    print(f"\nPasada 1: {len(to_fetch)} feeds nuevos a fetchear ({FETCH_WORKERS} workers)…")

    socket.setdefaulttimeout(FETCH_TIMEOUT)
    descriptions: dict[str, str] = dict(existing)

    if to_fetch:
        new_descs = fetch_all_channel_descs(to_fetch)
        descriptions.update(new_descs)

    with_desc_p1 = sum(1 for f in to_fetch if descriptions.get(f["url"]))
    print(f"\nPasada 1 completa: {with_desc_p1}/{len(to_fetch)} nuevos con descripción RSS")

    # Pasada 2: Gemini para feeds aún vacíos (todos los feeds del OPML)
    all_empty = [f for f in feeds if not descriptions.get(f["url"])]
    if all_empty:
        print(f"\nPasada 2: Gemini CLI para {len(all_empty)} feeds sin descripción…")
        gemini_descs = enrich_with_gemini(all_empty)
        descriptions.update(gemini_descs)
        still_empty = sum(1 for f in feeds if not descriptions.get(f["url"]))
        print(f"Gemini añadió {len(gemini_descs)} descripciones. Aún vacíos: {still_empty}")
    else:
        print("\nPasada 2: no hay feeds vacíos, Gemini no necesario")

    # Guardar
    OUTPUT_FILE.write_text(
        json.dumps(descriptions, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    total_filled = sum(1 for d in descriptions.values() if d)
    print(f"\nGuardado: {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"  {total_filled}/{len(descriptions)} entradas con descripción")
    if len(descriptions) - total_filled:
        print(f"  {len(descriptions) - total_filled} entradas aún vacías → edición manual en {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
