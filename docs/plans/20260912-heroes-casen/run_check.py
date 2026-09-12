#!/usr/bin/env python3
"""Capture an actual command, its status and a hash-bound log; never infer PASS."""
import argparse
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True)
    parser.add_argument('--task', required=True)
    parser.add_argument('--cwd', type=Path, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.id):
        parser.error('nonempty command and safe id required')
    out = ROOT / 'evidence/checks'
    out.mkdir(parents=True, exist_ok=True)
    log = out / (args.id + '.log')
    receipt = out / (args.id + '.json')
    if receipt.exists() or log.exists():
        parser.error('check ids are immutable; use a new id for each attempt')
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    with log.open('wb') as stream:
        try:
            result = subprocess.run(command, cwd=args.cwd, stdout=stream, stderr=subprocess.STDOUT, check=False)
            code = result.returncode
        except OSError as exc:
            stream.write(str(exc).encode())
            code = 127
    data = {'id': args.id, 'task_id': args.task, 'command': command, 'cwd': str(args.cwd.resolve()),
            'started_at': start, 'seconds': time.monotonic()-before, 'exit_code': code,
            'log': str(log.relative_to(ROOT)), 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
    receipt.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(data, ensure_ascii=False))
    raise SystemExit(code)

if __name__ == '__main__':
    main()
