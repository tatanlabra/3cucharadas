import maplibregl, { LngLatBounds } from "maplibre-gl";
import { PMTiles, Protocol } from "pmtiles";
import { authorizedParcelSource } from "./availability";
import {
  addCommuneLayers,
  addParcelLayers,
  addPmtilesSource,
  COMMUNE_FILL_ID,
  COMMUNE_LINE_ID,
  COMMUNE_SOURCE_ID,
  PARCEL_FILL_ID,
  PARCEL_LINE_ID,
  PARCEL_SOURCE_ID,
  removeParcelLayers,
  addUvLayers,
  removeUvLayers,
  UV_FILL_ID,
  UV_LINE_ID,
  UV_SOURCE_ID
} from "./layers";
import type { RangeResponse, Source } from "pmtiles";
import type { AppState, Bounds, CommuneDefaultView, TileSource, TilesManifest } from "./types";

let protocolInstalled = false;
let pmtilesProtocol: Protocol | null = null;

const FALLBACK_STYLE: maplibregl.StyleSpecification = {
  version: 8,
  sources: {},
  layers: [{ id: "background", type: "background", paint: { "background-color": "#0c1320" } }]
};

/**
 * Jekyll/WEBrick may answer a cached byte-range request with 304 and no body.
 * PMTiles needs the bytes for every range, so local development disables the
 * browser HTTP cache for this transport. It affects delivery only; archive
 * contents remain untouched.
 */
class NoStoreFetchSource implements Source {
  constructor(private readonly url: string) {}

  getKey(): string { return this.url; }

  async getBytes(offset: number, length: number, signal?: AbortSignal): Promise<RangeResponse> {
    const response = await fetch(this.url, {
      signal,
      cache: "no-store",
      headers: { Range: `bytes=${offset}-${offset + length - 1}` }
    });
    if (!response.ok) throw new Error(`PMTiles respondió ${response.status}`);
    const contentLength = response.headers.get("Content-Length");
    if (response.status === 200 && (!contentLength || Number(contentLength) > length)) {
      throw new Error("El origen PMTiles no soporta byte ranges");
    }
    return {
      data: await response.arrayBuffer(),
      etag: response.headers.get("ETag") ?? undefined,
      cacheControl: response.headers.get("Cache-Control") ?? "no-store",
      expires: response.headers.get("Expires") ?? undefined
    };
  }
}

function registerPmtiles(url: string): void {
  if (!pmtilesProtocol || pmtilesProtocol.get(url)) return;
  const hostname = new URL(url).hostname;
  const useNoStore = hostname === "localhost" || hostname === "127.0.0.1" || hostname === "[::1]";
  pmtilesProtocol.add(new PMTiles(useNoStore ? new NoStoreFetchSource(url) : url));
}

export const MAP_LOCALE = {
  "Map.Title": "Mapa interactivo de brechas catastrales",
  "NavigationControl.ZoomIn": "Acercar",
  "NavigationControl.ZoomOut": "Alejar",
  "NavigationControl.ResetBearing": "Restablecer orientación",
  "Popup.Close": "Cerrar"
};

export const PARCEL_POPUP_OPTIONS = {
  closeButton: true,
  focusAfterOpen: false,
  maxWidth: "260px"
} as const;

/** MapLibre already exposes a focusable canvas; add the page-level context. */
export function configureMapCanvasAccessibility(canvas: Pick<HTMLCanvasElement, "setAttribute">): void {
  canvas.setAttribute("role", "region");
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("aria-label", MAP_LOCALE["Map.Title"]);
  canvas.setAttribute("aria-describedby", "map-status");
}

/**
 * A parcel click is supplementary information, not a modal action. Announce it
 * politely while keeping keyboard focus on the control the reader is using.
 */
export function configureParcelPopupAccessibility(content: Pick<HTMLElement, "setAttribute">): void {
  content.setAttribute("role", "status");
  content.setAttribute("aria-live", "polite");
  content.setAttribute("aria-atomic", "true");
  content.setAttribute("aria-label", "Información referencial del predio");
}

function tileUrl(manifest: TilesManifest, path: string): string {
  const base = new URL(`${manifest.tiles_base.replace(/\/$/, "")}/`, window.location.origin);
  return new URL(path, base).toString();
}

function assetUrl(manifest: TilesManifest, path: string): string {
  const base = new URL(manifest.tiles_base, window.location.origin).toString().replace(/\/$/, "");
  return `${base}/${path.replace(/^\//, "")}`;
}

function rewritePmtilesStyle(style: maplibregl.StyleSpecification, manifest: TilesManifest): maplibregl.StyleSpecification {
  const copy = structuredClone(style);
  for (const source of Object.values(copy.sources ?? {})) {
    if (source.type !== "vector" || !("url" in source) || typeof source.url !== "string") continue;
    if (source.url.startsWith("pmtiles://")) continue;
    source.url = `pmtiles://${tileUrl(manifest, source.url)}`;
  }
  if (typeof copy.glyphs === "string" && !/^https?:\/\//.test(copy.glyphs)) {
    copy.glyphs = assetUrl(manifest, copy.glyphs);
  }
  if (typeof copy.sprite === "string" && !/^https?:\/\//.test(copy.sprite)) {
    copy.sprite = assetUrl(manifest, copy.sprite);
  }
  for (const source of Object.values(copy.sources ?? {})) {
    if (source.type === "vector" && "url" in source && typeof source.url === "string" && source.url.startsWith("pmtiles://")) {
      registerPmtiles(source.url.slice("pmtiles://".length));
    }
  }
  return copy;
}

async function getBaseStyle(manifest: TilesManifest): Promise<maplibregl.StyleSpecification> {
  if (!manifest.basemap.available) return FALLBACK_STYLE;
  const response = await fetch(tileUrl(manifest, manifest.basemap.style_url), { cache: "force-cache" });
  if (!response.ok) throw new Error(`estilo base no disponible (${response.status})`);
  return rewritePmtilesStyle(await response.json() as maplibregl.StyleSpecification, manifest);
}

export class MapController {
  private readonly map: maplibregl.Map;
  private readonly baseLayerIds: string[];
  private communeSourceReady = false;
  private parcelRegion: string | null = null;
  private parcelPopupBound = false;
  private defaultView: CommuneDefaultView | null = null;

  private constructor(map: maplibregl.Map, private readonly manifest: TilesManifest) {
    this.map = map;
    this.baseLayerIds = map.getStyle().layers?.map((layer) => layer.id) ?? [];
  }

  private overlayBeforeId(): string | undefined {
    return this.map.getLayer("roads-glow") ? "roads-glow" : undefined;
  }

  static async create(manifest: TilesManifest, container: HTMLElement): Promise<MapController> {
    if (!protocolInstalled) {
      const protocol = new Protocol();
      maplibregl.addProtocol("pmtiles", protocol.tile);
      pmtilesProtocol = protocol;
      protocolInstalled = true;
    }
    const style = await getBaseStyle(manifest).catch(() => FALLBACK_STYLE);
    const map = new maplibregl.Map({
      container,
      style,
      center: [-71.0, -33.0],
      zoom: 4.2,
      cooperativeGestures: true,
      locale: MAP_LOCALE
    });
    configureMapCanvasAccessibility(map.getCanvas());
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.addControl(new maplibregl.ScaleControl({ maxWidth: 120, unit: "metric" }), "bottom-left");
    await new Promise<void>((resolve) => map.once("load", () => resolve()));
    return new MapController(map, manifest);
  }

  addCommunes(onClick: (communeCode: string) => void): boolean {
    const source = this.manifest.communes;
    if (!source.available) return false;
    const url = tileUrl(this.manifest, source.url);
    registerPmtiles(url);
    addPmtilesSource(this.map, COMMUNE_SOURCE_ID, source, url);
    addCommuneLayers(this.map, source, this.overlayBeforeId());
    this.communeSourceReady = true;
    this.map.on("click", COMMUNE_FILL_ID, (event) => {
      const code = event.features?.[0]?.properties?.cod_comuna;
      if (typeof code === "string" || typeof code === "number") onClick(String(code));
    });
    this.map.on("mouseenter", COMMUNE_FILL_ID, () => { this.map.getCanvas().style.cursor = "pointer"; });
    this.map.on("mouseleave", COMMUNE_FILL_ID, () => { this.map.getCanvas().style.cursor = ""; });
    return true;
  }

  setCommuneFilter(communeCode: string | null): void {
    if (!this.communeSourceReady) return;
    const filter: maplibregl.FilterSpecification = communeCode
      ? ["==", "cod_comuna", communeCode]
      : ["has", "cod_comuna"];
    this.map.setFilter(COMMUNE_LINE_ID, filter);
  }

  fitBounds(bounds: Bounds | null | undefined, maxZoom = 12): void {
    if (!bounds) return;
    this.map.fitBounds(new LngLatBounds([bounds[0], bounds[1]], [bounds[2], bounds[3]]), {
      padding: 48,
      duration: 450,
      maxZoom
    });
  }

  /**
   * A z13 PMTiles focus tile is intentionally broad enough to be a stable
   * geographic hint.  A viewer, however, needs a closer initial frame to
   * perceive the individual parcels.  This changes only the camera envelope;
   * it never changes or simplifies source geometry.
   */
  fitParcelFocus(bounds: Bounds | null | undefined): void {
    if (!bounds) return;
    const [west, south, east, north] = bounds;
    const centerX = (west + east) / 2;
    const centerY = (south + north) / 2;
    const factor = 0.5;
    const focused: Bounds = [
      centerX - (east - west) * factor / 2,
      centerY - (north - south) * factor / 2,
      centerX + (east - west) * factor / 2,
      centerY + (north - south) * factor / 2
    ];
    this.fitBounds(focused, 18);
  }

  /** Use the agreed municipal-capital camera as the reset point. */
  setDefaultView(view: CommuneDefaultView): void {
    this.defaultView = view;
    this.map.easeTo({ center: view.center, zoom: view.zoom, duration: 450 });
  }

  resetView(): void {
    if (this.defaultView) this.map.easeTo({ center: this.defaultView.center, zoom: this.defaultView.zoom, duration: 450 });
  }

  setBasemapVisible(visible: boolean): void {
    for (const id of this.baseLayerIds) {
      if (this.map.getLayer(id)) this.map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
    }
  }

  setCommunesVisible(visible: boolean): void {
    for (const id of [COMMUNE_FILL_ID, COMMUNE_LINE_ID]) {
      if (this.map.getLayer(id)) this.map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
    }
  }

  setParcelsVisible(visible: boolean): void {
    for (const id of [PARCEL_FILL_ID, PARCEL_LINE_ID]) {
      if (this.map.getLayer(id)) this.map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
    }
  }

  setUvVisible(visible: boolean): void {
    for (const id of [UV_FILL_ID, UV_LINE_ID]) {
      if (this.map.getLayer(id)) this.map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
    }
  }

  /**
   * Monta o actualiza la capa de Unidades Vecinales de una comuna.
   *
   * Al cambiar de comuna reemplaza los datos con `setData` en vez de retirar y volver
   * a añadir la fuente: es más barato y evita el problema de teardown que el visor ya
   * arrastra en la capa predial.
   */
  async setUvLayer(url: string | null, theme: "light" | "dark" = "light"): Promise<boolean> {
    if (!url) {
      removeUvLayers(this.map);
      return false;
    }
    let payload: unknown;
    try {
      const response = await fetch(url, { cache: "force-cache" });
      if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
      payload = await response.json();
    } catch {
      // Una comuna sin capa UV degrada a mapa sin capa, no a mapa roto.
      removeUvLayers(this.map);
      return false;
    }
    const collection = { type: "FeatureCollection", features: (payload as { features?: unknown[] }).features ?? [] };
    const existing = this.map.getSource(UV_SOURCE_ID);
    if (existing && "setData" in existing) {
      (existing as maplibregl.GeoJSONSource).setData(collection as never);
      return true;
    }
    this.map.addSource(UV_SOURCE_ID, { type: "geojson", data: collection as never });
    addUvLayers(this.map, theme, this.overlayBeforeId());
    return true;
  }

  setParcelLayer(state: AppState): boolean {
    const region = state.regionCode;
    const source = authorizedParcelSource(this.manifest, state);
    if (!region || !source) {
      removeParcelLayers(this.map);
      this.parcelRegion = null;
      return false;
    }
    if (this.parcelRegion !== region) {
      removeParcelLayers(this.map);
      const url = tileUrl(this.manifest, source.url);
      registerPmtiles(url);
      addPmtilesSource(this.map, PARCEL_SOURCE_ID, source, url);
      addParcelLayers(this.map, source, state.parcelOpacity, this.overlayBeforeId());
      this.parcelRegion = region;
      if (!this.parcelPopupBound) {
        this.map.on("click", PARCEL_FILL_ID, (event) => {
          const properties = event.features?.[0]?.properties ?? {};
          const content = document.createElement("div");
          configureParcelPopupAccessibility(content);
          const parcel = document.createElement("p");
          parcel.textContent = `Predio: ${typeof properties.predio === "number" || typeof properties.predio === "string" ? properties.predio : "No disponible"}`;
          const appraisal = document.createElement("p");
          const fiscalValue = Number(properties.avaluo_fiscal_clp);
          appraisal.textContent = Number.isFinite(fiscalValue)
            ? `Avalúo fiscal: ${new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 }).format(fiscalValue)}`
            : "Avalúo fiscal: No disponible";
          const destination = document.createElement("strong");
          destination.textContent = `Destino predial: ${properties.destino_clase === "Residencial" ? "Residencial" : "No disponible"}`;
          const quality = document.createElement("p");
          quality.textContent = `Calidad geométrica: ${properties.calidad_geometrica === "Referencial" ? "Referencial" : "No disponible"}`;
          const notice = document.createElement("p");
          notice.textContent = "Geometría referencial; no acredita deslindes ni dominio.";
          content.append(destination, parcel, appraisal, quality, notice);
          new maplibregl.Popup(PARCEL_POPUP_OPTIONS).setLngLat(event.lngLat).setDOMContent(content).addTo(this.map);
        });
        this.parcelPopupBound = true;
      }
    }
    const filter: maplibregl.FilterSpecification = state.communeCode
      ? ["==", "cod_comuna", state.communeCode.padStart(5, "0")]
      : ["==", "cod_region", region];
    this.map.setFilter(PARCEL_FILL_ID, filter);
    this.map.setPaintProperty(PARCEL_FILL_ID, "fill-opacity", state.parcelLayerVisible ? state.parcelOpacity : 0);
    return true;
  }

  resize(): void { this.map.resize(); }
  destroy(): void { this.map.remove(); }
}
