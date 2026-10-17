import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import maplibreWorkerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import { PMTiles, Protocol } from "pmtiles";
import "./styles.scss";
import { resolveAssetTemplate, resolveOrdinaryAsset } from "./url_helpers";

type Point = {
  role: "closure" | "entry" | "receiver";
  rbd: number;
  name: string;
  event_year: number;
  coordinate_year: number;
  location_lag_years: number;
  latitude: number;
  longitude: number;
  market_segment: string;
  source_url: string;
  coordinate_source_kind?: "official_mineduc" | "official_mineduc_reference" | "osm_historical_site_candidate";
  coordinate_source_label_es?: string;
  coordinate_source_label_en?: string;
  address_evidence?: string;
  official_coordinate_year?: number;
  official_latitude?: number;
  official_longitude?: number;
  official_distance_m?: number;
  audit_url?: string;
};

type Trajectory = {
  branch: "exit" | "entry" | "combined" | "receiver";
  outcome: string;
  relative_year: number;
  calendar_year?: number;
  status: string;
  estimate: number | null;
  units: number;
  regime: string;
};

type Case = {
  id: string;
  case_kind: "systematic" | "author_documented";
  selection_note_es: string;
  selection_note_en: string;
  commune: string;
  event_period: string;
  education_segment: string;
  segment_family: string;
  distance_km: number;
  same_commune: boolean;
  poster_es?: string;
  poster_en?: string;
  points: Point[];
  trajectories: Trajectory[];
};

type Data = { basemap_manifest: string; cases: Case[] };
type Manifest = {
  tiles_base: string;
  basemap: { available: boolean; url: string; style_url: string; attribution: string };
};

maplibregl.setWorkerUrl(maplibreWorkerUrl);

const root = document.querySelector<HTMLElement>("[data-thesis-market-map]");

function absoluteTileUrl(manifest: Manifest, path: string): string {
  return resolveOrdinaryAsset(manifest.tiles_base, path, window.location.origin);
}

function rewriteStyle(style: maplibregl.StyleSpecification, manifest: Manifest): maplibregl.StyleSpecification {
  const copy = structuredClone(style);
  for (const source of Object.values(copy.sources || {})) {
    if (source.type !== "vector" || !("url" in source) || typeof source.url !== "string") continue;
    const url = absoluteTileUrl(manifest, source.url);
    source.url = `pmtiles://${url}`;
    protocol.add(new PMTiles(url));
  }
  if (typeof copy.glyphs === "string" && !/^https?:\/\//.test(copy.glyphs)) {
    copy.glyphs = resolveAssetTemplate(manifest.tiles_base, copy.glyphs);
  }
  if (typeof copy.sprite === "string" && !/^https?:\/\//.test(copy.sprite)) {
    copy.sprite = absoluteTileUrl(manifest, copy.sprite);
  }
  return copy;
}

const protocol = new Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

const OSM_FALLBACK_STYLE: maplibregl.StyleSpecification = {
  version: 8,
  sources: {
    "osm-raster": {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors"
    }
  },
  layers: [
    { id: "background", type: "background", paint: { "background-color": "#eef2f3" } },
    { id: "osm-raster", type: "raster", source: "osm-raster", paint: { "raster-opacity": 1 } }
  ]
};

async function fetchWithTimeout(url: string, init: RequestInit, timeoutMs = 3_000): Promise<Response> {
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } finally {
    window.clearTimeout(timer);
  }
}

function pointCollection(item: Case): GeoJSON.FeatureCollection {
  const points = item.points.flatMap((point) => {
    const primary: GeoJSON.Feature = {
      type: "Feature",
      properties: { ...point },
      geometry: { type: "Point", coordinates: [point.longitude, point.latitude] }
    };
    if (
      point.coordinate_source_kind !== "osm_historical_site_candidate"
      || point.official_latitude === undefined
      || point.official_longitude === undefined
      || point.official_coordinate_year === undefined
    ) return [primary];
    const official: GeoJSON.Feature = {
      type: "Feature",
      properties: {
        ...point,
        name: `${point.name} · punto MINEDUC ${point.official_coordinate_year}`,
        coordinate_source_kind: "official_mineduc_reference",
        coordinate_year: point.official_coordinate_year,
        latitude: point.official_latitude,
        longitude: point.official_longitude,
        source_url: "https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/"
      },
      geometry: { type: "Point", coordinates: [point.official_longitude, point.official_latitude] }
    };
    return [primary, official];
  });
  return {
    type: "FeatureCollection",
    features: points
  };
}

function linkCollection(item: Case): GeoJSON.FeatureCollection {
  const closure = item.points.find((point) => point.role === "closure");
  const counterpart = item.points.find((point) => point.role === "entry" || point.role === "receiver");
  if (!closure || !counterpart) return { type: "FeatureCollection", features: [] };
  return {
    type: "FeatureCollection",
    features: [{
      type: "Feature",
      properties: { distance_km: item.distance_km },
      geometry: {
        type: "LineString",
        coordinates: [[closure.longitude, closure.latitude], [counterpart.longitude, counterpart.latitude]]
      }
    }]
  };
}

function coordinateLabel(point: Point, lang: "es" | "en"): string {
  const year = point.coordinate_year;
  if (point.coordinate_source_kind === "osm_historical_site_candidate") {
    const distance = Math.round(point.official_distance_m || 0);
    return lang === "es"
      ? `Sede histórica candidata OSM · observada en ${year} · ${point.address_evidence || "directorio MINEDUC"} · punto oficial ${point.official_coordinate_year} conservado a ${distance} m`
      : `OSM historical-site candidate · observed in ${year} · ${point.address_evidence || "MINEDUC directory"} · official ${point.official_coordinate_year} point retained ${distance} m away`;
  }
  if (point.coordinate_source_kind === "official_mineduc_reference") {
    return lang === "es"
      ? `Punto oficial MINEDUC ${year} · conservado para contraste; no se usa como sede histórica en la línea`
      : `Official MINEDUC ${year} point · retained for comparison; not used as the historical site in the line`;
  }
  if (point.role === "entry" && point.location_lag_years > 0) {
    return lang === "es"
      ? `Coordenada oficial ${year} · ${point.location_lag_years} años después del evento`
      : `Official ${year} coordinate · ${point.location_lag_years} years after the event`;
  }
  if (point.role === "receiver" && point.location_lag_years > 0) {
    return lang === "es"
      ? `Coordenada oficial ${year} · referencia posterior documentada`
      : `Official ${year} coordinate · documented later reference`;
  }
  return lang === "es" ? `Coordenada oficial ${year}` : `Official ${year} coordinate`;
}

function displayOutcome(value: string, lang: string): string {
  const labels: Record<string, [string, string]> = {
    enrollment_total: ["Matrícula", "Enrolment"],
    initial_sala_cuna: ["Sala cuna", "Nursery"],
    initial_nivel_medio: ["Nivel medio", "Toddler level"],
    initial_transicion: ["Transición", "Pre-primary"],
    initial_heterogeneo: ["Heterogéneo", "Mixed level"],
    simce_relative: ["SIMCE relativo", "Relative SIMCE"],
    admission_core: ["Admisión núcleo", "Core admissions"]
  };
  return (labels[value] || [value, value])[lang === "en" ? 1 : 0];
}

function segmentLabel(value: string, lang: string): string {
  const labels: Record<string, [string, string]> = {
    "initial:transicion": ["Transición inicial", "Pre-primary"],
    basic: ["Educación básica", "Primary"],
    secondary: ["Educación media", "Secondary"]
  };
  return (labels[value] || [value, value])[lang === "en" ? 1 : 0];
}

function roleLabel(role: Point["role"], lang: string): string {
  if (role === "closure") return lang === "es" ? "Cierre" : "Closure";
  if (role === "receiver") return lang === "es" ? "Escuela receptora" : "Receiving school";
  return lang === "es" ? "Apertura compatible" : "Compatible opening";
}

function branchLabel(branch: Trajectory["branch"], lang: string): string {
  if (branch === "exit") return lang === "es" ? "Cierre" : "Closure";
  if (branch === "entry") return lang === "es" ? "Apertura" : "Opening";
  if (branch === "receiver") return lang === "es" ? "Receptora" : "Receiver";
  return lang === "es" ? "Ambas" : "Combined";
}

function appendText(parent: Element, tag: string, text: string, className?: string): HTMLElement {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  parent.append(node);
  return node;
}

async function init(host: HTMLElement): Promise<void> {
  const dataUrl = host.dataset.dataUrl || "/assets/data/thesis-extension-post2/cases.json";
  const lang = document.documentElement.lang.startsWith("en") ? "en" : "es";
  const [dataResponse] = await Promise.all([fetch(dataUrl, { cache: "no-cache" })]);
  if (!dataResponse.ok) throw new Error("datos cartográficos no disponibles");
  const data = await dataResponse.json() as Data;
  const manifestResponse = await fetch(data.basemap_manifest, { cache: "no-cache" });
  if (!manifestResponse.ok) throw new Error("manifiesto cartográfico no disponible");
  const manifest = await manifestResponse.json() as Manifest;
  let basemapMode = "pmtiles";
  let style: maplibregl.StyleSpecification;
  try {
    if (["127.0.0.1", "localhost"].includes(window.location.hostname)) {
      throw new Error("preview local: usar base OSM sin solicitar recursos CORS remotos");
    }
    const styleResponse = await fetchWithTimeout(
      absoluteTileUrl(manifest, manifest.basemap.style_url),
      { cache: "force-cache" }
    );
    if (!styleResponse.ok) throw new Error("estilo cartográfico no disponible");
    style = rewriteStyle(await styleResponse.json() as maplibregl.StyleSpecification, manifest);
  } catch {
    basemapMode = "osm-raster";
    style = OSM_FALLBACK_STYLE;
  }

  const canvas = host.querySelector<HTMLElement>("[data-market-map-canvas]");
  const aside = host.querySelector<HTMLElement>("[data-market-map-aside]");
  const status = host.querySelector<HTMLElement>("[data-market-map-status]");
  const posterLink = host.querySelector<HTMLAnchorElement>("[data-market-map-poster]");
  if (!canvas || !aside || !status || !posterLink) throw new Error("estructura del visor incompleta");

  const map = new maplibregl.Map({
    container: canvas,
    style,
    center: [-70.65, -33.45],
    zoom: 11,
    cooperativeGestures: true,
    attributionControl: true,
    locale: lang === "es" ? {
      "AttributionControl.ToggleAttribution": "Mostrar u ocultar atribución",
      "AttributionControl.MapFeedback": "Comentarios sobre el mapa",
      "Map.Title": "Mapa",
      "Marker.Title": "Marcador del mapa",
      "NavigationControl.ZoomIn": "Acercar",
      "NavigationControl.ZoomOut": "Alejar",
      "NavigationControl.ResetBearing": "Arrastre para rotar; haga clic para orientar al norte",
      "Popup.Close": "Cerrar ventana",
      "CooperativeGesturesHandler.WindowsHelpText": "Use Ctrl y la rueda para acercar el mapa",
      "CooperativeGesturesHandler.MacHelpText": "Use ⌘ y la rueda para acercar el mapa",
      "CooperativeGesturesHandler.MobileHelpText": "Use dos dedos para mover el mapa"
    } : undefined
  });
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
  canvas.setAttribute("role", "region");
  canvas.setAttribute("aria-label", lang === "es" ? "Mapa interactivo de cierres, aperturas y fusiones escolares" : "Interactive map of school closures, openings, and mergers");
  canvas.setAttribute("tabindex", "0");

  await new Promise<void>((resolve, reject) => {
    const timer = window.setTimeout(() => reject(new Error("tiempo de carga agotado")), 20_000);
    map.once("style.load", () => { window.clearTimeout(timer); resolve(); });
  });
  map.addSource("case-links", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
  map.addSource("case-schools", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
  const before = map.getLayer("roads-glow") ? "roads-glow" : undefined;
  map.addLayer({
    id: "case-links",
    type: "line",
    source: "case-links",
    paint: { "line-color": "#16738a", "line-width": 3, "line-dasharray": [2, 2], "line-opacity": .75 }
  }, before);
  map.addLayer({
    id: "case-school-points",
    type: "circle",
    source: "case-schools",
    paint: {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 9, 7, 14, 11],
      "circle-color": ["case", ["==", ["get", "coordinate_source_kind"], "official_mineduc_reference"], "rgba(255,255,255,0.78)", ["match", ["get", "role"], "closure", "#ff4fd8", "receiver", "#37e7ff", "#b8ff3c"]],
      "circle-stroke-color": ["case", ["==", ["get", "coordinate_source_kind"], "official_mineduc_reference"], "#ff4fd8", "#10121d"],
      "circle-stroke-width": ["case", ["==", ["get", "coordinate_source_kind"], "official_mineduc_reference"], 3, 2]
    }
  });
  map.addLayer({
    id: "case-school-labels",
    type: "symbol",
    source: "case-schools",
    minzoom: 10,
    layout: {
      "text-field": ["case", ["==", ["get", "coordinate_source_kind"], "official_mineduc_reference"], "M", ["==", ["get", "role"], "closure"], "C", ["==", ["get", "role"], "receiver"], "R", lang === "es" ? "A" : "O"],
      "text-font": ["Noto Sans Regular"],
      "text-size": 11,
      "text-offset": [0, 1.55],
      "text-anchor": "top",
      "text-allow-overlap": true
    },
    paint: { "text-color": "#172033", "text-halo-color": "#ffffff", "text-halo-width": 1.5 }
  });
  if (map.getSource("protomaps") && !map.getLayer("roads-name-post2")) {
    map.addLayer({
      id: "roads-name-post2",
      type: "symbol",
      source: "protomaps",
      "source-layer": "roads",
      minzoom: 12,
      filter: ["all", ["has", "name"], ["in", ["get", "kind"], ["literal", ["highway", "major_road", "medium_road"]]]],
      layout: {
        "symbol-placement": "line",
        "text-field": ["get", "name"],
        "text-font": ["Noto Sans Regular"],
        "text-size": 11,
        "text-max-angle": 35,
        "text-padding": 10
      },
      paint: { "text-color": "#526078", "text-halo-color": "#ffffff", "text-halo-width": 1.5 }
    });
  }

  map.on("click", "case-school-points", (event) => {
    const props = event.features?.[0]?.properties as Point | undefined;
    if (!props) return;
    const content = document.createElement("div");
    appendText(content, "strong", String(props.name));
    appendText(content, "span", `${roleLabel(props.role, lang)} · RBD ${props.rbd} · ${props.event_year}`);
    appendText(content, "span", coordinateLabel(props, lang));
    new maplibregl.Popup({ maxWidth: "280px" }).setLngLat(event.lngLat).setDOMContent(content).addTo(map);
  });
  map.on("mouseenter", "case-school-points", () => { map.getCanvas().style.cursor = "pointer"; });
  map.on("mouseleave", "case-school-points", () => { map.getCanvas().style.cursor = ""; });

  function selectCase(index: number, animate = true): void {
    const item = data.cases[index];
    if (!item) return;
    const pointData = pointCollection(item);
    (map.getSource("case-schools") as maplibregl.GeoJSONSource).setData(pointData);
    (map.getSource("case-links") as maplibregl.GeoJSONSource).setData(linkCollection(item));
    host.dataset.mapPointCount = String(pointData.features.length);
    const bounds = new maplibregl.LngLatBounds();
    item.points.forEach((point) => bounds.extend([point.longitude, point.latitude]));
    map.fitBounds(bounds, {
      padding: { top: 75, right: 75, bottom: 75, left: 75 },
      maxZoom: 15.5,
      duration: !animate || window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 450
    });
    const center = map.getCenter();
    host.dataset.activeCase = item.id;
    host.dataset.mapCenter = `${center.lat.toFixed(6)},${center.lng.toFixed(6)}`;
    let activeButton: HTMLButtonElement | null = null;
    host.querySelectorAll<HTMLButtonElement>("[data-market-map-tab]").forEach((button, buttonIndex) => {
      button.setAttribute("aria-selected", String(buttonIndex === index));
      button.tabIndex = buttonIndex === index ? 0 : -1;
      if (buttonIndex === index) activeButton = button;
    });
    const panel = host.querySelector<HTMLElement>("[data-market-map-panel]");
    if (panel && activeButton) panel.setAttribute("aria-labelledby", activeButton.id);
    const tabList = activeButton?.closest<HTMLElement>(".territorial-evidence__tabs");
    if (activeButton && tabList) {
      tabList.scrollLeft = Math.max(0, activeButton.offsetLeft - (tabList.clientWidth - activeButton.offsetWidth) / 2);
    }
    aside.replaceChildren();
    appendText(aside, "h4", item.commune);
    const localizedSegment = segmentLabel(item.education_segment, lang);
    appendText(aside, "p", `${item.event_period} · ${localizedSegment}`, "territorial-evidence__meta");
    const facts = document.createElement("dl");
    facts.className = "territorial-evidence__facts";
    const selectionNote = lang === "es" ? item.selection_note_es : item.selection_note_en;
    const distance = item.case_kind === "author_documented"
      ? `≈${item.distance_km.toLocaleString(lang === "es" ? "es-CL" : "en-GB", { maximumFractionDigits: 1 })} km`
      : `${item.distance_km.toLocaleString(lang === "es" ? "es-CL" : "en-GB", { maximumFractionDigits: 3 })} km`;
    const factRows = lang === "es"
      ? [["Distancia", distance], ["Misma comuna", item.same_commune ? "Sí" : "No"], ["Segmento", localizedSegment], ["Selección", selectionNote]]
      : [["Distance", distance], ["Same commune", item.same_commune ? "Yes" : "No"], ["Segment", localizedSegment], ["Selection", selectionNote]];
    for (const [label, value] of factRows) {
      const row = document.createElement("div");
      appendText(row, "dt", label);
      appendText(row, "dd", value);
      facts.append(row);
    }
    aside.append(facts);
    const schools = document.createElement("div");
    schools.className = "territorial-evidence__schools";
    for (const point of item.points) {
      const card = document.createElement("div");
      card.className = "territorial-evidence__school";
      card.dataset.role = point.role;
      appendText(card, "strong", point.name);
      appendText(card, "span", `${roleLabel(point.role, lang)} · RBD ${point.rbd} · ${point.event_year}`);
      appendText(card, "span", coordinateLabel(point, lang));
      schools.append(card);
    }
    aside.append(schools);
    const visibleRows = item.trajectories.filter((row) => row.outcome === "enrollment_total" || (item.segment_family === "initial" && row.outcome === "initial_transicion"));
    const table = document.createElement("table");
    table.className = "territorial-evidence__trajectory";
    const caption = document.createElement("caption");
    caption.textContent = lang === "es"
      ? "Matrícula alrededor del evento en escuelas distintas"
      : "Enrolment around the event in separate schools";
    table.append(caption);
    const head = document.createElement("thead");
    const headRow = document.createElement("tr");
    const usesCalendarYear = visibleRows.some((row) => Number.isInteger(row.calendar_year));
    for (const label of (lang === "es" ? ["Rama", "Indicador", usesCalendarYear ? "Año" : "t", "Valor"] : ["Branch", "Indicator", usesCalendarYear ? "Year" : "t", "Value"])) {
      const cell = appendText(headRow, "th", label);
      cell.setAttribute("scope", "col");
    }
    head.append(headRow);
    table.append(head);
    const body = document.createElement("tbody");
    for (const row of visibleRows) {
      const tr = document.createElement("tr");
      const branch = branchLabel(row.branch, lang);
      const value = row.estimate === null ? (lang === "es" ? "Suprimido" : "Suppressed") : row.estimate.toLocaleString(lang === "es" ? "es-CL" : "en-GB", { maximumFractionDigits: 3 });
      for (const cell of [branch, displayOutcome(row.outcome, lang), String(row.calendar_year ?? row.relative_year), value]) appendText(tr, "td", cell);
      body.append(tr);
    }
    table.append(body);
    aside.append(table);
    const sourceNote = document.createElement("p");
    sourceNote.className = "territorial-evidence__source";
    sourceNote.append(document.createTextNode(lang === "es" ? "Fuentes: directorios MINEDUC y mapa de calles OpenStreetMap." : "Sources: MINEDUC directories and OpenStreetMap street map."));
    if (item.case_kind === "author_documented") {
      sourceNote.append(document.createTextNode(lang === "es" ? " M = punto MINEDUC; C = sede histórica candidata; R = receptora." : " M = MINEDUC point; C = candidate historical site; R = receiver."));
      sourceNote.append(document.createTextNode(lang === "es" ? " Caso documentado: " : " Documented case: "));
      const sourceLinks = lang === "es"
        ? [["registro BCN", "https://www.bcn.cl/laborparlamentaria/documento?id=636175"], ["reglamento institucional", "https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf"]]
        : [["BCN record", "https://www.bcn.cl/laborparlamentaria/documento?id=636175"], ["institutional regulations", "https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf"]];
      sourceLinks.forEach(([label, href], sourceIndex) => {
        if (sourceIndex > 0) sourceNote.append(document.createTextNode(lang === "es" ? " y " : " and "));
        const link = document.createElement("a");
        link.href = href;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = label;
        sourceNote.append(link);
      });
      sourceNote.append(document.createTextNode("."));
    }
    aside.append(sourceNote);
    const poster = lang === "es" ? item.poster_es : item.poster_en;
    const hasDocumentedPoster = item.case_kind === "author_documented" && typeof poster === "string";
    if (hasDocumentedPoster) posterLink.href = poster;
    else posterLink.removeAttribute("href");
    posterLink.hidden = !hasDocumentedPoster;
    posterLink.replaceChildren(document.createTextNode(lang === "es" ? "Abrir la lámina de la fusión documentada" : "Open the documented merger evidence sheet"));
    const externalMark = document.createElement("span");
    externalMark.setAttribute("aria-hidden", "true");
    externalMark.textContent = " ↗";
    posterLink.append(externalMark);
    status.textContent = item.case_kind === "author_documented"
      ? (lang === "es"
        ? `${item.commune}: cierre y fusión documentados; la matrícula agregada no prueba el motivo administrativo.`
        : `${item.commune}: documented closure and merger; aggregate enrolment does not prove the administrative motive.`)
      : !item.same_commune
        ? (lang === "es"
          ? `${item.commune}: la apertura queda fuera de la comuna del cierre; es una selección analítica, no una relación local ni un destino.`
          : `${item.commune}: the opening lies outside the closure's municipality; it is an analytical selection, not a local relationship or destination.`)
      : (lang === "es"
        ? `${item.commune}: cierre y apertura del mismo segmento; la línea indica proximidad, no destino.`
        : `${item.commune}: closure and opening in the same segment; the line shows proximity, not destination.`);
  }

  const tabs = [...host.querySelectorAll<HTMLButtonElement>("[data-market-map-tab]")];
  const updateHash = (index: number): void => {
    const caseId = tabs[index]?.dataset.caseId;
    if (caseId) history.replaceState(null, "", `#territorial-case-${caseId}`);
  };
  tabs.forEach((button, index) => {
    button.addEventListener("click", () => {
      selectCase(index);
      updateHash(index);
    });
    button.addEventListener("keydown", (event) => {
      if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
      event.preventDefault();
      const next = event.key === "Home"
        ? 0
        : event.key === "End"
          ? tabs.length - 1
          : (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      tabs[next].focus();
      selectCase(next);
      updateHash(next);
    });
  });
  const requestedCase = location.hash.match(/^#territorial-case-(.+)$/)?.[1];
  const initialIndex = requestedCase
    ? Math.max(0, tabs.findIndex((button) => button.dataset.caseId === requestedCase))
    : 0;
  host.dataset.requestedCase = requestedCase || "";
  host.dataset.initialCaseIndex = String(initialIndex);
  selectCase(initialIndex, false);
  await new Promise<void>((resolve, reject) => {
    const onError = (event: { error?: Error }) => {
      cleanup();
      reject(event.error || new Error("recurso cartográfico no disponible"));
    };
    const onIdle = () => {
      cleanup();
      resolve();
    };
    const timer = window.setTimeout(() => {
      cleanup();
      reject(new Error("el mapa no alcanzó un estado estable"));
    }, 20_000);
    const cleanup = () => {
      window.clearTimeout(timer);
      map.off("error", onError);
      map.off("idle", onIdle);
    };
    map.on("error", onError);
    map.once("idle", onIdle);
  });
  const tabsContainer = host.querySelector<HTMLElement>("[data-market-map-tabs]");
  const panel = host.querySelector<HTMLElement>("[data-market-map-panel]");
  if (tabsContainer) tabsContainer.hidden = false;
  if (panel) panel.hidden = false;
  host.dataset.mapBasemap = basemapMode;
  host.dataset.mapState = "ready";
  host.dataset.mapLoaded = "true";
  map.resize();
  selectCase(initialIndex, false);
}

if (root) init(root).catch(() => root.dispatchEvent(new CustomEvent("thesis-post2-map:fallback")));
