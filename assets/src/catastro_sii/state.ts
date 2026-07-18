import type { AppState, CommuneRecord } from "./types";

const REGION_CODES: Record<string, string> = {
  "Arica y Parinacota": "15",
  Tarapacá: "01",
  Antofagasta: "02",
  Atacama: "03",
  Coquimbo: "04",
  Valparaíso: "05",
  "Libertador General Bernardo O'Higgins": "06",
  Maule: "07",
  Ñuble: "16",
  Biobío: "08",
  "La Araucanía": "09",
  "Los Ríos": "14",
  "Los Lagos": "10",
  "Aysén del General Carlos Ibáñez del Campo": "11",
  "Magallanes y de la Antártica Chilena": "12",
  "Metropolitana de Santiago": "13"
};

export function regionCodeForName(name: string): string | null {
  return REGION_CODES[name] ?? null;
}

export function toDataCommuneCode(value: string | null): string | null {
  if (!value || !/^\d{4,5}$/.test(value)) return null;
  return value.length === 5 && value.startsWith("0") ? value.slice(1) : value.padStart(4, "0");
}

export function toSharedCommuneCode(value: string | null): string | null {
  const code = toDataCommuneCode(value);
  return code ? code.padStart(5, "0") : null;
}

export function stateFromUrl(rows: CommuneRecord[]): AppState {
  const params = new URLSearchParams(window.location.search);
  const regionCode = params.get("region");
  const communeCode = toDataCommuneCode(params.get("comuna"));
  const commune = communeCode ? rows.find((row) => row.codigo_comuna === communeCode) : undefined;
  const matchingRegion = commune ? regionCodeForName(commune.region) : null;

  return {
    regionCode: matchingRegion && matchingRegion === regionCode ? regionCode : null,
    communeCode: matchingRegion && matchingRegion === regionCode ? communeCode : null,
    activeMetric: "cobertura_censo_pct",
    parcelLayerVisible: false,
    parcelOpacity: 0.28
  };
}

export function replaceUrl(state: AppState): void {
  const url = new URL(window.location.href);
  if (state.regionCode) url.searchParams.set("region", state.regionCode);
  else url.searchParams.delete("region");
  const commune = toSharedCommuneCode(state.communeCode);
  if (commune) url.searchParams.set("comuna", commune);
  else url.searchParams.delete("comuna");
  url.searchParams.set("metrica", state.activeMetric);
  window.history.replaceState({}, "", url);
}
