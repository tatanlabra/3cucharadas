(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);
  const state = { communes: [], regions: [], selected: null, cells: null, requestId: 0, mapCommuneCodes: new Set(), mapRegions: new Set() };
  const number = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 });
  const pct = (value) => value == null ? "No disponible" : `${Number(value).toLocaleString("es-CL", { maximumFractionDigits: 1 })}%`;
  const money = (value) => value == null ? "No disponible" : `$${number.format(value)}`;
  const set = (selector, value) => {
    const element = $(selector);
    if (element) element.textContent = value;
  };
  const sharedCode = (code) => String(code).padStart(5, "0");
  /** Código de región (2 dígitos) derivado de cualquier comuna suya, sin duplicar la
   * tabla REGION_CODES que ya vive en state.ts. */
  const regionCodeOf = (regionName) => {
    const row = state.communes.find((item) => item.region === regionName);
    return row ? sharedCode(row.codigo_comuna).slice(0, 2) : null;
  };
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
    const section = $("#bivariate-card");
    if (section) section.hidden = false;
    set("#map-availability-note", hasPredial
      ? `* ${row.comuna} aparece en el anexo geométrico piloto; el visor principal mantiene UV agregadas.`
      : "* marca comunas del anexo geométrico piloto. Esta comuna mantiene UV agregadas.");
    window.dispatchEvent(new CustomEvent("catastro:map-eligibility", { detail: { eligible, hasPredial, row } }));
    return eligible;
  }

  function renderCanvas(data) {
    const canvas = $("#density");
    if (!canvas) return;
    const host = canvas.parentElement;
    if (!host) return;
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

  const SCOPE_HINTS = {
    nacional: () => "El verde es la lectura principal en cualquier nivel. Aquí sumo las 346 comunas antes de dividir, el mismo criterio que uso comuna por comuna. La referencia histórica 2017 y la sensibilidad CASEN no se pueden sumar así, así que no aplican a este nivel: elige una región o una comuna para verlas.",
    regional: (label) => `Sumo las comunas de ${label} antes de dividir, el mismo criterio que uso a nivel nacional y comunal. La referencia histórica 2017 y la sensibilidad CASEN tampoco se pueden sumar así: elige una comuna para verlas.`,
    comunal: (label, region) => `Estás viendo ${label}, en ${region}. Estos son los valores propios de la comuna, sin agregar.`
  };

  function sumField(rows, field) {
    return rows.reduce((total, row) => total + (row[field] || 0), 0);
  }

  function buildScopeAggregate(rows, scope, label, region) {
    const viviendas = sumField(rows, "viviendas_totales_censo_2024");
    const hogares = sumField(rows, "hogares_censo_2024");
    const records = sumField(rows, "predios_habitacionales");
    const mapped = sumField(rows, "predios_habitacionales_mapeados");
    return {
      scope,
      label,
      region,
      coverage: viviendas ? (records / viviendas) * 100 : null,
      coverageHogar: hogares ? (records / hogares) * 100 : null,
      population: sumField(rows, "poblacion_censo_2024"),
      records,
      coordinates: records ? (mapped / records) * 100 : null,
      surface: sumField(rows, "superficie_total_m2"),
      assessment: sumField(rows, "avaluo_total_clp"),
      assessmentPercentile: null,
      historical: null,
      casenAvailable: false,
      casen: null,
      casenNote: "No aplica a este nivel"
    };
  }

  function buildCommunePayload(row) {
    return {
      scope: "comunal",
      label: row.comuna,
      region: row.region,
      coverage: row.cobertura_vivienda_pct,
      coverageHogar: row.cobertura_hogar_pct,
      population: row.poblacion_censo_2024,
      records: row.predios_habitacionales,
      coordinates: row.cobertura_coordenadas_pct,
      surface: row.superficie_total_m2,
      assessment: row.avaluo_total_clp,
      assessmentPercentile: row.percentil_avaluo_nacional,
      historical: row.cobertura_vs_proyeccion_base_2017_pct,
      casenAvailable: row.casen_sensibilidad_disponible,
      casen: row.cobertura_casen_sensibilidad_pct,
      casenNote: row.casen_nota
    };
  }

  function renderMetricScope(payload) {
    const { scope, label, region } = payload;
    set("#metric-scope-badge", scope === "comunal" ? `Nivel comunal · ${label}` : scope === "regional" ? `Nivel regional · ${label}` : "Nivel nacional");
    set("#metric-scope-hint", SCOPE_HINTS[scope](label, region));
    set("#coverage", pct(payload.coverage));
    set("#coverage-hogar", pct(payload.coverageHogar));
    set("#population", number.format(payload.population));
    set("#records", number.format(payload.records));
    set("#coordinates", pct(payload.coordinates));
    set("#surface", payload.surface == null ? "No disponible" : `${number.format(payload.surface)} m²`);
    set("#assessment", money(payload.assessment));
    const disabled = scope !== "comunal";
    set("#historical", disabled ? "No aplica a este nivel" : pct(payload.historical));
    set("#casen", disabled ? "No aplica a este nivel" : (payload.casenAvailable ? pct(payload.casen) : "No disponible"));
    set("#casen-note", disabled ? "No aplica a este nivel" : payload.casenNote);
    // El avalúo total sí es sumable y se muestra en los tres niveles: lo que no aplica
    // fuera de lo comunal es su percentil nacional. Por eso se reescribe la nota del
    // chip en vez de atenuar la tarjeta completa, que apagaría una cifra válida.
    const assessmentNote = $("#assessment-note");
    if (assessmentNote) {
      assessmentNote.textContent = disabled
        ? "CLP · el percentil nacional aplica sólo a nivel comunal"
        : `CLP, percentil nacional ${pct(payload.assessmentPercentile)}`;
    }
    for (const id of ["#historical", "#casen"]) {
      const chip = $(id)?.closest(".metric-chip");
      if (chip) chip.classList.toggle("scope-disabled", disabled);
    }
    flashMetrics();
  }

  function updateMetrics(row) {
    set("#territory", row.comuna);
    renderMetricScope(buildCommunePayload(row));
    set("#finding", row.hallazgo);
    set("#status", `${row.region} · ${row.fuente_sii_disponible ? "extracto SII disponible" : "sin extracto SII en el corte"}`);
    set("#selection-context", `Ahora estás mirando ${row.comuna}, ${row.region}.`);
    set("#bivariate-map-status", `Vista UV analítica para ${row.comuna}, ${row.region}.`);
  }

  function renderNationalMetrics() {
    renderMetricScope(buildScopeAggregate(state.communes, "nacional", "Chile", null));
  }

  function renderRegionalMetrics(region) {
    const rows = state.communes.filter((row) => row.region === region);
    renderMetricScope(buildScopeAggregate(rows, "regional", region, region));
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
    if (!$("#density")) return;
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
    if (initial) {
      selectCommune(initial);
      return;
    }
    select.value = "";
    if (region) {
      renderRegionalMetrics(region);
      set("#selection-context", `Región ${region} lista. Elige una comuna para cargar su UV.`);
      set("#status", "Sin comuna seleccionada");
    } else {
      renderNationalMetrics();
      set("#selection-context", "Elige una región y una comuna.");
      set("#status", "Contexto nacional listo");
    }
    window.dispatchEvent(new CustomEvent("catastro:region-selection", { detail: { region: region || null, communeCode: null } }));
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
      const params = new URLSearchParams(window.location.search);
      const urlCode = params.get("comuna");
      const normalizedUrlCode = urlCode && /^\d{4,5}$/.test(urlCode)
        ? (urlCode.length === 5 && urlCode.startsWith("0") ? urlCode.slice(1) : urlCode.padStart(4, "0"))
        : null;
      const requested = normalizedUrlCode && state.communes.find((row) => row.codigo_comuna === normalizedUrlCode);
      // El visor escribe `?region=<código de 2 dígitos>` desde state.ts::replaceUrl,
      // pero el <select> de este buscador trabaja con el nombre. Aceptar ambos evita
      // que una URL generada y compartida por el propio visor caiga al estado nacional.
      const urlRegion = params.get("region");
      const requestedRegion = urlRegion
        ? state.regions.find((region) => region.region === urlRegion)
          || state.regions.find((region) => regionCodeOf(region.region) === urlRegion.padStart(2, "0"))
        : null;
      const initial = requested || null;
      if (initial) {
        regionSelect.value = initial.region;
        populateCommunes(initial.region, initial.codigo_comuna);
      } else if (requestedRegion) {
        regionSelect.value = requestedRegion.region;
        populateCommunes(requestedRegion.region);
      } else {
        regionSelect.value = "";
        populateCommunes("");
      }
      const mapSection = $("#bivariate-card");
      if (mapSection) mapSection.hidden = false;
      set("#bivariate-map-status", requested ? "Preparando la comuna solicitada…" : "Elige una comuna para cargar el mapa UV.");
      window.dispatchEvent(new CustomEvent("catastro:map-eligibility", { detail: { eligible: true, hasPredial: Boolean(initial && hasPublishedMap(initial)), row: initial || null } }));
      window.dispatchEvent(new CustomEvent("catastro:legacy-ready", { detail: { selected: state.selected } }));
      window.addEventListener("resize", () => {
        if (state.cells) renderCanvas(state.cells);
      });
    } catch (_) {
      set("#status", "No se pudieron cargar los datos. Reintenta o revisa la metodología.");
      set("#map-note", "Modo degradado: datos no disponibles.");
      set("#bivariate-map-status", "No fue posible preparar la capa UV agregada.");
    }
  }

  boot();
})();
