"""Independent source comparisons and falsifiable presentation constraints."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/catastro_sii'))
from render_casen_shared_site import SOURCE, FREEZE, REVIEW, load_source, validate_source, plotted_rows, percent, ci_label, reviewed_binding, make_figure
from editorial_style import editorial_style
import matplotlib.pyplot as plt


class CasenFigureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text())
        cls.images=ROOT/'assets/images/avaluos-ii'

    def altered(self):return copy.deepcopy(self.source)

    def test_accepted_digest_and_independent_values(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce')
        self.assertEqual(reviewed_binding(SOURCE),'14eaab859814dda0d89066b79c7b395b8e1cbb3e90aa7e65f5f080fe3dddec80')
        # Values independently transcribed from D2-approved source, never drawing helpers.
        rows=plotted_rows(self.source)
        self.assertEqual(rows[0]['estimate'],0.01087822201092484)
        self.assertEqual(rows[0]['n_valid'],78654)
        self.assertEqual(rows[-2]['estimate'],0.09268113577023498)
        self.assertEqual(rows[-1]['estimate'],0.0859948617877048)
        self.assertEqual([r['n_valid'] for r in rows[-2:]],[1329,1608])

    def test_exported_rows_equal_source_and_geographic_order(self):
        exported=json.loads((self.images/'casen-shared-site-data.json').read_text())['rows']
        codes=['CL','15','1','2','3','4','5','13','6','7','16','8','9','14','10','11','12','5101','5109']
        source_by_key={(r['scope'],r['territory_code']):r for r in self.source['rows']}
        scopes=['national']+['region']*16+['commune']*2
        self.assertEqual(exported,[source_by_key[(scope,code)] for scope,code in zip(scopes,codes)])
        self.assertEqual(len(exported),19)
        with (self.images/'casen-shared-site-data.csv').open() as f: csv_rows=list(csv.DictReader(f))
        self.assertEqual([r['territory_code'] for r in csv_rows],codes)
        for expected,actual in zip(exported,csv_rows):
            self.assertEqual(float(actual['estimate']),expected['estimate'])
            self.assertEqual(actual['ci_low'],'' if expected['ci_low'] is None else str(expected['ci_low']))

    def test_observed_zero_and_one_without_ci_remain_observed(self):
        for p in (0.0,1.0):
            source=self.altered();row=source['rows'][0]
            row.update(estimate=p,se=None,ci_low=None,ci_high=None,ci_status='not_conclusive_boundary_or_degenerate')
            validate_source(source)
            self.assertEqual(plotted_rows(source)[0]['estimate'],p)
            self.assertEqual(percent(p,'en'),'0.00%' if p==0 else '100.00%')
            self.assertEqual(ci_label(row,'en'),'Not conclusive')
            row.update(se=0,ci_low=p,ci_high=p,ci_status='approximate_normal_95_taylor')
            with self.assertRaisesRegex(ValueError,'confidence interval'):validate_source(source)

    def test_missing_sample_and_empty_domain_are_not_zero(self):
        source=self.altered();row=next(r for r in source['rows'] if r['territory_code']=='5101')
        row.update(estimate=None,weighted_denominator=0,n_households=0,n_valid=0,n_missing=0,n_flagged=0,ci_status='no_sample')
        validate_source(source)
        self.assertIsNone(plotted_rows(source)[-2]['estimate'])
        self.assertEqual(percent(row['estimate'],'es'),'Sin dato')
        self.assertEqual(ci_label(row,'es'),'Sin muestra')
        row['estimate']=0
        with self.assertRaises(ValueError):validate_source(source)
        source=self.altered();row=source['rows'][0]
        row.update(estimate=None,weighted_denominator=0,n_valid=0,n_missing=row['n_households'],ci_low=None,ci_high=None,se=None,ci_status='not_estimable_empty_domain')
        validate_source(source)
        self.assertIsNone(plotted_rows(source)[0]['estimate'])
        self.assertEqual(ci_label(row,'en'),'No valid data')

    def test_actual_marks_distinguish_zero_from_missing(self):
        for observed in (True,False):
            source=self.altered();row=source['rows'][0]
            row.update(estimate=0.0 if observed else None,se=None,ci_low=None,ci_high=None,
                       ci_status='not_conclusive_boundary_or_degenerate' if observed else 'not_estimable_empty_domain')
            if not observed:
                row.update(weighted_denominator=0,n_valid=0,n_missing=row['n_households'])
            with editorial_style('light') as colors:
                fig,_=make_figure(plotted_rows(source),'en',colors)
                # Inspect actual plotted marks at the national source row y=0.
                points=[line for line in fig.axes[0].lines if list(line.get_ydata())==[0]]
                self.assertEqual(len(points),1 if observed else 0)
                if observed:self.assertEqual(list(points[0].get_xdata()),[0.0])
                self.assertIn('0.00%' if observed else 'No data',[t.get_text() for t in fig.texts])
                plt.close(fig)

    def test_singleton_keeps_estimate_without_interval(self):
        source=self.altered();row=source['rows'][0];expected=row['estimate']
        row.update(ci_status='not_estimable_singleton',se=None,ci_low=None,ci_high=None)
        validate_source(source)
        self.assertEqual(plotted_rows(source)[0]['estimate'],expected)
        self.assertEqual(ci_label(row,'en'),'Not estimable')

    def test_invalid_ci_bounds_and_nonfinite_values_rejected(self):
        for field,value in [('ci_low',-.1),('ci_low',.5),('ci_high',1.1),('ci_high',0),('se',None),('estimate',None),('estimate',float('nan')),('estimate',True)]:
            source=self.altered();source['rows'][0][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):validate_source(source)

    def test_communal_ci_wrong_units_weights_and_raw_fields_rejected(self):
        for change in ({'ci_low':0,'ci_high':1},{'ci_status':'approximate_normal_95_taylor'},{'unit':'dwelling'},{'weight':'expr'},{'folio':'DO_NOT_EXPORT'}):
            source=self.altered();row=next(r for r in source['rows'] if r['territory_code']=='5101');row.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):validate_source(source)

    def test_missing_region_duplicate_and_count_identity_rejected(self):
        source=self.altered();source['rows']=[r for r in source['rows'] if not(r['scope']=='region' and r['territory_code']=='15')]
        with self.assertRaises(ValueError):validate_source(source)
        source=self.altered();source['rows'].append(source['rows'][0])
        with self.assertRaises(ValueError):validate_source(source)
        source=self.altered();source['rows'][0]['n_missing']=1
        with self.assertRaises(ValueError):validate_source(source)

    def test_hash_and_review_binding_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'hash mismatch'):load_source(SOURCE,'0'*64)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'review.json';review=json.loads(REVIEW.read_text());review['open_p0_p1']=True;path.write_text(json.dumps(review))
            with self.assertRaisesRegex(ValueError,'Review is open'):reviewed_binding(SOURCE,FREEZE,path)
            review['open_p0_p1']=False;review['source_digest']='0'*64;path.write_text(json.dumps(review))
            with self.assertRaises(ValueError):reviewed_binding(SOURCE,FREEZE,path)

    def test_rendered_labels_and_portable_fonts(self):
        ns={'svg':'http://www.w3.org/2000/svg'}
        for lang in ('es','en'):
            for suffix in ('','-dark'):
                path=self.images/f'casen-shared-site-{lang}{suffix}.svg';raw=path.read_text();root=ET.fromstring(raw)
                self.assertEqual(root.get('width'),'864pt')
                self.assertEqual(root.get('height'),'964.8pt')
                self.assertLessEqual(path.stat().st_size,100000)
                self.assertIn('data:font/woff2;base64,',raw)
                texts=[''.join(node.itertext()) for node in root.findall('.//svg:text',ns)]
                for row in json.loads((self.images/'casen-shared-site-data.json').read_text())['rows']:
                    expected=f"{row['estimate']*100:.2f}%"
                    if lang=='es':expected=expected.replace('.',',')
                    self.assertIn(expected,texts)
                self.assertEqual(texts.count('Sin IC comunal' if lang=='es' else 'No communal CI'),2)

    def test_fiscal_sources_untouched_and_public_provenance(self):
        baseline=json.loads((ROOT/'docs/plans/20260912-heroes-casen/evidence/baseline.json').read_text());count=0
        for key,details in baseline['files'].items():
            if '/artifacts/fiscal_gap/' in key:
                path=SOURCE.parent.parent/'fiscal_gap'/Path(key).name
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),details['sha256']);count+=1
        self.assertEqual(count,9)
        raw=(self.images/'casen-shared-site-provenance.json').read_text();provenance=json.loads(raw)
        self.assertNotIn('/home/',raw);self.assertFalse(provenance['communal_representativeness'])
        self.assertEqual(provenance['source_estimates_sha256'],hashlib.sha256(SOURCE.read_bytes()).hexdigest())


if __name__=='__main__':unittest.main()
