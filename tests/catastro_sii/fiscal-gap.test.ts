import { describe, it, expect } from "vitest";
import { diagnosticRanking, fiscalGapPalette, type GapRow } from "../../assets/src/catastro_sii/fiscal-gap";
import fs from "node:fs";
const row = (code: string, gap: number | null, region = "R", residual = gap): GapRow => ({ codigo_comuna: code,
  comuna: code, region, signed_gap: gap, camp_sensitivity_positive_gap: residual,
  camp_census_households_observed_2024: gap === null || residual === null ? 0 : Math.max(gap-residual, 0),
  camp_absorbed_positive_gap: gap === null || residual === null ? null : Math.max(gap-residual, 0),
  camp_census_count_missing_polygons: 0, camp_adjustment_status: "complete_census_count", source_available: gap !== null,
  dwellings_2024: 100, residential_roles_2026s1: gap === null ? null : 100-gap });
describe("physical diagnostics are not a monetary ranking", () => {
  it("ranks positive camp-sensitivity residuals, with deterministic CUT tie-break", () => {
    const input = [row("102",30,"R",10), row("101",20,"R",10), row("103",null), row("104",20,"R",0), row("105",0)];
    expect(diagnosticRanking(input).map(r => r.codigo_comuna)).toEqual(["101","102"]);
    expect(input).toHaveLength(5);
  });
  it("ranks within a region", () => {
    expect(diagnosticRanking([row("101",10,"R"),row("102",20,"S")],"R")).toHaveLength(1);
  });
  it("keeps residual and camp sensitivity colors semantically stable across themes", () => {
    expect(fiscalGapPalette(false)).toEqual({ residual: "#0F6F78", absorbed: "#C57A23", selection: "#17212B" });
    expect(fiscalGapPalette(true)).toEqual({ residual: "#55C4C0", absorbed: "#F0B35B", selection: "#F3F5F8" });
  });
  it("ships no fiscal values while the component reconciliation is blocked", () => {
    const data = JSON.parse(fs.readFileSync("catastro_sii_brecha/data/fiscal-gap/communes.json", "utf8"));
    expect(data.metadata.fiscal_status).toBe("blocked_components");
    expect(data.metadata.monetary_ranking).toEqual([]);
    expect(data.communes).toHaveLength(346);
    expect(data.communes.every((r: {scenario_q1_clp: unknown}) => r.scenario_q1_clp === null)).toBe(true);
    expect(data.communes.filter((r: GapRow) => !r.source_available).map((r: GapRow) => r.codigo_comuna)).toEqual(["12202","16207"]);
  });
});
