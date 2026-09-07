"""Regression for the observed light dictionary contrast failure (4.49:1)."""
from pathlib import Path
import re
import unittest


def luminance(rgb):
    linear = [(v / 255 / 12.92 if v / 255 <= .04045 else ((v / 255 + .055) / 1.055) ** 2.4) for v in rgb]
    return sum(v * weight for v, weight in zip(linear, [.2126, .7152, .0722]))


def contrast(foreground, background):
    values = sorted([luminance(foreground), luminance(background)])
    return (values[1] + .05) / (values[0] + .05)


class DictionaryContrastTest(unittest.TestCase):
    def test_light_muted_has_margin_on_the_observed_field_background(self):
        css = (Path(__file__).resolve().parents[2] / 'catastro_sii_brecha/style.css').read_text()
        light = re.search(r':root\[data-theme="light"\]\s*\{([^}]+)\}', css)[1]
        token = re.search(r'--muted:\s*#([0-9a-f]{6})', light)[1]
        rgb = [int(token[i:i + 2], 16) for i in [0, 2, 4]]
        self.assertLess(contrast([97, 113, 138], [237, 242, 249]), 4.5)
        self.assertGreaterEqual(contrast(rgb, [237, 242, 249]), 4.5)

    def test_light_heading_gradient_uses_text_accent_tokens(self):
        css = (Path(__file__).resolve().parents[2] / 'catastro_sii_brecha/style.css').read_text()
        rule = re.search(r':root\[data-theme="light"\] \.lead-accent\s*\{([^}]+)\}', css)
        self.assertIsNotNone(rule, 'Bright night gradient is illegible on light cards')
        self.assertIn('var(--acid-text)', rule[1])
        self.assertIn('var(--cyan-text)', rule[1])
        self.assertIn('var(--ink-soft)', rule[1])
        self.assertIn('background-image:', rule[1], 'Do not reset background-clip: text through shorthand')
        for color in [[63, 107, 0], [5, 103, 124], [50, 67, 93]]:
            self.assertGreaterEqual(contrast(color, [246, 248, 252]), 4.5)
        self.assertLess(contrast([214, 255, 144], [246, 248, 252]), 3)

    def test_dark_hero_hint_does_not_inherit_light_muted_token(self):
        css = (Path(__file__).resolve().parents[2] / 'catastro_sii_brecha/style.css').read_text()
        self.assertRegex(css, r'\.hero \.hint\s*\{\s*color:\s*var\(--hero-sub\);\s*\}')

    def test_inactive_light_tabs_keep_readable_labels(self):
        css = (Path(__file__).resolve().parents[2] / 'catastro_sii_brecha/style.css').read_text()
        self.assertRegex(css, r':root\[data-theme="light"\] \.lab-tabs button\s*\{\s*color:\s*var\(--ink-soft\);\s*\}')

    def test_observed_failure_and_recovery(self):
        self.assertLess(contrast([97, 113, 138], [240, 244, 250]), 4.5)
        self.assertGreaterEqual(contrast([50, 67, 93], [240, 244, 250]), 4.5)

    def test_scoped_rule_uses_contrasting_existing_token(self):
        css = (Path(__file__).resolve().parents[2] / 'catastro_sii_brecha/style.css').read_text()
        rule = re.search(r':root\[data-theme="light"\] \.dictionary-grid p\s*\{([^}]+)\}', css)
        self.assertIsNotNone(rule, 'light-only dictionary contrast correction is required')
        self.assertRegex(rule[1], r'color:\s*var\(--ink-soft\)')
        light = re.search(r':root\[data-theme="light"\]\s*\{([^}]+)\}', css)[1]
        token = re.search(r'--ink-soft:\s*#([0-9a-f]{6})', light)[1]
        rgb = [int(token[i:i + 2], 16) for i in [0, 2, 4]]
        self.assertGreaterEqual(contrast(rgb, [240, 244, 250]), 4.5)
