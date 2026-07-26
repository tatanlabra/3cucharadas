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

describe("capa comunal analítica", () => {
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

  it("mantiene relleno visible para leer cuartiles comunales", () => {
    const opacity = addedCommuneFill()["fill-opacity"] as unknown[];
    // ["interpolate", ["linear"], ["zoom"], 3, 0.78, 10, 0.62, 14, 0.42]
    expect(opacity[0]).toBe("interpolate");
    expect(opacity.at(-2)).toBe(14);
    expect(opacity.at(-1)).toBeGreaterThan(0.4);
  });

  it("mantiene la capa clickeable para la selección comunal", () => {
    // Un fill-opacity 0 no retira la capa: el hit-testing usa la geometría, así que
    // eliminarla rompería el click que sincroniza selector, mapas y tabla.
    const map = { getLayer: vi.fn(() => undefined), addLayer: vi.fn() };
    addCommuneLayers(map as unknown as Parameters<typeof addCommuneLayers>[0], source);
    expect(map.addLayer).toHaveBeenCalledTimes(2);
  });
});
