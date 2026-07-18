import type maplibregl from "maplibre-gl";
import type { TileSource } from "./types";

export const COMMUNE_SOURCE_ID = "catastro-communes";
export const PARCEL_SOURCE_ID = "catastro-parcels";
export const COMMUNE_FILL_ID = "catastro-communes-fill";
export const COMMUNE_LINE_ID = "catastro-communes-line";
export const PARCEL_FILL_ID = "catastro-parcels-fill";
export const PARCEL_LINE_ID = "catastro-parcels-line";

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
    attribution: source.attribution
  });
}

export function addCommuneLayers(map: maplibregl.Map, source: TileSource): void {
  if (map.getLayer(COMMUNE_FILL_ID)) return;
  map.addLayer({
    id: COMMUNE_FILL_ID,
    type: "fill",
    source: COMMUNE_SOURCE_ID,
    "source-layer": source.source_layer,
    paint: {
      "fill-color": [
        "case",
        ["!", ["has", "cobertura_censo_pct"]], "#667085",
        ["<", ["get", "cobertura_censo_pct"], 80], "#4c78a8",
        ["<", ["get", "cobertura_censo_pct"], 100], "#72b7b2",
        ["<", ["get", "cobertura_censo_pct"], 120], "#f2cf5b",
        "#e45756"
      ],
      "fill-opacity": 0.48
    }
  });
  map.addLayer({
    id: COMMUNE_LINE_ID,
    type: "line",
    source: COMMUNE_SOURCE_ID,
    "source-layer": source.source_layer,
    paint: { "line-color": "#d9e6ef", "line-opacity": 0.72, "line-width": 0.75 }
  });
}

export function removeParcelLayers(map: maplibregl.Map): void {
  for (const id of [PARCEL_FILL_ID, PARCEL_LINE_ID]) {
    if (map.getLayer(id)) map.removeLayer(id);
  }
  if (map.getSource(PARCEL_SOURCE_ID)) map.removeSource(PARCEL_SOURCE_ID);
}

export function addParcelLayers(map: maplibregl.Map, source: TileSource, opacity: number): void {
  map.addLayer({
    id: PARCEL_FILL_ID,
    type: "fill",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: { "fill-color": "#ff4fd8", "fill-opacity": opacity }
  });
  map.addLayer({
    id: PARCEL_LINE_ID,
    type: "line",
    source: PARCEL_SOURCE_ID,
    "source-layer": source.source_layer,
    minzoom: source.minzoom,
    paint: { "line-color": "#ffd7f6", "line-opacity": 0.8, "line-width": 0.55 }
  });
}
