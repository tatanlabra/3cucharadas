import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import { AriaComponent, GridComponent, TooltipComponent } from "echarts/components";
import { SVGRenderer } from "echarts/renderers";

echarts.use([BarChart, AriaComponent, GridComponent, TooltipComponent, SVGRenderer]);
export interface GapRow {
  codigo_comuna: string; comuna: string; region: string;
  signed_gap: number | null; source_available: boolean;
  dwellings_2024: number; residential_roles_2026s1: number | null;
}
export function diagnosticRanking(rows: GapRow[], region: string | null = null): GapRow[] {
  return rows.filter(r => r.source_available && r.signed_gap !== null && Number.isFinite(r.signed_gap)
    && r.signed_gap > 0 && (!region || r.region === region))
    .sort((a, b) => b.signed_gap! - a.signed_gap! || a.codigo_comuna.padStart(5, "0").localeCompare(b.codigo_comuna.padStart(5, "0")));
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
  const chart = echarts.init(host, undefined, { renderer: "svg" });
  const number = new Intl.NumberFormat("es-CL");
  const render = () => {
    const ranking = diagnosticRanking(payload.communes, region);
    const top = ranking.slice(0, 15);
    const selected = payload.communes.find(r => r.codigo_comuna === code);
    const position = ranking.findIndex(r => r.codigo_comuna === code);
    status.textContent = `${region || "Chile"}: ${ranking.length} comunas con diferencia positiva. ` +
      (selected ? `${selected.comuna}: ${selected.signed_gap === null ? "sin fuente" : number.format(selected.signed_gap) + " de diferencia"}; ${position < 0 ? "fuera del ranking positivo" : "posición " + (position + 1) + (position >= 15 ? " (fuera de las 15 barras)" : "")}. ` : "") +
      "Diagnóstico de viviendas menos roles; el ranking en pesos está pendiente.";
    const color = getComputedStyle(host).color;
    chart.setOption({ aria: { enabled: true, label: { description: status.textContent ?? "Diagnóstico residencial; valores completos en la tabla" } }, animation: false,
      grid: { left: 125, right: 32, top: 12, bottom: 55 },
      xAxis: { type: "value", min: 0, name: "Viviendas menos roles H", nameLocation: "middle", nameGap: 30, splitNumber: host.clientWidth < 500 ? 2 : 5,
        axisLabel: { color, hideOverlap: true, formatter: (v: number) => host.clientWidth < 500 && v >= 1000 ? `${number.format(v / 1000)} mil` : number.format(v) }, nameTextStyle: { color } },
      yAxis: { type: "category", inverse: true, data: top.map(r => r.comuna), axisLabel: { color, width: 118, overflow: "truncate" } },
      tooltip: { trigger: "axis", renderMode: "richText" },
      series: [{ type: "bar", data: top.map(r => ({ value: r.signed_gap,
        itemStyle: { color: r.codigo_comuna === code ? "#b65225" : "#397e78" } })) }]
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
  new ResizeObserver(() => { chart.resize(); render(); }).observe(host);
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
