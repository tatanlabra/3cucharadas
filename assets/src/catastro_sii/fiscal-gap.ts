import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import { AriaComponent, GridComponent, TooltipComponent } from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import { chartBase, escapeHtml, getChart, themeColors } from "./chart-theme";

echarts.use([BarChart, AriaComponent, GridComponent, TooltipComponent, SVGRenderer]);
export interface GapRow {
  codigo_comuna: string; comuna: string; region: string;
  signed_gap: number | null; source_available: boolean;
  dwellings_2024: number; residential_roles_2026s1: number | null;
  camp_census_households_observed_2024: number;
  camp_census_count_missing_polygons: number;
  camp_sensitivity_positive_gap: number | null;
  camp_absorbed_positive_gap: number | null;
  camp_adjustment_status: string;
  materiality_acceptable_scenario: number | null;
  materiality_other_scenario: number | null;
  materiality_acceptable_share_observed: number | null;
  assessment_mean_clp: number | null;
  assessment_median_clp: number | null;
  assessment_above_exemption_share: number | null;
}
export interface FiscalGapPalette {
  residual: string;
  absorbed: string;
  selection: string;
  other: string;
  boundary: string;
}
export function fiscalGapPalette(dark: boolean): FiscalGapPalette {
  return dark
    ? { residual: "#55C4C0", absorbed: "#F0B35B", other: "#98A8BD", selection: "#F3F5F8", boundary: "#61758F" }
    : { residual: "#56BDB9", absorbed: "#EFB35F", other: "#99ABC2", selection: "#17212B", boundary: "#40566E" };
}
export function scenarioSegments(row: GapRow): [number, number, number] {
  const values = [row.materiality_acceptable_scenario, row.materiality_other_scenario, row.camp_absorbed_positive_gap];
  if (!values.every(v => v !== null && Number.isFinite(v) && v >= 0)
    || row.signed_gap === null || Math.abs(values.reduce<number>((s, v) => s + (v ?? 0), 0) - Math.max(row.signed_gap, 0)) > .00001)
    throw new Error("Composición del escenario incompatible");
  return values as [number, number, number];
}
export function diagnosticRanking(rows: GapRow[], region: string | null = null): GapRow[] {
  return rows.filter(r => r.source_available && r.camp_sensitivity_positive_gap !== null
    && Number.isFinite(r.camp_sensitivity_positive_gap) && r.camp_sensitivity_positive_gap > 0
    && (!region || r.region === region))
    .sort((a, b) => b.camp_sensitivity_positive_gap! - a.camp_sensitivity_positive_gap!
      || a.codigo_comuna.padStart(5, "0").localeCompare(b.codigo_comuna.padStart(5, "0")));
}
export function selectGapCommune(row: GapRow): void {
  const region = document.getElementById("region");
  const commune = document.getElementById("comuna");
  if (!(region instanceof HTMLSelectElement) || !(commune instanceof HTMLSelectElement)) return;
  region.value = row.region;
  region.dispatchEvent(new Event("change", { bubbles: true }));
  commune.value = row.codigo_comuna;
  commune.dispatchEvent(new Event("change", { bubbles: true }));
}
export async function mountFiscalGap(): Promise<void> {
  const host = document.getElementById("fiscal-gap-chart");
  const status = document.getElementById("fiscal-gap-selection");
  if (!host || !status) return;
  const response = await fetch("data/fiscal-gap/communes.json");
  if (!response.ok) throw new Error("Diagnóstico no disponible");
  const payload = await response.json() as { metadata: { fiscal_status: string }; communes: GapRow[] };
  // This release supports diagnostics only. New monetary data needs a reviewed adapter.
  if (payload.metadata.fiscal_status !== "blocked_components" || payload.communes.length !== 346)
    throw new Error("Contrato de diagnóstico incompatible");
  let region = (document.getElementById("region") as HTMLSelectElement | null)?.value || null;
  let code = (document.getElementById("comuna") as HTMLSelectElement | null)?.value || null;
  host.hidden = false;
  const chart = getChart(host, "Brecha inicial: campamentos y composición supuesta de la brecha restante");
  const number = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
  const percent = new Intl.NumberFormat("es-CL", { style: "percent", maximumFractionDigits: 1 });
  const currency = (n: number | null) => n === null ? "sin dato" : "$" + number.format(n);
  const render = () => {
    const ranking = diagnosticRanking(payload.communes, region);
    const top = ranking.slice(0, 15);
    const segments = top.map(scenarioSegments);
    const selected = payload.communes.find(r => r.codigo_comuna === code);
    const position = ranking.findIndex(r => r.codigo_comuna === code);
    status.textContent = `${region || "Chile"} · ${ranking.length} comunas con brecha restante positiva. ` +
      (selected ? `${selected.comuna}: ${selected.signed_gap === null ? "sin fuente de roles" : number.format(selected.signed_gap) + " al inicio y " + number.format(selected.camp_sensitivity_positive_gap ?? 0) + " tras el supuesto de campamentos"}; ${position < 0 ? "fuera del orden mostrado" : "posición " + (position + 1) + (position >= 15 ? " (fuera de las 15 barras)" : "")}.` : "Orden: mayor brecha restante primero.");
    const context = document.getElementById("fiscal-gap-territory");
    if (context) {
      context.hidden = !selected;
      context.textContent = selected ? `${selected.comuna} · En los roles habitacionales observados: avalúo mediano ${currency(selected.assessment_median_clp)}, promedio ${currency(selected.assessment_mean_clp)}; ${selected.assessment_above_exemption_share === null ? "sin dato" : percent.format(selected.assessment_above_exemption_share)} sobre el umbral general. Son referencias para revisar el catastro; no estiman los avalúos ni el impuesto de viviendas sin enlace predial.` : "";
    }
    const colors = themeColors();
    const palette = fiscalGapPalette(colors.dark);
    const styles = getComputedStyle(document.documentElement);
    palette.residual = styles.getPropertyValue("--gap-acceptable").trim() || palette.residual;
    palette.other = styles.getPropertyValue("--gap-other").trim() || palette.other;
    palette.absorbed = styles.getPropertyValue("--gap-camp").trim() || palette.absorbed;
    palette.boundary = styles.getPropertyValue("--gap-boundary").trim() || palette.boundary;
    const mobile = host.clientWidth < 500;
    const base = chartBase(`${status.textContent} Cada barra suma la brecha inicial: tipo y materiales aceptables supuestos, resto del escenario y descuento de campamentos. No son viviendas enlazadas a roles. Datos completos en la tabla.`);
    chart.setOption({
      ...base,
      animation: false,
      grid: { containLabel: true, left: 4, right: mobile ? 8 : 120, top: 10, bottom: mobile ? 18 : 42 },
      xAxis: { type: "value", min: 0, name: mobile ? "" : "Total de la barra = diferencia original", nameLocation: "middle", nameGap: 34,
        splitNumber: mobile ? 2 : 5,
        axisLine: { lineStyle: { color: colors.line } }, splitLine: { lineStyle: { color: colors.line, opacity: .58 } },
        axisLabel: { color: colors.muted, hideOverlap: true, formatter: (v: number) => mobile && v >= 1000 ? `${number.format(v / 1000)} mil` : number.format(v) },
        nameTextStyle: { color: colors.muted, fontWeight: 700 } },
      yAxis: { type: "category", inverse: true, data: top.map(r => r.comuna),
        axisLine: { show: false }, axisTick: { show: false },
        axisLabel: { color: colors.ink, width: mobile ? 102 : 132, overflow: "truncate", fontWeight: 650 } },
      tooltip: { ...base.tooltip as object, trigger: "axis", confine: true,
        extraCssText: `max-width:${Math.min(320, Math.max(180, host.clientWidth - 24))}px;white-space:normal`,
        formatter: (params: unknown) => {
        const list = params as Array<{ dataIndex: number }>;
        const row = top[list[0]?.dataIndex ?? 0];
        if (!row) return "";
        const quality = row.camp_census_count_missing_polygons
          ? `<br>Campamentos con conteo pendiente: ${number.format(row.camp_census_count_missing_polygons)}` : "";
        return `<strong>${escapeHtml(row.comuna)}</strong><br>Brecha inicial: ${number.format(row.signed_gap ?? 0)}` +
          `<br>Descuento supuesto por campamentos: ${number.format(row.camp_absorbed_positive_gap ?? 0)}` +
          `<br><strong>Brecha restante: ${number.format(row.camp_sensitivity_positive_gap ?? 0)}</strong>` +
          `<br>Tipo y materiales aceptables: ≈ ${number.format(row.materiality_acceptable_scenario ?? 0)} (escenario)` +
          `<br>Resto: ≈ ${number.format(row.materiality_other_scenario ?? 0)}` +
          `<br>Proporción observada trasladada: ${row.materiality_acceptable_share_observed === null ? "sin dato" : percent.format(row.materiality_acceptable_share_observed)}` +
          `<br>Avalúo mediano de roles habitacionales registrados: ${currency(row.assessment_median_clp)}${quality}` +
          `<br><em>Composición supuesta; no acredita omisión ni impuesto.</em>`;
      } },
      series: [
        { name: "Tipo y materiales aceptables (escenario)", type: "bar", stack: "gap", barWidth: mobile ? 14 : 18,
          itemStyle: { color: palette.residual },
          data: top.map((r, i) => ({ value: segments[i][0],
            itemStyle: { borderColor: r.codigo_comuna === code ? palette.selection : palette.boundary, borderWidth: r.codigo_comuna === code ? 2 : .8, borderRadius: [3, 0, 0, 3] } })) },
        { name: "Resto del escenario", type: "bar", stack: "gap", barWidth: mobile ? 14 : 18,
          itemStyle: { color: palette.other },
          data: top.map((r, i) => ({ value: segments[i][1],
            itemStyle: { borderColor: r.codigo_comuna === code ? palette.selection : palette.boundary, borderWidth: r.codigo_comuna === code ? 2 : .8 } })) },
        { name: "Campamentos (descuento supuesto)", type: "bar", stack: "gap", barWidth: mobile ? 14 : 18,
          itemStyle: { color: palette.absorbed },
          data: top.map((r, i) => ({ value: segments[i][2],
            itemStyle: { borderColor: r.codigo_comuna === code ? palette.selection : palette.boundary, borderWidth: r.codigo_comuna === code ? 2 : .8, borderRadius: [0, 3, 3, 0] } })),
          label: { show: !mobile, position: "right", color: colors.ink, fontWeight: 750,
            formatter: (params: unknown) => `${number.format(top[(params as { dataIndex: number }).dataIndex].camp_sensitivity_positive_gap ?? 0)} restan` } }
      ]
    }, true);
    chart.off("click");
    chart.on("click", params => { const row = top[params.dataIndex]; if (row) selectGapCommune(row); });
    // The complete static table remains the keyboard and no-JS alternative.
  };
  render();
  window.addEventListener("catastro:selection", event => {
    const row = (event as CustomEvent<{ row?: GapRow }>).detail?.row;
    if (row) { region = row.region; code = row.codigo_comuna; render(); }
  });
  window.addEventListener("catastro:region-selection", event => {
    const detail = (event as CustomEvent<{ region?: string; communeCode?: string }>).detail;
    region = detail?.region || null; code = detail?.communeCode || null; render();
  });
  window.addEventListener("catastro:theme", render);
  let previousMobile = host.clientWidth < 500;
  new ResizeObserver(() => {
    chart.resize();
    const nextMobile = host.clientWidth < 500;
    if (nextMobile !== previousMobile) { previousMobile = nextMobile; render(); }
  }).observe(host);
  document.querySelectorAll<HTMLButtonElement>("[data-gap-commune]").forEach(button => {
    button.addEventListener("click", () => {
      const row = payload.communes.find(r => r.codigo_comuna === button.dataset.gapCommune);
      if (row) selectGapCommune(row);
    });
    button.hidden = false;
  });
  const fallback = document.getElementById("fiscal-gap-static");
  if (fallback) fallback.hidden = true;
}
