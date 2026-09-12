"""Synthetic gate assurance only; fixtures are NOT browser measurements."""
import copy
import hashlib
import itertools
import tempfile
import unittest
from pathlib import Path
import verify_runtime_acceptance as gate

class RuntimeContractTest(unittest.TestCase):
    def fixture(self):
        rows=[]
        for pair,page,side,temp in itertools.product(range(1,6),['avaluos-ii','casen-long'],['baseline','candidate'],['cold','warm']):
            rows.append({'pair':pair,'page':page,'side':side,'temperature':temp,'missing':False,
              'metrics':{'lcp_ms':1000,'cls_session_window':0},
              'sample':{'cwv':{'lcp':{'startTime':1000},'fcp':500},'capturedAt':5000,
              'observation':{'shifts':[]},'visibility':'visible',
              'device':{'width':1440,'height':1000,'dpr':1,'theme':'light','userAgent':'SYNTHETIC_ASSURANCE_ONLY'}}})
        return rows

    def test_synthetic_green_is_not_empirical_acceptance(self):
        self.assertEqual(4,len(gate.performance(self.fixture())))

    def test_reject_missing_duplicate_bad_pair_or_hidden(self):
        mutations=[]
        r=self.fixture();r.pop();mutations.append(r)
        r=self.fixture();r[1]=copy.deepcopy(r[0]);mutations.append(r)
        r=self.fixture();r[0]['pair']=True;mutations.append(r)
        r=self.fixture();r[0]['missing']=0;mutations.append(r)
        r=self.fixture();r[0]['missing']=True;mutations.append(r)
        r=self.fixture();r[0]['sample']['visibility']='hidden';mutations.append(r)
        for rows in mutations:
            with self.subTest(rows=rows[0]['sample']['visibility']):
                with self.assertRaises(ValueError):gate.performance(rows)

    def test_reject_null_nan_boolean_and_forged_metric(self):
        for value in [None,float('nan'),True,999]:
            r=self.fixture();r[0]['metrics']['lcp_ms']=value
            with self.subTest(value=value):
                with self.assertRaises(ValueError):gate.performance(r)

    def test_threshold_and_regression_each_bind_independently(self):
        for baseline,candidate in [(2600,2600),(1000,1200)]:
            r=self.fixture()
            for row in r:
                value=baseline if row['side']=='baseline' else candidate
                row['metrics']['lcp_ms']=value;row['sample']['cwv']['lcp']['startTime']=value
            with self.assertRaises(ValueError):gate.performance(r)

    def test_raw_cls_and_device_mismatch(self):
        r=self.fixture();r[0]['sample']['observation']['shifts']=[{'startTime':10,'value':.12}];r[0]['metrics']['cls_session_window']=.12
        with self.assertRaises(ValueError):gate.performance(r)
        r=self.fixture();r[0]['sample']['device']['width']=390
        with self.assertRaises(ValueError):gate.performance(r)
        r=self.fixture();r[0]['metrics']['cls_session_window']=.01
        with self.assertRaises(ValueError):gate.performance(r)

    def test_cls_session_window_not_raw_sum(self):
        self.assertAlmostEqual(.07,gate.cls_window([{'startTime':0,'value':.03},{'startTime':500,'value':.04},{'startTime':2000,'value':.05}]))

    def test_current_hash_and_path_guards(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);f=root/'sample';f.write_text('observed')
            h=hashlib.sha256(f.read_bytes()).hexdigest();gate.file_map({'sample':h},root)
            f.write_text('changed')
            with self.assertRaises(ValueError):gate.file_map({'sample':h},root)
            for mapping in [{},{'../sample':h}]:
                with self.assertRaises(ValueError):gate.file_map(mapping,root)

    def test_observed_ui_and_counterexamples(self):
        directory=gate.PLAN/'evidence/hero-browser-first-person'
        matrix=gate.read(directory/'matrix.json');extras=gate.read(directory/'extras.json')
        self.assertEqual(80,gate.ui(matrix,extras)['matrix'])
        bad=copy.deepcopy(matrix);bad[0]['observed']['h1_count']=True
        with self.assertRaises(ValueError):gate.ui(bad,extras)
        bad=copy.deepcopy(matrix);bad[0]['observed']['disclosure_tag']='DETAILS'
        with self.assertRaises(ValueError):gate.ui(bad,extras)
        bad=copy.deepcopy(matrix);bad[0]['axe']['counts']['incomplete']=1
        with self.assertRaises(ValueError):gate.ui(bad,extras)
        bad=copy.deepcopy(extras);bad[1]=copy.deepcopy(bad[0])
        with self.assertRaises(ValueError):gate.ui(matrix,bad)
        with self.assertRaises(ValueError):gate.ui(matrix[:-1],extras)

    def test_observed_red_pilot_cannot_close_formal_contract(self):
        rows=gate.read(gate.PLAN/'evidence/performance/pilot-valid/runs.json')
        with self.assertRaises(ValueError):gate.performance(rows)

if __name__=='__main__':unittest.main()
