import { describe, it, expect } from "vitest";
import fs from "node:fs";
import { modeledRanking, modeledValues, type ModeledRow } from "../../assets/src/catastro_sii/modeled-tax";
const data = JSON.parse(fs.readFileSync("catastro_sii_brecha/data/fiscal-gap/communes.json", "utf8"));
const rows: ModeledRow[] = data.communes;

describe("general-rule monetary scenarios", () => {
  it("matches the canonical ranking while preserving unavailable observed net tax", () => {
    const ranked = modeledRanking(rows);
    expect(ranked.length).toBe(15);
    expect(ranked.map(r => r.codigo_comuna)).toEqual(data.metadata.model_ranking);
    expect(ranked[0].comuna).toBe("Lo Barnechea");
    expect(data.communes.every((r: {net_mean_annual_clp: unknown}) => r.net_mean_annual_clp === null)).toBe(true);
    expect(rows.filter(r => r.modeled_tax_status === "available").length).toBe(344);
  });
  it("applies q once and never sorts by physical gap", () => {
    const r = modeledRanking(rows)[0];
    expect(modeledValues(r,.5)).toEqual([r.modeled_gap_median_clp!*.5, r.modeled_gap_mean_clp!*.5]);
    expect(modeledValues(r,0)).toEqual([0,0]);
    expect(() => modeledValues(r,2)).toThrow();
    expect(() => modeledValues(r,NaN)).toThrow();
    expect(() => modeledValues({...r,modeled_gap_mean_clp:null},0)).toThrow();
  });
  it("rejects incomplete, below-threshold, nonpositive and nonfinite rows", () => {
    const r = modeledRanking(rows)[0];
    expect(modeledRanking([
      {...r,source_available:false}, {...r,modeled_tax_status:"incomplete_assessments"},
      {...r,assessment_median_clp:60030710}, {...r,camp_sensitivity_positive_gap:0},
      {...r,modeled_gap_median_clp:NaN}, {...r,modeled_gap_mean_clp:Infinity}
    ])).toEqual([]);
    expect(modeledRanking(rows,r.region).every(x => x.region === r.region)).toBe(true);
  });
  it("preserves a valid zero median and does not assume median is a lower bound", () => {
    const r = modeledRanking(rows)[0];
    expect(modeledValues({...r,modeled_gap_median_clp:0},1)[0]).toBe(0);
    expect(modeledValues({...r,modeled_gap_median_clp:200,modeled_gap_mean_clp:100},1)).toEqual([200,100]);
  });
});
