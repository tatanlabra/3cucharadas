#!/usr/bin/env python3
"""Verify completed-task receipts, current artifacts and derived TODO state."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[4]

def require(condition, why):
    if not condition:
        raise ValueError(why)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_receipt(receipt, check_files=True):
    require(bool(receipt.get('task_id')), 'missing_task_id')
    require(bool(receipt.get('checks')), 'empty_checks')
    require(bool(receipt.get('artifacts')), 'empty_artifacts')
    for check in receipt['checks']:
        require(check.get('exit_code') == 0, 'failed_check')
        require(bool(check.get('command') and check.get('log') and check.get('log_sha256')), 'incomplete_check')
        if check_files:
            log = ROOT / check['log']
            require(log.is_file(), 'missing_log')
            require(sha(log) == check['log_sha256'], 'changed_log')
    for record in receipt['artifacts']:
        require(bool(record.get('path') and record.get('sha256')), 'incomplete_artifact')
        if check_files:
            path = WORKSPACE / record['path']
            require(path.is_file(), 'missing_artifact')
            require(sha(path) == record['sha256'], 'changed_artifact')
    if receipt.get('kind') == 'manual_review':
        require(bool(receipt.get('review_provider') and receipt.get('identity_evidence') and receipt.get('source_digest')), 'missing_review_provenance')
        require(not receipt.get('open_p0_p1'), 'open_critical_findings')

def main():
    contract = json.loads((ROOT/'contract.json').read_text())
    states = {'pending':'[ ]', 'in_progress':'[~]', 'partial':'[~]', 'verified':'[x]', 'blocked':'[ghost]', 'incident':'[!]'}
    verified=[]
    for task in contract['tasks']:
        require(contract['todo_state'][task['id']] == states[task['status']], 'todo_disagreement')
        if task['status'] == 'verified':
            path=ROOT/task['evidence']
            require(path.is_file(), 'missing_receipt')
            receipt=json.loads(path.read_text())
            require(receipt.get('task_id') == task['id'], 'wrong_task_receipt')
            validate_receipt(receipt)
            verified.append(task['id'])
    print(json.dumps({'result':'PASS_CURRENT_EVIDENCE','verified':verified,'pending':[t['id'] for t in contract['tasks'] if t['status']!='verified']}))

if __name__ == '__main__':
    main()
