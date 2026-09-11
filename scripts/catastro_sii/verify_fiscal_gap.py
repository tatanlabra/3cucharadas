#!/usr/bin/env python3
"""Cross-artifact publication checks; rejects missing fiscal data masquerading as zero."""
import argparse
import hashlib
import json
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
                'irrecoverable_dwellings_2024','scenario_q1_clp']:
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
        elif r['signed_gap'] is not None or r['residential_roles_2026s1'] is not None:
            raise ValueError('Missing source converted to a numeric result')
        if any(r[k] is not None for k in r if k.startswith(('net_','scenario_'))):
            raise ValueError('Unresolved monetary field must remain null')
    if (meta['camp_polygons_2026'],meta['camp_census_households_observed_2024'],
        meta['camp_census_count_missing_polygons'],meta['irrecoverable_dwellings_2024']) != (1345,71760,222,73338):
        raise ValueError('Camp/Census totals drift')
    top=sorted([r for r in rows if r['source_available'] and r['camp_sensitivity_positive_gap']>0],key=lambda r:(-r['camp_sensitivity_positive_gap'],r['codigo_comuna'].zfill(5)))[:15]
    for lang in ['es','en']:
        markup=(ROOT/'_includes'/f'avaluos-ii-top-{lang}.html').read_text()
        svg=(ROOT/'assets/images/avaluos-ii'/f'gap-top15-{lang}.svg').read_text()
        previous=-1
        for r in top:
            index=markup.index(r['comuna'])
            if index<=previous: raise ValueError('Translated table rank differs')
            previous=index
            value_label=format(int(r['camp_sensitivity_positive_gap']),',').replace(',','.') if lang=='es' else format(int(r['camp_sensitivity_positive_gap']),',')
            if r['comuna'] not in svg or value_label not in svg:
                raise ValueError('Figure missing canonical label/value')
    page=(ROOT/'catastro_sii_brecha/index.html').read_text()
    if page.count('id="brecha-contribuciones"')!=1 or page.count('data-gap-commune=')!=346:
        raise ValueError('Viewer missing unique section or complete fallback table')
    dictionary=json.loads((data/'dictionary.json').read_text())
    if set(dictionary['columns'])!=set(frame.columns): raise ValueError('Dictionary drift')
    print('PASS: 346 rows; camp sensitivity/materiality; Parquet/JSON/CSV; blocked fiscal fields; ES/EN figures and tables; one viewer')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=ROOT/'catastro_sii_brecha/data/fiscal-gap')
    verify(p.parse_args().data)
