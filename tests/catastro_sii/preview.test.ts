import { describe, expect, it } from "vitest";
import { isLocalPreviewLocation, manifestUrlForLocation, manifestUrlsForLocation } from "../../assets/src/catastro_sii/preview";

describe("manifestUrlForLocation", () => {
  it("prioriza el overlay local y conserva fallback público en el preview normal", () => {
    expect(isLocalPreviewLocation("127.0.0.1", "")).toBe(false);
    expect(manifestUrlForLocation("127.0.0.1", "?region=03"))
      .toBe("/assets/data/catastro_sii/local/manifest.json");
    expect(manifestUrlsForLocation("127.0.0.1", "?region=03")).toEqual([
      "/assets/data/catastro_sii/local/manifest.json",
      "/assets/data/catastro_sii/manifest.json",
    ]);
  });

  it("permite el manifest local sólo con host y run id estrictos", () => {
    expect(isLocalPreviewLocation("127.0.0.1", "?catastroPreview=local&run=20260718T194751Z")).toBe(true);
    expect(manifestUrlForLocation("127.0.0.1", "?catastroPreview=local&run=20260718T194751Z"))
      .toBe("/assets/data/catastro_sii/local/20260718T194751Z/manifest.json");
    expect(manifestUrlForLocation("172.17.0.7", "?catastroPreview=local&run=20260718T194751Z"))
      .toBe("/assets/data/catastro_sii/local/20260718T194751Z/manifest.json");
  });

  it("no permite forzar el manifest local en producción o con una ruta arbitraria", () => {
    expect(isLocalPreviewLocation("3cucharadas.cl", "?catastroPreview=local&run=20260718T194751Z")).toBe(false);
    expect(isLocalPreviewLocation("localhost", "?catastroPreview=local&run=../../otro")).toBe(false);
    expect(isLocalPreviewLocation("localhost", "?run=20260718T194751Z")).toBe(false);
    expect(manifestUrlForLocation("3cucharadas.cl", "?catastroPreview=local&run=20260718T194751Z"))
      .toBe("/assets/data/catastro_sii/manifest.json");
    expect(manifestUrlForLocation("localhost", "?catastroPreview=local&run=../../otro"))
      .toBe("/assets/data/catastro_sii/manifest.json");
  });
});
