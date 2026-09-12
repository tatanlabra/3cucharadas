#!/usr/bin/env python3
"""Render reviewed, aggregate CASEN household estimates; no survey recomputation.

python scripts/catastro_sii/render_casen_shared_site.py --expected-sha256 <JSON digest>

The SVG and PNG use a 1152px intrinsic width. Embed with explicit zoom/scroll
and an equivalent HTML table, not by shrinking regional labels to a phone.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from editorial_style import editorial_style, embed_svg_fonts
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.transforms import blended_transform_factory

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT.parent/'catastros_sii/v5_brecha'
SOURCE = ANALYSIS/'artifacts/casen_shared_site/estimates.json'
PLAN = ROOT/'docs/plans/20260912-heroes-casen'
FREEZE = PLAN/'evidence/claude-science/round2/source-freeze.json'
REVIEW = PLAN/'evidence/receipts/D2.json'
IMAGES = ROOT/'assets/images/avaluos-ii'
# Same geographic ordering as the site's chart-theme.ts, never sorted by outcome.
REGION_ORDER = ('15','1','2','3','4','5','13','6','7','16','8','9','14','10','11','12')
REGION_LABELS = ('Arica y Parinacota','Tarapacá','Antofagasta','Atacama','Coquimbo',
                 'Valparaíso','Metropolitana de Santiago',"O’Higgins",'Maule','Ñuble',
                 'Biobío','La Araucanía','Los Ríos','Los Lagos','Aysén','Magallanes')
ROW_FIELDS = set('estimate weighted_denominator se ci_low ci_high n_psu n_strata design_df ci_status scope territory_code territory_name unit denominator_definition weight n_households n_valid n_missing n_flagged selection_note'.split())
CI_OK = 'approximate_normal_95_taylor'
CI_NONE = {'not_estimable_empty_domain','not_estimable_singleton',
           'not_conclusive_boundary_or_degenerate','descriptive_nonrepresentative_no_ci','no_sample'}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_source(source):
    require(source.get('schema_version') == 1 and bool(source.get('rows')), 'Missing/empty CASEN aggregate')
    seen = set()
    for row in source['rows']:
        require(set(row)==ROW_FIELDS, 'Unexpected aggregate fields; raw identifiers cannot be exported')
        key = (row['scope'],row['territory_code'])
        require(key not in seen, f'Duplicate territory: {key}')
        seen.add(key)
        require(row['scope'] in ('national','region','commune'), f'Unknown scope: {key}')
        require(row.get('unit') == 'household', f'Wrong unit: {key}')
        require(row.get('weight') == ('expc' if row['scope']=='commune' else 'expr'), f'Wrong weight: {key}')
        require(bool(row.get('denominator_definition')), f'Missing denominator: {key}')
        for field in ('n_households','n_valid','n_missing','n_flagged'):
            require(type(row.get(field)) is int and row[field] >= 0, f'Invalid count {field}: {key}')
        require(row['n_valid']+row['n_missing']==row['n_households'] and row['n_flagged']<=row['n_households'], f'Count identity: {key}')
        p, lo, hi, se = (row.get(k) for k in ('estimate','ci_low','ci_high','se'))
        denominator = row.get('weighted_denominator')
        require(finite(denominator) and denominator >= 0, f'Invalid weighted denominator: {key}')
        require((p is None and denominator==0 and row['n_valid']==0) or
                (finite(p) and 0 <= p <= 1 and denominator>0 and row['n_valid']>0), f'Invalid estimate/denominator: {key}')
        status = row.get('ci_status')
        require(status == CI_OK or status in CI_NONE, f'Unknown interval status: {key}')
        if status == CI_OK:
            require(row['scope'] != 'commune', f'Nonrepresentative commune cannot have CI: {key}')
            require(all(finite(v) for v in (p,lo,hi,se)) and se>0 and 0<p<1 and 0<=lo<=p<=hi<=1,
                    f'Invalid confidence interval: {key}')
        else:
            require(lo is None and hi is None and se is None, f'Unavailable CI must remain null: {key}')
        if row['scope'] == 'commune':
            require(status in ('descriptive_nonrepresentative_no_ci','no_sample'), f'Invalid communal status: {key}')
        else:
            require(status not in ('descriptive_nonrepresentative_no_ci','no_sample'), f'Invalid regional status: {key}')
        if status == 'no_sample':
            require(p is None and row['n_households']==0, f'No sample is not observed zero: {key}')
        if status == 'not_estimable_empty_domain':
            require(p is None, f'Empty domain has an estimate: {key}')
    needed = {('national','CL')} | {('region',code) for code in REGION_ORDER} | {('commune',code) for code in ('5101','5109')}
    require(needed <= seen, 'Missing national, regional or selected communal rows')
    require(sum(r['scope']=='national' for r in source['rows'])==1 and sum(r['scope']=='region' for r in source['rows'])==16,
            'Expected one national and all 16 regions')
    return source


def load_source(path=SOURCE, expected_sha256=None):
    if expected_sha256 is not None:
        require(digest(path)==expected_sha256, 'Frozen estimates hash mismatch')
    return validate_source(json.loads(Path(path).read_text()))


def reviewed_binding(path, freeze_path=FREEZE, review_path=REVIEW):
    freeze = json.loads(Path(freeze_path).read_text())
    review = json.loads(Path(review_path).read_text())
    actual = hashlib.sha256(json.dumps(freeze['manifest'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(actual==freeze['source_digest']==review['source_digest'] and review['open_p0_p1'] is False,
            'Review is open or not bound to the source freeze')
    require(freeze['manifest']['artifacts/casen_shared_site/estimates.json']==digest(path), 'Estimates differ from reviewed freeze')
    return actual


def plotted_rows(source):
    validate_source(source)
    by_key = {(r['scope'],r['territory_code']):r for r in source['rows']}
    keys = [('national','CL')]+[('region',code) for code in REGION_ORDER]+[('commune',code) for code in ('5101','5109')]
    return [by_key[key] for key in keys]


def percent(value, lang):
    if value is None:
        return 'Sin dato' if lang=='es' else 'No data'
    text = f'{value*100:.2f}'
    return (text.replace('.',',') if lang=='es' else text)+'%'


def integer(value, lang):
    text = format(value,',')
    return text.replace(',','.') if lang=='es' else text


def ci_label(row, lang):
    if row['ci_status']==CI_OK:
        return percent(row['ci_low'],lang).removesuffix('%')+'–'+percent(row['ci_high'],lang)
    labels = {
        'no_sample': ('Sin muestra','No sample'),
        'not_estimable_empty_domain': ('Sin dato válido','No valid data'),
        'not_estimable_singleton': ('No estimable','Not estimable'),
        'not_conclusive_boundary_or_degenerate': ('No concluyente','Not conclusive'),
        'descriptive_nonrepresentative_no_ci': ('Sin IC comunal','No communal CI'),
    }
    return labels[row['ci_status']][0 if lang=='es' else 1]


def draw_panel(fig, rect, rows, labels, lang, colors, communal=False):
    ax = fig.add_axes(rect)
    locations = [0]+[i+1 for i in range(1,len(rows))] if not communal else list(range(len(rows)))
    values = [r['ci_high'] if r['ci_high'] is not None else r['estimate'] for r in rows]
    maximum = max((v for v in values if v is not None), default=.01)*100
    ax.set_xlim(-.02*max(maximum,1), max(maximum*1.10,1))
    ax.set_ylim(max(locations)+.65,-.85)
    ax.set_yticks(locations, labels, fontsize=10.5)
    ax.tick_params(axis='y',length=0,pad=12,colors=colors['ink'])
    ax.tick_params(axis='x',length=0,pad=7,colors=colors['muted'],labelsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value,_:(f'{value:g}'.replace('.',',') if lang=='es' else f'{value:g}')+'%'))
    ax.grid(axis='x',color=colors['line'],linewidth=.7)
    ax.set_axisbelow(True); ax.spines[:].set_visible(False)
    transform = blended_transform_factory(fig.transFigure,ax.transData)
    for i,row in zip(locations,rows):
        if row['estimate'] is not None:
            value = row['estimate']*100
            color = colors['material'] if communal else colors['residual']
            if row['ci_status']==CI_OK:
                ax.errorbar(value,i,xerr=[[value-row['ci_low']*100],[row['ci_high']*100-value]],
                            fmt='D' if row['scope']=='national' else 'o',markersize=5.2,
                            capsize=3,elinewidth=1.5,color=color,zorder=3)
            else:
                ax.plot(value,i,'D' if communal else 'o',markerfacecolor='none',markeredgecolor=color,
                        markeredgewidth=1.5,markersize=6,zorder=3)
        for x,text,bold in ((.625,percent(row['estimate'],lang),True),(.806,ci_label(row,lang),False),
                            (.904,integer(row['n_valid'],lang),False),(.979,integer(row['n_missing'],lang),False)):
            fig.text(x,i,text,transform=transform,ha='right',va='center',fontsize=9.5,
                     weight='bold' if bold else 'normal',color=colors['ink'] if bold else colors['muted'])
    if not communal:
        ax.axhline(.9,color=colors['line'],linewidth=.8)
    ax.set_xlabel('Porcentaje de hogares · escala del panel' if lang=='es' else 'Percentage of households · panel scale',
                  fontsize=9,labelpad=9)
    return ax


def make_figure(rows, lang, colors):
    es = lang=='es'
    fig=plt.figure(figsize=(12,13.4))
    fig.text(.035,.965,'CASEN 2024  /  HOGARES Y SITIO PROPIO COMPARTIDO' if es else 'CASEN 2024  /  HOUSEHOLDS AND SHARED OWN SITES',
             fontsize=10,weight='bold',color=colors['muted'])
    fig.text(.035,.932,'Hogares que declaran compartir sitio propio' if es else 'Households reporting a shared own site',fontsize=22,weight='bold')
    fig.text(.035,.896,'Jefatura declara v9 = 3/4 · denominador: todos los hogares con respuesta válida.' if es else
             'Household head reports v9 = 3/4 · denominator: all households with a valid response.',fontsize=11,color=colors['muted'])
    fig.text(.035,.875,'No es una proporción de viviendas ni una corrección de la brecha fiscal.' if es else
             'Not a dwelling proportion or an adjustment to the fiscal gap.',fontsize=11,color=colors['muted'])
    fig.text(.035,.829,'CHILE Y LAS 16 REGIONES  /  ORDEN NORTE–SUR' if es else 'CHILE AND ALL 16 REGIONS  /  NORTH–SOUTH ORDER',fontsize=10,weight='bold')
    fig.text(.035,.808,'Ponderador expr · punto e IC 95% aproximado por Taylor' if es else
             'expr weights · estimate and approximate Taylor 95% CI',fontsize=10,color=colors['muted'])
    for x,text in ((.625,'Estimación' if es else 'Estimate'),(.806,'IC 95%' if es else '95% CI'),(.904,'n válido' if es else 'Valid n'),(.979,'Sin dato' if es else 'Missing')):
        fig.text(x,.781,text,ha='right',fontsize=9.5,weight='bold',color=colors['muted'])
    draw_panel(fig,(.25,.344,.285,.425),rows[:17],['Chile']+list(REGION_LABELS),lang,colors)
    fig.text(.035,.272,'DOS COMUNAS EXPLORADAS  /  SIN REPRESENTATIVIDAD COMUNAL' if es else
             'TWO EXPLORED COMMUNES  /  NOT REPRESENTATIVE AT COMMUNE LEVEL',fontsize=10,weight='bold')
    fig.text(.035,.251,'Selección posterior a exploración previa · ponderador expc · sin inferencia comunal' if es else
             'Selected after prior exploration · expc weights · no commune-level inference',fontsize=10,color=colors['muted'])
    for x,text in ((.625,'Estimación' if es else 'Estimate'),(.806,'Alcance' if es else 'Scope'),(.904,'n válido' if es else 'Valid n'),(.979,'Sin dato' if es else 'Missing')):
        fig.text(x,.229,text,ha='right',fontsize=9.5,weight='bold',color=colors['muted'])
    draw_panel(fig,(.25,.148,.285,.073),rows[17:],[r['territory_name'] for r in rows[17:]],lang,colors,communal=True)
    caption = ('n válido: hogares muestrales con v9 válida; “sin dato”: hogares con v9 ausente o inválida. IC limitado a [0, 1].\n'
               'Cero observado se conserva; no se transforma un IC no estimable ni una muestra ausente en cero.\n'
               'Fuente: CASEN 2024, Ministerio de Desarrollo Social y Familia. Datos y método en la tabla asociada.' if es else
               'Valid n: sampled households with valid v9; missing: households with absent or invalid v9. CI bounded to [0, 1].\n'
               'Observed zero stays zero; unavailable intervals and missing samples are never converted to zero.\n'
               'Source: CASEN 2024, Ministry of Social Development and Family. Data and method in the accompanying table.')
    fig.text(.035,.055,caption,fontsize=9,linespacing=1.65,color=colors['muted'])
    fig.text(.035,.026,'3cucharadas.cl  /  CASEN 2024 · hogares, no viviendas' if es else '3cucharadas.cl  /  CASEN 2024 · households, not dwellings',fontsize=9,color=colors['muted'])
    return fig,caption


def render(source, output=IMAGES, source_sha256=None, review_digest=None):
    rows=plotted_rows(source)
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    artifacts=[]
    for lang in ('es','en'):
        for theme in ('light','dark'):
            with editorial_style(theme) as colors:
                fig,caption=make_figure(rows,lang,colors)
                for extension in ('svg','png'):
                    path=output/f'casen-shared-site-{lang}{"-dark" if theme=="dark" else ""}.{extension}'
                    meta={'Date':None,'Description':caption} if extension=='svg' else {'Description':caption}
                    fig.savefig(path,dpi=180,metadata=meta)
                    if extension=='svg':
                        svg=embed_svg_fonts(path.read_text())
                        svg=svg.replace('<svg ','<svg role="img" aria-labelledby="casen-title casen-description" ',1)
                        end=svg.index('>',svg.index('<svg '))+1
                        title='Hogares que declaran sitio propio compartido, CASEN 2024' if lang=='es' else 'Households reporting a shared own site, CASEN 2024'
                        svg=svg[:end]+f'<title id="casen-title">{escape(title)}</title><desc id="casen-description">{escape(caption)}</desc>'+svg[end:]
                        path.write_text('\n'.join(line.rstrip() for line in svg.splitlines())+'\n')
                        ET.parse(path)
                    artifacts.append(dict(file=path.name,sha256=digest(path),bytes=path.stat().st_size))
                plt.close(fig)
    data_path=output/'casen-shared-site-data.json'
    data_path.write_text(json.dumps({'schema_version':1,'estimand':source['estimand'],'rows':rows},ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    csv_path=output/'casen-shared-site-data.csv'
    with csv_path.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    for path in (data_path,csv_path): artifacts.append(dict(file=path.name,sha256=digest(path),bytes=path.stat().st_size))
    provenance=dict(schema_version=1,unit='household',source_estimates_sha256=source_sha256,accepted_d1_freeze=review_digest,
                    plotted_rows=19,national_rows=1,regional_rows=16,communal_rows=2,
                    geography_order=list(REGION_ORDER),communal_selection=['5101','5109'],
                    communal_representativeness=False,communal_selection_timing='after prior exploration; not confirmatory',
                    source_url='https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024',
                    minimum_display_width_css_px=1000,intrinsic_css_px=[1152,1286.4],
                    limitations=['Household estimand, not dwelling/site proportion','No fiscal-gap correction','Approximate Taylor CI at national/regional level','Two exploratory communes without confidence intervals'],
                    code_sha256={Path(__file__).name:digest(__file__),'editorial_style.py':digest(Path(__file__).with_name('editorial_style.py'))},artifacts=artifacts)
    path=output/'casen-shared-site-provenance.json';path.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    artifacts.append(dict(file=path.name,sha256=digest(path),bytes=path.stat().st_size))
    return artifacts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--output',type=Path,default=IMAGES)
    parser.add_argument('--expected-sha256',required=True)
    parser.add_argument('--freeze',type=Path,default=FREEZE)
    parser.add_argument('--review-receipt',type=Path,default=REVIEW)
    args=parser.parse_args()
    source=load_source(args.source,args.expected_sha256)
    review_digest=reviewed_binding(args.source,args.freeze,args.review_receipt)
    artifacts=render(source,args.output,args.expected_sha256,review_digest)
    require(digest(args.source)==args.expected_sha256,'Source changed during render')
    print(json.dumps(dict(source_sha256=args.expected_sha256,review_digest=review_digest,artifacts=artifacts),indent=2))


if __name__=='__main__':main()
