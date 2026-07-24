import { describe, expect, it } from "vitest";
import { authorizedParcelCommuneCodes, authorizedParcelSource, defaultAuthorizedParcelRegion, parcelLayerRequested, uvLayerAvailable, uvShardUrl } from "../../assets/src/catastro_sii/availability";
import type { AppState, TilesManifest } from "../../assets/src/catastro_sii/types";

const state: AppState = {
  regionCode: "03",
  communeCode: "3102",
  activeMetric: "cobertura_censo_pct",
  parcelLayerVisible: true,
  parcelOpacity: 0.18,
  mapScale: "predial",
  uvLayerVisible: false
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

  it("does not expose a regional PMTiles outside its authorized pilot communes", () => {
    const authorized = {
      ...manifest,
      legal_publication_status: "AUTHORIZED_VECTOR" as const,
      parcel_regions: { "03": { ...manifest.parcel_regions["03"], communes: ["03102"] } }
    };
    expect(authorizedParcelSource(authorized, { ...state, communeCode: "3102" })?.url).toBe("predios.pmtiles");
    expect(authorizedParcelSource(authorized, { ...state, communeCode: "3101" })).toBeNull();
  });

  it("no solicita el PMTiles piloto hasta activar Predios explícitamente", () => {
    const authorized = { ...manifest, legal_publication_status: "AUTHORIZED_VECTOR" as const };
    expect(parcelLayerRequested(authorized, { ...state, mapScale: "uv", parcelLayerVisible: false })).toBe(false);
    expect(parcelLayerRequested(authorized, { ...state, mapScale: "predial", parcelLayerVisible: true })).toBe(true);
    expect(parcelLayerRequested(authorized, { ...state, mapScale: "mixta", parcelLayerVisible: true, uvLayerVisible: true })).toBe(true);
  });

  it("uses the first available authorized pilot as the default view", () => {
    const authorized = { ...manifest, legal_publication_status: "AUTHORIZED_VECTOR" as const };
    expect(defaultAuthorizedParcelRegion(manifest)).toBeNull();
    expect(defaultAuthorizedParcelRegion(authorized)).toBe("03");
  });

  it("exposes only authorized pilot communes for map selectors", () => {
    const authorized = {
      ...manifest,
      legal_publication_status: "AUTHORIZED_VECTOR" as const,
      parcel_regions: { "03": { ...manifest.parcel_regions["03"], communes: ["03102", "03202"] } }
    };
    expect([...authorizedParcelCommuneCodes(authorized)]).toEqual(["03102", "03202"]);
    expect([...authorizedParcelCommuneCodes(manifest)]).toEqual([]);
  });
});

describe("capa UV: gate paralelo al predial", () => {
  const index = { communes: ["3102", "13101", "5101"] };

  it("habilita solo comunas presentes en el indice", () => {
    expect(uvLayerAvailable(index, "3102")).toBe(true);
    expect(uvLayerAvailable(index, "3101")).toBe(false);
  });

  it("degrada sin indice o sin comuna", () => {
    expect(uvLayerAvailable(null, "3102")).toBe(false);
    expect(uvLayerAvailable({ communes: [] }, "3102")).toBe(false);
    expect(uvLayerAvailable(index, null)).toBe(false);
  });

  it("NO REGRESION: introducir la capa UV no mueve el gate predial", () => {
    // El gate predial protege microdato bajo autorizacion legal; el de UV solo publica
    // agregados. Si algun dia se acoplan, esta prueba lo detiene: una comuna con capa UV
    // pero fuera del piloto autorizado no puede obtener fuente predial.
    const authorized = {
      ...manifest,
      legal_publication_status: "AUTHORIZED_VECTOR" as const,
      parcel_regions: { "03": { ...manifest.parcel_regions["03"], communes: ["03102"] } }
    };
    expect(uvLayerAvailable({ communes: ["3101"] }, "3101")).toBe(true);
    expect(authorizedParcelSource(authorized, { ...state, communeCode: "3101" })).toBeNull();
    // Y a la inversa: estar en el piloto no implica tener capa UV.
    expect(authorizedParcelSource(authorized, { ...state, communeCode: "3102" })).not.toBeNull();
    expect(uvLayerAvailable({ communes: [] }, "3102")).toBe(false);
  });

  it("secuencia nacional -> comuna no piloto conserva intent UV y produce un solo shard", () => {
    const national: AppState = { ...state, communeCode: null, regionCode: null, mapScale: "uv", uvLayerVisible: true, parcelLayerVisible: false };
    expect(uvShardUrl(index, national)).toBeNull();
    const selected: AppState = { ...national, communeCode: "5101", regionCode: "05" };
    expect(uvShardUrl(index, selected)).toBe("data/uv/5101.json");
    expect(selected).toEqual(expect.objectContaining({ mapScale: "uv", uvLayerVisible: true, parcelLayerVisible: false }));
  });
});
