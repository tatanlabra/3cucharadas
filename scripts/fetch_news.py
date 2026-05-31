#!/usr/bin/env python3
"""Fetches 6 random RSS feeds from the personal OPML (assets/feedly-subscriptions.opml).

Selection strategy:
- Seeded with Santiago day (`America/Santiago`) -> same 6 feeds all day, different every day
- Stratified: 1 feed per OPML category, extras fill remaining slots
- Resilient: skips dead/slow feeds (6s timeout), with per-slot + global fallback budgets

Output: _data/feedly_news.json  (read by _includes/news-widget.html)
"""

import json
import os
import random
import re
import socket
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import feedparser
except ImportError:
    sys.exit("Missing dependency: pip install feedparser")

ROOT = Path(__file__).resolve().parents[1]
OPML_FILE = ROOT / "assets" / "feedly-subscriptions.opml"
OUTPUT_FILE = ROOT / "_data" / "feedly_news.json"
TARGET_COUNT = 6
SOCKET_TIMEOUT = 6                  # seconds per feed request
MAX_ATTEMPTS_PER_SLOT = 4           # tries before giving up on a category slot
MAX_GLOBAL_FALLBACK_ATTEMPTS = 64   # tries to complete missing slots from global pool
MAX_ARTICLE_AGE_DAYS = 60           # skip articles older than this
LOCAL_TZ = ZoneInfo("America/Santiago")


# ── OPML parsing ─────────────────────────────────────────────────────────────

def parse_opml(path: Path) -> dict[str, list[dict]]:
    """Return {category: [{url, title}, ...]} from an OPML file."""
    tree = ET.parse(path)
    body = tree.getroot().find("body")
    if body is None:
        return {}
    feeds_by_cat: dict[str, list[dict]] = {}
    for cat_node in body.findall("outline"):
        cat_name = cat_node.get("title") or cat_node.get("text") or "sin categoría"
        items = []
        for feed_node in cat_node.findall("outline"):
            xml_url = feed_node.get("xmlUrl", "").strip()
            if xml_url and feed_node.get("type") == "rss":
                items.append({
                    "url": xml_url,
                    "title": feed_node.get("title") or feed_node.get("text") or xml_url,
                })
        if items:
            feeds_by_cat[cat_name] = items
    return feeds_by_cat


# ── Stratified daily-seeded sampling ─────────────────────────────────────────

def stratified_sample(feeds_by_cat: dict, n: int, rng: random.Random) -> tuple[list[dict], list[dict]]:
    """Pick up to n feeds with per-category pools plus a global fallback pool."""
    categories = list(feeds_by_cat.keys())
    rng.shuffle(categories)

    selected: list[dict] = []
    selected_urls: set[str] = set()
    # Round 1: one random feed per category
    for cat in categories:
        pool = list(feeds_by_cat[cat])
        rng.shuffle(pool)
        feed = pool[0]
        selected.append({**feed, "category": cat, "_pool": pool[1:]})
        selected_urls.add(feed["url"])
        if len(selected) >= n:
            break

    # Round 2: fill remaining slots with extras from any category
    if len(selected) < n:
        extras: list[dict] = []
        for cat in categories:
            for feed in feeds_by_cat[cat]:
                if not any(s["url"] == feed["url"] for s in selected):
                    extras.append({**feed, "category": cat})
        rng.shuffle(extras)
        for feed in extras:
            if len(selected) >= n:
                break
            selected.append({**feed, "_pool": []})
            selected_urls.add(feed["url"])

    global_pool: list[dict] = []
    for cat in categories:
        for feed in feeds_by_cat[cat]:
            if feed["url"] in selected_urls:
                continue
            global_pool.append({**feed, "category": cat})
    rng.shuffle(global_pool)

    return selected, global_pool


# ── RSS fetching ──────────────────────────────────────────────────────────────

def _parse_date(entry: dict) -> tuple[datetime | None, bool]:
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc), True
            except Exception:
                pass
    return None, False


def _clean(text: str, max_len: int = 200) -> str:
    clean = re.sub(r"<[^>]+>", "", text or "")
    return " ".join(clean.split())[:max_len].rstrip()


_VERSION_RE = re.compile(r"^v?\d+(\.\d+)+\s*$", re.IGNORECASE)
def _is_informative(title: str) -> bool:
    """Return False if title looks like a version number or is too short to be useful."""
    t = title.strip()
    if len(t) < 20:
        return False
    if _VERSION_RE.match(t):
        return False
    # mostly digits/punctuation with very few letters
    letters = sum(1 for c in t if c.isalpha())
    if letters < 5:
        return False
    return True


def _build_article(feed_meta: dict, entry: dict, pub: datetime | None, descriptions: dict | None = None) -> dict:
    raw_title = _clean(entry.get("title", ""), 120)
    summary_text = _clean(entry.get("summary", entry.get("description", "")), 200)
    display_title = summary_text[:120] if summary_text and not _is_informative(raw_title) else raw_title
    published_iso = pub.isoformat() if pub else ""
    return {
        "title": raw_title,
        "display_title": display_title,
        "link": entry.get("link", feed_meta["url"]),
        "summary": summary_text,
        "published": published_iso,
        "source_label": feed_meta["title"],
        "category": feed_meta["category"],
        "feed_description": (descriptions or {}).get(feed_meta["url"], ""),
    }


def fetch_article(
    feed_meta: dict,
    descriptions: dict | None = None,
    *,
    allow_undated: bool = False,
) -> dict | None:
    """Fetch most recent article within MAX_ARTICLE_AGE_DAYS. Returns None on failure."""
    url = feed_meta["url"]
    try:
        parsed = feedparser.parse(
            url,
            request_headers={"User-Agent": "3cucharadas-bot/1.0 (+https://tatanlabra.gitlab.io/3cucharadas)"},
        )
    except Exception as exc:
        print(f"  WARN [{feed_meta['title']}]: {exc}", file=sys.stderr)
        return None

    entries = parsed.get("entries", [])
    if not entries:
        print(f"  WARN [{feed_meta['title']}]: no entries", file=sys.stderr)
        return None

    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_ARTICLE_AGE_DAYS)
    undated_candidate = None
    for e in entries[:10]:
        pub, has_explicit_date = _parse_date(e)
        if has_explicit_date and pub:
            if pub < cutoff:
                continue
            return _build_article(feed_meta, e, pub, descriptions)
        if allow_undated and undated_candidate is None:
            undated_candidate = e

    if allow_undated and undated_candidate is not None:
        print(f"  OK? [{feed_meta['title']}]: using undated fallback entry", file=sys.stderr)
        return _build_article(feed_meta, undated_candidate, None, descriptions)

    print(f"  SKIP [{feed_meta['title']}]: no recent articles (>{MAX_ARTICLE_AGE_DAYS}d)", file=sys.stderr)
    return None


def fetch_stratified(
    candidates: list[dict],
    global_pool: list[dict],
    target: int,
    descriptions: dict | None = None,
) -> list[dict]:
    """Try candidates per slot first, then fill globally to always target up to availability."""
    articles: list[dict] = []
    attempted_urls: set[str] = set()

    for candidate in candidates:
        if len(articles) >= target:
            break

        slot_attempts = 0
        slot_queue = [candidate] + [
            {**extra, "category": candidate["category"]}
            for extra in candidate.get("_pool", [])
        ]
        for feed_meta in slot_queue:
            if len(articles) >= target or slot_attempts >= MAX_ATTEMPTS_PER_SLOT:
                break
            if feed_meta["url"] in attempted_urls:
                continue

            attempted_urls.add(feed_meta["url"])
            slot_attempts += 1
            art = fetch_article(feed_meta, descriptions)
            if art:
                articles.append(art)
                print(f"  OK  [{feed_meta['category']}] {feed_meta['title']}")
                break

    # Global fallback with recent-only policy first
    global_attempts = 0
    for feed_meta in global_pool:
        if len(articles) >= target or global_attempts >= MAX_GLOBAL_FALLBACK_ATTEMPTS:
            break
        if feed_meta["url"] in attempted_urls:
            continue
        attempted_urls.add(feed_meta["url"])
        global_attempts += 1
        art = fetch_article(feed_meta, descriptions)
        if art:
            articles.append(art)
            print(f"  OK+ [{feed_meta['category']}] {feed_meta['title']} (global)")

    # Last-resort pass: allow undated entries to avoid dropping below target
    if len(articles) < target:
        for feed_meta in global_pool:
            if len(articles) >= target:
                break
            if feed_meta["url"] in attempted_urls:
                continue
            attempted_urls.add(feed_meta["url"])
            art = fetch_article(feed_meta, descriptions, allow_undated=True)
            if art:
                articles.append(art)
                print(f"  OK~ [{feed_meta['category']}] {feed_meta['title']} (undated last resort)")

    return articles


def resolve_seed_date() -> date:
    """Return seed date in America/Santiago. Supports RSS_SEED_DATE=YYYY-MM-DD override."""
    override = os.getenv("RSS_SEED_DATE", "").strip()
    if override:
        try:
            return date.fromisoformat(override)
        except ValueError:
            print(f"WARN invalid RSS_SEED_DATE={override!r}; falling back to local Santiago date", file=sys.stderr)
    return datetime.now(LOCAL_TZ).date()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not OPML_FILE.exists():
        sys.exit(f"OPML not found: {OPML_FILE}")

    socket.setdefaulttimeout(SOCKET_TIMEOUT)

    desc_file = ROOT / "assets" / "feed_descriptions.json"
    feed_descriptions: dict = {}
    if desc_file.exists():
        feed_descriptions = json.loads(desc_file.read_text(encoding="utf-8"))
        print(f"Descriptions table: {len(feed_descriptions)} entries loaded")

    feeds_by_cat = parse_opml(OPML_FILE)
    total = sum(len(v) for v in feeds_by_cat.values())
    print(f"OPML: {total} feeds in {len(feeds_by_cat)} categories")

    seed_date = resolve_seed_date()
    rng = random.Random(seed_date.isoformat())
    candidates, global_pool = stratified_sample(feeds_by_cat, TARGET_COUNT, rng)
    print(f"Selected {len(candidates)} candidates (stratified, seed={seed_date} America/Santiago):")
    print(
        f"Budgets: slot_attempts={MAX_ATTEMPTS_PER_SLOT} "
        f"global_attempts={MAX_GLOBAL_FALLBACK_ATTEMPTS}"
    )

    articles = fetch_stratified(candidates, global_pool, TARGET_COUNT, feed_descriptions)

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed_date": seed_date.isoformat(),
        "count": len(articles),
        "articles": articles,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {len(articles)} articles → {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
