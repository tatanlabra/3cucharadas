# D2: independent scientific code review, read only
Requested provider Anthropic, model alias sonnet. Return actual model only if observable; separate self-report from runtime evidence. No edits, tools unnecessary: full relevant packet is inline. No publication, no installs, no access to original microdata or personal configuration.
Source digest: e40cae6a5f77becf9634b51c1e4b75be3ea21bc1f2cfd56d5dd487c61d5b791f
Review estimand household vs dwelling, denominator all valid v9, survey domains all PSU, missingness, singletons, manual variance oracles, export correctness. Findings with severity P0/P1/P2, exact file+line, counterexample and remedy; accept or reject with limitations. Do not equate green tests with scientific proof. Return machine-readable JSON in code fence with task_id D2, source_digest, provider, requested_model, effective_identity_evidence, findings, limitations, verdict. Then concise rationale.
Official questionnaire https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf v9 printed p79 categories1..11; 3 own shared site paid,4 own shared site paying; v28 printed83 conditional principal household. Official use note https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf: expr national/regional, expc does not confer commune representativeness. Report unverified sources honestly.


## scripts/casen_shared_site.py
```
1: #!/usr/bin/env python3
2: """Read original CASEN sources; export only household aggregates and provenance."""
3: from pathlib import Path
4: import argparse
5: import hashlib
6: import io
7: import json
8: import platform
9: import subprocess
10: import sys
11: from datetime import datetime, timezone
12: import numpy as np
13: import pandas as pd
14: 
15: ROOT = Path(__file__).resolve().parents[1]
16: sys.path.insert(0,str(ROOT/'src'))
17: from casen_shared_site.core import prepare_households, estimates, require
18: 
19: 
20: def sha256(path):
21:     h=hashlib.sha256()
22:     with open(path,'rb') as f:
23:         for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
24:     return h.hexdigest()
25: 
26: 
27: def codebook_values(path,sheet,variable):
28:     data = pd.read_excel(path,sheet_name=sheet,header=None)
29:     match = data.index[data.iloc[:,1].eq(variable)]
30:     require(len(match)==1,f'codebook variable ambiguous: {variable}')
31:     i=int(match[0]); out={}
32:     while i<len(data) and (i==match[0] or pd.isna(data.iloc[i,1])):
33:         value,label=data.iloc[i,3],data.iloc[i,4]
34:         if isinstance(value,(int,float,np.number)) and not pd.isna(value): out[int(value)]=str(label).strip()
35:         i+=1
36:     return out
37: 
38: 
39: def main():
40:     parser=argparse.ArgumentParser(description=__doc__)
41:     for key in ['rdata','communes','codebook','communal-codebook','use-note','commune-universe']:
42:         parser.add_argument('--'+key,type=Path,required=True)
43:     parser.add_argument('--out',type=Path,default=ROOT/'artifacts/casen_shared_site')
44:     args=parser.parse_args()
45:     inputs={k:getattr(args,k.replace('-','_')) for k in ['rdata','communes','codebook','communal-codebook','use-note','commune-universe']}
46:     source_hashes={k:sha256(p) for k,p in inputs.items()}
47:     v9=codebook_values(args.codebook,'V','v9')
48:     require(set(v9)==set(range(1,12)),'v9 codebook codes changed')
49:     v28=codebook_values(args.codebook,'V','v28')
50:     require(set(v28)=={1,2},'v28 codebook codes changed')
51:     communal_book=pd.read_excel(args.communal_codebook,sheet_name='Base provincia comuna',header=None)
52:     require({'folio','id_persona','expc','comuna'}.issubset(set(communal_book.iloc[:,1].dropna())), 'communal codebook fields changed')
53:     region_names=codebook_values(args.codebook,'HdR','region')
54:     fields=['folio','id_persona','id_vivienda','pco1','v9','v28','expr','varstrat','varunit','region','area']
55:     # No microdata file: selected numeric columns travel R stdout -> Python memory only.
56:     rcode='''args<-commandArgs(TRUE);e<-new.env();load(args[1],envir=e); ds<-Filter(is.data.frame,as.list(e));stopifnot(length(ds)==1);d<-ds[[1]];cols<-strsplit(args[2],",",fixed=TRUE)[[1]];stopifnot(all(cols %in% names(d)));out<-as.data.frame(lapply(d[cols],as.numeric));write.table(out,stdout(),sep=",",row.names=FALSE,na="",quote=FALSE)'''
57:     r=subprocess.run(['Rscript','--vanilla','-e',rcode,str(args.rdata),','.join(fields)],check=True,capture_output=True)
58:     persons=pd.read_csv(io.BytesIO(r.stdout))
59:     with pd.io.stata.StataReader(args.communes,convert_categoricals=False) as reader:
60:         labels=reader.value_labels()
61:         communal=reader.read()
62:     # Numeric commune codes are labels supplied in the official complementary DTA.
63:     commune_labels=labels.get('comuna',{})
64:     if not commune_labels:
65:         candidates=[m for m in labels.values() if 5101 in m and 13101 in m]
66:         require(len(candidates)==1,'commune label dictionary unavailable')
67:         commune_labels=candidates[0]
68:     commune_names={int(k):str(v).strip() for k,v in commune_labels.items()}
69:     census=pd.read_excel(args.commune_universe,sheet_name='2',header=3)
70:     census=census.loc[pd.to_numeric(census['Código comuna'],errors='coerce').gt(0)]
71:     universe={int(row['Código comuna']):str(row['Comuna']).strip() for _,row in census.iterrows()}
72:     require(len(universe)==len(census),'duplicate commune in Census universe')
73:     require(set(commune_names).issubset(universe),'CASEN commune outside Census universe')
74:     # Keep official CASEN names for sampled communes; Census supplies absent names.
75:     commune_names={code:commune_names.get(code,name) for code,name in universe.items()}
76:     heads,audit=prepare_households(persons,communal)
77:     require(set(heads.region.unique())==set(range(1,17)),'source lacks a region')
78:     rows,sensitivity=estimates(heads,region_names,commune_names)
79:     missing_codes=sorted(set(universe)-set(heads.comuna.unique()))
80:     audit['commune_coverage']={'universe_source':args.commune_universe.name,'sheet':'2',
81:                               'universe_n':len(universe),'sampled_n':int(heads.comuna.nunique()),
82:                               'no_sample_n':len(missing_codes),
83:                               'no_sample':[{'territory_code':str(c),'territory_name':universe[c],'estimate':None,'ci_status':'no_sample'} for c in missing_codes]}
84:     audit.update(schema_version=1,sensitivity=sensitivity,codebook={'v9_valid':v9,'v9_positive':[3,4],'v9_missing_observed':audit['n_missing_v9'],'v28':v28},
85:                  ci={'method':'with-replacement ultimate-cluster Taylor ratio; complete household design including outside-domain PSU',
86:                      'z':1.959963985,'singleton_policy':'any singleton => SE/CI null; no undocumented adjustment',
87:                      'n_psu_definition':'All distinct (varstrat,varunit) pairs in full household sample, even outside domain',
88:                      'n_strata_definition':'All full-sample variance strata','finite_population_correction':False,
89:                      'commune':'descriptive, nonrepresentative, no CI'},
90: )
91:     audit['r2']={'formula':'R2(p_v) = R1 / (1 - p_v / 2)',
92:                  'assumptions':'p_v is hypothetical share of DWELLINGS in sites containing exactly two dwellings; all other sites contain one dwelling; R1=roles/dwellings, R2=roles/sites.',
93:                  'applied_to_fiscal_gap':False,'household_rate_used_as_parameter':False}
94:     args.out.mkdir(parents=True,exist_ok=True)
95:     table=pd.DataFrame(rows)
96:     table.to_csv(args.out/'estimates.csv',index=False)
97:     table.to_parquet(args.out/'estimates.parquet',index=False)
98:     def write(name,obj): (args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
99:     write('estimates.json',{'schema_version':1,'estimand':'p_h: household reports own site shared with other dwellings (v9=3/4) / all valid households','rows':rows})
100:     write('audit.json',audit)
101:     require(source_hashes=={k:sha256(p) for k,p in inputs.items()},'source changed during execution')
102:     code_paths=[Path(__file__),*(ROOT/'src/casen_shared_site').glob('*.py')]
103:     provenance={'schema_version':1,'generated_at':datetime.now(timezone.utc).isoformat(),
104:                 'sources':[{'id':k,'filename':p.name,'sha256':source_hashes[k]} for k,p in inputs.items()],
105:                 'official_source':'https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024',
106:                 'use_note':'https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf',
107:                 'code_sha256':{str(p.relative_to(ROOT)):sha256(p) for p in code_paths},
108:                 'outputs_sha256':{name:sha256(args.out/name) for name in ['estimates.csv','estimates.parquet','estimates.json','audit.json']},
109:                 'runtime':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,
110:                            'R':subprocess.run(['Rscript','--version'],capture_output=True,text=True,check=True).stdout.strip()},
111:                 'unit':'household','raw_data_exported':False,'sources_unchanged_after_run':True,
112:                 'limitations':['Not a dwelling or site count','Not a fiscal-gap adjustment','Communes nonrepresentative and exploratory','Normal approximation; no singleton correction','No global optimality claim']}
113:     write('provenance.json',provenance)
114:     print(json.dumps({'status':'ok','n_persons':len(persons),'n_households':len(heads),'n_rows':len(rows),'national':rows[0]},ensure_ascii=False))
115: 
116: if __name__=='__main__': main()
```

## src/casen_shared_site/core.py
```
1: """Audited household selection and full-design Taylor ratio linearization."""
2: from __future__ import annotations
3: import math
4: import numpy as np
5: import pandas as pd
6: 
7: Z = 1.959963985
8: VALID_V9 = frozenset(range(1, 12))
9: DENOMINATOR = 'All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.'
10: 
11: 
12: def require(condition, message):
13:     if not condition:
14:         raise ValueError(message)
15: 
16: 
17: def prepare_households(persons, communal):
18:     """Join at official person key, then select one head per household. Fail closed."""
19:     keys = ['folio', 'id_persona']
20:     for name, frame in [('main', persons), ('communal', communal)]:
21:         require(not frame[keys].isna().any().any(), f'{name}: missing person key')
22:         require(not frame.duplicated(keys).any(), f'{name}: duplicate person key')
23:     require(len(persons) > 0, 'empty source')
24:     joined = persons.merge(communal[keys + ['expc', 'comuna']], on=keys,
25:                            how='outer', validate='one_to_one', indicator=True)
26:     require(joined['_merge'].eq('both').all(), 'source join does not cover identical person keys')
27:     joined = joined.drop(columns='_merge')
28:     heads = joined.loc[joined.pco1.eq(1)].copy()
29:     require(len(heads) == joined.folio.nunique() and not heads.folio.duplicated().any(),
30:             'exactly one household head required for every folio')
31:     for field in ['id_vivienda', 'region', 'area', 'varstrat', 'varunit', 'v9', 'v28', 'comuna']:
32:         require(joined.groupby('folio')[field].nunique(dropna=False).le(1).all(),
33:                 f'inconsistent household field: {field}')
34:     require(not heads[['id_vivienda', 'region', 'area', 'varstrat', 'varunit', 'comuna']].isna().any().any(),
35:             'missing household design/geography')
36:     for weight in ['expr', 'expc']:
37:         require(np.isfinite(heads[weight]).all() and heads[weight].gt(0).all(), f'invalid {weight}')
38:     require(heads.region.isin(range(1, 17)).all(), 'invalid region')
39:     require(heads.area.isin([1, 2]).all(), 'invalid area')
40:     require(set(map(tuple, persons[['varstrat','varunit']].drop_duplicates().to_numpy())) ==
41:             set(map(tuple, heads[['varstrat','varunit']].drop_duplicates().to_numpy())),
42:             'head selection lost a design PSU')
43:     heads['valid_v9'] = heads.v9.isin(VALID_V9)
44:     heads['shared'] = heads.v9.isin([3, 4])
45:     # Non-response codes are not silently folded into the negative category.
46:     unknown = heads.v9.notna() & ~heads.valid_v9
47:     require(not unknown.any(), 'undocumented v9 code')
48:     heads['flagged'] = False  # Guard failures stop export; v9 missing is separately counted.
49:     audit = {'n_persons': len(persons), 'n_communal_persons': len(communal),
50:              'n_joined_persons': len(joined), 'n_households': len(heads),
51:              'n_dwellings': int(heads.id_vivienda.nunique()), 'one_head_per_folio': True,
52:              'person_join': 'one_to_one_complete', 'design_psus_preserved': True,
53:              'n_missing_v9': int((~heads.valid_v9).sum()),
54:              'v9_head_counts': {str(k):int(v) for k,v in heads.v9.value_counts(dropna=False).items()},
55:              'invalid_positive_weight': {'expr':0, 'expc':0},
56:              'n_flagged_definition': 'Excluded household inconsistencies; export fails closed if any. Missing v9 separately counted.'}
57:     design_sizes = heads[['varstrat','varunit']].drop_duplicates().groupby('varstrat').size()
58:     audit['design'] = {'n_psu':int(design_sizes.sum()),'n_strata':len(design_sizes),
59:                        'n_singleton_strata':int(design_sizes.eq(1).sum()),
60:                        'min_psu_per_stratum':int(design_sizes.min()),
61:                        'max_psu_per_stratum':int(design_sizes.max())}
62:     # Dwelling representative is diagnostic only; no official dwelling weight exists here.
63:     groups = heads.groupby('id_vivienda')
64:     sizes = groups.size()
65:     principals = groups.v28.apply(lambda s:int(s.eq(1).sum()))
66:     singleton_ids = sizes.index[sizes.eq(1)]
67:     multi_ids = sizes.index[sizes.gt(1)]
68:     eligible_multi = multi_ids[principals.loc[multi_ids].eq(1)]
69:     diagnostic = heads.loc[heads.id_vivienda.isin(singleton_ids) |
70:                            (heads.id_vivienda.isin(eligible_multi) & heads.v28.eq(1))]
71:     audit['dwelling_diagnostic'] = {
72:         'unit':'sampled dwelling, unweighted diagnostic; never official dwelling estimator',
73:         'singleton_dwellings':len(singleton_ids), 'multiple_household_dwellings':len(multi_ids),
74:         'multiple_with_unique_principal':len(eligible_multi),
75:         'multiple_without_unique_principal':len(multi_ids)-len(eligible_multi),
76:         'selected_representatives':len(diagnostic),
77:         'selected_valid_v9':int(diagnostic.valid_v9.sum()),
78:         'selected_shared_v9':int(diagnostic.shared.sum()),
79:         'global_v28_filter_rejected':True,
80:         'households_v28_missing':int(heads.v28.isna().sum())}
81:     return heads.reset_index(drop=True), audit
82: 
83: 
84: def taylor_ratio(weights, strata, psus, domain, numerator):
85:     """With-replacement ultimate-cluster variance over ALL design PSU, nested by stratum.
86: 
87:     No undocumented singleton correction: any singleton prevents variance estimation.
88:     No finite population correction, since stage-specific population counts are unavailable.
89:     """
90:     w = np.asarray(weights, dtype=float)
91:     d = np.asarray(domain, dtype=bool)
92:     y = np.asarray(numerator, dtype=bool)
93:     h, u = np.asarray(strata), np.asarray(psus)
94:     require(all(len(a) == len(w) for a in [d,y,h,u]) and len(w)>0, 'invalid design vector lengths')
95:     require(np.isfinite(w).all() and (w>0).all(), 'invalid Taylor weights')
96:     require(not pd.isna(h).any() and not pd.isna(u).any(), 'missing Taylor design')
97:     denominator = float(w[d].sum())
98:     p = float(w[d & y].sum()/denominator) if denominator else None
99:     e = w * np.where(d, y.astype(float) - (p or 0), 0) / (denominator or 1)
100:     totals = pd.DataFrame({'h':h, 'u':u, 'e':e}).groupby(['h','u'], sort=False).e.sum()
101:     counts = totals.groupby(level=0).size()
102:     result = {'estimate':p, 'weighted_denominator':denominator, 'se':None,
103:               'ci_low':None, 'ci_high':None, 'n_psu':len(totals), 'n_strata':len(counts),
104:               'design_df':int(len(totals)-len(counts))}
105:     if not denominator:
106:         result['ci_status'] = 'not_estimable_empty_domain'
107:     elif counts.eq(1).any():
108:         result['ci_status'] = 'not_estimable_singleton'
109:     else:
110:         variance = 0.0
111:         for _, cluster in totals.groupby(level=0):
112:             n = len(cluster)
113:             variance += n/(n-1) * float(((cluster-cluster.mean())**2).sum())
114:         if p in (0.0, 1.0) or variance <= 0:
115:             result['ci_status'] = 'not_conclusive_boundary_or_degenerate'
116:         else:
117:             se = math.sqrt(variance)
118:             result.update(se=se, ci_low=max(0,p-Z*se), ci_high=min(1,p+Z*se),
119:                           ci_status='approximate_normal_95_taylor')
120:     return result
121: 
122: 
123: def estimates(heads, region_names, commune_names):
124:     rows, sensitivity = [], []
125:     domains = [('national','CL','Chile',np.ones(len(heads),dtype=bool),'expr')]
126:     domains += [('region',str(code),region_names[code],heads.region.eq(code).to_numpy(),'expr') for code in range(1,17)]
127:     domains += [('commune',str(code),commune_names[code],heads.comuna.eq(code).to_numpy(),'expc') for code in sorted(commune_names)]
128:     for scope, code, name, selected, weight in domains:
129:         d = selected & heads.valid_v9.to_numpy()
130:         result = taylor_ratio(heads[weight],heads.varstrat,heads.varunit,d,heads.shared)
131:         if scope == 'commune':
132:             result.update(se=None,ci_low=None,ci_high=None,ci_status='descriptive_nonrepresentative_no_ci')
133:             if not selected.any():
134:                 result.update(ci_status='no_sample',n_psu=0,n_strata=0,design_df=0)
135:         result.update(scope=scope,territory_code=code,territory_name=name,unit='household',
136:                       denominator_definition=DENOMINATOR,weight=weight,n_households=int(selected.sum()),
137:                       n_valid=int(d.sum()),n_missing=int((selected & ~heads.valid_v9).sum()),
138:                       n_flagged=int((selected & heads.flagged).sum()),
139:                       selection_note=('Complete sampled-commune aggregate, sorted by code; no ranking. Valparaíso/Viña del Mar selected after prior exploration, not confirmatory.' if scope=='commune' else 'National and all 16 regions, no outcome selection.'))
140:         if scope == 'commune' and not selected.any():
141:             result['selection_note'] = 'Census commune without sampled CASEN households; no sample is not a zero rate.'
142:         rows.append(result)
143:         total = float(heads.loc[selected,weight].sum())
144:         num = float(heads.loc[d & heads.shared.to_numpy(),weight].sum())
145:         miss = float(heads.loc[selected & ~heads.valid_v9.to_numpy(),weight].sum())
146:         urban = selected & heads.area.eq(1).to_numpy()
147:         rural = selected & heads.area.eq(2).to_numpy()
148:         by_area = {}
149:         for label, mask in [('urban',urban),('rural',rural)]:
150:             valid = mask & heads.valid_v9.to_numpy()
151:             den = float(heads.loc[valid,weight].sum())
152:             by_area[label] = {'n_households':int(mask.sum()),'weighted_household_share':float(heads.loc[mask,weight].sum()/total) if total else None,
153:                               'estimate':float(heads.loc[valid & heads.shared.to_numpy(),weight].sum()/den) if den else None}
154:         sensitivity.append({'scope':scope,'territory_code':code,'missing_weight':miss,
155:                             'missing_all_negative':num/total if total else None,
156:                             'missing_all_positive':(num+miss)/total if total else None,
157:                             'complete_case':result['estimate'],'area':by_area})
158:     return rows, sensitivity
```

## tests/test_casen_shared_site.py
```
1: """Independent manual oracles and negative controls, no raw-data dependency."""
2: from pathlib import Path
3: import importlib.util
4: import math
5: import json
6: import hashlib
7: import os
8: import subprocess
9: import sys
10: import unittest
11: import numpy as np
12: import pandas as pd
13: 
14: ROOT=Path(__file__).resolve().parents[1]
15: sys.path.insert(0,os.environ.get('CASEN_TEST_SRC',str(ROOT/'src')))
16: from casen_shared_site.core import prepare_households,taylor_ratio,estimates
17: 
18: 
19: def fixture():
20:     # Four households, one non-head. v28 absent for both singleton dwellings.
21:     rows=[(1,1,10,1,3,np.nan,1,1,1,5,1),
22:           (1,2,10,4,3,np.nan,1,1,1,5,1),
23:           (2,1,20,1,5,np.nan,2,1,2,5,2),
24:           (3,1,30,1,4,1,1,2,3,13,1),
25:           (4,1,30,1,8,2,2,2,4,13,1)]
26:     p=pd.DataFrame(rows,columns=['folio','id_persona','id_vivienda','pco1','v9','v28','expr','varstrat','varunit','region','area'])
27:     c=p[['folio','id_persona']].copy();c['expc']=[2,2,4,2,4];c['comuna']=[5101,5101,5101,13101,13101]
28:     return p,c
29: 
30: 
31: class HouseholdContract(unittest.TestCase):
32:     def test_household_not_person_or_owner_denominator(self):
33:         h,a=prepare_households(*fixture())
34:         self.assertEqual((a['n_persons'],len(h),a['n_dwellings']),(5,4,3))
35:         self.assertAlmostEqual(h.loc[h.shared,'expr'].sum()/h.expr.sum(),1/3)
36:         self.assertEqual(h.valid_v9.sum(),4) # rental and ceded included
37:         self.assertEqual(a['dwelling_diagnostic']['selected_representatives'],3)
38:         self.assertEqual(a['dwelling_diagnostic']['multiple_with_unique_principal'],1)
39:         self.assertEqual(a['dwelling_diagnostic']['selected_shared_v9'],2)
40: 
41:     def test_duplicate_head_rejected(self):
42:         p,c=fixture();p.loc[1,'pco1']=1
43:         with self.assertRaisesRegex(ValueError,'exactly one'): prepare_households(p,c)
44: 
45:     def test_missing_head_rejected(self):
46:         p,c=fixture();p.loc[0,'pco1']=2
47:         with self.assertRaisesRegex(ValueError,'exactly one'): prepare_households(p,c)
48: 
49:     def test_incomplete_join_rejected(self):
50:         p,c=fixture()
51:         with self.assertRaisesRegex(ValueError,'identical person'): prepare_households(p,c.iloc[:-1])
52: 
53:     def test_duplicate_join_key_rejected(self):
54:         p,c=fixture()
55:         with self.assertRaisesRegex(ValueError,'duplicate person'): prepare_households(p,pd.concat([c,c.iloc[:1]]))
56: 
57:     def test_nonpositive_weight_rejected(self):
58:         p,c=fixture();p.loc[0,'expr']=0
59:         with self.assertRaisesRegex(ValueError,'invalid expr'): prepare_households(p,c)
60: 
61:     def test_inconsistent_household_rejected(self):
62:         p,c=fixture();p.loc[1,'v9']=4
63:         with self.assertRaisesRegex(ValueError,'inconsistent household'): prepare_households(p,c)
64: 
65:     def test_unknown_code_rejected(self):
66:         for code in [12,-88,-99]:
67:             p,c=fixture();p.loc[2,'v9']=code
68:             with self.assertRaisesRegex(ValueError,'undocumented v9'): prepare_households(p,c)
69: 
70:     def test_missing_is_not_negative_and_bounds(self):
71:         p,c=fixture();p.loc[2,'v9']=np.nan
72:         h,a=prepare_households(p,c)
73:         rows,s=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago'})
74:         self.assertEqual(a['n_missing_v9'],1)
75:         self.assertEqual(rows[0]['n_valid'],3)
76:         self.assertAlmostEqual(rows[0]['estimate'],.5)
77:         self.assertAlmostEqual(s[0]['missing_all_negative'],1/3)
78:         self.assertAlmostEqual(s[0]['missing_all_positive'],2/3)
79:         self.assertEqual(s[0]['area']['rural']['estimate'],None)
80:         self.assertAlmostEqual(s[0]['area']['urban']['weighted_household_share'],2/3)
81: 
82:     def test_multihousehold_ambiguous_principal_diagnostic_only(self):
83:         p,c=fixture();p.loc[4,'v28']=1
84:         h,a=prepare_households(p,c)
85:         self.assertEqual(len(h),4)
86:         self.assertEqual(a['dwelling_diagnostic']['multiple_without_unique_principal'],1)
87:         self.assertEqual(a['dwelling_diagnostic']['selected_representatives'],2)
88: 
89:     def test_communal_no_ci_no_ranking(self):
90:         h,_=prepare_households(*fixture())
91:         rows,_=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago'})
92:         communes=[r for r in rows if r['scope']=='commune']
93:         self.assertEqual([r['territory_code'] for r in communes],['5101','13101'])
94:         for r in communes:
95:             self.assertEqual(r['weight'],'expc')
96:             self.assertEqual(r['ci_status'],'descriptive_nonrepresentative_no_ci')
97:             self.assertIsNone(r['ci_low']); self.assertIsNone(r['se'])
98: 
99:     def test_absent_commune_is_null_not_zero(self):
100:         h,_=prepare_households(*fixture())
101:         rows,s=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago',2202:'Ollagüe'})
102:         row=next(r for r in rows if r['territory_code']=='2202')
103:         self.assertEqual(row['ci_status'],'no_sample')
104:         self.assertIsNone(row['estimate']);self.assertIsNone(row['ci_low'])
105:         self.assertEqual((row['n_households'],row['n_psu']),(0,0))
106: 
107: 
108: class TaylorContract(unittest.TestCase):
109:     def test_manual_two_strata_oracle(self):
110:         # w=(1,2,1,2), y=(1,0,1,0), T=6, p=1/3.
111:         # e=(1/9,-1/9,1/9,-1/9), variance=2*(2*2/81)=8/81.
112:         r=taylor_ratio([1,2,1,2],[1,1,2,2],[1,2,3,4],[1]*4,[1,0,1,0])
113:         self.assertAlmostEqual(r['estimate'],1/3)
114:         self.assertAlmostEqual(r['se'],math.sqrt(8/81))
115:         self.assertEqual((r['n_psu'],r['n_strata'],r['design_df']),(4,2,2))
116:         self.assertEqual(r['ci_low'],0)
117: 
118:     def test_manual_outside_domain_psu_oracle(self):
119:         # One stratum, 3 PSU: domain={first,second}; e=(1/4,-1/4,0).
120:         # Variance=3/2*(1/16+1/16)=3/16, versus wrong 1/4 when filtered.
121:         r=taylor_ratio([1,1,1],[1]*3,[1,2,3],[1,1,0],[1,0,0])
122:         self.assertAlmostEqual(r['se'],math.sqrt(3)/4)
123:         self.assertEqual(r['n_psu'],3)
124:         self.assertNotAlmostEqual(r['se'],.5)
125: 
126:     def test_singleton_inside_and_outside_domain_null(self):
127:         for d in ([1,1,1],[1,1,0]):
128:             r=taylor_ratio([1]*3,[1,1,2],[1,2,3],d,[1,0,0])
129:             self.assertEqual(r['ci_status'],'not_estimable_singleton')
130:             self.assertEqual((r['n_psu'],r['n_strata'],r['design_df']),(3,2,1))
131:             self.assertIsNone(r['se']);self.assertIsNone(r['ci_low'])
132: 
133:     def test_boundary_and_degenerate_no_false_exact_ci(self):
134:         for y in ([0,0],[1,1]):
135:             r=taylor_ratio([1,1],[1,1],[1,2],[1,1],y)
136:             self.assertEqual(r['ci_status'],'not_conclusive_boundary_or_degenerate')
137:             self.assertIsNone(r['ci_low'])
138:         r=taylor_ratio([1]*4,[1]*4,[1,1,2,2],[1]*4,[1,0,1,0])
139:         self.assertEqual(r['ci_status'],'not_conclusive_boundary_or_degenerate')
140: 
141:     def test_empty_domain_not_zero(self):
142:         r=taylor_ratio([1,1],[1,1],[1,2],[0,0],[1,0])
143:         self.assertIsNone(r['estimate']);self.assertIsNone(r['ci_low'])
144: 
145:     def test_psu_nested_by_stratum(self):
146:         r=taylor_ratio([1,2,1,2],[1,1,2,2],[1,2,1,2],[1]*4,[1,0,1,0])
147:         self.assertEqual(r['n_psu'],4)
148:         self.assertAlmostEqual(r['se'],math.sqrt(8/81))
149: 
150:     def test_invalid_weights_rejected(self):
151:         for w in ([0,1],[np.nan,1],[-1,1]):
152:             with self.assertRaisesRegex(ValueError,'invalid Taylor weights'):
153:                 taylor_ratio(w,[1,1],[1,2],[1,1],[1,0])
154: 
155: 
156: class AggregateArtifacts(unittest.TestCase):
157:     def setUp(self):
158:         self.path=ROOT/'artifacts/casen_shared_site'
159:         self.rows=json.loads((self.path/'estimates.json').read_text())['rows']
160:         self.audit=json.loads((self.path/'audit.json').read_text())
161: 
162:     def test_formats_and_hashes_match(self):
163:         csv=pd.read_csv(self.path/'estimates.csv',dtype={'territory_code':str})
164:         pq=pd.read_parquet(self.path/'estimates.parquet')
165:         js=pd.DataFrame(self.rows)
166:         pd.testing.assert_frame_equal(csv,pq,check_dtype=False,atol=1e-13,rtol=1e-13)
167:         pd.testing.assert_frame_equal(js,pq,check_dtype=False,atol=1e-13,rtol=1e-13)
168:         prov=json.loads((self.path/'provenance.json').read_text())
169:         for name,expected in prov['outputs_sha256'].items():
170:             self.assertEqual(hashlib.sha256((self.path/name).read_bytes()).hexdigest(),expected,name)
171:         for name,expected in prov['code_sha256'].items():
172:             self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),expected,name)
173: 
174:     def test_coverage_partition_and_weighted_identity(self):
175:         national=self.rows[0];regions=[r for r in self.rows if r['scope']=='region']
176:         communes=[r for r in self.rows if r['scope']=='commune']
177:         self.assertEqual({r['territory_code'] for r in regions},{str(i) for i in range(1,17)})
178:         self.assertEqual(sum(r['n_households'] for r in regions),self.audit['n_households'])
179:         self.assertEqual(sum(r['n_households'] for r in communes),self.audit['n_households'])
180:         self.assertAlmostEqual(sum(r['weighted_denominator'] for r in regions),national['weighted_denominator'])
181:         self.assertAlmostEqual(sum(r['weighted_denominator']*r['estimate'] for r in regions)/national['weighted_denominator'],national['estimate'])
182:         coverage=self.audit['commune_coverage']
183:         self.assertEqual(len(communes),coverage['universe_n'])
184:         self.assertEqual(sum(r['ci_status']=='no_sample' for r in communes),coverage['no_sample_n'])
185:         self.assertEqual(coverage['universe_n'],coverage['sampled_n']+coverage['no_sample_n'])
186:         for r in communes:
187:             self.assertIsNone(r['se']);self.assertIsNone(r['ci_low']);self.assertIsNone(r['ci_high'])
188:             if not r['n_households']: self.assertIsNone(r['estimate'])
189: 
190:     def test_schema_privacy_and_no_fiscal_plug_in(self):
191:         expected={'scope','territory_code','territory_name','unit','denominator_definition','weight',
192:                   'n_households','n_valid','n_missing','n_flagged','weighted_denominator','estimate',
193:                   'se','ci_low','ci_high','ci_status','n_psu','n_strata','design_df','selection_note'}
194:         for r in self.rows:
195:             self.assertEqual(set(r),expected)
196:             self.assertEqual(r['unit'],'household')
197:             self.assertEqual(r['n_valid']+r['n_missing'],r['n_households'])
198:             if r['estimate'] is not None:self.assertTrue(0<=r['estimate']<=1)
199:         self.assertFalse(self.audit['r2']['applied_to_fiscal_gap'])
200:         self.assertFalse(self.audit['r2']['household_rate_used_as_parameter'])
201:         for name in ['estimates.json','audit.json','provenance.json']:
202:             text=(self.path/name).read_text()
203:             self.assertNotIn('/home/',text)
204:             self.assertNotIn('"id_persona":',text)
205:             self.assertNotIn('"folio":',text)
206: 
207: 
208: if __name__=='__main__': unittest.main()
```

## docs/casen-shared-site-method.md
```
1: # CASEN 2024: hogares con sitio propio compartido
2: 
3: ## Estimando y límites
4: 
5: `p_h = Σ expr × I(v9 ∈ {3,4}) / Σ expr × I(v9 ∈ {1,…,11})`, con una observación por hogar: su jefatura (`pco1=1`). El denominador incluye arrendatarios, cesionarios y las demás tenencias válidas; no se restringe a propietarios. Cada región usa la misma definición con dominio regional. El cálculo comunal usa `expc` y se publica únicamente como descripción exploratoria, sin inferencia representativa ni intervalos.
6: 
7: El indicador cuenta **hogares** que declaran sitio propio compartido con otras viviendas. No identifica todos los sitios compartidos: otros regímenes de tenencia pueden coexistir en un sitio. Tampoco identifica viviendas únicas, sitios únicos, roles fiscales, exenciones ni una fracción causal de la brecha entre roles y viviendas.
8: 
9: La [nota oficial de uso, enero de 2026](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf), páginas 1–5, define cobertura, unidades, factores y cruce por persona. Su distinción territorial sustenta `expr` para nacional/regiones y la advertencia comunal. El [portal oficial CASEN 2024](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024) proporciona la base y los libros de códigos; se congelan sus archivos locales por SHA-256 en `provenance.json`. La encuesta tiene dominios de diseño; ello no garantiza automáticamente precisión suficiente de este indicador particular.
10: 
11: ## Fuentes, extracción y validación
12: 
13: - R carga el RData original en un entorno aislado y entrega únicamente once columnas numéricas por una tubería de memoria a Python; ningún archivo derivado contiene personas, hogares ni identificadores.
14: - La base complementaria se une por `(folio, id_persona)` con cardinalidad uno a uno y cobertura idéntica en ambos sentidos; no hay unión por posición ni multiplicación de filas.
15: - Todos los hogares deben tener una sola jefatura; cada campo de vivienda, diseño, geografía, `v9` y `v28` debe ser consistente dentro del hogar. Un incumplimiento aborta la exportación.
16: - Se exigen pesos de jefatura `expr` y `expc` positivos y finitos, territorios/diseño no faltantes y conservación de todos los pares `(varstrat,varunit)` al pasar de personas a jefaturas.
17: - El libro de códigos, hoja `V`, contiene `v9=1,…,11`; positivos 3 y 4. `NA` se trata como falta de respuesta; cualquier código no documentado, incluidos sentinelas trasladados desde otra pregunta, aborta. Los códigos no se recodifican a cero.
18: - `v28=1/2` es una pregunta condicionada. No se usa como filtro general. En el diagnóstico de vivienda se toma el hogar único; en viviendas multihogar se exige un principal único. La selección es un diagnóstico muestral no ponderado, nunca un peso oficial de vivienda.
19: - `n_flagged` cuenta inconsistencias excluyentes: este pipeline falla cerrado ante cualquiera; los artefactos exitosos muestran cero. `n_missing` se refiere exclusivamente a `v9` ausente.
20: 
21: ## Incertidumbre de diseño
22: 
23: Para dominio `d`, total ponderado válido `T_d` y razón `p`, la contribución de cada hogar es `e_j = w_j I(j ∈ d) (y_j-p)/T_d`. Se agregan estas contribuciones por PSU anidada en estrato. La varianza es `Σ_h [m_h/(m_h−1)] Σ_i (e_hi−media_h)^2`.
24: 
25: Se conservan **todas las PSU del diseño**, incluyendo las exteriores al dominio y las que solo contienen respuestas no válidas, con contribución cero. `n_psu`, `n_strata` y `design_df` describen ese diseño completo, no el número de PSU efectivamente observado en una comuna. Para comunas sin muestra los tres se declaran cero y `ci_status=no_sample`.
26: 
27: La aproximación usa reposición a nivel de conglomerado y no aplica corrección de población finita, por faltar los tamaños por etapa. `IC95 = clip(p ± 1.959963985 SE, 0, 1)` es un intervalo normal aproximado, no un intervalo exacto. Cualquier estrato con una sola PSU invalida SE e IC (`not_estimable_singleton`), incluso fuera del dominio: no se inventa una política oficial para singleton. Razones en 0/1 o varianza degenerada producen `not_conclusive_boundary_or_degenerate` con SE/IC nulos, nunca una falsa certeza exacta. Dominio vacío produce estimación nula. Todas las comunas muestreadas tienen `descriptive_nonrepresentative_no_ci`.
28: 
29: La referencia Julia `_taylor_prop_se` se lee sin modificarla. La paridad se limita a fixtures con al menos dos PSU por estrato porque esa función omite singleton, mientras este pipeline los declara no estimables. Coincidencia entre implementaciones es una comprobación de consistencia; la prueba independiente es el oráculo algebraico manual: pesos `(1,2,1,2)`, dos estratos con dos PSU, `p=1/3`, `V=8/81`; otro dominio con dos de tres PSU exige `V=3/16`, que cambia incorrectamente a `1/4` si se elimina la PSU externa.
30: 
31: ## Robustez, cobertura y selección
32: 
33: `audit.json:sensitivity` entrega por territorio composición urbano/rural, tasas dentro de cada área, ponderación utilizada y cotas al reponer toda falta de respuesta como negativa o positiva. Son descripciones de composición, no un efecto causal urbano/rural. Si `Y` es el total positivo, `M` el peso faltante y `T` el total de hogares, las cotas son `Y/T` y `(Y+M)/T`. Si no hay faltantes ambas coinciden con la estimación de casos completos; esto no prueba ausencia de sesgos de medición o no respuesta de encuesta.
34: 
35: El universo comunal procede de `V1_Viviendas-y-hogares-censados.xlsx`, Censo 2024, hoja 2. El cruce observado tiene 346 comunas: 335 muestreadas y 11 sin muestra; se incluyen todas por CUT, sin ranking. Las comunas fuera de la muestra CASEN tienen `estimate=null`, `ci_status=no_sample` y conteos muestrales cero; no se imputan tasas cero. `audit.json:commune_coverage` contiene el cruce y los nombres/CUT ausentes. Valparaíso y Viña del Mar fueron seleccionadas después de exploración previa; sus resultados no son contrastes confirmatorios.
36: 
37: ## Resultado observado de esta ejecución
38: 
39: | Comprobación | Observación |
40: |---|---|
41: | Personas / hogares / viviendas muestrales | 218.367 / 78.654 / 77.618 |
42: | Positivos `v9=3/4` entre jefaturas | 787 hogares, sin faltantes `v9` |
43: | Total nacional expandido de hogares válidos | 7.143.171 con `expr` |
44: | `p_h` nacional | 1,0878222 %; SE 0,0600480 puntos porcentuales |
45: | IC normal aproximado nacional | 0,9701303–1,2055141 % |
46: | Diseño completo | 12.512 PSU, 756 estratos, 11.756 grados de libertad |
47: | Diagnóstico de vivienda | 76.712 viviendas unihogar y 906 multihogar; las 906 tienen principal único |
48: | Filtro general `v28` | Rechazado: 76.252 jefaturas tienen `v28` faltante |
49: 
50: Como contraste descriptivo, la composición nacional expandida es 88,4510 % urbana y 11,5490 % rural; las respectivas tasas son 1,0668 % y 1,2491 %. Valparaíso tiene 98,5093 % de peso urbano y Viña del Mar 100 %; sus tasas comunales descriptivas son 9,2681 % y 8,5995 %. No hay observaciones rurales en Viña del Mar: la tasa rural es nula en el sentido de dato ausente (`null`), no una tasa cero.
51: 
52: Estas cifras pertenecen a la ejecución y fuentes cuyos hashes figuran en los recibos; no son un oráculo fijado para futuras versiones.
53: 
54: ## Anexo algebraico sin aplicación fiscal
55: 
56: Definir `R1 = roles/viviendas` y `p_v` como una proporción **hipotética de viviendas** que están en sitios con exactamente dos viviendas, suponiendo que todos los otros sitios contienen una vivienda. Entonces `sitios = viviendas × (1 − p_v/2)` y `R2(p_v) = roles/sitios = R1/(1 − p_v/2)`. La fórmula cambia si cambia la definición del parámetro o la multiplicidad. **No sustituir `p_v` por `p_h`**, ni usar esta identidad para ajustar la brecha fiscal: no se dispone del enlace representativo vivienda–sitio–rol que permitiría hacerlo.
57: 
58: ## Reproducción y aceptación
59: 
60: Desde la raíz del repositorio analítico, definir argumentos con rutas locales autorizadas; las rutas privadas no forman parte de los artefactos públicos:
61: 
62: ```sh
63: /opt/entornos/mamba312/bin/python v5_brecha/scripts/casen_shared_site.py \
64:   --rdata "$CASEN_RDATA" --communes "$CASEN_COMMUNES" \
65:   --codebook "$CASEN_CODEBOOK" --communal-codebook "$CASEN_COMMUNAL_CODEBOOK" \
66:   --use-note "$CASEN_USE_NOTE" --commune-universe "$CENSUS_COMMUNES"
67: /opt/entornos/mamba312/bin/python -m unittest discover \
68:   -s v5_brecha/tests -p test_casen_shared_site.py -v
69: /opt/entornos/mamba312/bin/python v5_brecha/artifacts/casen_shared_site/evidence/reproduce_checks.py \
70:   --julia-reference "$JULIA_TAYLOR_SOURCE" --julia-project "$JULIA_REFERENCE_PROJECT"
71: ```
72: 
73: No se ejecuta `prepare_sources`, no se instala software y no se escribe en las fuentes externas. `evidence/verification.json` registra suites, hashes y paridad Julia. Cinco mutaciones aisladas deben salir no cero: quitar PSU exteriores, limitar indebidamente la tenencia del denominador, fabricar IC exacto de borde, contar personas como hogares y omitir singleton. La recuperación usa el código original cuyo hash se conserva. Los fixtures negativos de unión, pesos y claves deben rechazar la entrada. Los artefactos CSV/Parquet/JSON se comparan entre sí y con la partición regional ponderada.
74: 
75: `provenance.json` liga fuentes, código y salidas; `evidence/pipeline-receipt.json` liga ejecución y aceptación. Un hash distinto, una falla científica, falta de muestra convertida a cero, o datos privados en la exportación bloquea D1 y exige regenerar/revisar. Un test verde no demuestra causalidad, representatividad comunal ni optimalidad global.
76: 
77: Rollback: retirar únicamente los archivos propios de este módulo y sus agregados tras revisar el diff; conservar evidencia y trabajo ajeno. No modificar las fuentes, el pipeline fiscal anterior ni las proyecciones del blog. No se realiza commit ni publicación desde D1.
```

## artifacts/casen_shared_site/evidence/verification.json
```
1: {
2:   "task_id": "D1",
3:   "status": "verified_local_checks",
4:   "tests": [
5:     {
6:       "name": "tests-green",
7:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
8:       "exit_code": 0,
9:       "log": "tests-green.log",
10:       "sha256": "c45633d8d4c15afc7254391eeab3b268759a13a5454d4df75a5f45d411d90c01"
11:     },
12:     {
13:       "name": "red-drop-outside-domain-psu",
14:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
15:       "exit_code": 1,
16:       "log": "red-drop-outside-domain-psu.log",
17:       "sha256": "5e1423c9faeb54c59f74512e01c68081c78724b7d5186776fb8508f7788c21a3"
18:     },
19:     {
20:       "name": "red-wrong-ownership-denominator",
21:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
22:       "exit_code": 1,
23:       "log": "red-wrong-ownership-denominator.log",
24:       "sha256": "5ad45a3c6dfa4545675e927454f4af34c679e93bf2d87a70a4d2c70b1738defe"
25:     },
26:     {
27:       "name": "red-false-exact-boundary-ci",
28:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
29:       "exit_code": 1,
30:       "log": "red-false-exact-boundary-ci.log",
31:       "sha256": "4c077cad96a59cf80ab7a800adf543ef20b1e7354935a180e146e0a63d2b21ba"
32:     },
33:     {
34:       "name": "red-households-counted-as-persons",
35:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
36:       "exit_code": 1,
37:       "log": "red-households-counted-as-persons.log",
38:       "sha256": "9d293484b6494baa67096743446e0cd767acab951333eaf05636e7213a0ed6f0"
39:     },
40:     {
41:       "name": "red-singleton-silently-skipped",
42:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
43:       "exit_code": 1,
44:       "log": "red-singleton-silently-skipped.log",
45:       "sha256": "aab777941b98109b1f0ab90c6a9e75e16a50dd855fc2a3b418207bb6f3027970"
46:     },
47:     {
48:       "name": "tests-green-recovery",
49:       "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
50:       "exit_code": 0,
51:       "log": "tests-green-recovery.log",
52:       "sha256": "37e97c5285c28b4fe09a90202f36664180bf84bb8fb50dded558435419829ab8"
53:     }
54:   ],
55:   "mutants": "Synthetic code copies; each substitution applied once; originals unchanged",
56:   "code_sha256": {
57:     "src/casen_shared_site/core.py": "d9d530f911eb9ad3e5986b48167d8965a2e3e4c188295f4af56b76eddec3122f",
58:     "src/casen_shared_site/__init__.py": "5fd5525ded8ec6dd2e20997fdcdc61a9b76b7b415ee635ca043541aaf206fc2d"
59:   },
60:   "test_sha256": "5f9b0c27cf426f216dff98f3415f998de7946c2b915f5f3ed8c86c447dce4794",
61:   "harness_sha256": "75dd82b753ca0ba02f8906463431335f5396d7faef1f2fc7a580e4cb69168070",
62:   "julia": {
63:     "exit_code": 0,
64:     "version": "julia version 1.10.12",
65:     "reference_filename": "07b_complex_survey_ci.jl",
66:     "reference_sha256": "d0a2b89a3cf50ca440c908ed2027c87f6a976ebd4b4ce5fa7d86470a021ae94b",
67:     "project_sha256": {
68:       "Project.toml": "66faecd6009a1098604002a1f4fa0285d9a362e420bf03b5d1005762c3831088",
69:       "Manifest.toml": "3c116302af0fdd87c61ab6f848e2acddda47ed14afe28c4020c065ef45bdd14c"
70:     },
71:     "project_unchanged": true,
72:     "log_sha256": "9457aeb7f313bfaf48cc9589c2076441796bcd719d774308fd898aed18dbfbcb",
73:     "comparisons": [
74:       {
75:         "fixture": [
76:           [
77:             1.0,
78:             2.0,
79:             1.0,
80:             2.0
81:           ],
82:           [
83:             1,
84:             1,
85:             2,
86:             2
87:           ],
88:           [
89:             1,
90:             2,
91:             3,
92:             4
93:           ],
94:           [
95:             1,
96:             1,
97:             1,
98:             1
99:           ],
100:           [
101:             1,
102:             0,
103:             1,
104:             0
105:           ]
106:         ],
107:         "python": [
108:           0.3333333333333333,
109:           0.31426968052735443,
110:           0,
111:           0.9492905887444039,
112:           4,
113:           2
114:         ],
115:         "julia": [
116:           0.3333333333333333,
117:           0.31426968052735443,
118:           0.0,
119:           0.9492905887444039,
120:           4.0,
121:           2.0
122:         ],
123:         "max_abs_error": 0.0
124:       },
125:       {
126:         "fixture": [
127:           [
128:             1.0,
129:             1.0,
130:             1.0
131:           ],
132:           [
133:             1,
134:             1,
135:             1
136:           ],
137:           [
138:             1,
139:             2,
140:             3
141:           ],
142:           [
143:             1,
144:             1,
145:             0
146:           ],
147:           [
148:             1,
149:             0,
150:             0
151:           ]
152:         ],
153:         "python": [
154:           0.5,
155:           0.4330127018922193,
156:           0,
157:           1,
158:           3,
159:           1
160:         ],
161:         "julia": [
162:           0.5,
163:           0.4330127018922193,
164:           0.0,
165:           1.0,
166:           3.0,
167:           1.0
168:         ],
169:         "max_abs_error": 0.0
170:       },
171:       {
172:         "fixture": [
173:           [
174:             2.0,
175:             3.0,
176:             5.0,
177:             7.0,
178:             11.0,
179:             13.0
180:           ],
181:           [
182:             1,
183:             1,
184:             1,
185:             2,
186:             2,
187:             2
188:           ],
189:           [
190:             1,
191:             1,
192:             2,
193:             1,
194:             2,
195:             3
196:           ],
197:           [
198:             1,
199:             1,
200:             1,
201:             0,
202:             1,
203:             1
204:           ],
205:           [
206:             1,
207:             0,
208:             1,
209:             1,
210:             0,
211:             1
212:           ]
213:         ],
214:         "python": [
215:           0.5882352941176471,
216:           0.31425086615204784,
217:           0,
218:           1,
219:           5,
220:           2
221:         ],
222:         "julia": [
223:           0.5882352941176471,
224:           0.31425086615204784,
225:           0.0,
226:           1.0,
227:           5.0,
228:           2.0
229:         ],
230:         "max_abs_error": 0.0
231:       }
232:     ],
233:     "limitation": "Parity is consistency, not independence; manual variance oracles are independent. Singleton policy intentionally differs from reference."
234:   }
235: }
```

## Selected aggregate rows
[{"estimate": 0.01087822201092484, "weighted_denominator": 7143171.0, "se": 0.0006004799586134849, "ci_low": 0.00970130291832812, "ci_high": 0.012055141103521561, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "national", "territory_code": "CL", "territory_name": "Chile", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 78654, "n_valid": 78654, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.002404976451272248, "weighted_denominator": 129731.0, "se": 0.0009116351034780554, "ci_low": 0.0006182044809935113, "ci_high": 0.004191748421550985, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "1", "territory_name": "Región de Tarapacá", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3093, "n_valid": 3093, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.006728903719364384, "weighted_denominator": 235551.0, "se": 0.0015141788962487943, "ci_low": 0.0037611676158696952, "ci_high": 0.009696639822859072, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "2", "territory_name": "Región de Antofagasta", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3505, "n_valid": 3505, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.0018459199739399533, "weighted_denominator": 110514.0, "se": 0.0008435974745070696, "ci_low": 0.00019249930606914144, "ci_high": 0.003499340641810765, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "3", "territory_name": "Región de Atacama", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3257, "n_valid": 3257, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.005675596877125919, "weighted_denominator": 308690.0, "se": 0.0023442154284028997, "ci_low": 0.0010810190643748899, "ci_high": 0.010270174689876949, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "4", "territory_name": "Región de Coquimbo", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3638, "n_valid": 3638, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.045882158099933755, "weighted_denominator": 736648.0, "se": 0.004366456052431676, "ci_low": 0.0373240614950824, "ci_high": 0.05444025470478511, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "5", "territory_name": "Región de Valparaíso", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 8415, "n_valid": 8415, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.006028670638941807, "weighted_denominator": 370065.0, "se": 0.0014592162820137443, "ci_low": 0.0031686592798692652, "ci_high": 0.008888681998014349, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "6", "territory_name": "Región del Libertador Gral. Bernardo O'Higgins", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 5324, "n_valid": 5324, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.002671231631019933, "weighted_denominator": 439872.0, "se": 0.0010221409144820436, "ci_low": 0.0006678722510401625, "ci_high": 0.004674591010999703, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "7", "territory_name": "Región del Maule", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 5578, "n_valid": 5578, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.006970642520753843, "weighted_denominator": 604105.0, "se": 0.00109352391178467, "ci_low": 0.0048273750369195725, "ci_high": 0.009113910004588114, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "8", "territory_name": "Región del Biobío", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 8124, "n_valid": 8124, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.010735675757528288, "weighted_denominator": 383022.0, "se": 0.001549664976968499, "ci_low": 0.007698388213854176, "ci_high": 0.0137729633012024, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "9", "territory_name": "Región de La Araucanía", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 5458, "n_valid": 5458, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.006824321540607509, "weighted_denominator": 339814.0, "se": 0.0012907780644712146, "ci_low": 0.00429444302161592, "ci_high": 0.009354200059599097, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "10", "territory_name": "Región de Los Lagos", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 4280, "n_valid": 4280, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.001584929583842775, "weighted_denominator": 44166.0, "se": 0.0009221196086734182, "ci_low": 0, "ci_high": 0.0033922508067049683, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "11", "territory_name": "Región de Aysén del Gral. Carlos Ibáñez del Campo", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 1753, "n_valid": 1753, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.0016036913034915455, "weighted_denominator": 71086.0, "se": 0.0008411077576807385, "ci_low": 0, "ci_high": 0.0032522322160499, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "12", "territory_name": "Región de Magallanes y de la Antártica Chilena", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 2354, "n_valid": 2354, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.00784518152629943, "weighted_denominator": 2940786.0, "se": 0.0007928231606586692, "ci_low": 0.00629127668493457, "ci_high": 0.00939908636766429, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "13", "territory_name": "Región Metropolitana de Santiago", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 14151, "n_valid": 14151, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.007866902300063304, "weighted_denominator": 151648.0, "se": 0.0015809497713765307, "ci_low": 0.004768297686071321, "ci_high": 0.010965506914055288, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "14", "territory_name": "Región de Los Ríos", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3433, "n_valid": 3433, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.00376259537538587, "weighted_denominator": 85845.0, "se": 0.0011509883172494335, "ci_low": 0.0015066997264212264, "ci_high": 0.006018491024350514, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "15", "territory_name": "Región de Arica y Parinacota", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 2795, "n_valid": 2795, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": 0.006439559980796126, "weighted_denominator": 191628.0, "se": 0.001376371651684508, "ci_low": 0.003741921113519526, "ci_high": 0.009137198848072726, "n_psu": 12512, "n_strata": 756, "design_df": 11756, "ci_status": "approximate_normal_95_taylor", "scope": "region", "territory_code": "16", "territory_name": "Región de Ñuble", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expr", "n_households": 3496, "n_valid": 3496, "n_missing": 0, "n_flagged": 0, "selection_note": "National and all 16 regions, no outcome selection."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "2202", "territory_name": "Ollagüe", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "5104", "territory_name": "Juan Fernández", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "5201", "territory_name": "Isla de Pascua", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "10103", "territory_name": "Cochamó", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "10401", "territory_name": "Chaitén", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "10402", "territory_name": "Futaleufú", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "10403", "territory_name": "Hualaihué", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "10404", "territory_name": "Palena", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "11203", "territory_name": "Guaitecas", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "11302", "territory_name": "O'Higgins", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}, {"estimate": null, "weighted_denominator": 0.0, "se": null, "ci_low": null, "ci_high": null, "n_psu": 0, "n_strata": 0, "design_df": 0, "ci_status": "no_sample", "scope": "commune", "territory_code": "12202", "territory_name": "Antártica", "unit": "household", "denominator_definition": "All households with exactly one head (pco1=1), valid v9 (1..11), positive weight; no ownership or v28 restriction.", "weight": "expc", "n_households": 0, "n_valid": 0, "n_missing": 0, "n_flagged": 0, "selection_note": "Census commune without sampled CASEN households; no sample is not a zero rate."}]