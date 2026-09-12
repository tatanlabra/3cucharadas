"""Aggregate-only static figures and bilingual accessible model tables."""
import html
import math
import matplotlib
import matplotlib.pyplot as plt


def ranked(rows):
    return sorted((r for r in rows if r.get('modeled_tax_status') == 'available'
                   and r['source_available'] and r['camp_sensitivity_positive_gap'] > 0
                   and r['assessment_median_clp'] > 60030710),
                  key=lambda r: (-r['modeled_gap_mean_clp'], r['codigo_comuna'].zfill(5)))[:15]


def label(value, lang, decimals=1):
    text = f'{value:,.{decimals}f}'
    return text.translate(str.maketrans(',.', '.,')) if lang == 'es' else text


def table(rows, lang):
    headers = (['Comuna', 'Residuo', 'Mediana × residuo', 'Promedio × residuo', 'Promedio × 50%', 'Promedio × 25%', 'Campamentos sin conteo']
               if lang == 'es' else ['Commune', 'Residual', 'Median × residual', 'Mean × residual', 'Mean × 50%', 'Mean × 25%', 'Settlements without counts'])
    caption = ('Escenarios en millones de pesos anuales equivalentes, reglas generales 2026S1. Mediana y promedio incluyen los ceros. No es deuda observada.' if lang == 'es' else
               'Scenarios in million CLP annual equivalents, 2026H1 general rules. Median and mean include zeros. Not observed tax debt.')
    lines = [f'<div class="avaluos-ii-table" role="region" tabindex="0" aria-label="{caption}" style="overflow-x:auto"><table><caption>{caption}</caption><thead><tr>',
             ''.join(f'<th scope="col">{h}</th>' for h in headers), '</tr></thead><tbody>']
    for r in rows:
        values = [label(r['camp_sensitivity_positive_gap'], lang, 0),
                  *[label(r[k]/1e6, lang) for k in ['modeled_gap_median_clp', 'modeled_gap_mean_clp', 'modeled_q05_mean_clp', 'modeled_q025_mean_clp']],
                  str(r['camp_census_count_missing_polygons'])]
        lines.append('<tr><th scope="row">'+html.escape(r['comuna'])+'</th>'+''.join(f'<td>{v}</td>' for v in values)+'</tr>')
    return '\n'.join(lines+['</tbody></table></div>'])+'\n'


def validate_modeled(source):
    top = ranked(source['communes'])
    if not top or [r['codigo_comuna'] for r in top] != source['metadata']['model_ranking'][:15]:
        raise ValueError('Model ranking differs from canonical metadata')
    for row in top:
        for statistic in ('mean', 'median'):
            product = row.get(f'modeled_gap_{statistic}_clp')
            annual = row.get(f'modeled_{statistic}_annual_clp')
            if any(type(value) not in (int, float) or not math.isfinite(value) or value < 0 for value in (product, annual)):
                raise ValueError('Missing/nonfinite modeled value')
            if not math.isclose(product, row['camp_sensitivity_positive_gap']*annual, rel_tol=1e-10):
                raise ValueError('Model multiplication differs')
    return top


def render_modeled(source, images):
    """Write figures only; independent of viewer and HTML-table projection."""
    import hashlib
    from pathlib import Path
    from matplotlib.lines import Line2D
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    from matplotlib.transforms import blended_transform_factory
    from editorial_style import editorial_style, embed_svg_fonts
    top = validate_modeled(source)
    images = Path(images)
    images.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for lang in ('es', 'en'):
        es = lang == 'es'
        for theme in ('light', 'dark'):
            with editorial_style(theme) as colors:
                fig = plt.figure(figsize=(12, 10.7))
                ax = fig.add_axes((.205, .205, .52, .58))
                median = [r['modeled_gap_median_clp']/1e6 for r in top]
                mean = [r['modeled_gap_mean_clp']/1e6 for r in top]
                ax.barh([i-.16 for i in range(len(top))], median, height=.24, color=colors['track'])
                ax.barh([i+.16 for i in range(len(top))], mean, height=.24, color=colors['residual'])
                ax.set_yticks(range(len(top)), [r['comuna'] for r in top], fontsize=11)
                ax.set_ylim(len(top)-.35, -.9)
                ax.set_xlim(0, max(median+mean)*1.05)
                ax.spines[:].set_visible(False)
                ax.tick_params(axis='y', length=0, pad=12, colors=colors['ink'])
                ax.tick_params(axis='x', length=0, pad=8, colors=colors['muted'], labelsize=10)
                ax.xaxis.set_major_locator(MaxNLocator(5))
                ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: label(value,lang,0)))
                ax.grid(axis='x', color=colors['line'], linewidth=.7)
                ax.set_axisbelow(True)
                trans = blended_transform_factory(fig.transFigure, ax.transData)
                for i, (med, avg) in enumerate(zip(median, mean)):
                    for x, value, bold in ((.827, med, False), (.952, avg, True)):
                        fig.text(x, i, label(value,lang), transform=trans, ha='right', va='center',
                                 fontsize=10.5, weight='bold' if bold else 'normal', color=colors['ink'])
                fig.text(.035,.958,'AVALÚOS II  /  ESCENARIO TRIBUTARIO' if es else 'PROPERTY ASSESSMENTS II  /  TAX SCENARIO',
                         fontsize=10, weight='bold', color=colors['muted'])
                fig.text(.035,.915,'La dimensión tributaria del escenario' if es else 'The tax dimension of the scenario',fontsize=23,weight='bold')
                fig.text(.035,.877,'Residuo positivo y avalúo mediano sobre el monto exento · perfil aplicado al 100%' if es else
                         'Positive residual and median assessment above the exemption · profile applied to 100%',fontsize=11,color=colors['muted'])
                fig.legend([Line2D([0],[0],color=colors['track'],lw=6), Line2D([0],[0],color=colors['residual'],lw=6)],
                           ['Mediana × residuo','Promedio × residuo'] if es else ['Median × residual','Mean × residual'],
                           loc='upper left',bbox_to_anchor=(.03,.853),ncol=2,frameon=False,fontsize=10.5,labelcolor=colors['ink'])
                for x, text in ((.827,'Mediana' if es else 'Median'),(.952,'Promedio' if es else 'Mean')):
                    fig.text(x,.794,text,ha='right',fontsize=10,weight='bold',color=colors['muted'])
                ax.set_xlabel('Millones de pesos anuales equivalentes · reglas 2026S1' if es else
                              'Million CLP annual equivalents · 2026H1 rules',fontsize=10,labelpad=12)
                fig.text(.035,.129,'DOS ESCENARIOS · NO ES DEUDA OBSERVADA' if es else 'TWO SCENARIOS · NOT OBSERVED TAX DEBT',fontsize=10,weight='bold')
                caption = ('Impuesto general por predio, luego mediana y promedio incluidos los ceros; multiplicados por el residuo.\n'
                           'Sin aseo, sobretasas ni beneficios particulares. No son intervalos de confianza ni giros de contribuciones.\n'
                           '15 mayores escenarios promedio dentro del filtro declarado; campamentos bajo supuesto uno a uno.' if es else
                           'General tax per property, then median and mean including zeros; multiplied by the residual.\n'
                           'No refuse charge, surtaxes or individual benefits. Not confidence intervals or issued tax bills.\n'
                           '15 largest mean scenarios within the stated filter; settlements under a one-household-per-dwelling assumption.')
                fig.text(.035,.059,caption,fontsize=9.3,linespacing=1.6,color=colors['muted'])
                fig.text(.035,.026,'3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones',fontsize=9,color=colors['muted'])
                for extension in ('svg','png'):
                    target = images/f'monetary-top15-{lang}{"-dark" if theme == "dark" else ""}.{extension}'
                    metadata = {'Date':None,'Description':caption} if extension == 'svg' else {'Description':caption}
                    fig.savefig(target,dpi=180,metadata=metadata)
                    if extension == 'svg':
                        target.write_text('\n'.join(line.rstrip() for line in embed_svg_fonts(target.read_text()).splitlines())+'\n')
                    artifacts.append(dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size))
                plt.close(fig)
    return artifacts


def project_modeled(source, root, images):
    """Legacy projection entrypoint retains tables; standalone uses render_modeled."""
    top = validate_modeled(source)
    render_modeled(source, images)
    for lang in ('es', 'en'):
        (root/'_includes'/f'avaluos-ii-monetary-{lang}.html').write_text(table(top, lang))
    return table(top, 'es')
