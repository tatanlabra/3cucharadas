import { describe, expect, it, vi } from "vitest";
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

    constructor(readonly options: Record<string, unknown>) {
      FakeMap.instances.push(this);
    }

    getCanvas(): FakeCanvas { return this.canvas; }
    addControl(control: unknown): void { this.controls.push(control); }
    once(_event: string, callback: () => void): void { callback(); }
    fitBounds(bounds: unknown, options: Record<string, unknown>): void { this.fittedBounds.push({ bounds, options }); }
    easeTo(_options: Record<string, unknown>): void {}
    getStyle(): { layers: [] } { return { layers: [] }; }
  }

  return { FakeCanvas, FakeMap };
});

vi.mock("maplibre-gl", () => ({
  default: {
    addProtocol: vi.fn(),
    Map: runtime.FakeMap,
    NavigationControl: class {},
    GeolocateControl: class {},
    ScaleControl: class {}
  },
  LngLatBounds: class {}
}));

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

describe("accesibilidad del visor cartográfico", () => {
  it("mantiene los controles MapLibre y el cierre del popup en al menos 44 px", () => {
    const styles = readFileSync("assets/src/catastro_sii/styles.scss", "utf8");

    expect(styles).toMatch(/\.maplibregl-ctrl button[\s\S]*?min-width:\s*44px[\s\S]*?min-height:\s*44px/);
    expect(styles).toMatch(/\.maplibregl-popup-close-button[\s\S]*?min-width:\s*44px[\s\S]*?min-height:\s*44px/);
  });

  it("localiza las etiquetas expuestas por los controles de MapLibre", async () => {
    await MapController.create(manifest, {} as HTMLElement);
    const map = runtime.FakeMap.instances.at(-1);

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
    vi.stubGlobal("window", { location: { origin: "https://3cucharadas.cl" } });
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("R2 no disponible"));
    await MapController.create({
      ...manifest,
      basemap: { available: true, url: "base.pmtiles", style_url: "style.json", attribution: "© OpenStreetMap contributors" }
    }, {} as HTMLElement);
    const map = runtime.FakeMap.instances.at(-1);
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
