#!/usr/bin/env python3
"""Cross-artifact publication checks; rejects missing fiscal data masquerading as zero."""
import argparse
import hashlib
import json
import math
import struct
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]


def verify(data: Path):
    document=json.loads((data/'communes.json').read_text());meta=document['metadata'];rows=document['communes']
    if len(rows)!=346 or len({r['codigo_comuna'] for r in rows})!=346:
        raise ValueError('Missing or duplicate CUT')
    sha=hashlib.sha256((data/'communes.parquet').read_bytes()).hexdigest()
    if sha != meta['parquet_sha256']: raise ValueError('Parquet hash mismatch')
    frame=pd.read_parquet(data/'communes.parquet')
    if json.loads(frame.to_json(orient='records',force_ascii=False,double_precision=12))!=rows:
        raise ValueError('Parquet/JSON disagreement')
    csv=pd.read_csv(data/'communes.csv',dtype={'codigo_comuna':str,'conara_sources':str})
    for key in ['dwellings_2024','residential_roles_2026s1','signed_gap',
                'camp_census_households_observed_2024','camp_sensitivity_positive_gap',
                'irrecoverable_dwellings_2024','materiality_acceptable_scenario','materiality_other_scenario',
                'assessment_median_clp','assessment_mean_clp','assessment_above_exemption_share','scenario_q1_clp']:
        pd.testing.assert_series_equal(frame[key].astype(float),csv[key].astype(float),check_names=False)
    if meta['fiscal_status']!='blocked_components' or meta['monetary_ranking']:
        raise ValueError('No reviewed monetary adapter exists for this release')
    source_audit=json.loads((data/'source-audit.json').read_text())
    if source_audit['canonical_json_sha256'] != hashlib.sha256((data/'communes.json').read_bytes()).hexdigest():
        raise ValueError('Official source audit is stale for this canonical table')
    if source_audit['fiscal_status']!='blocked_components' or len(source_audit['comparisons'])!=346:
        raise ValueError('Official control cannot certify net H tax or omit communes')
    for r in rows:
        if r['source_available']:
            if r['signed_gap']!=r['dwellings_2024']-r['residential_roles_2026s1']:
                raise ValueError('Arithmetic disagreement')
            if r['camp_sensitivity_signed_gap'] != r['signed_gap']-r['camp_census_households_observed_2024']:
                raise ValueError('Camp sensitivity arithmetic disagreement')
            if r['camp_sensitivity_positive_gap'] != max(r['camp_sensitivity_signed_gap'],0):
                raise ValueError('Camp sensitivity truncation disagreement')
            acceptable,other = r['materiality_acceptable_scenario'],r['materiality_other_scenario']
            if r['occupied_private_dwellings_2024'] > 0:
                if not math.isclose(acceptable+other,r['camp_sensitivity_positive_gap'],abs_tol=1e-6):
                    raise ValueError('Materiality partition does not conserve the residual')
                expected = r['camp_sensitivity_positive_gap'] * r['materiality_acceptable_dwellings_2024'] / r['occupied_private_dwellings_2024']
                if acceptable < 0 or other < 0 or not math.isclose(acceptable,expected,abs_tol=1e-6):
                    raise ValueError('Materiality transfer differs from the stated scenario')
            elif acceptable is not None or other is not None:
                raise ValueError('No observed composition converted to a numeric scenario')
            if r['assessment_valid_roles_2026s1'] + r['assessment_missing_roles_2026s1'] != r['residential_roles_2026s1']:
                raise ValueError('Assessment coverage differs from administrative H roles')
        elif r['signed_gap'] is not None or r['residential_roles_2026s1'] is not None:
            raise ValueError('Missing source converted to a numeric result')
        if any(r[k] is not None for k in r if k.startswith(('net_','scenario_'))):
            raise ValueError('Unresolved monetary field must remain null')
    if (meta['camp_polygons_2026'],meta['camp_census_households_observed_2024'],
        meta['camp_census_count_missing_polygons'],meta['irrecoverable_dwellings_2024']) != (1345,71760,222,72642):
        raise ValueError('Camp/Census totals drift')
    if (meta['materiality_acceptable_dwellings_2024'],meta['materiality_missing_dwellings_2024'],meta['assessment_exemption_clp']) != (5774146,4388,60030710):
        raise ValueError('Materiality/assessment source definition drift')
    top=sorted([r for r in rows if r['source_available'] and r['camp_sensitivity_positive_gap']>0],key=lambda r:(-r['camp_sensitivity_positive_gap'],r['codigo_comuna'].zfill(5)))[:15]
    maps=json.loads((data/'maps-audit.json').read_text())
    if maps['canonical_sha256'] != hashlib.sha256((data/'communes.json').read_bytes()).hexdigest():
        raise ValueError('Maps do not use the current canonical analysis')
    if [m['codigo_comuna'] for m in maps['maps']] != [r['codigo_comuna'].zfill(5) for r in top[:2]]:
        raise ValueError('Maps are not the two largest remaining gaps')
    for mapping,row in zip(maps['maps'],top):
        if (mapping['residential_roles'] != row['residential_roles_2026s1']
            or mapping['roles_with_supplied_geometry']+mapping['roles_without_geometry'] != mapping['residential_roles']
            or mapping['commune_cnc_polygons'] != row['camp_polygons_2026']
            or mapping['residual_commune'] != row['camp_sensitivity_positive_gap']
            or not mapping['raster_only'] or mapping['invented_geometry']
            or mapping['individual_identifiers_exported'] or mapping['spatial_matching_to_census']):
            raise ValueError('Map universe or interpretation differs from the analysis')
        if len(mapping['outputs']) != 2:
            raise ValueError('Each map requires light and dark variants')
        for output in mapping['outputs']:
            name=output['file']
            if Path(name).name != name or not name.endswith('.png'):
                raise ValueError('Map must be a raster in the image directory')
            content=(ROOT/'assets/images/avaluos-ii'/name).read_bytes()
            if hashlib.sha256(content).hexdigest() != output['sha256']:
                raise ValueError('Map raster hash differs from its source evidence')
            if content[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',content[16:24]) != (1800,1350):
                raise ValueError('Map raster dimensions or format differ')
        if len(mapping.get('previews', [])) != 4:
            raise ValueError('Maps lack responsive light/dark previews')
        for preview in mapping['previews']:
            name=preview['file']
            if Path(name).name != name or not name.endswith('.webp'):
                raise ValueError('Map preview must stay in the image directory')
            content=(ROOT/'assets/images/avaluos-ii'/name).read_bytes()
            if hashlib.sha256(content).hexdigest() != preview['sha256']:
                raise ValueError('Responsive map preview differs from its evidence')
    for lang in ['es','en']:
        markup=(ROOT/'_includes'/f'avaluos-ii-top-{lang}.html').read_text()
        svg=(ROOT/'assets/images/avaluos-ii'/f'gap-top15-{lang}.svg').read_text()
        dark_svg=(ROOT/'assets/images/avaluos-ii'/f'gap-top15-{lang}-dark.svg').read_text()
        previous=-1
        for r in top:
            index=markup.index(r['comuna'])
            if index<=previous: raise ValueError('Translated table rank differs')
            previous=index
            value_label=format(int(r['camp_sensitivity_positive_gap']),',').replace(',','.') if lang=='es' else format(int(r['camp_sensitivity_positive_gap']),',')
            if any(r['comuna'] not in chart or value_label not in chart for chart in [svg,dark_svg]):
                raise ValueError('Figure missing canonical label/value')
    page=(ROOT/'catastro_sii_brecha/index.html').read_text()
    if page.count('id="brecha-contribuciones"')!=1 or page.count('data-gap-commune=')!=346:
        raise ValueError('Viewer missing unique section or complete fallback table')
    if '__COMMUNE_TABLE__' in page or page.count('class="gap-key"') != 1:
        raise ValueError('Unresolved template or missing semantic legend')
    for asset in ['style.css','app.js','assets/site-ui.js']:
        digest=hashlib.sha256((ROOT/'catastro_sii_brecha'/asset).read_bytes()).hexdigest()
        if asset+'?v='+digest not in page:
            raise ValueError('Viewer references stale asset: '+asset)
    dictionary=json.loads((data/'dictionary.json').read_text())
    if set(dictionary['columns'])!=set(frame.columns): raise ValueError('Dictionary drift')
    print('PASS: 346 rows; camp sensitivity/materiality; Parquet/JSON/CSV; blocked fiscal fields; ES/EN figures and tables; one viewer')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=ROOT/'catastro_sii_brecha/data/fiscal-gap')
    verify(p.parse_args().data)
