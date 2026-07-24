import fs from "node:fs";
import { describe, expect, it } from "vitest";
import { containsForbiddenIndividualField, parseInsightsV1, parseLegacyCommunes } from "../../assets/src/catastro_sii/insights";

function fixture() {
  const groups = [1, 2, 3, 4].map((quartile) => ({
    quartile,
    n: 10,
    min: 1,
    q1: 1.2,
    median: 1.4,
    q3: 1.6,
    max: 2,
    points: [[1, 0], [1.5, 1], [2, 0]]
  }));
  return {
    schema_version: 1,
    generated_at: "2026-07-22T12:00:00Z",
    source_hash: "a".repeat(64),
    universe: { uv: 40, communes: 1, complete_quartiles: 40, urban_uv: 20 },
    limits: ["No mide riqueza"],
    pipeline: {
      nodes: [
        { id: "records", label: "Registros originales", value: 100, unit: "records" },
        { id: "unique", label: "Predios únicos", value: 90, unit: "properties" }
      ],
      links: [{ source: "records", target: "unique", value: 90 }]
    },
    violin_densities: {
      panels: ["household", "m2-national", "m2-urban"].map((id) => ({
        id,
        title: id,
        metric: id,
        universe: "UV con dato",
        display_scale: "original",
        bandwidth_method: "scott",
        cut: 0,
        groups
      }))
    },
    quartile_transition: {
      matrix: [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]],
      same_quartile_pct: 19.9,
      moved_two_plus_pct: 45.8,
      n: 40
    },
    sensitivity: { rows: [{ id: "m2", label: "Por m²", n: 40, pearson: -0.58, spearman: -0.57, universe: "Nacional" }] },
    communes: [{ code: "3102", name: "Caldera", region: "Atacama", vulnerability: 2, av_total: 100, av_household: 20, av_person: 10, av_m2: 5, households: 5, urban_pct: 90 }]
  };
}

describe("contrato insights-v1", () => {
  it("acepta el fixture exacto con unidades records/properties", () => {
    const parsed = parseInsightsV1(fixture());
    expect(parsed.schema_version).toBe(1);
    expect(parsed.pipeline.nodes.map((node) => node.unit)).toEqual(["records", "properties"]);
    expect(parsed.violin_densities.panels).toHaveLength(3);
    expect(parsed.quartile_transition.matrix).toHaveLength(4);
  });

  it("rechaza versión desconocida, qa residual y atributos individuales", () => {
    expect(() => parseInsightsV1({ ...fixture(), schema_version: 2 })).toThrow(/schema_version/);
    expect(() => parseInsightsV1({ ...fixture(), qa: 4 })).toThrow(/qa residual/);
    expect(containsForbiddenIndividualField({ nested: { predio: "123" } })).toBe(true);
    for (const field of ["pred_uid", "rut", "run", "geometry", "coordinates"]) {
      expect(containsForbiddenIndividualField({ [field]: "no publicar" })).toBe(true);
    }
  });

  it("rechaza literales de unidad que vuelvan ambiguo registro y predio", () => {
    const input = fixture();
    input.pipeline.nodes[0].unit = "registros";
    expect(() => parseInsightsV1(input)).toThrow(/records de properties/);
  });

  const publishedPath = [
    "catastro_sii_brecha/data/insights-v1.json",
    "../catastros_sii/uv_avaluo/data/derived/publication/insights-v1.json"
  ].find((candidate) => fs.existsSync(candidate));
  const itWithPublishedArtifact = publishedPath ? it : it.skip;
  itWithPublishedArtifact("valida el artefacto real integrado en el sitio", () => {
    const parsed = parseInsightsV1(JSON.parse(fs.readFileSync(publishedPath as string, "utf8")));
    expect(parsed.universe).toEqual(expect.objectContaining({ uv: 6891, communes: 346, complete_quartiles: 6843, urban_uv: 3221 }));
    expect(parsed.pipeline.nodes.map((node) => node.unit)).toEqual(["records", "records", "properties", "properties", "properties"]);
    expect(parsed.quartile_transition.n).toBe(6843);
    expect(parsed.communes).toHaveLength(346);
  });
});

describe("fallback comunal legacy", () => {
  it("preserva sólo el avalúo total y no inventa hogar, persona ni m²", () => {
    const rows = parseLegacyCommunes({
      n: 1,
      codigo: ["3102"],
      comuna: ["CALDERA"],
      region: ["ATACAMA"],
      series: {
        avaluo_total_mmm: [2.5],
        vulnerabilidad_media: [3.1],
        hogares: [100],
        pct_urbano: [88]
      }
    });
    expect(rows[0]).toEqual(expect.objectContaining({ av_total: 2_500_000_000, av_household: null, av_person: null, av_m2: null }));
  });
});
