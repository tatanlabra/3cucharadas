#!/usr/bin/env python3
"""Check docs/contracts/ux-transversal.yml against the rendered site.

Usage: python3 tests/test_ux_transversal_contract.py public

Only the standard library: the CI image runs this with the system python3.
"Puede que también te interese" is recomputed here from the posts' front matter
instead of trusting the Liquid that produces it.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (ROOT / "_site")
CONTRACT = ROOT / "docs" / "contracts" / "ux-transversal.yml"


def rendered(path: str) -> str:
    return (SITE / path).read_text(encoding="utf-8")


def css() -> str:
    return rendered("assets/css/main.css")


def luminance(hex_color: str) -> float:
    def channel(value: int) -> float:
        v = value / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def css_rules(source: str) -> list[tuple[str, str]]:
    """Flat (selector, body) pairs; @media wrappers are irrelevant for these checks."""
    flat = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    return [(sel.strip(), body) for sel, body in re.findall(r"([^{}@;]+)\{([^{}]*)\}", flat)]


def css_rules_in_context(source: str) -> list[tuple[tuple[str, ...], str, str]]:
    """(cadena de @media/@supports, selector, cuerpo) para CSS compilado, con anidamiento."""
    flat = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    rules: list[tuple[tuple[str, ...], str, str]] = []
    stack: list[str] = []
    start = 0
    index = 0
    while index < len(flat):
        char = flat[index]
        if char == "{":
            prelude = flat[start:index].strip()
            if prelude.startswith("@"):
                stack.append(prelude)
                start = index + 1
            else:
                close = flat.index("}", index)
                rules.append((tuple(stack), prelude, flat[index + 1:close]))
                index = close
                start = index + 1
        elif char == "}":
            if stack:
                stack.pop()
            start = index + 1
        index += 1
    return rules


def selector_parts(selector: str) -> list[str]:
    """Separa una lista de selectores sin cortar dentro de :is(), :not() ni :where()."""
    parts, depth, start = [], 0, 0
    for index, char in enumerate(selector):
        depth += (char == "(") - (char == ")")
        if char == "," and depth == 0:
            parts.append(selector[start:index].strip())
            start = index + 1
    parts.append(selector[start:].strip())
    return parts


def front_matter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    block = text.split("---", 2)[1]
    data: dict[str, object] = {}
    lines = block.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        if key == "tags":
            if value.startswith("["):
                data[key] = [t.strip().strip("'\"") for t in value.strip("[]").split(",") if t.strip()]
            else:
                items = []
                for follow in lines[index + 1:]:
                    item = re.match(r"^\s*-\s*(.+)$", follow)
                    if not item:
                        break
                    items.append(item.group(1).strip().strip("'\""))
                data[key] = items
        elif key in {"lang", "permalink", "date", "hidden", "related"}:
            data[key] = value.strip().strip("'\"")
    return data


def site_timezone():
    match = re.search(r"^timezone\s*:\s*[\"']?([^\"'\s#]+)", (ROOT / "_config.yml").read_text(encoding="utf-8"), re.MULTILINE)
    try:
        return ZoneInfo(match.group(1) if match else "UTC")
    except ZoneInfoNotFoundError:
        # Imagen de CI sin tzdata: solo afecta a posts con fecha sin hora, y el
        # desfase de Chile (-3/-4) no cambia el orden entre días distintos.
        return timezone(timedelta(hours=-4))


def parse_date(value: str, zone) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(value, fmt)
        except ValueError:
            continue
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=zone)
    raise AssertionError(f"fecha no reconocida: {value}")


def posts_by_lang() -> dict[str, list[dict[str, object]]]:
    zone = site_timezone()
    posts = []
    for path in sorted((ROOT / "_posts").glob("*.md")):
        data = front_matter(path)
        if str(data.get("hidden", "")).lower() == "true":
            continue
        data["path"] = path.name
        data["when"] = parse_date(str(data["date"]), zone)
        posts.append(data)
    # Jekyll ordena por fecha y desempata por ruta; site.posts es el orden inverso.
    posts.sort(key=lambda p: (p["when"], p["path"]), reverse=True)
    grouped: dict[str, list[dict[str, object]]] = {}
    for post in posts:
        grouped.setdefault(str(post.get("lang", "es")), []).append(post)
    return grouped


def expected_related(page: dict[str, object], candidates: list[dict[str, object]]) -> list[str]:
    own = set(page["tags"])
    chosen: list[dict[str, object]] = []
    for need in (3, 2, 1):
        for post in candidates:
            if post is page or post in chosen:
                continue
            if len(own & set(post["tags"])) >= need:
                chosen.append(post)
    for post in candidates:
        if len(chosen) >= 4:
            break
        if post is not page and post not in chosen:
            chosen.append(post)
    return [str(p["permalink"]) for p in chosen[:4]]


def related_hrefs(page_html: str) -> list[str]:
    block = page_html.split('class="page__related"', 1)
    if len(block) < 2:
        return []
    titles = re.findall(r'class="archive__item-title[^"]*"[^>]*>.*?<a href="([^"]+)"', block[1], re.DOTALL)
    return [html.unescape(t) for t in titles][:4]


class UxTransversalContract(unittest.TestCase):
    def test_contract_ids_have_tests(self) -> None:
        ids = re.findall(r"^\s*-\s*id:\s*(\S+)", CONTRACT.read_text(encoding="utf-8"), re.MULTILINE)
        self.assertGreater(len(ids), 0)
        for invariant in ids:
            self.assertTrue(hasattr(self, "test_" + invariant.replace("-", "_")), invariant)

    def test_theme_color_crema(self) -> None:
        toggle = rendered("assets/js/theme-toggle.js")
        match = re.search(r"function updateThemeColor\(theme\)\s*\{(.*?)\n  \}", toggle, re.DOTALL)
        self.assertIsNotNone(match, "updateThemeColor no encontrado")
        self.assertIn('"#faf7f0"', match.group(1))
        self.assertNotIn('"#ffffff"', match.group(1))
        self.assertIn('<meta name="theme-color" content="#faf7f0"', rendered("index.html"))

    def test_primera_visita_sistema(self) -> None:
        for page in ("index.html", "en/index.html"):
            head = rendered(page).split("</head>", 1)[0]
            self.assertIn("prefers-color-scheme: dark", head, page)
            self.assertRegex(head, r"storedTheme === null", page)
        toggle = rendered("assets/js/theme-toggle.js")
        self.assertRegex(toggle, r"stored === null \?")
        # El tema del sistema no se guarda como si fuera una elección.
        self.assertNotRegex(toggle, r"if \(theme === DARK_THEME\) \{\s*storeTheme\(theme\);")

    def test_carrusel_nocturno_contraste(self) -> None:
        rules = css_rules(css())
        layer = None
        for selector, body in rules:
            if 'academic-night' in selector and selector.endswith(".evidence-carousel"):
                found = re.search(r"--carousel-layer:\s*(#[0-9a-fA-F]{6})", body)
                if found:
                    layer = found.group(1)
        self.assertIsNotNone(layer, "capa nocturna del carrusel no encontrada")
        tones = set()
        for page in SITE.rglob("index.html"):
            tones.update(re.findall(r'class="evidence-carousel__slide"[^>]*data-tone="([a-z-]+)"', page.read_text(encoding="utf-8")))
        self.assertGreater(len(tones), 0, "no hay carruseles de evidencia en el sitio")
        for tone in sorted(tones):
            color = None
            for selector, body in rules:
                plain = selector.replace('"', "").replace("'", "")  # Sass comprimido quita las comillas
                if ("academic-night" in plain and f"data-tone={tone}]" in plain
                        and plain.endswith(".evidence-carousel__metric")):
                    found = re.search(r"(?<![-\w])color:\s*(#[0-9a-fA-F]{6})", body)
                    if found:
                        color = found.group(1)
            self.assertIsNotNone(color, f"tono {tone} sin color nocturno de métrica")
            self.assertGreaterEqual(contrast(color, layer), 4.5, f"{tone}: {color} sobre {layer}")

    def test_medida_linea(self) -> None:
        rules = css_rules(css())
        measures = [re.search(r"--measure:\s*([\d.]+)ch", body) for _, body in rules]
        measures = [float(m.group(1)) for m in measures if m]
        self.assertEqual(len(set(measures)), 1, f"--measure ausente o con varios valores: {measures}")
        self.assertTrue(45 <= measures[0] <= 66, measures[0])
        prose = re.compile(r"\.page__content\s*>\s*(?::is\()?[^,{]*\bp\b")
        literal = re.compile(r"max-(?:width|inline-size):\s*[\d.]+ch")
        users = 0
        for selector, body in rules:
            if not prose.search(selector):
                continue
            self.assertIsNone(literal.search(body), f"medida literal en {selector}")
            users += "var(--measure)" in body
        self.assertGreaterEqual(users, 1, "ninguna regla de prosa usa var(--measure)")

    def test_pie_objetivos_tactiles(self) -> None:
        for selector, body in css_rules(css()):
            if selector.replace("  ", " ").endswith(".page__footer-follow .social-icons a"):
                found = re.search(r"min-block-size:\s*(\d+)px", body)
                if found and int(found.group(1)) >= 24:
                    return
        self.fail("los enlaces sociales del pie no tienen min-block-size >= 24px")

    def test_comentarios_h2(self) -> None:
        source = (ROOT / "_includes" / "comments.html").read_text(encoding="utf-8")
        self.assertNotIn('<h4 class="page__comments-title"', source)
        self.assertIn('<h2 class="page__comments-title"', source)

    def test_relacionados_por_etiquetas(self) -> None:
        checked = 0
        for lang, posts in posts_by_lang().items():
            for post in posts:
                if str(post.get("related", "true")).lower() == "false":
                    continue
                url = str(post["permalink"])
                built = ("en" + url if lang == "en" and not url.startswith("/en/") else url).strip("/")
                page = SITE / built / "index.html"
                self.assertTrue(page.is_file(), page)
                got = [h.removeprefix("/en") if lang == "en" else h for h in related_hrefs(page.read_text(encoding="utf-8"))]
                self.assertEqual(got, expected_related(post, posts), url)
                checked += 1
        self.assertGreater(checked, 0)

    def test_movimiento_accesible(self) -> None:
        rules = css_rules_in_context(css())
        hides = [(m, s, b) for m, s, b in rules if ".motion-pending" in s and re.search(r"opacity:\s*0(?![.\d])", b)]
        self.assertTrue(hides, "no hay estado pendiente: ¿se retiró la aparición sin retirar el contrato?")
        for media, selector, _ in hides:
            self.assertFalse(any("print" in m or "reduce" in m for m in media), f"oculta en print/reduce: {selector}")
        resets = {kind: False for kind in ("reduce", "print")}
        for media, selector, body in rules:
            if ".motion-pending" in selector and re.search(r"opacity:\s*1", body):
                chain = " ".join(media)
                if "prefers-reduced-motion: reduce" in chain or "prefers-reduced-motion:reduce" in chain:
                    resets["reduce"] = True
                if "print" in chain and "transition:none" in body.replace(" ", ""):
                    resets["print"] = True
        self.assertEqual(resets, {"reduce": True, "print": True})
        for media, selector, body in rules:
            parts = [p.strip() for p in selector.split(",")]
            if any(p in (".archive__item", ".page__content>figure", ".page__content > figure") for p in parts):
                self.assertNotRegex(body, r"opacity:\s*0(?![.\d])", f"oculto por defecto: {selector}")
            if ".archive__item:hover" in selector and "transform" in body:
                chain = " ".join(media).replace(" ", "")
                self.assertIn("hover:hover", chain, selector)
                self.assertIn("prefers-reduced-motion:no-preference", chain, selector)
        script = rendered("assets/js/motion.js")
        self.assertIn('matchMedia("(prefers-reduced-motion: reduce)")', script)
        self.assertRegex(script, r"getBoundingClientRect\(\)\.top < fold\) return")
        self.assertIn("unobserve", script)
        self.assertIn("/assets/js/motion.js", rendered("index.html"))

    def test_firma_tres_cucharadas(self) -> None:
        heading = re.compile(r"<h2([^>]*)>\s*(?:Cucharada|Spoonful) [1-3]\b")
        checked = 0
        for page in SITE.rglob("index.html"):
            text = page.read_text(encoding="utf-8")
            found = heading.findall(text)
            if len(found) != 3:
                continue
            checked += 1
            for attrs in found:
                self.assertRegex(attrs, r'\bid="[^"]+"', f"cucharada sin id en {page}")
            self.assertIn("/assets/js/motion.js", text, page)
        self.assertGreater(checked, 0, "ningún post con tres cucharadas")
        script = rendered("assets/js/motion.js")
        self.assertIn('setAttribute("aria-current", "step")', script)
        sizes = []
        for _, selector, body in css_rules_in_context(css()):
            if selector.strip() == ".cucharadas__step":
                sizes += [float(v) for v in re.findall(r"(?:inline|block)-size:\s*([\d.]+)rem", body)]
        self.assertEqual(len(sizes), 2, "tamaño del indicador no declarado en rem")
        self.assertTrue(all(v * 16 >= 24 for v in sizes), sizes)

    def test_transicion_tarjeta_post(self) -> None:
        for page in ("index.html", "en/index.html"):
            head = rendered(page).split("</head>", 1)[0]
            inline = re.search(r"<style>([^<]*@view-transition[^<]*)</style>", head)
            self.assertIsNotNone(inline, page)
            self.assertIn("prefers-reduced-motion: no-preference", inline.group(1))
        pages = 0
        for page in SITE.rglob("index.html"):
            names = re.findall(r"view-transition-name:\s*([\w-]+)", page.read_text(encoding="utf-8"))
            if names:
                pages += 1
                duplicated = sorted({n for n in names if names.count(n) > 1})
                self.assertEqual(duplicated, [], f"{page}: nombres repetidos")
        self.assertGreater(pages, 0, "ninguna página declara nombres de transición")

    def test_identidad_cromatica(self) -> None:
        compiled = css()
        for skin in ("#0000ff", "#b60000"):
            self.assertNotIn(skin, compiled.lower(), f"color de la skin contrast: {skin}")
        rules = css_rules_in_context(compiled)
        def color_of(selector: str, prop: str) -> str | None:
            for _, sel, body in rules:
                if sel.strip() == selector:
                    found = re.search(rf"(?<![-\w]){prop}:\s*(#[0-9a-fA-F]{{6}})", body)
                    if found:
                        return found.group(1)
            return None
        link = color_of("a", "color")
        self.assertIsNotNone(link, "sin color base de enlace")
        self.assertGreaterEqual(contrast(link, "#faf7f0"), 4.5, link)
        toc = color_of(".toc .nav__title", "background")
        self.assertIsNotNone(toc)
        self.assertGreaterEqual(contrast("#ffffff", toc), 4.5, toc)

    def test_fuentes_subconjunto(self) -> None:
        manifest = json.loads((ROOT / "assets" / "fonts" / "subset-manifest.json").read_text(encoding="utf-8"))
        total = 0
        for rel, meta in manifest["files"].items():
            data = (SITE / rel).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), meta["sha256"], rel)
            total += len(data)
        self.assertLessEqual(total, 450_000, f"fuentes: {total} bytes")
        faces = re.findall(r"@font-face\{[^}]*\}", css())
        served = [re.search(r"url\(([^)]+)\)", f).group(1).strip("\"'").split("?")[0] for f in faces
                  if "Fira" in f]
        self.assertTrue(served)
        for url in served:
            self.assertIn(url.lstrip("/"), manifest["files"], f"@font-face fuera del manifiesto: {url}")
        text, code = set(), set()
        for page in SITE.rglob("*.html"):
            raw = re.sub(r"<(script|style)\b.*?</\1>", " ", page.read_text(encoding="utf-8", errors="ignore"), flags=re.S | re.I)
            raw = re.sub(r'<span class="katex.*?</span>\s*</span>\s*</span>', " ", raw, flags=re.S)
            for block in re.findall(r"<(?:code|pre)\b[^>]*>(.*?)</(?:code|pre)>", raw, flags=re.S | re.I):
                code.update(ord(c) for c in html.unescape(re.sub(r"<[^>]+>", "", block)) if ord(c) > 31)
            text.update(ord(c) for c in html.unescape(re.sub(r"<[^>]+>", " ", raw)) if ord(c) > 31)
        def inside(cp: int, spans: list[list[int]]) -> bool:
            return any(start <= cp <= end for start, end in spans)
        for family, used in (("fira-sans", text), ("firacode-nerd", code)):
            # Solo es regresión lo que la fuente completa tenía y el subconjunto perdió.
            # Emoji y símbolos que Fira nunca trajo siguen saliendo de la fuente del sistema.
            lost = sorted(hex(c) for c in used
                          if inside(c, manifest["original_ranges"][family])
                          and not inside(c, manifest["covered_ranges"][family]))
            self.assertEqual(lost, [], f"{family}: el subconjunto perdió caracteres usados; correr scripts/build_font_subsets.py")

    def test_iconos_autohospedados(self) -> None:
        manifest = json.loads((ROOT / "assets" / "vendor" / "fontawesome" / "subset-manifest.json").read_text(encoding="utf-8"))
        for rel, meta in manifest["files"].items():
            self.assertEqual(hashlib.sha256((SITE / rel).read_bytes()).hexdigest(), meta["sha256"], rel)
        sheet = rendered("assets/vendor/fontawesome/fa-subset.css")
        modifiers = {"fa-fw", "fa-lg", "fa-xs", "fa-sm", "fa-solid", "fa-regular", "fa-brands", "fa-spin", "fa-pulse"}
        used = set()
        for page in SITE.rglob("*.html"):
            text = page.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("cdnjs.cloudflare.com/ajax/libs/font-awesome", text, page)
            for attr in re.findall(r'class="([^"]*\bfa[sbr]?\b[^"]*)"', text):
                used.update(c for c in attr.split() if c.startswith("fa-") and c not in modifiers)
        for script in (SITE / "assets" / "js").rglob("*.js"):
            used.update(c for c in re.findall(r"\bfa-[a-z0-9-]+", script.read_text(encoding="utf-8", errors="ignore"))
                        if c not in modifiers)
        self.assertGreater(len(used), 0)
        for icon in sorted(used):
            self.assertRegex(sheet, rf"\.{re.escape(icon)}[,{{]", f"ícono sin regla: {icon}")
            self.assertIn(icon, manifest["icons"], f"ícono fuera del subconjunto: {icon}")

    def test_imagenes_responsivas(self) -> None:
        data = json.loads((ROOT / "_data" / "image_variants.json").read_text(encoding="utf-8"))
        self.assertGreater(len(data["images"]), 0)
        seen = 0
        for page in SITE.rglob("*.html"):
            for tag in re.findall(r"<img\b[^>]*>", page.read_text(encoding="utf-8", errors="ignore")):
                src = re.search(r'\ssrc="([^"?]+)', tag)
                if not src or src.group(1) not in data["images"]:
                    continue
                seen += 1
                srcset = re.search(r'\ssrcset="([^"]+)"', tag)
                self.assertIsNotNone(srcset, f"{page}: {src.group(1)} sin srcset")
                for variant in data["images"][src.group(1)]["variants"]:
                    self.assertIn(variant["src"], srcset.group(1))
        self.assertGreater(seen, 0, "ninguna figura declarada aparece en el sitio")
        for entry in data["images"].values():
            for variant in entry["variants"]:
                self.assertTrue((SITE / variant["src"].lstrip("/")).is_file(), variant["src"])

    def test_avisos_enlace_contraste(self) -> None:
        rules = css_rules_in_context(css())
        box = next(((s, b) for _, s, b in rules
                    if s.startswith(".page__content blockquote,") and re.search(r"background:\s*#[0-9a-fA-F]{6}", b)), None)
        self.assertIsNotNone(box, "sin fondo oscuro para citas y avisos")
        background = re.search(r"background:\s*(#[0-9a-fA-F]{6})", box[1]).group(1)
        variants = {"blockquote"} | set(re.findall(r"\.page__content \.(notice[\w-]*)", box[0]))
        covered: set[str] = set()
        for _, selector, body in rules:
            found = re.search(r"(?<![-\w])color:\s*(#[0-9a-fA-F]{6})", body)
            if not found:
                continue
            for part in selector_parts(selector):
                if not (part.startswith(".page__content ") and part.endswith(" a")):
                    continue
                owners = {"blockquote"} if part == ".page__content blockquote a" else set(re.findall(r"\.(notice[\w-]*)", part))
                if owners & variants:
                    self.assertGreaterEqual(contrast(found.group(1), background), 4.5, f"{part}: {found.group(1)} sobre {background}")
                    covered |= owners
        self.assertEqual(sorted(variants - covered), [], "variantes de aviso sin color de enlace propio")

    def test_sin_entrada_animada(self) -> None:
        last: dict[str, str] = {}
        targets = (".masthead", ".page__hero", ".page__hero--overlay", "#main", ".page__footer")
        for _, selector, body in css_rules_in_context(css()):
            parts = {p.strip() for p in selector.split(",")}
            for value in re.findall(r"(?<![-\w])animation:\s*([^;]+)", body):
                for target in targets:
                    if target in parts:
                        last[target] = value.strip()
        self.assertTrue(last, "ninguna regla de animación sobre la estructura: ¿cambió el tema?")
        for target in targets:
            self.assertEqual(last.get(target, "none"), "none", target)

    def test_minutos_lectura_plural(self) -> None:
        source = (ROOT / "_includes" / "page__meta.html").read_text(encoding="utf-8")
        # Ningún post baja de 400 palabras, así que la rama del singular no aparece en el
        # sitio construido: se exige en la fuente.
        self.assertRegex(source, r"\{%\s*elsif minutes == 1\s*%\}\s*1 \{\{ ui_text\.minute_read_one")
        seen = 0
        for page in SITE.rglob("index.html"):
            text = page.read_text(encoding="utf-8")
            self.assertNotIn("minuto(s)", text, page)
            for count, word in re.findall(r"(\d+)\s+(minutos?) de lectura", text):
                seen += 1
                self.assertEqual(word == "minuto", count == "1", f"{page}: {count} {word}")
        self.assertGreater(seen, 0, "ninguna página en español muestra tiempo de lectura")

    def test_autor_cabecera_objetivos_tactiles(self) -> None:
        wanted = {".author__urls a": False, ".masthead__brand .site-title": False}
        for _, selector, body in css_rules_in_context(css()):
            found = re.search(r"min-block-size:\s*(\d+)px", body)
            if not found or int(found.group(1)) < 24:
                continue
            for part in (p.strip() for p in selector.split(",")):
                if part in wanted:
                    wanted[part] = True
        self.assertEqual([k for k, ok in wanted.items() if not ok], [], "objetivos bajo 24 px")


    def test_navegacion_en_linea(self) -> None:
        rules = css_rules_in_context(css())
        def found(selector: str, prop: str, value: str, wide: bool) -> bool:
            for media, sel, body in rules:
                inside = any("min-width: 64em" in m or "min-width:64em" in m for m in media)
                if inside != wide or selector not in selector_parts(sel):
                    continue
                if re.search(rf"(?<![-\w]){prop}:\s*{value}\b", body):
                    return True
            return False
        # Bajo 64em, panel plegado; desde 64em, la MISMA regla en línea y sin botón.
        self.assertTrue(found(".masthead__nav .masthead__nav-list", "display", "none", wide=False))
        self.assertTrue(found(".masthead__nav .masthead__nav-list", "display", "flex", wide=True))
        self.assertTrue(found('.masthead__nav .masthead__nav-toggle[aria-expanded=true]~.masthead__nav-list', "display", "flex", wide=True)
                        or found('.masthead__nav .masthead__nav-toggle[aria-expanded="true"] ~ .masthead__nav-list', "display", "flex", wide=True),
                        "el panel abierto en estrecho quedaría en bloque al ensanchar")
        self.assertTrue(found(".masthead__nav .masthead__nav-toggle", "display", "none", wide=True))
        for page in ("index.html", "en/index.html"):
            links = re.findall(r'class="masthead__nav-link"', rendered(page))
            self.assertGreaterEqual(len(links), 2, page)

    def test_escala_y_lectura_fina(self) -> None:
        compiled = css()
        sizes = {}
        for level in (1, 2, 3, 4):
            found = re.search(rf"(?:^|[}};,]){{1}}h{level}\{{[^}}]*?font-size:\s*([\d.]+)em", compiled)
            self.assertIsNotNone(found, f"h{level} sin tamaño en em")
            sizes[level] = float(found.group(1))
        self.assertEqual(sizes, {1: 1.953, 2: 1.5625, 3: 1.25, 4: 1.125})
        rules = css_rules_in_context(compiled)
        def body_of(selector: str) -> str:
            return " ".join(b for _, sel, b in rules if selector in selector_parts(sel))
        notice = body_of(".page__content :is(.notice,.notice--primary,.notice--info,.notice--warning,.notice--success,.notice--danger)")
        self.assertRegex(notice, r"font-size:\s*\.875em")
        self.assertRegex(body_of(".page__content figcaption"), r"font-size:\s*\.8em")
        self.assertRegex(body_of(".toc__menu a"), r"hyphens:\s*manual")

    def test_tablas_leyenda_y_fondo(self) -> None:
        compiled = css()
        root = re.search(r":root\{[^}]*--fondo:\s*(#[0-9a-fA-F]{6})", compiled)
        self.assertIsNotNone(root, "--fondo sin definir: las sombras de las tablas caen en #fdfdfd")
        page_bg = re.search(r"html\{[^}]*background-color:\s*(#[0-9a-fA-F]{6})", compiled)
        self.assertIsNotNone(page_bg)
        self.assertEqual(root.group(1).lower(), page_bg.group(1).lower())
        rules = css_rules_in_context(compiled)
        wrapper = " ".join(b for _, sel, b in rules if sel.strip() == ".tabla-desliza")
        self.assertIn("var(--fondo", wrapper)
        self.assertRegex(wrapper, r"container-type:\s*inline-size")
        caption = " ".join(b for _, sel, b in rules if sel.replace(" ", "") == ".tabla-desliza>table>caption")
        self.assertRegex(caption, r"(?<![-\w])inline-size:\s*100cqi")
        self.assertRegex(caption, r"position:\s*sticky")


    def test_anatomia_del_post(self) -> None:
        checked = 0
        for lang, posts in posts_by_lang().items():
            for post in posts:
                url = str(post["permalink"])
                built = ("en" + url if lang == "en" and not url.startswith("/en/") else url).strip("/")
                text = (SITE / built / "index.html").read_text(encoding="utf-8")
                self.assertTrue('<div id="main" role="main" class="main--post">' in text, f"{url}: #main sin main--post")
                about = "/en/about/" if lang == "en" else "/about/"
                byline = re.search(rf'class="page__byline">.*?<a href="{re.escape(about)}" rel="author">', text, re.S)
                self.assertTrue(byline, f"{url}: sin firma compacta hacia {about}")
                self.assertTrue('class="author__name p-name"' in text, f"{url}: sin h-card del autor")
                checked += 1
        self.assertGreater(checked, 0)
        rules = css_rules_in_context(css())
        def gutters(width: str) -> dict[str, str]:
            found: dict[str, str] = {}
            for media, selector, body in rules:
                if not any(f"min-width: {width}" in m or f"min-width:{width}" in m for m in media):
                    continue
                for prop in ("padding-inline-start", "padding-inline-end"):
                    value = re.search(rf"(?<![-\w]){prop}:\s*([\d.]+px)", body)
                    if value and selector.strip() in ("#main.main--post>.page", "#main.main--post > .page", ".page"):
                        found[f"{selector.strip().split()[-1].split('>')[-1]}:{prop}"] = value.group(1)
            return found
        for width, gutter in (("64em", "200px"), ("80em", "300px")):
            found = gutters(width)
            self.assertEqual(found.get(".page:padding-inline-start"), gutter, f"{width}: {found}")
            self.assertEqual(found.get(".page:padding-inline-end"), gutter, f"{width}: el índice cambió de ancho")
        order: dict[str, str] = {}
        for media, selector, body in rules:
            if any("min-width: 64em" in x for x in media):
                key = selector.replace(" ", "")
                order[key] = order.get(key, "") + ";" + body
        self.assertRegex(order.get("#main.main--post>.sidebar", ""), r"order:\s*2")
        self.assertRegex(order.get("#main.main--post", ""), r"flex-direction:\s*column")


    def test_portada_ultima_cucharada(self) -> None:
        grouped = posts_by_lang()
        for lang, prefix in (("es", ""), ("en", "en/")):
            home = rendered(prefix + "index.html")
            hero = re.search(r'id="home-latest-title"[^>]*>\s*<a href="([^"]+)"', home)
            self.assertIsNotNone(hero, f"{prefix}index.html sin hero de la última cucharada")
            newest = str(grouped[lang][0]["permalink"])
            expected = "/en" + newest if lang == "en" and not newest.startswith("/en/") else newest
            self.assertEqual(hero.group(1), expected, f"{prefix}index.html: el hero no es el post más reciente")
            grid = re.findall(r'<h2 class="archive__item-title[^"]*" itemprop="headline">\s*<a href="([^"]+)"', home)
            self.assertGreater(len(grid), 0)
            self.assertNotIn(expected, grid, "la grilla repite el post del hero")
            self.assertEqual(len(re.findall(r'fetchpriority="high"', home)), 1, f"{prefix}index.html: más de un LCP declarado")
            self.assertIn('class="author__name p-name"', home)
            self.assertRegex(home, r'href="https://mastodon\.social/[^"]+"[^>]*rel="[^"]*\bme\b')
            page2 = SITE / prefix / "page2" / "index.html"
            if page2.is_file():
                self.assertNotIn('id="home-latest-title"', page2.read_text(encoding="utf-8"))
        rules = css_rules_in_context(css())
        teaser = " ".join(b for _, sel, b in rules if sel.strip() == ".home-latest .home__entries.entries-grid .archive__item-teaser")
        self.assertRegex(teaser, r"aspect-ratio:\s*2\s*/\s*1")
        self.assertRegex(teaser, r"max-height:\s*none")
        codera = [sel for _, sel, b in rules if ".home-codera-hero .page__hero--overlay" in sel and "background-image" in b]
        self.assertTrue(codera)
        for sel in codera:
            self.assertIn(":not(.page__hero--latest)", sel, "la imagen de marca se descargaría bajo el hero nuevo")


    def test_botones_interaccion(self) -> None:
        rules = css_rules_in_context(css())
        family = {".btn", ".masthead__nav-link", ".page__taxonomy-item", ".pagination--pager", ".subscribe-rss__topic"}
        transition = [b for m, sel, b in rules if family <= set(selector_parts(sel)) and "transition-property" in b]
        self.assertTrue(transition, "sin transición común para botones y controles")
        for body in transition:
            props = re.search(r"transition-property:\s*([^;]+)", body).group(1)
            self.assertNotIn("all", props)
            self.assertIn("transform", props)
        focus = [b for _, sel, b in rules if ":focus-visible" in sel and all(f in sel for f in family)]
        self.assertTrue(focus, "sin foco común")
        self.assertTrue(any(re.search(r"outline:\s*([2-9])px solid", b) for b in focus))
        for media, sel, body in rules:
            if "transform" not in body or not any(f in sel for f in family):
                continue
            chain = " ".join(media).replace(" ", "")
            if ":active" in sel or ":hover" in sel:
                self.assertIn("prefers-reduced-motion:no-preference", chain, sel)
            if ":hover" in sel:
                self.assertIn("hover:hover", chain, sel)
        self.assertTrue(any(sel.strip() == ".btn" and re.search(r"border-radius:\s*999px", b) for _, sel, b in rules))
        checked = 0
        for page in SITE.rglob("index.html"):
            text = page.read_text(encoding="utf-8")
            share = text.split('<section class="page__share">', 1)
            if len(share) == 2:
                block = share[1].split("</section>", 1)[0]
                self.assertNotIn("fa-twitter\"", block, page)
                self.assertIn("fa-x-twitter", block, page)
            nav = text.split('<nav class="pagination pagination--post"', 1)
            if len(nav) == 2:
                block = nav[1].split("</nav>", 1)[0]
                self.assertNotIn('aria-disabled="true"', block, page)
                self.assertIn('class="pagination__title"', block, page)
                checked += 1
        self.assertGreater(checked, 0, "ningún post con «Anterior / Siguiente»")

    def test_fechas_en_idioma(self) -> None:
        english = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, 20\d\d")
        spanish = re.compile(r"\d{1,2} de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de 20\d\d")
        seen = 0
        for page in SITE.rglob("index.html"):
            if "en" in page.relative_to(SITE).parts[:1]:
                continue
            text = re.sub(r"<(script|style)\b.*?</\1>", " ", page.read_text(encoding="utf-8"), flags=re.S)
            visible = re.sub(r"<[^>]+>", " ", text)
            self.assertIsNone(english.search(visible), f"{page}: fecha con mes en inglés")
            seen += bool(spanish.search(visible))
        self.assertGreater(seen, 0, "ninguna página en español muestra una fecha")


    def test_titulo_y_parrafo_alineados(self) -> None:
        prose = re.compile(r"\.page__content\s*>\s*(?::is\()?[^,{]*\bp\b")
        auto_start = re.compile(r"margin-left:\s*auto|margin-inline-start:\s*auto|margin-inline:\s*auto|margin:\s*[^;]*\bauto\b[^;]*\bauto\b")
        checked = 0
        for _, selector, body in css_rules_in_context(css()):
            if not prose.search(selector):
                continue
            checked += 1
            self.assertIsNone(auto_start.search(body), f"prosa centrada (sangría aparente tras los títulos): {selector}")
        self.assertGreater(checked, 0)


    def test_tablas_region_unica(self) -> None:
        nested = re.compile(r'role="region"[^>]*>(?:\s*<div\b[^>]*>)*\s*<div class="tabla-desliza"')
        wrapped = 0
        for page in SITE.rglob("index.html"):
            text = page.read_text(encoding="utf-8")
            if 'class="tabla-desliza"' not in text:
                continue
            self.assertIsNone(nested.search(text), f"{page}: región dentro de región")
            self.assertNotIn("width:max-content;min-width:100%", text, page)
            for attrs, caption in re.findall(r'<div class="tabla-desliza"([^>]*)>\s*<table\b[^>]*>\s*<caption>(.*?)</caption>', text, re.S):
                wrapped += 1
                label = re.search(r'aria-label="([^"]*)"', attrs).group(1)
                plain = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", caption)).strip())
                self.assertEqual(html.unescape(label), plain, f"{page}: región sin el nombre de su leyenda")
        self.assertGreater(wrapped, 0, "ninguna tabla con leyenda: ¿cambió el plugin?")
        provenance = json.loads((ROOT / "assets" / "data" / "avaluos-ii-extension" / "provenance.json").read_text(encoding="utf-8"))
        sealed = {k: v for k, v in provenance["outputs_sha256"].items() if k.startswith("avaluos-ii-extension-")}
        self.assertTrue(sealed)
        for name, digest in sealed.items():
            self.assertEqual(hashlib.sha256((ROOT / "_includes" / name).read_bytes()).hexdigest(), digest,
                             f"{name}: el include sellado cambió; la corrección va en el HTML renderizado")


    def test_sin_jquery(self) -> None:
        self.assertFalse((SITE / "assets" / "js" / "main.min.js").exists(), "el artefacto sigue publicando main.min.js")
        pages = 0
        for page in SITE.rglob("index.html"):
            text = page.read_text(encoding="utf-8")
            if "<script" not in text:
                continue
            self.assertNotIn("main.min.js", text, page)
            self.assertNotRegex(text, r'<script[^>]+src="[^"]*jquery', page)
            if "/assets/js/theme-toggle.js" in text:
                pages += 1
                self.assertIn("/assets/js/site-core.js", text, page)
        self.assertGreater(pages, 0)
        core = rendered("assets/js/site-core.js")
        for hook in (".author__urls-wrapper button", ".search-content", "nav.toc a", "header-link", "clipboard-copy-button", "showModal"):
            self.assertIn(hook, core, f"site-core.js no cubre {hook}")
        own = [p for p in (SITE / "assets" / "js").glob("*.js")] + [SITE / "assets" / "js" / "lunr" / "lunr-site.js"]
        for script in own:
            code = re.sub(r"/\*.*?\*/|//[^\n]*", "", script.read_text(encoding="utf-8", errors="ignore"), flags=re.S)
            self.assertIsNone(re.search(r"\bjQuery\b|(?<![\w.])\$\(", code), f"{script.name} usa jQuery")
        smooth = [m for m, sel, b in css_rules_in_context(css()) if re.search(r"scroll-behavior:\s*smooth", b) and sel.strip() == "html"]
        self.assertTrue(smooth, "sin desplazamiento suave")
        for media in smooth:
            self.assertIn("prefers-reduced-motion:no-preference", " ".join(media).replace(" ", ""))
        ui = (ROOT / "_data" / "ui-text.yml").read_text(encoding="utf-8")
        for key in ("results_found", "results_found_one"):
            for value in re.findall(rf"^\s*{key}\s*:\s*\"([^\"]*)\"", ui, re.M)[:2]:
                self.assertNotIn("(s)", value)


    def test_recursos_versionados(self) -> None:
        pinned = re.compile(r"/\d+\.\d+(?:\.\d+)?/|[-.][0-9a-f]{8,}\.(?:js|css)$")
        seen = 0
        for page in SITE.rglob("*.html"):
            text = page.read_text(encoding="utf-8", errors="ignore")
            refs = re.findall(r'<script\b[^>]*\bsrc="(/[^"]+)"', text)
            refs += re.findall(r'<link\b[^>]*\brel="stylesheet"[^>]*\bhref="(/[^"]+)"', text)
            for ref in refs:
                seen += 1
                path = ref.split("?", 1)[0]
                self.assertTrue("?v=" in ref or pinned.search(path), f"{page}: {ref} sin versión")
        self.assertGreater(seen, 0)


    def test_tokens_de_interfaz(self) -> None:
        rules = css_rules_in_context(css())
        def declared(selector: str) -> dict[str, str]:
            out: dict[str, str] = {}
            for media, sel, body in rules:
                if not media and sel.strip() == selector:
                    out.update({k: v.strip() for k, v in re.findall(r"(--[\w-]+):\s*([^;]+)", body)})
            return out
        root = declared(":root")
        night = {**root, **declared("html[data-theme=academic-night]")}
        names = ("--ui-paper", "--ui-surface", "--ui-ink", "--ui-link", "--ui-line", "--ui-strong-bg", "--ui-strong-fg")
        for name in names:
            self.assertIn(name, root, f"{name} sin valor claro")
            self.assertIn(name, declared("html[data-theme=academic-night]"), f"{name} sin valor oscuro")
        def resolve(table: dict[str, str], name: str) -> str:
            value = table[name]
            for _ in range(5):
                ref = re.fullmatch(r"var\((--[\w-]+)\)", value)
                if not ref:
                    break
                value = table[ref.group(1)]
            return value
        for theme, table in (("claro", root), ("oscuro", night)):
            for fg, bg in (("--ui-ink", "--ui-paper"), ("--ui-ink", "--ui-surface"), ("--ui-link", "--ui-surface"), ("--ui-strong-fg", "--ui-strong-bg")):
                a, b = resolve(table, fg), resolve(table, bg)
                self.assertRegex(a + b, r"^#[0-9a-fA-F]{6}#[0-9a-fA-F]{6}$", f"{theme}: {fg}/{bg} no resuelven a hex")
                self.assertGreaterEqual(contrast(a, b), 4.5, f"{theme}: {fg} {a} sobre {bg} {b}")
        # Cascada: por selector y propiedad gana la última declaración (las del tema
        # quedan antes en el CSS compilado); esa tiene que ser un token.
        components = (".page__share .btn", ".page__share .btn:hover", ".pagination__label",
                      ".page__taxonomy-item", ".page__taxonomy-item:hover")
        last: dict[tuple[str, str], str] = {}
        for media, sel, body in rules:
            for part in selector_parts(sel):
                if part in components and not media:
                    for prop, value in re.findall(r"(?<![-\w])(color|background|background-color|border-color|border):\s*([^;]+)", body):
                        last[(part, prop)] = value.strip()
                if "academic-night" in part and any(part.endswith(c) for c in components):
                    self.fail(f"regla por tema: {part}")
        self.assertTrue(last)
        for (part, prop), value in last.items():
            if re.fullmatch(r"transparent|rgba\(0,\s*0,\s*0,\s*0\)", value):
                continue
            self.assertNotRegex(value, r"#[0-9a-fA-F]{3,6}\b|rgba?\(", f"{part} {prop}: color literal {value}")


    def test_sass_import_contenido(self) -> None:
        source = (ROOT / "assets" / "css" / "main.scss").read_text(encoding="utf-8")
        imports = re.findall(r'^\s*@import\s+"([^"]+)"', source, re.M)
        self.assertEqual(len(imports), 2, f"@import nuevos en main.scss: {imports}")
        self.assertTrue(imports[0].startswith("minimal-mistakes/skins/") and imports[1] == "minimal-mistakes", imports)
        lock = (ROOT / "Gemfile.lock").read_text(encoding="utf-8")
        versions = re.findall(r"^\s{4}sass-embedded \((\d+)\.\d+\.\d+", lock, re.M)
        self.assertTrue(versions, "sass-embedded no aparece resuelto en Gemfile.lock")
        for major in versions:
            self.assertLess(int(major), 3, "Dart Sass 3 elimina @import: migrar main.scss y salir de los parciales del tema antes de subir")


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
