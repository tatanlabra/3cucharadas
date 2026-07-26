import type { AppState, Bounds, CommuneDefaultView, CommuneRecord, VisualizationView } from "./types";

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

/** 12202 no está en el PMTiles comunal continental. Este encuadre se deriva del
 * shard UV publicado (extent -77.58383,-55.85101,-75.47444,-53.29438). */
export const COMMUNE_VIEW_FALLBACKS: Readonly<Record<string, Bounds>> = {
  "12202": [-77.58383, -55.85101, -75.47444, -53.29438]
};

/** Cámaras editoriales para comunas donde el extent UV cubre mucho territorio rural. */
export const COMMUNE_CITY_DEFAULT_VIEWS: Readonly<Record<string, CommuneDefaultView>> = {
  "3102": { center: [-70.8267, -27.0674], zoom: 13.35, bearing: -14, pitch: 48 },
  "3202": { center: [-70.0494, -26.367], zoom: 13.35, bearing: -14, pitch: 48 }
};

export function communeViewBounds(row: CommuneRecord): Bounds | null {
  return row.bounds ?? COMMUNE_VIEW_FALLBACKS[row.codigo_comuna] ?? null;
}

export function communeCityDefaultView(code: string | null): CommuneDefaultView | null {
  const normalized = toDataCommuneCode(code);
  return normalized ? COMMUNE_CITY_DEFAULT_VIEWS[normalized] ?? null : null;
}

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
  const validTerritory = Boolean(matchingRegion && (!regionCode || matchingRegion === regionCode));
  return {
    regionCode: validTerritory ? matchingRegion : null,
    communeCode: validTerritory ? communeCode : null,
    activeMetric: "cobertura_censo_pct",
    parcelLayerVisible: false,
    parcelOpacity: 0.18,
    mapScale: "uv",
    uvLayerVisible: true
  };
}

export function replaceUrl(state: AppState, view?: VisualizationView): void {
  const url = new URL(window.location.href);
  if (state.regionCode) url.searchParams.set("region", state.regionCode);
  else url.searchParams.delete("region");
  const commune = toSharedCommuneCode(state.communeCode);
  if (commune) url.searchParams.set("comuna", commune);
  else url.searchParams.delete("comuna");
  url.searchParams.set("metrica", state.activeMetric);
  url.searchParams.set("capa", "uv");
  url.searchParams.delete("normalizacion");
  if (view) url.searchParams.set("vista", view);
  window.history.replaceState({}, "", url);
}

/** Acepta URLs antiguas con capa predial/mixta, pero serializa la experiencia analítica nueva. */
export function reconcileMapAvailability(state: AppState, _parcelAvailable: boolean): AppState {
  return { ...state, mapScale: "uv", uvLayerVisible: true, parcelLayerVisible: false };
}

const LAB_VIEWS = new Set<VisualizationView>(["flujo", "avaluos", "distribuciones", "sensibilidad", "comunas"]);

export function visualizationViewFromUrl(search = window.location.search): VisualizationView {
  const value = new URLSearchParams(search).get("vista") as VisualizationView | null;
  return value && (value === "mapa" || LAB_VIEWS.has(value)) ? value : "mapa";
}

export function replaceVisualizationView(view: VisualizationView): void {
  const url = new URL(window.location.href);
  url.searchParams.set("vista", view);
  url.searchParams.delete("normalizacion");
  window.history.replaceState({}, "", url);
}

export function isLaboratoryView(value: VisualizationView): value is Exclude<VisualizationView, "mapa"> {
  return LAB_VIEWS.has(value);
}
