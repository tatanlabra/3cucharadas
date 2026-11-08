"""Discriminating red/green tests for the v2 source gate; no release approval."""
import csv
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/verify_thesis_scientific_reset.py'
PUBLIC_IV=SCRIPT.parents[1]/'assets/data/tesis-scientific-reset/post4-public-projection.json'
PUBLIC_III_SENS=SCRIPT.parents[1]/'assets/data/tesis-scientific-reset/post3-sensitivity-source.json'
VENDOR_IV=SCRIPT.with_name('post4_public_projection.py')
spec=importlib.util.spec_from_file_location('reset_gate',SCRIPT)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(value if isinstance(value,str) else json.dumps(value),encoding='utf-8')
    return path

def binding(path,base):return {'path':str(path.relative_to(base)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

class GateTests(unittest.TestCase):
    def test_render_inputs_are_required_and_bound_to_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);bindings={}
            with self.assertRaises(gate.GateError):gate.check_render_inputs(root,bindings)
            for name in ('_includes/thesis-reset-figure.html','_data/tesis_reset_figures.json','assets/css/main.scss'):
                write(root/name,'{}' if name.endswith('.json') else 'baseline')
            vendor=root/'scripts/post4_public_projection.py';vendor.parent.mkdir(parents=True)
            vendor.write_bytes(VENDOR_IV.read_bytes())
            (root/'scripts/verify_thesis_scientific_reset.py').write_bytes(SCRIPT.read_bytes())
            for name in gate.IV_TABLE_NAMES:
                write(root/'_includes/tesis-reset-tables'/name,'<table><caption>Fixture</caption></table>')
            gate.check_render_inputs(root,bindings)
            self.assertEqual(len(bindings),11)
            review=write(root/'review.json',{'decision':'APPROVE','scope':'semantic_scientific_reset_iii_iv','reviewer':'fixture-peer','bindings':dict(bindings)})
            gate.check_review(root,'review.json',bindings)
            write(root/'_includes/thesis-reset-figure.html','changed rendered figure')
            gate.check_render_inputs(root,bindings)
            with self.assertRaisesRegex(gate.GateError,'stale exact bindings'):gate.check_review(root,'review.json',bindings)
            vendor.write_bytes(vendor.read_bytes()+b'\n# drift\n')
            with self.assertRaisesRegex(gate.GateError,'projection code drift'):gate.check_render_inputs(root,bindings)

    def test_accessible_table_is_manifest_member_without_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);folder=root/'figures';folder.mkdir()
            self.assertEqual(gate.public_member(root,folder,'post4-comparisons-es.html'),folder/'post4-comparisons-es.html')
            for name in ('../post4.html','/tmp/post4.html','post4.js','post4.html/extra'):
                with self.assertRaises(gate.GateError):gate.public_member(root,folder,name)

    def test_live_missing_contract_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            run=subprocess.run([sys.executable,str(SCRIPT),'--root',str(root),'--contract',str(root/'absent.json')],capture_output=True,text=True)
            self.assertEqual(run.returncode,1,run.stderr)
            self.assertIn('contract missing',run.stderr)

    def test_legacy_contract_cannot_bypass_v2(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);contract=write(root/'contract.json',{'schema_version':1,'series':{'III':{},'IV':{}}})
            run=subprocess.run([sys.executable,str(SCRIPT),'--root',str(root),'--contract',str(contract)],capture_output=True,text=True)
            self.assertEqual(run.returncode,1,run.stderr)
            self.assertIn('legacy bypass rejected',run.stderr)

    def test_review_exact_hash_bindings_red_green(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);artifact=write(root/'artifact.csv','value\n1\n')
            bindings={'artifact.csv':gate.sha(artifact)}
            review=write(root/'review.json',{'decision':'APPROVE','scope':'semantic_scientific_reset_iii_iv','reviewer':'fixture-independent-peer','bindings':bindings})
            gate.check_review(root,'review.json',bindings)
            write(artifact,'value\n2\n')
            with self.assertRaisesRegex(gate.GateError,'stale exact bindings'):gate.check_review(root,'review.json',{'artifact.csv':gate.sha(artifact)})

    def test_v2_without_source_receipt_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);contract=write(root/'contract.json',{'schema_version':2,'series':{'III':{},'IV':{}}})
            run=subprocess.run([sys.executable,str(SCRIPT),'--root',str(root),'--contract',str(contract)],capture_output=True,text=True)
            self.assertEqual(run.returncode,1,run.stderr)
            self.assertIn('file binding missing',run.stderr)

    def test_bound_file_red_and_green(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=write(root/'a.json','{}');good=binding(path,root)
            self.assertEqual(gate.bound(good,root,public=root),path)
            write(path,'{"changed":1}')
            with self.assertRaisesRegex(gate.GateError,'stale SHA-256'):gate.bound(good,root,public=root)
            outside=write(root.parent/'codex-reset-test-outside.json','{}')
            try:
                with self.assertRaisesRegex(gate.GateError,'public path escapes'):gate.bound({'path':str(outside),'sha256':gate.sha(outside)},root,public=root)
            finally:outside.unlink()

    def test_public_small_count_red_green(self):
        with tempfile.TemporaryDirectory() as temp:
            path=write(Path(temp)/'aggregate.json',{'results':[{'n_treated':10}]})
            gate.public_text(path)
            write(path,{'results':[{'n_treated':9}]})
            with self.assertRaisesRegex(gate.GateError,'public small count exposed'):gate.public_text(path)

    def test_full_csv_uses_source_values_and_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'results-all.csv'
            src={'results':[{'outcome':'a','era':'modern','cohort_year':2018,'estimand':'descriptive','estimation_status':'ESTIMABLE_DESCRIPTIVE','identification_status':'DESCRIPTIVE_ONLY','estimate_pp':1.2,'ci_low_pp':None,'ci_high_pp':None,'n_treated':30,'n_control':90,'limitation':'not causal'}]}
            fields=['outcome','era','cohort_year','estimand','estimation_status','identification_status','estimate_pp','ci_low_pp','ci_high_pp','n_treated','n_control','limitation']
            def emit(row):
                with path.open('w',newline='',encoding='utf-8') as stream:
                    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerow(row)
            row={k:'' if v is None else str(v) for k,v in src['results'][0].items()}
            emit(row)
            self.assertEqual(len(gate.csv_against_source(path,src,'III')),1)
            row['estimate_pp']='2.1';emit(row)
            with self.assertRaisesRegex(gate.GateError,'CSV source drift'):gate.csv_against_source(path,src,'III')
            row['estimate_pp']='1.2';row['limitation']='causal';emit(row)
            with self.assertRaisesRegex(gate.GateError,'CSV source drift'):gate.csv_against_source(path,src,'III')

    def test_iii_before_after_complement_json_csv_red_green(self):
        results=[{'outcome':'a' if i<39 else f'pooled_{i}','era':'modern',
                  'cohort_year':2005+i if i<39 else None,'estimate_pp':1.2,
                  'treated_students_lost_to_support':1} for i in range(43)]
        coverage=[{'outcome':'a','era':'modern','cohort_year':2005+i,
                   'treated_students_before_support':20,
                   'treated_students_after_support':19} for i in range(39)]
        raw={'results':results,'coverage':coverage}
        shown={'projection':{'source_sha256':'a'*64,
                             'excluded_fields':['treated_students_lost_to_support'],
                             'coverage_excluded_fields':['treated_students_before_support'],
                             'redactions':[]},
               'results':[{k:v for k,v in row.items() if k!='treated_students_lost_to_support'}
                          for row in results],
               'coverage':[{k:v for k,v in row.items() if k!='treated_students_before_support'}
                           for row in coverage]}
        gate.check_projection(shown,raw,'III','a'*64)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'coverage-all.csv'
            def emit(rows):
                fields=sorted(set().union(*(set(row) for row in rows)))
                with path.open('w',encoding='utf-8',newline='') as stream:
                    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows)
            emit(shown['coverage'])
            self.assertEqual(len(gate.csv_against_iii_coverage(path,shown['coverage'])),39)
            shown['coverage'][0]['treated_students_before_support']=20
            with self.assertRaisesRegex(gate.GateError,'excluded count reintroduced'):
                gate.check_projection(shown,raw,'III','a'*64)
            shown['coverage'][0].pop('treated_students_before_support')
            emit(coverage)
            with self.assertRaisesRegex(gate.GateError,'excluded count reintroduced'):
                gate.csv_against_iii_coverage(path,shown['coverage'])

    def test_iii_projected_sensitivity_inventory_and_suppression_red_green(self):
        self.assertEqual(gate.sha(PUBLIC_III_SENS),gate.POST3_SENSITIVITY_PUBLIC_BYTES_SHA)
        self.assertEqual(gate.sha(PUBLIC_III_SENS.with_name('post3-public-aggregate.json')),
                         gate.POST3_PRIMARY_PUBLIC_BYTES_SHA)
        projected=json.loads(PUBLIC_III_SENS.read_text())
        record={'primary_sha256':projected['projection']['primary_source_sha256'],
                'sensitivity_sha256':projected['projection']['source_sha256']}
        gate.check_iii_sensitivity_public(projected,record)
        missing=copy.deepcopy(projected);missing['sensitivities'].pop()
        with self.assertRaisesRegex(gate.GateError,'inventory incomplete'):
            gate.check_iii_sensitivity_public(missing,record)
        leaked=copy.deepcopy(projected)
        suppressed=next(row for row in leaked['sensitivities'] if row['status']
                        =='PUBLIC_SUPPRESSED_SMALL_COMPOSITION_CHANGE')
        suppressed['estimate_pp']=0.0
        with self.assertRaisesRegex(gate.GateError,'suppressed sensitivity value reintroduced'):
            gate.check_iii_sensitivity_public(leaked,record)

    def test_iv_combined_public_projection_real_red_green(self):
        self.assertEqual(gate.sha(VENDOR_IV),gate.POST4_PROJECTION_CODE_SHA)
        self.assertEqual(gate.sha(PUBLIC_IV),gate.POST4_PUBLIC_BYTES_SHA)
        library=gate.post4_projection_library()
        public=json.loads(PUBLIC_IV.read_text())
        split=library.split_public_projection(public)
        record={'primary_sha256':library.PRIMARY_SHA256,
                'sensitivity_sha256':library.SENSITIVITY_SHA256}
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);combined=root/'post4-public-projection.json'
            combined.write_bytes(PUBLIC_IV.read_bytes())
            spec={'public_privacy_projection':binding(combined,root)}
            companion,observed,parts=gate.check_iv_projection(root,spec,split['primary'],record,{})
            self.assertEqual(companion,combined)
            self.assertEqual(observed,public)
            self.assertEqual(parts,split)
            with self.assertRaisesRegex(gate.GateError,'file binding missing'):
                gate.check_iv_projection(root,{},split['primary'],record,{})
            raw={'results':[{'outcome':'any_he_2yr','n_treated':8,'rates':{'treated_post':1}}]}
            write(combined,raw);spec['public_privacy_projection']=binding(combined,root)
            with self.assertRaisesRegex(gate.GateError,'combined projection bytes drift'):
                gate.check_iv_projection(root,spec,split['primary'],record,{})
            with patch.object(gate,'POST4_PUBLIC_BYTES_SHA',gate.sha(combined)):
                with self.assertRaisesRegex(gate.GateError,'public small count exposed'):
                    gate.check_iv_projection(root,spec,split['primary'],record,{})
            raw['results'][0]['n_treated']=20
            write(combined,raw);spec['public_privacy_projection']=binding(combined,root)
            with patch.object(gate,'POST4_PUBLIC_BYTES_SHA',gate.sha(combined)):
                with self.assertRaisesRegex(gate.GateError,'public combined projection invalid'):
                    gate.check_iv_projection(root,spec,split['primary'],record,{})
            mutated=json.loads(PUBLIC_IV.read_text())
            mutated['results'][0]['estimate_pp']=mutated['results'][0]['estimate_pp']+1
            write(combined,mutated);spec['public_privacy_projection']=binding(combined,root)
            with patch.object(gate,'POST4_PUBLIC_BYTES_SHA',gate.sha(combined)):
                with self.assertRaisesRegex(gate.GateError,'exact-content digest drift'):
                    gate.check_iv_projection(root,spec,split['primary'],record,{})
            combined.write_bytes(PUBLIC_IV.read_bytes());spec['public_privacy_projection']=binding(combined,root)
            wrong_primary=json.loads(json.dumps(split['primary']))
            wrong_primary['results'][0]['estimate_pp']+=1
            with self.assertRaisesRegex(gate.GateError,'primary differs from combined split'):
                gate.check_iv_projection(root,spec,wrong_primary,record,{})
            wrong_record={**record,'sensitivity_sha256':'0'*64}
            with self.assertRaisesRegex(gate.GateError,'combined/private source receipt drift'):
                gate.check_iv_projection(root,spec,split['primary'],wrong_record,{})

    def test_iv_public_projection_local_recomputes_from_pinned_aggregates(self):
        base=Path('/home/ende/Descargas/investigacion/tesis_2/article_post2/post4/analysis/post4-scientific-reset-v2/results')
        primary=base/'primary-r1-20261108T1416Z/aggregate_results.json'
        sensitivity=base/'sensitivity-calendar-r2/aggregate_sensitivities.json'
        if not primary.is_file() or not sensitivity.is_file():self.skipTest('pinned local aggregates unavailable')
        library=gate.post4_projection_library();public=json.loads(PUBLIC_IV.read_text())
        split=library.split_public_projection(public)
        record={'primary_sha256':library.PRIMARY_SHA256,'sensitivity_sha256':library.SENSITIVITY_SHA256}
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);combined=root/'post4-public-projection.json';combined.write_bytes(PUBLIC_IV.read_bytes())
            spec={'public_privacy_projection':binding(combined,root)}
            private={'primary':binding(primary,base),'sensitivity':binding(sensitivity,base)}
            gate.check_iv_projection(root,spec,split['primary'],record,{},private,base)
            swapped={'primary':private['sensitivity'],'sensitivity':private['primary']}
            with self.assertRaisesRegex(gate.GateError,'reprojection failed'):
                gate.check_iv_projection(root,spec,split['primary'],record,{},swapped,base)

    def test_duplicate_and_empty_inventory_red(self):
        rows=[{'outcome':'a','era':'modern','cohort_year':2018}]
        self.assertEqual(len(gate.unique(rows,gate.key3,'fixture')),1)
        for bad in ([],rows+rows):
            with self.assertRaises(gate.GateError):gate.unique(bad,gate.key3,'fixture')

    def test_manifest_figure_variant_and_source_red_green(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);folder=root/'assets/images/tesis-post3';folder.mkdir(parents=True)
            row={'outcome':'grade_progression_or_lag','era':'modern','cohort_year':2018,'estimand':'descriptive','estimation_status':'ESTIMABLE_DESCRIPTIVE','identification_status':'DESCRIPTIVE_ONLY','estimate_pp':1.2,'ci_low_pp':None,'ci_high_pp':None,'n_treated':30,'n_control':90,'limitation':'not causal'}
            coverage=[{'outcome':row['outcome'],'era':'modern','cohort_year':2005+i,
                       'treated_students_after_support':20} for i in range(39)]
            primary=write(root/'primary.json',{'results':[row],'coverage':coverage})
            stem='post3-grade_progression_or_lag-modern'
            fields=list(row)
            def emit(name):
                path=folder/name
                with path.open('w',newline='',encoding='utf-8') as stream:
                    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerow({k:'' if v is None else v for k,v in row.items()})
                return path
            coverage_csv=folder/'coverage-all.csv'
            with coverage_csv.open('w',newline='',encoding='utf-8') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(coverage[0]));writer.writeheader();writer.writerows(coverage)
            paths=[emit('results-all.csv'),emit(f'{stem}.csv'),coverage_csv]
            paths += [write(folder/f'{stem}-{lang}-{theme}-{size}.{ext}','<svg></svg>' if ext=='svg' else 'png') for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]
            figure={'outcome':row['outcome'],'era':'modern','source_rows':[row],'alt':{'es':'Alt','en':'Alt'},'source_citation':{'es':'Fuente','en':'Source'},'caption':{'es':'Límite','en':'Limit'}}
            manifest={'f2_complete':True,'publication_authorized':True,'source_sha256':gate.sha(primary),'figures':[figure],'files':[{'name':p.name,'sha256':gate.sha(p)} for p in paths]}
            path=write(folder/'manifest.json',manifest);spec={'manifest':binding(path,root)}
            docs={(kind,lang):stem for kind in ('post','annex') for lang in ('es','en')}
            self.assertEqual(gate.check_manifest(root,'III',spec,primary,gate.sha(primary),{},docs),1)
            manifest['files']=manifest['files'][:-1];write(path,manifest);spec['manifest']=binding(path,root)
            with self.assertRaisesRegex(gate.GateError,'figure variant/CSV missing'):gate.check_manifest(root,'III',spec,primary,gate.sha(primary),{},docs)
            manifest['files'].append({'name':paths[-1].name,'sha256':gate.sha(paths[-1])})
            manifest['source_sha256']='0'*64;write(path,manifest);spec['manifest']=binding(path,root)
            with self.assertRaisesRegex(gate.GateError,'manifest source drift'):gate.check_manifest(root,'III',spec,primary,gate.sha(primary),{},docs)

    def test_document_identity_structure_and_lexical_red(self):
        fixed=gate.IDENTITY['III']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            name=f"_posts/{fixed['date'][:10]}-{fixed['slug']}.md"
            path=root/name
            route=f"/datos/educacion/politica-publica/{fixed['slug']}/"
            head=f"---\nlang: es\nref: {fixed['ref']}\npermalink: {route}\ndate: {fixed['date']}\n---\n"
            body='\n'.join(f'## Cucharada {n}: Pregunta\nResultado descriptivo con límite claro.' for n in (1,2,3))
            write(path,head+body)
            self.assertEqual(gate.document(root,fixed,'post','es')[0],path)
            write(path,head+body+'\nLos cierres escolares causan daño.')
            with self.assertRaisesRegex(gate.GateError,'lexical causal promotion'):gate.document(root,fixed,'post','es')
            write(path,head+body.replace('Cucharada 2','Cucharada 4'))
            with self.assertRaisesRegex(gate.GateError,'three ordered spoonfuls'):gate.document(root,fixed,'post','es')

    def test_full_public_v2_review_graph_is_acyclic(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);data=root/'assets/data/tesis-scientific-reset';data.mkdir(parents=True)
            contract={'schema_version':2,'series':{},'source_receipt':None,'semantic_review':'assets/data/tesis-scientific-reset/review.json'}
            receipt={'schema_version':1,'status':'LOCAL_F2_VALIDATED_PUBLIC_BINDING','series':{}}
            public_iv=json.loads(PUBLIC_IV.read_text())
            iv_parts=gate.post4_projection_library().split_public_projection(public_iv)
            for series,fixed in gate.IDENTITY.items():
                number=fixed['number'];folder=root/f'assets/images/tesis-post{number}';folder.mkdir(parents=True)
                count=43 if series=='III' else 138
                if series=='III':
                    rows=[]
                    for i in range(count):
                        row={'outcome':'grade_progression_or_lag' if i<39 else f'pooled_{i}',
                             'era':'historical','estimand':'descriptive',
                             'estimation_status':'ESTIMABLE_DESCRIPTIVE',
                             'identification_status':'DESCRIPTIVE_ONLY','estimate_pp':1.2,
                             'ci_low_pp':None,'ci_high_pp':None,'n_treated':20,'n_control':30,
                             'limitation':'descriptive, not causal',
                             'cohort_year':2005+i if i<39 else None}
                        rows.append(row)
                    coverage=[{'outcome':'grade_progression_or_lag','era':'historical',
                               'cohort_year':2005+i,'treated_students_after_support':19}
                              for i in range(39)]
                    primary_sha='b'*64;sensitivity_sha='c'*64;protocol_sha='a'*64
                    aggregate=write(data/f'{series}-aggregate.json',{
                        'metadata':{'protocol_sha256':protocol_sha},
                        'projection':{'source_sha256':primary_sha,
                                      'excluded_fields':['treated_students_lost_to_support'],
                                      'coverage_excluded_fields':['treated_students_before_support'],
                                      'redactions':[]},'results':rows,'coverage':coverage})
                else:
                    rows=iv_parts['primary']['results'];primary_sha=gate.post4_projection_library().PRIMARY_SHA256
                    sensitivity_sha=gate.post4_projection_library().SENSITIVITY_SHA256
                    protocol_sha=gate.post4_projection_library().PROTOCOL_SHA256
                    aggregate=write(data/f'{series}-aggregate.json',iv_parts['primary'])
                def csv_file(path,these):
                    fields=sorted(set().union(*(set(row) for row in these)))
                    with path.open('w',newline='',encoding='utf-8') as stream:
                        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
                        writer.writerows({k:json.dumps(v,sort_keys=True) if isinstance(v,(list,dict)) else '' if v is None else v for k,v in row.items()} for row in these)
                    return path
                stem='post3-grade_progression_or_lag-historical' if series=='III' else 'post4-access-historical'
                primary_stem=stem
                files=[csv_file(folder/'results-all.csv',rows),csv_file(folder/f'{stem}.csv',rows[:1]),
                       csv_file(folder/'coverage-all.csv',coverage) if series=='III'
                       else write(folder/'coverage-all.csv','coverage\n1\n')]
                files += [write(folder/f'{stem}-{lang}-{theme}-{size}.{ext}','<svg></svg>' if ext=='svg' else 'png') for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]
                fig={'era':'historical','source_rows':rows[:1],'alt':{'es':'Alt','en':'Alt'},'caption':{'es':'Límite','en':'Limit'},'source_citation':{'es':'Fuente','en':'Source'}}
                fig.update({'outcome':'grade_progression_or_lag'} if series=='III' else {'kind':'access'})
                if series=='IV':
                    companion=folder/'public-combined-projection.json';companion.write_bytes(PUBLIC_IV.read_bytes());files.append(companion)
                manifest_payload={'f2_complete':True,'publication_authorized':True,
                                  'source_sha256':primary_sha if series=='III' else gate.sha(PUBLIC_IV),
                                  'figures':[fig],'files':[{'name':p.name,'sha256':gate.sha(p)} for p in files]}
                if series=='IV':manifest_payload.update({'family':'post4_primary_projected',
                    'source_file':'public-combined-projection.json',
                    'projection_code_sha256':gate.POST4_PROJECTION_CODE_SHA})
                manifest=write(folder/'manifest.json',manifest_payload)
                series_spec={'public_aggregate':binding(aggregate,root),'manifest':binding(manifest,root),'derivative_manifests':[]}
                record={'protocol_sha256':protocol_sha,'primary_sha256':primary_sha,'sensitivity_sha256':sensitivity_sha,'public_aggregate_sha256':gate.sha(aggregate)}
                if series=='III':
                    sensitivity_rows=[{'name':f'sensitivity_{i}','outcome':'grade_progression_or_lag',
                                       'era':'historical','metric':None,'status':'DESCRIPTIVE_SENSITIVITY_NO_CI'}
                                      for i in range(49)]
                    sensitivity_source=write(data/'post3-sensitivity-source.json',{
                        'metadata':{'primary_results_sha256':primary_sha},
                        'status':'SENSITIVITIES_COMPLETE',
                        'projection':{'source_sha256':sensitivity_sha,
                                      'primary_source_sha256':primary_sha,
                                      'policy':'post3-f3-candidate-allowlist-r1'},
                        'sensitivities':sensitivity_rows})
                    sensitivity_folder=folder/'sensitivity';sensitivity_folder.mkdir()
                    sensitivity_stem='post3-sensitivity-did'
                    sensitivity_files=[csv_file(sensitivity_folder/'sensitivity-inventory-all.csv',
                                                [{k:r[k] for k in ('name','outcome','era','metric','status')}
                                                 for r in sensitivity_rows]),
                                       csv_file(sensitivity_folder/f'{sensitivity_stem}.csv',
                                                sensitivity_rows[:1])]
                    sensitivity_files += [write(sensitivity_folder/f'{sensitivity_stem}-{lang}-{theme}-{size}.{ext}',
                                                 '<svg></svg>' if ext=='svg' else 'png')
                                          for lang in ('es','en') for theme in ('light','dark')
                                          for size in ('desktop','mobile') for ext in ('svg','png')]
                    sensitivity_manifest=write(sensitivity_folder/'manifest.json',{
                        'family':'sensitivity','source_sha256':gate.sha(sensitivity_source),
                        'f2_complete':True,'publication_authorized':True,
                        'units':{'did':'percentage_points'},
                        'figures':[{'stem':sensitivity_stem,'source_rows':sensitivity_rows[:1],
                                    'alt':{'es':'Alt','en':'Alt'},'caption':{'es':'Límite','en':'Limit'},
                                    'source_citation':{'es':'Fuente','en':'Source'}}],
                        'files':[{'name':p.name,'sha256':gate.sha(p)} for p in sensitivity_files]})
                    series_spec['derivative_manifests']=[{'family':'sensitivity',
                        'source':binding(sensitivity_source,root),
                        'manifest':binding(sensitivity_manifest,root)}]
                    sensor_dir=folder/'anticipation';sensor_dir.mkdir()
                    source_files=[{'name':f'{year}_{outcome}.json','sha256':'f'*64} for outcome,years in [('grade_progression_or_lag',range(2005,2025)),('persistent_nonenrollment_two_years',range(2005,2024))] for year in years]
                    source_hash=hashlib.sha256(json.dumps(sorted(source_files,key=lambda x:x['name']),sort_keys=True,separators=(',',':')).encode()).hexdigest()
                    sensor_rows=[]
                    for item in source_files:
                        year,outcome=item['name'].split('_',1);outcome=outcome.removesuffix('.json')
                        for arm in ('treated','control'):
                            boundary=year=='2005'
                            sensor_rows.append({'outcome':outcome,'era':'historical' if int(year)<=2015 else 'modern','cohort_year':year,'baseline_year':'' if boundary else str(int(year)-2),'transition_year':'' if boundary else str(int(year)-1),'arm':arm,'n':'' if boundary else '20','schools':'' if boundary else '10','rate_pp':'' if boundary else '50.0','display_status':'NOT_ESTIMABLE_PANEL_BOUNDARY' if boundary else 'OBSERVED','reason_es':'Límite','reason_en':'Limit'})
                    def sensor_csv(path,these):
                        with path.open('w',newline='',encoding='utf-8') as stream:
                            writer=csv.DictWriter(stream,fieldnames=list(sensor_rows[0]));writer.writeheader();writer.writerows(these)
                        return path
                    sensor_stem='post3-anticipation-grade_progression_or_lag-historical'
                    sensor_files=[sensor_csv(sensor_dir/'anticipation-all.csv',sensor_rows),sensor_csv(sensor_dir/f'{sensor_stem}.csv',sensor_rows[:2])]
                    sensor_files += [write(sensor_dir/f'{sensor_stem}-{lang}-{theme}-{size}.{ext}','<svg></svg>' if ext=='svg' else 'png') for lang in ('es','en') for theme in ('light','dark') for size in ('desktop','mobile') for ext in ('svg','png')]
                    sensor_manifest=write(sensor_dir/'manifest.json',{'family':'anticipation','source_status':'PRE_EVENT_ANTICIPATION_QA_NO_EFFECTS','f2_complete':True,'publication_authorized':True,'source_sha256':source_hash,'source_files':source_files,'figures':[{'stem':sensor_stem,'source_rows':sensor_rows[:2],'alt':{'es':'Alt','en':'Alt'},'caption':{'es':'Límite','en':'Limit'},'source_citation':{'es':'Fuente','en':'Source'}}],'files':[{'name':p.name,'sha256':gate.sha(p)} for p in sensor_files]})
                    series_spec['anticipation_manifest']=binding(sensor_manifest,root)
                    record.update({'primary_receipt_sha256':'d'*64,'anticipation_source_sha256':source_hash,'validators':[{'name':name,'status':'passed','exit_code':0} for name in ('primary','sensitivity','anticipation')]})
                else:
                    inv=write(data/'iv-inventory.json',{'status':'PREOUTCOME_EXPECTED_KEYS_NO_EFFECT_SELECTION','result_keys':[{'variant':'primary' if i<144 else 'sensitivity','outcome':'any_he_2yr','taxonomy':'historical','cohort':i} for i in range(2344)],'coverage_keys':[{'id':i} for i in range(4992)],'heterogeneity_contrast_keys':[{'id':i} for i in range(800)]})
                    series_spec['inventory']=binding(inv,root)
                    record.update({'inventory_sha256':gate.sha(inv),'reconciliation_sha256':'d'*64,'validators':[{'name':'reconciliation','status':'passed','exit_code':0}]})
                    public_companion=data/'post4-public-projection.json'
                    public_companion.write_bytes(PUBLIC_IV.read_bytes())
                    series_spec['public_privacy_projection']=binding(public_companion,root)
                    sensitivity_folder=folder/'sensitivity';sensitivity_folder.mkdir()
                    sensitivity_copy=sensitivity_folder/'public-combined-projection.json'
                    sensitivity_copy.write_bytes(PUBLIC_IV.read_bytes())
                    sensitivity_files=[sensitivity_copy]
                    comparison=['primary','stable_attributes','other_commune','common_grade_year_support',
                                'age_gender_treated_post_standardized','never_plus_future_school_exposure',
                                'never_plus_future_outcome','future_only_school_exposure','future_only_outcome',
                                'school_student_two_way_variance','fixed_effects_diagnostic']
                    calendar=['pretrend_placebo_late','late_strict_pre','pretrend_placebo_early','early_strict_pre']
                    pooled={(r.get('variant'),r.get('era')):r for r in public_iv['results']
                            if r.get('outcome')=='any_he_2yr' and r.get('cohort') is None
                            and r.get('variant') in set(comparison+calendar)}
                    sensitivity_figures=[];sensitivity_stems=[]
                    for kind,variants in (('comparison',comparison),('calendar',calendar)):
                        all_rows=[]
                        for era in ('historical','modern'):
                            stem=f'post4-sensitivity-{kind}-{era}';sensitivity_stems.append(stem)
                            display_rows=[]
                            for variant in variants:
                                origin=pooled[(variant,era)]
                                period=origin.get('cohort_range')
                                inherited=period is None
                                if inherited:period=pooled[('primary',era)]['cohort_range']
                                display_rows.append({k:origin[k] for k in ('variant','outcome','era','estimand','estimate_pp','ci_low_pp','ci_high_pp','confidence_level','treated_schools','control_schools','flags','estimation_status','identification_status','limitation')} |
                                                    {'cohort_start':period[0],'cohort_end':period[1],
                                                     'period_inherited_from_primary':inherited})
                            all_rows.extend(display_rows)
                            sensitivity_figures.append({'kind':kind,'era':era,'stem':stem,'source_rows':display_rows,
                                                        'alt':{'es':'Alt','en':'Alt'},'caption':{'es':'Límite','en':'Limit'},
                                                        'source_citation':{'es':'Fuente','en':'Source'}})
                            sensitivity_files.extend(write(sensitivity_folder/f'{stem}-{lang}-{theme}-{size}.{ext}',
                                                           '<svg></svg>' if ext=='svg' else 'png')
                                                     for lang in ('es','en') for theme in ('light','dark')
                                                     for size in ('desktop','mobile') for ext in ('svg','png'))
                        sensitivity_files.append(csv_file(sensitivity_folder/f'post4-sensitivity-{kind}-all.csv',all_rows))
                    sensitivity_files.append(write(sensitivity_folder/'post4-sensitivity-calendar-window-matrix.csv',
                                                   'outcome,grade,comparison\nany_he_2yr,1,late\n'))
                    for name in gate.IV_TABLE_NAMES:
                        origin=write(sensitivity_folder/name,'<table><caption>Projected fixture</caption></table>')
                        inline=root/'_includes/tesis-reset-tables'/name
                        inline.parent.mkdir(parents=True,exist_ok=True);inline.write_bytes(origin.read_bytes())
                        sensitivity_files.append(origin)
                    sensitivity_manifest=write(sensitivity_folder/'manifest.json',{
                        'family':'sensitivity','series':'IV','source_file':'public-combined-projection.json',
                        'projection_code_sha256':gate.POST4_PROJECTION_CODE_SHA,
                        'source_sha256':gate.sha(PUBLIC_IV),'f2_complete':True,'publication_authorized':True,
                        'units':{'comparison':'percentage_points','calendar':'percentage_points'},
                        'figures':sensitivity_figures,
                        'files':[{'name':p.name,'sha256':gate.sha(p)} for p in sensitivity_files]})
                    series_spec['derivative_manifests']=[{'family':'sensitivity',
                        'source':binding(public_companion,root),'manifest':binding(sensitivity_manifest,root)}]
                contract['series'][series]=series_spec;receipt['series'][series]=record
                for kind in ('post','annex'):
                    for lang in ('es','en'):
                        route=f"/datos/educacion/politica-publica/{fixed['slug']}/"+('anexo-metodologico/' if kind=='annex' else '')
                        name=f"_posts/{fixed['date'][:10]}-{fixed['slug']}{'-en' if lang=='en' else ''}.md" if kind=='post' else f"_pages/{fixed['annex']}{'-en' if lang=='en' else ''}.md"
                        head=f"---\nlang: {lang}\nref: {fixed['ref'] if kind=='post' else fixed['annex']}\npermalink: {route}\n"+(f"date: {fixed['date']}\n" if kind=='post' else '')+'---\n'
                        body=('\n'.join(f"## {'Cucharada' if lang=='es' else 'Spoonful'} {i}: Question\nA descriptive result with a visible limit and source context." for i in (1,2,3)) if kind=='post' else '## Appendix\nContext.')
                        body+='\n'+primary_stem
                        if series=='III' and kind=='annex':body+='\n'+sensor_stem+'\n'+sensitivity_stem
                        if series=='IV':body+='\n'+'\n'.join(sensitivity_stems)
                        write(root/name,head+body)
            for name in ('_includes/thesis-reset-figure.html','_data/tesis_reset_figures.json','assets/css/main.scss'):
                write(root/name,'{}' if name.endswith('.json') else 'fixture render input')
            vendor=root/'scripts/post4_public_projection.py';vendor.parent.mkdir(parents=True)
            vendor.write_bytes(VENDOR_IV.read_bytes())
            (root/'scripts/verify_thesis_scientific_reset.py').write_bytes(SCRIPT.read_bytes())
            receipt_path=write(data/'source-receipt.json',receipt);contract['source_receipt']=binding(receipt_path,root)
            contract_path=write(data/'publication-contract.json',contract)
            review_path=data/'review.json'
            bindings={str(p.relative_to(root)):gate.sha(p) for p in root.rglob('*') if p.is_file() and p!=review_path}
            write(review_path,{'decision':'APPROVE','scope':'semantic_scientific_reset_iii_iv','reviewer':'fixture-independent-peer','bindings':bindings})
            def verify_fixture():
                with (
                    patch.object(gate,'POST3_PRIMARY_PUBLIC_BYTES_SHA',gate.sha(data/'III-aggregate.json')),
                    patch.object(gate,'POST3_SENSITIVITY_PUBLIC_BYTES_SHA',gate.sha(sensitivity_source)),
                ):
                    return gate.verify(root,contract_path)
            self.assertEqual(verify_fixture()['scope'],'public_custody_only_requires_local_f2_receipt')
            raw_unprojected=root/'assets/images/tesis-post3/sensitivities-all.csv'
            write(raw_unprojected,'grade_unknown_treated\n20\n')
            with self.assertRaisesRegex(gate.GateError,'unprojected primary sensitivities CSV'):
                gate.check_manifest(root,'III',contract['series']['III'],
                                    root/contract['series']['III']['public_aggregate']['path'],
                                    receipt['series']['III']['primary_sha256'],{},
                                    {(kind,lang):primary_stem for kind in ('post','annex') for lang in ('es','en')})
            raw_unprojected.unlink()
            iv_spec=contract['series']['IV']
            with self.assertRaisesRegex(gate.GateError,'companion manifest required'):
                gate.check_derivatives(root,'IV',{**iv_spec,'derivative_manifests':[]},{},{},
                                       iv_companion=public_companion,iv_combined=public_iv)
            wrong_entry={'family':'sensitivity','source':binding(aggregate,root),
                         'manifest':binding(sensitivity_manifest,root)}
            with self.assertRaisesRegex(gate.GateError,'source must be combined projection'):
                gate.check_derivatives(root,'IV',{**iv_spec,'derivative_manifests':[wrong_entry]},
                                       {},{},iv_companion=public_companion,iv_combined=public_iv)
            sensitivity_figures[0]['source_rows'][0]['estimate_pp']+=1
            with self.assertRaisesRegex(gate.GateError,'figure source drift'):
                gate.check_iv_sensitivity_rows(sensitivity_figures,sensitivity_folder,public_iv)
            sensitivity_figures[0]['source_rows'][0]['estimate_pp']-=1
            comparison_csv=sensitivity_folder/'post4-sensitivity-comparison-all.csv'
            saved=comparison_csv.read_bytes()
            with comparison_csv.open(encoding='utf-8',newline='') as stream:
                reader=csv.DictReader(stream);fields=reader.fieldnames;csv_rows=list(reader)
            csv_rows[0]['estimate_pp']='999'
            with comparison_csv.open('w',encoding='utf-8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(csv_rows)
            with self.assertRaisesRegex(gate.GateError,'CSV source drift'):
                gate.check_iv_sensitivity_rows(sensitivity_figures,sensitivity_folder,public_iv)
            comparison_csv.write_bytes(saved)
            gate.check_iv_sensitivity_rows(sensitivity_figures,sensitivity_folder,public_iv)
            inline=root/'_includes/tesis-reset-tables'/gate.IV_TABLE_NAMES[0]
            saved_inline=inline.read_bytes();inline.write_bytes(b'<table><caption>Changed</caption></table>')
            sensitivity_docs={(kind,lang):'\n'.join(sensitivity_stems)
                              for kind in ('post','annex') for lang in ('es','en')}
            with self.assertRaisesRegex(gate.GateError,'inline sensitivity table bytes drift'):
                gate.check_derivatives(root,'IV',iv_spec,{},sensitivity_docs,
                                       iv_companion=public_companion,iv_combined=public_iv)
            inline.write_bytes(saved_inline)
            # Refresh every custody binding so omissions reach the inventory
            # guard, rather than failing earlier on a stale hash.
            inventory_payload=json.loads(inv.read_text())
            def refresh_iv_inventory_bindings():
                contract['series']['IV']['inventory']=binding(inv,root)
                receipt['series']['IV']['inventory_sha256']=gate.sha(inv)
                write(receipt_path,receipt)
                contract['source_receipt']=binding(receipt_path,root)
                write(contract_path,contract)
                current={str(p.relative_to(root)):gate.sha(p) for p in root.rglob('*') if p.is_file() and p!=review_path}
                write(review_path,{'decision':'APPROVE','scope':'semantic_scientific_reset_iii_iv','reviewer':'fixture-independent-peer','bindings':current})
            for axis in ('result_keys','coverage_keys'):
                removed=inventory_payload[axis].pop()
                write(inv,inventory_payload);refresh_iv_inventory_bindings()
                with self.assertRaisesRegex(gate.GateError,'IV public preoutcome inventory incomplete'):
                    verify_fixture()
                inventory_payload[axis].append(removed)
                write(inv,inventory_payload);refresh_iv_inventory_bindings()
                self.assertEqual(verify_fixture()['scope'],'public_custody_only_requires_local_f2_receipt')
            contract['changed_after_review']=True;write(contract_path,contract)
            with self.assertRaisesRegex(gate.GateError,'stale exact bindings'):verify_fixture()

if __name__=='__main__':unittest.main()
