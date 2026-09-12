import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('verify_fiscal_gap', ROOT/'scripts/catastro_sii/verify_fiscal_gap.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ModelCrossArtifactTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'catastro_sii_brecha/data/fiscal-gap/communes.json').read_text())

    def test_canonical(self):
        self.assertEqual(len(module.verify_modeled(self.data['communes'],self.data['metadata'])),15)

    def test_corruptions_fail_closed(self):
        for field,value in [('modeled_gap_mean_clp',-1),('modeled_q05_mean_clp',1),('modeled_positive_share',2),('modeled_median_annual_clp',None)]:
            with self.subTest(field=field):
                data=copy.deepcopy(self.data)
                row=next(r for r in data['communes'] if r['modeled_tax_status']=='available' and r['camp_sensitivity_positive_gap']>0)
                row[field]=value
                with self.assertRaises(ValueError): module.verify_modeled(data['communes'],data['metadata'])

    def test_unknown_is_not_zero(self):
        row=next(r for r in self.data['communes'] if not r['source_available'])
        row['modeled_gap_mean_clp']=0
        with self.assertRaises(ValueError): module.verify_modeled(self.data['communes'],self.data['metadata'])

    def test_rule_and_ranking_changes_rejected(self):
        self.data['metadata']['modeled_tax_model']['unit']='CLP_net_annual'
        with self.assertRaises(ValueError): module.verify_modeled(self.data['communes'],self.data['metadata'])


if __name__=='__main__': unittest.main()
