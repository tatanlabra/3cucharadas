#!/usr/bin/env python3
"""Fail-closed, source-bound local gate for the III/IV scientific reset.

Hashes and structural checks establish custody and coverage, not causal validity or
semantic equivalence. The latter requires a separate review bound to exact bytes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / 'assets/data/tesis-scientific-reset/publication-contract.json'
POST4_PROJECTION_CODE_SHA = '62d564549acfbecf39afc28e0e4eb7ec06395b85ef685d396c9ba84e97420031'
POST4_PUBLIC_BYTES_SHA = 'c06aaae2dd8ddf7165e826f10e2f5d39140b1bf19da46cd9dc9fc985f33e99c0'
POST3_PRIMARY_PUBLIC_BYTES_SHA = 'bea720c01e1cb04b8759ff5651d1b164a411576b8a4f1533c2fb0e564f0871b9'
POST3_SENSITIVITY_PUBLIC_BYTES_SHA = 'edcc575f08d4caf3a08b74bf7ffb5fdb807ce1d813ce2bed6cb58631ab638aea'
IV_TABLE_NAMES=tuple(f'post4-sensitivity-{kind}-{lang}.html'
                     for kind in ('comparison-table','calendar-table','calendar-window-matrix')
                     for lang in ('es','en'))
IDENTITY = {
    'III': {'date': '2026-10-23 10:00:00 -0300', 'ref': 'costos-cierre-escolar-trayectorias', 'annex': 'tesis-post3-anexo-metodologico', 'number': '3', 'slug': 'costos-cierre-escolar-trayectorias'},
    'IV': {'date': '2026-11-04 10:00:00 -0300', 'ref': 'cierre-escolar-educacion-superior-causal-ml', 'annex': 'tesis-post4-anexo-metodologico', 'number': '4', 'slug': 'cierre-escolar-educacion-superior-causal-ml'},
}
SHA = re.compile(r'^[a-f0-9]{64}$')
PRIVATE = re.compile(r'/(?:home|mnt|opt|run|tmp)/|file://|\b\d{7,8}-[0-9kK]\b|\b(?:mrun|rut|run|person_id|student_id)\s*[:=]\s*\S+', re.I)
SMALL_COUNT = re.compile(r'^(?:n|n_treated|n_control|baseline_n|observed_n|valid_baseline_n|valid_followup_n|complete_case_n|grade_unknown_n|treated_students_lost_to_support|control_students_removed|common_students|d1_only_students|d2_only_students|arm_switches|post_baseline_students_excluded|repeated_students|.*_student_count|.*_students)$')
FORBIDDEN = {
 'es': [r'\b(?:los cierres(?: escolares)?|cerrar escuelas|el cierre escolar)\s+(?:causan?|provocan?|reducen?|aumentan?|perjudican?|dañan?)\b', r'\b(?:efecto|impacto) causal (?:confirmado|demostrado|identificado)\b', r'\b(?:demostramos|identificamos) (?:un|el) efecto causal\b'],
 'en': [r'\b(?:school closures|closing schools|school closure)\s+(?:causes?|reduces?|increases?|harms?|damages?)\b', r'\b(?:confirmed|demonstrated|identified) causal (?:effect|impact)\b', r'\b(?:we demonstrate|we identify) (?:a|the) causal effect\b'],
}

class GateError(Exception):
    pass

def need(ok, message):
    if not ok: raise GateError(message)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def obj(path):
    value = json.loads(path.read_text(encoding='utf-8'))
    need(isinstance(value, dict), f'JSON object required: {path}')
    return value

def bound(binding, base, *, public=None):
    need(isinstance(binding, dict), 'file binding missing')
    name, expected = binding.get('path'), binding.get('sha256')
    need(isinstance(name, str) and name and isinstance(expected, str) and SHA.fullmatch(expected), 'file binding invalid')
    path = (base / name).resolve()
    if public:
        need(not Path(name).is_absolute() and path.is_relative_to(public), f'public path escapes site: {name}')
    need(path.is_file() and sha(path) == expected, f'missing/stale SHA-256: {name}')
    return path

def public_text(path):
    if path.suffix.lower() in {'.md','.csv','.svg','.json','.html','.txt'}:
        need(not PRIVATE.search(path.read_text(encoding='utf-8')), f'private path or identifier: {path}')
    if path.suffix.lower()=='.json':
        def visit(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    if SMALL_COUNT.fullmatch(key) and isinstance(item,int) and not isinstance(item,bool):
                        need(item==0 or item>=10,f'public small count exposed: {path}:{key}')
                    visit(item)
            elif isinstance(value,list):
                for item in value:visit(item)
        visit(obj(path))
    if path.suffix.lower()=='.csv':
        with path.open(encoding='utf-8',newline='') as stream:
            reader=csv.DictReader(stream)
            for row in reader:
                for key,value in row.items():
                    if SMALL_COUNT.fullmatch(key) and value and re.fullmatch(r'\d+',value):
                        need(int(value)==0 or int(value)>=10,f'public small count exposed: {path}:{key}')

def public_member(root,folder,name):
    need(isinstance(name,str) and re.fullmatch(r'[a-z0-9_-]+\.(?:csv|svg|png|json|html)',name),'invalid public file name')
    path=folder/name
    need(not path.is_symlink() and path.resolve().is_relative_to(root),'public file escapes site')
    return path

def add_public_binding(root,bindings,path):
    path=path.resolve()
    need(path.is_relative_to(root),'public binding escapes site')
    bindings[str(path.relative_to(root))]=sha(path)

def check_render_inputs(root,bindings):
    names=('_includes/thesis-reset-figure.html','_data/tesis_reset_figures.json',
           'assets/css/main.scss','scripts/post4_public_projection.py',
           'scripts/verify_thesis_scientific_reset.py')
    names+=tuple(f'_includes/tesis-reset-tables/{name}' for name in IV_TABLE_NAMES)
    for name in names:
        path=root/name
        need(path.is_file() and not path.is_symlink(),f'render input missing or symlink: {name}')
        if name=='scripts/post4_public_projection.py':
            need(sha(path)==POST4_PROJECTION_CODE_SHA,'Post IV public projection code drift')
        else:public_text(path)
        add_public_binding(root,bindings,path)

def post4_projection_library():
    path=ROOT/'scripts/post4_public_projection.py'
    need(path.is_file() and sha(path)==POST4_PROJECTION_CODE_SHA,'Post IV public projection code missing/drift')
    spec=importlib.util.spec_from_file_location('post4_public_projection',path)
    need(spec is not None and spec.loader is not None,'Post IV public projection import failed')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def check_iv_projection(root,spec,primary_public,record,bindings,private_spec=None,private_base=None):
    companion=bound(spec.get('public_privacy_projection'),root,public=root)
    need(sha(companion)==POST4_PUBLIC_BYTES_SHA,'IV public combined projection bytes drift')
    public_text(companion);add_public_binding(root,bindings,companion)
    combined=obj(companion);library=post4_projection_library()
    try:
        library.validate_public_projection(combined)
        split=library.split_public_projection(combined)
        library.validate_split_public_projection(split)
    except (ValueError,TypeError,KeyError) as exc:
        raise GateError(f'IV public combined projection invalid: {exc}') from exc
    need(combined['source_sha256']=={'primary_aggregate':record['primary_sha256'],
                                    'sensitivity_aggregate':record['sensitivity_sha256']},
         'IV combined/private source receipt drift')
    need(primary_public==split['primary'],'IV public primary differs from combined split')
    if private_spec is not None:
        need(private_base is not None,'IV private evidence base missing')
        primary=bound(private_spec['primary'],private_base)
        sensitivity=bound(private_spec['sensitivity'],private_base)
        try:reprojected=library.project_files(primary,sensitivity)
        except (ValueError,TypeError,KeyError) as exc:
            raise GateError(f'IV private/public reprojection failed: {exc}') from exc
        need(reprojected==combined,'IV public combined projection differs from pinned private reprojection')
    return companion,combined,split

def document(root, fixed, kind, lang):
    if kind == 'post':
        name = f"_posts/{fixed['date'][:10]}-{fixed['slug']}{'-en' if lang == 'en' else ''}.md"
    else: name = f"_pages/{fixed['annex']}{'-en' if lang == 'en' else ''}.md"
    path = (root/name).resolve()
    need(path.is_file(), f'document missing: {name}')
    text = path.read_text(encoding='utf-8'); public_text(path)
    need(text.startswith('---\n') and '\n---\n' in text[4:], f'front matter missing: {name}')
    head, body = text[4:].split('\n---\n',1)
    fields = dict((m.group(1), m.group(2).strip().strip('"\'')) for line in head.splitlines() if (m:=re.match(r'^([\w-]+):\s*(.*)$',line)))
    route = f"/datos/educacion/politica-publica/{fixed['slug']}/" + ('anexo-metodologico/' if kind == 'annex' else '')
    need(fields.get('lang') == lang and fields.get('ref') == (fixed['ref'] if kind=='post' else fixed['annex']) and fields.get('permalink') == route, f'identity drift: {name}')
    if kind == 'post':
        need(fields.get('date') == fixed['date'], f'date drift: {name}')
        headings = re.findall(r'^##\s+(Cucharada|Spoonful)\s+([1-3])\s*:',body,re.M|re.I)
        word = 'cucharada' if lang=='es' else 'spoonful'
        need(headings == [(word.title(), str(i)) for i in (1,2,3)], f'three ordered spoonfuls required: {name}')
        need(all(re.search(r'\w', body[body.find(f'## {word.title()} {i}:')+5:body.find(f'## {word.title()} {i+1}:') if i<3 else None] or '') for i in (1,2,3)), f'empty spoonful: {name}')
    need(not re.search(r'\bELI5\b|\bEn simple\s*:',head+'\n'+body,re.I), f'ELI5 label exposed: {name}')
    for pattern in FORBIDDEN[lang]:
        need(not re.search(pattern,head+'\n'+body,re.I), f'lexical causal promotion: {name}')
    need(body.count('<details')==body.count('</details>'),f'details tags unbalanced: {name}')
    definitions=re.findall(r'^\[\^([A-Za-z0-9_-]+)\]:',body,re.M)
    need(len(definitions)==len(set(definitions)),f'duplicate footnote definition: {name}')
    citations=set(re.findall(r'\[\^([A-Za-z0-9_-]+)\]',re.sub(r'^\[\^[A-Za-z0-9_-]+\]:.*$', '', body,flags=re.M)))
    need(citations==set(definitions),f'footnote citation/definition mismatch: {name}')
    for math in re.findall(r'\$\$(.*?)\$\$',body,re.S):
        need(not re.search(r'(?<!\\)%|\d,\d',math),f'KaTeX percent/comma number invalid: {name}')
    return path, body

def key3(row): return (row['outcome'],row['era'],row.get('cohort_year'))
def key4(row): return (row['outcome'],row.get('taxonomy',row.get('era')),row.get('cohort'))
def key4full(row): return (row['variant'],row['outcome'],row.get('taxonomy',row.get('era')),row['cohort'],row.get('axis'),str(row.get('value')))

def check_projection(public,private,series,source_sha):
    need(series=='III','legacy projection validator only supports III')
    check_iii_projection_shape(public,source_sha)
    projection=public.get('projection')
    excluded=projection.get('excluded_fields')
    raw={key3(r):r for r in private['results']};shown={key3(r):r for r in public['results']}
    need(len(raw)==len(private['results']) and len(shown)==len(public['results']) and set(raw)==set(shown),f'{series} public/private primary coverage drift')
    for key,row in shown.items():
        origin=raw[key];expected_fields=set(origin)-set(excluded)
        need(set(row)==expected_fields,f'{series} projection fields drift: {key}')
        for field,value in row.items():
            need(value==origin[field],f'{series} public aggregate source value drift: {key}:{field}')
    raw_coverage={key3(r):r for r in private['coverage']}
    shown_coverage={key3(r):r for r in public['coverage']}
    need(len(raw_coverage)==len(private['coverage']) and set(raw_coverage)==set(shown_coverage),
         'III public/private coverage drift')
    for key,row in shown_coverage.items():
        origin=raw_coverage[key]
        need(set(row)==set(origin)-{'treated_students_before_support'},f'III coverage projection fields drift: {key}')
        need(all(value==origin[field] for field,value in row.items()),f'III coverage source value drift: {key}')

def check_iii_projection_shape(public,source_sha):
    projection=public.get('projection')
    need(isinstance(projection,dict) and projection.get('source_sha256')==source_sha,
         'III public projection source binding missing')
    need(projection.get('excluded_fields')==['treated_students_lost_to_support'] and
         projection.get('coverage_excluded_fields')==['treated_students_before_support'] and
         projection.get('redactions')==[], 'III projection exclusions/redactions invalid')
    results,coverage=public.get('results'),public.get('coverage')
    need(isinstance(results,list) and len(results)==43 and isinstance(coverage,list) and len(coverage)==39,
         'III public projection 43/39 inventory incomplete')
    unique(results,key3,'III public primary');unique(coverage,key3,'III public coverage')
    cohort_keys={key3(row) for row in results if row.get('cohort_year') is not None}
    pooled_keys={key3(row) for row in results if row.get('cohort_year') is None}
    need(len(cohort_keys)==39 and len(pooled_keys)==4 and cohort_keys=={key3(row) for row in coverage},
         'III public result/coverage cohort keys drift')
    need(all('treated_students_lost_to_support' not in row for row in results) and
         all('treated_students_before_support' not in row for row in coverage),
         'III excluded count reintroduced in public JSON')
    need(all('treated_students_after_support' in row for row in coverage),
         'III after-support coverage missing')

def nested_subset(projected,source):
    if isinstance(projected,dict):
        return isinstance(source,dict) and all(k in source and nested_subset(v,source[k])
                                               for k,v in projected.items())
    if isinstance(projected,list):
        return isinstance(source,list) and len(projected)==len(source) and all(
            nested_subset(a,b) for a,b in zip(projected,source))
    return projected==source

def check_iii_sensitivity_public(public,record,private=None):
    projection=public.get('projection')
    need(isinstance(projection,dict) and projection.get('source_sha256')==record['sensitivity_sha256'] and
         projection.get('primary_source_sha256')==record['primary_sha256'] and
         projection.get('policy')=='post3-f3-candidate-allowlist-r1',
         'III sensitivity projection source/policy drift')
    need(public.get('metadata',{}).get('primary_results_sha256')==record['primary_sha256'],
         'III sensitivity primary source binding drift')
    rows=public.get('sensitivities')
    need(isinstance(rows,list) and len(rows)==49,'III sensitivity projected inventory incomplete')
    key=lambda r:(r['name'],r.get('outcome'),r.get('era'),r.get('metric'))
    unique(rows,key,'III public sensitivities')
    suppressed={'PUBLIC_SUPPRESSED_SMALL_COMPOSITION_CHANGE',
                'ESTIMABLE_BUT_PUBLICLY_SUPPRESSED_SMALL_ZERO_GROUP'}
    forbidden={'estimate_pp','estimate','ci_low','ci_high','lower_pp','upper_pp','se',
               'results','result','overlap','by_arm','cohorts','coverage','observation'}
    for row in rows:
        need(isinstance(row.get('status'),str) and row['status'],'III sensitivity status missing')
        if row['status'] in suppressed:
            need(not forbidden.intersection(row),'III suppressed sensitivity value reintroduced')
    need(all('treated_students_before_support' not in json.dumps(row) and
             'treated_students_lost_to_support' not in json.dumps(row) for row in rows),
         'III excluded count reintroduced in sensitivity JSON')
    if private is not None:
        raw=private.get('sensitivities')
        need(isinstance(raw,list) and len(raw)==49,'III private sensitivity inventory incomplete')
        source={key(r):r for r in raw}
        need(len(source)==49 and set(source)=={key(r) for r in rows},
             'III public/private sensitivity key drift')
        need(public.get('status')==private.get('status') and
             nested_subset(public.get('metadata'),private.get('metadata')),
             'III sensitivity source metadata/status drift')
        for row in rows:
            need(nested_subset(row,source[key(row)]),f'III sensitivity source value drift: {key(row)}')

def csv_against_iii_sensitivity_inventory(path,rows):
    public_text(path)
    fields={'name','outcome','era','metric','status'}
    with path.open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream);shown=list(reader)
        need(set(reader.fieldnames or [])==fields and len(shown)==49,
             'III sensitivity inventory CSV fields/rows drift')
    expected={tuple('' if row.get(k) is None else str(row[k]) for k in sorted(fields))
              for row in rows}
    actual={tuple(row[k] for k in sorted(fields)) for row in shown}
    need(len(expected)==49 and len(actual)==49 and actual==expected,
         'III sensitivity inventory CSV source drift')

def unique(rows, key, label):
    need(isinstance(rows,list) and rows, f'empty {label}')
    keys=[key(r) for r in rows]
    need(len(keys)==len(set(keys)), f'duplicate {label}')
    return set(keys)

def check_f2_iii(spec, base, bindings):
    protocol=bound(spec['protocol'],base); primary=bound(spec['primary'],base)
    receipt=bound(spec['primary_receipt'],base); sensitivity=bound(spec['sensitivity'],base)
    for p in (protocol,primary,receipt,sensitivity): bindings[str(p)]=sha(p)
    p,s=obj(primary),obj(sensitivity)
    need(p.get('metadata',{}).get('protocol_sha256')==sha(protocol)==s.get('metadata',{}).get('protocol_sha256'), 'III protocol binding drift')
    need(s.get('metadata',{}).get('primary_results_sha256')==sha(primary), 'III sensitivity primary binding drift')
    need(len(p.get('results',[]))==43 and len(p.get('coverage',[]))==39, 'III primary/coverage inventory incomplete')
    unique(p['results'],key3,'III primary'); unique(p['coverage'],key3,'III coverage')
    need(len(s.get('sensitivities',[]))==49, 'III sensitivity inventory incomplete')
    unique(s['sensitivities'],lambda r:(r['name'],r.get('outcome'),r.get('era'),r.get('metric')),'III sensitivities')
    research=Path(__file__).resolve().parents[3]/'incubadora/tesis_mae_mejorada'
    validator=research/'research/post3/scientific_reset_v2/validate_primary_results.py'
    sens_validator=research/'research/post3/scientific_reset_v2/validate_sensitivity_results.py'
    for script,args in ((validator,['--result',str(primary),'--run-receipt',str(receipt)]),(sens_validator,['--result',str(sensitivity)])):
        need(script.is_file(),f'research validator missing: {script}')
        proc=subprocess.run([sys.executable,str(script),*args],cwd=research,env={**os.environ,'PYTHONPATH':str(research/'src'),'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        need(proc.returncode==0, f'research validator failed: {script.name}: {proc.stderr.strip()[:300]}')
    return p

def check_f2_iv(spec,base,bindings):
    paths={k:bound(spec[k],base) for k in ('protocol','primary','sensitivity','inventory','reconciliation')}
    for p in paths.values(): bindings[str(p)]=sha(p)
    p,s,i,r=[obj(paths[k]) for k in ('primary','sensitivity','inventory','reconciliation')]
    need(i.get('status')=='PREOUTCOME_EXPECTED_KEYS_NO_EFFECT_SELECTION', 'IV preoutcome inventory absent')
    need(i.get('source_sha256',{}).get('protocol')==sha(paths['protocol']), 'IV inventory/protocol binding drift')
    expected=unique(i.get('result_keys'),key4full,'IV expected results')
    coverage=unique(i.get('coverage_keys'),lambda x:json.dumps(x,sort_keys=True),'IV coverage')
    contrast=unique(i.get('heterogeneity_contrast_keys'),lambda x:json.dumps(x,sort_keys=True),'IV contrasts')
    need(len(expected)==2344 and len(coverage)==4992 and len(contrast)==800, 'IV frozen inventory counts drift')
    need(len([x for x in expected if x[0]=='primary'])==144, 'IV primary inventory count drift')
    need(len(p.get('results',[]))==138 and len(s.get('result_key_status',[]))==2200, 'IV primary/sensitivity coverage incomplete')
    need(p.get('metadata',{}).get('protocol_sha256')==sha(paths['protocol'])==s.get('metadata',{}).get('protocol_sha256'), 'IV source protocol drift')
    actual=unique(r.get('result_key_status'),key4full,'IV reconciliation')
    need(actual==expected and r.get('expected_result_keys')==2344 and r.get('expected_contrast_keys')==800 and r.get('status')=='F2_COMPLETE_RESULT_KEY_RECONCILIATION_NO_PUBLIC_EXPORT', 'IV reconciliation coverage mismatch')
    h=r.get('source_sha256',{})
    need(all(h.get(k)==sha(paths[v]) for k,v in [('primary_aggregate','primary'),('sensitivity_aggregate','sensitivity'),('expected_output_inventory','inventory'),('protocol','protocol')]), 'IV reconciliation source binding drift')
    primary_keys={('primary',*key4(row),None,'None') for row in p['results']}
    need(primary_keys <= expected, 'IV unplanned primary result')
    sensitivity_keys=unique(s['result_key_status'],key4full,'IV sensitivity result keys')
    need(sensitivity_keys=={x for x in expected if x[0]!='primary'},'IV sensitivity key coverage mismatch')
    report_rows={key4full(row):row for row in r['result_key_status']}
    for row in p['results']:
        report=report_rows[('primary',*key4(row),None,'None')]
        need(report['estimation_status']==row['estimation_status'] and report['result_present'] is True,'IV primary status reconciliation drift')
    for row in s['result_key_status']:
        report=report_rows[key4full(row)]
        need(report['estimation_status']==row['estimation_status'] and report['result_present']==row['result_present'],'IV sensitivity status reconciliation drift')
    need(s.get('coverage_inventory_match',{}).get('matched_keys')==4992 and s.get('matched_heterogeneity_contrast_keys')==800,'IV coverage/contrast receipt incomplete')
    research=Path(__file__).resolve().parents[3]/'incubadora/tesis_mae_mejorada'
    reconciler=research/'research/post4/scientific_reset_v2/reconcile_post4_outputs.py'
    need(reconciler.is_file(),'IV research reconciler missing')
    with tempfile.TemporaryDirectory(prefix='codex-post4-reconcile-',dir='/tmp') as temp:
        output=Path(temp)/'reconciliation.json'
        proc=subprocess.run([sys.executable,str(reconciler),'--primary',str(paths['primary']),'--sensitivities',str(paths['sensitivity']),'--output',str(output)],cwd=reconciler.parent,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        need(proc.returncode==0,f'IV research reconciler failed: {proc.stderr.strip()[:300]}')
        need(obj(output)==r,'IV reconciliation differs from research authority')
    return p

def csv_against_source(path,source,series):
    public_text(path)
    with path.open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream); rows=list(reader); fields=reader.fieldnames or []
    required=({'outcome','era','cohort_year','estimand','estimation_status','identification_status','estimate_pp','ci_low_pp','ci_high_pp','n_treated','n_control','limitation'}
              if series=='III' else {'variant','outcome','era','cohort','estimation_status'})
    need(required<=set(fields) and len(rows)>0, f'public CSV fields/rows missing: {path}')
    lookup={key3(r) if series=='III' else key4(r):r for r in source['results']}
    need(len(lookup)==len(source['results']), f'duplicate source row: {series}')
    need(set(fields)==set().union(*(set(r) for r in source['results'])),f'CSV missing/extra source columns: {path}')
    seen=set()
    for row in rows:
        cohort=row['cohort_year' if series=='III' else 'cohort']
        cohort=int(cohort) if cohort else None
        key=(row['outcome'],row['era'],cohort)
        need(key in lookup and key not in seen, f'CSV unplanned/duplicate row: {path}:{key}')
        seen.add(key); src=lookup[key]
        for field in fields:
            val=src.get(field)
            if isinstance(val,(list,dict)):
                try: equal=json.loads(row[field])==val
                except (json.JSONDecodeError,TypeError): equal=False
            else:
                expected='' if val is None else str(val)
                equal=row[field]==expected
            need(equal,f'CSV source drift: {path}:{key}:{field}')
    return seen

def csv_against_iii_coverage(path,coverage):
    public_text(path)
    with path.open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream);rows=list(reader);fields=reader.fieldnames or []
    need('treated_students_before_support' not in fields and
         'treated_students_after_support' in fields,
         'III coverage CSV excluded count reintroduced or after-support missing')
    need(len(rows)==39 and set(fields)==set().union(*(set(r) for r in coverage)),
         'III coverage CSV fields/rows drift')
    source={key3(r):r for r in coverage};need(len(source)==39,'III coverage source keys drift')
    seen=set()
    for row in rows:
        year=row['cohort_year'];key=(row['outcome'],row['era'],int(year) if year else None)
        need(key in source and key not in seen,f'III coverage CSV key drift: {key}')
        seen.add(key)
        for field in fields:
            value=source[key][field]
            expected='' if value is None else str(value)
            need(row[field]==expected,f'III coverage CSV source drift: {key}:{field}')
    need(seen==set(source),'III coverage CSV inventory incomplete')
    return seen

def check_manifest(root,series,spec,aggregate,expected_source_sha,bindings,docs):
    manifest_path=bound(spec['manifest'],root,public=root); manifest=obj(manifest_path);add_public_binding(root,bindings,manifest_path)
    public_text(manifest_path)
    need(manifest.get('f2_complete') is True and manifest.get('publication_authorized') is True, f'{series} manifest F2/publication flag false')
    need(manifest.get('source_sha256')==expected_source_sha,f'{series} manifest source drift')
    figures=manifest.get('figures'); files=manifest.get('files')
    need(isinstance(figures,list) and figures and isinstance(files,list) and files,f'{series} manifest empty')
    names=[x.get('name') for x in files]
    need(len(names)==len(set(names)) and all(isinstance(n,str) and re.fullmatch(r'[a-z0-9_-]+\.(?:csv|svg|png|json|html)',n) for n in names),f'{series} manifest file names invalid')
    folder=manifest_path.parent
    if series=='IV':
        need(manifest.get('family')=='post4_primary_projected' and
             manifest.get('projection_code_sha256')==POST4_PROJECTION_CODE_SHA,
             'IV primary manifest projection code binding drift')
        source_file=manifest.get('source_file')
        need(source_file=='public-combined-projection.json' and source_file in names,
             'IV manifest combined projection companion missing')
        need(sha(public_member(root,folder,source_file))==expected_source_sha,
             'IV manifest combined projection companion drift')
    for item in files:
        file=public_member(root,folder,item['name'])
        need(file.is_file() and item.get('sha256')==sha(file),f'{series} manifest file hash drift: {item["name"]}')
        public_text(file);add_public_binding(root,bindings,file)
    if series=='III':
        need('sensitivities-all.csv' not in names and
             not (folder/'sensitivities-all.csv').exists(),
             'III unprojected primary sensitivities CSV remains public')
    need('results-all.csv' in names and 'coverage-all.csv' in names,f'{series} results/coverage CSV missing')
    public_aggregate=obj(aggregate)
    keys=csv_against_source(folder/'results-all.csv',public_aggregate,series)
    need(keys==set(key3(r) if series=='III' else key4(r) for r in public_aggregate['results']),f'{series} public primary table incomplete')
    if series=='III':csv_against_iii_coverage(folder/'coverage-all.csv',public_aggregate['coverage'])
    source_rows={key3(r) if series=='III' else key4(r):r for r in public_aggregate['results']}
    stems=set()
    for fig in figures:
        stem=(f"post3-anticipation-{fig['outcome']}-{fig['era']}" if fig.get('family')=='anticipation' else f"post3-{fig['outcome']}-{fig['era']}") if series=='III' else f"post4-{fig['kind']}-{fig['era']}"
        need(stem not in stems,f'{series} duplicate figure: {stem}');stems.add(stem)
        need(isinstance(fig.get('source_rows'),list) and fig['source_rows'],f'{series} figure without data: {stem}')
        for row in fig['source_rows']:
            cohort=row.get('cohort_year' if series=='III' else 'cohort')
            key=(row.get('outcome',fig.get('outcome')),row.get('era',fig.get('era')),cohort)
            need(key in source_rows,f'{series} figure unplanned source row: {stem}:{key}')
            original=source_rows[key]
            if series=='IV':need(set(row)<=set(original),f'IV figure unreviewed source field: {stem}:{key}')
            for field,value in row.items():
                if field in original:
                    need(value==original[field],f'{series} figure source drift: {stem}:{key}:{field}')
            if series=='IV':
                aliases={'n_treated_post_generation':'n_treated','n_control_post_generation':'n_control','treated_schools_both_generations':'treated_schools','control_schools_both_generations':'control_schools'}
                for alias,field in aliases.items():
                    if alias in row:need(row[alias]==original[field],f'{series} figure denominator drift: {stem}:{key}:{alias}')
        if fig.get('family')=='anticipation':
            need(series=='III' and 'anticipation-all.csv' in names, 'anticipation master CSV missing')
        for name in [f'{stem}.csv',*[f'{stem}-{lang}-{theme}-{size}.{ext}' for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]]:
            need(name in names,f'{series} figure variant/CSV missing: {name}')
        if series=='III':
            figure_keys={(fig['outcome'],fig['era'],row['cohort_year']) for row in fig['source_rows']}
            figure_source={'results':[source_rows[key] for key in figure_keys]}
            need(csv_against_source(folder/f'{stem}.csv',figure_source,'III')==figure_keys,
                 f'III figure CSV inventory drift: {stem}')
        for lang in ('es','en'):
            need(isinstance((fig.get('alt') or {}).get(lang),str) and (fig.get('alt') or {})[lang].strip(),f'{series} alt missing: {stem}:{lang}')
            need(isinstance((fig.get('source_citation') or {}).get(lang),str) and (fig.get('source_citation') or {})[lang].strip(),f'{series} source citation missing: {stem}:{lang}')
            caption=fig.get('caption',{}).get(lang) if isinstance(fig.get('caption'),dict) else fig.get(f'caption_{lang}')
            need(isinstance(caption,str) and caption.strip(),f'{series} caption missing: {stem}:{lang}')
            need(stem in docs[('post',lang)] or stem in docs[('annex',lang)],f'{series} figure link missing: {stem}:{lang}')
    return len(figures)

def check_anticipation(root,spec,bindings,docs,source_dir=None):
    if source_dir is not None:
        source_dir=Path(source_dir).resolve()
        need(source_dir.is_dir(),'III anticipation source directory missing')
    manifest_path=bound(spec['anticipation_manifest'],root,public=root)
    manifest=obj(manifest_path);add_public_binding(root,bindings,manifest_path)
    need(manifest.get('family')=='anticipation' and manifest.get('source_status')=='PRE_EVENT_ANTICIPATION_QA_NO_EFFECTS','III anticipation manifest state invalid')
    need(manifest.get('f2_complete') is True and manifest.get('publication_authorized') is True,'III anticipation F2/publication flag false')
    source_files=manifest.get('source_files')
    need(isinstance(source_files,list) and len(source_files)==39,'III anticipation source inventory incomplete')
    names=[x.get('name') for x in source_files]
    need(len(set(names))==39 and all(re.fullmatch(r'20\d\d_[a-z0-9_]+\.json',n or '') for n in names),'III anticipation source names invalid')
    for item in source_files:
        need(isinstance(item.get('sha256'),str) and SHA.fullmatch(item['sha256']),'III anticipation source hash invalid')
        if source_dir is not None:
            path=source_dir/item['name']
            need(path.is_file() and item['sha256']==sha(path),f'III anticipation source hash drift: {item["name"]}')
    source_digest=hashlib.sha256(json.dumps(sorted(source_files,key=lambda x:x['name']),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    need(manifest.get('source_sha256')==source_digest,'III anticipation inventory hash drift')
    if source_dir is not None:
        research=Path(__file__).resolve().parents[3]/'incubadora/tesis_mae_mejorada'
        code="import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from research.post3.scientific_reset_v2.validate_anticipation import validate; validate(Path(sys.argv[2]))"
        proc=subprocess.run([sys.executable,'-c',code,str(research),str(source_dir)],cwd=research,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        need(proc.returncode==0,f'III research anticipation QA failed: {proc.stderr.strip()[:300]}')
    folder=manifest_path.parent; files=manifest.get('files')
    need(isinstance(files,list) and files,'III anticipation derivative inventory empty')
    names=[x.get('name') for x in files]
    need(len(names)==len(set(names)) and 'anticipation-all.csv' in names,'III anticipation derivative names invalid')
    for item in files:
        path=public_member(root,folder,item['name'])
        need(path.is_file() and item.get('sha256')==sha(path),f'III anticipation derivative hash drift: {item["name"]}')
        public_text(path);add_public_binding(root,bindings,path)
    with (folder/'anticipation-all.csv').open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream); rows=list(reader); fields=reader.fieldnames
    expected_fields={'outcome','era','cohort_year','baseline_year','transition_year','arm','n','schools','rate_pp','display_status','reason_es','reason_en'}
    need(set(fields or [])==expected_fields and len(rows)==78,'III anticipation CSV schema/coverage incomplete')
    actual={}
    for row in rows:
        key=(row['cohort_year'],row['outcome'],row['arm'])
        need(key not in actual,'III anticipation duplicate arm/cohort')
        actual[key]=row
    expected={(name.split('_',1)[0],name.split('_',1)[1].removesuffix('.json'),arm) for name in (x['name'] for x in source_files) for arm in ('treated','control')}
    need(set(actual)==expected,'III anticipation cohort/arm coverage mismatch')
    for (year,outcome,arm),row in actual.items():
        need(row['era']==('historical' if int(year)<=2015 else 'modern'),'III anticipation era drift')
        if source_dir is None:
            need(row['display_status'] in {'OBSERVED','NOT_ESTIMABLE_PANEL_BOUNDARY','PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY','PRIVACY_SUPPRESSED_SMALL_SCHOOL_GROUP'},'III anticipation status invalid')
            if int(year)==2005:
                need(row['display_status']=='NOT_ESTIMABLE_PANEL_BOUNDARY','III boundary rendered as observation')
            else:
                need(row['display_status']!='NOT_ESTIMABLE_PANEL_BOUNDARY' and row['baseline_year']==str(int(year)-2) and row['transition_year']==str(int(year)-1),'III anticipation time anchor drift')
            if row['display_status']=='OBSERVED':
                need(row['n'].isdigit() and int(row['n'])>=10 and row['schools'].isdigit() and int(row['schools'])>=10 and re.fullmatch(r'\d+(?:\.\d+)?',row['rate_pp']) and 0<=float(row['rate_pp'])<=100,'III anticipation observed value invalid')
            if row['display_status']!='OBSERVED':
                need(all(not row[k] for k in ('n','schools','rate_pp')),'III anticipation hidden value exposed')
            continue
        sensor=obj(source_dir/f'{year}_{outcome}.json')['sensor']
        if sensor['status']=='NOT_ESTIMABLE_PANEL_BOUNDARY':
            need(row['display_status']=='NOT_ESTIMABLE_PANEL_BOUNDARY' and all(not row[k] for k in ('n','schools','rate_pp','baseline_year','transition_year')),'III boundary rendered as observation')
            continue
        source_arm=sensor['arms'][arm]
        need(row['baseline_year']==str(sensor['baseline_year']) and row['transition_year']==str(sensor['transition_year']),'III anticipation time anchor drift')
        if row['display_status']=='OBSERVED':
            expected_rate='' if source_arm['transition_rate'] is None else format(100*source_arm['transition_rate'],'.1f')
            need(row['n']==str(source_arm['n']) and row['schools']==str(source_arm['schools']) and row['rate_pp']==expected_rate,'III anticipation rate/denominator drift')
        else:
            need(row['display_status'].startswith('PRIVACY_SUPPRESSED') and all(not row[k] for k in ('n','schools','rate_pp')),'III anticipation suppression leaked value')
        need(row['reason_es'].strip() and row['reason_en'].strip(),'III anticipation reason missing')
    figures=manifest.get('figures')
    need(isinstance(figures,list) and figures,'III anticipation figures missing')
    for fig in figures:
        stem=fig.get('stem')
        need(isinstance(stem,str) and re.fullmatch(r'post3-anticipation-[a-z0-9_]+-(?:historical|modern)',stem),'III anticipation figure stem invalid')
        need(isinstance(fig.get('source_rows'),list) and fig['source_rows'],'III anticipation figure rows missing')
        for name in [f'{stem}.csv',*[f'{stem}-{lang}-{theme}-{size}.{ext}' for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]]:
            need(name in names,f'III anticipation variant missing: {name}')
        for lang in ('es','en'):
            need(all(isinstance((fig.get(field) or {}).get(lang),str) and fig[field][lang].strip() for field in ('alt','caption','source_citation')),'III anticipation alt/caption/source missing')
            need(stem in docs[('post',lang)] or stem in docs[('annex',lang)],f'III anticipation link missing: {stem}:{lang}')
    return len(figures)

def check_iv_sensitivity_rows(figures,folder,combined):
    expected_variants={
        'comparison': {'primary','stable_attributes','other_commune','common_grade_year_support',
                       'age_gender_treated_post_standardized','never_plus_future_school_exposure',
                       'never_plus_future_outcome','future_only_school_exposure','future_only_outcome',
                       'school_student_two_way_variance','fixed_effects_diagnostic'},
        'calendar': {'pretrend_placebo_late','late_strict_pre','pretrend_placebo_early','early_strict_pre'},
    }
    variants=set().union(*expected_variants.values())
    eligible=[r for r in combined['results'] if r.get('outcome')=='any_he_2yr'
              and r.get('cohort') is None and r.get('variant') in variants]
    source={(r.get('variant'),r.get('outcome'),r.get('era'),r.get('cohort')):r for r in eligible}
    need(len(source)==len(eligible),
         'IV pooled sensitivity source keys duplicate')
    by_kind={'comparison':[],'calendar':[]}
    panels=set()
    for fig in figures:
        kind,era=fig.get('kind'),fig.get('era')
        need(kind in by_kind and era in {'historical','modern'} and (kind,era) not in panels,
             'IV sensitivity family/era panel missing or duplicate')
        panels.add((kind,era));rows=fig['source_rows']
        need({r.get('variant') for r in rows}==expected_variants[kind] and len(rows)==len(expected_variants[kind]),
             f'IV sensitivity panel variants incomplete: {kind}:{era}')
        for row in rows:
            need(set(row)<=set(source.get((row.get('variant'),row.get('outcome'),row.get('era'),None),{})) |
                 {'cohort_start','cohort_end','period_inherited_from_primary'},
                 'IV sensitivity figure unreviewed source field')
            need('rates' not in row and not any(SMALL_COUNT.fullmatch(field) for field in row),
                 'IV sensitivity figure exposes person counts or arm rates')
            key=(row.get('variant'),row.get('outcome'),row.get('era'),None)
            original=source.get(key)
            need(original is not None and row.get('era')==era,
                 f'IV sensitivity figure source row missing: {key}')
            for field,value in row.items():
                if field in original:
                    need(value==original[field],f'IV sensitivity figure source drift: {key}:{field}')
            period=original.get('cohort_range')
            if period is None:
                primary=source.get(('primary','any_he_2yr',era,None))
                need(row.get('period_inherited_from_primary') is True and primary is not None,
                     f'IV sensitivity period inheritance invalid: {key}')
                period=primary.get('cohort_range')
            else:need(row.get('period_inherited_from_primary') is False,
                      f'IV sensitivity period inheritance drift: {key}')
            need(period==[row.get('cohort_start'),row.get('cohort_end')],
                 f'IV sensitivity cohort period drift: {key}')
        by_kind[kind].extend(rows)
    need(panels=={(kind,era) for kind in by_kind for era in ('historical','modern')},
         'IV sensitivity four panels required')
    for kind,expected_count in (('comparison',22),('calendar',8)):
        rows=by_kind[kind]
        need(len(rows)==expected_count,f'IV sensitivity {kind} row count drift')
        path=folder/f'post4-sensitivity-{kind}-all.csv'
        public_text(path)
        with path.open(encoding='utf-8',newline='') as stream:
            reader=csv.DictReader(stream);csv_rows=list(reader);fields=reader.fieldnames or []
        need(len(csv_rows)==expected_count and set(fields)==set().union(*(set(r) for r in rows))
             and 'rates' not in fields and not any(SMALL_COUNT.fullmatch(field) for field in fields),
             f'IV sensitivity {kind} CSV fields/rows drift')
        seen=set();lookup={(r['variant'],r['era']):r for r in rows}
        need(len(lookup)==expected_count,f'IV sensitivity {kind} rows duplicate')
        for row in csv_rows:
            key=(row['variant'],row['era'])
            need(key in lookup and key not in seen,f'IV sensitivity {kind} CSV key drift: {key}')
            seen.add(key);original=lookup[key]
            for field in fields:
                value=original.get(field)
                if isinstance(value,(list,dict)):
                    try:matches=json.loads(row[field])==value
                    except (json.JSONDecodeError,TypeError):matches=False
                else:matches=row[field]==('' if value is None else str(value))
                need(matches,f'IV sensitivity {kind} CSV source drift: {key}:{field}')

def check_derivatives(root,series,spec,bindings,docs,*,iv_companion=None,iv_combined=None,
                      iii_record=None,iii_private=None):
    entries=spec.get('derivative_manifests')
    need(isinstance(entries,list),'derivative_manifests list required')
    if series=='IV':need(len(entries)==1 and iv_companion is not None and iv_combined is not None,
                          'IV sensitivity companion manifest required')
    else:need(len(entries)==1 and iii_record is not None,'III sensitivity projected companion required')
    count=0
    for entry in entries:
        need(isinstance(entry,dict) and entry.get('family')=='sensitivity','unsupported derivative family')
        source=bound(entry.get('source'),root,public=root)
        if series=='IV':need(source==iv_companion,'IV sensitivity source must be combined projection')
        public_text(source)
        if series=='III':
            expected=root/'assets/data/tesis-scientific-reset/post3-sensitivity-source.json'
            need(source==expected.resolve(),'III sensitivity source must be public projected aggregate')
            need(sha(source)==POST3_SENSITIVITY_PUBLIC_BYTES_SHA,
                 'III public sensitivity projection bytes drift')
            public_sensitivity=obj(source)
            check_iii_sensitivity_public(public_sensitivity,iii_record,iii_private)
        manifest_path=bound(entry.get('manifest'),root,public=root)
        manifest=obj(manifest_path)
        public_text(manifest_path)
        add_public_binding(root,bindings,source);add_public_binding(root,bindings,manifest_path)
        need(manifest.get('family')=='sensitivity' and manifest.get('source_sha256')==sha(source),'sensitivity manifest source drift')
        if series=='IV':need(manifest.get('series')=='IV' and manifest.get('source_file')=='public-combined-projection.json',
                             'IV sensitivity manifest companion binding missing')
        if series=='IV':need(manifest.get('projection_code_sha256')==POST4_PROJECTION_CODE_SHA,
                             'IV sensitivity manifest projection code binding drift')
        need(manifest.get('f2_complete') is True and manifest.get('publication_authorized') is True,'sensitivity manifest not authorized')
        need(isinstance(manifest.get('units'),dict) and manifest['units'],'sensitivity units missing')
        figures=manifest.get('figures'); files=manifest.get('files')
        need(isinstance(figures,list) and figures and isinstance(files,list) and files,'sensitivity figures/files missing')
        names=[f.get('name') for f in files]
        need(len(names)==len(set(names)),'sensitivity duplicate file names')
        for item in files:
            name=item['name'];path=public_member(root,manifest_path.parent,name)
            need(path.is_file() and item.get('sha256')==sha(path),f'sensitivity file hash drift: {name}')
            public_text(path);add_public_binding(root,bindings,path)
        if series=='III':
            need('sensitivity-inventory-all.csv' in names,'III sensitivity inventory CSV missing')
            csv_against_iii_sensitivity_inventory(
                manifest_path.parent/'sensitivity-inventory-all.csv',public_sensitivity['sensitivities'])
        if series=='IV':
            need('public-combined-projection.json' in names and
                 sha(manifest_path.parent/'public-combined-projection.json')==sha(source),
                 'IV sensitivity manifest combined projection companion drift')
            need({'post4-sensitivity-comparison-all.csv','post4-sensitivity-calendar-all.csv',
                  'post4-sensitivity-calendar-window-matrix.csv'}<=set(names),
                 'IV sensitivity shared CSV missing')
            need({name for name in names if name.endswith('.html')}==set(IV_TABLE_NAMES),
                 'IV inline sensitivity table inventory drift')
            for name in IV_TABLE_NAMES:
                inline=root/'_includes/tesis-reset-tables'/name
                need(inline.is_file() and not inline.is_symlink() and
                     inline.read_bytes()==(manifest_path.parent/name).read_bytes(),
                     f'IV inline sensitivity table bytes drift: {name}')
                public_text(inline);add_public_binding(root,bindings,inline)
            check_iv_sensitivity_rows(figures,manifest_path.parent,iv_combined)
        for fig in figures:
            stem=fig.get('stem')
            need(isinstance(stem,str) and re.fullmatch(r'post[34]-[a-z0-9_-]+',stem),'sensitivity figure stem invalid')
            need(isinstance(fig.get('source_rows'),list) and fig['source_rows'],'sensitivity figure rows missing')
            csv_names=[f'{stem}.csv'] if series=='III' else []
            for name in [*csv_names,*[f'{stem}-{lang}-{theme}-{size}.{ext}' for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]]:
                need(name in names,f'sensitivity visual/CSV missing: {name}')
            for lang in ('es','en'):
                need(all(isinstance((fig.get(field) or {}).get(lang),str) and fig[field][lang].strip() for field in ('alt','caption','source_citation')),'sensitivity figure alt/caption/source missing')
                need(stem in docs[('post',lang)] or stem in docs[('annex',lang)],f'sensitivity figure link missing: {stem}:{lang}')
            count+=1
    return count

def check_no_unmanifested_figures(root,series,docs,bindings):
    number=IDENTITY[series]['number']
    prefix=f'assets/images/tesis-post{number}/'
    for (kind,lang),body in docs.items():
        for rel in re.findall(re.escape(prefix)+r'[a-zA-Z0-9_./-]+\.(?:svg|png|csv)',body):
            need(rel in bindings,f'unmanifested figure/data reference: {series}:{kind}:{lang}:{rel}')

def check_review(root,review_name,bindings):
    need(isinstance(review_name,str) and review_name and not Path(review_name).is_absolute(),'semantic review path invalid')
    review_path=(root/review_name).resolve()
    need(review_path.is_relative_to(root) and review_path.is_file(),'semantic review path missing/escaping')
    public_text(review_path);review=obj(review_path)
    need(review.get('decision')=='APPROVE' and review.get('scope')=='semantic_scientific_reset_iii_iv' and isinstance(review.get('reviewer'),str) and review['reviewer'].strip(), 'independent semantic review missing')
    need(review.get('bindings')==bindings,'semantic review missing/stale exact bindings')

def verify(root,contract_path,local_evidence=None):
    root=Path(root).resolve(); contract_path=Path(contract_path).resolve()
    need(root.is_dir() and contract_path.is_file(),'site root/publication contract missing')
    contract=obj(contract_path);public_text(contract_path)
    need(contract.get('schema_version')==2 and set(contract.get('series',{}))=={'III','IV'},'scientific reset v2 III/IV contract required; legacy bypass rejected')
    need(contract_path.is_relative_to(root),'publication contract must be within site root')
    bindings={};add_public_binding(root,bindings,contract_path)
    checked={'documents':0,'figures':0,'primary_rows':0}
    receipt_path=bound(contract.get('source_receipt'),root,public=root)
    public_text(receipt_path);receipt=obj(receipt_path)
    need(receipt.get('schema_version')==1 and receipt.get('status')=='LOCAL_F2_VALIDATED_PUBLIC_BINDING' and set(receipt.get('series',{}))=={'III','IV'},'source receipt missing/incomplete')
    add_public_binding(root,bindings,receipt_path)
    private=obj(Path(local_evidence).resolve()) if local_evidence else None
    if private:
        need(set(private.get('series',{}))=={'III','IV'},'private F2 evidence III/IV missing')
    for series,fixed in IDENTITY.items():
        spec=contract['series'][series]
        record=receipt['series'][series]
        need(isinstance(record,dict),'source receipt series invalid')
        hash_fields={'protocol_sha256','primary_sha256','sensitivity_sha256','public_aggregate_sha256'}
        hash_fields|=({'primary_receipt_sha256','anticipation_source_sha256'} if series=='III' else {'inventory_sha256','reconciliation_sha256'})
        need(all(isinstance(record.get(k),str) and SHA.fullmatch(record[k]) for k in hash_fields),f'{series} source receipt hashes missing/invalid')
        validators=record.get('validators')
        expected_validators={'primary','sensitivity','anticipation'} if series=='III' else {'reconciliation'}
        need(isinstance(validators,list) and {x.get('name') for x in validators}==expected_validators and all(x.get('exit_code')==0 and x.get('status')=='passed' for x in validators),'source validation receipts missing/red')
        aggregate=bound(spec.get('public_aggregate'),root,public=root)
        public_text(aggregate);add_public_binding(root,bindings,aggregate)
        need(record.get('public_aggregate_sha256')==sha(aggregate),'public aggregate/receipt hash drift')
        source=obj(aggregate)
        need(source.get('metadata',{}).get('protocol_sha256')==record['protocol_sha256'],f'{series} public aggregate protocol drift')
        iv_companion=None;iv_combined=None
        if series=='III':
            need(sha(aggregate)==POST3_PRIMARY_PUBLIC_BYTES_SHA,
                 'III public primary projection bytes drift')
            check_iii_projection_shape(source,record['primary_sha256'])
        else:
            private_spec=private['series']['IV'] if private else None
            iv_companion,iv_combined,_=check_iv_projection(
                root,spec,source,record,bindings,private_spec,
                Path(local_evidence).resolve().parent if private else None)
        need(isinstance(source.get('results'),list) and len(source['results'])==(43 if series=='III' else 138),'public aggregate primary coverage incomplete')
        unique(source['results'],key3 if series=='III' else key4,f'{series} public primary')
        if series=='IV':
            inventory=bound(spec.get('inventory'),root,public=root)
            public_text(inventory);add_public_binding(root,bindings,inventory)
            inv=obj(inventory)
            need(record.get('inventory_sha256')==sha(inventory) and inv.get('status')=='PREOUTCOME_EXPECTED_KEYS_NO_EFFECT_SELECTION','IV public inventory receipt drift')
            expected_keys=unique(inv.get('result_keys'),key4full,'IV public expected')
            need(len(expected_keys)==2344 and len([x for x in expected_keys if x[0]=='primary'])==144 and len(unique(inv.get('coverage_keys'),lambda x:json.dumps(x,sort_keys=True),'IV public coverage'))==4992 and len(unique(inv.get('heterogeneity_contrast_keys'),lambda x:json.dumps(x,sort_keys=True),'IV public contrasts'))==800,'IV public preoutcome inventory incomplete')
        docs={}
        for kind in ('post','annex'):
            for lang in ('es','en'):
                path,body=document(root,fixed,kind,lang);add_public_binding(root,bindings,path);docs[(kind,lang)]=body;checked['documents']+=1
            es_notes=set(re.findall(r'^\[\^([A-Za-z0-9_-]+)\]:',docs[(kind,'es')],re.M))
            en_notes=set(re.findall(r'^\[\^([A-Za-z0-9_-]+)\]:',docs[(kind,'en')],re.M))
            need(es_notes==en_notes,f'{series} {kind} bilingual footnote parity drift')
        if private:
            private_spec=private['series'][series]
            local_bindings={}
            primary=check_f2_iii(private_spec,Path(local_evidence).resolve().parent,local_bindings) if series=='III' else check_f2_iv(private_spec,Path(local_evidence).resolve().parent,local_bindings)
            names={'protocol':'protocol_sha256','primary':'primary_sha256','sensitivity':'sensitivity_sha256'}
            names.update({'primary_receipt':'primary_receipt_sha256'} if series=='III' else {'inventory':'inventory_sha256','reconciliation':'reconciliation_sha256'})
            for name,field in names.items():
                need(record.get(field)==sha(bound(private_spec[name],Path(local_evidence).resolve().parent)),f'{series} private F2/public receipt drift: {field}')
            if series=='III':check_projection(source,primary,series,record['primary_sha256'])
        checked['primary_rows']+=len(source['results'])
        checked['figures']+=check_manifest(root,series,spec,aggregate,
                                           record['primary_sha256'] if series=='III' else sha(iv_companion),
                                           bindings,docs)
        if series=='III':
            checked['figures']+=check_anticipation(root,spec,bindings,docs,private['series']['III'].get('anticipation_source_dir') if private else None)
            anticipation_manifest=obj(bound(spec['anticipation_manifest'],root,public=root))
            need(record.get('anticipation_source_sha256')==anticipation_manifest.get('source_sha256'),'III anticipation source receipt drift')
        iii_private=None
        if private and series=='III':
            iii_private=obj(bound(private['series']['III']['sensitivity'],
                                  Path(local_evidence).resolve().parent))
        checked['figures']+=check_derivatives(root,series,spec,bindings,docs,
                                               iv_companion=iv_companion,iv_combined=iv_combined,
                                               iii_record=record if series=='III' else None,
                                               iii_private=iii_private)
        check_no_unmanifested_figures(root,series,docs,bindings)
    check_render_inputs(root,bindings)
    check_review(root,contract['semantic_review'],bindings)
    checked['scope']='local_f2_revalidated_and_public_custody' if private else 'public_custody_only_requires_local_f2_receipt'
    return checked

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--contract',type=Path,default=DEFAULT_CONTRACT)
    parser.add_argument('--local-evidence',type=Path,help='private local F2 inputs; never place in the public contract')
    args=parser.parse_args()
    try: checked=verify(args.root,args.contract,args.local_evidence)
    except (GateError,OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(f'FAIL scientific-reset-publication: {exc}',file=sys.stderr);return 1
    print('PASS scientific-reset-publication: '+json.dumps(checked,sort_keys=True));return 0

if __name__=='__main__': raise SystemExit(main())
