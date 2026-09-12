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

def local_path(base, value):
    require(isinstance(value, str) and bool(value), 'empty_path')
    path = Path(value)
    require(not path.is_absolute() and '..' not in path.parts, 'unsafe_path')
    result = base / path
    require(result.resolve().is_relative_to(base.resolve()), 'escaping_symlink')
    return result

def validate_receipt(receipt, task, check_files=True):
    require(bool(receipt.get('task_id')), 'missing_task_id')
    require(receipt['task_id'] == task['id'], 'wrong_task_receipt')
    require(bool(receipt.get('checks')), 'empty_checks')
    require(bool(receipt.get('artifacts')), 'empty_artifacts')
    expected = {a['id'] for a in task['acceptance']}
    covered = set()
    for check in receipt['checks']:
        require(type(check.get('exit_code')) is int and check['exit_code'] == 0, 'failed_check')
        require(check.get('task_id') == task['id'], 'wrong_check_task')
        ids = check.get('acceptance_ids')
        require(isinstance(ids, list) and bool(ids) and all(isinstance(x, str) for x in ids), 'missing_acceptance_coverage')
        require(set(ids) <= expected, 'unknown_acceptance_id')
        covered.update(ids)
        require(bool(check.get('command') and check.get('log') and check.get('log_sha256')), 'incomplete_check')
        log = local_path(ROOT, check['log'])
        if check_files:
            require(log.is_file(), 'missing_log')
            require(sha(log) == check['log_sha256'], 'changed_log')
    require(covered == expected, 'incomplete_acceptance_coverage')
    for record in receipt['artifacts']:
        require(bool(record.get('path') and record.get('sha256')), 'incomplete_artifact')
        path = local_path(WORKSPACE, record['path'])
        if check_files:
            require(path.is_file(), 'missing_artifact')
            require(sha(path) == record['sha256'], 'changed_artifact')
    manual = any(a.get('kind') == 'manual_review' for a in task['acceptance'])
    if manual:
        require(receipt.get('kind') == 'manual_review', 'wrong_review_kind')
        require(bool(receipt.get('review_provider') and receipt.get('identity_evidence') and receipt.get('source_digest')), 'missing_review_provenance')
        require(receipt.get('open_p0_p1') is False, 'open_critical_findings')
        manifest_path = local_path(WORKSPACE, receipt.get('source_manifest'))
        source_root = local_path(WORKSPACE, receipt.get('source_root'))
        if check_files:
            frozen = json.loads(manifest_path.read_text())
            manifest = frozen.get('manifest')
            require(isinstance(manifest, dict) and bool(manifest), 'empty_source_manifest')
            digest = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            require(digest == frozen.get('source_digest') == receipt['source_digest'], 'stale_source_digest')
            for relative, expected_sha in manifest.items():
                source = local_path(source_root, relative)
                require(source.is_file() and sha(source) == expected_sha, 'changed_review_source')

def main():
    contract = json.loads((ROOT/'contract.json').read_text())
    states = {'pending':'[ ]', 'in_progress':'[~]', 'partial':'[~]', 'verified':'[x]', 'blocked':'[ghost]', 'incident':'[!]'}
    require(isinstance(contract.get('tasks'), list) and bool(contract['tasks']), 'empty_tasks')
    tasks = {t['id']: t for t in contract['tasks']}
    require(len(tasks) == len(contract['tasks']), 'duplicate_task_id')
    require(set(contract['todo_state']) == set(tasks), 'todo_task_mismatch')
    visited, visiting = set(), set()
    def visit(task_id):
        require(task_id in tasks, 'missing_dependency')
        require(task_id not in visiting, 'dependency_cycle')
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in tasks[task_id].get('depends_on', []):
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in tasks:
        visit(task_id)
    verified=[]
    for task in contract['tasks']:
        acceptance = task.get('acceptance')
        require(isinstance(acceptance, list) and bool(acceptance), 'empty_acceptance')
        ids = [a.get('id') for a in acceptance]
        require(all(isinstance(x, str) and x for x in ids) and len(ids) == len(set(ids)), 'invalid_acceptance_ids')
        require(contract['todo_state'][task['id']] == states[task['status']], 'todo_disagreement')
        if task['status'] == 'verified':
            for dependency in task.get('depends_on', []):
                require(tasks[dependency]['status'] == 'verified' or tasks[dependency].get('optional') is True, 'unverified_dependency')
            path=local_path(ROOT, task['evidence'])
            require(path.is_file(), 'missing_receipt')
            receipt=json.loads(path.read_text())
            require(receipt.get('task_id') == task['id'], 'wrong_task_receipt')
            validate_receipt(receipt, task)
            verified.append(task['id'])
    print(json.dumps({'result':'PASS_CURRENT_EVIDENCE','verified':verified,'pending':[t['id'] for t in contract['tasks'] if t['status']!='verified']}))

if __name__ == '__main__':
    main()
