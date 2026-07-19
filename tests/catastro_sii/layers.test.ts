import { describe, expect, it, vi } from "vitest";
import { addCommuneLayers, COMMUNE_FILL_ID, sourceAttribution } from "../../assets/src/catastro_sii/layers";
import type { TileSource } from "../../assets/src/catastro_sii/types";

const source: TileSource = {
  available: true,
  url: "example.pmtiles",
  source_layer: "example",
  minzoom: 1,
  maxzoom: 2
};

describe("atribución de fuentes PMTiles", () => {
  it("entrega una atribución válida aunque el manifest comunal no la declare", () => {
    expect(sourceAttribution(source)).toBe("Fuente cartográfica: 3 Cucharadas.");
  });

  it("conserva la atribución explícita de una capa", () => {
    expect(sourceAttribution({ ...source, attribution: "© OpenStreetMap contributors" }))
      .toBe("© OpenStreetMap contributors");
  });
});

describe("capa comunal en vista predial", () => {
  function addedCommuneFill(): Record<string, unknown> {
    const layers: Record<string, unknown>[] = [];
    const map = {
      getLayer: () => undefined,
      addLayer: (layer: Record<string, unknown>) => { layers.push(layer); }
    } as unknown as Parameters<typeof addCommuneLayers>[0];
    addCommuneLayers(map, source);
    const fill = layers.find((layer) => layer.id === COMMUNE_FILL_ID);
    expect(fill).toBeDefined();
    return (fill as { paint: Record<string, unknown> }).paint;
  }

  it("desvanece el relleno comunal antes de que entren los predios", () => {
    const opacity = addedCommuneFill()["fill-opacity"] as unknown[];
    // ["interpolate", ["linear"], ["zoom"], 11, 0.28, 13, 0.05, 14, 0]
    expect(opacity[0]).toBe("interpolate");
    expect(opacity.at(-2)).toBe(14);
    expect(opacity.at(-1)).toBe(0);
    const parcelMinzoom = 13;
    const stopAtParcelZoom = opacity[opacity.indexOf(parcelMinzoom) + 1] as number;
    expect(stopAtParcelZoom).toBeLessThan(0.1);
  });

  it("mantiene la capa clickeable para la selección comunal", () => {
    // Un fill-opacity 0 no retira la capa: el hit-testing usa la geometría, así que
    // eliminar la capa —en vez de desvanecerla— rompería el click en las 344 comunas
    // sin piloto predial.
    const map = { getLayer: vi.fn(() => undefined), addLayer: vi.fn() };
    addCommuneLayers(map as unknown as Parameters<typeof addCommuneLayers>[0], source);
    expect(map.addLayer).toHaveBeenCalledTimes(2);
  });
});
