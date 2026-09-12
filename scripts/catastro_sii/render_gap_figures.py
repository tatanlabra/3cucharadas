#!/usr/bin/env python3
"""Render frozen communal fiscal aggregates only; never project viewer/data files.

Example (from blog root):
  python scripts/catastro_sii/render_gap_figures.py --expected-sha256 <frozen JSON hash>

SVG/PNG carry scenario caveats; the embedding page must provide an HTML table
and explicit zoom/scroll at narrow widths (minimum presentation width 1000px).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from editorial_style import editorial_style, embed_svg_fonts
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT.parent/'catastros_sii/v5_brecha/artifacts/fiscal_gap/communes.json'
IMAGES = ROOT/'assets/images/avaluos-ii'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def number(value, lang):
    if value is None:
        return '—'
    return format(round(value), ',').replace(',', '.') if lang == 'es' else format(round(value), ',')


def validate_rows(rows):
    if not rows:
        raise ValueError('Empty communal source')
    seen = set()
    for row in rows:
        code = str(row['codigo_comuna']).zfill(5)
        if code in seen:
            raise ValueError(f'Duplicate commune: {code}')
        seen.add(code)
        if type(row['source_available']) is not bool:
            raise ValueError(f'Invalid availability: {code}')
        if not row['source_available']:
            continue
        keys = ('signed_gap', 'camp_sensitivity_positive_gap', 'camp_absorbed_positive_gap')
        if any(type(row.get(k)) not in (int, float) or not math.isfinite(row[k]) for k in keys):
            raise ValueError(f'Missing/nonfinite gap: {code}')
        initial = max(row['signed_gap'], 0)  # existing positive-gap scenario rule
        residual = row['camp_sensitivity_positive_gap']
        absorbed = row['camp_absorbed_positive_gap']
        if not 0 <= residual <= initial or absorbed < 0 or not math.isclose(initial, residual+absorbed, abs_tol=1e-7):
            raise ValueError(f'Invalid nested gap: {code}')
        acceptable = row.get('materiality_acceptable_scenario')
        other = row.get('materiality_other_scenario')
        if acceptable is None and other is None:
            continue  # unknown remains unknown; no zero imputation
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in (acceptable, other)):
            raise ValueError(f'Incomplete materiality scenario: {code}')
        if not 0 <= acceptable <= residual or other < 0 or not math.isclose(acceptable+other, residual, abs_tol=1e-7):
            raise ValueError(f'Invalid nested materiality: {code}')
    return rows


def load_source(path=SOURCE, expected_sha256=None):
    path = Path(path)
    if expected_sha256 is not None and digest(path) != expected_sha256:
        raise ValueError('Frozen JSON hash mismatch')
    source = json.loads(path.read_text())
    validate_rows(source['communes'])
    return source


def ranked(rows, limit=15):
    validate_rows(rows)
    eligible = [r for r in rows if r['source_available'] and r['camp_sensitivity_positive_gap'] > 0]
    if not eligible:
        raise ValueError('No positive residuals to plot')
    return sorted(eligible, key=lambda r: (-r['camp_sensitivity_positive_gap'], str(r['codigo_comuna']).zfill(5)))[:limit]


def make_figure(rows, lang, colors, missing_polygons):
    es = lang == 'es'
    fig = plt.figure(figsize=(12, 10.7))
    ax = fig.add_axes((.205, .205, .435, .58))
    initial = [r['signed_gap'] for r in rows]
    maximum = math.ceil(max(initial)/10000)*10000
    ax.set_xlim(0, maximum)
    ax.set_ylim(len(rows)-.35, -.9)
    ax.set_yticks(range(len(rows)), [r['comuna'] for r in rows], fontsize=11)
    ax.tick_params(axis='y', length=0, pad=12, colors=colors['ink'])
    ax.tick_params(axis='x', length=0, pad=8, colors=colors['muted'], labelsize=10)
    ax.spines[:].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(10000))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: number(value, lang)))
    ax.grid(axis='x', color=colors['line'], linewidth=.7, zorder=0)
    ax.set_axisbelow(True)
    columns = (.717, .832, .952)
    for i, row in enumerate(rows):
        residual = row['camp_sensitivity_positive_gap']
        acceptable = row.get('materiality_acceptable_scenario')
        # Three nested marks share a zero: outline = initial; solid = residual;
        # narrow interior stroke = materiality scenario. Not additive categories.
        ax.barh(i, initial[i], height=.58, facecolor=colors['surface'], edgecolor=colors['track'], linewidth=1.05, zorder=2)
        ax.barh(i, residual, height=.40, color=colors['residual'], zorder=3)
        if acceptable is not None:
            ax.barh(i, acceptable, height=.15, color=colors['material'], edgecolor=colors['surface'], linewidth=.6, zorder=4)
        values = (initial[i], residual, acceptable)
        for j, value in enumerate(values):
            # Figure x + axes y via a blended transform keeps columns aligned.
            from matplotlib.transforms import blended_transform_factory
            trans = blended_transform_factory(fig.transFigure, ax.transData)
            fig.text(columns[j], i, ('≈ ' if j == 2 and value is not None else '')+number(value, lang),
                     transform=trans, ha='right', va='center', fontsize=10.5,
                     color=colors['ink'] if j != 2 else colors['muted'],
                     weight='bold' if j == 1 else 'normal')
    fig.text(.035, .958, 'AVALÚOS II  /  DIAGNÓSTICO RESIDENCIAL' if es else 'PROPERTY ASSESSMENTS II  /  RESIDENTIAL DIAGNOSTIC',
             color=colors['muted'], fontsize=10, weight='bold')
    fig.text(.035, .915, 'La brecha que queda por explicar' if es else 'The gap that remains unexplained', fontsize=23, weight='bold')
    fig.text(.035, .877, '15 comunas con mayor residuo después del supuesto de campamentos' if es else
             '15 communes with the largest residual after the settlement assumption', fontsize=12, color=colors['muted'])
    handles = [Line2D([0], [0], color=colors['track'], lw=1.4),
               Line2D([0], [0], color=colors['residual'], lw=7),
               Line2D([0], [0], color=colors['material'], lw=3)]
    labels = ['Brecha inicial', 'Tras campamentos', 'Tipo y materiales aceptables ≈'] if es else ['Initial gap', 'After settlements', 'Acceptable type and materials ≈']
    fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(.03,.853), ncol=3, frameon=False,
               fontsize=10.5, handlelength=1.7, columnspacing=2.2, labelcolor=colors['ink'])
    for x, label in zip(columns, ['Inicial', 'Restante', 'Aceptables ≈'] if es else ['Initial', 'Remaining', 'Acceptable ≈']):
        fig.text(x, .794, label, ha='right', fontsize=10, weight='bold', color=colors['muted'])
    ax.set_xlabel('Viviendas − roles habitacionales  /  escala común' if es else 'Dwellings − residential records  /  common scale', fontsize=10, labelpad=12)
    caveat = ('ESCENARIOS ANIDADOS · NO SON CASOS IDENTIFICADOS' if es else 'NESTED SCENARIOS · NOT IDENTIFIED CASES')
    fig.text(.035, .129, caveat, fontsize=10, weight='bold', color=colors['ink'])
    caption = ('Censo 2024 − roles SII 2026S1. Se descuentan hogares observados en campamentos bajo supuesto uno a uno.\n'
               'Al residuo se aplica la proporción comunal de tipo y materiales aceptables del Censo; cifras ≈ redondeadas.\n'
               f'No identifica viviendas sin rol ni deuda tributaria. {number(missing_polygons, lang)} polígonos CNC sin conteo; descuento incompleto.' if es else
               '2024 Census − 2026H1 SII records. Observed settlement households are deducted assuming one household per dwelling.\n'
               'The residual uses the Census commune share with acceptable type and materials; ≈ figures are rounded.\n'
               f'Identifies neither unregistered homes nor tax debt. {number(missing_polygons, lang)} CNC polygons lack counts; deduction is incomplete.')
    fig.text(.035, .059, caption, fontsize=9.3, linespacing=1.6, color=colors['muted'])
    fig.text(.035, .026, '3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones', fontsize=9, color=colors['muted'])
    return fig, caveat+'\n'+caption


def render(source, output=IMAGES):
    rows = ranked(source['communes'])
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for lang in ('es', 'en'):
        for theme in ('light', 'dark'):
            with editorial_style(theme) as colors:
                fig, caption = make_figure(rows, lang, colors, source['metadata']['camp_census_count_missing_polygons'])
                base = output/f'gap-top15-{lang}{"-dark" if theme == "dark" else ""}'
                for extension in ('svg', 'png'):
                    target = base.with_suffix('.'+extension)
                    metadata = {'Date': None, 'Description': caption} if extension == 'svg' else {'Description': caption}
                    fig.savefig(target, dpi=180, metadata=metadata)
                    if extension == 'svg':
                        # Preserve selectable text and provide standalone SVG semantics.
                        raw = target.read_text()
                        raw = raw.replace('<svg ', '<svg role="img" aria-labelledby="figure-title figure-description" ', 1)
                        escaped = lambda value: value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        end = raw.index('>', raw.index('<svg '))+1
                        raw = raw[:end]+'\n<title id="figure-title">'+escaped('Escenarios de brecha residencial' if lang == 'es' else 'Residential gap scenarios')+'</title>\n<desc id="figure-description">'+escaped(caption)+'</desc>'+raw[end:]
                        target.write_text('\n'.join(line.rstrip() for line in embed_svg_fonts(raw).splitlines())+'\n')
                        ET.parse(target)
                    artifacts.append({'file': target.name, 'sha256': digest(target), 'bytes': target.stat().st_size})
                plt.close(fig)
    return artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, default=IMAGES)
    parser.add_argument('--expected-sha256', required=True)
    args = parser.parse_args()
    source = load_source(args.source, args.expected_sha256)
    before = digest(args.source)
    from modeled_fiscal_projection import render_modeled
    artifacts = render(source, args.output) + render_modeled(source, args.output)
    if digest(args.source) != before:
        raise ValueError('Source changed during rendering')
    print(json.dumps({'source_sha256': before, 'selected_codes': [r['codigo_comuna'] for r in ranked(source['communes'])],
                      'minimum_display_width_css_px': 1000, 'artifacts': artifacts}, indent=2))


if __name__ == '__main__':
    main()
