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
  balancedRows,
  bindLegendSelectionControls,
  chartBase,
  escapeHtml,
  finiteNumber,
  formatCurrencyTick,
  formatMillonesClp,
  getChart,
  integer,
  logAxisBounds,
  replaceTable,
  sortRegionsNorthToSouth,
  themeColors
} from "./chart-theme";
import { toDataCommuneCode } from "./state";
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
    const coverage = commune.cobertura_vivienda_pct;
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

/** Estado de resalte del chart. Espeja lo que el resto del visor ya entiende por
 * "selección": una comuna concreta, o sólo una región cuando el buscador quedó a
 * medio camino. El mismo criterio de atenuación que usa `renderCommunes` en
 * analytics.ts (0.78 normal / 0.12 apagado), pero disparado por territorio en vez
 * de por texto de búsqueda. */
export interface GhostState {
  activeCode: string | null;
  activeRegion: string | null;
}

export function ghostStyleFor(
  point: { code: string; region: string },
  ghost: GhostState
): { opacity: number; highlight: boolean } {
  if (ghost.activeCode) {
    return point.code === ghost.activeCode
      ? { opacity: 1, highlight: true }
      : { opacity: 0.12, highlight: false };
  }
  if (ghost.activeRegion) {
    return point.region === ghost.activeRegion
      ? { opacity: 0.78, highlight: false }
      : { opacity: 0.12, highlight: false };
  }
  return { opacity: 0.78, highlight: false };
}

let ghostState: GhostState = { activeCode: null, activeRegion: null };

/** El chart puede montarse después de que app.js ya resolvió una selección desde
 * `?comuna=`/`?region=`. Leer los `<select>` en el montaje evita que la primera
 * pintura salga sin ghost y salte al recibir el primer evento. */
function initialGhostState(): GhostState {
  const regionSelect = document.getElementById("region");
  const communeSelect = document.getElementById("comuna");
  const region = regionSelect instanceof HTMLSelectElement && regionSelect.value ? regionSelect.value : null;
  const code = communeSelect instanceof HTMLSelectElement ? toDataCommuneCode(communeSelect.value) : null;
  return { activeCode: code, activeRegion: region };
}

/** Mismo mecanismo real que usa el selector gráfico del mapa (ver `selectFromMap`
 * en app.ts / `selectCommune` en app.js): fijar `.value` de los `<select>` del
 * buscador principal y disparar `change` para que el resto del visor reaccione.
 * No se emite `catastro:selection` acá: ese evento lo dispara `selectCommune` en
 * app.js como consecuencia del `change`, y este módulo lo escucha para ghostear.
 * Emitirlo también desde aquí duplicaría el ciclo. Tampoco desplaza la página:
 * la selección debe sincronizar el visor sin sacar al lector de su posición. */
function selectCommuneInFinder(code: string, region: string): void {
  const regionSelect = document.getElementById("region");
  const communeSelect = document.getElementById("comuna");
  if (!(regionSelect instanceof HTMLSelectElement) || !(communeSelect instanceof HTMLSelectElement)) return;
  regionSelect.value = region;
  regionSelect.dispatchEvent(new Event("change", { bubbles: true }));
  communeSelect.value = code;
  communeSelect.dispatchEvent(new Event("change", { bubbles: true }));
}

interface ScatterDatum {
  name: string;
  code: string;
  region: string;
  coverageReal: number;
  value: [number, number, number];
  itemStyle: { color: string; opacity: number; borderColor?: string; borderWidth?: number };
}

/** Un componente `legend` de ECharts por fila (su `type: "plain"` no sabe hacer
 * grillas), repartidos en 3 filas balanceadas: 6/5/5. Con 4 filas la leyenda comía
 * ~160px del alto y aplastaba la grilla de burbujas. */
function legendRows(regions: string[]): string[][] {
  return balancedRows(regions, 3);
}

function chartOption(points: CoveragePoint[]): EChartsCoreOption {
  const colors = themeColors();
  const regions = sortRegionsNorthToSouth([...new Set(points.map((point) => point.region))]);
  const maximumHouseholds = Math.max(...points.map((point) => point.households), 1);
  const size = (value: number) => 6 + 26 * Math.sqrt(value / maximumHouseholds);
  const median = medianOf(points.map((point) => point.coverageReal));
  const lowest = lowestCoveragePoint(points);
  const mostTruncated = mostTruncatedPoint(points);
  const highlightCodes = new Set([lowest?.code, mostTruncated?.code].filter((code): code is string => Boolean(code)));
  const xLogBounds = logAxisBounds(points.map((point) => point.avaluoTotalClp));

  const series = regions.map((region, index) => {
    const regionPoints = points.filter((point) => point.region === region);
    const data: ScatterDatum[] = regionPoints.map((point) => {
      const ghost = ghostStyleFor(point, ghostState);
      return {
        name: point.name,
        code: point.code,
        region: point.region,
        coverageReal: point.coverageReal,
        value: [point.avaluoTotalClp, point.coverageDisplay, point.households],
        itemStyle: {
          color: CHART_COLORS[index % CHART_COLORS.length],
          opacity: ghost.opacity,
          ...(ghost.highlight ? { borderColor: colors.ink, borderWidth: 2 } : {})
        }
      };
    });
    const markPointData = regionPoints
      .filter((point) => highlightCodes.has(point.code))
      .map((point) => ({
        name: point.name,
        coord: [point.avaluoTotalClp, point.coverageDisplay],
        // colors.ink es un token de texto/foreground (casi blanco en tema oscuro,
        // casi negro en claro) — usarlo como relleno de ícono producía el "relleno
        // blanco" reportado. El relleno pasa a ser el mismo color de la región del
        // pin (ya usado en las burbujas y como borde acá antes), con el fondo del
        // chart como borde para separarlo de las burbujas de abajo.
        // El pin comparte la opacidad de su burbuja: si el chart quedó ghosteado por
        // una selección, un pin a opacidad plena se leería como si fuera lo resaltado.
        itemStyle: {
          color: CHART_COLORS[index % CHART_COLORS.length],
          borderColor: colors.surface,
          borderWidth: 2,
          opacity: ghostStyleFor(point, ghostState).opacity
        },
        // El pin de "más sobre el tope" cae en y=100, el máximo del eje: con la etiqueta
        // arriba queda cortada contra el borde del SVG. Cerca del tope se dibuja abajo.
        label: { formatter: point.name, position: point.coverageDisplay >= 88 ? "bottom" : "top" }
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
              // El label sale del ícono (a 44px no alcanza para nombres largos como
              // "Isla de Pascua" o "Chile Chico", y se cortaba sin wrap) y se dibuja
              // arriba del pin con el mismo tratamiento que ya usa el tooltip del
              // chart (chartBase(): fondo colors.surface, borde colors.line, texto
              // colors.ink), para que el contraste sea contra el fondo del chart,
              // no contra el color de relleno del pin.
              label: {
                position: "top",
                distance: 10,
                color: colors.ink,
                fontWeight: 800,
                fontSize: 11,
                backgroundColor: colors.surface,
                borderColor: colors.line,
                borderWidth: 1,
                borderRadius: 6,
                padding: [3, 7],
                overflow: "break",
                width: 120
              },
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

  const narrow = window.innerWidth < 640;
  const rows = legendRows(regions);
  const legendRowHeight = narrow ? 20 : 22;
  const legendBottomBase = 6;
  const legend = rows.map((rowData, rowIndex) => ({
    type: "plain" as const,
    orient: "horizontal" as const,
    data: rowData,
    left: "center" as const,
    bottom: legendBottomBase + (rows.length - 1 - rowIndex) * legendRowHeight,
    itemWidth: 14,
    itemHeight: 10,
    itemGap: narrow ? 10 : 18,
    textStyle: { color: colors.muted, fontSize: narrow ? 10 : 12 }
  }));
  const gridBottom = legendBottomBase + rows.length * legendRowHeight + 66;

  return {
    ...chartBase(
      `Dispersión de ${points.length} comunas: avalúo fiscal total en escala log10 en el eje horizontal y cobertura residencial frente a las viviendas particulares totales del Censo 2024, con tope en 100%, en el eje vertical. El tamaño de la burbuja usa hogares del Censo 2024 y el color agrupa por región. Una línea punteada marca la mediana nacional de cobertura; dos burbujas destacadas muestran la comuna con menor cobertura y la comuna cuyo valor real supera más el tope de 100%.`
    ),
    legend,
    grid: { left: 64, right: 26, top: 40, bottom: gridBottom },
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
      // Partido en 2 líneas + fontSize chico: con nameLocation:"middle" en un eje Y,
      // ECharts rota el nombre 90°, así que su extensión corre a lo largo del eje
      // (vertical), no del ancho del chart. Una sola línea de 65 caracteres a
      // fontSize 12 pedía ~450px verticales contra los ~230px que deja esta grilla
      // (chart de 430px, top:40, bottom:~160 por la leyenda 4×4) y se recortaba
      // contra el borde del SVG o se montaba sobre la leyenda. Con 2 líneas de
      // máx. 34 caracteres a fontSize 10 baja a ~200px y cabe sin tocar `grid`.
      name: "Cobertura residencial frente a\nviviendas Censo 2024 (%, tope 100)",
      nameLocation: "middle",
      nameGap: 44,
      nameRotate: 90,
      nameTextStyle: { fontSize: 10, lineHeight: 12 },
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
        return `<strong>${escapeHtml(name)}</strong> · ${escapeHtml(region)}<br>Avalúo fiscal total: ${formatMillonesClp(value[0])}<br>Cobertura residencial: ${integer.format(Math.min(coverageReal, 100))}%${truncatedNote}<br>Hogares Censo 2024: ${integer.format(value[2])}`;
      }
    }
  };
}

function renderChart(points: CoveragePoint[]): ECharts {
  const element = document.getElementById("coverage-teaser-chart");
  if (!element) throw new Error("contenedor del gráfico introductorio ausente");
  const chart = getChart(element, `Dispersión introductoria de ${points.length} comunas: avalúo fiscal total frente a cobertura residencial`);
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
      formatMillonesClp(point.avaluoTotalClp),
      `${integer.format(point.coverageReal)}%${point.truncated ? " (recortado a 100% en el gráfico)" : ""}`,
      integer.format(point.households)
    ]);
  replaceTable("coverage-teaser-table", ["Comuna", "Región", "Avalúo fiscal total (millones CLP)", "Cobertura residencial", "Hogares Censo 2024"], rows);
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
    ghostState = initialGhostState();
    renderChart(points);
    renderTable(points);
    // Los atajos de leyenda nacen `hidden` en el marcado: sin bundle o sin datos no
    // controlan nada, así que sólo aparecen cuando ya hay un chart montado.
    const legendControls = document.getElementById("coverage-teaser-legend-controls");
    if (legendControls) legendControls.hidden = false;
    bindLegendSelectionControls("coverage-teaser-chart", "coverage-teaser-legend-all", "coverage-teaser-legend-none");
    const truncatedCount = points.filter((point) => point.truncated).length;
    setStatus(`${integer.format(points.length)} comunas con avalúo fiscal registrado${truncatedCount ? ` · ${integer.format(truncatedCount)} superan 100% de cobertura y se muestran recortadas en el eje vertical, aunque el valor real sigue disponible en el tooltip` : ""}. Haz clic en una burbuja para cargarla abajo, o revisa primero la tabla completa.`);
  } catch (error) {
    setStatus(`No fue posible cargar este gráfico introductorio: ${error instanceof Error ? error.message : "error inesperado"}. El resto del visor sigue disponible con normalidad.`);
    return;
  }
  window.addEventListener("catastro:theme", () => {
    if (cachedPoints) renderChart(cachedPoints);
  });
  // Mismos dos eventos que ya consumen app.ts y analytics.ts: `catastro:selection`
  // cuando hay comuna resuelta, `catastro:region-selection` cuando el buscador
  // quedó en región (o volvió a nacional).
  window.addEventListener("catastro:selection", (event) => {
    const row = (event as CustomEvent<{ row?: CommuneRecord }>).detail?.row;
    if (!row) return;
    ghostState = { activeCode: row.codigo_comuna, activeRegion: row.region };
    if (cachedPoints) renderChart(cachedPoints);
  });
  window.addEventListener("catastro:region-selection", (event) => {
    const detail = (event as CustomEvent<{ region?: string | null; communeCode?: string | null }>).detail;
    const regionName = typeof detail?.region === "string" && detail.region.trim() ? detail.region.trim() : null;
    ghostState = { activeCode: toDataCommuneCode(detail?.communeCode ?? null), activeRegion: regionName };
    if (cachedPoints) renderChart(cachedPoints);
  });
  let lastNarrow = window.innerWidth < 640;
  window.addEventListener("resize", () => {
    const narrow = window.innerWidth < 640;
    if (narrow !== lastNarrow && cachedPoints) {
      // La grilla 4×4 se mantiene en todos los anchos, pero el tamaño de fuente e
      // itemGap del legend se ajustan al cruzar el breakpoint móvil, así que hay que
      // reconstruir el option completo, no sólo redimensionar el lienzo existente.
      lastNarrow = narrow;
      renderChart(cachedPoints);
      return;
    }
    const element = document.getElementById("coverage-teaser-chart");
    if (element) echarts.getInstanceByDom(element)?.resize();
  });
}
