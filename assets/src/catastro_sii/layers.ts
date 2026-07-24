import type maplibregl from "maplibre-gl";
import type { TileSource, UvValuationMode } from "./types";

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

/** Matriz bivariada 4×3: cuartil IGVUST oficial × avalúo normalizado.
 *
 *  `qv=1` es MAYOR vulnerabilidad y se conserva como cuartil oficial. Sólo el eje
 *  de avalúo se compacta visualmente: q1=bajo, q2-q3=medio, q4=alto. Así el mapa
 *  mantiene los cuatro tramos IGVUST sin obligar a descifrar 16 tonos casi iguales.
 *
 *  Las claves son `"<qv><avaluo>"`. La celda 13 (mayor vulnerabilidad + mayor
 *  avalúo/m²) es el foco oscuro; las demás quedan deliberadamente transparentes.
 */
export const BIVARIATE_PALETTE: Record<"light" | "dark", Record<string, string>> = {
  light: {
    "11": "#e4e9ed", "12": "#a9a6d8", "13": "#4a245d",
    "21": "#dce9ec", "22": "#8ca9cb", "23": "#555a9d",
    "31": "#d2e7eb", "32": "#6ab3c7", "33": "#247fac",
    "41": "#edf3ef", "42": "#8fccd2", "43": "#1597a7"
  },
  dark: {
    "11": "#6d7481", "12": "#5f5a91", "13": "#2b184d",
    "21": "#5c7480", "22": "#4f6f92", "23": "#3c4685",
    "31": "#435f6b", "32": "#32798f", "33": "#236fa1",
    "41": "#313941", "42": "#28717d", "43": "#1494a5"
  }
};

/** Color de una UV sin cuartil calculable: sin hogares RSH o sin predios. */
export const BIVARIATE_MISSING: Record<"light" | "dark", string> = {
  light: "#f1f4f7",
  dark: "#252b33"
};

export const UV_QUARTILE_PROPERTY: Record<UvValuationMode, "qa_h" | "qa_m2"> = {
  household: "qa_h",
  m2: "qa_m2"
};

function valuationDisplayClassExpression(property: string): unknown[] {
  const value = ["to-number", ["get", property], 0];
  return [
    "case",
    ["==", value, 1], "1",
    ["==", value, 4], "3",
    ["all", [">=", value, 2], ["<=", value, 3]], "2",
    "x"
  ];
}

/**
 * Expresión `match` de MapLibre para el relleno bivariado.
 *
 * Es una función pura sobre el tema: no toca el mapa, así que se puede testear
 * sin instanciar MapLibre ni un canvas.
 */
export function bivariateFillExpression(
  theme: "light" | "dark" = "light",
  valuationMode: UvValuationMode = "household"
): unknown[] {
  const palette = BIVARIATE_PALETTE[theme];
  const quartileProperty = UV_QUARTILE_PROPERTY[valuationMode];
  const expression: unknown[] = [
    "match",
    ["concat", ["to-string", ["get", "qv"]], valuationDisplayClassExpression(quartileProperty)]
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
  valuationMode: UvValuationMode = "household",
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
        : bivariateFillExpression(theme, valuationMode)) as never,
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
  valuationMode: UvValuationMode,
  layerStyle: UvLayerStyle = "bivariate"
): void {
  if (!map.getLayer(UV_FILL_ID)) return;
  map.setPaintProperty(
    UV_FILL_ID,
    "fill-color",
    (layerStyle === "simple" ? UV_SIMPLE_BLUE : bivariateFillExpression(theme, valuationMode)) as never
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
