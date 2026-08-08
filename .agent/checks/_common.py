"""Utilidades compartidas por los comprobadores del contrato.

Todo lo que hay aquí lee el ARTEFACTO construido, no el código fuente: el
objetivo es comprobar lo que el navegador y Googlebot reciben de verdad, no lo
que las plantillas pretenden emitir.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

SITE_URL = "https://3cucharadas.cl"

# Rutas del artefacto que no son páginas indexables ni deben analizarse.
IGNORED_DIRS = {"assets", "vendor", "node_modules", ".git"}


@dataclass
class Page:
    """Lo que interesa del <head> de una página construida."""

    path: Path
    url: str
    lang: str = ""
    title: str = ""
    canonical: str = ""
    robots: list[str] = field(default_factory=list)
    hreflang: dict[str, str] = field(default_factory=dict)
    refresh_to: str = ""
    internal_links: set[str] = field(default_factory=set)
    content_links: set[str] = field(default_factory=set)
    body_classes: list[str] = field(default_factory=list)

    @property
    def noindex(self) -> bool:
        return any("noindex" in value.lower() for value in self.robots)

    @property
    def indexable(self) -> bool:
        return not self.noindex and not self.refresh_to


class _HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page_lang = ""
        self.title = ""
        self.canonical = ""
        self.robots: list[str] = []
        self.hreflang: dict[str, str] = {}
        self.refresh_to = ""
        self.links: set[str] = set()
        # Enlaces dentro de <div id="main">, es decir los que escribe la propia
        # página. Separarlos del cromo global (masthead, footer) evita atribuirle
        # a una plantilla enlaces que en realidad están en las 30 páginas del
        # sitio, como el <a href="/feed.xml"> del pie.
        self.content_links: set[str] = set()
        self.body_classes: list[str] = []
        self._in_title = False
        self._main_depth = -1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.page_lang = attr.get("lang", "")
        elif tag == "body":
            self.body_classes = attr.get("class", "").split()
        elif tag == "title":
            self._in_title = True
        elif tag == "link":
            rel = attr.get("rel", "").lower()
            href = attr.get("href", "")
            if rel == "canonical" and href:
                self.canonical = href.strip()
            elif rel == "alternate" and attr.get("hreflang"):
                self.hreflang[attr["hreflang"].strip()] = href.strip()
        elif tag == "meta":
            name = attr.get("name", "").lower()
            equiv = attr.get("http-equiv", "").lower()
            if name == "robots" and attr.get("content"):
                self.robots.append(attr["content"].strip())
            elif equiv == "refresh":
                match = re.search(r"url\s*=\s*(\S+)", attr.get("content", ""), re.I)
                if match:
                    self.refresh_to = match.group(1).strip().strip("'\"")
        elif tag == "a":
            href = attr.get("href", "").strip()
            if href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
                self.links.add(href)
                if self._main_depth >= 0:
                    self.content_links.add(href)

        if tag == "div":
            if self._main_depth >= 0:
                self._main_depth += 1
            elif attr.get("id") == "main":
                self._main_depth = 0

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "div" and self._main_depth >= 0:
            self._main_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def file_to_url(path: Path, root: Path) -> str:
    """`<root>/en/about/index.html` -> `/en/about/`; `<root>/404.html` -> `/404.html`."""
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def url_to_path(url: str, root: Path) -> Path:
    """Inversa de `file_to_url`, tolerante a URLs absolutas."""
    rel = url.removeprefix(SITE_URL).split("?", 1)[0].split("#", 1)[0]
    rel = rel.lstrip("/")
    if not rel:
        return root / "index.html"
    if rel.endswith("/"):
        return root / rel / "index.html"
    if rel.endswith(".html"):
        return root / rel
    return root / rel / "index.html"


def normalize(url: str) -> str:
    """Deja una URL comparable: absoluta y con barra final coherente."""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    elif url.startswith("/"):
        url = SITE_URL + url
    return url.rstrip("/") or SITE_URL


def iter_html(root: Path):
    """Recorre las páginas HTML del artefacto, saltando assets y vendor."""
    for path in sorted(root.rglob("*.html")):
        parts = set(path.relative_to(root).parts[:-1])
        if parts & IGNORED_DIRS:
            continue
        yield path


def read_page(path: Path, root: Path) -> Page:
    parser = _HeadParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return Page(
        path=path,
        url=file_to_url(path, root),
        lang=parser.page_lang,
        title=parser.title,
        canonical=parser.canonical,
        robots=parser.robots,
        hreflang=parser.hreflang,
        refresh_to=parser.refresh_to,
        internal_links=parser.links,
        content_links=parser.content_links,
        body_classes=parser.body_classes,
    )


def load_pages(root: Path) -> list[Page]:
    return [read_page(path, root) for path in iter_html(root)]


def sitemap_locs(root: Path) -> list[str]:
    """URLs declaradas en `<loc>` del sitemap raíz del artefacto."""
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        return []
    tree = ElementTree.fromstring(sitemap.read_text(encoding="utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in tree.findall(".//sm:loc", ns) if el.text]


def require_artifact(raw: str) -> Path:
    root = Path(raw)
    if not root.is_absolute():
        root = Path(__file__).resolve().parents[2] / raw
    if not root.is_dir():
        sys.exit(f"ERROR: el artefacto '{raw}' no existe. Construir primero con jekyll build.")
    return root


def report(label: str, problems: list[str], checked: int) -> int:
    """Imprime el veredicto de un comprobador. Devuelve el exit code."""
    if problems:
        print(f"FAIL {label}: {len(problems)} problema(s) sobre {checked} elemento(s)")
        for line in problems:
            print(f"  · {line}")
        return 1
    print(f"OK   {label}: {checked} elemento(s) sin problemas")
    return 0
