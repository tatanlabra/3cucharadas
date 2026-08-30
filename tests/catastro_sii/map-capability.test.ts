import { describe, expect, it } from "vitest";
import { supportsWebGL2 } from "../../assets/src/catastro_sii/map-capability";

describe("capacidad WebGL2 del mapa", () => {
  it("habilita el mapa cuando el contexto WebGL2 está disponible", () => {
    expect(supportsWebGL2(() => ({ getContext: () => ({}) as WebGL2RenderingContext }))).toBe(true);
  });

  it("conserva la alternativa textual si WebGL2 falta o el navegador falla", () => {
    expect(supportsWebGL2(() => ({ getContext: () => null }))).toBe(false);
    expect(supportsWebGL2(() => { throw new Error("canvas bloqueado"); })).toBe(false);
  });
});
