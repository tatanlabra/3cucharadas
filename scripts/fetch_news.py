#!/usr/bin/env python3
"""Fetches 6 random RSS feeds from the personal OPML (assets/feedly-subscriptions.opml).

Selection strategy:
- Seeded with today's date → same 6 feeds all day, different every day
- Stratified: 1 feed per OPML category, extras fill remaining slots
- Resilient: skips dead/slow feeds (6s timeout), fills gaps from other categories

Output: _data/feedly_news.json  (read by _includes/news-widget.html)
"""

import json
import random
import re
import socket
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import feedparser
except ImportError:
    sys.exit("Missing dependency: pip install feedparser")

ROOT = Path(__file__).resolve().parents[1]
OPML_FILE = ROOT / "assets" / "feedly-subscriptions.opml"
OUTPUT_FILE = ROOT / "_data" / "feedly_news.json"
TARGET_COUNT = 6
SOCKET_TIMEOUT = 6          # seconds per feed request
MAX_ATTEMPTS_PER_SLOT = 4   # tries before giving up on a category slot
MAX_ARTICLE_AGE_DAYS = 60   # skip articles older than this


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

def stratified_sample(feeds_by_cat: dict, n: int, rng: random.Random) -> list[dict]:
    """Pick up to n feeds: 1 per category first, then extras to fill the quota."""
    categories = list(feeds_by_cat.keys())
    rng.shuffle(categories)

    selected: list[dict] = []
    # Round 1: one random feed per category
    for cat in categories:
        pool = list(feeds_by_cat[cat])
        rng.shuffle(pool)
        feed = pool[0]
        selected.append({**feed, "category": cat, "_pool": pool[1:]})
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

    return selected


# ── RSS fetching ──────────────────────────────────────────────────────────────

def _parse_date(entry: dict) -> datetime:
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def _clean(text: str, max_len: int = 200) -> str:
    clean = re.sub(r"<[^>]+>", "", text or "")
    return " ".join(clean.split())[:max_len].rstrip()


_VERSION_RE = re.compile(r"^v?\d+(\.\d+)+\s*$", re.IGNORECASE)
_NONWORD_RE = re.compile(r"[^\w\s]", re.UNICODE)


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


def fetch_article(feed_meta: dict, descriptions: dict | None = None) -> dict | None:
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
    for e in entries[:10]:
        pub = _parse_date(e)
        if pub < cutoff:
            continue
        raw_title = _clean(e.get("title", ""), 120)
        summary_text = _clean(e.get("summary", e.get("description", "")), 200)
        display_title = summary_text[:120] if summary_text and not _is_informative(raw_title) else raw_title
        return {
            "title": raw_title,
            "display_title": display_title,
            "link": e.get("link", url),
            "summary": summary_text,
            "published": pub.isoformat(),
            "source_label": feed_meta["title"],
            "category": feed_meta["category"],
            "feed_description": (descriptions or {}).get(url, ""),
        }

    print(f"  SKIP [{feed_meta['title']}]: no recent articles (>{MAX_ARTICLE_AGE_DAYS}d)", file=sys.stderr)
    return None


def fetch_stratified(candidates: list[dict], target: int, descriptions: dict | None = None) -> list[dict]:
    """Try each candidate in order; fall back to pool extras for failed slots."""
    articles: list[dict] = []
    for candidate in candidates:
        if len(articles) >= target:
            break
        art = fetch_article(candidate, descriptions)
        if art:
            articles.append(art)
            print(f"  OK  [{candidate['category']}] {candidate['title']}")
        else:
            # Try extras from the same-category pool
            for extra in candidate.get("_pool", []):
                art = fetch_article({**extra, "category": candidate["category"]}, descriptions)
                if art:
                    articles.append(art)
                    print(f"  OK* [{candidate['category']}] {extra['title']} (fallback)")
                    break
    return articles


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

    rng = random.Random(date.today().isoformat())
    candidates = stratified_sample(feeds_by_cat, TARGET_COUNT, rng)
    print(f"Selected {len(candidates)} candidates (stratified, seed={date.today()}):")

    articles = fetch_stratified(candidates, TARGET_COUNT, feed_descriptions)

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(articles),
        "articles": articles,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {len(articles)} articles → {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
