import maplibregl, { LngLatBounds } from "maplibre-gl";
import { PMTiles, Protocol } from "pmtiles";
import { authorizedParcelSource, parcelLayerRequested } from "./availability";
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
  updateUvFillExpression,
  UV_FILL_ID,
  UV_LINE_ID,
  UV_SOURCE_ID
} from "./layers";
import type { RangeResponse, Source } from "pmtiles";
import type { UvLayerStyle } from "./layers";
import type { AppState, Bounds, CommuneDefaultView, TileSource, TilesManifest, UvValuationMode } from "./types";

let protocolInstalled = false;
let pmtilesProtocol: Protocol | null = null;

const FALLBACK_STYLE: maplibregl.StyleSpecification = {
  version: 8,
  sources: {
    "osm-raster": {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors"
    }
  },
  layers: [
    { id: "background", type: "background", paint: { "background-color": "#f5f8fb" } },
    { id: "osm-raster", type: "raster", source: "osm-raster", paint: { "raster-opacity": 1 } }
  ]
};

/** Encuadre de Chile continental e insular americano para la vista inicial.
 * La comuna Antártica permanece seleccionable y recibe su propio fit al elegirla. */
export const NATIONAL_DEFAULT_BOUNDS: Bounds = [-76.2, -56.2, -66.0, -17.3];
export const NATIONAL_DEFAULT_CENTER: [number, number] = [-71.1, -36.7];
export const NATIONAL_DEFAULT_ZOOM = 3.1;
export const NATIONAL_FIT_MIN_WIDTH = 640;
export const LOCAL_DETAIL_ZOOM = 13;
export const LOCAL_DETAIL_BEARING = -14;
export const LOCAL_DETAIL_PITCH = 48;

/**
 * En una pantalla angosta, ajustar todo Chile reduce la cámara por debajo del
 * minzoom de la capa comunal y MapLibre deja de solicitar tiles. La vista
 * nacional móvil conserva por ello una cámara z3.1; el usuario puede desplazarse
 * o elegir territorio con los selectores sin encontrarse con un mapa vacío.
 */
export function shouldFitNationalBounds(viewportWidth: number, communeMinzoom: number): boolean {
  return viewportWidth >= NATIONAL_FIT_MIN_WIDTH && communeMinzoom <= 3;
}

type BoundsAccumulator = { west: number; south: number; east: number; north: number; seen: boolean };

function extendBoundsFromCoordinates(value: unknown, bounds: BoundsAccumulator): void {
  if (!Array.isArray(value)) return;
  if (
    value.length >= 2
    && typeof value[0] === "number"
    && typeof value[1] === "number"
    && Number.isFinite(value[0])
    && Number.isFinite(value[1])
  ) {
    const [lng, lat] = value;
    if (lng < -180 || lng > 180 || lat < -90 || lat > 90) return;
    bounds.west = Math.min(bounds.west, lng);
    bounds.south = Math.min(bounds.south, lat);
    bounds.east = Math.max(bounds.east, lng);
    bounds.north = Math.max(bounds.north, lat);
    bounds.seen = true;
    return;
  }
  for (const child of value) extendBoundsFromCoordinates(child, bounds);
}

export function geojsonFeatureBounds(collection: { features?: unknown[] }): Bounds | null {
  const bounds: BoundsAccumulator = {
    west: Number.POSITIVE_INFINITY,
    south: Number.POSITIVE_INFINITY,
    east: Number.NEGATIVE_INFINITY,
    north: Number.NEGATIVE_INFINITY,
    seen: false
  };
  for (const feature of collection.features ?? []) {
    const coordinates = (feature as { geometry?: { coordinates?: unknown } } | null)?.geometry?.coordinates;
    extendBoundsFromCoordinates(coordinates, bounds);
  }
  return bounds.seen ? [bounds.west, bounds.south, bounds.east, bounds.north] : null;
}

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
  "GeolocateControl.FindMyLocation": "Mostrar mi ubicación",
  "GeolocateControl.LocationNotAvailable": "Ubicación no disponible",
  "Popup.Close": "Cerrar"
};

export function mapTransitionDuration(): number {
  return typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ? 0 : 450;
}

export const PARCEL_POPUP_OPTIONS = {
  closeButton: true,
  focusAfterOpen: false,
  maxWidth: "260px"
} as const;

export const UV_POPUP_OPTIONS = {
  closeButton: false,
  closeOnClick: false,
  focusAfterOpen: false,
  maxWidth: "290px"
} as const;

export const UV_CLICK_POPUP_OPTIONS = {
  closeButton: true,
  closeOnClick: true,
  focusAfterOpen: false,
  maxWidth: "290px"
} as const;

type UvHoverFormatter = (properties: Record<string, unknown>) => HTMLElement | string;

/** MapLibre already exposes a focusable canvas; add the page-level context. */
export function configureMapCanvasAccessibility(
  canvas: Pick<HTMLCanvasElement, "setAttribute">,
  describedBy = "map-status"
): void {
  canvas.setAttribute("role", "region");
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("aria-label", MAP_LOCALE["Map.Title"]);
  canvas.setAttribute("aria-describedby", describedBy);
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

export function configureUvPopupAccessibility(content: Pick<HTMLElement, "setAttribute">): void {
  content.setAttribute("role", "status");
  content.setAttribute("aria-live", "polite");
  content.setAttribute("aria-atomic", "true");
  content.setAttribute("aria-label", "Información agregada de la unidad vecinal");
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
  private uvHoverBound = false;
  private uvClickBound = false;
  private uvHoverFormatter: UvHoverFormatter | null = null;
  private activeHoverPopup: maplibregl.Popup | null = null;
  private activeClickPopup: maplibregl.Popup | null = null;
  private defaultView: CommuneDefaultView | null = null;
  private defaultBounds: { bounds: Bounds; maxZoom: number } | null = null;
  private perspectiveEnabled = true;

  private constructor(map: maplibregl.Map, private readonly manifest: TilesManifest) {
    this.map = map;
    this.baseLayerIds = map.getStyle().layers?.map((layer) => layer.id) ?? [];
  }

  private overlayBeforeId(): string | undefined {
    return this.map.getLayer("roads-glow") ? "roads-glow" : undefined;
  }

  static async create(
    manifest: TilesManifest,
    container: HTMLElement,
    describedBy = "map-status"
  ): Promise<MapController> {
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
      center: NATIONAL_DEFAULT_CENTER,
      zoom: Math.max(NATIONAL_DEFAULT_ZOOM, manifest.communes.minzoom || 0),
      cooperativeGestures: true,
      locale: MAP_LOCALE
    });
    configureMapCanvasAccessibility(map.getCanvas(), describedBy);
    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), "top-right");
    map.addControl(new maplibregl.GeolocateControl({ trackUserLocation: false }), "top-right");
    if ("FullscreenControl" in maplibregl) map.addControl(new maplibregl.FullscreenControl(), "top-right");
    map.addControl(new maplibregl.ScaleControl({ maxWidth: 200, unit: "metric" }), "bottom-left");
    await new Promise<void>((resolve) => map.once("load", () => resolve()));
    const controller = new MapController(map, manifest);
    const viewportWidth = container.clientWidth
      || (typeof window !== "undefined" ? window.innerWidth : 1024)
      || 1024;
    if (shouldFitNationalBounds(viewportWidth, manifest.communes.minzoom)) {
      controller.fitBounds(NATIONAL_DEFAULT_BOUNDS, 5);
    } else {
      controller.setDefaultView({
        center: NATIONAL_DEFAULT_CENTER,
        zoom: Math.max(NATIONAL_DEFAULT_ZOOM, manifest.communes.minzoom || 0),
        bearing: 0,
        pitch: 0
      }, false);
    }
    return controller;
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
    this.defaultView = null;
    this.defaultBounds = { bounds: [...bounds], maxZoom };
    this.map.fitBounds(new LngLatBounds([bounds[0], bounds[1]], [bounds[2], bounds[3]]), {
      padding: 48,
      duration: mapTransitionDuration(),
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
  setDefaultView(view: CommuneDefaultView, perspective = true): void {
    this.defaultView = view;
    this.defaultBounds = null;
    this.perspectiveEnabled = perspective;
    this.map.easeTo({
      center: view.center,
      zoom: view.zoom,
      bearing: perspective ? view.bearing ?? LOCAL_DETAIL_BEARING : 0,
      pitch: perspective ? view.pitch ?? LOCAL_DETAIL_PITCH : 0,
      duration: mapTransitionDuration()
    });
  }

  focusLocalBounds(bounds: Bounds | null | undefined, zoom = LOCAL_DETAIL_ZOOM): void {
    if (!bounds) return;
    const [west, south, east, north] = bounds;
    const center: [number, number] = [(west + east) / 2, (south + north) / 2];
    this.setDefaultView({ center, zoom });
  }

  resetView(): void {
    if (this.defaultView) {
      this.map.easeTo({
        center: this.defaultView.center,
        zoom: this.defaultView.zoom,
        bearing: this.perspectiveEnabled ? this.defaultView.bearing ?? LOCAL_DETAIL_BEARING : 0,
        pitch: this.perspectiveEnabled ? this.defaultView.pitch ?? LOCAL_DETAIL_PITCH : 0,
        duration: mapTransitionDuration()
      });
      return;
    }
    if (this.defaultBounds) {
      const { bounds, maxZoom } = this.defaultBounds;
      this.map.fitBounds(new LngLatBounds([bounds[0], bounds[1]], [bounds[2], bounds[3]]), { padding: 48, duration: mapTransitionDuration(), maxZoom });
    }
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

  setPerspective(enabled: boolean): void {
    this.perspectiveEnabled = enabled;
    this.map.easeTo({
      bearing: enabled ? this.defaultView?.bearing ?? LOCAL_DETAIL_BEARING : 0,
      pitch: enabled ? this.defaultView?.pitch ?? LOCAL_DETAIL_PITCH : 0,
      duration: mapTransitionDuration()
    });
  }

  private orderAnalysisLayers(): void {
    const beforeId = this.overlayBeforeId();
    for (const id of [UV_FILL_ID, PARCEL_FILL_ID, PARCEL_LINE_ID, UV_LINE_ID]) {
      if (this.map.getLayer(id)) this.map.moveLayer(id, beforeId);
    }
  }

  bindUvHover(formatter: UvHoverFormatter): void {
    this.uvHoverFormatter = formatter;
    if (this.uvHoverBound) return;
    const popup = new maplibregl.Popup(UV_POPUP_OPTIONS);
    this.map.on("mousemove", UV_FILL_ID, (event) => {
      const properties = event.features?.[0]?.properties ?? {};
      const content = this.uvHoverFormatter?.(properties);
      if (!content) return;
      this.map.getCanvas().style.cursor = "crosshair";
      if (typeof content === "string") {
        popup.setLngLat(event.lngLat).setHTML(content).addTo(this.map);
      } else {
        popup.setLngLat(event.lngLat).setDOMContent(content).addTo(this.map);
      }
      this.activeHoverPopup = popup;
    });
    this.map.on("mouseleave", UV_FILL_ID, () => {
      this.map.getCanvas().style.cursor = "";
      popup.remove();
      if (this.activeHoverPopup === popup) this.activeHoverPopup = null;
    });
    this.uvHoverBound = true;
  }

  bindUvClick(formatter: UvHoverFormatter): void {
    this.uvHoverFormatter = formatter;
    if (this.uvClickBound) return;
    this.map.on("click", UV_FILL_ID, (event) => {
      const properties = event.features?.[0]?.properties ?? {};
      const content = this.uvHoverFormatter?.(properties);
      if (!content) return;
      if (typeof content !== "string") configureUvPopupAccessibility(content);
      this.activeHoverPopup?.remove();
      this.activeHoverPopup = null;
      this.activeClickPopup?.remove();
      const popup = new maplibregl.Popup(UV_CLICK_POPUP_OPTIONS).setLngLat(event.lngLat);
      if (typeof content === "string") popup.setHTML(content);
      else popup.setDOMContent(content);
      popup.addTo(this.map);
      this.activeClickPopup = popup;
    });
    this.uvClickBound = true;
  }

  /**
   * Monta o actualiza la capa de Unidades Vecinales de una comuna.
   *
   * Al cambiar de comuna reemplaza los datos con `setData` en vez de retirar y volver
   * a añadir la fuente: es más barato y evita el problema de teardown que el visor ya
   * arrastra en la capa predial.
   */
  async setUvLayer(
    url: string | null,
    theme: "light" | "dark" = "light",
    valuationMode: UvValuationMode = "household",
    focusLocal = false,
    layerStyle: UvLayerStyle = "bivariate"
  ): Promise<boolean> {
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
      updateUvFillExpression(this.map, theme, valuationMode, layerStyle);
      if (focusLocal) this.focusLocalBounds(geojsonFeatureBounds(collection));
      this.orderAnalysisLayers();
      return true;
    }
    this.map.addSource(UV_SOURCE_ID, { type: "geojson", data: collection as never });
    addUvLayers(this.map, theme, valuationMode, this.overlayBeforeId(), layerStyle);
    if (focusLocal) this.focusLocalBounds(geojsonFeatureBounds(collection));
    this.orderAnalysisLayers();
    return true;
  }

  setParcelLayer(state: AppState): boolean {
    const region = state.regionCode;
    if (!parcelLayerRequested(this.manifest, state)) {
      removeParcelLayers(this.map);
      this.parcelRegion = null;
      return false;
    }
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
      this.orderAnalysisLayers();
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
          this.activeHoverPopup?.remove();
          this.activeHoverPopup = null;
          this.activeClickPopup?.remove();
          this.activeClickPopup = new maplibregl.Popup(PARCEL_POPUP_OPTIONS).setLngLat(event.lngLat).setDOMContent(content).addTo(this.map);
        });
        this.parcelPopupBound = true;
      }
    }
    const filter: maplibregl.FilterSpecification = state.communeCode
      ? ["==", "cod_comuna", state.communeCode.padStart(5, "0")]
      : ["==", "cod_region", region];
    this.map.setFilter(PARCEL_FILL_ID, filter);
    this.map.setPaintProperty(PARCEL_FILL_ID, "fill-opacity", state.parcelLayerVisible ? state.parcelOpacity : 0);
    this.orderAnalysisLayers();
    return true;
  }

  resize(): void { this.map.resize(); }
  destroy(): void { this.map.remove(); }
}
