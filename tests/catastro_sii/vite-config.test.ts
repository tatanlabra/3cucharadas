import { describe, expect, it } from "vitest";
import config from "../../vite.catastro.config";

describe("Vite Catastro SII paths", () => {
  it("emite los chunks perezosos bajo el directorio público de assets", () => {
    expect(config.base).toBe("/assets/dist/catastro_sii/");
  });
});
