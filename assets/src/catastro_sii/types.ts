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
  bearing?: number;
  pitch?: number;
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
  poblacion_equivalente_censo?: number | null;
  hogares_censo_2024?: number | null;
  viviendas_ocupadas_censo_2024?: number | null;
  predios_habitacionales_mapeados?: number | null;
  superficie_total_m2?: number | null;
  cobertura_superficie_pct?: number | null;
  avaluo_total_clp?: number | null;
  avaluo_por_predio_clp?: number | null;
  cobertura_avaluo_pct?: number | null;
  percentil_avaluo_nacional?: number | null;
  percentil_avaluo_regional?: number | null;
  cobertura_vs_proyeccion_base_2017_pct?: number | null;
  casen_sensibilidad_disponible?: boolean | null;
  cobertura_casen_sensibilidad_pct?: number | null;
  casen_nota?: string | null;
  fuente_sii_disponible?: boolean | null;
  periodo_catastro?: string | null;
  bounds?: Bounds | null;
}

/** Intención visible del mapa. Predios y UV pueden coexistir como capas independientes. */
export type MapScale = "predial" | "uv" | "mixta";

/** Eje de avalúo soportado por la paleta; el visor público fija el mapa UV en m². */
export type UvValuationMode = "household" | "m2";

/** Vista compartible del visor. `mapa` vive fuera del laboratorio analítico. */
export type VisualizationView = "mapa" | "flujo" | "avaluos" | "distribuciones" | "sensibilidad" | "comunas";

/** Propiedades del GeoJSON de Unidades Vecinales que produce el pipeline uv_avaluo.
 *  `qv` es el cuartil IGVUST nacional, donde 1 = MAYOR vulnerabilidad. `qa_h` y
 *  `qa_m2` conservan los cuartiles analíticos originales; la leyenda puede compactar
 *  visualmente el eje de avalúo sin modificar estos campos fuente. */
export interface UvFeatureProperties {
  uv: number;
  nombre: string | null;
  qv: number | null;
  qa_h: number | null;
  qa_m2: number | null;
  pob: number;
  hog: number;
  urb: number;
  av: number;
  avh: number;
  avm2: number;
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

export interface InsightsUniverse {
  uv: number;
  communes: number;
  complete_quartiles: number;
  urban_uv: number;
}

export interface PipelineNode {
  id: string;
  label: string;
  value: number;
  unit: "records" | "properties";
}

export interface PipelineLink {
  source: string;
  target: string;
  value: number;
}

export interface ViolinGroup {
  quartile: number;
  n: number;
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
  points: Array<[number, number]>;
}

export interface ViolinPanel {
  id: string;
  title: string;
  metric: string;
  universe: string;
  display_scale?: "original";
  bandwidth_method?: string;
  cut?: number;
  groups: ViolinGroup[];
}

export interface SensitivityRow {
  id: string;
  label: string;
  n: number;
  pearson: number;
  spearman: number;
  universe: string;
}

export interface CommuneInsight {
  code: string;
  name: string;
  region: string;
  vulnerability: number | null;
  av_total: number | null;
  av_household: number | null;
  av_person: number | null;
  av_m2: number | null;
  households: number | null;
  urban_pct: number | null;
}

/** Sólo contiene agregados territoriales; nunca registros prediales individuales. */
export interface InsightsV1 {
  schema_version: 1;
  generated_at: string;
  source_hash: string;
  universe: InsightsUniverse;
  limits: string[];
  pipeline: { nodes: PipelineNode[]; links: PipelineLink[] };
  violin_densities: { panels: ViolinPanel[] };
  quartile_transition: {
    matrix: number[][];
    same_quartile_pct: number;
    moved_two_plus_pct: number;
    n: number;
  };
  sensitivity: { rows: SensitivityRow[] };
  communes: CommuneInsight[];
}
