import fs from "node:fs";
import { afterEach, describe, expect, it, vi } from "vitest";
import { communeAggregateFor, communeQuartiles, loadTerritorialAggregates, parseTerritorialAggregates } from "../../assets/src/catastro_sii/territorial";

afterEach(() => vi.unstubAllGlobals());

const payload = JSON.parse(fs.readFileSync("catastro_sii_brecha/data/agregados_territoriales.json", "utf8"));

describe("agregados territoriales del visor", () => {
  it("carga 346 comunas, 16 regiones y preserva las seis comunas sin avm2 positivo", () => {
    const parsed = parseTerritorialAggregates(payload);
    expect(parsed.national.n_comunas).toBe(346);
    expect(parsed.national.n_regiones).toBe(16);
    expect(parsed.national.n_comunas_con_avm2).toBe(340);
    expect(parsed.national.comunas_sin_avm2).toEqual(["05201", "11303", "12102", "12103", "12104", "12202"]);
    expect(Object.keys(parsed.communes)).toHaveLength(346);
    expect(Object.keys(parsed.regions)).toHaveLength(16);
    expect(parsed.regions).toHaveProperty("Valparaíso");
    expect(parsed.technical_notes.uv_universe_reconciliation).toMatchObject({
      insights_v1_uv: 6891,
      published_uv_features: 6888,
      difference: 3
    });
  });

  it("resuelve comunas con codigo compartible o codigo local de datos", () => {
    const parsed = parseTerritorialAggregates(payload);
    expect(communeAggregateFor(parsed, "03202")?.comuna).toBe("Diego de Almagro");
    expect(communeAggregateFor(parsed, "3202")?.codigo_comuna).toBe("03202");
    expect(communeQuartiles(parsed)["03202"]).toBe(3);
  });

  it("no contiene geometria ni campos prediales individuales", () => {
    const rendered = JSON.stringify(payload);
    for (const forbidden of ["geometry", "coordinates", "predio", "pred_uid", "rol", "rut", "run", "direccion", "avaluo_fiscal_clp"]) {
      expect(rendered).not.toContain(`"${forbidden}"`);
    }
    expect(() => parseTerritorialAggregates({ ...payload, communes: { ...payload.communes, "03202": { ...payload.communes["03202"], geometry: {} } } }))
      .toThrow(/campo prohibido/);
  });

  it("expone loader fetch separado de insights-v1", async () => {
    const fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => payload });
    vi.stubGlobal("fetch", fetch);
    const parsed = await loadTerritorialAggregates("/catastro_sii_brecha/data/agregados_territoriales.json");
    expect(parsed.national.n_comunas).toBe(346);
    expect(fetch).toHaveBeenCalledWith("/catastro_sii_brecha/data/agregados_territoriales.json", { cache: "force-cache" });
  });
});
