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
    top = sorted([r for r in records if r['source_available'] and r['signed_gap'] > 0],
                 key=lambda r: (-r['signed_gap'],r['codigo_comuna'].zfill(5)))[:15]
    for lang in ['es','en']:
        headers = ['Comuna','CUT','Viviendas 2024','Roles H 2026S1','Diferencia'] if lang=='es' else ['Commune','CUT','Dwellings 2024','H roles 2026H1','Difference']
        table_lines = ['<div class="avaluos-ii-table" role="region" tabindex="0" aria-label="'+('Diagnóstico residencial' if lang=='es' else 'Residential diagnostic')+'" style="overflow-x:auto">', '<table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>']
        for r in top:
            values=[r['codigo_comuna'].zfill(5),*[(format(int(r[k]),',').replace(',','.') if lang=='es' else format(int(r[k]),',')) for k in ['dwellings_2024','residential_roles_2026s1','signed_gap']]]
            table_lines.append('<tr><th scope="row">'+html.escape(r['comuna'])+'</th>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>')
        table_lines.append('</tbody></table></div>')
        (ROOT/'_includes'/f'avaluos-ii-top-{lang}.html').write_text('\n'.join(table_lines)+'\n')
        fig, ax = plt.subplots(figsize=(11,8.5))
        fig.patch.set_facecolor('#fbf8f2'); ax.set_facecolor('#fbf8f2')
        values = [r['signed_gap'] for r in top]
        ax.barh([r['comuna'] for r in top], values, color='#397e78')
        ax.invert_yaxis(); ax.set_xlim(0,max(values)*1.19)
        for i, v in enumerate(values): ax.text(v+max(values)*.015,i,(format(int(v),',').replace(',','.') if lang=='es' else format(int(v),',')),va='center',fontsize=10)
        ax.spines[['top','right','left']].set_visible(False)
        ax.tick_params(axis='y',length=0); ax.grid(axis='x',alpha=.15); ax.set_axisbelow(True)
        title = 'Avalúos II · Las 15 mayores diferencias observadas' if lang=='es' else 'Property assessments II · 15 largest observed differences'
        ax.set_title(title,loc='left',pad=22,fontsize=15,weight='bold')
        ax.set_xlabel('Viviendas particulares Censo 2024 − roles H, SII 2026S1' if lang=='es' else 'Private dwellings, Census 2024 − residential roles, SII 2026H1')
        caption = ('Diagnóstico físico; NO es un ranking de recaudación perdida. Fuentes: INE Censo 2024;\nespejo catastral, extracción 24-07-2026, identidad CONARA corregida. Dos comunas sin extracto del espejo excluidas.\nVivienda ≠ rol. La conversión a CLP está bloqueada: aseo e impuesto no están separados.\nDatos y método: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones' if lang=='es' else
                   'Physical diagnostic; NOT a ranking of lost tax revenue. Sources: INE Census 2024; cadastral\nmirror extracted 24 July 2026, corrected CONARA mapping. Two communes without mirror extracts excluded.\nDwelling ≠ cadastral role. CLP conversion blocked: refuse charges and tax are not separated.\nData and method: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones')
        fig.text(.04,.025,caption,fontsize=9,linespacing=1.55)
        fig.subplots_adjust(left=.23,right=.97,top=.90,bottom=.22)
        with matplotlib.rc_context({'svg.fonttype':'none','svg.hashsalt':'avaluos-ii'}):
            fig.savefig(IMAGES/f'gap-top15-{lang}.svg',metadata={'Date':None})
        svg_path = IMAGES/f'gap-top15-{lang}.svg'
        svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
        fig.savefig(IMAGES/f'gap-top15-{lang}.png',dpi=180,metadata={'Description':caption})
        plt.close(fig)
    def number(x): return 'Sin fuente' if x is None else format(int(x),',').replace(',','.')
    table = ''.join(f'<tr><th scope="row">{html.escape(r["comuna"])} <button type="button" data-gap-commune="{r["codigo_comuna"]}" hidden>Seleccionar {html.escape(r["comuna"])}</button></th><td>{r["codigo_comuna"]}</td><td>{number(r["dwellings_2024"])}</td><td>{number(r["residential_roles_2026s1"])}</td><td>{number(r["signed_gap"])}</td></tr>' for r in records)
    section = '''<!-- fiscal-gap:start; generated by scripts/catastro_sii/project_fiscal_gap.py -->
    <section class="card" id="brecha-contribuciones" aria-labelledby="fiscal-gap-title">
      <span class="section-eyebrow">Avalúos II · diagnóstico actualizado</span>
      <h2 id="fiscal-gap-title">La brecha residencial y su pregunta fiscal</h2>
      <p>¿Cuánto podría representar en contribuciones la diferencia entre viviendas y roles habitacionales? El primer paso es hacer comparable el registro. Este corte usa Censo 2024 y el extracto SII 2026S1 descargado el 24 de julio de 2026: __OBS_H__ roles H frente a __OFF_H__ en el cuadro oficial. Incluye roles sin coordenadas; corrige el cruce CONARA de Aysén, Chile Chico y Coyhaique.</p>
      <p><strong>Ranking monetario pendiente.</strong> El campo semestral disponible puede incluir aseo y sobretasas. Sin separar componentes no se puede calcular la contribución neta media ni una brecha en pesos. Una barra representa viviendas particulares menos roles H, no deuda ni negligencia demostrada.</p>
      <p>Referencia prevista: <code>máx(viviendas − roles H, 0) × q × media anual equivalente</code>, incluyendo ceros. Sensibilidad: q = 0, 0,25, 0,5 y 1; q = 1 es una referencia hipotética, no una probabilidad estimada ni una cota de evasión.</p>
      <p id="fiscal-gap-selection" role="status">Chile: diagnóstico nacional. El selector territorial de arriba controla este gráfico al activarse JavaScript.</p>
      <div id="fiscal-gap-chart" style="height:620px;width:100%" hidden role="img" aria-label="Quince mayores diferencias positivas entre viviendas censadas y roles habitacionales; tabla completa a continuación"></div>
      <figure id="fiscal-gap-static"><img src="/assets/images/avaluos-ii/gap-top15-es.svg" width="1100" height="850" style="max-width:100%;height:auto" alt="Diagnóstico nacional de las 15 mayores diferencias positivas; valores exactos en la tabla siguiente."><figcaption>Comparación de unidades distintas y fechas distintas: Censo 2024 y catastro 2026S1. El ranking físico no sustituye al ranking fiscal.</figcaption></figure>
      <details><summary>Ver las 346 comunas: datos, faltantes y diferencias negativas</summary><div class="lab-table-scroll" tabindex="0" role="region" aria-label="Tabla completa del diagnóstico residencial"><table class="lab-data-table"><caption>Censo 2024 y SII 2026S1 · viviendas y roles; no CLP</caption><thead><tr><th scope="col">Comuna</th><th scope="col">CUT</th><th scope="col">Viviendas</th><th scope="col">Roles H</th><th scope="col">Diferencia</th></tr></thead><tbody>''' + table + '''</tbody></table></div></details>
      <p>Antártica y Trehuaco no tienen fuente en este extracto: se conservan como ausentes, nunca como cero roles. Una diferencia negativa tampoco prueba ausencia de omisiones. Vacancia, viviendas rurales en predios agrícolas, copropiedad, roles matrices y cambios de fecha pueden alterar la comparación.</p>
      <p><strong>Control oficial adicional, revisado el 10-09-2026.</strong> MINVU informa __TREHUACO_H__ roles H en Trehuaco y __ANTARTICA_H__ en Antártica para 2026S1. Sus planillas suman __MINVU_H__ H, __MINVU_SII_DIFFERENCE__ más que el cuadro nacional SII. Frente al espejo hay __MATCHED_DIFFERENCE__ roles adicionales en __DIFFERENT_COMMUNES__ comunas cubiertas, además de Trehuaco. Se conserva este control separado del extracto del gráfico. Los CSV comunales SII de 2026S1 separan impuesto neto y aseo para todos los destinos no agrícolas; no entregan el neto habitacional requerido. <a href="data/fiscal-gap/source-audit.json">Consultar conciliación y fuentes oficiales</a>.</p>
      <p><strong>Cortes separados.</strong> Las otras secciones mantienen la extracción anterior de 2026 y el análisis UV del post I. Este diagnóstico añade un corte más reciente y un contraste 2024S2; no forma una serie homogénea de altas prediales. La errata territorial se documenta junto al método.</p>
      <p>Fuentes: <a href="https://censo2024.ine.gob.cl/resultados/">INE Censo 2024</a> · <a href="https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html">SII 2026S1</a> · <a href="https://www.sii.cl/documentos/resoluciones/2010/2010-5.pdf">SII: composición del dato (Producto 3)</a> · <a href="https://catastral.cl/">espejo catastral</a>.</p>
      <p>Descargar: <a href="data/fiscal-gap/communes.csv">CSV completo</a> · <a href="data/fiscal-gap/communes.parquet">Parquet canónico</a> · <a href="data/fiscal-gap/dictionary.json">Diccionario</a> · <a href="data/fiscal-gap/inputs.json">Huellas de fuentes</a> · <a href="/assets/images/avaluos-ii/gap-top15-es.svg">SVG con advertencias</a> · <a href="/assets/images/avaluos-ii/gap-top15-es.png">PNG</a> · <a href="data/fiscal-gap/method.md">Método y errata</a>.</p>
    </section>
    <!-- fiscal-gap:end -->'''
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
    page.write_text(content)
    print('Projected',len(records),'communes; diagnostic top 15:',[(r['comuna'],r['signed_gap']) for r in top])

if __name__=='__main__': project()
