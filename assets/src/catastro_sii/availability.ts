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

/** Índice de comunas con capa de Unidades Vecinales publicada. */
export interface UvIndex {
  communes: string[];
  generated_at?: string;
}

/**
 * Gate de la capa UV. Es deliberadamente **independiente** del gate predial:
 * `authorizedParcelSource` protege microdato predial bajo autorización legal, mientras
 * que la capa UV solo publica agregados por Unidad Vecinal. Mezclarlos haría que un
 * cambio en la política de una capa moviera silenciosamente la otra.
 *
 * Por lo mismo la disponibilidad vive en su propio índice y no en `parcel_regions`.
 */
export function uvLayerAvailable(index: UvIndex | null, communeCode: string | null): boolean {
  if (!index?.communes?.length || !communeCode) return false;
  return index.communes.includes(communeCode);
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
