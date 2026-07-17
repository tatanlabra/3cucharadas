(() => {
  "use strict";
  const $ = (selector) => document.querySelector(selector);
  const config = window.CATASTRO_MAP_CONFIG || {};
  const state = { communes: [], regions: [], selected: null, map: null, cells: null };
  const number = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
  const pct = (value) => value == null ? "No disponible" : `${Number(value).toLocaleString("es-CL", { maximumFractionDigits: 1 })}%`;
  const money = (value) => value == null ? "No disponible" : `$${number.format(value)}`;
  const set = (id, value) => { $(id).textContent = value; };

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const tag = document.createElement("script"); tag.src = src; tag.onload = resolve; tag.onerror = reject; document.head.append(tag);
    });
  }

  async function initialiseMap() {
    if (!config.maptilerKey || !config.maplibreScript) return;
    try {
      if (!window.maplibregl) await loadScript(config.maplibreScript);
      const style = config.styleUrl.replace("{key}", encodeURIComponent(config.maptilerKey));
      state.map = new window.maplibregl.Map({ container: "map", style, center: [-71, -33], zoom: 4, attributionControl: true });
      state.map.addControl(new window.maplibregl.NavigationControl({ showCompass: false }), "top-right");
      state.map.on("load", () => { set("#attribution", "© OpenStreetMap contributors · © MapTiler"); if (state.cells) renderMapLibre(state.cells); });
    } catch (_) { set("#map-note", "Fondo cartográfico no disponible; se mantiene la capa agregada."); }
  }

  function cellCenter(cell, zoom) {
    const n = 2 ** zoom, lon = ((cell[0] + .5) / n) * 360 - 180;
    const lat = Math.atan(Math.sinh(Math.PI * (1 - 2 * ((cell[1] + .5) / n)))) * 180 / Math.PI;
    return [lon, lat];
  }

  function renderMapLibre(data) {
    if (!state.map || !state.map.isStyleLoaded()) return;
    const features = data.cells.map((cell) => ({ type: "Feature", properties: { n: cell[2] }, geometry: { type: "Point", coordinates: cellCenter(cell, data.zoom) } }));
    const source = { type: "geojson", data: { type: "FeatureCollection", features } };
    if (state.map.getLayer("density-cells")) state.map.removeLayer("density-cells");
    if (state.map.getSource("density-cells")) state.map.removeSource("density-cells");
    state.map.addSource("density-cells", source);
    state.map.addLayer({ id: "density-cells", type: "circle", source: "density-cells", paint: { "circle-color": "#b8ff3c", "circle-opacity": .72, "circle-blur": .32, "circle-radius": ["interpolate", ["linear"], ["ln", ["get", "n"]], 0, 2, 9, 12] } });
    if (features.length) {
      const coords = features.map((feature) => feature.geometry.coordinates);
      const bounds = coords.reduce((box, point) => box.extend(point), new window.maplibregl.LngLatBounds(coords[0], coords[0]));
      state.map.fitBounds(bounds, { padding: 52, duration: 450, maxZoom: 13 });
    }
  }

  function renderCanvas(data) {
    const canvas = $("#density"), host = canvas.parentElement, width = host.clientWidth, height = host.clientHeight, ratio = window.devicePixelRatio || 1;
    canvas.width = width * ratio; canvas.height = height * ratio; canvas.style.width = `${width}px`; canvas.style.height = `${height}px`;
    const ctx = canvas.getContext("2d"); ctx.scale(ratio, ratio); ctx.clearRect(0, 0, width, height);
    if (!data.cells.length) return;
    const xs = data.cells.map((cell) => cell[0]), ys = data.cells.map((cell) => cell[1]);
    const pad = Math.max(12, Math.min(width, height) * .08), xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
    const dx = Math.max(1, xmax - xmin), dy = Math.max(1, ymax - ymin), max = Math.max(...data.cells.map((cell) => cell[2]));
    for (const [x, y, count] of data.cells) {
      const px = pad + ((x - xmin) / dx) * (width - pad * 2), py = pad + ((y - ymin) / dy) * (height - pad * 2);
      const radius = 1.5 + Math.sqrt(count / max) * 10;
      const glow = ctx.createRadialGradient(px, py, 0, px, py, radius * 2.5); glow.addColorStop(0, "rgba(184,255,60,.9)"); glow.addColorStop(1, "rgba(184,255,60,0)");
      ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(px, py, radius * 2.5, 0, Math.PI * 2); ctx.fill();
    }
  }

  function updateMetrics(row) {
    set("#territory", row.comuna);
    set("#coverage", pct(row.cobertura_censo_pct)); set("#population", number.format(row.poblacion_censo_2024)); set("#records", number.format(row.predios_habitacionales));
    set("#coordinates", pct(row.cobertura_coordenadas_pct)); set("#surface", row.superficie_total_m2 == null ? "No disponible" : `${number.format(row.superficie_total_m2)} m²`);
    set("#assessment", money(row.avaluo_total_clp)); set("#assessment-percentile", pct(row.percentil_avaluo_nacional)); set("#historical", pct(row.cobertura_vs_proyeccion_base_2017_pct));
    set("#casen", row.casen_sensibilidad_disponible ? pct(row.cobertura_casen_sensibilidad_pct) : "No disponible"); set("#casen-note", row.casen_nota);
    set("#finding", row.hallazgo); set("#status", `${row.region} · ${row.fuente_sii_disponible ? "extracto SII disponible" : "sin extracto SII en el corte"}`);
  }

  async function selectCommune(code) {
    const row = state.communes.find((item) => item.codigo_comuna === code); if (!row) return;
    state.selected = row; $("#comuna").value = code; updateMetrics(row); set("#map-note", "Cargando celdas agregadas…");
    try {
      const response = await fetch(`data/${row.mapa.path}`, { cache: "force-cache" }); if (!response.ok) throw new Error("mapa no disponible");
      state.cells = await response.json(); renderCanvas(state.cells); renderMapLibre(state.cells); set("#map-note", `${number.format(state.cells.cells.length)} celdas agregadas · zoom ${state.cells.zoom}`);
    } catch (_) { state.cells = { cells: [], zoom: 0 }; renderCanvas(state.cells); set("#map-note", "No fue posible cargar la capa de celdas."); }
  }

  function populateCommunes(region, selectedCode) {
    const select = $("#comuna"), rows = state.communes.filter((row) => row.region === region).sort((a, b) => a.comuna.localeCompare(b.comuna, "es"));
    select.innerHTML = ""; for (const row of rows) { const option = document.createElement("option"); option.value = row.codigo_comuna; option.textContent = row.comuna; select.append(option); }
    select.disabled = !rows.length; if (rows.length) selectCommune(selectedCode && rows.some((row) => row.codigo_comuna === selectedCode) ? selectedCode : rows[0].codigo_comuna);
  }

  async function boot() {
    try {
      const [manifest, communes, regions] = await Promise.all([fetch("data/manifest.json"), fetch("data/comunas.json"), fetch("data/regiones.json")]);
      if (![manifest, communes, regions].every((response) => response.ok)) throw new Error("datos incompletos");
      state.communes = await communes.json(); state.regions = await regions.json(); const regionSelect = $("#region"); regionSelect.innerHTML = "";
      for (const region of state.regions) { const option = document.createElement("option"); option.value = region.region; option.textContent = `${region.region} (${region.comunas})`; regionSelect.append(option); }
      regionSelect.addEventListener("change", () => populateCommunes(regionSelect.value)); $("#comuna").addEventListener("change", (event) => selectCommune(event.target.value));
      populateCommunes(regionSelect.value); await initialiseMap(); window.addEventListener("resize", () => { if (state.cells && !state.map) renderCanvas(state.cells); });
    } catch (_) { set("#status", "No se pudieron cargar los datos. Reintenta o revisa la metodología."); set("#map-note", "Modo degradado: datos no disponibles."); }
  }
  boot();
})();
