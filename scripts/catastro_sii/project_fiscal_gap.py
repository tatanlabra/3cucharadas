#!/usr/bin/env python3
"""Project the canonical Parquet/JSON into the one viewer and ES/EN figures.

No raw records are copied. Existing post I and historical viewer data retain
 their extraction date; new diagnostics have their own provenance.
"""
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/avaluos-ii-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT.parent / 'catastros_sii/v5_brecha/artifacts/fiscal_gap'
DEST = ROOT / 'catastro_sii_brecha/data/fiscal-gap'
IMAGES = ROOT / 'assets/images/avaluos-ii'


def project():
    source = json.loads((SOURCE/'communes.json').read_text())
    sha = hashlib.sha256((SOURCE/'communes.parquet').read_bytes()).hexdigest()
    if sha != source['metadata']['parquet_sha256']:
        raise ValueError('Canonical Parquet hash mismatch')
    records = json.loads(pd.read_parquet(SOURCE/'communes.parquet').to_json(orient='records', force_ascii=False, double_precision=12))
    if records != source['communes'] or source['metadata']['fiscal_status'] != 'blocked_components':
        raise ValueError('Parquet/JSON disagreement or unreviewed fiscal release')
    source_audit = json.loads((SOURCE/'source-audit.json').read_text())
    if source_audit['canonical_json_sha256'] != hashlib.sha256((SOURCE/'communes.json').read_bytes()).hexdigest():
        raise ValueError('Official source audit must be regenerated for this canonical table')
    DEST.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE.parents[1]/'docs/avaluos-ii-method.md', DEST/'method.md')
    for name in ['communes.json','communes.csv','communes.parquet','dictionary.json','inputs.json','audit.json','runtime.json','source-audit.json']:
        shutil.copyfile(SOURCE/name, DEST/name)
    map_evidence = SOURCE.parents[1]/'docs/avaluos-ii-annex-maps-evidence.json'
    maps = json.loads(map_evidence.read_text())
    if maps['canonical_sha256'] != hashlib.sha256((SOURCE/'communes.json').read_bytes()).hexdigest():
        raise ValueError('Map evidence refers to a different canonical table')
    # Only aggregate provenance and raster hashes; no source geometry/identifiers.
    public_maps = {key: value for key, value in maps.items() if not key.startswith('historical_template')}
    for mapping in public_maps['maps']:
        mapping['previews'] = []
        for output in mapping['outputs']:
            source_image = IMAGES/output['file']
            if hashlib.sha256(source_image.read_bytes()).hexdigest() != output['sha256']:
                raise ValueError('Map PNG differs from the renderer evidence')
            with Image.open(source_image) as source_png:
                for width in [900, 1800]:
                    preview = IMAGES/f'{source_image.stem}-{width}.webp'
                    source_png.convert('RGB').resize((width, width*3//4), Image.Resampling.LANCZOS).save(preview, quality=88, method=6)
                    mapping['previews'].append(dict(file=preview.name, width=width, height=width*3//4,
                        bytes=preview.stat().st_size, sha256=hashlib.sha256(preview.read_bytes()).hexdigest()))
    (DEST/'maps-audit.json').write_text(json.dumps(public_maps, ensure_ascii=False, indent=2)+'\n')
    top = sorted([r for r in records if r['source_available'] and r['camp_sensitivity_positive_gap'] > 0],
                 key=lambda r: (-r['camp_sensitivity_positive_gap'],r['codigo_comuna'].zfill(5)))[:15]
    for lang in ['es','en']:
        headers = (['Comuna','CUT','Brecha inicial','Campamentos: descuento','Brecha restante','Aceptables: escenario ≈','Avalúo mediano habitacional (CLP)','Conteo CNC'] if lang=='es' else
                   ['Commune','CUT','Initial gap','Settlement deduction','Remaining gap','Acceptable: scenario ≈','Median residential assessment (CLP)','Settlement count'])
        table_lines = ['<div class="avaluos-ii-table" role="region" tabindex="0" aria-label="'+('Diagnóstico residencial' if lang=='es' else 'Residential diagnostic')+'" style="overflow-x:auto">', '<table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>']
        for r in top:
            quality = ('Sin polígono CNC' if lang=='es' else 'No CNC polygon') if not r['camp_polygons_2026'] else (
                ('Parcial' if r['camp_census_count_missing_polygons'] else 'Completo') if lang=='es' else
                ('Partial' if r['camp_census_count_missing_polygons'] else 'Complete'))
            values=[r['codigo_comuna'].zfill(5),*[(format(round(r[k]),',').replace(',','.') if lang=='es' else format(round(r[k]),',')) if r[k] is not None else '—' for k in ['signed_gap','camp_absorbed_positive_gap','camp_sensitivity_positive_gap','materiality_acceptable_scenario','assessment_median_clp']],quality]
            table_lines.append('<tr><th scope="row">'+html.escape(r['comuna'])+'</th>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>')
        table_lines.append('</tbody></table></div>')
        (ROOT/'_includes'/f'avaluos-ii-top-{lang}.html').write_text('\n'.join(table_lines)+'\n')
        for dark in [False, True]:
            surface, ink, muted, line = ('#10121d','#f3f5f8','#a9afbd','#2a3041') if dark else ('#ffffff','#132033','#445570','#d6dfea')
            colors = ['#55c4c0','#98a8bd','#f0b35b'] if dark else ['#56bdb9','#99abc2','#efb35f']
            boundary = '#61758f' if dark else '#40566e'
            fig, ax = plt.subplots(figsize=(11,8.5))
            fig.patch.set_facecolor(surface); ax.set_facecolor(surface)
            labels = [r['comuna'] for r in top]
            original = [r['signed_gap'] for r in top]
            residual = [r['camp_sensitivity_positive_gap'] for r in top]
            acceptable = [r['materiality_acceptable_scenario'] for r in top]
            other = [r['materiality_other_scenario'] for r in top]
            absorbed = [r['camp_absorbed_positive_gap'] for r in top]
            ax.barh(labels, acceptable, height=.54, color=colors[0], edgecolor=boundary, linewidth=.65, label='Tipo y materiales aceptables (escenario)' if lang=='es' else 'Acceptable type and materials (scenario)')
            ax.barh(labels, other, left=acceptable, height=.54, color=colors[1], edgecolor=boundary, linewidth=.65, label='Resto del escenario' if lang=='es' else 'Rest of scenario')
            ax.barh(labels, absorbed, left=residual, height=.54, color=colors[2], edgecolor=boundary, linewidth=.65, label='Campamentos (descuento supuesto)' if lang=='es' else 'Settlements (assumed deduction)')
            ax.invert_yaxis(); ax.set_xlim(0,max(original)*1.38)
            for i, v in enumerate(residual):
                value = format(int(v),',').replace(',','.') if lang=='es' else format(int(v),',')
                ax.text(original[i]+max(original)*.016,i,value+(' restan' if lang=='es' else ' remain'),va='center',fontsize=9,color=ink,weight='bold')
            ax.spines[['top','right','left']].set_visible(False); ax.spines['bottom'].set_color(line)
            ax.tick_params(axis='y',length=0,labelcolor=ink); ax.tick_params(axis='x',colors=muted)
            ax.grid(axis='x',color=line,alpha=.72); ax.set_axisbelow(True)
            handles, legend_labels = ax.get_legend_handles_labels()
            fig.legend(handles,legend_labels,loc='upper left',bbox_to_anchor=(.03,.93),frameon=False,ncol=1,fontsize=9,labelcolor=ink)
            title = 'Avalúos II · ¿Cuánto queda por explicar?' if lang=='es' else 'Property assessments II · What remains unexplained?'
            fig.text(.04,.95,title,fontsize=17,weight='bold',color=ink)
            ax.set_xlabel('La barra completa es la brecha inicial · orden por brecha restante' if lang=='es' else 'Full bar = initial gap · sorted by remaining gap',color=muted,fontsize=10)
            caption = ('Censo 2024 − roles habitacionales 2026S1. Descontamos hogares observados en campamentos bajo supuesto uno a uno.\nRepartimos lo restante con la proporción comunal de tipo y materiales aceptables observada en el Censo.\nLas partes son escenarios: no identifican viviendas sin rol ni contribuciones impagas. 222 polígonos CNC sin conteo.\nDatos y método: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones' if lang=='es' else
                       '2024 Census − 2026H1 residential records. Observed settlement households are deducted under a one-to-one assumption.\nThe remainder uses the observed commune share of dwellings with acceptable type and materials.\nSegments are scenarios: they identify neither unregistered homes nor unpaid tax. 222 CNC polygons lack counts.\nData and method: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones')
            fig.text(.04,.025,caption,fontsize=9,linespacing=1.5,color=muted)
            fig.subplots_adjust(left=.22,right=.97,top=.79,bottom=.20)
            suffix = '-dark' if dark else ''
            with matplotlib.rc_context({'svg.fonttype':'none','svg.hashsalt':'avaluos-ii'}):
                fig.savefig(IMAGES/f'gap-top15-{lang}{suffix}.svg',metadata={'Date':None})
            svg_path = IMAGES/f'gap-top15-{lang}{suffix}.svg'
            svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
            fig.savefig(IMAGES/f'gap-top15-{lang}{suffix}.png',dpi=180,metadata={'Description':caption})
            plt.close(fig)
    def number(x): return 'Sin fuente' if x is None else format(round(x),',').replace(',','.')
    def percentage(x): return 'Sin dato' if x is None else f'{100*x:.1f}%'.replace('.',',')
    def quality(r):
        if r['camp_adjustment_status']=='missing_role_source': return 'Sin fuente de roles'
        if r['camp_adjustment_status']=='partial_census_count': return f'Parcial: {number(r["camp_census_count_missing_polygons"])} sin dato'
        if r['camp_adjustment_status']=='complete_census_count': return 'Conteo completo'
        return 'Sin polígono CNC vigente'
    table_rows = []
    for r in records:
        values = [r['codigo_comuna'], *[number(r[k]) for k in ['dwellings_2024','residential_roles_2026s1','signed_gap','camp_census_households_observed_2024','camp_sensitivity_positive_gap','materiality_acceptable_scenario']], percentage(r['materiality_acceptable_share_observed']), *[number(r[k]) for k in ['assessment_median_clp','assessment_mean_clp']], percentage(r['assessment_above_exemption_share']), quality(r)]
        label = html.escape(r['comuna'])
        table_rows.append(f'<tr><th scope="row">{label} <button type="button" data-gap-commune="{r["codigo_comuna"]}" hidden>Seleccionar {label}</button></th>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in values)+'</tr>')
    section = (Path(__file__).parent/'templates/fiscal_gap_section.html').read_text()
    initial = sum(max(r['signed_gap'],0) for r in records if r['source_available'])
    absorbed = sum(r['camp_absorbed_positive_gap'] for r in records if r['source_available'])
    labels = {
        '__COMMUNE_TABLE__': ''.join(table_rows),
        '__GAP_TOTAL__': number(initial),
        '__CAMP_ABSORBED__': number(absorbed),
        '__RESIDUAL_TOTAL__': number(initial-absorbed),
        '__CAMP_PCT__': f'{100*absorbed/initial:.2f}'.replace('.',','),
        '__ACCEPTABLE_TOTAL__': number(source['metadata']['materiality_acceptable_dwellings_2024']),
        '__OCCUPIED_TOTAL__': number(source['metadata']['occupied_private_dwellings_2024']),
        '__EXEMPTION__': number(source['metadata']['assessment_exemption_clp']),
    }
    for label,value in labels.items(): section = section.replace(label,value)
    section = section.replace('__OBS_H__', number(source['metadata']['observed_residential_roles'])).replace('__OFF_H__', number(source['metadata']['official_residential_roles']))
    official_by_cut = {r['codigo_comuna']: r for r in source_audit['comparisons']}
    audit_labels = {
        '__TREHUACO_H__': official_by_cut['16207']['minvu_h'],
        '__ANTARTICA_H__': official_by_cut['12202']['minvu_h'],
        '__MINVU_H__': source_audit['minvu_residential_roles'],
        '__MINVU_SII_DIFFERENCE__': source_audit['minvu_minus_sii'],
        '__MATCHED_DIFFERENCE__': source_audit['matched_commune_total_difference'],
        '__DIFFERENT_COMMUNES__': source_audit['matched_commune_count_differences'],
    }
    for label, value in audit_labels.items():
        section = section.replace(label, number(value))
    page = ROOT/'catastro_sii_brecha/index.html'
    content = page.read_text()
    if '<!-- fiscal-gap:start;' in content:
        start = content.index('<!-- fiscal-gap:start;'); end = content.index('<!-- fiscal-gap:end -->') + len('<!-- fiscal-gap:end -->')
        content = content[:start] + section + content[end:]
    else:
        content = content.replace('    <section class="card territory-detail-card', section+'\n\n    <section class="card territory-detail-card',1)
        content = content.replace('<a href="#territory-detail">Tu comuna</a>', '<a href="#brecha-contribuciones">Brecha y contribuciones</a>\n      <a href="#territory-detail">Tu comuna</a>',1)
    css_hash = hashlib.sha256((ROOT/'catastro_sii_brecha/style.css').read_bytes()).hexdigest()
    content = re.sub(r'style\.css\?v=[a-f0-9]+', 'style.css?v='+css_hash, content)
    loader_hash = hashlib.sha256((ROOT/'catastro_sii_brecha/assets/map-app-loader.js').read_bytes()).hexdigest()
    content = re.sub(r'assets/map-app-loader\.js(?:\?v=[a-f0-9]+)?', 'assets/map-app-loader.js?v='+loader_hash, content)
    for asset in ['app.js', 'assets/site-ui.js']:
        asset_hash = hashlib.sha256((ROOT/'catastro_sii_brecha'/asset).read_bytes()).hexdigest()
        content = re.sub(r'src="'+re.escape(asset)+r'(?:\?v=[a-f0-9]+)?"', 'src="'+asset+'?v='+asset_hash+'"', content)
    page.write_text(content)
    print('Projected',len(records),'communes; residual top 15:',[(r['comuna'],r['camp_sensitivity_positive_gap']) for r in top])

if __name__=='__main__': project()
