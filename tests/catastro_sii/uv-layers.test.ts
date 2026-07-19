import { describe, expect, it } from "vitest";
import {
  BIVARIATE_MISSING,
  BIVARIATE_PALETTE,
  bivariateFillExpression,
  UV_FILL_ID,
  UV_LINE_ID,
  addUvLayers,
  removeUvLayers
} from "../../assets/src/catastro_sii/layers";

function fakeMap() {
  const layers: Record<string, unknown>[] = [];
  const removed: string[] = [];
  const map = {
    getLayer: (id: string) => layers.find((layer) => layer.id === id),
    addLayer: (layer: Record<string, unknown>) => { layers.push(layer); },
    removeLayer: (id: string) => {
      removed.push(id);
      const index = layers.findIndex((layer) => layer.id === id);
      if (index >= 0) layers.splice(index, 1);
    },
    getSource: () => undefined,
    removeSource: () => undefined
  };
  return { map: map as unknown as Parameters<typeof addUvLayers>[0], layers, removed };
}

describe("paleta bivariada", () => {
  it("cubre las 16 celdas en ambos temas", () => {
    for (const theme of ["light", "dark"] as const) {
      const cells = Object.keys(BIVARIATE_PALETTE[theme]);
      expect(cells).toHaveLength(16);
      for (const qv of [1, 2, 3, 4]) {
        for (const qa of [1, 2, 3, 4]) expect(cells).toContain(`${qv}${qa}`);
      }
    }
  });

  it("destaca la contradiccion: mucha vulnerabilidad con mucho avaluo", () => {
    // qv=1 es MAYOR vulnerabilidad y qa=4 mayor avaluo por hogar. Esa celda es el
    // hallazgo que el mapa persigue, asi que debe ser la mas oscura de su fila en
    // el tema claro -- si alguien reordena la paleta, esta prueba lo detiene.
    const light = BIVARIATE_PALETTE.light;
    const luminance = (hex: string) => {
      const value = hex.replace("#", "");
      const channels = [0, 2, 4].map((index) => parseInt(value.slice(index, index + 2), 16) / 255);
      const linear = channels.map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
      return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
    };
    const row = [1, 2, 3, 4].map((qa) => luminance(light[`1${qa}`]));
    expect(Math.min(...row)).toBe(row[3]);
  });

  it("la expresion es un match valido de MapLibre con fallback", () => {
    const expression = bivariateFillExpression("light");
    expect(expression[0]).toBe("match");
    // match + input + 16 pares + fallback
    expect(expression).toHaveLength(2 + 16 * 2 + 1);
    expect(expression.at(-1)).toBe(BIVARIATE_MISSING.light);
  });

  it("cada tema usa su propio fallback", () => {
    expect(bivariateFillExpression("dark").at(-1)).toBe(BIVARIATE_MISSING.dark);
    expect(bivariateFillExpression("dark").at(-1)).not.toBe(BIVARIATE_MISSING.light);
  });
});

describe("ciclo de vida de la capa UV", () => {
  it("anade relleno y borde, y es idempotente", () => {
    const { map, layers } = fakeMap();
    addUvLayers(map);
    addUvLayers(map);
    expect(layers.map((layer) => layer.id)).toEqual([UV_FILL_ID, UV_LINE_ID]);
  });

  it("retira ambas capas al cambiar de escala", () => {
    const { map, removed } = fakeMap();
    addUvLayers(map);
    removeUvLayers(map);
    expect(removed).toEqual([UV_FILL_ID, UV_LINE_ID]);
  });
});
