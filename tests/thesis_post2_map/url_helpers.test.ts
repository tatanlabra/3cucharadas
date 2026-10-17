import { describe, expect, it } from "vitest";
import { resolveAssetTemplate, resolveOrdinaryAsset } from "../../assets/src/thesis_post2_map/url_helpers";

describe("resolveAssetTemplate", () => {
  it("preserves MapLibre glyph placeholders literally", () => {
    expect(resolveAssetTemplate("https://tiles.example/base", "fonts/{fontstack}/{range}.pbf"))
      .toBe("https://tiles.example/base/fonts/{fontstack}/{range}.pbf");
  });

  it("resolves ordinary relative assets without a duplicate slash", () => {
    expect(resolveAssetTemplate("https://tiles.example/base/", "/map.pmtiles"))
      .toBe("https://tiles.example/base/map.pmtiles");
  });

  it("leaves absolute URLs untouched", () => {
    expect(resolveAssetTemplate("https://tiles.example/base", "https://cdn.example/style.json"))
      .toBe("https://cdn.example/style.json");
  });

  it("normalises ordinary paths while preserving query and hash", () => {
    expect(resolveOrdinaryAsset("https://tiles.example/base/dir", "../map.pmtiles?rev=2#tile"))
      .toBe("https://tiles.example/base/map.pmtiles?rev=2#tile");
  });
});
