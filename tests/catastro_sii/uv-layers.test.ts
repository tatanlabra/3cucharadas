import { describe, expect, it } from "vitest";
import {
  BIVARIATE_MISSING,
  BIVARIATE_PALETTE,
  PARCEL_FILL_ORANGE,
  PARCEL_LINE_ORANGE,
  UV_SIMPLE_BLUE,
  UV_QUARTILE_PROPERTY,
  bivariateFillExpression,
  PARCEL_FILL_ID,
  PARCEL_LINE_ID,
  UV_FILL_ID,
  UV_LINE_ID,
  addUvLayers,
  addParcelLayers,
  updateUvFillExpression,
  removeUvLayers
} from "../../assets/src/catastro_sii/layers";

function fakeMap() {
  const layers: Record<string, unknown>[] = [];
  const removed: string[] = [];
  const paints: Array<{ id: string; property: string; value: unknown }> = [];
  const map = {
    getLayer: (id: string) => layers.find((layer) => layer.id === id),
    addLayer: (layer: Record<string, unknown>) => { layers.push(layer); },
    removeLayer: (id: string) => {
      removed.push(id);
      const index = layers.findIndex((layer) => layer.id === id);
      if (index >= 0) layers.splice(index, 1);
    },
    setPaintProperty: (id: string, property: string, value: unknown) => {
      paints.push({ id, property, value });
    },
    getSource: () => undefined,
    removeSource: () => undefined
  };
  return { map: map as unknown as Parameters<typeof addUvLayers>[0], layers, removed, paints };
}

describe("paleta bivariada", () => {
  it("conserva cuatro cuartiles IGVUST y tres tramos visuales de avalúo", () => {
    for (const theme of ["light", "dark"] as const) {
      const cells = Object.keys(BIVARIATE_PALETTE[theme]);
      expect(cells).toHaveLength(12);
      for (const qv of [1, 2, 3, 4]) {
        for (const qa of [1, 2, 3]) expect(cells).toContain(`${qv}${qa}`);
      }
    }
  });

  it("mantiene una paleta legible sin declarar una contradicción social", () => {
    // qv=1 es MAYOR vulnerabilidad. El extremo de mayor avalúo se mantiene
    // distinguible, pero su interpretación depende del denominador elegido.
    const light = BIVARIATE_PALETTE.light;
    const luminance = (hex: string) => {
      const value = hex.replace("#", "");
      const channels = [0, 2, 4].map((index) => parseInt(value.slice(index, index + 2), 16) / 255);
      const linear = channels.map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
      return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
    };
    const row = [1, 2, 3].map((qa) => luminance(light[`1${qa}`]));
    expect(Math.min(...row)).toBe(row[2]);
  });

  it("la expresión mantiene qv oficial y compacta sólo el eje de avalúo", () => {
    for (const mode of ["household", "m2"] as const) {
      const expression = bivariateFillExpression("light", mode);
      expect(expression[0]).toBe("match");
      expect(expression[1]).toEqual([
        "concat",
        ["to-string", ["get", "qv"]],
        [
          "case",
          ["==", ["to-number", ["get", UV_QUARTILE_PROPERTY[mode]], 0], 1], "1",
          ["==", ["to-number", ["get", UV_QUARTILE_PROPERTY[mode]], 0], 4], "3",
          ["all", [">=", ["to-number", ["get", UV_QUARTILE_PROPERTY[mode]], 0], 2], ["<=", ["to-number", ["get", UV_QUARTILE_PROPERTY[mode]], 0], 3]], "2",
          "x"
        ]
      ]);
      // match + input + 12 pares + fallback
      expect(expression).toHaveLength(2 + 12 * 2 + 1);
      expect(expression.at(-1)).toBe(BIVARIATE_MISSING.light);
    }
  });

  it("cada tema usa su propio fallback", () => {
    expect(bivariateFillExpression("dark").at(-1)).toBe(BIVARIATE_MISSING.dark);
    expect(bivariateFillExpression("dark").at(-1)).not.toBe(BIVARIATE_MISSING.light);
  });
});

describe("ciclo de vida de la capa UV", () => {
  it("anade relleno bivariado y borde azul, y es idempotente", () => {
    const { map, layers } = fakeMap();
    addUvLayers(map);
    addUvLayers(map);
    expect(layers.map((layer) => layer.id)).toEqual([UV_FILL_ID, UV_LINE_ID]);
    expect(layers[0]).toMatchObject({ paint: { "fill-opacity": 0.62 } });
    expect(layers[1]).toMatchObject({
      paint: {
        "line-color": UV_SIMPLE_BLUE,
        "line-opacity": 0.68,
        "line-width": ["interpolate", ["linear"], ["zoom"], 10, 0.65, 13, 0.95, 16, 1.45]
      }
    });
  });

  it("puede montar UV como capa simple azul sin expresion bivariada", () => {
    const { map, layers } = fakeMap();
    addUvLayers(map, "light", "m2", undefined, "simple");
    expect(layers[0]).toMatchObject({ paint: { "fill-color": UV_SIMPLE_BLUE, "fill-opacity": 0.12 } });
    expect(layers[1]).toMatchObject({
      paint: {
        "line-color": UV_SIMPLE_BLUE,
        "line-opacity": 0.94,
        "line-width": ["interpolate", ["linear"], ["zoom"], 10, 1.1, 13, 1.8, 16, 2.55]
      }
    });
  });

  it("retira ambas capas al cambiar de escala", () => {
    const { map, removed } = fakeMap();
    addUvLayers(map);
    removeUvLayers(map);
    expect(removed).toEqual([UV_FILL_ID, UV_LINE_ID]);
  });

  it("actualiza el eje bivariado sin recargar la fuente", () => {
    const { map, paints } = fakeMap();
    addUvLayers(map, "dark", "household");
    updateUvFillExpression(map, "dark", "m2");
    expect(paints).toEqual([{
      id: UV_FILL_ID,
      property: "fill-color",
      value: bivariateFillExpression("dark", "m2")
    }, {
      id: UV_FILL_ID,
      property: "fill-opacity",
      value: 0.62
    }, {
      id: UV_LINE_ID,
      property: "line-color",
      value: UV_SIMPLE_BLUE
    }, {
      id: UV_LINE_ID,
      property: "line-opacity",
      value: 0.68
    }]);
  });

  it("actualiza la capa simple sin arrastrar el color bivariado", () => {
    const { map, paints } = fakeMap();
    addUvLayers(map, "light", "m2", undefined, "simple");
    updateUvFillExpression(map, "dark", "household", "simple");
    expect(paints).toContainEqual({ id: UV_FILL_ID, property: "fill-color", value: UV_SIMPLE_BLUE });
    expect(paints).toContainEqual({ id: UV_FILL_ID, property: "fill-opacity", value: 0.12 });
    expect(paints).toContainEqual({ id: UV_LINE_ID, property: "line-opacity", value: 0.94 });
  });
});

describe("capa predial piloto", () => {
  it("usa relleno naranja transparente y borde rojo-anaranjado fino", () => {
    const { map, layers } = fakeMap();
    addParcelLayers(map, { available: true, url: "x.pmtiles", source_layer: "predios", minzoom: 13, maxzoom: 18 }, 0.18);
    expect(layers.map((layer) => layer.id)).toEqual([PARCEL_FILL_ID, PARCEL_LINE_ID]);
    expect(layers[0]).toMatchObject({ paint: { "fill-color": PARCEL_FILL_ORANGE, "fill-opacity": 0.11 } });
    expect(layers[1]).toMatchObject({
      paint: {
        "line-color": PARCEL_LINE_ORANGE,
        "line-opacity": 0.94,
        "line-width": ["interpolate", ["linear"], ["zoom"], 13, 0.34, 16, 0.62, 18, 0.92]
      }
    });
  });
});
