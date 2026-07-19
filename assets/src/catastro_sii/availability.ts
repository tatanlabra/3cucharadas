import type { AppState, TileSource, TilesManifest } from "./types";

/** Return a parcel source only after both the legal and territory gates pass. */
export function authorizedParcelSource(manifest: TilesManifest, state: AppState): TileSource | null {
  if (!state.regionCode || manifest.legal_publication_status !== "AUTHORIZED_VECTOR") return null;
  const source = manifest.parcel_regions[state.regionCode];
  if (!source?.available) return null;
  const commune = state.communeCode?.padStart(5, "0");
  if (source.communes?.length && (!commune || !source.communes.includes(commune))) return null;
  return source;
}

export function defaultAuthorizedParcelRegion(manifest: TilesManifest): string | null {
  if (manifest.legal_publication_status !== "AUTHORIZED_VECTOR") return null;
  return Object.entries(manifest.parcel_regions).find(([, source]) => source.available)?.[0] ?? null;
}

/** Shared five-digit commune codes that may load a published parcel map. */
export function authorizedParcelCommuneCodes(manifest: TilesManifest): ReadonlySet<string> {
  const codes = new Set<string>();
  if (manifest.legal_publication_status !== "AUTHORIZED_VECTOR") return codes;
  for (const source of Object.values(manifest.parcel_regions)) {
    if (!source.available) continue;
    for (const code of source.communes ?? []) codes.add(code.padStart(5, "0"));
  }
  return codes;
}
