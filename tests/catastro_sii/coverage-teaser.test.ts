import { describe, expect, it } from "vitest";
import {
  buildCoveragePoints,
  ghostStyleFor,
  lowestCoveragePoint,
  medianOf,
  mostTruncatedPoint
} from "../../assets/src/catastro_sii/coverage-teaser";
import type { CommuneRecord } from "../../assets/src/catastro_sii/types";

function commune(overrides: Partial<CommuneRecord> & Pick<CommuneRecord, "codigo_comuna" | "comuna" | "region">): CommuneRecord {
  return {
    avaluo_total_clp: 1_000_000_000,
    cobertura_vivienda_pct: 80,
    hogares_censo_2024: 1000,
    ...overrides
  };
}

describe("buildCoveragePoints", () => {
  it("recorta la cobertura en 100 pero conserva el valor real para el tooltip y la tabla", () => {
    const [point] = buildCoveragePoints([
      commune({ codigo_comuna: "0101", comuna: "Alta cobertura", region: "Tarapacá", cobertura_vivienda_pct: 932.9 })
    ]);
    expect(point.coverageDisplay).toBe(100);
    expect(point.coverageReal).toBeCloseTo(932.9);
    expect(point.truncated).toBe(true);
  });

  it("no recorta ni marca como truncada una cobertura bajo 100", () => {
    const [point] = buildCoveragePoints([
      commune({ codigo_comuna: "0102", comuna: "Cobertura normal", region: "Tarapacá", cobertura_vivienda_pct: 83.5 })
    ]);
    expect(point.coverageDisplay).toBeCloseTo(83.5);
    expect(point.coverageReal).toBeCloseTo(83.5);
    expect(point.truncated).toBe(false);
  });

  it("excluye comunas con avalúo nulo o no positivo", () => {
    const points = buildCoveragePoints([
      commune({ codigo_comuna: "0201", comuna: "Sin avalúo", region: "Antofagasta", avaluo_total_clp: null }),
      commune({ codigo_comuna: "0202", comuna: "Avalúo cero", region: "Antofagasta", avaluo_total_clp: 0 }),
      commune({ codigo_comuna: "0203", comuna: "Avalúo negativo", region: "Antofagasta", avaluo_total_clp: -5 }),
      commune({ codigo_comuna: "0204", comuna: "Avalúo válido", region: "Antofagasta", avaluo_total_clp: 500 })
    ]);
    expect(points).toHaveLength(1);
    expect(points[0].code).toBe("0204");
  });

  it("excluye comunas con cobertura censal nula", () => {
    const points = buildCoveragePoints([
      commune({ codigo_comuna: "0301", comuna: "Sin cobertura", region: "Atacama", cobertura_vivienda_pct: null })
    ]);
    expect(points).toHaveLength(0);
  });

  it("usa 0 hogares cuando el dato censal falta, en vez de descartar la comuna", () => {
    const [point] = buildCoveragePoints([
      commune({ codigo_comuna: "0401", comuna: "Sin hogares", region: "Coquimbo", hogares_censo_2024: null })
    ]);
    expect(point.households).toBe(0);
  });
});

describe("medianOf", () => {
  it("devuelve null para una lista vacía", () => {
    expect(medianOf([])).toBeNull();
  });

  it("promedia los dos centrales en listas pares", () => {
    expect(medianOf([10, 20, 30, 40])).toBe(25);
  });

  it("toma el valor central en listas impares sin depender del orden de entrada", () => {
    expect(medianOf([40, 10, 30])).toBe(30);
  });
});

describe("extremos destacados", () => {
  const points = buildCoveragePoints([
    commune({ codigo_comuna: "1", comuna: "Baja cobertura", region: "Tarapacá", cobertura_vivienda_pct: 1.6 }),
    commune({ codigo_comuna: "2", comuna: "Cobertura media", region: "Tarapacá", cobertura_vivienda_pct: 80 }),
    commune({ codigo_comuna: "3", comuna: "Muy sobre el tope", region: "Tarapacá", cobertura_vivienda_pct: 932.9 })
  ]);

  it("lowestCoveragePoint identifica la comuna con menor cobertura real", () => {
    expect(lowestCoveragePoint(points)?.code).toBe("1");
  });

  it("mostTruncatedPoint identifica la comuna que más se aleja del tope de 100", () => {
    expect(mostTruncatedPoint(points)?.code).toBe("3");
  });

  it("ambas devuelven null para una lista vacía", () => {
    expect(lowestCoveragePoint([])).toBeNull();
    expect(mostTruncatedPoint([])).toBeNull();
  });
});

describe("ghosting por selección territorial", () => {
  const caldera = { code: "3102", region: "Atacama" };
  const iquique = { code: "1101", region: "Tarapacá" };

  it("con comuna activa resalta sólo esa burbuja y apaga el resto", () => {
    const ghost = { activeCode: "3102", activeRegion: "Atacama" };
    expect(ghostStyleFor(caldera, ghost)).toEqual({ opacity: 1, highlight: true });
    expect(ghostStyleFor(iquique, ghost)).toEqual({ opacity: 0.12, highlight: false });
  });

  it("la comuna manda por sobre la región cuando ambas están activas", () => {
    const ghost = { activeCode: "3102", activeRegion: "Atacama" };
    const otraDeAtacama = { code: "3202", region: "Atacama" };
    expect(ghostStyleFor(otraDeAtacama, ghost)).toEqual({ opacity: 0.12, highlight: false });
  });

  it("con sólo región activa deja esa región legible y apaga las demás, sin resaltar ninguna", () => {
    const ghost = { activeCode: null, activeRegion: "Atacama" };
    expect(ghostStyleFor(caldera, ghost)).toEqual({ opacity: 0.78, highlight: false });
    expect(ghostStyleFor(iquique, ghost)).toEqual({ opacity: 0.12, highlight: false });
  });

  it("sin selección devuelve la opacidad base para todas", () => {
    const ghost = { activeCode: null, activeRegion: null };
    expect(ghostStyleFor(caldera, ghost)).toEqual({ opacity: 0.78, highlight: false });
    expect(ghostStyleFor(iquique, ghost)).toEqual({ opacity: 0.78, highlight: false });
  });
});
