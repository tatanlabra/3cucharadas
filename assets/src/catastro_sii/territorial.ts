import type { CommuneAggregate, TerritorialAggregates } from "./types";

export const territorialAggregatesUrl = "/catastro_sii_brecha/data/agregados_territoriales.json";

const FORBIDDEN_KEYS = new Set(["geometry", "coordinates", "predio", "pred_uid", "rol", "rut", "run", "direccion", "avaluo_fiscal_clp"]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function assertNoForbiddenKeys(value: unknown): void {
  if (Array.isArray(value)) {
    for (const item of value) assertNoForbiddenKeys(item);
    return;
  }
  if (!isRecord(value)) return;
  for (const key of Object.keys(value)) {
    if (FORBIDDEN_KEYS.has(key)) throw new Error(`agregados territoriales contiene campo prohibido: ${key}`);
    assertNoForbiddenKeys(value[key]);
  }
}

function sharedCode(value: unknown): string | null {
  const text = String(value ?? "").trim();
  if (!/^\d{4,5}$/.test(text)) return null;
  return text.length === 5 ? text : text.padStart(5, "0");
}

function validCommuneAggregate(value: unknown, key: string): value is CommuneAggregate {
  if (!isRecord(value)) return false;
  if (value.codigo_comuna !== key) return false;
  if (typeof value.codigo_comuna_dato !== "string") return false;
  if (typeof value.comuna !== "string" || typeof value.region !== "string") return false;
  const quartile = value.cuartil_nacional_avm2;
  return quartile === null || quartile === 1 || quartile === 2 || quartile === 3 || quartile === 4;
}

export function parseTerritorialAggregates(payload: unknown): TerritorialAggregates {
  assertNoForbiddenKeys(payload);
  if (!isRecord(payload)) throw new Error("agregados territoriales invalido");
  if (payload.schema_version !== 1) throw new Error("version de agregados territoriales no soportada");
  if (!isRecord(payload.national) || !isRecord(payload.regions) || !isRecord(payload.communes)) {
    throw new Error("agregados territoriales sin bloques national/regions/communes");
  }
  if (payload.national.n_comunas !== 346) throw new Error("agregados territoriales sin 346 comunas");
  if (payload.national.n_regiones !== 16) throw new Error("agregados territoriales sin 16 regiones");
  if (payload.national.n_comunas_con_avm2 !== 340) throw new Error("agregados territoriales sin 340 comunas con avm2");
  const note = isRecord(payload.technical_notes)
    && isRecord(payload.technical_notes.uv_universe_reconciliation)
    ? payload.technical_notes.uv_universe_reconciliation
    : null;
  if (!note || note.insights_v1_uv !== 6891 || note.published_uv_features !== 6888 || note.difference !== 3) {
    throw new Error("agregados territoriales sin reconciliacion UV valida");
  }
  if (Object.keys(payload.communes).length !== 346) throw new Error("indice comunal territorial incompleto");
  if (Object.keys(payload.regions).length !== 16) throw new Error("indice regional territorial incompleto");
  for (const [code, aggregate] of Object.entries(payload.communes)) {
    if (sharedCode(code) !== code || !validCommuneAggregate(aggregate, code)) {
      throw new Error(`agregado comunal invalido: ${code}`);
    }
  }
  return payload as unknown as TerritorialAggregates;
}

export async function loadTerritorialAggregates(url = territorialAggregatesUrl): Promise<TerritorialAggregates> {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`${url} respondio ${response.status}`);
  return parseTerritorialAggregates(await response.json());
}

export function communeAggregateFor(
  aggregates: TerritorialAggregates,
  communeCode: string | null | undefined
): CommuneAggregate | null {
  const code = sharedCode(communeCode);
  return code ? aggregates.communes[code] ?? null : null;
}

export function communeQuartiles(aggregates: TerritorialAggregates): Record<string, 1 | 2 | 3 | 4 | null> {
  return Object.fromEntries(
    Object.entries(aggregates.communes).map(([code, row]) => [code, row.cuartil_nacional_avm2])
  );
}
