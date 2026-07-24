import { afterEach, describe, expect, it, vi } from "vitest";
import {
  isLaboratoryView,
  communeCityDefaultView,
  communeViewBounds,
  reconcileMapAvailability,
  regionCodeForName,
  replaceUrl,
  replaceVisualizationView,
  stateFromUrl,
  toDataCommuneCode,
  toSharedCommuneCode,
  visualizationViewFromUrl
} from "../../assets/src/catastro_sii/state";
import type { CommuneRecord } from "../../assets/src/catastro_sii/types";

afterEach(() => vi.unstubAllGlobals());

describe("territorial code contract", () => {
  it("normalizes the shared five-digit commune code without altering local records", () => {
    expect(toDataCommuneCode("03202")).toBe("3202");
    expect(toDataCommuneCode("3102")).toBe("3102");
    expect(toSharedCommuneCode("3102")).toBe("03102");
  });

  it("rejects malformed codes and maps the Atacama pilot", () => {
    expect(toDataCommuneCode("32A02")).toBeNull();
    expect(regionCodeForName("Atacama")).toBe("03");
  });

  it("encuadra 12202 desde el extent del shard UV aunque falte en PMTiles comunal", () => {
    expect(communeViewBounds({ codigo_comuna: "12202", comuna: "Antártica", region: "Magallanes y de la Antártica Chilena", bounds: null }))
      .toEqual([-77.58383, -55.85101, -75.47444, -53.29438]);
  });

  it("declara cámaras urbanas para comunas piloto cuyo extent UV cubre demasiado territorio rural", () => {
    expect(communeCityDefaultView("03102")).toEqual({ center: [-70.8267, -27.0674], zoom: 13.35, bearing: -14, pitch: 48 });
    expect(communeCityDefaultView("03202")).toEqual({ center: [-70.0494, -26.367], zoom: 13.35, bearing: -14, pitch: 48 });
    expect(communeCityDefaultView("03103")).toBeNull();
  });
});

describe("estado compartible", () => {
  const rows: CommuneRecord[] = [{ codigo_comuna: "3102", comuna: "Caldera", region: "Atacama" }];

  function browser(href: string): { replaced: string[] } {
    const replaced: string[] = [];
    const url = new URL(href);
    vi.stubGlobal("window", {
      location: { href: url.href, search: url.search },
      history: { replaceState: (_state: unknown, _title: string, value: string | URL) => replaced.push(String(value)) }
    });
    return { replaced };
  }

  it("abre UV y acepta comuna sin repetir región", () => {
    browser("https://3cucharadas.cl/catastro_sii_brecha/?comuna=03102");
    expect(stateFromUrl(rows)).toEqual(expect.objectContaining({
      regionCode: "03",
      communeCode: "3102",
      mapScale: "uv",
      uvLayerVisible: true,
      parcelLayerVisible: false
    }));
  });

  it("restaura predial y vista, y serializa sin normalizacion cartografica", () => {
    const runtime = browser("https://3cucharadas.cl/catastro_sii_brecha/?region=03&comuna=03102&capa=predial&normalizacion=m2&vista=sensibilidad");
    const state = stateFromUrl(rows);
    expect(state).toEqual(expect.objectContaining({ mapScale: "predial", parcelLayerVisible: true, uvLayerVisible: false }));
    expect(visualizationViewFromUrl()).toBe("sensibilidad");
    expect(isLaboratoryView("sensibilidad")).toBe(true);
    expect(isLaboratoryView("avaluos")).toBe(true);
    replaceUrl(state, "mapa");
    replaceVisualizationView("comunas");
    expect(runtime.replaced.join("\n")).not.toContain("normalizacion=");
    expect(runtime.replaced[0]).toContain("vista=mapa");
    expect(runtime.replaced.join("\n")).toContain("vista=comunas");
  });

  it("serializa una vista mixta cuando predios y UV quedan activos simultáneamente", () => {
    const runtime = browser("https://3cucharadas.cl/catastro_sii_brecha/?region=03&comuna=03102&capa=mixta&normalizacion=m2");
    const state = stateFromUrl(rows);
    expect(state).toEqual(expect.objectContaining({ mapScale: "mixta", parcelLayerVisible: true, uvLayerVisible: true, parcelOpacity: 0.18 }));
    replaceUrl(state, "mapa");
    expect(runtime.replaced[0]).toContain("capa=mixta");
  });

  it("conserva una vista analítica durante la hidratación inicial del mapa", () => {
    const runtime = browser("https://3cucharadas.cl/catastro_sii_brecha/?region=03&comuna=03102&vista=sensibilidad");
    replaceUrl(stateFromUrl(rows));
    expect(runtime.replaced[0]).toContain("vista=sensibilidad");
  });

  it("degrada una URL predial a UV al seleccionar una comuna fuera del piloto", () => {
    browser("https://3cucharadas.cl/catastro_sii_brecha/?region=03&comuna=03102&capa=predial");
    const predial = stateFromUrl(rows);
    expect(reconcileMapAvailability(predial, true)).toEqual(expect.objectContaining({ mapScale: "predial", parcelLayerVisible: true, uvLayerVisible: false }));
    expect(reconcileMapAvailability(predial, false)).toEqual(expect.objectContaining({ mapScale: "uv", parcelLayerVisible: false, uvLayerVisible: true }));
    const mixed = { ...predial, mapScale: "mixta" as const, parcelLayerVisible: true, uvLayerVisible: true };
    expect(reconcileMapAvailability(mixed, true)).toEqual(expect.objectContaining({ mapScale: "mixta", parcelLayerVisible: true, uvLayerVisible: true }));
  });
});
