import * as echarts from "echarts/core";
import { ScatterChart } from "echarts/charts";
import {
  AriaComponent,
  DatasetComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TooltipComponent
} from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import type { ECharts, EChartsCoreOption } from "echarts/core";
import {
  CHART_COLORS,
  chartBase,
  currency,
  escapeHtml,
  finiteNumber,
  formatCurrencyTick,
  getChart,
  integer,
  logAxisBounds,
  reducedMotion,
  replaceTable,
  themeColors
} from "./chart-theme";
import type { CommuneRecord } from "./types";

const communesUrl = "/catastro_sii_brecha/data/comunas.json";

echarts.use([
  SVGRenderer,
  ScatterChart,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  AriaComponent,
  MarkPointComponent,
  MarkLineComponent
]);

export interface CoveragePoint {
  code: string;
  name: string;
  region: string;
  avaluoTotalClp: number;
  coverageDisplay: number;
  coverageReal: number;
  households: number;
  truncated: boolean;
}

/** Sólo comunas con avalúo fiscal positivo entran al eje log10; la cobertura se
 * recorta en 100 para el eje pero el valor real siempre viaja en el punto (tooltip
 * y tabla lo muestran sin recortar). */
export function buildCoveragePoints(communes: CommuneRecord[]): CoveragePoint[] {
  return communes.reduce<CoveragePoint[]>((points, commune) => {
    const avaluo = commune.avaluo_total_clp;
    const coverage = commune.cobertura_censo_pct;
    if (!finiteNumber(avaluo) || avaluo <= 0 || !finiteNumber(coverage)) return points;
    points.push({
      code: commune.codigo_comuna,
      name: commune.comuna,
      region: commune.region,
      avaluoTotalClp: avaluo,
      coverageDisplay: Math.min(coverage, 100),
      coverageReal: coverage,
      households: finiteNumber(commune.hogares_censo_2024) ? commune.hogares_censo_2024 : 0,
      truncated: coverage > 100
    });
    return points;
  }, []);
}

export function medianOf(values: number[]): number | null {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

export function lowestCoveragePoint(points: CoveragePoint[]): CoveragePoint | null {
  return points.reduce<CoveragePoint | null>((min, point) => (!min || point.coverageReal < min.coverageReal ? point : min), null);
}

export function mostTruncatedPoint(points: CoveragePoint[]): CoveragePoint | null {
  return points.reduce<CoveragePoint | null>((max, point) => (!max || point.coverageReal > max.coverageReal ? point : max), null);
}

async function json<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
  return response.json() as Promise<T>;
}

/** Mismo mecanismo real que usa el selector gráfico del mapa (ver `selectFromMap`
 * en app.ts / `selectCommune` en app.js): fijar `.value` de los `<select>` del
 * buscador principal y disparar `change` para que el resto del visor reaccione.
 * El evento `catastro:selection` no se usa como disparador porque nadie lo emite
 * desde este buscador. */
function selectCommuneInFinder(code: string, region: string): void {
  const regionSelect = document.getElementById("region");
  const communeSelect = document.getElementById("comuna");
  if (!(regionSelect instanceof HTMLSelectElement) || !(communeSelect instanceof HTMLSelectElement)) return;
  regionSelect.value = region;
  regionSelect.dispatchEvent(new Event("change", { bubbles: true }));
  communeSelect.value = code;
  communeSelect.dispatchEvent(new Event("change", { bubbles: true }));
  document.getElementById("explorar")?.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "start" });
}

interface ScatterDatum {
  name: string;
  code: string;
  region: string;
  coverageReal: number;
  value: [number, number, number];
  itemStyle: { color: string; opacity: number };
}

function chartOption(points: CoveragePoint[]): EChartsCoreOption {
  const colors = themeColors();
  const regions = [...new Set(points.map((point) => point.region))].sort((a, b) => a.localeCompare(b, "es"));
  const maximumHouseholds = Math.max(...points.map((point) => point.households), 1);
  const size = (value: number) => 6 + 26 * Math.sqrt(value / maximumHouseholds);
  const median = medianOf(points.map((point) => point.coverageReal));
  const lowest = lowestCoveragePoint(points);
  const mostTruncated = mostTruncatedPoint(points);
  const highlightCodes = new Set([lowest?.code, mostTruncated?.code].filter((code): code is string => Boolean(code)));
  const xLogBounds = logAxisBounds(points.map((point) => point.avaluoTotalClp));

  const series = regions.map((region, index) => {
    const regionPoints = points.filter((point) => point.region === region);
    const data: ScatterDatum[] = regionPoints.map((point) => ({
      name: point.name,
      code: point.code,
      region: point.region,
      coverageReal: point.coverageReal,
      value: [point.avaluoTotalClp, point.coverageDisplay, point.households],
      itemStyle: { color: CHART_COLORS[index % CHART_COLORS.length], opacity: 0.78 }
    }));
    const markPointData = regionPoints
      .filter((point) => highlightCodes.has(point.code))
      .map((point) => ({
        name: point.name,
        coord: [point.avaluoTotalClp, point.coverageDisplay],
        itemStyle: { color: colors.ink, borderColor: CHART_COLORS[index % CHART_COLORS.length], borderWidth: 2 },
        label: { formatter: point.name }
      }));
    return {
      name: region,
      type: "scatter" as const,
      symbolSize: (value: number[]) => size(value[2]),
      data,
      emphasis: { focus: "series", itemStyle: { opacity: 1, borderColor: colors.ink, borderWidth: 2 } },
      ...(markPointData.length
        ? {
            markPoint: {
              symbol: "pin",
              symbolSize: 44,
              data: markPointData,
              label: { color: "#10121d", fontWeight: 800, fontSize: 10 },
              tooltip: { show: false }
            }
          }
        : {}),
      ...(index === 0 && median != null
        ? {
            markLine: {
              symbol: "none",
              silent: true,
              lineStyle: { color: colors.muted, type: "dashed" as const, width: 1.4 },
              label: {
                formatter: `Mediana nacional: ${integer.format(median)}%`,
                color: colors.muted,
                position: "insideEndTop" as const
              },
              data: [{ yAxis: median }]
            }
          }
        : {})
    };
  });

  return {
    ...chartBase(
      `Dispersión de ${points.length} comunas: avalúo fiscal total en escala log10 en el eje horizontal y cobertura residencial equivalente frente al Censo 2024, con tope en 100%, en el eje vertical. El tamaño de la burbuja usa hogares del Censo 2024 y el color agrupa por región. Una línea punteada marca la mediana nacional de cobertura; dos burbujas destacadas muestran la comuna con menor cobertura y la comuna cuyo valor real supera más el tope de 100%.`
    ),
    legend: { type: "scroll", bottom: 0, textStyle: { color: colors.muted }, pageTextStyle: { color: colors.muted } },
    grid: { left: 64, right: 26, top: 40, bottom: 92 },
    xAxis: {
      type: "log",
      logBase: 10,
      name: "Avalúo fiscal total (log10; etiquetas CLP)",
      nameLocation: "middle",
      nameGap: 34,
      ...xLogBounds,
      axisLabel: { color: colors.muted, formatter: (value: number) => formatCurrencyTick(value) },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.6 } }
    },
    yAxis: {
      type: "value",
      min: 0,
      max: 100,
      name: "Cobertura censal equivalente (%, tope 100)",
      nameLocation: "middle",
      nameGap: 44,
      axisLabel: { color: colors.muted, formatter: (value: number) => `${integer.format(value)}%` },
      splitLine: { lineStyle: { color: colors.line, opacity: 0.55 } }
    },
    series,
    tooltip: {
      formatter: (params: unknown) => {
        const item = params as { componentType?: string; data?: ScatterDatum };
        if (item.componentType !== "series" || !item.data) return "";
        const { name, region, value, coverageReal } = item.data;
        const truncatedNote = coverageReal > 100
          ? `<br><em>Valor real ${integer.format(coverageReal)}%, recortado a 100% en el gráfico.</em>`
          : "";
        return `<strong>${escapeHtml(name)}</strong> · ${escapeHtml(region)}<br>Avalúo fiscal total: ${currency.format(value[0])}<br>Cobertura equivalente: ${integer.format(Math.min(coverageReal, 100))}%${truncatedNote}<br>Hogares Censo 2024: ${integer.format(value[2])}`;
      }
    }
  };
}

function renderChart(points: CoveragePoint[]): ECharts {
  const element = document.getElementById("coverage-teaser-chart");
  if (!element) throw new Error("contenedor del gráfico introductorio ausente");
  const chart = getChart(element, `Dispersión introductoria de ${points.length} comunas: avalúo fiscal total frente a cobertura censal equivalente`);
  chart.setOption(chartOption(points), true);
  chart.off("click");
  chart.on("click", (params: unknown) => {
    const item = params as { componentType?: string; seriesType?: string; data?: ScatterDatum };
    if (item.componentType !== "series" || item.seriesType !== "scatter" || !item.data) return;
    selectCommuneInFinder(item.data.code, item.data.region);
  });
  return chart;
}

function renderTable(points: CoveragePoint[]): void {
  const rows = points
    .slice()
    .sort((a, b) => a.coverageReal - b.coverageReal)
    .map((point) => [
      point.name,
      point.region,
      currency.format(point.avaluoTotalClp),
      `${integer.format(point.coverageReal)}%${point.truncated ? " (recortado a 100% en el gráfico)" : ""}`,
      integer.format(point.households)
    ]);
  replaceTable("coverage-teaser-table", ["Comuna", "Región", "Avalúo fiscal total", "Cobertura equivalente", "Hogares Censo 2024"], rows);
}

let cachedPoints: CoveragePoint[] | null = null;

function setStatus(message: string): void {
  const status = document.getElementById("coverage-teaser-status");
  if (status) status.textContent = message;
}

export async function mountCoverageTeaser(): Promise<void> {
  const container = document.getElementById("coverage-teaser-chart");
  if (!container) return;
  setStatus("Cargando comunas…");
  try {
    const communes = await json<CommuneRecord[]>(communesUrl);
    const points = buildCoveragePoints(communes);
    if (!points.length) {
      setStatus("No hay datos comunales disponibles para este gráfico.");
      return;
    }
    cachedPoints = points;
    renderChart(points);
    renderTable(points);
    const truncatedCount = points.filter((point) => point.truncated).length;
    setStatus(`${integer.format(points.length)} comunas con avalúo fiscal registrado${truncatedCount ? ` · ${integer.format(truncatedCount)} superan 100% de cobertura y se muestran recortadas en el eje vertical, aunque el valor real sigue disponible en el tooltip` : ""}. Haz clic en una burbuja para cargarla abajo, o revisa primero la tabla completa.`);
  } catch (error) {
    setStatus(`No fue posible cargar este gráfico introductorio: ${error instanceof Error ? error.message : "error inesperado"}. El resto del visor sigue disponible con normalidad.`);
    return;
  }
  window.addEventListener("catastro:theme", () => {
    if (cachedPoints) renderChart(cachedPoints);
  });
  window.addEventListener("resize", () => {
    const element = document.getElementById("coverage-teaser-chart");
    if (element) echarts.getInstanceByDom(element)?.resize();
  });
}
