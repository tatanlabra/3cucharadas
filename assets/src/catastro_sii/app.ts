import "maplibre-gl/dist/maplibre-gl.css";
import { authorizedParcelSource, uvLayerAvailable, uvShardUrl } from "./availability";
import type { UvIndex } from "./availability";
import { MapController } from "./map";
import { manifestUrlsForLocation } from "./preview";
import { communeCityDefaultView, communeViewBounds, reconcileMapAvailability, regionCodeForName, replaceUrl, stateFromUrl, toDataCommuneCode } from "./state";
import type { AppState, Bounds, CommuneRecord, TilesManifest, UvFeatureProperties } from "./types";

const communesUrl = "/catastro_sii_brecha/data/comunas.json";
const uvIndexUrl = "/catastro_sii_brecha/data/uv/index.json";
const chileSelectorUrl = "/catastro_sii_brecha/data/chile-selector.json";
const SVG_NS = "http://www.w3.org/2000/svg";
const DEFAULT_COMMUNE_CODE = "3202";

type TerritoryIndex = { communes?: Record<string, { bounds?: [number, number, number, number] }> };
type ChileSelectorFeature = { code: string; comuna: string; region: string; d: string };
type ChileSelectorData = { viewBox: string; features: ChileSelectorFeature[] };

function setStatus(message: string): void {
  const element = document.getElementById("map-status");
  if (element) element.textContent = message;
}

function setBivariateStatus(message: string): void {
  const element = document.getElementById("bivariate-map-status");
  if (element) element.textContent = message;
}

function setBivariateSelectorStatus(message: string): void {
  const element = document.getElementById("bivariate-selector-status");
  if (element) element.textContent = message;
}

const UV_LEGEND_COPY: {
  title: string;
  axis: string;
  aria: string;
  note: string;
} = {
  title: "Avalúo por m² × vulnerabilidad",
  axis: "Mayor avalúo por m² →",
  aria: "Matriz de 12 combinaciones: tres tramos visuales de avalúo por metro cuadrado predial asignado en el eje horizontal y cuatro cuartiles nacionales oficiales de vulnerabilidad IGVUST en el vertical.",
  note: "Filas: cuartiles nacionales oficiales IGVUST sobre las 6.891 unidades vecinales, con q1 como mayor vulnerabilidad. Columnas: avalúo por m² compactado en bajo, medio y alto. La celda más oscura destaca alto avalúo unitario con mayor vulnerabilidad; no mide ingreso, riqueza ni precio de mercado."
};

function updateUvLegend(): void {
  const copy = UV_LEGEND_COPY;
  const title = document.getElementById("bivariate-uv-legend-title");
  const axis = document.getElementById("bivariate-uv-axis-x");
  const matrix = document.getElementById("bivariate-uv-matrix");
  const note = document.getElementById("bivariate-uv-legend-note");
  if (title) title.textContent = copy.title;
  if (axis) axis.textContent = copy.axis;
  if (matrix) matrix.setAttribute("aria-label", copy.aria);
  if (note) note.textContent = copy.note;
}

/** El pie declara "modo degradado" hasta que el fondo cartográfico carga de verdad.
 *  Si el mapa nunca monta, ese texto inicial sigue siendo la descripción correcta. */
function setAttribution(credit: string | undefined): void {
  const element = document.getElementById("attribution");
  if (element && credit) element.textContent = credit;
}

async function json<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
  return response.json() as Promise<T>;
}

async function firstJson<T>(urls: string[]): Promise<T> {
  let lastError: unknown;
  for (const url of urls) {
    try {
      return await json<T>(url);
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError instanceof Error ? lastError : new Error("No hay un manifest cartográfico disponible");
}

function finiteNumber(value: unknown): number | null {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

const integerFormatter = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
const percentFormatter = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 1 });
const currencyFormatter = new Intl.NumberFormat("es-CL", {
  maximumFractionDigits: 0,
  style: "currency",
  currency: "CLP"
});
const compactCurrencyFormatter = new Intl.NumberFormat("es-CL", {
  notation: "compact",
  compactDisplay: "short",
  maximumFractionDigits: 1,
  style: "currency",
  currency: "CLP"
});

function optionalNumber(value: unknown): number | null {
  if (value === null || value === undefined || value === "") return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function formatInteger(value: unknown): string {
  const number = optionalNumber(value);
  return number === null ? "No disponible" : integerFormatter.format(number);
}

function formatPercent(value: unknown): string {
  const number = optionalNumber(value);
  return number === null ? "No disponible" : `${percentFormatter.format(number)}%`;
}

function formatCurrency(value: unknown): string {
  const number = optionalNumber(value);
  return number === null ? "No disponible" : currencyFormatter.format(number);
}

function formatSquareMeters(value: unknown): string {
  const number = optionalNumber(value);
  return number === null ? "No disponible" : `${integerFormatter.format(number)} m²`;
}

type UvSummary = {
  classified: number;
  missing: number;
  vulnerableHighM2: number;
  vulnerableLowM2: number;
  lessVulnerableHighM2: number;
};

function summarizeUvFeatures(features: Array<{ properties?: Partial<UvFeatureProperties> }>): UvSummary {
  const summary: UvSummary = {
    classified: 0,
    missing: 0,
    vulnerableHighM2: 0,
    vulnerableLowM2: 0,
    lessVulnerableHighM2: 0
  };
  for (const feature of features) {
    const qv = finiteNumber(feature.properties?.qv);
    const qaM2 = finiteNumber(feature.properties?.qa_m2);
    if (!qv || !qaM2) {
      summary.missing += 1;
      continue;
    }
    summary.classified += 1;
    if (qv === 1 && qaM2 === 4) summary.vulnerableHighM2 += 1;
    if (qv === 1 && qaM2 === 1) summary.vulnerableLowM2 += 1;
    if (qv === 4 && qaM2 === 4) summary.lessVulnerableHighM2 += 1;
  }
  return summary;
}

function bivariateFinding(row: CommuneRecord, summary: UvSummary): string {
  if (!summary.classified) {
    return `${row.comuna}: el shard UV carga geometría, pero no trae suficientes celdas clasificadas para leer el bivariado. Revisa fuga territorial y denominadores antes de interpretar.`;
  }
  const total = integerFormatter.format(summary.classified);
  const focus = integerFormatter.format(summary.vulnerableHighM2);
  const low = integerFormatter.format(summary.vulnerableLowM2);
  const missing = summary.missing ? ` ${integerFormatter.format(summary.missing)} UV quedan sin celda por falta de cuartil o denominador.` : "";
  return `${row.comuna}: ${total} UV clasificadas. ${focus} combinan mayor vulnerabilidad IGVUST con alto avalúo fiscal por m²; ${low} combinan mayor vulnerabilidad con bajo avalúo por m².${missing} El color orienta la inspección, no certifica una explicación social.`;
}

async function uvSummaryFromUrl(url: string): Promise<UvSummary | null> {
  try {
    const payload = await json<{ features?: Array<{ properties?: Partial<UvFeatureProperties> }> }>(url);
    return summarizeUvFeatures(payload.features ?? []);
  } catch {
    return null;
  }
}

function uvHoverContent(properties: Record<string, unknown>): HTMLElement {
  const content = document.createElement("div");
  content.className = "uv-popup";
  const title = document.createElement("strong");
  const name = typeof properties.nombre === "string" && properties.nombre.trim()
    ? properties.nombre.trim()
    : `UV ${String(properties.uv ?? "sin nombre")}`;
  title.textContent = name;
  const qv = finiteNumber(properties.qv);
  const qaM2 = finiteNumber(properties.qa_m2);
  const avm2 = finiteNumber(properties.avm2);
  const households = finiteNumber(properties.hog);
  const population = finiteNumber(properties.pob);
  const rows = [
    `IGVUST: ${qv ? `q${qv}` : "sin cuartil"}`,
    `Avalúo/m²: ${qaM2 ? `q${qaM2}` : "sin cuartil"}${avm2 ? ` · ${compactCurrencyFormatter.format(avm2)}` : ""}`,
    `RSH: ${households ? `${integerFormatter.format(households)} hogares` : "hogares sin dato"} · ${population ? `${integerFormatter.format(population)} personas` : "personas sin dato"}`
  ];
  content.append(title);
  for (const row of rows) {
    const line = document.createElement("p");
    line.textContent = row;
    content.append(line);
  }
  return content;
}

export class CatastroMapApplication {
  private state: AppState;
  private map: MapController | null = null;
  private bivariateMap: MapController | null = null;
  private selectedRow: CommuneRecord | null = null;
  private selectedRegionName: string | null = null;

  private constructor(
    private readonly manifest: TilesManifest,
    private readonly rows: CommuneRecord[],
    uvIndex: UvIndex | null = null,
    private readonly chileSelector: ChileSelectorData | null = null
  ) {
    this.state = stateFromUrl(rows);
    this.uvIndex = uvIndex;
  }

  static async start(): Promise<CatastroMapApplication> {
    const manifestUrls = manifestUrlsForLocation(window.location.hostname, window.location.search);
    const [manifest, rows, chileSelector] = await Promise.all([
      firstJson<TilesManifest>(manifestUrls),
      json<CommuneRecord[]>(communesUrl),
      json<ChileSelectorData>(chileSelectorUrl).catch(() => null)
    ]);
    const territories: TerritoryIndex = manifest.communes.territories_url
      ? await json<TerritoryIndex>(manifest.communes.territories_url).catch(() => ({ communes: {} }))
      : { communes: {} };
    const boundsByCommune = territories.communes ?? {};
    const enriched = rows.map((row) => ({ ...row, bounds: boundsByCommune[row.codigo_comuna.padStart(5, "0")]?.bounds ?? null }));
    // El indice puede no existir todavia: la capa UV degrada a ausente, no a error.
    const uvIndex = await json<UvIndex>(uvIndexUrl).catch(() => null);
    return new CatastroMapApplication(manifest, enriched, uvIndex, chileSelector);
  }

  async mount(): Promise<void> {
    const container = document.getElementById("map");
    if (!container) return;
    container.classList.add("catastro-maplibre");
    this.map = await MapController.create(this.manifest, container);
    const mapShell = container.closest(".map-shell");
    mapShell?.classList.add("map-ready");
    setAttribution(this.manifest.basemap?.attribution);
    const legacyCanvas = document.getElementById("density");
    if (legacyCanvas instanceof HTMLCanvasElement) {
      legacyCanvas.style.setProperty("display", "none", "important");
      legacyCanvas.setAttribute("aria-hidden", "true");
    }
    const legacyNote = document.getElementById("map-note");
    if (legacyNote) legacyNote.style.setProperty("display", "none", "important");
    requestAnimationFrame(() => this.map?.resize());
    const communesAdded = this.map.addCommunes((code) => this.selectFromMap(code));
    this.map.bindUvHover(uvHoverContent);
    this.map.bindUvClick(uvHoverContent);
    this.bindMapTools();
    this.bindSelectionDock();
    await this.mountBivariateMap();
    if (communesAdded) setStatus("Capa comunal nacional lista. Elige una región o comuna para explorar.");
    else setStatus("La capa comunal PMTiles aún no está disponible en este manifest.");

    window.addEventListener("catastro:selection", (event) => {
      const row = (event as CustomEvent<{ row?: CommuneRecord }>).detail?.row;
      if (row) {
        const isInitialUrlSelection = this.selectedRow === null && this.state.communeCode === row.codigo_comuna;
        this.selectRow(row, !isInitialUrlSelection);
      }
    });
    window.addEventListener("catastro:legacy-ready", (event) => {
      const row = (event as CustomEvent<{ selected?: CommuneRecord }>).detail?.selected;
      if (row) this.selectRow(row);
    });
    window.addEventListener("resize", () => this.map?.resize());
    this.applyInitialSelection();
  }

  private async mountBivariateMap(): Promise<void> {
    const container = document.getElementById("bivariate-map");
    if (!container) return;
    container.classList.add("catastro-maplibre");
    this.bivariateMap = await MapController.create(this.manifest, container, "bivariate-map-status");
    this.bivariateMap.bindUvHover(uvHoverContent);
    this.bivariateMap.bindUvClick(uvHoverContent);
    container.closest(".map-shell")?.classList.add("map-ready");
    this.bindBivariateTools();
    this.renderChileSelector();
    requestAnimationFrame(() => this.bivariateMap?.resize());
  }

  private applyInitialSelection(): void {
    const selector = document.getElementById("comuna");
    const selectedCode = this.state.communeCode
      ?? (selector instanceof HTMLSelectElement ? toDataCommuneCode(selector.value) : null);
    if (!selectedCode) {
      const defaultRow = this.rows.find((entry) => entry.codigo_comuna === DEFAULT_COMMUNE_CODE);
      if (defaultRow) {
        this.state.regionCode = regionCodeForName(defaultRow.region);
        this.state.communeCode = defaultRow.codigo_comuna;
        this.state.parcelLayerVisible = true;
        this.state.uvLayerVisible = true;
        this.state.mapScale = "mixta";
        this.selectFromMap(defaultRow.codigo_comuna);
        return;
      }
      this.state.parcelLayerVisible = false;
      this.state.mapScale = "uv";
      // Mantener el intent UV encendido: sin comuna no hay fetch; al seleccionar
      // una, el shard se carga sin que el checkbox mienta sobre el estado.
      this.state.uvLayerVisible = true;
      this.map?.setCommuneFilter(null);
      void this.bivariateMap?.setUvLayer(null);
      const bivariateCard = document.getElementById("bivariate-card");
      if (bivariateCard) bivariateCard.hidden = false;
      this.renderChileSelector();
      setBivariateStatus("Bivariado en espera de comuna.");
      setStatus("Contexto comunal nacional listo. Elige una comuna para cargar su capa UV.");
      return;
    }
    const row = this.rows.find((entry) => entry.codigo_comuna === selectedCode);
    if (row) {
      this.selectRow(row);
      return;
    }
    setStatus("Contexto comunal nacional listo. Elige una comuna para cargar su capa UV.");
  }

  private selectFromMap(code: string): void {
    const row = this.rows.find((entry) => entry.codigo_comuna === toDataCommuneCode(code));
    if (!row) return;
    const region = document.getElementById("region");
    const commune = document.getElementById("comuna");
    if (region instanceof HTMLSelectElement && commune instanceof HTMLSelectElement) {
      region.value = row.region;
      region.dispatchEvent(new Event("change", { bubbles: true }));
      commune.value = row.codigo_comuna;
      commune.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }
    this.selectRow(row, true);
  }

  private selectRow(row: CommuneRecord, activateMapView = false): void {
    this.selectedRow = row;
    this.state.regionCode = regionCodeForName(row.region);
    this.state.communeCode = row.codigo_comuna;
    if (row.codigo_comuna === DEFAULT_COMMUNE_CODE && !new URLSearchParams(window.location.search).has("comuna")) {
      this.state.parcelLayerVisible = true;
      this.state.uvLayerVisible = true;
      this.state.mapScale = "mixta";
    }
    this.updateSelectionDock(row);
    this.updateTerritoryTable(row);
    const territory = document.getElementById("territory");
    if (territory) territory.textContent = row.comuna;
    const section = document.getElementById("cartographic-map");
    if (section) section.hidden = false;
    this.map?.setCommuneFilter(row.codigo_comuna.padStart(5, "0"));
    const bivariateCard = document.getElementById("bivariate-card");
    if (bivariateCard) bivariateCard.hidden = false;
    this.syncBivariateSelectors(row);
    const parcelSource = this.state.regionCode ? this.manifest.parcel_regions[this.state.regionCode] : undefined;
    const parcelAvailable = Boolean(authorizedParcelSource(this.manifest, { ...this.state, parcelLayerVisible: true }));
    this.state = reconcileMapAvailability(this.state, parcelAvailable);
    replaceUrl(this.state, activateMapView ? "mapa" : undefined);
    const cameraSet = this.map ? this.applyCommuneCamera(this.map, row, parcelSource, true) : false;
    const bivariateCameraSet = this.bivariateMap ? this.applyCommuneCamera(this.bivariateMap, row, parcelSource, false) : false;
    const parcelsLoaded = this.state.parcelLayerVisible
      ? (this.map?.setParcelLayer(this.state) ?? false)
      : (this.map?.setParcelLayer({ ...this.state, regionCode: null }) ?? false);
    const parcelToggle = document.getElementById("map-layer-parcels");
    if (parcelToggle instanceof HTMLInputElement) {
      parcelToggle.disabled = !parcelAvailable;
      parcelToggle.checked = parcelsLoaded;
    }
    const uvToggle = document.getElementById("map-layer-uv");
    if (uvToggle instanceof HTMLInputElement) uvToggle.checked = this.state.uvLayerVisible;
    const tiltToggle = document.getElementById("map-tilt");
    if (tiltToggle instanceof HTMLButtonElement) tiltToggle.setAttribute("aria-pressed", "true");
    setStatus(
      parcelsLoaded && this.state.uvLayerVisible
        ? `Mapa de ${row.comuna}: OSM, predios referenciales y unidades vecinales activos.`
        : parcelsLoaded
          ? `Mapa de ${row.comuna}: capa predial regional referencial activa.`
        : parcelAvailable
          ? `Mapa UV de ${row.comuna}. Activa Predios para cargar el piloto regional bajo demanda.`
          : `Mapa UV de ${row.comuna}. El asterisco identifica las comunas con piloto predial.`
    );
    void this.refreshUvLayer(!cameraSet);
    void this.refreshBivariateLayer(!bivariateCameraSet);
  }

  private applyCommuneCamera(
    controller: MapController,
    row: CommuneRecord,
    parcelSource: TilesManifest["parcel_regions"][string] | undefined,
    perspective = true
  ): boolean {
    const communeCode = row.codigo_comuna.padStart(5, "0");
    const cityView = communeCityDefaultView(row.codigo_comuna);
    const defaultView = parcelSource?.commune_default_views?.[communeCode];
    const parcelFocus = parcelSource?.commune_focus_bounds?.[communeCode];
    const fallbackBounds: Bounds | null = communeViewBounds(row);
    if (cityView) {
      controller.setDefaultView(cityView, perspective);
      return true;
    }
    if (defaultView) {
      controller.setDefaultView(defaultView, perspective);
      return true;
    }
    if (parcelFocus) {
      controller.fitParcelFocus(parcelFocus);
      return true;
    }
    if (fallbackBounds) {
      controller.fitBounds(fallbackBounds, 13);
      return true;
    }
    return false;
  }

  private bindBivariateTools(): void {
    const region = document.getElementById("bivariate-region");
    const commune = document.getElementById("bivariate-comuna");
    if (!(region instanceof HTMLSelectElement) || !(commune instanceof HTMLSelectElement)) return;
    this.populateBivariateRegions();
    region.addEventListener("change", () => {
      const regionName = region.value || null;
      this.selectedRegionName = regionName;
      this.populateBivariateCommunes(region.value);
      this.renderChileSelector();
      this.dispatchRegionSelection(regionName);
      setBivariateSelectorStatus(regionName ? `${regionName}: selector filtrado; elige una comuna para fijar ambos mapas.` : "Selector nacional listo; elige una comuna.");
      setBivariateStatus(region.value ? `Región ${region.value} lista; elige una comuna para cargar el mapa UV.` : "Bivariado en espera de comuna.");
    });
    commune.addEventListener("change", () => {
      const code = toDataCommuneCode(commune.value);
      if (code) this.selectFromMap(code);
    });
  }

  private populateBivariateRegions(): void {
    const region = document.getElementById("bivariate-region");
    if (!(region instanceof HTMLSelectElement)) return;
    const current = region.value;
    const regions = [...new Set(this.rows.map((row) => row.region).filter(Boolean))];
    region.innerHTML = "";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Elige una región";
    region.append(placeholder);
    for (const name of regions) {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      region.append(option);
    }
    if (current && regions.includes(current)) region.value = current;
  }

  private populateBivariateCommunes(regionName: string, selectedCode: string | null = null): void {
    const commune = document.getElementById("bivariate-comuna");
    if (!(commune instanceof HTMLSelectElement)) return;
    const rows = regionName
      ? this.rows.filter((row) => row.region === regionName).sort((a, b) => a.comuna.localeCompare(b.comuna, "es"))
      : [];
    commune.innerHTML = "";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = rows.length ? "Elige una comuna" : "Elige una región primero";
    commune.append(placeholder);
    for (const row of rows) {
      const option = document.createElement("option");
      option.value = row.codigo_comuna;
      option.textContent = row.comuna;
      commune.append(option);
    }
    commune.disabled = !rows.length;
    if (selectedCode && rows.some((row) => row.codigo_comuna === selectedCode)) {
      commune.value = selectedCode;
    }
  }

  private syncBivariateSelectors(row: CommuneRecord): void {
    this.selectedRegionName = row.region;
    const region = document.getElementById("bivariate-region");
    if (region instanceof HTMLSelectElement) region.value = row.region;
    this.populateBivariateCommunes(row.region, row.codigo_comuna);
    this.dispatchRegionSelection(row.region, row.codigo_comuna);
    this.renderChileSelector();
  }

  private dispatchRegionSelection(regionName: string | null, communeCode: string | null = null): void {
    window.dispatchEvent(new CustomEvent("catastro:region-selection", {
      detail: { region: regionName, communeCode }
    }));
  }

  private renderChileSelector(): void {
    const svg = document.getElementById("bivariate-chile-selector");
    if (!(svg instanceof SVGSVGElement)) return;
    svg.replaceChildren();
    if (!this.chileSelector?.features.length) {
      svg.setAttribute("aria-label", "Selector gráfico no disponible");
      setBivariateSelectorStatus("Selector gráfico no disponible; usa Región y Comuna.");
      return;
    }
    const rowByCode = new Map(this.rows.map((row) => [row.codigo_comuna, row]));
    const selectedCode = this.selectedRow?.codigo_comuna ?? null;
    const activeRegion = this.selectedRegionName ?? this.selectedRow?.region ?? "";
    let selectable = 0;
    let withUv = 0;

    svg.setAttribute("viewBox", this.chileSelector.viewBox);
    svg.setAttribute("focusable", "false");
    const title = document.createElementNS(SVG_NS, "title");
    title.textContent = "Selector gráfico de comunas de Chile";
    const group = document.createElementNS(SVG_NS, "g");
    group.setAttribute("class", "chile-selector-layer");

    for (const feature of this.chileSelector.features) {
      const code = toDataCommuneCode(feature.code);
      const row = code ? rowByCode.get(code) ?? null : null;
      const regionName = row?.region ?? feature.region;
      const hasUv = row ? uvLayerAvailable(this.uvIndex, row.codigo_comuna) : false;
      const sameRegion = Boolean(activeRegion && regionName === activeRegion);
      const selected = Boolean(selectedCode && row?.codigo_comuna === selectedCode && (!activeRegion || sameRegion));
      const path = document.createElementNS(SVG_NS, "path");
      path.setAttribute("d", feature.d);
      path.setAttribute("fill-rule", "evenodd");
      path.dataset.region = regionName;
      path.dataset.comuna = row?.comuna ?? feature.comuna;
      if (row) {
        selectable += 1;
        if (hasUv) withUv += 1;
        path.dataset.code = row.codigo_comuna;
        path.setAttribute("role", "button");
        path.setAttribute("tabindex", "0");
        path.setAttribute("aria-label", `${row.comuna}, ${row.region}. ${hasUv ? "Con capa UV publicada" : "Sin capa UV publicada"}. Seleccionar comuna.`);
        path.classList.add("chile-feature", "available");
        path.classList.toggle("has-uv", hasUv);
        path.addEventListener("click", () => this.selectFromMap(row.codigo_comuna));
        path.addEventListener("keydown", (event) => {
          if (event.key !== "Enter" && event.key !== " ") return;
          event.preventDefault();
          this.selectFromMap(row.codigo_comuna);
        });
        const describeInteraction = (action: "clic" | "Enter") => {
          const current = this.selectedRow?.codigo_comuna === row.codigo_comuna;
          if (current) return `${row.comuna}, ${row.region}: selección activa para mapas, tablas y ranking comunal.`;
          return `${row.comuna}, ${row.region}${hasUv ? `: UV publicado; ${action} para cargar.` : `: sin shard UV publicado; ${action} actualiza la ficha.`}`;
        };
        path.addEventListener("pointerenter", () => {
          setBivariateSelectorStatus(describeInteraction("clic"));
        });
        path.addEventListener("focus", () => {
          setBivariateSelectorStatus(describeInteraction("Enter"));
        });
      } else {
        path.classList.add("chile-feature", "unavailable");
        path.setAttribute("aria-label", `${feature.comuna}, ${feature.region}: no está en el índice comunal del visor.`);
      }
      path.classList.toggle("selected-region", sameRegion);
      path.classList.toggle("selected-commune", selected);
      path.classList.toggle("dimmed", Boolean(activeRegion && !sameRegion));
      const label = document.createElementNS(SVG_NS, "title");
      label.textContent = row
        ? `${row.comuna}, ${row.region}${hasUv ? " · UV publicado" : " · sin shard UV publicado"}`
        : `${feature.comuna}, ${feature.region}`;
      path.append(label);
      group.append(path);
    }

    svg.append(title, group);
    if (this.selectedRow && (!activeRegion || this.selectedRow.region === activeRegion)) {
      setBivariateSelectorStatus(`${this.selectedRow.comuna}, ${this.selectedRow.region}: selección activa para mapas, tablas y ranking comunal.`);
    } else if (activeRegion) {
      setBivariateSelectorStatus(`${activeRegion}: filtro regional activo; elige comuna para cargar los mapas UV.`);
    } else {
      setBivariateSelectorStatus(`Selector nacional listo: ${integerFormatter.format(selectable)} comunas en el SVG, ${integerFormatter.format(withUv)} con shard UV publicado.`);
    }
  }

  private async refreshBivariateLayer(focusLocal = false): Promise<void> {
    const legend = document.getElementById("bivariate-uv-legend");
    const finding = document.getElementById("bivariate-finding");
    const code = this.state.communeCode;
    const row = this.selectedRow;
    const available = uvLayerAvailable(this.uvIndex, code);
    const shardUrl = uvShardUrl(this.uvIndex, this.state);
    if (!row || !available || !shardUrl) {
      await this.bivariateMap?.setUvLayer(null);
      if (legend) legend.hidden = true;
      if (finding) finding.textContent = "Elige una comuna para cargar el cruce UV. Si no hay shard publicado, el bivariado queda vacío y no simula datos.";
      if (row) this.updateTerritoryTable(row, null);
      setBivariateStatus("Bivariado UV no disponible para la comuna seleccionada.");
      return;
    }
    updateUvLegend();
    const loaded = await this.bivariateMap?.setUvLayer(shardUrl, this.currentTheme(), "m2", focusLocal, "bivariate");
    if (legend) legend.hidden = !loaded;
    if (!loaded) {
      if (finding) finding.textContent = `${row.comuna}: no hay capa UV publicada para el bivariado.`;
      this.updateTerritoryTable(row, null);
      setBivariateStatus("La capa bivariada no pudo cargarse.");
      return;
    }
    const summary = await uvSummaryFromUrl(shardUrl);
    if (finding) finding.textContent = summary ? bivariateFinding(row, summary) : `${row.comuna}: bivariado cargado; el resumen no pudo calcularse desde el shard.`;
    this.updateTerritoryTable(row, summary);
    setBivariateStatus(`${row.comuna}, ${row.region}: bivariado UV por m² cargado. Pasa el cursor o haz clic sobre una UV para leer sus datos.`);
    requestAnimationFrame(() => this.bivariateMap?.resize());
  }

  /** Índice de comunas con capa UV publicada. `null` mientras no se haya cargado. */
  private uvIndex: UvIndex | null = null;

  private currentTheme(): "light" | "dark" {
    return document.documentElement.dataset.theme === "light" ? "light" : "dark";
  }

  private syncMapScale(): void {
    this.state.mapScale = this.state.parcelLayerVisible && this.state.uvLayerVisible
      ? "mixta"
      : this.state.parcelLayerVisible
        ? "predial"
        : "uv";
  }

  private bindSelectionDock(): void {
    const reset = document.getElementById("selection-reset");
    if (!(reset instanceof HTMLButtonElement)) return;
    reset.addEventListener("click", () => {
      const defaultRow = this.rows.find((entry) => entry.codigo_comuna === DEFAULT_COMMUNE_CODE);
      if (!defaultRow) return;
      this.state.regionCode = regionCodeForName(defaultRow.region);
      this.state.communeCode = defaultRow.codigo_comuna;
      this.state.parcelLayerVisible = true;
      this.state.uvLayerVisible = true;
      this.state.mapScale = "mixta";
      this.selectFromMap(defaultRow.codigo_comuna);
    });
  }

  private updateSelectionDock(row: CommuneRecord): void {
    const dock = document.getElementById("selection-dock");
    const title = document.getElementById("selection-dock-title");
    const meta = document.getElementById("selection-dock-meta");
    const reset = document.getElementById("selection-reset");
    dock?.classList.add("has-selection");
    if (title) title.textContent = row.comuna;
    if (meta) {
      meta.textContent = [
        row.region,
        `código ${row.codigo_comuna.padStart(5, "0")}`,
        `${formatInteger(row.predios_habitacionales)} predios H`,
        `${formatPercent(row.cobertura_censo_pct)} cobertura`
      ].join(" · ");
    }
    if (reset instanceof HTMLButtonElement) {
      reset.textContent = row.codigo_comuna === DEFAULT_COMMUNE_CODE ? "Reset Diego" : "Volver a Diego";
    }
  }

  private updateTerritoryTable(row: CommuneRecord, summary: UvSummary | null = null): void {
    const name = document.getElementById("territory-detail-name");
    const lead = document.getElementById("territory-detail-summary");
    const body = document.getElementById("territory-detail-table-body");
    if (name) name.textContent = row.comuna;
    if (lead) {
      const uvText = summary
        ? `${formatInteger(summary.classified)} UV clasificadas; ${formatInteger(summary.missing)} sin celda bivariada.`
        : "Resumen UV pendiente o no disponible para la comuna seleccionada.";
      lead.textContent = `${row.comuna}, ${row.region}: cobertura residencial equivalente ${formatPercent(row.cobertura_censo_pct)}, ${formatInteger(row.predios_habitacionales)} predios H y avalúo fiscal total ${formatCurrency(row.avaluo_total_clp)}. ${uvText}`;
    }
    if (!body) return;

    const casen = row.casen_sensibilidad_disponible
      ? `${formatPercent(row.cobertura_casen_sensibilidad_pct)} como sensibilidad no representativa comunal`
      : "No disponible";
    const uvSummary = summary
      ? `${formatInteger(summary.classified)} clasificadas; ${formatInteger(summary.vulnerableHighM2)} con mayor vulnerabilidad y alto avalúo/m²; ${formatInteger(summary.missing)} sin clasificación completa`
      : "Pendiente, sin shard o sin variables suficientes";
    const rows: Array<[string, string, string]> = [
      ["Selección", `${row.comuna}, ${row.region}`, `Código compartible ${row.codigo_comuna.padStart(5, "0")}`],
      ["Catastro SII", row.fuente_sii_disponible ? row.periodo_catastro ?? "Disponible" : "Sin extracto SII en el corte", "Predios de destino H; geometría referencial cuando existe."],
      ["Predios H", formatInteger(row.predios_habitacionales), `${formatInteger(row.predios_habitacionales_mapeados)} con geometría; ${formatPercent(row.cobertura_coordenadas_pct)} con coordenadas válidas.`],
      ["Población Censo 2024", formatInteger(row.poblacion_censo_2024), `${formatInteger(row.hogares_censo_2024)} hogares; ${formatInteger(row.viviendas_ocupadas_censo_2024)} viviendas ocupadas.`],
      ["Población equivalente SII", formatInteger(row.poblacion_equivalente_censo), `Brecha equivalente: ${formatInteger(row.brecha_equivalente_censo)} personas frente al Censo.`],
      ["Superficie reportada", formatSquareMeters(row.superficie_total_m2), `Cobertura de superficie válida: ${formatPercent(row.cobertura_superficie_pct)}.`],
      ["Avalúo fiscal total", formatCurrency(row.avaluo_total_clp), `Por predio: ${formatCurrency(row.avaluo_por_predio_clp)}; cobertura de avalúo: ${formatPercent(row.cobertura_avaluo_pct)}.`],
      ["Ranking de avalúo", `Percentil nacional ${formatPercent(row.percentil_avaluo_nacional)}`, `Percentil regional ${formatPercent(row.percentil_avaluo_regional)}.`],
      ["Referencia 2017", formatPercent(row.cobertura_vs_proyeccion_base_2017_pct), "Comparación auxiliar frente a la proyección base 2017."],
      ["Sensibilidad CASEN", casen, row.casen_nota ?? "No usar CASEN para rankings comunales."],
      ["UV bivariado", uvSummary, "Cuartiles IGVUST oficiales; el eje de avalúo por m² se compacta visualmente en tres tramos."]
    ];
    body.replaceChildren(...rows.map(([metric, value, note]) => {
      const tr = document.createElement("tr");
      const th = document.createElement("th");
      const td = document.createElement("td");
      const small = document.createElement("small");
      th.scope = "row";
      th.textContent = metric;
      td.textContent = value;
      small.textContent = note;
      td.append(document.createElement("br"), small);
      tr.append(th, td);
      return tr;
    }));
  }

  /** Carga la capa UV de la comuna activa, si tiene una publicada. */
  private async refreshUvLayer(focusLocal = false): Promise<void> {
    const label = document.getElementById("map-layer-uv-label");
    const code = this.state.communeCode;
    const available = uvLayerAvailable(this.uvIndex, code);
    const shardUrl = uvShardUrl(this.uvIndex, this.state);

    // El control solo aparece donde hay datos: un checkbox que no puede hacer nada
    // confunde más de lo que informa.
    if (label) label.hidden = !available;
    if (!available || !shardUrl || !this.state.uvLayerVisible) {
      await this.map?.setUvLayer(null);
      return;
    }
    const loaded = await this.map?.setUvLayer(
      shardUrl,
      this.currentTheme(),
      "m2",
      focusLocal,
      "simple"
    );
    if (loaded) this.map?.setUvVisible(true);
    else setStatus("La capa de unidades vecinales no está disponible para esta comuna.");
  }

  private bindMapTools(): void {
    const base = document.getElementById("map-layer-basemap");
    const parcels = document.getElementById("map-layer-parcels");
    const uv = document.getElementById("map-layer-uv");
    const reset = document.getElementById("map-reset");
    const tilt = document.getElementById("map-tilt");

    if (uv instanceof HTMLInputElement) uv.checked = this.state.uvLayerVisible;
    if (parcels instanceof HTMLInputElement) parcels.checked = this.state.parcelLayerVisible;

    if (uv instanceof HTMLInputElement) {
      uv.addEventListener("change", () => {
        this.state.uvLayerVisible = uv.checked;
        this.syncMapScale();
        replaceUrl(this.state, "mapa");
        void this.refreshUvLayer();
        setStatus(uv.checked ? "Unidades vecinales visibles como capa azul transparente." : "Capa de unidades vecinales oculta.");
      });
    }
    // El segundo mapa usa una expresión bivariada que depende del tema; se
    // reconstruye junto a la capa simple para mantener ambos mapas sincronizados.
    window.addEventListener("catastro:theme", () => {
      if (this.state.uvLayerVisible) void this.refreshUvLayer();
      void this.refreshBivariateLayer();
    });

    if (base instanceof HTMLInputElement) {
      base.addEventListener("change", () => {
        this.map?.setBasemapVisible(base.checked);
        replaceUrl(this.state, "mapa");
      });
    }
    if (parcels instanceof HTMLInputElement) {
      parcels.addEventListener("change", () => {
        this.state.parcelLayerVisible = parcels.checked;
        this.syncMapScale();
        const loaded = this.map?.setParcelLayer(this.state) ?? false;
        this.state.parcelLayerVisible = parcels.checked && loaded;
        if (parcels.checked && !loaded) parcels.checked = false;
        this.syncMapScale();
        this.map?.setParcelsVisible(parcels.checked);
        replaceUrl(this.state, "mapa");
        setStatus(this.state.parcelLayerVisible ? "Capa predial referencial visible junto a las unidades vecinales si están activas." : "Capa predial oculta; las métricas se mantienen.");
      });
    }
    if (reset instanceof HTMLButtonElement) {
      reset.addEventListener("click", () => {
        this.map?.resetView();
        replaceUrl(this.state, "mapa");
        if (this.selectedRow) setStatus(`Vista inicial de ${this.selectedRow.comuna} restablecida.`);
      });
    }
    if (tilt instanceof HTMLButtonElement) {
      tilt.addEventListener("click", () => {
        const enabled = tilt.getAttribute("aria-pressed") !== "true";
        tilt.setAttribute("aria-pressed", String(enabled));
        this.map?.setPerspective(enabled);
        if (this.selectedRow) {
          setStatus(enabled ? `Perspectiva 3D de ${this.selectedRow.comuna} activa.` : `Vista plana de ${this.selectedRow.comuna} activa.`);
        }
      });
    }
  }
}
