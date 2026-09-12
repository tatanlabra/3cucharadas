#!/usr/bin/env python3
"""Recompute runtime criteria from recorded observations; no claim of attestation."""
import argparse
import hashlib
import itertools
import json
import math
import statistics
from pathlib import Path

PLAN = Path(__file__).resolve().parent
BLOG = PLAN.parents[2]

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def number(value, name, positive=False):
    require(type(value) in (int, float) and math.isfinite(value) and (value > 0 if positive else value >= 0), 'Invalid '+name)
    return value

def file_map(mapping, root):
    require(isinstance(mapping, dict) and bool(mapping), 'Empty hash manifest')
    for name, expected in mapping.items():
        p = root/name
        require(not Path(name).is_absolute() and '..' not in Path(name).parts and p.resolve().is_relative_to(root.resolve()), 'Unsafe manifest path')
        require(p.is_file() and sha(p) == expected, 'Stale or missing artifact: '+name)

def bind(directory, source_path, built_site):
    receipt = read(directory/'receipt.json')
    file_map(receipt['files'], directory)
    source = read(source_path)
    digest = hashlib.sha256(json.dumps(source['manifest'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    require(digest == source['source_digest'], 'Invalid source digest')
    file_map(source['manifest'], BLOG)
    inputs = receipt['inputs']
    require(inputs['source_digest'] == digest and inputs['source_manifest_sha256'] == sha(source_path), 'Runtime/source mismatch')
    build_path = (directory/inputs['build_manifest']).resolve()
    require(build_path.is_relative_to(PLAN.resolve()), 'Build manifest outside evidence package')
    require(sha(build_path) == inputs['build_manifest_sha256'], 'Stale build manifest')
    build = read(build_path)
    # Both emitted schemas bind the whole served tree; UI additionally freezes its source components.
    if 'files' in build:
        require(build.get('source_digest') == digest, 'Build/source mismatch')
        file_map(build['files'], built_site)
    elif 'built_files' in build and 'source_components' in build:
        file_map(build['source_components'], BLOG)
        file_map(build['built_files'], built_site)
    else:
        raise ValueError('Unsupported build manifest schema')
    return receipt

def cls_window(shifts):
    start = previous = None
    total = maximum = 0.0
    for row in sorted(shifts, key=lambda x:x['startTime']):
        time = number(row['startTime'], 'CLS time')
        value = number(row['value'], 'CLS shift')
        if start is None or time-previous >= 1000 or time-start >= 5000:
            start, total = time, value
        else:
            total += value
        previous = time
        maximum = max(maximum, total)
    return maximum

def performance(runs):
    expected = set(itertools.product(range(1,6), ['avaluos-ii','casen-long'], ['baseline','candidate'], ['cold','warm']))
    require(isinstance(runs,list) and len(runs)==40, 'Need all40 paired observations')
    seen = set(); groups = {}; devices = set()
    for row in runs:
        require(type(row['pair']) is int, 'Invalid pair number')
        key = row['pair'], row['page'], row['side'], row['temperature']
        require(key in expected and key not in seen, 'Duplicate or unexpected observation')
        seen.add(key)
        require(row.get('missing') is False, 'Missing measurement')
        raw = row['sample']; metrics = row['metrics']; cwv = raw['cwv']
        lcp = number(metrics['lcp_ms'], 'LCP', True)
        require(isinstance(cwv['lcp'],dict) and lcp == number(cwv['lcp']['startTime'],'raw LCP',True), 'LCP differs from raw observer')
        number(cwv['fcp'],'FCP',True)
        require(lcp <= number(raw['capturedAt'],'capture time',True), 'LCP after capture')
        cls = cls_window(raw['observation']['shifts'])
        require(math.isclose(cls, number(metrics['cls_session_window'],'CLS'), rel_tol=1e-10, abs_tol=1e-10), 'CLS differs from raw shifts')
        require(cls <= .1, 'CLS exceeds0.1')
        device = raw['device']; devices.add(tuple(device[x] for x in ['width','height','dpr','theme','userAgent']))
        require(raw['visibility']=='visible', 'Measurement in hidden page')
        groups.setdefault((row['page'],row['temperature'],row['side']),[]).append(lcp)
    require(seen == expected and len(devices)==1, 'Incomplete pairs or different browser setup')
    output=[]
    for page,temp in itertools.product(['avaluos-ii','casen-long'],['cold','warm']):
        baseline = statistics.median(groups[(page,temp,'baseline')]); candidate = statistics.median(groups[(page,temp,'candidate')])
        regression = (candidate/baseline-1)*100
        require(candidate <= 2500, f'{page}/{temp}: median LCP exceeds2500ms')
        require(regression <= 10+1e-10, f'{page}/{temp}: LCP regression exceeds10%')
        output.append({'page':page,'temperature':temp,'baseline_median_ms':baseline,'candidate_median_ms':candidate,'regression_percent':regression})
    return output

def ui(matrix, extras):
    inventory = {r['file'] for r in read(PLAN/'evidence/routes-baseline.json')}
    require(isinstance(matrix,list) and len(matrix)==80, 'Need80 UI cases')
    require(isinstance(extras,list) and len(extras)==8, 'Need8 narrow/reflow cases')
    combinations=set()
    for row in matrix:
        o=row['observed']; key=(row['post_file'],o['width'],o['theme'])
        require(key not in combinations and key[0] in inventory and key[1] in [390,1440] and key[2] in ['light','academic-night'], 'Duplicate or unexpected UI case')
        combinations.add(key)
        require(row.get('failures')==[], 'UI case failed')
        require(all(type(o[x]) is int for x in ['h1_count','hero_count','disclosure_count','badge_count']), 'Invalid UI counts')
        require(o['h1_count']==1 and o['hero_count']==1 and o['disclosure_count']==1 and o['disclosure_tag']=='P' and o['badge_count']==0, 'Incorrect hero/disclosure structure')
        require(o['page_overflow']<=1, 'Page overflow')
        for name in ['axe','policy_axe']:
            require(row[name]['counts']['violations']==0 and row[name]['counts']['incomplete']==0, 'Unresolved UI accessibility result')
    require(len(combinations)==len(inventory)*4, 'UI coverage incomplete')
    extra_combinations=set()
    for row in extras:
        o=row['observed']; key=(o['lang'],o['width'],o['theme'])
        require(key not in extra_combinations and key[0] in ['es','en'] and key[1] in [320,720] and key[2] in ['light','academic-night'], 'Duplicate or unexpected narrow/reflow case')
        extra_combinations.add(key)
        require(row.get('failures')==[] and row['axe']['counts']['violations']==0 and row['axe']['counts']['incomplete']==0,'Narrow/reflow check unresolved')
    return {'posts':len(inventory),'matrix':len(matrix),'extras':len(extras)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=['performance','ui'])
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--source-manifest',type=Path,default=PLAN/'evidence/editorial/source-first-person-before-build.json')
    parser.add_argument('--built-site',type=Path,default=BLOG/'_site')
    args=parser.parse_args()
    bind(args.directory,args.source_manifest,args.built_site)
    result=performance(read(args.directory/'runs.json')) if args.kind=='performance' else ui(read(args.directory/'matrix.json'),read(args.directory/'extras.json'))
    print(json.dumps({'result':'PASS_RECOMPUTED_RUNTIME_CRITERIA','kind':args.kind,'observed':result,'limitation':'Checks consistency of recorded observations and current files; not cryptographic attestation or global accessibility/performance certification.'}))
