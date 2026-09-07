"""Bound graph label contrast even over a bright canvas behind its 90% panel."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def ratio(fg, bg):
    def lum(rgb):
        values = [v / 255 for v in rgb]
        values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(v * w for v, w in zip(values, [.2126, .7152, .0722]))
    a, b = sorted([lum(fg), lum(bg)])
    return (b + .05) / (a + .05)


class GraphContrastTest(unittest.TestCase):
    def test_fallback_hides_the_id_specific_flex_panel(self):
        template = (ROOT / 'scripts/penta_rag_graph/rag-graph.template.html').read_text()
        self.assertRegex(template, r'html\.graph-fallback-active #insights[^}]*display:none')

    def test_old_muted_fails_bright_backdrop_control(self):
        self.assertLess(ratio([121, 130, 169], [49, 50, 60]), 4.5)
        self.assertGreaterEqual(ratio([145, 154, 189], [49, 50, 60]), 4.5)

    def test_template_and_artifact_preserve_contrast_bound(self):
        for path in ['scripts/penta_rag_graph/rag-graph.template.html', 'assets/visualizations/penta-rag-knowledge-graph/index.html']:
            css = (ROOT / path).read_text().split('</style>', 1)[0]
            color = re.search(r'--muted:#([0-9a-f]{6})', css)[1]
            fg = [int(color[i:i + 2], 16) for i in [0, 2, 4]]
            # Actual panel alpha, not an assumed opaque background.
            panel = re.search(r'--panel:rgba\((\d+),(\d+),(\d+),([.\d]+)\)', css)
            alpha = float(panel[4])
            bg = [float(panel[i]) * alpha + 255 * (1 - alpha) for i in [1, 2, 3]]
            self.assertGreaterEqual(ratio(fg, bg), 4.5, path)
            self.assertRegex(css, r'\.scene-container \.scene-nav-info\s*\{[^}]*background:var\(--bg\)')
