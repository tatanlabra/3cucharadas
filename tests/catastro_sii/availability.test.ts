import { describe, expect, it } from "vitest";
import { authorizedParcelSource, defaultAuthorizedParcelRegion } from "../../assets/src/catastro_sii/availability";
import type { AppState, TilesManifest } from "../../assets/src/catastro_sii/types";

const state: AppState = {
  regionCode: "03",
  communeCode: "3102",
  activeMetric: "cobertura_censo_pct",
  parcelLayerVisible: true,
  parcelOpacity: 0.28
};

const manifest: TilesManifest = {
  schema_version: 1,
  generated_at: null,
  legal_publication_status: "PENDING",
  tiles_base: "https://tiles.example.test/catastro-sii",
  basemap: { available: false, url: "", style_url: "", attribution: "" },
  communes: { available: true, url: "comunas.pmtiles", source_layer: "comunas", minzoom: 4, maxzoom: 8 },
  parcel_regions: {
    "03": { available: true, url: "predios.pmtiles", source_layer: "predios", minzoom: 13, maxzoom: 18 }
  }
};

describe("parcel loading safety gate", () => {
  it("does not yield a predial source while legal publication is pending", () => {
    expect(authorizedParcelSource(manifest, state)).toBeNull();
  });

  it("yields only the selected region after vector authorization", () => {
    const authorized = { ...manifest, legal_publication_status: "AUTHORIZED_VECTOR" as const };
    expect(authorizedParcelSource(authorized, state)?.url).toBe("predios.pmtiles");
    expect(authorizedParcelSource(authorized, { ...state, regionCode: "04" })).toBeNull();
  });

  it("uses the first available authorized pilot as the default view", () => {
    const authorized = { ...manifest, legal_publication_status: "AUTHORIZED_VECTOR" as const };
    expect(defaultAuthorizedParcelRegion(manifest)).toBeNull();
    expect(defaultAuthorizedParcelRegion(authorized)).toBe("03");
  });
});
