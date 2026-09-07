"""Named scroll containers must expose the corresponding accessibility role."""
from html.parser import HTMLParser
from pathlib import Path
import unittest


class Regions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.named = 0
        self.invalid = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and attrs.get("aria-label"):
            self.named += 1
            allowed = {"region"} if attrs.get("tabindex") == "0" else {"region", "group", "tablist", "img"}
            self.invalid += attrs.get("role") not in allowed


class AccessibleRegionsTest(unittest.TestCase):
    def test_negative_then_recovery(self):
        for role, expected in [("", 1), (' role="region"', 0)]:
            parser = Regions()
            parser.feed(f'<div{role} tabindex="0" aria-label="Scroll chart"></div>')
            self.assertEqual(parser.invalid, expected)

    def test_real_template_is_nonempty_and_valid(self):
        parser = Regions()
        source = Path(__file__).resolve().parents[2] / "catastro_sii_brecha/index.html"
        parser.feed(source.read_text())
        self.assertGreaterEqual(parser.named, 14)
        self.assertEqual(parser.invalid, 0)

    def test_noninteractive_named_group_negative_then_recovery(self):
        for role, expected in [("", 1), (' role="group"', 0)]:
            parser = Regions()
            parser.feed(f'<div{role} aria-label="Column dictionary"></div>')
            self.assertEqual(parser.invalid, expected)
