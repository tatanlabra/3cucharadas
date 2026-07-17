(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const config = window.CATASTRO_MAP_CONFIG || {};
  const state = { communes: [], regions: [], selected: null, map: null, cells: null, requestId: 0 };
  const number = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
  const pct = (value) => value == null ? "No disponible" : `${Number(value).toLocaleString("es-CL", { maximumFractionDigits: 1 })}%`;
  const money = (value) => value == null ? "No disponible" : `$${number.format(value)}`;
  const set = (selector, value) => {
    const element = $(selector);
    if (element) element.textContent = value;
  };

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const tag = document.createElement("script");
      tag.src = src;
      tag.onload = resolve;
      tag.onerror = reject;
      document.head.append(tag);
    });
  }

  function loadStyle(href) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`link[data-maplibre-css="${href}"]`)) return resolve();
      const tag = document.createElement("link");
      tag.rel = "stylesheet";
      tag.href = href;
      tag.dataset.maplibreCss = href;
      tag.onload = resolve;
      tag.onerror = reject;
      document.head.append(tag);
    });
  }

  async function initialiseMap() {
    if (!config.maptilerKey || !config.maplibreScript) {
      const selected = state.selected;
      set("#map-status", selected
        ? `Celdas agregadas para ${selected.comuna}; fondo OSM aún no configurado.`
        : "Capa agregada en modo local; fondo OSM aún no configurado.");
      return;
    }
    try {
      if (config.maplibreCss) await loadStyle(config.maplibreCss);
      if (!window.maplibregl) await loadScript(config.maplibreScript);
      const style = config.styleUrl.replace("{key}", encodeURIComponent(config.maptilerKey));
      state.map = new window.maplibregl.Map({
        container: "map",
        style,
        center: [-71, -33],
        zoom: 4,
        attributionControl: true
      });
      state.map.addControl(new window.maplibregl.NavigationControl({ showCompass: false }), "top-right");
      state.map.on("load", () => {
        set("#attribution", "© OpenStreetMap contributors · © MapTiler");
        set("#map-status", "Fondo OSM activo; la luz neón sigue mostrando celdas agregadas.");
        $("#map")?.closest(".map-shell")?.classList.add("map-ready");
        if (state.cells) renderMapLibre(state.cells);
      });
    } catch (_) {
      set("#map-note", "Fondo cartográfico no disponible; se mantiene la capa agregada.");
      set("#map-status", "La vista agregada sigue disponible sin fondo cartográfico.");
    }
  }

  function cellCenter(cell, zoom) {
    const n = 2 ** zoom;
    const lon = ((cell[0] + 0.5) / n) * 360 - 180;
    const lat = Math.atan(Math.sinh(Math.PI * (1 - 2 * ((cell[1] + 0.5) / n)))) * 180 / Math.PI;
    return [lon, lat];
  }

  function renderMapLibre(data) {
    if (!state.map || !state.map.isStyleLoaded() || !data.cells.length) return;
    const features = data.cells.map((cell) => ({
      type: "Feature",
      properties: { n: cell[2] },
      geometry: { type: "Point", coordinates: cellCenter(cell, data.zoom) }
    }));
    const source = { type: "geojson", data: { type: "FeatureCollection", features } };
    if (state.map.getLayer("density-cells")) state.map.removeLayer("density-cells");
    if (state.map.getSource("density-cells")) state.map.removeSource("density-cells");
    state.map.addSource("density-cells", source);
    state.map.addLayer({
      id: "density-cells",
      type: "circle",
      source: "density-cells",
      paint: {
        "circle-color": "#b8ff3c",
        "circle-opacity": 0.72,
        "circle-blur": 0.32,
        "circle-radius": ["interpolate", ["linear"], ["ln", ["get", "n"]], 0, 2, 9, 12]
      }
    });
    const coordinates = features.map((feature) => feature.geometry.coordinates);
    const bounds = coordinates.reduce((box, point) => box.extend(point), new window.maplibregl.LngLatBounds(coordinates[0], coordinates[0]));
    state.map.fitBounds(bounds, { padding: 52, duration: 450, maxZoom: 13 });
  }

  function renderCanvas(data) {
    const canvas = $("#density");
    const host = canvas.parentElement;
    const width = host.clientWidth;
    const height = host.clientHeight;
    const ratio = window.devicePixelRatio || 1;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    const context = canvas.getContext("2d");
    context.scale(ratio, ratio);
    context.clearRect(0, 0, width, height);
    if (!data.cells.length) return;

    const xs = data.cells.map((cell) => cell[0]);
    const ys = data.cells.map((cell) => cell[1]);
    const pad = Math.max(12, Math.min(width, height) * 0.08);
    const xmin = Math.min(...xs);
    const xmax = Math.max(...xs);
    const ymin = Math.min(...ys);
    const ymax = Math.max(...ys);
    const dx = Math.max(1, xmax - xmin);
    const dy = Math.max(1, ymax - ymin);
    const max = Math.max(...data.cells.map((cell) => cell[2]));

    for (const [x, y, count] of data.cells) {
      const px = pad + ((x - xmin) / dx) * (width - pad * 2);
      const py = pad + ((y - ymin) / dy) * (height - pad * 2);
      const radius = 1.5 + Math.sqrt(count / max) * 10;
      const glow = context.createRadialGradient(px, py, 0, px, py, radius * 2.5);
      glow.addColorStop(0, "rgba(184,255,60,.9)");
      glow.addColorStop(1, "rgba(184,255,60,0)");
      context.fillStyle = glow;
      context.beginPath();
      context.arc(px, py, radius * 2.5, 0, Math.PI * 2);
      context.fill();
    }
  }

  function flashMetrics() {
    const grid = $(".metric-grid");
    if (!grid || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    grid.classList.remove("refresh");
    void grid.offsetWidth;
    grid.classList.add("refresh");
  }

  function updateMetrics(row) {
    set("#territory", row.comuna);
    set("#coverage", pct(row.cobertura_censo_pct));
    set("#population", number.format(row.poblacion_censo_2024));
    set("#records", number.format(row.predios_habitacionales));
    set("#coordinates", pct(row.cobertura_coordenadas_pct));
    set("#surface", row.superficie_total_m2 == null ? "No disponible" : `${number.format(row.superficie_total_m2)} m²`);
    set("#assessment", money(row.avaluo_total_clp));
    set("#assessment-percentile", pct(row.percentil_avaluo_nacional));
    set("#historical", pct(row.cobertura_vs_proyeccion_base_2017_pct));
    set("#casen", row.casen_sensibilidad_disponible ? pct(row.cobertura_casen_sensibilidad_pct) : "No disponible");
    set("#casen-note", row.casen_nota);
    set("#finding", row.hallazgo);
    set("#status", `${row.region} · ${row.fuente_sii_disponible ? "extracto SII disponible" : "sin extracto SII en el corte"}`);
    set("#map-status", `Celdas agregadas para ${row.comuna}, ${row.region}.`);
    flashMetrics();
  }

  function updateNationalSummary(rows) {
    const records = rows.reduce((total, row) => total + (row.predios_habitacionales || 0), 0);
    const mapped = rows.reduce((total, row) => total + (row.predios_habitacionales_mapeados || 0), 0);
    set("#national-records", number.format(records));
    set("#national-communes", number.format(rows.length));
    set("#national-coordinate-coverage", pct(records ? (mapped / records) * 100 : null));
  }

  async function selectCommune(code) {
    const row = state.communes.find((item) => item.codigo_comuna === code);
    if (!row) return;
    const requestId = ++state.requestId;
    state.selected = row;
    $("#comuna").value = code;
    updateMetrics(row);
    set("#map-note", "Cargando celdas agregadas…");
    try {
      const response = await fetch(`data/${row.mapa.path}`, { cache: "force-cache" });
      if (!response.ok) throw new Error("mapa no disponible");
      const cells = await response.json();
      if (requestId !== state.requestId) return;
      state.cells = cells;
      renderCanvas(cells);
      renderMapLibre(cells);
      set("#map-note", `${number.format(cells.cells.length)} celdas agregadas · zoom ${cells.zoom}`);
    } catch (_) {
      if (requestId !== state.requestId) return;
      state.cells = { cells: [], zoom: 0 };
      renderCanvas(state.cells);
      set("#map-note", "No fue posible cargar la capa de celdas.");
      set("#map-status", "La ficha comunal se mantiene, pero la capa de celdas no está disponible.");
    }
  }

  function populateCommunes(region, selectedCode) {
    const select = $("#comuna");
    const rows = state.communes.filter((row) => row.region === region).sort((a, b) => a.comuna.localeCompare(b.comuna, "es"));
    select.innerHTML = "";
    for (const row of rows) {
      const option = document.createElement("option");
      option.value = row.codigo_comuna;
      option.textContent = row.comuna;
      select.append(option);
    }
    select.disabled = !rows.length;
    if (rows.length) {
      const initial = selectedCode && rows.some((row) => row.codigo_comuna === selectedCode) ? selectedCode : rows[0].codigo_comuna;
      selectCommune(initial);
    }
  }

  async function boot() {
    try {
      const [manifest, communes, regions] = await Promise.all([
        fetch("data/manifest.json"),
        fetch("data/comunas.json"),
        fetch("data/regiones.json")
      ]);
      if (![manifest, communes, regions].every((response) => response.ok)) throw new Error("datos incompletos");
      state.communes = await communes.json();
      state.regions = await regions.json();
      updateNationalSummary(state.communes);

      const regionSelect = $("#region");
      regionSelect.innerHTML = "";
      for (const region of state.regions) {
        const option = document.createElement("option");
        option.value = region.region;
        option.textContent = `${region.region} (${region.comunas})`;
        regionSelect.append(option);
      }
      regionSelect.addEventListener("change", () => populateCommunes(regionSelect.value));
      $("#comuna").addEventListener("change", (event) => selectCommune(event.target.value));
      populateCommunes(regionSelect.value);
      await initialiseMap();
      window.addEventListener("resize", () => {
        if (state.cells && !state.map) renderCanvas(state.cells);
        if (state.map) state.map.resize();
      });
    } catch (_) {
      set("#status", "No se pudieron cargar los datos. Reintenta o revisa la metodología.");
      set("#map-note", "Modo degradado: datos no disponibles.");
      set("#map-status", "No fue posible preparar la capa agregada.");
    }
  }

  boot();
})();
