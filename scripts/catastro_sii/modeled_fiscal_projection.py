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


def project_modeled(source, root, images):
    top = ranked(source['communes'])
    if not top or [r['codigo_comuna'] for r in top] != source['metadata']['model_ranking'][:15]:
        raise ValueError('Model ranking differs from canonical metadata')
    for r in top:
        for statistic in ['mean', 'median']:
            if not math.isclose(r[f'modeled_gap_{statistic}_clp'], r['camp_sensitivity_positive_gap']*r[f'modeled_{statistic}_annual_clp'], rel_tol=1e-10):
                raise ValueError('Model multiplication differs')
    for lang in ['es', 'en']:
        (root/'_includes'/f'avaluos-ii-monetary-{lang}.html').write_text(table(top, lang))
        for dark in [False, True]:
            surface, ink, muted, line = ('#10121d','#f3f5f8','#a9afbd','#2a3041') if dark else ('#ffffff','#132033','#445570','#d6dfea')
            fig, ax = plt.subplots(figsize=(11, 8.5))
            fig.patch.set_facecolor(surface); ax.set_facecolor(surface)
            boundary = '#61758f' if dark else '#40566e'
            median = [r['modeled_gap_median_clp']/1e6 for r in top]
            mean = [r['modeled_gap_mean_clp']/1e6 for r in top]
            ax.barh([i-.16 for i in range(len(top))], median, height=.28, color='#98a8bd', edgecolor=boundary, linewidth=.65, label='Mediana' if lang=='es' else 'Median')
            ax.barh([i+.16 for i in range(len(top))], mean, height=.28, color='#55c4c0', edgecolor=boundary, linewidth=.65, label='Promedio' if lang=='es' else 'Mean')
            ax.set_yticks(range(len(top)), [r['comuna'] for r in top]); ax.invert_yaxis()
            ax.set_xlim(0, max(median+mean)*1.2)
            for i, v in enumerate(mean):
                ax.text(v+max(mean)*.012, i+.16, label(v,lang), va='center', fontsize=8, color=ink)
            ax.spines[['top','right','left']].set_visible(False); ax.spines['bottom'].set_color(line)
            ax.tick_params(axis='y',length=0,labelcolor=ink); ax.tick_params(axis='x',colors=muted)
            ax.grid(axis='x',color=line,alpha=.72); ax.set_axisbelow(True)
            ax.legend(loc='lower right',frameon=False,labelcolor=ink)
            title = 'Avalúos II · Dimensión tributaria del escenario' if lang=='es' else 'Property assessments II · Tax dimension of the scenario'
            fig.text(.04,.95,title,fontsize=17,weight='bold',color=ink)
            fig.text(.04,.905,'Residuo positivo y avalúo mediano sobre el monto exento · perfil aplicado al 100%' if lang=='es' else
                     'Positive residual and median assessment above the exemption · profile applied to 100%', fontsize=10,color=muted)
            ax.set_xlabel('Millones de pesos · anual equivalente con reglas 2026S1' if lang=='es' else 'Million CLP · annual equivalent at 2026H1 rules',color=muted,fontsize=10)
            caption = ('Impuesto general calculado por predio antes de obtener mediana/promedio, incluidos ceros.\nSe multiplican por el residuo tras el supuesto de campamentos. Sin aseo, sobretasas ni beneficios particulares.\nDos escenarios, no intervalo de confianza, giros ni deuda observada. Orden por escenario promedio.\nMétodo: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones' if lang=='es' else
                       'General tax calculated per property before computing median/mean, including zeros.\nMultiplied by the residual after the settlement assumption. No refuse charge, surtaxes or individual benefits.\nTwo scenarios, not confidence bounds, tax bills or observed debt. Sorted by mean scenario.\nMethod: 3cucharadas.cl/catastro_sii_brecha/#brecha-contribuciones')
            fig.text(.04,.025,caption,fontsize=9,linespacing=1.5,color=muted)
            fig.subplots_adjust(left=.22,right=.97,top=.86,bottom=.20)
            suffix = '-dark' if dark else ''
            target = images/f'monetary-top15-{lang}{suffix}.svg'
            with matplotlib.rc_context({'svg.fonttype':'none','svg.hashsalt':'avaluos-ii-modeled'}):
                fig.savefig(target,metadata={'Date':None})
            target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
            fig.savefig(images/f'monetary-top15-{lang}{suffix}.png',dpi=180,metadata={'Description':caption})
            plt.close(fig)
    return table(top, 'es')
