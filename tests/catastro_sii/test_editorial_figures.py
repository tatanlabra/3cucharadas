"""Source-row oracles and rejection cases for the aggregate-only renderers."""
import copy
import base64
from io import BytesIO
import re
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts/catastro_sii'))
from render_gap_figures import SOURCE, load_source, ranked, validate_rows, number
from editorial_style import THEMES, contrast, SVG_FONT_FAMILY, svg_text_by_weight, subset_woff2
from modeled_fiscal_projection import validate_modeled


class EditorialFiguresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_source()
        cls.rows = cls.source['communes']

    def test_frozen_source_binding(self):
        baseline = json.loads((ROOT/'docs/plans/20260912-heroes-casen/evidence/baseline.json').read_text())
        matched = 0
        for key, details in baseline['files'].items():
            if '/artifacts/fiscal_gap/' in key:
                path = SOURCE.parent/Path(key).name
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), details['sha256'], key)
                matched += 1
        self.assertGreaterEqual(matched, 9)

    def test_selected_source_values_independent_oracle(self):
        selected = ranked(self.rows)
        # Independently recorded from frozen canonical rows, not figure geometry.
        self.assertEqual([r['comuna'] for r in selected], [
            'Valparaíso', 'Puerto Montt', 'Los Ángeles', 'Valdivia', 'Villarrica',
            'Santiago', 'Arica', 'Iquique', 'Temuco', 'Melipilla', 'Viña del Mar',
            'Recoleta', 'Calama', 'Coquimbo', 'Padre Las Casas'])
        self.assertEqual([r['camp_sensitivity_positive_gap'] for r in selected],
                         [29961,28404,27175,20631,19977,19466,19022,18949,17563,16501,16016,15502,15211,14421,14361])
        self.assertEqual(selected[0]['signed_gap'], 32533)
        self.assertAlmostEqual(selected[0]['materiality_acceptable_scenario'], 25550.993869383816)
        self.assertEqual(selected[10]['camp_absorbed_positive_gap'], 8014)
        self.assertEqual(len(self.rows), 346)

    def fixture(self):
        return [dict(codigo_comuna='1', comuna='Fixture', source_available=True,
                     signed_gap=100, camp_sensitivity_positive_gap=80,
                     camp_absorbed_positive_gap=20, materiality_acceptable_scenario=60,
                     materiality_other_scenario=20)]

    def test_invalid_nesting_rejected(self):
        for key, value in [('camp_sensitivity_positive_gap',101), ('camp_absorbed_positive_gap',19),
                           ('materiality_acceptable_scenario',81), ('materiality_other_scenario',19)]:
            with self.subTest(key=key):
                rows = self.fixture(); rows[0][key] = value
                with self.assertRaises(ValueError): validate_rows(rows)

    def test_missing_nonfinite_residual_never_becomes_zero(self):
        for value in (None, float('nan'), float('inf'), True):
            rows = self.fixture(); rows[0]['camp_sensitivity_positive_gap'] = value
            with self.subTest(value=value), self.assertRaises(ValueError): validate_rows(rows)

    def test_missing_materiality_remains_unknown(self):
        rows = self.fixture()
        rows[0]['materiality_acceptable_scenario'] = None
        with self.assertRaises(ValueError): validate_rows(rows)
        rows[0]['materiality_other_scenario'] = None
        self.assertIsNone(ranked(rows)[0]['materiality_acceptable_scenario'])
        self.assertEqual(number(None, 'es'), '—')
        self.assertEqual(number(0, 'es'), '0')

    def test_negative_gap_preserved_and_only_positive_residual_ranked(self):
        rows = self.fixture(); negative = copy.deepcopy(rows[0]); negative.update(
            codigo_comuna='2', signed_gap=-10, camp_sensitivity_positive_gap=0,
            camp_absorbed_positive_gap=0, materiality_acceptable_scenario=0, materiality_other_scenario=0)
        rows.append(negative)
        validate_rows(rows)
        self.assertEqual(negative['signed_gap'], -10)
        self.assertEqual(len(ranked(rows)), 1)

    def test_duplicate_empty_and_no_positive_sources_rejected(self):
        for rows in ([], self.fixture()*2):
            with self.assertRaises(ValueError): validate_rows(rows)
        rows = self.fixture(); rows[0]['source_available'] = False
        with self.assertRaises(ValueError): ranked(rows)

    def test_frozen_hash_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            load_source(SOURCE, '0'*64)

    def test_legible_text_and_nontext_colors(self):
        for name, colors in THEMES.items():
            for key in ('ink', 'muted'):
                self.assertGreaterEqual(contrast(colors[key], colors['surface']),4.5,(name,key))
            for key in ('track', 'residual', 'material'):
                self.assertGreaterEqual(contrast(colors[key], colors['surface']),3,(name,key))

    def test_monetary_source_oracle_and_rejections(self):
        top = validate_modeled(self.source)
        self.assertEqual(top[0]['comuna'], 'Lo Barnechea')
        self.assertAlmostEqual(top[0]['modeled_gap_mean_clp']/1e6, 6669.222406430229)
        self.assertAlmostEqual(top[1]['modeled_gap_median_clp']/1e6, 450.6057550121401)
        for bad in (None, float('nan'), -1, 1):
            source = copy.deepcopy(self.source)
            row = next(r for r in source['communes'] if r['codigo_comuna'] == '13115')
            row['modeled_gap_median_clp'] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): validate_modeled(source)

    def test_rendered_svg_has_source_labels_and_values(self):
        # Actual exported artifact, independent of Matplotlib drawing helpers.
        ns = {'svg':'http://www.w3.org/2000/svg'}
        for lang in ('es','en'):
            for suffix in ('','-dark'):
                path = ROOT/f'assets/images/avaluos-ii/gap-top15-{lang}{suffix}.svg'
                svg = ET.parse(path).getroot()
                text = [''.join(node.itertext()) for node in svg.findall('.//svg:text',ns)]
                self.assertEqual(svg.get('width'), '864pt')
                for row in ranked(self.rows):
                    self.assertIn(row['comuna'],text)
                    # Independent formatting of canonical observed values.
                    expected = format(row['camp_sensitivity_positive_gap'],',')
                    if lang == 'es': expected = expected.replace(',','.')
                    self.assertIn(expected,text)
                self.assertIn('≈ 25.551' if lang == 'es' else '≈ 25,551',text)
                self.assertIsNotNone(svg.find('svg:desc',ns))

    def assert_embedded_font_contract(self, svg):
        from fontTools.ttLib import TTFont
        used = svg_text_by_weight(svg)
        faces = re.findall(r"font-weight:(400|700);src:url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)", svg)
        self.assertEqual({int(weight) for weight, _ in faces}, {weight for weight, chars in used.items() if chars})
        for weight, encoded in faces:
            payload = base64.b64decode(encoded, validate=True)
            self.assertEqual(payload[:4], b'wOF2')
            font = TTFont(BytesIO(payload))
            self.assertTrue({ord(c) for c in used[int(weight)]} <= set(font.getBestCmap()))
            self.assertEqual(font['name'].getDebugName(1), SVG_FONT_FAMILY)
            self.assertIn('Mozilla Foundation', font['name'].getDebugName(0))
            self.assertIn('Open Font License', font['name'].getDebugName(13))
            self.assertIn('OFL', font['name'].getDebugName(14))
            self.assertNotIn('Fira', font['name'].getDebugName(6))

    def test_all_exported_svg_fonts_self_contained_under_100kb(self):
        paths = list((ROOT/'assets/images/avaluos-ii').glob('gap-top15-*.svg'))
        paths += list((ROOT/'assets/images/avaluos-ii').glob('monetary-top15-*.svg'))
        self.assertEqual(len(paths), 8)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertLessEqual(path.stat().st_size, 100000)
                self.assert_embedded_font_contract(path.read_text())

    def test_font_gate_rejects_missing_embedding_and_missing_glyphs(self):
        svg = (ROOT/'assets/images/avaluos-ii/gap-top15-es.svg').read_text()
        missing_face = re.sub(r'<style[^>]+id="embedded-editorial-fonts".*?</style>', '', svg)
        with self.assertRaises(AssertionError): self.assert_embedded_font_contract(missing_face)
        # A decodable font is insufficient: deliberately omit every glyph except A.
        payload = base64.b64encode(subset_woff2({'A'},400)).decode('ascii')
        missing_glyphs = re.sub(r'(font-weight:400;src:url\(data:font/woff2;base64,)[A-Za-z0-9+/=]+',
                               lambda match: match[1]+payload, svg)
        with self.assertRaises(AssertionError): self.assert_embedded_font_contract(missing_glyphs)

    def test_subsetting_is_deterministic_and_missing_glyph_rejected(self):
        self.assertEqual(subset_woff2(set('Á≈−A1'),400), subset_woff2(set('1A−≈Á'),400))
        with self.assertRaisesRegex(ValueError, 'lacks required'):
            subset_woff2({'\U0010ffff'},400)

    def test_english_and_spanish_number_format(self):
        self.assertEqual(number(25550.993869383816,'es'),'25.551')
        self.assertEqual(number(25550.993869383816,'en'),'25,551')


if __name__ == '__main__': unittest.main()
