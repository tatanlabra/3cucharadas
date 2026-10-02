#!/usr/bin/env python3
"""Check the rendered bilingual site, not just Liquid source strings."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("_site").resolve()


def rendered(path: str) -> str:
    return (SITE / path).read_text(encoding="utf-8")


def store(path: str) -> list[dict[str, object]]:
    source = rendered(path).strip()
    if not source.startswith("var store = ") or not source.endswith(";"):
        raise AssertionError(f"invalid search store: {path}")
    return json.loads(source.removeprefix("var store = ").removesuffix(";"))


def recent_urls(path: str) -> list[str]:
    match = re.search(r'<ul class="recent-posts">(.*?)</ul>', rendered(path), re.DOTALL)
    if not match:
        raise AssertionError(f"recent posts missing: {path}")
    return re.findall(r'<a href="([^"]+)"', match.group(1))


class SiteUxTest(unittest.TestCase):
    def test_search_stores_are_localized(self) -> None:
        spanish = store("search-store.js")
        english = store("en/search-store.js")
        self.assertGreater(len(spanish), 0)
        self.assertEqual(len(spanish), len(english))
        for language, entries in (("es", spanish), ("en", english)):
            for entry in entries:
                self.assertEqual(entry["lang"], language)
                url = str(entry["url"])
                self.assertEqual(url.startswith("/en/"), language == "en")
                self.assertTrue(url.endswith("/"))
                self.assertTrue((SITE / url.lstrip("/") / "index.html").is_file(), url)

    def test_search_assets_and_semantics(self) -> None:
        for prefix, expected in (("", "/search-store.js"), ("en/", "/en/search-store.js")):
            home = rendered(prefix + "index.html")
            self.assertIn(f'<script src="{expected}"></script>', home)
            self.assertIn('src="/assets/js/lunr/lunr-site.js"', home)
            self.assertNotIn('src="/assets/js/lunr/lunr-store.js"', home)
            self.assertIn('<main id="search-main" class="search-content" tabindex="-1">', home)
            self.assertIn('id="skip-content-link" href="#main"', home)
            self.assertIn('aria-controls="search-main" aria-expanded="false"', home)
            self.assertIn('class="results" data-results-found=', home)
            self.assertIn('<header class="masthead">', home)
            self.assertIn('<nav class="skip-links" aria-label=', home)
            self.assertIn('<h2 class="archive__subtitle">', home)
            self.assertIn('<p class="author__name p-name"', home)

    def test_english_navigation(self) -> None:
        for path in ("en/index.html", "en/page2/index.html"):
            home = rendered(path)
            self.assertRegex(home, r">Previous</a>")
            self.assertRegex(home, r">Next</a>")
            self.assertNotRegex(home, r">(?:Anterior|Siguiente)</a>")
        for path in ("en/categories/index.html", "en/year-archive/index.html"):
            archive = rendered(path)
            self.assertIn('class="back-to-top">Back to top', archive)
            self.assertNotIn('class="back-to-top">Volver arriba', archive)

    def test_about_uses_current_posts(self) -> None:
        for prefix in ("", "en/"):
            latest = re.findall(
                r'<h2 class="archive__item-title[^"]*" itemprop="headline">\s*<a href="([^"]+)"',
                rendered(prefix + "index.html"),
                re.DOTALL,
            )[:3]
            self.assertEqual(len(latest), 3)
            self.assertEqual(recent_urls(prefix + "about/index.html"), latest)
            about = rendered(prefix + "about/index.html")
            heading_id = "recent-posts" if prefix else "publicaciones-recientes"
            self.assertTrue(f'<h2 id="{heading_id}">' in about, prefix + "about/index.html")
            self.assertNotIn('CASEN 2024 en 3 cucharadas: lectura territorial', about)
        self.assertIn("de qué trata", rendered("about/index.html"))

    def test_404_is_bilingual_and_noindex(self) -> None:
        page = rendered("404.html")
        self.assertIn('name="robots" content="noindex', page)
        self.assertIn('class="not-found-copy" lang="es"', page)
        self.assertIn('class="not-found-copy" lang="en"', page)
        self.assertIn('href="/en/"', page)
        self.assertIn('href="/en/year-archive/"', page)
        self.assertIn('href="/en/feed.xml"', page)
        self.assertIn('<h2>Page not found</h2>', page)

    def test_dark_search_links_have_local_rule(self) -> None:
        css = rendered("assets/css/main.css")
        self.assertIn('.search-content .archive__item-title a', css)
        self.assertIn('color:var(--night-link)', css)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
