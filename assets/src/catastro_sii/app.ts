import "maplibre-gl/dist/maplibre-gl.css";
import { defaultAuthorizedParcelRegion } from "./availability";
import { MapController } from "./map";
import { manifestUrlForLocation } from "./preview";
import { regionCodeForName, replaceUrl, stateFromUrl, toDataCommuneCode } from "./state";
import type { AppState, Bounds, CommuneRecord, TilesManifest } from "./types";

const communesUrl = "/catastro_sii_brecha/data/comunas.json";

type TerritoryIndex = { communes?: Record<string, { bounds?: [number, number, number, number] }> };

function setStatus(message: string): void {
  const element = document.getElementById("map-status");
  if (element) element.textContent = message;
}

async function json<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
  return response.json() as Promise<T>;
}

export class CatastroMapApplication {
  private state: AppState;
  private map: MapController | null = null;

  private constructor(private readonly manifest: TilesManifest, private readonly rows: CommuneRecord[]) {
    this.state = stateFromUrl(rows);
  }

  static async start(): Promise<CatastroMapApplication> {
    const manifestUrl = manifestUrlForLocation(window.location.hostname, window.location.search);
    const [manifest, rows] = await Promise.all([json<TilesManifest>(manifestUrl), json<CommuneRecord[]>(communesUrl)]);
    const territories: TerritoryIndex = manifest.communes.territories_url
      ? await json<TerritoryIndex>(manifest.communes.territories_url).catch(() => ({ communes: {} }))
      : { communes: {} };
    const boundsByCommune = territories.communes ?? {};
    const enriched = rows.map((row) => ({ ...row, bounds: boundsByCommune[row.codigo_comuna.padStart(5, "0")]?.bounds ?? null }));
    return new CatastroMapApplication(manifest, enriched);
  }

  async mount(): Promise<void> {
    const container = document.getElementById("map");
    if (!container) return;
    container.classList.add("catastro-maplibre");
    this.map = await MapController.create(this.manifest, container);
    const mapShell = container.closest(".map-shell");
    mapShell?.classList.add("map-ready");
    const communesAdded = this.map.addCommunes((code) => this.selectFromMap(code));
    if (communesAdded) setStatus("Capa comunal nacional lista. Elige una región o comuna para explorar.");
    else setStatus("La capa comunal PMTiles aún no está disponible en este manifest.");

    window.addEventListener("catastro:selection", (event) => {
      const row = (event as CustomEvent<{ row?: CommuneRecord }>).detail?.row;
      if (row) this.selectRow(row);
    });
    window.addEventListener("catastro:legacy-ready", (event) => {
      const row = (event as CustomEvent<{ selected?: CommuneRecord }>).detail?.selected;
      if (row) this.selectRow(row);
    });
    window.addEventListener("resize", () => this.map?.resize());
    this.applyInitialSelection();
  }

  private applyInitialSelection(): void {
    const selector = document.getElementById("comuna");
    const selectedCode = this.state.communeCode
      ?? (selector instanceof HTMLSelectElement ? toDataCommuneCode(selector.value) : null);
    if (!selectedCode) {
      this.activateDefaultParcelPilot();
      return;
    }
    const row = this.rows.find((entry) => entry.codigo_comuna === selectedCode);
    if (row) this.selectRow(row);
  }

  private selectFromMap(code: string): void {
    const row = this.rows.find((entry) => entry.codigo_comuna === toDataCommuneCode(code));
    if (!row) return;
    const region = document.getElementById("region");
    const commune = document.getElementById("comuna");
    if (region instanceof HTMLSelectElement && commune instanceof HTMLSelectElement) {
      region.value = row.region;
      region.dispatchEvent(new Event("change", { bubbles: true }));
      commune.value = row.codigo_comuna;
      commune.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }
    this.selectRow(row);
  }

  private selectRow(row: CommuneRecord): void {
    this.state.regionCode = regionCodeForName(row.region);
    this.state.communeCode = row.codigo_comuna;
    replaceUrl(this.state);
    this.map?.setCommuneFilter(this.state.communeCode.padStart(5, "0"));
    this.map?.fitBounds(row.bounds, 13);
    this.map?.setParcelLayer(this.state);
  }

  private activateDefaultParcelPilot(): boolean {
    const regionCode = defaultAuthorizedParcelRegion(this.manifest);
    if (!regionCode) return false;
    const entry = this.manifest.parcel_regions[regionCode];
    this.state.regionCode = regionCode;
    this.state.communeCode = null;
    this.state.parcelLayerVisible = true;
    replaceUrl(this.state);
    const selected = this.rows.filter((row) => entry.communes?.includes(row.codigo_comuna.padStart(5, "0")));
    const bounds = selected.reduce<Bounds | null>((combined, row) => {
      if (!row.bounds) return combined;
      if (!combined) return [...row.bounds];
      return [
        Math.min(combined[0], row.bounds[0]), Math.min(combined[1], row.bounds[1]),
        Math.max(combined[2], row.bounds[2]), Math.max(combined[3], row.bounds[3])
      ];
    }, null);
    this.map?.fitBounds(bounds, 10);
    const loaded = this.map?.setParcelLayer(this.state) ?? false;
    if (loaded) setStatus(`${entry.scope ?? "Piloto regional"} visible por defecto. Cartografía referencial.`);
    return loaded;
  }
}
