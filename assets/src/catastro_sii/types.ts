export type LegalPublicationStatus =
  | "AUTHORIZED_VECTOR"
  | "AUTHORIZED_RASTER_ONLY"
  | "PENDING"
  | "REJECTED";

export type Bounds = [number, number, number, number];

/** Camera-only metadata. It guides the initial view and never alters geometry. */
export interface CommuneDefaultView {
  center: [number, number];
  zoom: number;
}

export interface TileSource {
  available: boolean;
  url: string;
  source_layer: string;
  minzoom: number;
  maxzoom: number;
  style_url?: string;
  attribution?: string;
  territories_url?: string;
  scope?: string;
  pilot?: boolean;
  communes?: string[];
  commune_focus_bounds?: Record<string, Bounds>;
  commune_default_views?: Record<string, CommuneDefaultView>;
}

export interface TilesManifest {
  schema_version: number;
  generated_at: string | null;
  legal_publication_status: LegalPublicationStatus;
  tiles_base: string;
  basemap: Omit<TileSource, "source_layer" | "minzoom" | "maxzoom"> & {
    style_url: string;
    attribution: string;
  };
  communes: TileSource;
  parcel_regions: Record<string, TileSource>;
}

export interface CommuneRecord {
  codigo_comuna: string;
  comuna: string;
  region: string;
  cobertura_censo_pct?: number | null;
  brecha_equivalente_censo?: number | null;
  cobertura_coordenadas_pct?: number | null;
  predios_habitacionales?: number | null;
  poblacion_censo_2024?: number | null;
  bounds?: Bounds | null;
}

/** Escala del mapa. La capa UV es un gate independiente del piloto predial. */
export type MapScale = "predial" | "uv";

/** Propiedades del GeoJSON de Unidades Vecinales que produce el pipeline uv_avaluo.
 *  `qv` es el cuartil IGVUST nacional, donde 1 = MAYOR vulnerabilidad (convención
 *  MDSF vigente desde enero de 2026). `qa` es el cuartil nacional de avalúo por
 *  hogar: mismo alcance que `qv`, que es lo que hace legítimo cruzarlos. */
export interface UvFeatureProperties {
  uv: number;
  nombre: string | null;
  qv: number | null;
  qa: number | null;
  pob: number;
  hog: number;
  urb: number;
  av: number;
  avh: number;
  pv: number;
}

export interface AppState {
  regionCode: string | null;
  communeCode: string | null;
  activeMetric: "cobertura_censo_pct" | "brecha_equivalente_censo";
  parcelLayerVisible: boolean;
  parcelOpacity: number;
  mapScale: MapScale;
  uvLayerVisible: boolean;
}
