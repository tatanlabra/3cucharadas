import maplibregl, { LngLatBounds } from "maplibre-gl";
import { Protocol } from "pmtiles";
import { authorizedParcelSource } from "./availability";
import {
  addCommuneLayers,
  addParcelLayers,
  addPmtilesSource,
  COMMUNE_FILL_ID,
  COMMUNE_LINE_ID,
  COMMUNE_SOURCE_ID,
  PARCEL_FILL_ID,
  PARCEL_SOURCE_ID,
  removeParcelLayers
} from "./layers";
import type { AppState, Bounds, TileSource, TilesManifest } from "./types";

let protocolInstalled = false;

const FALLBACK_STYLE: maplibregl.StyleSpecification = {
  version: 8,
  sources: {},
  layers: [{ id: "background", type: "background", paint: { "background-color": "#0c1320" } }]
};

function tileUrl(manifest: TilesManifest, path: string): string {
  return new URL(path, `${manifest.tiles_base.replace(/\/$/, "")}/`).toString();
}

function rewritePmtilesStyle(style: maplibregl.StyleSpecification, manifest: TilesManifest): maplibregl.StyleSpecification {
  const copy = structuredClone(style);
  for (const source of Object.values(copy.sources ?? {})) {
    if (source.type !== "vector" || !("url" in source) || typeof source.url !== "string") continue;
    if (source.url.startsWith("pmtiles://")) continue;
    source.url = `pmtiles://${tileUrl(manifest, source.url)}`;
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
  private communeSourceReady = false;
  private parcelRegion: string | null = null;
  private parcelPopupBound = false;

  private constructor(map: maplibregl.Map, private readonly manifest: TilesManifest) {
    this.map = map;
  }

  static async create(manifest: TilesManifest, container: HTMLElement): Promise<MapController> {
    if (!protocolInstalled) {
      const protocol = new Protocol();
      maplibregl.addProtocol("pmtiles", protocol.tile);
      protocolInstalled = true;
    }
    const style = await getBaseStyle(manifest).catch(() => FALLBACK_STYLE);
    const map = new maplibregl.Map({
      container,
      style,
      center: [-71.0, -33.0],
      zoom: 4.2,
      cooperativeGestures: true
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    await new Promise<void>((resolve) => map.once("load", () => resolve()));
    return new MapController(map, manifest);
  }

  addCommunes(onClick: (communeCode: string) => void): boolean {
    const source = this.manifest.communes;
    if (!source.available) return false;
    addPmtilesSource(this.map, COMMUNE_SOURCE_ID, source, tileUrl(this.manifest, source.url));
    addCommuneLayers(this.map, source);
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
      addPmtilesSource(this.map, PARCEL_SOURCE_ID, source, tileUrl(this.manifest, source.url));
      addParcelLayers(this.map, source, state.parcelOpacity);
      this.parcelRegion = region;
      if (!this.parcelPopupBound) {
        this.map.on("click", PARCEL_FILL_ID, (event) => {
          const properties = event.features?.[0]?.properties ?? {};
          const content = document.createElement("div");
          const destination = document.createElement("strong");
          destination.textContent = `Destino predial: ${properties.destino_clase === "Residencial" ? "Residencial" : "No disponible"}`;
          const quality = document.createElement("p");
          quality.textContent = `Calidad geométrica: ${properties.calidad_geometrica === "Referencial" ? "Referencial" : "No disponible"}`;
          const notice = document.createElement("p");
          notice.textContent = "Geometría referencial; no acredita deslindes ni dominio.";
          content.append(destination, quality, notice);
          new maplibregl.Popup({ closeButton: true, maxWidth: "260px" }).setLngLat(event.lngLat).setDOMContent(content).addTo(this.map);
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
