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

export function formatCurrencyTick(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "";
  if (value >= 1_000_000_000_000) return `$${formatter.format(value / 1_000_000_000_000)} billones`;
  if (value >= 1_000_000_000) return `$${formatter.format(value / 1_000_000_000)} mil millones`;
  if (value >= 1_000_000) return `$${formatter.format(value / 1_000_000)} millones`;
  if (value >= 1_000) return `$${formatter.format(value / 1_000)} mil`;
  return value >= 100 ? currency.format(value) : currencySmall.format(value);
}
