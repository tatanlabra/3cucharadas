import { describe, expect, it, vi } from "vitest";
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

    constructor(readonly options: Record<string, unknown>) {
      FakeMap.instances.push(this);
    }

    getCanvas(): FakeCanvas { return this.canvas; }
    addControl(): void {}
    once(_event: string, callback: () => void): void { callback(); }
  }

  return { FakeCanvas, FakeMap };
});

vi.mock("maplibre-gl", () => ({
  default: {
    addProtocol: vi.fn(),
    Map: runtime.FakeMap,
    NavigationControl: class {}
  },
  LngLatBounds: class {}
}));

vi.mock("pmtiles", () => ({ Protocol: class { tile = vi.fn(); } }));

import {
  configureMapCanvasAccessibility,
  configureParcelPopupAccessibility,
  MAP_LOCALE,
  MapController,
  PARCEL_POPUP_OPTIONS
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
  it("localiza las etiquetas expuestas por los controles de MapLibre", async () => {
    await MapController.create(manifest, {} as HTMLElement);
    const map = runtime.FakeMap.instances.at(-1);

    expect(map?.options.locale).toEqual(expect.objectContaining({
      "Map.Title": "Mapa interactivo de brechas catastrales",
      "NavigationControl.ZoomIn": "Acercar",
      "NavigationControl.ZoomOut": "Alejar",
      "NavigationControl.ResetBearing": "Restablecer orientación",
      "Popup.Close": "Cerrar"
    }));
    expect(MAP_LOCALE["Map.Title"]).toBe("Mapa interactivo de brechas catastrales");
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
});
