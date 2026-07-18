export type LegalPublicationStatus =
  | "AUTHORIZED_VECTOR"
  | "AUTHORIZED_RASTER_ONLY"
  | "PENDING"
  | "REJECTED";

export type Bounds = [number, number, number, number];

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

export interface AppState {
  regionCode: string | null;
  communeCode: string | null;
  activeMetric: "cobertura_censo_pct" | "brecha_equivalente_censo";
  parcelLayerVisible: boolean;
  parcelOpacity: number;
}
