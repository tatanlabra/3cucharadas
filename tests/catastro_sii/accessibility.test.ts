import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import type { TilesManifest } from "../../assets/src/catastro_sii/types";

const runtime = vi.hoisted(() => {
  class FakeCanvas {
    readonly attributes = new Map<string, string>();

    setAttribute(name: string, value: string): void {
      this.attributes.set(name, value);
    }
  }

  class FakeMap {
    static readonly instances: FakeMap[] = [];
    readonly canvas = new FakeCanvas();
    readonly controls: unknown[] = [];
    readonly fittedBounds: Array<{ bounds: unknown; options: Record<string, unknown> }> = [];
    readonly events = new Map<string, Array<() => void>>();
    removed = false;

    constructor(readonly options: Record<string, unknown>) {
      FakeMap.instances.push(this);
    }

    getCanvas(): FakeCanvas { return this.canvas; }
    addControl(control: unknown): void { this.controls.push(control); }
    once(event: string, callback: () => void): void {
      this.events.set(event, [...(this.events.get(event) ?? []), callback]);
    }
    emit(event: string): void {
      const callbacks = this.events.get(event) ?? [];
      this.events.delete(event);
      for (const callback of callbacks) callback();
    }
    remove(): void { this.removed = true; this.events.clear(); }
    fitBounds(bounds: unknown, options: Record<string, unknown>): void { this.fittedBounds.push({ bounds, options }); }
    easeTo(_options: Record<string, unknown>): void {}
    getStyle(): { layers: [] } { return { layers: [] }; }
  }

  return { FakeCanvas, FakeMap, setWorkerUrl: vi.fn() };
});

vi.mock("maplibre-gl", () => ({
  addProtocol: vi.fn(),
  setWorkerUrl: runtime.setWorkerUrl,
  Map: runtime.FakeMap,
  NavigationControl: class {},
  GeolocateControl: class {},
  ScaleControl: class {},
  LngLatBounds: class {}
}));

vi.mock("maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url", () => ({ default: "/assets/dist/maplibre-worker-test.mjs" }));

vi.mock("pmtiles", () => ({ Protocol: class { tile = vi.fn(); } }));

import {
  configureMapCanvasAccessibility,
  configureParcelPopupAccessibility,
  configureUvPopupAccessibility,
  MAP_LOCALE,
  MapController,
  NATIONAL_DEFAULT_BOUNDS,
  NATIONAL_DEFAULT_CENTER,
  NATIONAL_DEFAULT_ZOOM,
  PARCEL_POPUP_OPTIONS,
  UV_CLICK_POPUP_OPTIONS,
  mapTransitionDuration,
  shouldFitNationalBounds
} from "../../assets/src/catastro_sii/map";

const manifest: TilesManifest = {
  schema_version: 1,
  generated_at: null,
  legal_publication_status: "PENDING",
  tiles_base: "/assets/data/catastro_sii/local/run",
  basemap: { available: false, url: "", style_url: "", attribution: "" },
  communes: { available: false, url: "", source_layer: "comunas", minzoom: 4, maxzoom: 12 },
  parcel_regions: {}
};

function mapContainer(): HTMLElement {
  // Model the DOM properties used by create; an empty object is not a real div.
  return { dataset: {}, clientWidth: 1024 } as HTMLElement;
}

beforeEach(() => {
  runtime.FakeMap.instances.length = 0;
  vi.stubGlobal("window", {
    location: { origin: "https://3cucharadas.cl" },
    innerWidth: 1024,
    setTimeout: (callback: () => void, delay: number) => globalThis.setTimeout(callback, delay),
    clearTimeout: (timer: ReturnType<typeof globalThis.setTimeout>) => globalThis.clearTimeout(timer)
  });
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

async function initializedMap(): Promise<InstanceType<typeof runtime.FakeMap>> {
  // The async style request precedes the constructor. Flush that work without
  // pretending a registration immediately fires a MapLibre event.
  for (let attempt = 0; attempt < 30; attempt += 1) {
    const map = runtime.FakeMap.instances.at(-1);
    if (map) return map;
    await Promise.resolve();
  }
  throw new Error("MapLibre no se inicializó en la prueba");
}

describe("accesibilidad del visor cartográfico", () => {
  it("configura el worker ESM empaquetado para MapLibre 6", () => {
    expect(runtime.setWorkerUrl).toHaveBeenCalledWith("/assets/dist/maplibre-worker-test.mjs");
  });

  it("mantiene los controles MapLibre y el cierre del popup en al menos 44 px", () => {
    const styles = readFileSync("assets/src/catastro_sii/styles.scss", "utf8");

    expect(styles).toMatch(/\.maplibregl-ctrl button[\s\S]*?min-width:\s*44px[\s\S]*?min-height:\s*44px/);
    expect(styles).toMatch(/\.maplibregl-popup-close-button[\s\S]*?min-width:\s*44px[\s\S]*?min-height:\s*44px/);
  });

  it("localiza las etiquetas expuestas por los controles de MapLibre", async () => {
    const creation = MapController.create(manifest, mapContainer());
    const map = await initializedMap();
    map.emit("style.load");
    await creation;

    expect(map?.options.locale).toEqual(expect.objectContaining({
      "Map.Title": "Mapa interactivo de brechas catastrales",
      "NavigationControl.ZoomIn": "Acercar",
      "NavigationControl.ZoomOut": "Alejar",
      "NavigationControl.ResetBearing": "Restablecer orientación",
      "GeolocateControl.FindMyLocation": "Mostrar mi ubicación",
      "Popup.Close": "Cerrar"
    }));
    expect(MAP_LOCALE["Map.Title"]).toBe("Mapa interactivo de brechas catastrales");
    expect(map?.controls).toHaveLength(3);
    expect(map?.options).toEqual(expect.objectContaining({ center: NATIONAL_DEFAULT_CENTER, zoom: 4 }));
    expect(map?.fittedBounds).toHaveLength(0);
    expect(NATIONAL_DEFAULT_ZOOM).toBe(3.1);
    expect(NATIONAL_DEFAULT_BOUNDS).toEqual([-76.2, -56.2, -66, -17.3]);
  });

  it("no ajusta Chile bajo el minzoom comunal en viewport móvil", () => {
    expect(shouldFitNationalBounds(390, 3)).toBe(false);
    expect(shouldFitNationalBounds(768, 3)).toBe(true);
    expect(shouldFitNationalBounds(1440, 4)).toBe(false);
  });

  it("mantiene un estilo de respaldo legible si falla el origen base", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("R2 no disponible"));
    const creation = MapController.create({
      ...manifest,
      basemap: { available: true, url: "base.pmtiles", style_url: "style.json", attribution: "© OpenStreetMap contributors" }
    }, mapContainer());
    const map = await initializedMap();
    map.emit("style.load");
    await creation;
    expect(map?.options.style).toEqual(expect.objectContaining({
      version: 8,
      sources: expect.objectContaining({
        "osm-raster": expect.objectContaining({
          type: "raster",
          attribution: "© OpenStreetMap contributors"
        })
      }),
      layers: expect.arrayContaining([
        expect.objectContaining({ id: "background", type: "background" }),
        expect.objectContaining({ id: "osm-raster", type: "raster" })
      ])
    }));
    fetchSpy.mockRestore();
    vi.unstubAllGlobals();
  });

  it("habilita el controlador con el estilo sin anunciar todavía el fondo completo", async () => {
    const container = mapContainer();
    let ready = false;
    const creation = MapController.create(manifest, container).then(() => { ready = true; });
    const map = await initializedMap();
    expect(container.dataset.basemapState).toBe("loading");
    expect(ready).toBe(false);
    map.emit("sourcedata");
    await Promise.resolve();
    expect(ready).toBe(false);
    map.emit("style.load");
    await creation;
    expect(ready).toBe(true);
    expect(container.dataset.basemapState).toBe("loading");
    map.emit("load");
    expect(container.dataset.basemapState).toBe("ready");
  });

  it("libera el mapa y rechaza una inicialización cuyo estilo nunca llega", async () => {
    vi.useFakeTimers();
    const creation = MapController.create(manifest, mapContainer());
    const rejected = expect(creation).rejects.toThrow("El estilo cartográfico no terminó de cargar");
    const map = await initializedMap();
    await vi.advanceTimersByTimeAsync(20_000);
    await rejected;
    expect(map.removed).toBe(true);
    expect(vi.getTimerCount()).toBe(0);
  });

  it("elimina transiciones cartográficas si el sistema reduce movimiento", () => {
    vi.stubGlobal("window", { matchMedia: () => ({ matches: true }) });
    expect(mapTransitionDuration()).toBe(0);
    vi.stubGlobal("window", { matchMedia: () => ({ matches: false }) });
    expect(mapTransitionDuration()).toBe(450);
    vi.unstubAllGlobals();
  });

  it("mantiene un canvas regional, nombrado, descrito y alcanzable por teclado", () => {
    const canvas = new runtime.FakeCanvas();

    configureMapCanvasAccessibility(canvas as unknown as HTMLCanvasElement);

    expect(Object.fromEntries(canvas.attributes)).toEqual({
      role: "region",
      tabindex: "0",
      "aria-label": "Mapa interactivo de brechas catastrales",
      "aria-describedby": "map-status"
    });
  });

  it("anuncia el detalle predial sin trasladar el foco al popup", () => {
    const content = new runtime.FakeCanvas();

    configureParcelPopupAccessibility(content as unknown as HTMLElement);

    expect(Object.fromEntries(content.attributes)).toEqual({
      role: "status",
      "aria-live": "polite",
      "aria-atomic": "true",
      "aria-label": "Información referencial del predio"
    });
    expect(PARCEL_POPUP_OPTIONS).toEqual({
      closeButton: true,
      focusAfterOpen: false,
      maxWidth: "260px"
    });
  });

  it("anuncia el detalle UV clickeado sin trasladar el foco al popup", () => {
    const content = new runtime.FakeCanvas();

    configureUvPopupAccessibility(content as unknown as HTMLElement);

    expect(Object.fromEntries(content.attributes)).toEqual({
      role: "status",
      "aria-live": "polite",
      "aria-atomic": "true",
      "aria-label": "Información agregada de la unidad vecinal"
    });
    expect(UV_CLICK_POPUP_OPTIONS).toEqual({
      closeButton: true,
      closeOnClick: true,
      focusAfterOpen: false,
      maxWidth: "290px"
    });
  });
});
