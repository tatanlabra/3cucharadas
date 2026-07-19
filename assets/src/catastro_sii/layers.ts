import type maplibregl from "maplibre-gl";
import type { TileSource } from "./types";

export const COMMUNE_SOURCE_ID = "catastro-communes";
export const PARCEL_SOURCE_ID = "catastro-parcels";
export const COMMUNE_FILL_ID = "catastro-communes-fill";
export const COMMUNE_LINE_ID = "catastro-communes-line";
export const PARCEL_FILL_ID = "catastro-parcels-fill";
export const PARCEL_LINE_ID = "catastro-parcels-line";

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
