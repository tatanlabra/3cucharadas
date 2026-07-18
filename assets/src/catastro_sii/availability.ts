import type { AppState, TileSource, TilesManifest } from "./types";

/** Return a parcel source only after both the legal and territory gates pass. */
export function authorizedParcelSource(manifest: TilesManifest, state: AppState): TileSource | null {
  if (!state.regionCode || manifest.legal_publication_status !== "AUTHORIZED_VECTOR") return null;
  const source = manifest.parcel_regions[state.regionCode];
  return source?.available ? source : null;
}
