import type maplibregl from "maplibre-gl";
import type { TileSource } from "./types";

export const COMMUNE_SOURCE_ID = "catastro-communes";
export const PARCEL_SOURCE_ID = "catastro-parcels";
export const COMMUNE_FILL_ID = "catastro-communes-fill";
export const COMMUNE_LINE_ID = "catastro-communes-line";
export const PARCEL_FILL_ID = "catastro-parcels-fill";
export const PARCEL_LINE_ID = "catastro-parcels-line";
export const UV_SOURCE_ID = "catastro-uv";
export const UV_FILL_ID = "catastro-uv-fill";
export const UV_LINE_ID = "catastro-uv-line";
export type UvLayerStyle = "simple" | "bivariate";

export const UV_SIMPLE_BLUE = "#21468b";
export const PARCEL_FILL_ORANGE = "#f97316";
export const PARCEL_LINE_ORANGE = "#e44714";

/** Cuartiles nacionales de mediana comunal de avalúo fiscal por m2. */
export const COMMUNE_QUARTILE_PALETTE: Record<"light" | "dark", Record<1 | 2 | 3 | 4, string>> = {
  light: {
    1: "#d7eef1",
    2: "#91c9c6",
    3: "#408c93",
    4: "#164e63"
  },
  dark: {
    1: "#5da7ad",
    2: "#3f8793",
    3: "#256a78",
    4: "#0f4655"
  }
};

export const COMMUNE_QUARTILE_MISSING: Record<"light" | "dark", string> = {
  light: "#edf1f4",
  dark: "#222a31"
};

/** Matriz bivariada 4×2: cuartil IGVUST oficial × avalúo contra mediana regional.
 *
 *  `qv=1` es MAYOR vulnerabilidad y se conserva como cuartil oficial. El eje de
 *  avalúo se corta en dos columnas: `avm2` bajo/igual a la mediana regional activa
 *  y `avm2` sobre esa mediana. La comparación usa el valor directo del shard UV.
 *
 *  Las claves son `"<qv><avaluo>"`. La celda 12 (mayor vulnerabilidad + mayor
 *  avalúo/m²) es el foco oscuro; las demás quedan deliberadamente transparentes.
 */
export const BIVARIATE_PALETTE: Record<"light" | "dark", Record<string, string>> = {
  light: {
    "11": "#f5a8bd", "12": "#8e0f4e",
    "21": "#d59ae0", "22": "#6a1a70",
    "31": "#9db5f2", "32": "#4a3a9e",
    "41": "#7ad4f7", "42": "#0b7ab5"
  },
  dark: {
    "11": "#d98fa8", "12": "#8f2158",
    "21": "#bd8ac9", "22": "#6d2b7d",
    "31": "#8fa3dd", "32": "#454099",
    "41": "#6fbde0", "42": "#1f6fa8"
  }
};

/** Color de una UV sin cuartil calculable: sin hogares RSH o sin predios. */
export const BIVARIATE_MISSING: Record<"light" | "dark", string> = {
  light: "#f1f4f7",
  dark: "#252b33"
};

function avm2RegionalClassExpression(regionalMedianAvm2: number | null | undefined): unknown[] {
  if (!Number.isFinite(regionalMedianAvm2) || Number(regionalMedianAvm2) <= 0) return ["literal", "x"];
  const value = ["to-number", ["get", "avm2"], -1];
  return [
    "case",
    ["all", [">", value, 0], ["<=", value, Number(regionalMedianAvm2)]], "1",
    [">", value, Number(regionalMedianAvm2)], "2",
    "x"
  ];
}

export function communeQuartileFillExpression(
  theme: "light" | "dark" = "light",
  quartilesByCommune: Record<string, 1 | 2 | 3 | 4 | null> = {}
): unknown[] {
  const palette = COMMUNE_QUARTILE_PALETTE[theme];
  const expression: unknown[] = ["match", ["to-string", ["get", "cod_comuna"]]];
  for (const [code, quartile] of Object.entries(quartilesByCommune)) {
    if (quartile !== 1 && quartile !== 2 && quartile !== 3 && quartile !== 4) continue;
    const labels = new Set([code, code.startsWith("0") ? code.slice(1) : code.padStart(5, "0")]);
    for (const label of labels) expression.push(label, palette[quartile]);
  }
  expression.push(COMMUNE_QUARTILE_MISSING[theme]);
  return expression;
}

/**
 * Expresión `match` de MapLibre para el relleno bivariado.
 *
 * Es una función pura sobre el tema: no toca el mapa, así que se puede testear
 * sin instanciar MapLibre ni un canvas.
 */
export function bivariateFillExpression(
  theme: "light" | "dark" = "light",
  regionalMedianAvm2: number | null = null
): unknown[] {
  const palette = BIVARIATE_PALETTE[theme];
  const expression: unknown[] = [
    "match",
    ["concat", ["to-string", ["get", "qv"]], avm2RegionalClassExpression(regionalMedianAvm2)]
  ];
  for (const [cell, color] of Object.entries(palette)) {
    expression.push(cell, color);
  }
  expression.push(BIVARIATE_MISSING[theme]);
  return expression;
}

export function sourceAttribution(source: TileSource): string {
  return source.attribution ?? "Fuente cartográfica: 3 Cucharadas.";
}

export function addPmtilesSource(
  map: maplibregl.Map,
  id: string,
  source: TileSource,
  url: string
): void {
  if (map.getSource(id)) map.removeSource(id);
  map.addSource(id, {
    type: "vector",
    url: `pmtiles://${url}`,
    minzoom: source.minzoom,
    maxzoom: source.maxzoom,
    attribution: sourceAttribution(source)
  });
}

export function addCommuneLayers(
  map: maplibregl.Map,
  source: TileSource,
  beforeId?: string,
  fillColor: unknown = communeQuartileFillExpression()
): void {
  if (map.getLayer(COMMUNE_FILL_ID)) return;
  map.addLayer({
    id: COMMUNE_FILL_ID,
    type: "fill",
    source: COMMUNE_SOURCE_ID,
    "source-layer": source.source_layer,
    paint: {
      "fill-color": fillColor as never,
      "fill-opacity": ["interpolate", ["linear"], ["zoom"], 3, 0.78, 10, 0.62, 14, 0.42]
    }
  }, beforeId);
  map.addLayer({
    id: COMMUNE_LINE_ID,
    type: "line",
    source: COMMUNE_SOURCE_ID,
    "source-layer": source.source_layer,
    // El borde sí orienta a zoom alto —dice dónde termina la comuna— y no lava color.
    paint: { "line-color": "#5f7786", "line-opacity": 0.65, "line-width": 0.75 }
  }, beforeId);
}

/** Capa de Unidades Vecinales. Fuente GeoJSON same-origin, cargada por comuna. */
export function addUvLayers(
  map: maplibregl.Map,
  theme: "light" | "dark" = "light",
  regionalMedianAvm2: number | null = null,
  beforeId?: string,
  layerStyle: UvLayerStyle = "bivariate"
): void {
  if (map.getLayer(UV_FILL_ID)) return;
  map.addLayer({
    id: UV_FILL_ID,
    type: "fill",
    source: UV_SOURCE_ID,
    paint: {
      "fill-color": (layerStyle === "simple"
        ? UV_SIMPLE_BLUE
        : bivariateFillExpression(theme, regionalMedianAvm2)) as never,
      "fill-opacity": layerStyle === "simple" ? 0.12 : 0.62
    }
  }, beforeId);
  map.addLayer({
    id: UV_LINE_ID,
    type: "line",
    source: UV_SOURCE_ID,
    paint: {
      "line-color": UV_SIMPLE_BLUE,
      "line-opacity": layerStyle === "simple" ? 0.94 : 0.68,
      "line-width": layerStyle === "simple"
        ? ["interpolate", ["linear"], ["zoom"], 10, 1.1, 13, 1.8, 16, 2.55]
        : ["interpolate", ["linear"], ["zoom"], 10, 0.65, 13, 0.95, 16, 1.45]
    }
  }, beforeId);
}

/** Actualiza sólo la expresión de relleno cuando cambia tema o denominador. */
export function updateUvFillExpression(
  map: maplibregl.Map,
  theme: "light" | "dark",
  regionalMedianAvm2: number | null,
  layerStyle: UvLayerStyle = "bivariate"
): void {
  if (!map.getLayer(UV_FILL_ID)) return;
  map.setPaintProperty(
    UV_FILL_ID,
    "fill-color",
    (layerStyle === "simple" ? UV_SIMPLE_BLUE : bivariateFillExpression(theme, regionalMedianAvm2)) as never
  );
  map.setPaintProperty(UV_FILL_ID, "fill-opacity", layerStyle === "simple" ? 0.12 : 0.62);
  map.setPaintProperty(UV_LINE_ID, "line-color", UV_SIMPLE_BLUE);
  map.setPaintProperty(UV_LINE_ID, "line-opacity", layerStyle === "simple" ? 0.94 : 0.68);
}

export function removeUvLayers(map: maplibregl.Map): void {
  for (const id of [UV_FILL_ID, UV_LINE_ID]) {
    if (map.getLayer(id)) map.removeLayer(id);
  }
  if (map.getSource(UV_SOURCE_ID)) map.removeSource(UV_SOURCE_ID);
}

export function removeParcelLayers(map: maplibregl.Map): void {
  for (const id of [PARCEL_FILL_ID, PARCEL_LINE_ID]) {
    if (map.getLayer(id)) map.removeLayer(id);
  }
  if (map.getSource(PARCEL_SOURCE_ID)) map.removeSource(PARCEL_SOURCE_ID);
}

export function addParcelLayers(map: maplibregl.Map, source: TileSource, opacity: number, beforeId?: string): void {
  const fillOpacity = Math.max(0.055, Math.min(opacity, 0.11));
  map.addLayer({
    id: PARCEL_FILL_ID,
    type: "fill",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: {
      "fill-color": PARCEL_FILL_ORANGE,
      "fill-opacity": fillOpacity
    }
  }, beforeId);
  map.addLayer({
    id: PARCEL_LINE_ID,
    type: "line",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: {
      "line-color": PARCEL_LINE_ORANGE,
      "line-opacity": 0.94,
      "line-width": ["interpolate", ["linear"], ["zoom"], 13, 0.34, 16, 0.62, 18, 0.92]
    }
  }, beforeId);
}
