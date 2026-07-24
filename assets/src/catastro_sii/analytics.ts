import * as echarts from "echarts/core";
import { BarChart, CustomChart, HeatmapChart, LineChart, SankeyChart, ScatterChart } from "echarts/charts";
import {
  AriaComponent,
  DataZoomComponent,
  DatasetComponent,
  GridComponent,
  LegendComponent,
  TooltipComponent
} from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import type { ECharts, EChartsCoreOption } from "echarts/core";
import { loadInsights } from "./insights";
import type { InsightsLoadResult } from "./insights";
import { isLaboratoryView, replaceVisualizationView, toDataCommuneCode, visualizationViewFromUrl } from "./state";
import type {
  CommuneInsight,
  InsightsV1,
  SensitivityRow,
  ViolinPanel,
  VisualizationView
} from "./types";

echarts.use([
  SVGRenderer,
  BarChart,
  LineChart,
  SankeyChart,
  ScatterChart,
  HeatmapChart,
  CustomChart,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  DataZoomComponent,
  AriaComponent
]);

type LaboratoryView = Exclude<VisualizationView, "mapa">;
type BubbleMetric = "av_total" | "av_household" | "av_person" | "av_m2";
type RankingUnit = "communes" | "regions";

const LAB_VIEWS: LaboratoryView[] = ["flujo", "avaluos", "distribuciones", "sensibilidad", "comunas"];
// Una clave estable por región: no se reciclan colores dentro de las 16 regiones.
const CHART_COLORS = [
  "#37e7ff", "#b8ff3c", "#ff4fd8", "#ffd166",
  "#8c7cff", "#62d6a6", "#ff7d66", "#60a5fa",
  "#19c3b1", "#ef5f75", "#b58cff", "#8bd346",
  "#f7a35c", "#4cc9f0", "#e76fbd", "#7f91a8"
];
const formatter = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 2 });
const integer = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
const currency = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 });

const METRICS: Record<BubbleMetric, { label: string; short: string }> = {
  av_total: { label: "Avalúo fiscal total", short: "total" },
  av_household: { label: "Avalúo fiscal por hogar RSH", short: "por hogar" },
  av_person: { label: "Avalúo fiscal por persona RSH", short: "por persona" },
  av_m2: { label: "Avalúo fiscal por m² predial asignado", short: "por m²" }
};

interface RankingRecord {
  id: string;
  name: string;
  region: string;
  unitLabel: string;
  vulnerability: number;
  rank: number;
  metrics: Record<BubbleMetric, number | null>;
  households: number;
  urban_pct: number | null;
  members: number;
}

function finiteNumber(value: number | null | undefined): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function weightedMean(values: Array<{ value: number | null | undefined; weight: number | null | undefined }>): number | null {
  let numerator = 0;
  let denominator = 0;
  for (const item of values) {
    if (!finiteNumber(item.value) || !finiteNumber(item.weight) || item.weight <= 0) continue;
    numerator += item.value * item.weight;
    denominator += item.weight;
  }
  return denominator > 0 ? numerator / denominator : null;
}

function assignNationalRanks(records: Omit<RankingRecord, "rank">[]): RankingRecord[] {
  return records
    .filter((record) => Number.isFinite(record.vulnerability))
    .sort((a, b) => b.vulnerability - a.vulnerability || a.name.localeCompare(b.name, "es"))
    .map((record, index) => ({ ...record, rank: index + 1 }));
}

function communeRankings(communes: CommuneInsight[]): RankingRecord[] {
  return assignNationalRanks(communes.flatMap((commune) => {
    if (!finiteNumber(commune.vulnerability) || !finiteNumber(commune.households) || commune.households <= 0) return [];
    return [{
      id: commune.code,
      name: commune.name,
      region: commune.region,
      unitLabel: "Comuna",
      vulnerability: commune.vulnerability,
      metrics: {
        av_total: commune.av_total,
        av_household: commune.av_household,
        av_person: commune.av_person,
        av_m2: commune.av_m2
      },
      households: commune.households,
      urban_pct: commune.urban_pct,
      members: 1
    }];
  }));
}

function regionRankings(communes: CommuneInsight[]): RankingRecord[] {
  const byRegion = new Map<string, CommuneInsight[]>();
  communes.forEach((commune) => {
    if (!finiteNumber(commune.vulnerability) || !finiteNumber(commune.households) || commune.households <= 0) return;
    byRegion.set(commune.region, [...(byRegion.get(commune.region) ?? []), commune]);
  });
  return assignNationalRanks([...byRegion.entries()].map(([region, rows]) => {
    const households = rows.reduce((sum, row) => sum + (row.households ?? 0), 0);
    const total = rows.reduce((sum, row) => sum + (row.av_total ?? 0), 0);
    return {
      id: region,
      name: region,
      region,
      unitLabel: "Región",
      vulnerability: weightedMean(rows.map((row) => ({ value: row.vulnerability, weight: row.households }))) ?? 0,
      metrics: {
        av_total: total > 0 ? total : null,
        av_household: households > 0 && total > 0 ? total / households : null,
        av_person: weightedMean(rows.map((row) => ({ value: row.av_person, weight: row.households }))),
        av_m2: weightedMean(rows.map((row) => ({ value: row.av_m2, weight: row.households })))
      },
      households,
      urban_pct: weightedMean(rows.map((row) => ({ value: row.urban_pct, weight: row.households }))),
      members: rows.length
    };
  }));
}

function themeColors(): { ink: string; muted: string; line: string; surface: string; dark: boolean } {
  const styles = getComputedStyle(document.documentElement);
  return {
    ink: styles.getPropertyValue("--ink").trim() || "#f3f5f8",
    muted: styles.getPropertyValue("--muted").trim() || "#a9afbd",
    line: styles.getPropertyValue("--line").trim() || "#2a3041",
    surface: styles.getPropertyValue("--surface").trim() || "#10121d",
    dark: document.documentElement.dataset.theme !== "light"
  };
}

function reducedMotion(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function escapeHtml(value: unknown): string {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function chartBase(ariaDescription: string): EChartsCoreOption {
  const colors = themeColors();
  return {
    animation: !reducedMotion(),
    animationDuration: reducedMotion() ? 0 : 360,
    color: CHART_COLORS,
    textStyle: { color: colors.ink, fontFamily: 'Inter, "Inter var", system-ui, sans-serif' },
    aria: { enabled: true, decal: { show: true }, description: ariaDescription },
    tooltip: {
      trigger: "item",
      confine: true,
      backgroundColor: colors.surface,
      borderColor: colors.line,
      textStyle: { color: colors.ink },
      extraCssText: "max-width:320px;white-space:normal"
    }
  };
}

function getChart(element: HTMLElement, label: string): ECharts {
  const existing = echarts.getInstanceByDom(element);
  element.setAttribute("role", "img");
  element.setAttribute("aria-label", label);
  return existing ?? echarts.init(element, undefined, { renderer: "svg" });
}

function makeElement<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text != null) element.textContent = text;
  return element;
}

function replaceTable(hostId: string, headers: string[], rows: Array<Array<string | number>>): void {
  const host = document.getElementById(hostId);
  if (!host) return;
  const table = makeElement("table", "lab-data-table");
  const caption = makeElement("caption", "visually-hidden", "Datos equivalentes a la visualización");
  const thead = makeElement("thead");
  const headRow = makeElement("tr");
  for (const header of headers) headRow.append(makeElement("th", undefined, header));
  thead.append(headRow);
  const tbody = makeElement("tbody");
  for (const row of rows) {
    const tr = makeElement("tr");
    row.forEach((cell, index) => tr.append(index === 0 ? makeElement("th", undefined, String(cell)) : makeElement("td", undefined, String(cell))));
    tbody.append(tr);
  }
  table.append(caption, thead, tbody);
  host.replaceChildren(table);
}

function displayLogValue(value: number): string {
  const original = 10 ** value;
  return original >= 1_000_000_000
    ? `$${formatter.format(original / 1_000_000_000)} mil millones`
    : original >= 1_000_000
      ? `$${formatter.format(original / 1_000_000)} millones`
      : currency.format(original);
}

function appraisalLabel(value: number): string {
  return `${formatter.format(value / 1_000_000_000_000)} billones`;
}

function renderAppraisals(data: InsightsV1): void {
  const regionsElement = document.getElementById("lab-appraisal-regions-chart");
  const communesElement = document.getElementById("lab-appraisal-communes-chart");
  if (!regionsElement || !communesElement) return;
  const colors = themeColors();
  const total = data.communes.reduce((sum, commune) => sum + (commune.av_total ?? 0), 0);
  const regions = Array.from(data.communes.reduce((map, commune) => {
    map.set(commune.region, (map.get(commune.region) ?? 0) + (commune.av_total ?? 0));
    return map;
  }, new Map<string, number>()))
    .map(([name, value]) => ({ name, value, share: total ? value / total : 0 }))
    .sort((a, b) => b.value - a.value);
  const communes = data.communes
    .filter((commune) => (commune.av_total ?? 0) > 0)
    .slice()
    .sort((a, b) => (b.av_total ?? 0) - (a.av_total ?? 0))
    .slice(0, 12);

  getChart(regionsElement, "Avalúo fiscal total asignado por región").setOption({
    ...chartBase("Barras horizontales del avalúo fiscal total asignado por región. El total nacional asignado alcanza 587,4 billones de pesos."),
    grid: { left: 184, right: 28, top: 18, bottom: 46 },
    xAxis: {
      type: "value",
      name: "Billones CLP",
      nameLocation: "middle",
      nameGap: 30,
      axisLabel: { color: colors.muted, formatter: (value: number) => formatter.format(value / 1_000_000_000_000) },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.6 } }
    },
    yAxis: {
      type: "category",
      inverse: true,
      data: regions.map((region) => region.name),
      axisLabel: { color: colors.muted, width: 170, overflow: "truncate" },
      axisLine: { lineStyle: { color: colors.line } }
    },
    series: [{
      type: "bar",
      data: regions.map((region, index) => ({
        value: region.value,
        itemStyle: { color: index === 0 ? "#37e7ff" : index < 3 ? "#62d6a6" : "#4d6475", opacity: index === 0 ? 0.82 : 0.62 }
      })),
      label: {
        show: true,
        position: "right",
        color: colors.ink,
        fontWeight: 800,
        formatter: (params: unknown) => `${formatter.format(100 * regions[(params as { dataIndex: number }).dataIndex].share)}%`
      },
      tooltip: { formatter: (params: unknown) => {
        const index = (params as { dataIndex: number }).dataIndex;
        const region = regions[index];
        return `<strong>${escapeHtml(region.name)}</strong><br>${appraisalLabel(region.value)}<br>${formatter.format(100 * region.share)}% del total asignado`;
      } }
    }]
  }, true);

  getChart(communesElement, "Doce comunas con mayor avalúo fiscal total asignado").setOption({
    ...chartBase("Barras horizontales de las comunas con mayor avalúo fiscal total asignado. La escala permite ubicar magnitud antes de normalizar."),
    grid: { left: 128, right: 26, top: 18, bottom: 46 },
    xAxis: {
      type: "value",
      name: "Billones CLP",
      nameLocation: "middle",
      nameGap: 30,
      axisLabel: { color: colors.muted, formatter: (value: number) => formatter.format(value / 1_000_000_000_000) },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.6 } }
    },
    yAxis: {
      type: "category",
      inverse: true,
      data: communes.map((commune) => commune.name),
      axisLabel: { color: colors.muted, width: 118, overflow: "truncate" },
      axisLine: { lineStyle: { color: colors.line } }
    },
    series: [{
      type: "bar",
      data: communes.map((commune, index) => ({
        value: commune.av_total ?? 0,
        itemStyle: { color: index < 5 ? "#8c7cff" : "#2f7f91", opacity: index < 5 ? 0.72 : 0.56 }
      })),
      label: {
        show: true,
        position: "right",
        color: colors.ink,
        fontWeight: 800,
        formatter: (params: unknown) => formatter.format(Number((params as { value: number }).value) / 1_000_000_000_000)
      },
      tooltip: { formatter: (params: unknown) => {
        const commune = communes[(params as { dataIndex: number }).dataIndex];
        return `<strong>${escapeHtml(commune.name)}</strong> · ${escapeHtml(commune.region)}<br>${appraisalLabel(commune.av_total ?? 0)}<br>${formatter.format(commune.av_m2 ?? 0)} CLP/m² asignado`;
      } }
    }]
  }, true);

  replaceTable(
    "lab-appraisal-table",
    ["Territorio", "Avalúo total", "% nacional"],
    regions.slice(0, 8).map((region) => [region.name, appraisalLabel(region.value), `${formatter.format(100 * region.share)}%`])
  );
}

function renderFlow(data: InsightsV1): void {
  const element = document.getElementById("lab-flow-chart");
  if (!element) return;
  const chart = getChart(element, "Flujo de registros originales, duplicados, predios únicos e intersección con unidades vecinales");
  const units = new Map(data.pipeline.nodes.map((node) => [node.id, node.unit]));
  const option: EChartsCoreOption = {
    ...chartBase("El flujo distingue registros de entrada de predios únicos; el último corte separa los predios que tocan al menos una unidad vecinal."),
    series: [{
      type: "sankey",
      left: 12,
      right: 16,
      top: 18,
      bottom: 28,
      nodeWidth: 18,
      nodeGap: 14,
      draggable: false,
      emphasis: { focus: "adjacency" },
      lineStyle: { color: "gradient", curveness: 0.52, opacity: 0.42 },
      label: { color: themeColors().ink, fontWeight: 700, width: 150, overflow: "break" },
      data: data.pipeline.nodes.map((node, index) => ({
        name: node.id,
        value: node.value,
        itemStyle: { color: CHART_COLORS[index % CHART_COLORS.length] },
        label: { formatter: `${node.label}\n${integer.format(node.value)}` }
      })),
      links: data.pipeline.links.map((link) => ({ source: link.source, target: link.target, value: link.value })),
      tooltip: {
        formatter: (params: unknown) => {
          const item = params as { dataType?: string; name?: string; value?: number; data?: { source?: string; target?: string } };
          if (item.dataType === "edge") {
            return `${escapeHtml(item.data?.source)} → ${escapeHtml(item.data?.target)}<br><strong>${integer.format(Number(item.value))}</strong>`;
          }
          const unit = units.get(item.name ?? "") === "records" ? "registros" : "predios únicos";
          return `${escapeHtml(item.name)}<br><strong>${integer.format(Number(item.value))}</strong> ${unit}`;
        }
      }
    }]
  };
  chart.setOption(option, true);
  replaceTable("lab-flow-table", ["Etapa", "Conteo", "Unidad"], data.pipeline.nodes.map((node) => [node.label, integer.format(node.value), node.unit === "records" ? "registros" : "predios únicos"]));
}

function violinOption(panel: ViolinPanel): EChartsCoreOption {
  const colors = themeColors();
  const allValues = panel.groups.flatMap((group) => group.points.map((point) => point[0]));
  const minimum = Math.min(...allValues);
  const maximum = Math.max(...allValues);
  return {
    ...chartBase(`${panel.title}. Distribución estimada por cuartil de vulnerabilidad; cada violín incluye mediana y rango intercuartílico.`),
    grid: { left: 70, right: 16, top: 28, bottom: 52 },
    xAxis: {
      type: "category",
      data: ["Q1 mayor", "Q2", "Q3", "Q4 menor"],
      name: "Vulnerabilidad IGVUST",
      nameLocation: "middle",
      nameGap: 34,
      axisLabel: { color: colors.muted },
      axisLine: { lineStyle: { color: colors.line } }
    },
    yAxis: {
      type: "value",
      min: minimum,
      max: maximum,
      axisLabel: { color: colors.muted, formatter: (value: number) => displayLogValue(value) },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.55 } }
    },
    series: [{
      type: "custom",
      coordinateSystem: "cartesian2d",
      data: panel.groups.map((group) => [group.quartile - 1, group.median]),
      renderItem: (params: { dataIndex: number }, api: { coord: (value: number[]) => number[]; size: (value: number[]) => number[] }) => {
        const group = panel.groups[params.dataIndex];
        const center = api.coord([group.quartile - 1, group.median]);
        const maxDensity = Math.max(...group.points.map((point) => point[1]), Number.EPSILON);
        const halfWidth = Math.min(38, api.size([1, 0])[0] * 0.35);
        const right = group.points.map(([value, density]) => [center[0] + (density / maxDensity) * halfWidth, api.coord([group.quartile - 1, value])[1]]);
        const left = group.points.slice().reverse().map(([value, density]) => [center[0] - (density / maxDensity) * halfWidth, api.coord([group.quartile - 1, value])[1]]);
        const q1 = api.coord([group.quartile - 1, group.q1]);
        const median = api.coord([group.quartile - 1, group.median]);
        const q3 = api.coord([group.quartile - 1, group.q3]);
        const color = CHART_COLORS[(group.quartile - 1) % CHART_COLORS.length];
        return {
          type: "group",
          children: [
            { type: "polygon", shape: { points: [...right, ...left] }, style: { fill: color, opacity: 0.58, stroke: color, lineWidth: 1.2 } },
            { type: "line", shape: { x1: center[0] - halfWidth * 0.36, y1: q1[1], x2: center[0] + halfWidth * 0.36, y2: q1[1] }, style: { stroke: colors.ink, lineWidth: 1.2 } },
            { type: "line", shape: { x1: center[0] - halfWidth * 0.36, y1: q3[1], x2: center[0] + halfWidth * 0.36, y2: q3[1] }, style: { stroke: colors.ink, lineWidth: 1.2 } },
            { type: "line", shape: { x1: center[0] - halfWidth * 0.48, y1: median[1], x2: center[0] + halfWidth * 0.48, y2: median[1] }, style: { stroke: colors.ink, lineWidth: 2.4 } }
          ]
        };
      },
      tooltip: {
        formatter: (params: unknown) => {
          const item = params as { dataIndex: number };
          const group = panel.groups[item.dataIndex];
          return `<strong>Cuartil ${group.quartile}</strong><br>n = ${integer.format(group.n)}<br>Mediana: ${displayLogValue(group.median)}<br>IQR: ${displayLogValue(group.q1)} – ${displayLogValue(group.q3)}`;
        }
      }
    }]
  };
}

function renderDistributionSummary(data: InsightsV1): void {
  const element = document.getElementById("lab-violin-summary-chart");
  if (!element) return;
  const colors = themeColors();
  const panels = data.violin_densities.panels;
  const allMedians = panels.flatMap((panel) => panel.groups.map((group) => group.median));
  getChart(element, "Medianas de avalúo por cuartil IGVUST y denominador").setOption({
    ...chartBase("Líneas de medianas por cuartil oficial IGVUST. El cambio de pendiente muestra cuánto se mueve la lectura al cambiar el denominador."),
    legend: { top: 0, textStyle: { color: colors.ink } },
    grid: { left: 92, right: 26, top: 54, bottom: 58 },
    xAxis: {
      type: "category",
      data: ["Q1 mayor", "Q2", "Q3", "Q4 menor"],
      name: "Cuartil nacional IGVUST oficial",
      nameLocation: "middle",
      nameGap: 34,
      axisLabel: { color: colors.muted },
      axisLine: { lineStyle: { color: colors.line } }
    },
    yAxis: {
      type: "value",
      min: Math.min(...allMedians),
      max: Math.max(...allMedians),
      name: "Mediana",
      axisLabel: { color: colors.muted, formatter: (value: number) => displayLogValue(value) },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.55 } }
    },
    series: panels.map((panel, index) => ({
      name: panel.title,
      type: "line" as const,
      smooth: false,
      symbolSize: 9,
      lineStyle: { width: 3 },
      itemStyle: { color: CHART_COLORS[index % CHART_COLORS.length] },
      data: panel.groups.map((group) => group.median)
    })),
    tooltip: {
      trigger: "axis",
      formatter: (params: unknown) => {
        const items = params as Array<{ seriesName: string; value: number; axisValue: string }>;
        const title = items[0]?.axisValue ?? "Cuartil";
        return `<strong>${escapeHtml(title)}</strong><br>${items.map((item) => `${escapeHtml(item.seriesName)}: ${displayLogValue(Number(item.value))}`).join("<br>")}`;
      }
    }
  }, true);
}

function renderViolins(data: InsightsV1): void {
  const host = document.getElementById("lab-violin-charts");
  if (!host) return;
  renderDistributionSummary(data);
  if (!host.children.length) {
    data.violin_densities.panels.forEach((panel, index) => {
      const article = makeElement("article", "lab-mini-chart");
      article.append(makeElement("h4", undefined, `${String.fromCharCode(65 + index)} · ${panel.title}`));
      const chart = makeElement("div", "lab-chart lab-violin-chart");
      chart.id = `lab-violin-${panel.id}`;
      article.append(chart, makeElement("p", "lab-chart-note", `${panel.universe} · n por cuartil visible en la tabla.`));
      host.append(article);
    });
  }
  data.violin_densities.panels.forEach((panel) => {
    const element = document.getElementById(`lab-violin-${panel.id}`);
    if (!element) return;
    getChart(element, panel.title).setOption(violinOption(panel), true);
  });
  replaceTable(
    "lab-distributions-table",
    ["Panel y cuartil", "n", "Q1", "Mediana", "Q3"],
    data.violin_densities.panels.flatMap((panel) => panel.groups.map((group) => [
      `${panel.title} · Q${group.quartile}`,
      integer.format(group.n),
      displayLogValue(group.q1),
      displayLogValue(group.median),
      displayLogValue(group.q3)
    ]))
  );
}

function heatmapColor(value: number, maximum: number): string {
  const ratio = maximum ? value / maximum : 0;
  if (ratio > 0.75) return "#ff4fd8";
  if (ratio > 0.5) return "#8c7cff";
  if (ratio > 0.25) return "#37e7ff";
  return "#31536b";
}

function renderTransition(data: InsightsV1): void {
  const element = document.getElementById("lab-transition-chart");
  if (!element) return;
  const colors = themeColors();
  const maximum = Math.max(...data.quartile_transition.matrix.flat());
  const cells = data.quartile_transition.matrix.flatMap((row, household) => row.map((value, m2) => ({
    value: [m2, household, value],
    itemStyle: { color: heatmapColor(value, maximum), decal: (household + m2) % 2 ? { symbol: "rect", dashArrayX: [1, 0], dashArrayY: [4, 3] } : undefined }
  })));
  getChart(element, "Matriz de transición desde cuartil de avalúo por hogar hacia cuartil por metro cuadrado").setOption({
    ...chartBase(`Matriz 4 por 4. ${formatter.format(data.quartile_transition.same_quartile_pct)} por ciento permanece en el mismo cuartil y ${formatter.format(data.quartile_transition.moved_two_plus_pct)} por ciento cambia dos o más.`),
    grid: { left: 84, right: 20, top: 24, bottom: 64 },
    xAxis: { type: "category", data: ["Q1", "Q2", "Q3", "Q4"], name: "Avalúo por m²", nameLocation: "middle", nameGap: 36, axisLabel: { color: colors.muted }, axisLine: { lineStyle: { color: colors.line } } },
    yAxis: { type: "category", data: ["Q1", "Q2", "Q3", "Q4"], inverse: true, name: "Avalúo por hogar", nameLocation: "middle", nameGap: 50, axisLabel: { color: colors.muted }, axisLine: { lineStyle: { color: colors.line } } },
    series: [{
      type: "heatmap",
      data: cells,
      label: { show: true, color: colors.ink, fontWeight: 800, formatter: (params: unknown) => integer.format(Number((params as { value: number[] }).value[2])) },
      emphasis: { itemStyle: { borderColor: colors.ink, borderWidth: 2 } },
      tooltip: { formatter: (params: unknown) => {
        const values = (params as { value: number[] }).value;
        return `Hogar Q${values[1] + 1} → m² Q${values[0] + 1}<br><strong>${integer.format(values[2])} UV</strong>`;
      } }
    }]
  }, true);
  replaceTable("lab-transition-table", ["Cuartil hogar → m²", "Q1", "Q2", "Q3", "Q4"], data.quartile_transition.matrix.map((row, index) => [`Q${index + 1}`, ...row.map(integer.format)]));
}

function renderSensitivityRows(rows: SensitivityRow[]): void {
  const element = document.getElementById("lab-sensitivity-chart");
  if (!element) return;
  const colors = themeColors();
  const labels = rows.map((row) => row.label);
  const connectors = rows.map((row, index) => [index, row.pearson, row.spearman]);
  getChart(element, "Comparación pareada de correlaciones Pearson y Spearman según denominador y universo").setOption({
    ...chartBase("Cada fila compara Pearson y Spearman. La cercanía de ambos puntos evalúa robustez a rangos, no causalidad."),
    legend: { top: 0, textStyle: { color: colors.ink }, data: ["Pearson", "Spearman"] },
    grid: { left: 164, right: 28, top: 52, bottom: 48 },
    xAxis: { type: "value", min: -1, max: 1, name: "Correlación", nameLocation: "middle", nameGap: 30, axisLabel: { color: colors.muted }, splitLine: { lineStyle: { color: colors.line } } },
    yAxis: { type: "category", data: labels, inverse: true, axisLabel: { color: colors.muted, width: 142, overflow: "truncate" }, axisLine: { lineStyle: { color: colors.line } } },
    series: [
      {
        type: "custom",
        silent: true,
        data: connectors,
        renderItem: (params: { dataIndex: number }, api: { coord: (value: number[]) => number[] }) => {
          const row = rows[params.dataIndex];
          const first = api.coord([row.pearson, params.dataIndex]);
          const second = api.coord([row.spearman, params.dataIndex]);
          return { type: "line", shape: { x1: first[0], y1: first[1], x2: second[0], y2: second[1] }, style: { stroke: colors.muted, lineWidth: 2, opacity: 0.65 } };
        }
      },
      { name: "Pearson", type: "scatter", symbolSize: 13, data: rows.map((row, index) => [row.pearson, index, row.n, row.universe]), itemStyle: { color: CHART_COLORS[0] } },
      { name: "Spearman", type: "scatter", symbolSize: 13, data: rows.map((row, index) => [row.spearman, index, row.n, row.universe]), itemStyle: { color: CHART_COLORS[1], decal: { symbol: "circle", dashArrayX: [1, 2], dashArrayY: [2, 2] } } }
    ],
    tooltip: { formatter: (params: unknown) => {
      const item = params as { seriesName?: string; value?: Array<number | string> };
      return `${escapeHtml(item.seriesName)}: <strong>${formatter.format(Number(item.value?.[0]))}</strong><br>n = ${integer.format(Number(item.value?.[2]))}<br>${escapeHtml(item.value?.[3])}`;
    } }
  }, true);
  replaceTable("lab-sensitivity-table", ["Indicador", "n", "Pearson", "Spearman", "Universo"], rows.map((row) => [row.label, integer.format(row.n), formatter.format(row.pearson), formatter.format(row.spearman), row.universe]));
}

function communeMetricValue(commune: CommuneInsight, metric: BubbleMetric): number | null {
  return commune[metric];
}

function metricValue(record: RankingRecord, metric: BubbleMetric): number | null {
  return record.metrics[metric];
}

function territoryRecords(communes: CommuneInsight[], unit: RankingUnit): RankingRecord[] {
  return unit === "regions" ? regionRankings(communes) : communeRankings(communes);
}

function selectedCommune(communes: CommuneInsight[], code: string | null): CommuneInsight | null {
  return code ? communes.find((commune) => commune.code === code) ?? null : null;
}

function applySelectedTerritoryFilter(
  records: RankingRecord[],
  unit: RankingUnit,
  selected: CommuneInsight | null,
  selectedRegionName: string | null,
  enabled: boolean
): RankingRecord[] {
  if (!enabled) return records;
  if (selected) {
    return unit === "regions"
      ? records.filter((record) => record.region === selected.region)
      : records.filter((record) => record.id === selected.code);
  }
  if (selectedRegionName) return records.filter((record) => record.region === selectedRegionName);
  return records;
}

function updateCommuneFilterNote(
  communes: CommuneInsight[],
  unit: RankingUnit,
  selectedCode: string | null,
  selectedRegionName: string | null,
  enabled: boolean
): void {
  const note = document.getElementById("lab-commune-filter-note");
  const reset = document.getElementById("lab-commune-reset");
  if (!note) return;
  const selected = selectedCommune(communes, selectedCode);
  const hasFilter = Boolean(selected || selectedRegionName);
  if (reset instanceof HTMLButtonElement) reset.disabled = !enabled || !hasFilter;
  if (!hasFilter) {
    note.textContent = "Sin filtro territorial activo; se muestran todos los territorios disponibles.";
    return;
  }
  if (!enabled) {
    const label = selected ? `${selected.name}, ${selected.region}` : selectedRegionName;
    note.textContent = `Filtro superior disponible: ${label}. Reset aplicado: el ranking vuelve al país completo.`;
    return;
  }
  if (!selected && selectedRegionName) {
    note.textContent = unit === "regions"
      ? `Filtro superior activo: ${selectedRegionName}. La vista regional muestra esa región.`
      : `Filtro superior activo: ${selectedRegionName}. La tabla y el gráfico muestran comunas de esa región.`;
    return;
  }
  if (!selected) return;
  note.textContent = unit === "regions"
    ? `Filtro superior activo: ${selected.name}. La vista regional queda limitada a ${selected.region}.`
    : `Filtro superior activo: ${selected.name}, ${selected.region}. La tabla y el gráfico muestran esa comuna.`;
}

function renderCommunes(
  communes: CommuneInsight[],
  metric: BubbleMetric,
  rankingUnit: RankingUnit,
  urbanOnly: boolean,
  query: string,
  selectedCode: string | null,
  selectedRegionName: string | null,
  selectedFilterEnabled: boolean
): void {
  const element = document.getElementById("lab-communes-chart");
  const status = document.getElementById("lab-communes-status");
  if (!element) return;
  const colors = themeColors();
  const normalizedQuery = query.trim().toLocaleLowerCase("es-CL");
  const allRanked = territoryRecords(communes, rankingUnit);
  const selected = selectedCommune(communes, selectedCode);
  const effectiveRegionName = selected?.region ?? selectedRegionName;
  const eligible = applySelectedTerritoryFilter(allRanked, rankingUnit, selected, effectiveRegionName, selectedFilterEnabled).filter((record) => {
    const value = metricValue(record, metric);
    return value != null && value > 0 && record.households > 0 && (!urbanOnly || (record.urban_pct ?? 0) > 50);
  });
  const seriesKeys = rankingUnit === "regions"
    ? ["Regiones"]
    : [...new Set(eligible.map((record) => record.region))].sort((a, b) => a.localeCompare(b, "es"));
  const maximumHouseholds = Math.max(...eligible.map((record) => record.households), 1);
  const size = (value: number) => 5 + 25 * Math.sqrt(value / maximumHouseholds);
  const matches = (record: RankingRecord) => !normalizedQuery || `${record.name} ${record.region}`.toLocaleLowerCase("es-CL").includes(normalizedQuery);
  const unitPlural = rankingUnit === "regions" ? "regiones" : "comunas";
  const maxRank = Math.max(...allRanked.map((record) => record.rank), 1);
  const series = seriesKeys.map((key, keyIndex) => ({
    name: key,
    type: "scatter" as const,
    symbolSize: (value: number[]) => size(value[2]),
    data: eligible.filter((record) => rankingUnit === "regions" || record.region === key).map((record) => ({
      name: record.name,
      value: [record.rank, metricValue(record, metric), record.households, record.vulnerability, record.urban_pct, record.id, record.members],
      itemStyle: { opacity: matches(record) ? 0.84 : 0.12, color: CHART_COLORS[keyIndex % CHART_COLORS.length] }
    })),
    emphasis: { focus: "series", itemStyle: { opacity: 1, borderColor: colors.ink, borderWidth: 2 } }
  }));
  const xLabel = `Ranking nacional IGVUST (1 = mayor vulnerabilidad relativa)`;
  getChart(element, `Burbujas de ${eligible.length} ${unitPlural}: avalúo ${METRICS[metric].short} por ranking nacional IGVUST; tamaño por hogares RSH`).setOption({
    ...chartBase(`Gráfico descriptivo. El eje horizontal es ranking nacional IGVUST, el vertical ${METRICS[metric].label}, el área hogares RSH y el color región cuando la unidad es comuna.`),
    legend: { type: "scroll", bottom: 0, textStyle: { color: colors.muted }, pageTextStyle: { color: colors.muted }, show: rankingUnit === "communes" },
    grid: { left: 78, right: 22, top: 22, bottom: 92 },
    xAxis: {
      type: "value",
      min: 1,
      max: maxRank,
      name: xLabel,
      nameLocation: "middle",
      nameGap: 32,
      axisLabel: { color: colors.muted, formatter: (value: number) => integer.format(value) },
      splitLine: { lineStyle: { color: colors.line } }
    },
    yAxis: { type: "log", name: METRICS[metric].label, axisLabel: { color: colors.muted, formatter: (value: number) => value >= 1_000_000_000 ? `${formatter.format(value / 1_000_000_000)} MM` : value >= 1_000_000 ? `${formatter.format(value / 1_000_000)} M` : integer.format(value) }, splitLine: { lineStyle: { color: colors.line } } },
    dataZoom: [{ type: "inside", xAxisIndex: 0, filterMode: "none" }],
    series,
    tooltip: { formatter: (params: unknown) => {
      const item = params as { name?: string; seriesName?: string; value?: Array<number | string> };
      const unit = rankingUnit === "regions" ? `${integer.format(Number(item.value?.[6]))} comunas` : escapeHtml(item.seriesName);
      return `<strong>${escapeHtml(item.name)}</strong> · ${unit}<br>Rank IGVUST: <strong>${integer.format(Number(item.value?.[0]))}</strong> de ${integer.format(maxRank)}<br>Indicador IGVUST de ordenamiento: ${formatter.format(Number(item.value?.[3]))}<br>${escapeHtml(METRICS[metric].label)}: ${currency.format(Number(item.value?.[1]))}<br>Hogares RSH: ${integer.format(Number(item.value?.[2]))}<br>Urbano: ${formatter.format(Number(item.value?.[4]))}%`;
    } }
  }, true);
  updateCommuneFilterNote(communes, rankingUnit, selectedCode, effectiveRegionName, selectedFilterEnabled);
  const selectedCopy = selectedFilterEnabled
    ? selected
      ? ` · filtrado por ${rankingUnit === "regions" ? selected.region : selected.name}`
      : effectiveRegionName
        ? ` · filtrado por ${effectiveRegionName}`
        : ""
    : "";
  const regionCaveat = rankingUnit === "regions" && metric !== "av_total" ? " · métricas regionales normalizadas ponderadas por hogares RSH" : "";
  if (status) status.textContent = `${eligible.length} ${unitPlural} con datos${urbanOnly ? " y más de 50% urbano" : ""}${normalizedQuery ? ` · ${eligible.filter(matches).length} coincidencias resaltadas` : ""}${selectedCopy}${regionCaveat}.`;
  const tableRows = eligible
    .filter(matches)
    .sort((a, b) => a.rank - b.rank)
    .map((record) => [integer.format(record.rank), record.name, record.region, currency.format(metricValue(record, metric) ?? 0), integer.format(record.households), `${formatter.format(record.urban_pct ?? 0)}%`]);
  replaceTable("lab-communes-table", ["Rank IGVUST", "Territorio", "Región", METRICS[metric].label, "Hogares RSH", "% urbano"], tableRows);
}

export class DenominatorLaboratory {
  private result: InsightsLoadResult | null = null;
  private activeView: LaboratoryView;
  private rendered = new Set<LaboratoryView>();
  private bubbleMetric: BubbleMetric = "av_total";
  private rankingUnit: RankingUnit = "communes";
  private urbanOnly = false;
  private query = "";
  private selectedCommuneCode: string | null = toDataCommuneCode(new URLSearchParams(window.location.search).get("comuna"));
  private selectedRegionName: string | null = null;
  private selectedFilterEnabled = Boolean(this.selectedCommuneCode);

  constructor(private readonly host: HTMLElement) {
    const requested = visualizationViewFromUrl();
    this.activeView = isLaboratoryView(requested) ? requested : "flujo";
  }

  async mount(): Promise<void> {
    this.bindTabs();
    this.bindCommuneControls();
    this.activate(this.activeView, false);
    this.setStatus("Cargando el artefacto analítico agregado…");
    try {
      this.result = await loadInsights();
      this.host.dataset.state = this.result.source === "v1" ? "ready" : "partial";
      this.setStatus(this.result.warning ?? `Artefacto v1 listo: ${integer.format(this.result.data.universe.uv)} UV y ${integer.format(this.result.communes.length)} comunas.`);
      this.rendered.clear();
      this.renderActive();
    } catch (error) {
      this.host.dataset.state = "error";
      this.setStatus(`No fue posible cargar el laboratorio: ${error instanceof Error ? error.message : "error inesperado"}. El mapa y las métricas comunales siguen disponibles.`);
    }
    window.addEventListener("catastro:theme", () => {
      this.rendered.clear();
      this.renderActive();
    });
    window.addEventListener("catastro:selection", (event) => {
      const row = (event as CustomEvent<{ row?: { codigo_comuna?: string; region?: string } }>).detail?.row;
      const code = toDataCommuneCode(row?.codigo_comuna ?? null);
      if (!code) return;
      this.selectedCommuneCode = code;
      this.selectedRegionName = typeof row?.region === "string" ? row.region : this.selectedRegionName;
      this.selectedFilterEnabled = true;
      this.rendered.delete("comunas");
      this.renderCommunes();
    });
    window.addEventListener("catastro:region-selection", (event) => {
      const detail = (event as CustomEvent<{ region?: string | null; communeCode?: string | null }>).detail;
      const regionName = typeof detail?.region === "string" && detail.region.trim() ? detail.region.trim() : null;
      const communeCode = toDataCommuneCode(detail?.communeCode ?? null);
      this.selectedRegionName = regionName;
      if (communeCode) this.selectedCommuneCode = communeCode;
      else if (!regionName) this.selectedCommuneCode = null;
      this.selectedFilterEnabled = Boolean(regionName || communeCode);
      this.rendered.delete("comunas");
      this.renderCommunes();
    });
    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(() => {
        this.host.querySelectorAll<HTMLElement>(".lab-chart").forEach((element) => echarts.getInstanceByDom(element)?.resize());
      });
      observer.observe(this.host);
    }
    if (isLaboratoryView(visualizationViewFromUrl())) {
      window.requestAnimationFrame(() => this.host.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "start" }));
    }
  }

  private bindTabs(): void {
    this.host.querySelectorAll<HTMLButtonElement>("[data-lab-tab]").forEach((tab) => {
      tab.addEventListener("click", () => {
        const view = tab.dataset.labTab as LaboratoryView;
        if (LAB_VIEWS.includes(view)) this.activate(view, true);
      });
      tab.addEventListener("keydown", (event) => {
        if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
        event.preventDefault();
        const current = LAB_VIEWS.indexOf(this.activeView);
        const next = event.key === "Home" ? 0 : event.key === "End" ? LAB_VIEWS.length - 1 : (current + (event.key === "ArrowRight" ? 1 : -1) + LAB_VIEWS.length) % LAB_VIEWS.length;
        this.activate(LAB_VIEWS[next], true);
        this.host.querySelector<HTMLButtonElement>(`[data-lab-tab="${LAB_VIEWS[next]}"]`)?.focus();
      });
    });
  }

  private bindCommuneControls(): void {
    const unit = document.getElementById("lab-ranking-unit");
    const metric = document.getElementById("lab-commune-metric");
    const universe = document.getElementById("lab-commune-universe");
    const search = document.getElementById("lab-commune-search");
    const reset = document.getElementById("lab-commune-reset");
    if (unit instanceof HTMLSelectElement) unit.addEventListener("change", () => {
      this.rankingUnit = unit.value === "regions" ? "regions" : "communes";
      this.renderCommunes();
    });
    if (metric instanceof HTMLSelectElement) metric.addEventListener("change", () => {
      this.bubbleMetric = metric.value as BubbleMetric;
      this.renderCommunes();
    });
    if (universe instanceof HTMLSelectElement) universe.addEventListener("change", () => {
      this.urbanOnly = universe.value === "urban";
      this.renderCommunes();
    });
    if (search instanceof HTMLInputElement) search.addEventListener("input", () => {
      this.query = search.value;
      this.renderCommunes();
    });
    if (reset instanceof HTMLButtonElement) reset.addEventListener("click", () => {
      this.selectedFilterEnabled = false;
      this.rendered.delete("comunas");
      this.renderCommunes();
    });
  }

  private activate(view: LaboratoryView, updateUrl: boolean): void {
    this.activeView = view;
    this.host.querySelectorAll<HTMLButtonElement>("[data-lab-tab]").forEach((tab) => {
      const selected = tab.dataset.labTab === view;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    this.host.querySelectorAll<HTMLElement>("[data-lab-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.labPanel !== view;
    });
    if (updateUrl) replaceVisualizationView(view);
    this.renderActive();
  }

  private renderActive(): void {
    if (!this.result || this.rendered.has(this.activeView)) {
      this.resizeActive();
      return;
    }
    if (this.activeView === "comunas") {
      this.renderCommunes();
      this.rendered.add("comunas");
      return;
    }
    const data = this.result.data;
    if (!data) {
      const panel = this.host.querySelector<HTMLElement>(`[data-lab-panel="${this.activeView}"] .lab-panel-message`);
      if (panel) panel.textContent = "Esta vista requiere insights-v1.json. Se mantiene disponible el explorador comunal parcial.";
      return;
    }
    if (this.activeView === "flujo") renderFlow(data);
    else if (this.activeView === "avaluos") renderAppraisals(data);
    else if (this.activeView === "distribuciones") renderViolins(data);
    else {
      renderTransition(data);
      renderSensitivityRows(data.sensitivity.rows);
    }
    this.rendered.add(this.activeView);
    this.resizeActive();
  }

  private renderCommunes(): void {
    if (!this.result) return;
    const metricSelect = document.getElementById("lab-commune-metric");
    const fallback = this.result.source === "legacy";
    if (metricSelect instanceof HTMLSelectElement) {
      for (const option of Array.from(metricSelect.options)) option.disabled = fallback && option.value !== "av_total";
      if (fallback) {
        this.bubbleMetric = "av_total";
        metricSelect.value = "av_total";
      }
    }
    renderCommunes(
      this.result.communes,
      this.bubbleMetric,
      this.rankingUnit,
      this.urbanOnly,
      this.query,
      this.selectedCommuneCode,
      this.selectedRegionName,
      this.selectedFilterEnabled
    );
  }

  private resizeActive(): void {
    this.host.querySelectorAll<HTMLElement>(`[data-lab-panel="${this.activeView}"] .lab-chart`).forEach((element) => echarts.getInstanceByDom(element)?.resize());
  }

  private setStatus(message: string): void {
    const status = document.getElementById("lab-status");
    if (status) status.textContent = message;
  }
}

export async function mountDenominatorLaboratory(): Promise<void> {
  const host = document.getElementById("denominator-lab");
  if (!host) return;
  const laboratory = new DenominatorLaboratory(host);
  await laboratory.mount();
}
