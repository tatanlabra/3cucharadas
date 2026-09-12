#!/usr/bin/env python3
"""Publish only reviewed CASEN aggregates and a bilingual equivalent HTML table."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def number(value, lang, digits=0):
    if value is None:
        return 'Sin dato' if lang == 'es' else 'No data'
    value = f'{value:,.{digits}f}'
    return value.translate(str.maketrans(',.', '.,')) if lang == 'es' else value

def percent(value, lang):
    return number(value * 100, lang, 2) + (' %' if lang == 'es' else '%') if value is not None else number(None, lang)

def table(rows, lang, exploratory=False):
    es = lang == 'es'
    caption = ('Casos comunales exploratorios; expc; sin representatividad ni IC comunales.' if es else
               'Exploratory commune cases; expc; no commune representativeness or confidence intervals.') if exploratory else (
               'Hogares que declaran sitio propio compartido; expr; IC normal aproximado del 95 %.' if es else
               'Households reporting an owned shared site; expr; approximate normal 95% confidence intervals.')
    headings = ['Territorio', 'Hogares muestrales', 'Sin respuesta', 'Proporción', 'IC 95 %'] if es else ['Territory', 'Sample households', 'Missing answers', 'Share', '95% CI']
    out = ['<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="'+html.escape(caption)+'">',
           '<table><caption>'+html.escape(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headings)+'</tr></thead><tbody>']
    for row in rows:
        interval = (percent(row['ci_low'],lang)+'–'+percent(row['ci_high'],lang)) if row['ci_low'] is not None else (
            ('No corresponde' if es else 'Not applicable') if exploratory else ('No estimable' if es else 'Not estimable'))
        name = ('Chile' if row['scope']=='national' else row['territory_name'])
        cells = [number(row['n_households'],lang), number(row['n_missing'],lang), percent(row['estimate'],lang),interval]
        out.append('<tr data-territory="'+html.escape(row['territory_code'])+'"><th scope="row">'+html.escape(name)+'</th>'+''.join('<td>'+html.escape(c)+'</td>' for c in cells)+'</tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path,required=True)
    parser.add_argument('--expected-sha256',required=True)
    args=parser.parse_args()
    source=args.source_dir/'estimates.json'
    if sha(source)!=args.expected_sha256:
        raise ValueError('Reviewed aggregate digest mismatch; no projection written')
    data=json.loads(source.read_text());rows=data['rows']
    national=[r for r in rows if r['scope']=='national']
    regional=[r for r in rows if r['scope']=='region']
    cases=[next(r for r in rows if r['scope']=='commune' and r['territory_code']==c) for c in ['5101','5109']]
    if len(national)!=1 or len(regional)!=16 or any(r['unit']!='household' for r in rows):
        raise ValueError('Unexpected territorial coverage or unit')
    if any(r['ci_low'] is not None or r['ci_high'] is not None for r in rows if r['scope']=='commune'):
        raise ValueError('A commune interval would contradict the approved estimand')
    output=ROOT/'catastro_sii_brecha/data/casen-shared-site';output.mkdir(parents=True,exist_ok=True)
    for name in ['estimates.json','estimates.csv','estimates.parquet','audit.json','provenance.json']:
        shutil.copyfile(args.source_dir/name,output/name)
    method=args.source_dir.parents[1]/'docs/casen-shared-site-method.md'
    (output/'method.md').write_text(method.read_text().replace('/opt/entornos/mamba312/bin/python','python3'))
    pieces=[]
    for lang in ['es','en']:
        pieces.append("{% if include.lang == '"+lang+"' %}")
        summary='Tabla nacional y regional: proporción, muestra e incertidumbre' if lang=='es' else 'National and regional table: share, sample and uncertainty'
        pieces += ['<details><summary>'+summary+'</summary>',table(national+regional,lang),'</details>',table(cases,lang,True)]
        pieces.append('<p><a href="/catastro_sii_brecha/data/casen-shared-site/estimates.csv">'+('Descargar las 346 comunas (CSV); 11 sin muestra conservadas como dato ausente.' if lang=='es' else 'Download all 346 communes (CSV); 11 outside the sample remain missing data.')+'</a></p>')
        pieces.append('{% endif %}')
    include=ROOT/'_includes/casen-shared-site-table.html';include.write_text('\n'.join(pieces)+'\n')
    receipt={'source_estimates_sha256':args.expected_sha256,'unit':'household','rows':len(rows),
             'national_regional_table_rows':17,'exploratory_cases':['5101','5109'],
             'projection_script_sha256':sha(Path(__file__)), 'outputs_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file() and p.name!='projection.json'},
             'table_sha256':sha(include),'raw_records_exported':False}
    (output/'projection.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':
    main()
