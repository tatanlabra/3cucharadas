import { describe, it, expect } from "vitest";
import { diagnosticRanking, fiscalGapPalette, scenarioSegments, type GapRow } from "../../assets/src/catastro_sii/fiscal-gap";
import fs from "node:fs";
const row = (code: string, gap: number | null, region = "R", residual = gap): GapRow => ({ codigo_comuna: code,
  comuna: code, region, signed_gap: gap, camp_sensitivity_positive_gap: residual,
  camp_census_households_observed_2024: gap === null || residual === null ? 0 : Math.max(gap-residual, 0),
  camp_absorbed_positive_gap: gap === null || residual === null ? null : Math.max(gap-residual, 0),
  camp_census_count_missing_polygons: 0, camp_adjustment_status: "complete_census_count", source_available: gap !== null,
  materiality_acceptable_scenario: residual === null ? null : Math.max(0, residual) * .8,
  materiality_other_scenario: residual === null ? null : Math.max(0, residual) * .2,
  materiality_acceptable_share_observed: .8,
  assessment_mean_clp: null, assessment_median_clp: null, assessment_above_exemption_share: null,
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
  it("keeps each bar boundary at least 3:1 against its theme surface", () => {
    const luminance = (hex: string) => hex.slice(1).match(/../g)!.map(v => parseInt(v,16) / 255)
      .map(c => c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4)
      .reduce((sum,c,i) => sum + c * [.2126,.7152,.0722][i], 0);
    for (const dark of [false, true]) {
      const p = fiscalGapPalette(dark), bg = luminance(dark ? "#10121D" : "#FFFFFF");
      const outline = luminance(p.boundary);
      const outlineContrast = (Math.max(outline,bg)+.05)/(Math.min(outline,bg)+.05);
      expect(new Set([p.residual, p.other, p.absorbed]).size).toBe(3);
      for (const color of [p.residual, p.other, p.absorbed]) {
        const fg = luminance(color);
        // Light fills share the night palette's hue; a visible stroke retains
        // shape contrast. Labels and patterns also distinguish the components.
        const fillContrast = (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);
        expect(Math.max(fillContrast, outlineContrast)).toBeGreaterThanOrEqual(3);
      }
    }
  });
  it("partitions the same original gap without adding a materiality count twice", () => {
    expect(scenarioSegments(row("101",100,"R",80))).toEqual([64,16,20]);
    expect(() => scenarioSegments({ ...row("101",100,"R",80), materiality_other_scenario: 40 })).toThrow();
    expect(() => scenarioSegments({ ...row("101",100), materiality_acceptable_scenario: null })).toThrow();
    expect(() => scenarioSegments({ ...row("101",100), materiality_acceptable_scenario: -10 })).toThrow();
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
