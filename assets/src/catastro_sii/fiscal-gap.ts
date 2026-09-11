import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import { AriaComponent, GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import { chartBase, escapeHtml, getChart, themeColors } from "./chart-theme";

echarts.use([BarChart, AriaComponent, GridComponent, LegendComponent, TooltipComponent, SVGRenderer]);
export interface GapRow {
  codigo_comuna: string; comuna: string; region: string;
  signed_gap: number | null; source_available: boolean;
  dwellings_2024: number; residential_roles_2026s1: number | null;
  camp_census_households_observed_2024: number;
  camp_census_count_missing_polygons: number;
  camp_sensitivity_positive_gap: number | null;
  camp_absorbed_positive_gap: number | null;
  camp_adjustment_status: string;
}
export interface FiscalGapPalette {
  residual: string;
  absorbed: string;
  selection: string;
}
export function fiscalGapPalette(dark: boolean): FiscalGapPalette {
  return dark
    ? { residual: "#55C4C0", absorbed: "#F0B35B", selection: "#F3F5F8" }
    : { residual: "#0F6F78", absorbed: "#C57A23", selection: "#17212B" };
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
  const chart = getChart(host, "Diferencia original y residuo después de descontar hogares censados en campamentos");
  const number = new Intl.NumberFormat("es-CL");
  const render = () => {
    const ranking = diagnosticRanking(payload.communes, region);
    const top = ranking.slice(0, 15);
    const selected = payload.communes.find(r => r.codigo_comuna === code);
    const position = ranking.findIndex(r => r.codigo_comuna === code);
    status.textContent = `${region || "Chile"}: ${ranking.length} comunas con residuo positivo. ` +
      (selected ? `${selected.comuna}: ${selected.signed_gap === null ? "sin fuente" : number.format(selected.signed_gap) + " original, " + number.format(selected.camp_census_households_observed_2024) + " hogares de campamento observados y " + number.format(selected.camp_sensitivity_positive_gap ?? 0) + " de residuo"}; ${position < 0 ? "fuera del ranking residual" : "posición " + (position + 1) + (position >= 15 ? " (fuera de las 15 barras)" : "")}. ` : "") +
      "Sensibilidad uno a uno; no es corrección observada ni ranking en pesos.";
    const colors = themeColors();
    const palette = fiscalGapPalette(colors.dark);
    const mobile = host.clientWidth < 500;
    chart.setOption({
      ...chartBase(status.textContent ?? "Sensibilidad residencial; valores completos en la tabla"),
      animation: false,
      legend: { top: 2, left: "center", itemWidth: 15, itemHeight: 9, selectedMode: false,
        textStyle: { color: colors.ink, fontSize: mobile ? 10 : 12 },
        data: ["Residuo", "Parte absorbida"] },
      grid: { containLabel: true, left: 8, right: mobile ? 12 : 62, top: mobile ? 58 : 42, bottom: mobile ? 26 : 54 },
      xAxis: { type: "value", min: 0, name: mobile ? "" : "Total de la barra = diferencia original", nameLocation: "middle", nameGap: 34,
        splitNumber: mobile ? 2 : 5,
        axisLine: { lineStyle: { color: colors.line } }, splitLine: { lineStyle: { color: colors.line, opacity: .58 } },
        axisLabel: { color: colors.muted, hideOverlap: true, formatter: (v: number) => mobile && v >= 1000 ? `${number.format(v / 1000)} mil` : number.format(v) },
        nameTextStyle: { color: colors.muted, fontWeight: 700 } },
      yAxis: { type: "category", inverse: true, data: top.map(r => r.comuna),
        axisLine: { show: false }, axisTick: { show: false },
        axisLabel: { color: colors.ink, width: mobile ? 94 : 122, overflow: "truncate", fontWeight: 650 } },
      tooltip: { trigger: "axis", confine: true, formatter: (params: unknown) => {
        const list = params as Array<{ dataIndex: number }>;
        const row = top[list[0]?.dataIndex ?? 0];
        if (!row) return "";
        const quality = row.camp_census_count_missing_polygons
          ? `<br><span style="color:${colors.muted}">Parcial: ${number.format(row.camp_census_count_missing_polygons)} polígonos S/I</span>` : "";
        return `<strong>${escapeHtml(row.comuna)}</strong><br>Diferencia original: ${number.format(row.signed_gap ?? 0)}` +
          `<br>Hogares Censo en campamentos: ${number.format(row.camp_census_households_observed_2024)}` +
          `<br><strong>Residuo: ${number.format(row.camp_sensitivity_positive_gap ?? 0)}</strong>${quality}`;
      } },
      series: [
        { name: "Residuo", type: "bar", stack: "gap", barWidth: mobile ? 14 : 18,
          itemStyle: { color: palette.residual },
          data: top.map(r => ({ value: r.camp_sensitivity_positive_gap,
            itemStyle: { borderColor: r.codigo_comuna === code ? palette.selection : "transparent", borderWidth: r.codigo_comuna === code ? 2 : 0, borderRadius: [4, 0, 0, 4] } })),
          label: { show: !mobile, position: "right", color: colors.ink, fontWeight: 750,
            formatter: (params: unknown) => number.format(Number((params as { value: number }).value)) } },
        { name: "Parte absorbida", type: "bar", stack: "gap", barWidth: mobile ? 14 : 18,
          itemStyle: { color: palette.absorbed },
          data: top.map(r => ({ value: r.camp_absorbed_positive_gap,
            itemStyle: { borderColor: r.codigo_comuna === code ? palette.selection : "transparent", borderWidth: r.codigo_comuna === code ? 2 : 0, borderRadius: [0, 4, 4, 0] } })) }
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
