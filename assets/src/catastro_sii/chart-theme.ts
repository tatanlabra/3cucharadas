import * as echarts from "echarts/core";
import type { ECharts, EChartsCoreOption } from "echarts/core";

/** Utilidades de gráficos echarts compartidas por todos los módulos analíticos del
 * visor (laboratorio nacional y teaser de cobertura). Deliberadamente sólo importa
 * "echarts/core": no registra tipos de gráfico ni componentes pesados, así un módulo
 * que sólo necesita, por ejemplo, ScatterChart no arrastra Sankey/Heatmap/Custom al
 * cargar perezosamente. Cada módulo consumidor sigue llamando su propio
 * `echarts.use([...])` con sólo lo que realmente usa. */

// Una clave estable por región: no se reciclan colores dentro de las 16 regiones.
export const CHART_COLORS = [
  "#37e7ff", "#b8ff3c", "#ff4fd8", "#ffd166",
  "#8c7cff", "#62d6a6", "#ff7d66", "#60a5fa",
  "#19c3b1", "#ef5f75", "#b58cff", "#8bd346",
  "#f7a35c", "#4cc9f0", "#e76fbd", "#7f91a8"
];

export const formatter = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 2 });
export const integer = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
export const currency = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 });
const currencySmall = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 2 });

export function finiteNumber(value: number | null | undefined): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

export function themeColors(): { ink: string; muted: string; line: string; surface: string; dark: boolean } {
  const styles = getComputedStyle(document.documentElement);
  return {
    ink: styles.getPropertyValue("--ink").trim() || "#f3f5f8",
    muted: styles.getPropertyValue("--muted").trim() || "#a9afbd",
    line: styles.getPropertyValue("--line").trim() || "#2a3041",
    surface: styles.getPropertyValue("--surface").trim() || "#10121d",
    dark: document.documentElement.dataset.theme !== "light"
  };
}

export function reducedMotion(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function escapeHtml(value: unknown): string {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function chartBase(ariaDescription: string): EChartsCoreOption {
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

export function getChart(element: HTMLElement, label: string): ECharts {
  const existing = echarts.getInstanceByDom(element);
  element.setAttribute("role", "img");
  element.setAttribute("aria-label", label);
  return existing ?? echarts.init(element, undefined, { renderer: "svg" });
}

/** Enciende o apaga la leyenda completa de una instancia ya montada.
 *
 * ECharts 6.1 registra `legendAllSelect` y `legendInverseSelect` (ver
 * `component/legend/legendAction.js`). El handler consulta
 * `ecModel.eachComponent({ mainType: "legend", query: payload })`, y con un payload
 * sin `legendIndex`/`legendId`/`legendName` la query queda vacía: `queryComponents`
 * devuelve entonces *todos* los componentes `legend` del option. Por eso un único
 * dispatch alcanza a los cuatro `legend` con que el teaser arma su grilla 4×4 y no
 * hace falta iterar por índice.
 *
 * Para vaciar la leyenda se encadenan las dos acciones. `legendInverseSelect` sólo
 * invierte: sobre un estado mixto encendería lo que estaba apagado en vez de apagarlo
 * todo. Pasar antes por `legendAllSelect` uniforma el estado y la inversión lo apaga
 * entero, en dos dispatches en vez de un `legendUnSelect` por región. */
export function setLegendSelection(chart: ECharts, selectAll: boolean): void {
  chart.dispatchAction({ type: "legendAllSelect" });
  if (!selectAll) chart.dispatchAction({ type: "legendInverseSelect" });
}

/** Enlaza el par de botones «Seleccionar todas» / «Deseleccionar todas» al gráfico
 * del contenedor indicado. La instancia se resuelve dentro del click, no al enlazar:
 * ambos gráficos rehacen su option con `setOption(..., true)` en cada re-render y el
 * enlace ocurre una sola vez. */
export function bindLegendSelectionControls(chartElementId: string, allButtonId: string, noneButtonId: string): void {
  const element = document.getElementById(chartElementId);
  if (!element) return;
  const controls: Array<[string, boolean]> = [[allButtonId, true], [noneButtonId, false]];
  for (const [buttonId, selectAll] of controls) {
    const button = document.getElementById(buttonId);
    if (!(button instanceof HTMLButtonElement)) continue;
    button.addEventListener("click", () => {
      const chart = echarts.getInstanceByDom(element);
      if (chart) setLegendSelection(chart, selectAll);
    });
  }
}

export function makeElement<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text != null) element.textContent = text;
  return element;
}

export function replaceTable(hostId: string, headers: string[], rows: Array<Array<string | number>>): void {
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

export function logAxisBounds(values: Array<number | null | undefined>): { min: number; max: number } | Record<string, never> {
  const positives = values.filter((value): value is number => finiteNumber(value) && value > 0);
  if (!positives.length) return {};
  let minExponent = Math.floor(Math.log10(Math.min(...positives)));
  let maxExponent = Math.ceil(Math.log10(Math.max(...positives)));
  if (minExponent === maxExponent) {
    minExponent -= 1;
    maxExponent += 1;
  }
  return { min: 10 ** minExponent, max: 10 ** maxExponent };
}

/** Avalúos grandes en millones de CLP, con el mismo criterio ya usado en las tablas
 * publicadas del blog (ej. "Avalúo/hogar mediano (millones CLP)" en el post de
 * avalúo-vulnerabilidad): separador de miles es-CL, sin decimales, sufijo explícito.
 * No reemplaza formatCurrencyTick (ejes, con "mil millones"/"billones") ni
 * currencySmall (montos menores a $100). */
export function formatMillonesClp(value: number): string {
  if (!Number.isFinite(value)) return "";
  return `$${integer.format(Math.round(value / 1_000_000))} millones`;
}

export function formatCurrencyTick(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "";
  if (value >= 1_000_000_000_000) return `$${formatter.format(value / 1_000_000_000_000)} billones`;
  if (value >= 1_000_000_000) return `$${formatter.format(value / 1_000_000_000)} mil millones`;
  if (value >= 1_000_000) return `$${formatter.format(value / 1_000_000)} millones`;
  if (value >= 1_000) return `$${formatter.format(value / 1_000)} mil`;
  return value >= 100 ? currency.format(value) : currencySmall.format(value);
}

/** Orden geográfico norte→sur de las 16 regiones. Ordenar la leyenda
 * alfabéticamente rompe la intuición territorial: en un país de 4.300 km de largo
 * el lector espera recorrer el mapa, no el diccionario, y con orden alfabético
 * Arica queda junto a Aysén, que están a 3.700 km. */
export const REGIONS_NORTH_TO_SOUTH: readonly string[] = [
  "Arica y Parinacota",
  "Tarapacá",
  "Antofagasta",
  "Atacama",
  "Coquimbo",
  "Valparaíso",
  "Metropolitana de Santiago",
  "Libertador General Bernardo O'Higgins",
  "Maule",
  "Ñuble",
  "Biobío",
  "La Araucanía",
  "Los Ríos",
  "Los Lagos",
  "Aysén del General Carlos Ibáñez del Campo",
  "Magallanes y de la Antártica Chilena"
];

/** Cualquier región que no esté en la tabla va al final, en orden alfabético: un
 * nombre nuevo o distinto no debe desaparecer ni romper el orden del resto. */
export function sortRegionsNorthToSouth(regions: string[]): string[] {
  const rank = (name: string): number => {
    const index = REGIONS_NORTH_TO_SOUTH.indexOf(name);
    return index === -1 ? REGIONS_NORTH_TO_SOUTH.length : index;
  };
  return [...regions].sort((a, b) => rank(a) - rank(b) || a.localeCompare(b, "es"));
}

/** Reparte en `rows` filas lo más parejo posible: 16 en 3 filas da 6/5/5, no 6/6/4.
 * Filas desiguales al final se leen como si sobraran elementos. */
export function balancedRows<T>(items: T[], rows: number): T[][] {
  const groups: T[][] = [];
  let start = 0;
  for (let row = 0; row < rows && start < items.length; row += 1) {
    const size = Math.ceil((items.length - start) / (rows - row));
    groups.push(items.slice(start, start + size));
    start += size;
  }
  return groups;
}
