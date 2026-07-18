import { describe, expect, it } from "vitest";
import { sourceAttribution } from "../../assets/src/catastro_sii/layers";
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
