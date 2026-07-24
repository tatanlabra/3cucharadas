(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const state = { communes: [], regions: [], selected: null, cells: null, requestId: 0, mapCommuneCodes: new Set(), mapRegions: new Set() };
  const number = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
  const pct = (value) => value == null ? "No disponible" : `${Number(value).toLocaleString("es-CL", { maximumFractionDigits: 1 })}%`;
  const money = (value) => value == null ? "No disponible" : `$${number.format(value)}`;
  const DEFAULT_COMMUNE_CODE = "3202";
  const set = (selector, value) => {
    const element = $(selector);
    if (element) element.textContent = value;
  };
  const sharedCode = (code) => String(code).padStart(5, "0");
  const hasPublishedMap = (row) => state.mapCommuneCodes.has(sharedCode(row.codigo_comuna));

  function formatVersionTimestamp(value) {
    if (!value) return "Versión: sin sello de publicación disponible";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "Versión: sin sello de publicación disponible";
    const parts = new Intl.DateTimeFormat("es-CL", {
      timeZone: "America/Santiago",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true
    }).formatToParts(date);
    const valueFor = (type) => parts.find((part) => part.type === type)?.value || "";
    const period = valueFor("dayPeriod").toUpperCase().replace(/[.\s]/g, "") || "AM";
    return `Versión: ${valueFor("day")}/${valueFor("month")}/${valueFor("year")} ${valueFor("hour")}:${valueFor("minute")} ${period}`;
  }

  function formatVersionDate(value) {
    if (!value) return "Versión: sin sello disponible";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "Versión: sin sello disponible";
    const parts = new Intl.DateTimeFormat("es-CL", {
      timeZone: "America/Santiago",
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    }).formatToParts(date);
    const valueFor = (type) => parts.find((part) => part.type === type)?.value || "";
    return `Versión: ${valueFor("day")}/${valueFor("month")}/${valueFor("year")}`;
  }

  function configurePublishedMaps(manifest) {
    const published = manifest?.legal_publication_status === "AUTHORIZED_VECTOR";
    for (const source of Object.values(manifest?.parcel_regions || {})) {
      if (!published || !source?.available || !Array.isArray(source.communes)) continue;
      for (const code of source.communes) state.mapCommuneCodes.add(sharedCode(code));
    }
    for (const row of state.communes) {
      if (hasPublishedMap(row)) state.mapRegions.add(row.region);
    }
    set("#map-version", formatVersionTimestamp(manifest?.generated_at));
    set("#map-version-date", formatVersionDate(manifest?.generated_at));
  }

  function updateMapVisibility(row) {
    // Las 346 comunas tienen capa UV agregada. El gate predial permanece separado:
    // el asterisco sólo informa dónde se puede solicitar ese PMTiles regional.
    const hasPredial = hasPublishedMap(row);
    const eligible = true;
    const section = $("#cartographic-map");
    if (section) section.hidden = false;
    set("#map-availability-note", hasPredial
      ? `* ${row.comuna} tiene piloto predial SII; todas las comunas mantienen su mapa UV agregado.`
      : "* indica disponibilidad predial SII en Caldera o Diego de Almagro. Esta comuna mantiene su mapa UV agregado.");
    window.dispatchEvent(new CustomEvent("catastro:map-eligibility", { detail: { eligible, hasPredial, row } }));
    return eligible;
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
    set("#selection-context", `Ahora estás mirando ${row.comuna}, ${row.region}.`);
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
    const mapEligible = updateMapVisibility(row);
    if (mapEligible) window.dispatchEvent(new CustomEvent("catastro:selection", { detail: { row } }));
    if (!mapEligible) {
      state.cells = null;
      return;
    }
    set("#map-note", "Cargando celdas agregadas…");
    try {
      const response = await fetch(`data/${row.mapa.path}`, { cache: "force-cache" });
      if (!response.ok) throw new Error("mapa no disponible");
      const cells = await response.json();
      if (requestId !== state.requestId) return;
      state.cells = cells;
      renderCanvas(cells);
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
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = rows.length ? "Elige una comuna" : "Elige una región primero";
    select.append(placeholder);
    for (const row of rows) {
      const option = document.createElement("option");
      option.value = row.codigo_comuna;
      option.textContent = `${row.comuna}${hasPublishedMap(row) ? " *" : ""}`;
      select.append(option);
    }
    select.disabled = !rows.length;
    const initial = selectedCode && rows.some((row) => row.codigo_comuna === selectedCode) ? selectedCode : null;
    if (initial) selectCommune(initial);
    else {
      select.value = "";
      set("#selection-context", region ? `Región ${region} lista. Elige una comuna para cargar su UV.` : "Elige una región y una comuna.");
      set("#status", region ? "Sin comuna seleccionada" : "Contexto nacional listo");
    }
  }

  async function boot() {
    try {
      const publishedManifestUrl = window.CATASTRO_MAP_CONFIG?.publishedManifestUrl || "/assets/data/catastro_sii/manifest.json";
      const [manifest, communes, regions, publishedManifest] = await Promise.all([
        fetch("data/manifest.json"),
        fetch("data/comunas.json"),
        fetch("data/regiones.json"),
        fetch(publishedManifestUrl).then((response) => response.ok ? response.json() : null).catch(() => null)
      ]);
      if (![manifest, communes, regions].every((response) => response.ok)) throw new Error("datos incompletos");
      state.communes = await communes.json();
      state.regions = await regions.json();
      configurePublishedMaps(publishedManifest);
      updateNationalSummary(state.communes);

      const regionSelect = $("#region");
      regionSelect.innerHTML = "";
      const regionPlaceholder = document.createElement("option");
      regionPlaceholder.value = "";
      regionPlaceholder.textContent = "Elige una región";
      regionSelect.append(regionPlaceholder);
      for (const region of state.regions) {
        const option = document.createElement("option");
        option.value = region.region;
        option.textContent = `${region.region}${state.mapRegions.has(region.region) ? " *" : ""} (${region.comunas})`;
        regionSelect.append(option);
      }
      regionSelect.addEventListener("change", () => populateCommunes(regionSelect.value));
      $("#comuna").addEventListener("change", (event) => {
        if (event.target.value) selectCommune(event.target.value);
      });
      const urlCode = new URLSearchParams(window.location.search).get("comuna");
      const normalizedUrlCode = urlCode && /^\d{4,5}$/.test(urlCode)
        ? (urlCode.length === 5 && urlCode.startsWith("0") ? urlCode.slice(1) : urlCode.padStart(4, "0"))
        : null;
      const requested = normalizedUrlCode && state.communes.find((row) => row.codigo_comuna === normalizedUrlCode);
      const defaultCommune = state.communes.find((row) => row.codigo_comuna === DEFAULT_COMMUNE_CODE);
      const initial = requested || defaultCommune;
      if (initial) {
        regionSelect.value = initial.region;
        populateCommunes(initial.region, initial.codigo_comuna);
      } else {
        regionSelect.value = "";
        populateCommunes("");
      }
      const mapSection = $("#cartographic-map");
      if (mapSection) mapSection.hidden = false;
      set("#map-status", requested ? "Preparando la comuna solicitada…" : "Preparando Diego de Almagro como selección inicial…");
      window.dispatchEvent(new CustomEvent("catastro:map-eligibility", { detail: { eligible: true, hasPredial: Boolean(initial && hasPublishedMap(initial)), row: initial || null } }));
      window.dispatchEvent(new CustomEvent("catastro:legacy-ready", { detail: { selected: state.selected } }));
      window.addEventListener("resize", () => {
        if (state.cells) renderCanvas(state.cells);
      });
    } catch (_) {
      set("#status", "No se pudieron cargar los datos. Reintenta o revisa la metodología.");
      set("#map-note", "Modo degradado: datos no disponibles.");
      set("#map-status", "No fue posible preparar la capa agregada.");
    }
  }

  boot();
})();
