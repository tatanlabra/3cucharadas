import { describe, it, expect } from "vitest";
import { diagnosticRanking, type GapRow } from "../../assets/src/catastro_sii/fiscal-gap";
import fs from "node:fs";
const row = (code: string, gap: number | null, region = "R"): GapRow => ({ codigo_comuna: code,
  comuna: code, region, signed_gap: gap, source_available: gap !== null,
  dwellings_2024: 100, residential_roles_2026s1: gap === null ? null : 100-gap });
describe("physical diagnostics are not a monetary ranking", () => {
  it("retains only positive observed differences, with deterministic CUT tie-break", () => {
    const input = [row("102",10), row("101",10), row("103",null), row("104",-2), row("105",0)];
    expect(diagnosticRanking(input).map(r => r.codigo_comuna)).toEqual(["101","102"]);
    expect(input).toHaveLength(5);
  });
  it("ranks within a region", () => {
    expect(diagnosticRanking([row("101",10,"R"),row("102",20,"S")],"R")).toHaveLength(1);
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
