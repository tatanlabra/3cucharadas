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

/** Matriz bivariada 4×4: cuartil de vulnerabilidad (qv) × cuartil de avalúo (qa).
 *
 *  Generada por interpolación bilineal entre cuatro esquinas con significado, no
 *  elegida a ojo. `qv=1` es MAYOR vulnerabilidad (convención MDSF) y `qa=4` mayor
 *  avalúo por hogar, así que la celda `14` —territorio muy vulnerable donde el
 *  catastro registra mucho valor— es la contradicción que el mapa busca mostrar y
 *  recibe el color más saliente del conjunto.
 *
 *  Las claves son `"<qv><qa>"`. Ambos modos se validaron contra su propia
 *  superficie; el modo oscuro tiene menos separación entre celdas adyacentes, por
 *  eso la leyenda y el popup nunca son opcionales.
 */
export const BIVARIATE_PALETTE: Record<"light" | "dark", Record<string, string>> = {
  light: {
    "11": "#c94f3d", "12": "#ae4551", "13": "#8d3961", "14": "#5b2a6e",
    "21": "#d49891", "22": "#b58694", "23": "#8e6e98", "24": "#4f4f9b",
    "31": "#dec4be", "32": "#bcacbd", "33": "#908ebd", "34": "#3f66bc",
    "41": "#e8e6e1", "42": "#c3cadd", "43": "#91a7da", "44": "#2a78d6"
  },
  dark: {
    "11": "#e0705c", "12": "#ce708a", "13": "#b96faa", "14": "#a06fc4",
    "21": "#bd6252", "22": "#b06d8d", "23": "#a077b3", "24": "#8e7fd1",
    "31": "#8f5146", "32": "#886a91", "33": "#817dbc", "34": "#788ddd",
    "41": "#3a3a37", "42": "#476794", "43": "#5284c4", "44": "#5b9ae8"
  }
};

/** Color de una UV sin cuartil calculable: sin hogares RSH o sin predios. */
export const BIVARIATE_MISSING: Record<"light" | "dark", string> = {
  light: "#f0efec",
  dark: "#2b2b29"
};

/**
 * Expresión `match` de MapLibre para el relleno bivariado.
 *
 * Es una función pura sobre el tema: no toca el mapa, así que se puede testear
 * sin instanciar MapLibre ni un canvas.
 */
export function bivariateFillExpression(theme: "light" | "dark" = "light"): unknown[] {
  const palette = BIVARIATE_PALETTE[theme];
  const expression: unknown[] = [
    "match",
    ["concat", ["to-string", ["get", "qv"]], ["to-string", ["get", "qa"]]]
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

export function addCommuneLayers(map: maplibregl.Map, source: TileSource, beforeId?: string): void {
  if (map.getLayer(COMMUNE_FILL_ID)) return;
  map.addLayer({
    id: COMMUNE_FILL_ID,
    type: "fill",
    source: COMMUNE_SOURCE_ID,
    "source-layer": source.source_layer,
    paint: {
      "fill-color": [
        "case",
        ["!", ["has", "cobertura_censo_pct"]], "#98a7b0",
        ["<", ["get", "cobertura_censo_pct"], 80], "#b8c8d2",
        ["<", ["get", "cobertura_censo_pct"], 100], "#9bbbc1",
        ["<", ["get", "cobertura_censo_pct"], 120], "#6f9fa7",
        "#4e7f89"
      ],
      // La fuente comunal corta en z12; más allá MapLibre sobre-escala esa tesela y el
      // relleno cubre el viewport completo con un velo plano que no distingue nada y
      // apaga el basemap y los predios. Se desvanece justo donde entra la capa predial
      // (z13). La capa sigue existiendo: mantiene el click de selección comunal.
      "fill-opacity": ["interpolate", ["linear"], ["zoom"], 11, 0.28, 13, 0.05, 14, 0]
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
  beforeId?: string
): void {
  if (map.getLayer(UV_FILL_ID)) return;
  map.addLayer({
    id: UV_FILL_ID,
    type: "fill",
    source: UV_SOURCE_ID,
    paint: {
      "fill-color": bivariateFillExpression(theme) as never,
      "fill-opacity": 0.72
    }
  }, beforeId);
  map.addLayer({
    id: UV_LINE_ID,
    type: "line",
    source: UV_SOURCE_ID,
    paint: { "line-color": "#3c4a52", "line-opacity": 0.55, "line-width": 0.6 }
  }, beforeId);
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
  map.addLayer({
    id: PARCEL_FILL_ID,
    type: "fill",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: {
      "fill-color": [
        "interpolate", ["linear"], ["to-number", ["get", "avaluo_fiscal_clp"], 0],
        0, "#d6e3e7", 25_000_000, "#94b8c7", 100_000_000, "#3d7896"
      ],
      "fill-opacity": Math.max(opacity, 0.52)
    }
  }, beforeId);
  map.addLayer({
    id: PARCEL_LINE_ID,
    type: "line",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: { "line-color": "#315f78", "line-opacity": 0.82, "line-width": 0.65 }
  }, beforeId);
}
