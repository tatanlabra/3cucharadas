import { describe, expect, it } from "vitest";
import { manifestUrlForLocation } from "../../assets/src/catastro_sii/preview";

describe("manifestUrlForLocation", () => {
  it("permite el manifest local sólo con host y run id estrictos", () => {
    expect(manifestUrlForLocation("127.0.0.1", "?catastroPreview=local&run=20260718T194751Z"))
      .toBe("/assets/data/catastro_sii/local/20260718T194751Z/manifest.json");
  });

  it("no permite forzar el manifest local en producción o con una ruta arbitraria", () => {
    expect(manifestUrlForLocation("3cucharadas.cl", "?catastroPreview=local&run=20260718T194751Z"))
      .toBe("/assets/data/catastro_sii/manifest.json");
    expect(manifestUrlForLocation("localhost", "?catastroPreview=local&run=../../otro"))
      .toBe("/assets/data/catastro_sii/manifest.json");
  });
});
