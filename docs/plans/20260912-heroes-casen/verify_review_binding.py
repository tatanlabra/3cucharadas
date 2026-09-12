#!/usr/bin/env python3
"""Check a review's declared scope against current files; not a quality judge."""
import argparse
import hashlib
import json
from pathlib import Path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(review, frozen, source_root):
    manifest = frozen.get('manifest')
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError('empty source manifest')
    actual = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if actual != frozen.get('source_digest') or actual != review.get('source_digest'):
        raise ValueError('review source digest mismatch')
    critical = review.get('open_p0_p1')
    if not (critical is False or isinstance(critical, list) and not critical):
        raise ValueError('review has unresolved or undeclared critical findings')
    if not review.get('provider') or not review.get('verdict'):
        raise ValueError('missing review identity/verdict')
    for name, expected in manifest.items():
        relative = Path(name)
        path = source_root / relative
        if relative.is_absolute() or '..' in relative.parts or not path.resolve().is_relative_to(source_root.resolve()):
            raise ValueError('unsafe manifest path')
        if not path.is_file() or digest(path) != expected:
            raise ValueError('reviewed file changed: ' + name)
    return {'result':'PASS_REVIEW_BINDING','task_id':review.get('task_id'),
            'source_digest':actual,'files_verified':len(manifest),
            'limitation':'Digest integrity does not establish reviewer independence or substantive quality.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.review.read_text()), json.loads(args.manifest.read_text()), args.source_root)))
