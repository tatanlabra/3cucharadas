"""CLI contract assurance using isolated synthetic receipts; never edits live evidence.

Normal use: python -m unittest discover -s docs/plans/20260912-heroes-casen
  -p test_execution_evidence.py -v
EXECUTION_VERIFIER_SOURCE may select a frozen verifier snapshot for red replay.
CONTRACT_ASSURANCE_RECORD optionally writes machine-readable observations.
These fixtures check receipt integrity and binding, not substantive review quality.
"""
from pathlib import Path
import atexit
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

PLAN=Path(__file__).resolve().parent
TARGET=Path(os.environ.get('EXECUTION_VERIFIER_SOURCE',str(PLAN/'verify_execution.py')))
VERIFIER_SOURCE=TARGET.read_bytes() # One immutable version for the entire suite.
VERIFIER_HASH=hashlib.sha256(VERIFIER_SOURCE).hexdigest()
OBSERVATIONS=[]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical_digest(manifest):
    return digest(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode())

@atexit.register
def record():
    path=os.environ.get('CONTRACT_ASSURANCE_RECORD')
    if path:
        Path(path).write_text(json.dumps({'verifier_sha256':VERIFIER_HASH,
            'test_suite_sha256':digest(Path(__file__).read_bytes()),
            'scope':'Synthetic CLI receipts only; no review quality or performance certification',
            'observations':OBSERVATIONS},indent=2)+'\n')

class IsolatedCLI(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='contract-assurance-')
        self.addCleanup(self.temp.cleanup)
        self.workspace=Path(self.temp.name)/'workspace'
        self.plan=self.workspace/'activos/blog/docs/plans/fixture-plan'
        self.plan.mkdir(parents=True)
        (self.plan/'verify_execution.py').write_bytes(VERIFIER_SOURCE)
        self.input=self.workspace/'inputs/source.txt'
        self.input.parent.mkdir();self.input.write_text('approved input v1\n')
        self.log=self.plan/'check.log';self.log.write_text('Synthetic fixture check completed\n')
        self.artifact=self.workspace/'outputs/result.txt'
        self.artifact.parent.mkdir();self.artifact.write_text('synthetic aggregate result\n')
        self.acceptance=[{'id':'AC-A1','kind':'shell','command':'fixture-check-one','cwd':'blog_repo'},
                         {'id':'AC-A2','kind':'shell','command':'fixture-check-two','cwd':'blog_repo'}]
        self.receipt={'task_id':'A','kind':'shell','checks':[self.check('A',['AC-A1']),self.check('A',['AC-A2'])],
                      'artifacts':[{'path':'outputs/result.txt','sha256':digest(self.artifact.read_bytes())}]}
        self.task={'id':'A','status':'verified','evidence':'receipt-A.json','depends_on':[],
                   'acceptance':copy.deepcopy(self.acceptance),'optional':False}
        self.contract={'schema_version':1,'id':'synthetic-assurance','tasks':[self.task],'todo_state':{'A':'[x]'}}
        self.receipts={'A':self.receipt}

    def check(self,task,ids):
        return {'id':'synthetic-'+ids[0], 'task_id':task,'acceptance_ids':ids,'command':['fixture-check'],
                'exit_code':0,'log':'check.log','log_sha256':digest(self.log.read_bytes())}

    def manual(self):
        self.task['acceptance']=[{'id':'AC-A1','kind':'manual_review','digest_check':{
            'algorithm':'sha256','compare':'source_digest against current frozen source manifest'}}]
        self.receipt.update(kind='manual_review',checks=[self.check('A',['AC-A1'])],
                            review_provider='synthetic-provider',identity_evidence='synthetic identity receipt; not a real model review',
                            open_p0_p1=False,source_manifest='inputs/manifest.json',source_root='inputs')
        manifest={'source.txt':digest(self.input.read_bytes())}
        self.source_digest=canonical_digest(manifest)
        (self.input.parent/'manifest.json').write_text(json.dumps({'manifest':manifest,'source_digest':self.source_digest}))
        self.receipt['source_digest']=self.source_digest

    def add_dependency(self,status='verified'):
        dependency=copy.deepcopy(self.task)
        dependency.update(id='B',status=status,evidence='receipt-B.json',acceptance=[{'id':'AC-B1','kind':'shell'}])
        self.contract['tasks'].append(dependency)
        self.contract['todo_state']['B']='[x]' if status=='verified' else '[ ]'
        self.receipts['B']={'task_id':'B','kind':'shell','checks':[self.check('B',['AC-B1'])],
                            'artifacts':copy.deepcopy(self.receipt['artifacts'])}
        self.task['depends_on']=['B']
        return dependency

    def run_cli(self,expected):
        (self.plan/'contract.json').write_text(json.dumps(self.contract))
        for task,receipt in self.receipts.items():
            (self.plan/('receipt-'+task+'.json')).write_text(json.dumps(receipt))
        r=subprocess.run([sys.executable,str(self.plan/'verify_execution.py')],cwd=self.workspace,
                         capture_output=True,text=True,timeout=15)
        def clean(text):return text.replace(str(Path(self.temp.name)),'<isolated-fixture>')
        OBSERVATIONS.append({'test':self.id().split('.')[-1],'expected':expected,
                             'exit_code':r.returncode,'stdout':clean(r.stdout),'stderr':clean(r.stderr),
                             'expectation_met':(r.returncode==0)==(expected=='accept')})
        if expected=='accept':
            self.assertEqual(r.returncode,0,clean(r.stderr))
            self.assertEqual(json.loads(r.stdout)['result'],'PASS_CURRENT_EVIDENCE')
        else:
            self.assertNotEqual(r.returncode,0,'Verifier accepted a forbidden fixture: '+clean(r.stdout))

    def test_valid_shell_receipt_accepts(self):self.run_cli('accept')
    def test_valid_manual_current_digest_accepts(self):self.manual();self.run_cli('accept')
    def test_one_check_may_cover_multiple_acceptance_ids(self):
        self.receipt['checks']=[self.check('A',['AC-A1','AC-A2'])];self.run_cli('accept')
    def test_repeated_coverage_is_allowed(self):
        self.receipt['checks'].append(self.check('A',['AC-A1']));self.run_cli('accept')
    def test_verified_dependency_accepts(self):self.add_dependency();self.run_cli('accept')
    def test_explicit_optional_pending_dependency_accepts(self):
        self.add_dependency(status='pending')['optional']=True;self.run_cli('accept')

    def test_failed_check_rejected(self):self.receipt['checks'][0]['exit_code']=1;self.run_cli('reject')
    def test_missing_exit_code_rejected(self):del self.receipt['checks'][0]['exit_code'];self.run_cli('reject')
    def test_missing_command_rejected(self):del self.receipt['checks'][0]['command'];self.run_cli('reject')
    def test_empty_checks_rejected(self):self.receipt['checks']=[];self.run_cli('reject')
    def test_missing_checks_rejected(self):del self.receipt['checks'];self.run_cli('reject')
    def test_empty_artifacts_rejected(self):self.receipt['artifacts']=[];self.run_cli('reject')
    def test_missing_artifacts_rejected(self):del self.receipt['artifacts'];self.run_cli('reject')
    def test_changed_artifact_rejected(self):self.artifact.write_text('tampered\n');self.run_cli('reject')
    def test_missing_artifact_rejected(self):self.artifact.unlink();self.run_cli('reject')
    def test_changed_log_rejected(self):self.log.write_text('tampered\n');self.run_cli('reject')
    def test_missing_log_rejected(self):self.log.unlink();self.run_cli('reject')
    def test_wrong_receipt_task_binding_rejected_by_cli(self):self.receipt['task_id']='B';self.run_cli('reject')
    def test_todo_disagreement_rejected(self):self.contract['todo_state']['A']='[ ]';self.run_cli('reject')
    def test_missing_task_receipt_rejected(self):self.task['evidence']='missing.json';self.run_cli('reject')

    def test_wrong_check_task_binding_rejected(self):self.receipt['checks'][0]['task_id']='B';self.run_cli('reject')
    def test_missing_check_task_binding_rejected(self):del self.receipt['checks'][0]['task_id'];self.run_cli('reject')
    def test_missing_acceptance_coverage_rejected(self):self.receipt['checks'].pop();self.run_cli('reject')
    def test_absent_acceptance_ids_rejected(self):
        for check in self.receipt['checks']:del check['acceptance_ids']
        self.run_cli('reject')
    def test_unknown_acceptance_id_rejected(self):self.receipt['checks'][0]['acceptance_ids'].append('AC-UNRELATED');self.run_cli('reject')
    def test_empty_acceptance_ids_rejected(self):self.receipt['checks'][0]['acceptance_ids']=[];self.run_cli('reject')
    def test_acceptance_ids_string_rejected(self):self.receipt['checks'][0]['acceptance_ids']='AC-A1';self.run_cli('reject')
    def test_no_contract_acceptance_rejected(self):self.task['acceptance']=[];self.run_cli('reject')
    def test_missing_dependency_rejected(self):self.task['depends_on']=['UNKNOWN'];self.run_cli('reject')
    def test_unverified_dependency_rejected(self):self.add_dependency(status='pending');self.run_cli('reject')
    def test_dependency_cycle_rejected(self):self.add_dependency()['depends_on']=['A'];self.run_cli('reject')
    def test_duplicate_task_ids_rejected(self):self.contract['tasks'].append(copy.deepcopy(self.task));self.run_cli('reject')
    def test_empty_task_collection_rejected(self):self.contract['tasks']=[];self.contract['todo_state']={};self.run_cli('reject')

    def test_stale_manual_receipt_digest_rejected(self):self.manual();self.receipt['source_digest']='0'*64;self.run_cli('reject')
    def test_changed_manual_source_rejected(self):self.manual();self.input.write_text('new source\n');self.run_cli('reject')
    def test_missing_manual_manifest_rejected(self):self.manual();(self.input.parent/'manifest.json').unlink();self.run_cli('reject')
    def test_empty_manual_manifest_rejected(self):
        self.manual();empty={};h=canonical_digest(empty)
        (self.input.parent/'manifest.json').write_text(json.dumps({'manifest':empty,'source_digest':h}))
        self.receipt['source_digest']=h;self.run_cli('reject')
    def test_manual_kind_cannot_be_bypassed(self):
        self.manual();self.receipt['kind']='shell';self.receipt.pop('source_digest');self.receipt.pop('identity_evidence');self.run_cli('reject')
    def test_open_critical_findings_rejected(self):self.manual();self.receipt['open_p0_p1']=True;self.run_cli('reject')
    def test_missing_review_identity_rejected(self):self.manual();self.receipt.pop('identity_evidence');self.run_cli('reject')

    def test_boolean_exit_code_is_not_integer_zero(self):self.receipt['checks'][0]['exit_code']=False;self.run_cli('reject')
    def test_absolute_artifact_path_rejected(self):self.receipt['artifacts'][0]['path']=str(self.artifact);self.run_cli('reject')
    def test_artifact_traversal_rejected(self):self.receipt['artifacts'][0]['path']='outputs/../outputs/result.txt';self.run_cli('reject')
    def test_absolute_log_path_rejected(self):self.receipt['checks'][0]['log']=str(self.log);self.run_cli('reject')
    def test_absolute_receipt_path_rejected(self):self.task['evidence']=str(self.plan/'receipt-A.json');self.run_cli('reject')
    def test_source_manifest_traversal_rejected(self):self.manual();self.receipt['source_manifest']='inputs/../inputs/manifest.json';self.run_cli('reject')

    def test_artifact_symlink_escape_rejected(self):
        outside=Path(self.temp.name)/'outside.txt';outside.write_text(self.artifact.read_text())
        self.artifact.unlink();self.artifact.symlink_to(outside);self.run_cli('reject')
    def test_log_symlink_escape_rejected(self):
        outside=Path(self.temp.name)/'outside.log';outside.write_text(self.log.read_text())
        self.log.unlink();self.log.symlink_to(outside);self.run_cli('reject')
    def test_review_source_symlink_escape_rejected(self):
        self.manual();outside=Path(self.temp.name)/'outside-source.txt';outside.write_text(self.input.read_text())
        self.input.unlink();self.input.symlink_to(outside);self.run_cli('reject')

if __name__=='__main__':unittest.main(verbosity=2)
