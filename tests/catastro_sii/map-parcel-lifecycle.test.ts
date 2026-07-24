import { describe, expect, it, vi } from "vitest";
import type { AppState, TileSource, TilesManifest } from "../../assets/src/catastro_sii/types";

vi.mock("maplibre-gl", () => ({
  default: {
    addProtocol: vi.fn(),
    Map: class {},
    NavigationControl: class {},
    GeolocateControl: class {},
    ScaleControl: class {},
    Popup: class {}
  },
  LngLatBounds: class {}
}));

vi.mock("pmtiles", () => ({ Protocol: class {} }));

import { geojsonFeatureBounds, LOCAL_DETAIL_ZOOM, MapController } from "../../assets/src/catastro_sii/map";
import {
  PARCEL_FILL_ID,
  PARCEL_LINE_ID,
  PARCEL_SOURCE_ID,
  UV_FILL_ID,
  UV_LINE_ID,
  UV_SOURCE_ID
} from "../../assets/src/catastro_sii/layers";

vi.stubGlobal("window", { location: { origin: "http://127.0.0.1:4001" } });

const parcelSource: TileSource = {
  available: true,
  url: "predios-03.pmtiles",
  source_layer: "predios",
  minzoom: 13,
  maxzoom: 18
};

const manifest: TilesManifest = {
  schema_version: 1,
  generated_at: null,
  legal_publication_status: "AUTHORIZED_VECTOR",
  tiles_base: "/assets/data/catastro_sii/local/run",
  basemap: { available: false, url: "", style_url: "", attribution: "" },
  communes: { available: false, url: "", source_layer: "comunas", minzoom: 4, maxzoom: 12 },
  parcel_regions: { "03": parcelSource }
};

const pilotState: AppState = {
  regionCode: "03",
  communeCode: "3102",
  activeMetric: "cobertura_censo_pct",
  parcelLayerVisible: true,
  parcelOpacity: 0.18,
  mapScale: "predial",
  uvLayerVisible: false
};

/**
 * Minimal MapLibre double. Its registries model the important invariant: MapLibre
 * only permits a source to be removed after every dependent layer is gone.
 */
class FakeMap {
  readonly sources = new Map<string, unknown>();
  readonly layers = new Map<string, unknown>();
  readonly calls: string[] = [];
  lastEaseTo: unknown = null;

  addSource(id: string, source: unknown): void {
    this.calls.push(`addSource:${id}`);
    this.sources.set(id, source);
  }

  getSource(id: string): unknown { return this.sources.get(id); }

  removeSource(id: string): void {
    if ([...this.layers.values()].some((layer) => (layer as { source?: string }).source === id)) {
      throw new Error(`source ${id} removed before dependent layers`);
    }
    this.calls.push(`removeSource:${id}`);
    this.sources.delete(id);
  }

  addLayer(layer: { id: string }): void {
    this.calls.push(`addLayer:${layer.id}`);
    this.layers.set(layer.id, layer);
  }

  getLayer(id: string): unknown { return this.layers.get(id); }

  removeLayer(id: string): void {
    this.calls.push(`removeLayer:${id}`);
    this.layers.delete(id);
  }

  moveLayer(id: string, beforeId?: string): void {
    this.calls.push(`moveLayer:${id}:${beforeId ?? "top"}`);
  }

  on(): void {}
  setFilter(): void {}
  setPaintProperty(): void {}
  setLayoutProperty(): void {}
  getStyle(): { layers: [] } { return { layers: [] }; }
  easeTo(options: unknown): void { this.lastEaseTo = options; }
}

function controllerFor(map: FakeMap): MapController {
  // The production constructor is deliberately private; use it only to inject
  // the MapLibre test double and exercise the public setParcelLayer contract.
  const Constructor = MapController as unknown as new (map: FakeMap, manifest: TilesManifest) => MapController;
  return new Constructor(map, manifest);
}

describe("lifecycle de la capa predial", () => {
  it("no registra fuente predial mientras la vista inicial sea UV", () => {
    const map = new FakeMap();
    const controller = controllerFor(map);
    expect(controller.setParcelLayer({ ...pilotState, mapScale: "uv", parcelLayerVisible: false })).toBe(false);
    expect(map.getSource(PARCEL_SOURCE_ID)).toBeUndefined();
    expect(map.calls.some((call) => call === `addSource:${PARCEL_SOURCE_ID}`)).toBe(false);
  });

  it("permite fuente predial cuando el mapa queda en capa mixta", () => {
    const map = new FakeMap();
    const controller = controllerFor(map);
    expect(controller.setParcelLayer({ ...pilotState, mapScale: "mixta", uvLayerVisible: true })).toBe(true);
    expect(map.getSource(PARCEL_SOURCE_ID)).toBeDefined();
  });

  it("retira las capas y la fuente prediales anteriores al seleccionar una región sin PMTiles autorizado", () => {
    const map = new FakeMap();
    const controller = controllerFor(map);

    expect(controller.setParcelLayer(pilotState)).toBe(true);
    expect(map.getSource(PARCEL_SOURCE_ID)).toBeDefined();
    expect(map.getLayer(PARCEL_FILL_ID)).toBeDefined();
    expect(map.getLayer(PARCEL_LINE_ID)).toBeDefined();

    expect(controller.setParcelLayer({ ...pilotState, regionCode: "04", communeCode: null })).toBe(false);

    expect(map.getLayer(PARCEL_FILL_ID)).toBeUndefined();
    expect(map.getLayer(PARCEL_LINE_ID)).toBeUndefined();
    expect(map.getSource(PARCEL_SOURCE_ID)).toBeUndefined();
    expect(map.calls.slice(-3)).toEqual([
      `removeLayer:${PARCEL_FILL_ID}`,
      `removeLayer:${PARCEL_LINE_ID}`,
      `removeSource:${PARCEL_SOURCE_ID}`
    ]);
  });
});

describe("fallback de shard UV", () => {
  it("calcula bounds locales desde un GeoJSON UV para la cámara cercana", () => {
    expect(geojsonFeatureBounds({
      features: [
        { geometry: { coordinates: [[[-70.86, -26.41], [-70.84, -26.41], [-70.84, -26.39], [-70.86, -26.39], [-70.86, -26.41]]] } },
        { geometry: { coordinates: [[[-70.82, -26.43], [-70.81, -26.43], [-70.81, -26.42], [-70.82, -26.42], [-70.82, -26.43]]] } }
      ]
    })).toEqual([-70.86, -26.43, -70.81, -26.39]);
  });

  it("usa zoom local cercano al seleccionar una comuna con shard UV", () => {
    const map = new FakeMap();
    const controller = controllerFor(map);
    controller.focusLocalBounds([-70.86, -26.43, -70.81, -26.39]);
    const options = map.lastEaseTo as { center: [number, number]; zoom: number };
    expect(options.center[0]).toBeCloseTo(-70.835, 6);
    expect(options.center[1]).toBeCloseTo(-26.41, 6);
    expect(options.zoom).toBe(LOCAL_DETAIL_ZOOM);
  });

  it("retira una capa anterior y devuelve false si el shard falla", async () => {
    const map = new FakeMap();
    map.addSource(UV_SOURCE_ID, { type: "geojson" });
    map.addLayer({ id: UV_FILL_ID, source: UV_SOURCE_ID } as never);
    map.addLayer({ id: UV_LINE_ID, source: UV_SOURCE_ID } as never);
    const controller = controllerFor(map);
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ ok: false, status: 404 } as Response);
    await expect(controller.setUvLayer("data/uv/5101.json")).resolves.toBe(false);
    expect(map.getLayer(UV_FILL_ID)).toBeUndefined();
    expect(map.getLayer(UV_LINE_ID)).toBeUndefined();
    expect(map.getSource(UV_SOURCE_ID)).toBeUndefined();
    fetchSpy.mockRestore();
  });
});
