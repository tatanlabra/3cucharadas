import { chartBase, escapeHtml, getChart, replaceTable, themeColors } from "./chart-theme";
import type { GapRow } from "./fiscal-gap";

export interface ModeledRow extends GapRow {
  modeled_tax_status: string;
  modeled_mean_annual_clp: number | null;
  modeled_median_annual_clp: number | null;
  modeled_gap_mean_clp: number | null;
  modeled_gap_median_clp: number | null;
}
export function modeledRanking(rows: ModeledRow[], region: string | null = null): ModeledRow[] {
  return rows.filter(r => r.source_available && r.modeled_tax_status === "available"
    && (r.camp_sensitivity_positive_gap ?? 0) > 0 && (r.assessment_median_clp ?? 0) > 60030710
    && r.modeled_gap_mean_clp !== null && Number.isFinite(r.modeled_gap_mean_clp) && r.modeled_gap_mean_clp >= 0
    && r.modeled_gap_median_clp !== null && Number.isFinite(r.modeled_gap_median_clp) && r.modeled_gap_median_clp >= 0
    && (!region || r.region === region))
    .sort((a,b) => b.modeled_gap_mean_clp! - a.modeled_gap_mean_clp!
      || a.codigo_comuna.padStart(5,"0").localeCompare(b.codigo_comuna.padStart(5,"0")));
}
export function modeledValues(row: ModeledRow, q: number): [number, number] {
  if (![0, .25, .5, 1].includes(q) || row.modeled_gap_mean_clp === null || row.modeled_gap_median_clp === null
    || ![row.modeled_gap_mean_clp, row.modeled_gap_median_clp].every(v => Number.isFinite(v) && v >= 0))
    throw new Error("Escenario tributario incompatible");
  return [row.modeled_gap_median_clp * q, row.modeled_gap_mean_clp * q];
}
export function mountModeledTax(rows: ModeledRow[]): void {
  const host = document.getElementById("modeled-tax-chart");
  const status = document.getElementById("modeled-tax-status");
  const select = document.getElementById("modeled-tax-q");
  if (!host || !status || !(select instanceof HTMLSelectElement)) return;
  host.hidden = false;
  let region = (document.getElementById("region") as HTMLSelectElement | null)?.value || null;
  const chart = getChart(host, "Contribución general teórica: escenarios con mediana y promedio");
  const money = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 1 });
  const amount = (v: number) => "$" + money.format(v / 1e6) + " millones";
  const render = () => {
    const q = Number(select.value), top = modeledRanking(rows, region).slice(0, 15);
    const values = top.map(r => modeledValues(r, q));
    host.style.height = `${Math.min(660, Math.max(190, top.length*38+90))}px`;
    host.hidden = top.length === 0;
    status.textContent = top.length ? `${region || "Chile"} · ${top.length} comunas con residuo positivo y avalúo mediano sobre el umbral. Se aplica el perfil registrado al ${q * 100}% del residuo. Orden por escenario promedio al 100%.`
      : `${region || "Chile"} · Ninguna comuna cumple este filtro de priorización. Consulta el diagnóstico físico y la tabla nacional.`;
    const activeTable = document.getElementById("modeled-tax-current");
    if (activeTable) {
      activeTable.hidden = !top.length;
      replaceTable("modeled-tax-current-table", ["Comuna", `Mediana · ${q*100}%`, `Promedio · ${q*100}%`],
        top.map((r,i) => [r.comuna, amount(values[i][0]), amount(values[i][1])]));
    }
    const colors = themeColors(), mobile = host.clientWidth < 500;
    const base = chartBase(status.textContent + " Dos escenarios, no intervalo estadístico ni deuda observada. Tabla accesible disponible.");
    chart.setOption({ ...base, animation: false,
      grid: { containLabel: true, left: 4, right: 12, top: 12, bottom: 42 },
      xAxis: { type: "value", min: 0, splitNumber: mobile ? 2 : 5,
        name: "Millones de pesos · anual equivalente", nameLocation: "middle", nameGap: 30,
        nameTextStyle: { color: colors.muted, fontSize: 11 },
        axisLabel: { color: colors.muted, formatter: (v: number) => money.format(v / 1e6) },
        splitLine: { lineStyle: { color: colors.line } } },
      yAxis: { type: "category", inverse: true, data: top.map(r => r.comuna),
        axisTick: { show: false }, axisLine: { show: false },
        axisLabel: { color: colors.ink, width: mobile ? 102 : 140, overflow: "truncate", fontWeight: 650 } },
      tooltip: { ...base.tooltip as object, trigger: "axis", confine: true,
        extraCssText: `max-width:${mobile ? 230 : 330}px;white-space:normal`,
        formatter: (params: unknown) => {
          const index = (params as {dataIndex: number}[])[0]?.dataIndex;
          const row = top[index]; if (!row) return "";
          return `<strong>${escapeHtml(row.comuna)}</strong><br>Escenario mediana: ${amount(values[index][0])}`
            + `<br>Escenario promedio: ${amount(values[index][1])}<br>Perfil aplicado al ${q * 100}% del residuo.`
            + (row.camp_census_count_missing_polygons ? `<br>Campamentos sin conteo: ${row.camp_census_count_missing_polygons}.` : "")
            + "<br><em>Regla general sin beneficios individuales. No es giro, deuda ni recaudación.</em>";
        } },
      series: [
        { name: "Escenario mediana", type: "bar", barMaxWidth: 12,
          itemStyle: { color: colors.dark ? "#98A8BD" : "#99ABC2", borderWidth: .8, borderColor: colors.dark ? "#61758F" : "#40566E" }, data: values.map(v => v[0]) },
        { name: "Escenario promedio", type: "bar", barMaxWidth: 12,
          itemStyle: { color: colors.dark ? "#55C4C0" : "#56BDB9", borderWidth: .8, borderColor: colors.dark ? "#61758F" : "#40566E" }, data: values.map(v => v[1]) }
      ]
    }, true);
    chart.resize();
  };
  select.disabled = false;
  select.addEventListener("change", render);
  window.addEventListener("catastro:theme", render);
  window.addEventListener("catastro:selection", event => {
    const row = (event as CustomEvent<{row?: GapRow}>).detail?.row;
    if (row) { region = row.region; render(); }
  });
  window.addEventListener("catastro:region-selection", event => {
    region = (event as CustomEvent<{region?: string}>).detail?.region || null; render();
  });
  let previousMobile = host.clientWidth < 500;
  new ResizeObserver(() => {
    chart.resize(); const mobile = host.clientWidth < 500;
    if (previousMobile !== mobile) { previousMobile = mobile; render(); }
  }).observe(host);
  render();
}
