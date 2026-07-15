const state = {
  regional: [],
  comunal: [],
  uv: [],
  filteredRegional: [],
  filteredComunal: [],
  filteredUv: [],
  mapData: null,
  selectedRegion: "",
  regionList: [],
  sort: {
    reg: { key: "rank_nac", dir: "asc" },
    com: { key: "rank_nac", dir: "asc" },
    uv: { key: "c_ig_nac", dir: "asc" }
  }
};

const nf = new Intl.NumberFormat("es-CL");
const pf = new Intl.NumberFormat("es-CL", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1
});

const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const kpiTargets = [];
let kpiAnimated = false;
let mapIntroDone = false;
let mapTip = null;

const columns = {
  reg: [
    ["rank_nac", "Rank", "number"],
    ["Region", "Región", "text"],
    ["c_ig_nac", "Cuartil", "quarter"],
    ["n_comunas", "Comunas", "number"],
    ["n_uv", "UV", "number"],
    ["pob_rsh_reg", "Personas RSH", "number"],
    ["hog_reg", "Hogares", "number"],
    ["cobertura_rsh", "Cobertura RSH", "percent"]
  ],
  com: [
    ["rank_nac", "Rank", "number"],
    ["Comuna", "Comuna", "text"],
    ["Region", "Región", "text"],
    ["c_ig_nac", "C nac.", "quarter"],
    ["c_ig_reg", "C reg.", "quarter"],
    ["Clasificación", "Tipo", "text"],
    ["pob_rsh_com", "Personas RSH", "number"],
    ["hog_com", "Hogares", "number"],
    ["cobertura_rsh", "Cobertura", "percent"],
    ["cobertura_rsh_raw", "Cob. raw", "percent"]
  ],
  uv: [
    ["Region", "Región", "text"],
    ["rank_nac", "Rank", "number"],
    ["uv_nombre", "Unidad Vecinal", "text"],
    ["Comuna", "Comuna", "text"],
    ["c_ig_nac", "C nac.", "quarter"],
    ["c_ig_reg", "C reg.", "quarter"],
    ["c_ig_com", "C com.", "quarter"],
    ["pob_rsh_uv", "Personas RSH", "number"],
    ["uv_definida", "Definida", "boolean"]
  ]
};

function parseCSV(text) {
  const rows = [];
  let row = [];
  let value = "";
  let inQuotes = false;
  const clean = text.replace(/^\uFEFF/, "");

  for (let i = 0; i < clean.length; i += 1) {
    const char = clean[i];
    const next = clean[i + 1];

    if (char === "\"") {
      if (inQuotes && next === "\"") {
        value += "\"";
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === "," && !inQuotes) {
      row.push(value);
      value = "";
    } else if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i += 1;
      row.push(value);
      if (row.some((cell) => cell.length > 0)) rows.push(row);
      row = [];
      value = "";
    } else {
      value += char;
    }
  }

  if (value.length || row.length) {
    row.push(value);
    if (row.some((cell) => cell.length > 0)) rows.push(row);
  }

  if (!rows.length) return [];
  const headers = rows[0].map((header) => header.trim());
  return rows.slice(1).map((cells) => {
    const item = {};
    headers.forEach((header, index) => {
      item[header] = (cells[index] ?? "").trim();
    });
    return item;
  });
}

async function loadText(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`No se pudo cargar ${path}: ${response.status}`);
  return response.text();
}

async function loadCSV(path) {
  return parseCSV(await loadText(path));
}

async function loadJSON(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`No se pudo cargar ${path}: ${response.status}`);
  return response.json();
}

function showNotice(message) {
  const main = document.querySelector("main");
  if (!main) return;
  main.insertAdjacentHTML(
    "afterbegin",
    `<section class="card notice-card"><h2>Algo no se pudo cargar</h2><p>${escapeHTML(message)}</p>` +
    `<p class="hint">El resto del visor sigue disponible. Los datos completos están en ` +
    `<a href="https://bidat.gob.cl/directorio/SIVUST%20-%20Vulnerabilidad%20Socioterritorial" target="_blank" rel="noopener">BIDAT</a>.</p></section>`
  );
}

function asNumber(value) {
  if (value === null || value === undefined || value === "" || value === "NaN") return NaN;
  return Number(String(value).replace(",", "."));
}

function isMissing(value) {
  return value === null || value === undefined || value === "" || value === "NaN";
}

function formatNumber(value) {
  const parsed = asNumber(value);
  return Number.isFinite(parsed) ? nf.format(parsed) : "—";
}

function formatPercent(value) {
  const parsed = asNumber(value);
  return Number.isFinite(parsed) ? `${pf.format(parsed)}%` : "—";
}

function normalize(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();
}

function sameRegion(a, b) {
  return normalize(a) === normalize(b);
}

function titleCaseRegion(value) {
  const small = new Set(["de", "del", "y"]);
  return String(value ?? "")
    .toLocaleLowerCase("es-CL")
    .split(/\s+/)
    .map((part, index) => {
      if (!part) return part;
      if (index > 0 && small.has(part)) return part;
      return part.charAt(0).toLocaleUpperCase("es-CL") + part.slice(1);
    })
    .join(" ");
}

function displayRegion(value) {
  const text = String(value ?? "");
  return text === text.toLocaleUpperCase("es-CL") ? titleCaseRegion(text) : text;
}

function quarterBadge(value) {
  const q = String(value ?? "").trim();
  if (!["1", "2", "3", "4"].includes(q)) return "—";
  return `<span class="badge q${q}" title="Cuartil ${q}">C${q}</span>`;
}

function booleanMark(value) {
  const yes = String(value).toLowerCase() === "true";
  return yes ? '<span class="yes">Sí</span>' : '<span class="no">No</span>';
}

function displayValue(row, key, type) {
  const value = row[key];
  if (type === "quarter") return quarterBadge(value);
  if (type === "number") return formatNumber(value);
  if (type === "percent") return formatPercent(value);
  if (type === "boolean") return booleanMark(value);
  if (isMissing(value)) return "—";
  if (key === "Region") return escapeHTML(displayRegion(value));
  return escapeHTML(value);
}

function escapeHTML(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sortRows(rows, tableKey) {
  const { key, dir } = state.sort[tableKey];
  const col = columns[tableKey].find(([colKey]) => colKey === key);
  const type = col ? col[2] : "text";
  const factor = dir === "asc" ? 1 : -1;

  return [...rows].sort((a, b) => {
    if (type === "number" || type === "percent" || type === "quarter") {
      const av = asNumber(a[key]);
      const bv = asNumber(b[key]);
      if (!Number.isFinite(av) && !Number.isFinite(bv)) return 0;
      if (!Number.isFinite(av)) return 1;
      if (!Number.isFinite(bv)) return -1;
      return (av - bv) * factor;
    }
    return normalize(a[key]).localeCompare(normalize(b[key]), "es") * factor;
  });
}

function renderTable(id, tableKey, rows) {
  const table = document.getElementById(id);
  const sorted = sortRows(rows, tableKey);
  const header = columns[tableKey]
    .map(([key, label, type]) => {
      const active = state.sort[tableKey].key === key;
      const mark = active ? (state.sort[tableKey].dir === "asc" ? "↑" : "↓") : "";
      const numClass = ["number", "percent"].includes(type) ? " class=\"num\"" : "";
      return `<th${numClass}><button type="button" data-table="${tableKey}" data-key="${key}">${label} <span aria-hidden="true">${mark}</span></button></th>`;
    })
    .join("");

  const body = sorted
    .map((row) => {
      const cells = columns[tableKey]
        .map(([key, _label, type]) => {
          const numClass = ["number", "percent"].includes(type) ? ' class="num"' : "";
          return `<td${numClass}>${displayValue(row, key, type)}</td>`;
        })
        .join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  table.innerHTML = `<thead><tr>${header}</tr></thead><tbody>${body}</tbody>`;
  table.querySelectorAll("th button").forEach((button) => {
    button.addEventListener("click", () => {
      const key = button.dataset.key;
      const current = state.sort[tableKey];
      state.sort[tableKey] = {
        key,
        dir: current.key === key && current.dir === "asc" ? "desc" : "asc"
      };
      rerender(tableKey);
    });
  });
}

function rerender(tableKey) {
  if (tableKey === "reg") renderTable("tbl-reg", "reg", state.filteredRegional);
  if (tableKey === "com") renderTable("tbl-com", "com", state.filteredComunal);
  if (tableKey === "uv") renderTable("tbl-uv", "uv", state.filteredUv);
}

function registerKpi(id, target, format) {
  const el = document.getElementById(id);
  if (!el) return;
  if (!Number.isFinite(target)) {
    el.textContent = "—";
    return;
  }
  el.textContent = format(0);
  kpiTargets.push({ el, target, format });
}

function updateKpis(metadata) {
  const qa = metadata.qa ?? {};
  const cov = metadata.qa_cobertura_rsh ?? {};
  const intFmt = (value) => nf.format(Math.round(value));
  registerKpi("kpi-uv", asNumber(qa.uv_total), intFmt);
  registerKpi("kpi-com", asNumber(qa.comunas), intFmt);
  registerKpi("kpi-reg", asNumber(qa.regiones), intFmt);
  registerKpi("kpi-pob", asNumber(qa.pob_rsh_total), intFmt);
  registerKpi("kpi-cob", asNumber(cov.cobertura_rsh_nacional) * 100, (value) => `${pf.format(value)}%`);
  registerKpi("kpi-hog", asNumber(qa.hogares_total), intFmt);
}

function animateCount(el, target, format, duration = 1100) {
  const start = performance.now();
  function tick(now) {
    const progress = Math.min(1, (now - start) / duration);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = format(target * eased);
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = format(target);
  }
  requestAnimationFrame(tick);
}

function animateKpis(instant) {
  if (kpiAnimated) return;
  kpiAnimated = true;
  kpiTargets.forEach(({ el, target, format }) => {
    if (instant || prefersReduced) el.textContent = format(target);
    else animateCount(el, target, format);
  });
}

function setupReveal() {
  const els = document.querySelectorAll(".reveal");
  if (prefersReduced || !("IntersectionObserver" in window)) {
    els.forEach((el) => el.classList.add("in"));
    animateKpis(true);
    return;
  }
  // threshold 0 (revela en cuanto el borde entra) en vez de un porcentaje: una
  // sección más alta que el viewport —como la tabla de UV, ~210.000 px— nunca
  // llega a cubrir un 14% de sí misma, así que con threshold 0.14 no cruzaba el
  // umbral y se quedaba en opacity:0 de forma permanente.
  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("in");
      if (entry.target.id === "kpis") animateKpis(false);
      obs.unobserve(entry.target);
    });
  }, { threshold: 0, rootMargin: "0px 0px -80px 0px" });
  els.forEach((el) => io.observe(el));
}

function setupThemeToggle() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try {
      localStorage.setItem("sivust-theme", next);
    } catch (error) {
      /* almacenamiento no disponible: el tema queda solo en memoria */
    }
  });
}

function activeRegionRows(rows) {
  const region = state.selectedRegion;
  return region ? rows.filter((row) => sameRegion(row.Region, region)) : [...rows];
}

function applyRegionalFilter() {
  state.filteredRegional = activeRegionRows(state.regional);
  renderTable("tbl-reg", "reg", state.filteredRegional);
}

function applyComunalFilters() {
  const query = normalize(document.getElementById("f-com").value);
  state.filteredComunal = activeRegionRows(state.comunal).filter((row) => {
    return !query || normalize(`${row.Comuna} ${row.Region}`).includes(query);
  });
  document.getElementById("com-count").textContent = `${nf.format(state.filteredComunal.length)} comunas`;
  renderTable("tbl-com", "com", state.filteredComunal);
  highlightFirstComuna(Boolean(query));
}

function highlightFirstComuna(hasQuery) {
  const table = document.getElementById("tbl-com");
  if (!table) return;
  const first = table.querySelector("tbody tr");
  if (hasQuery && first) first.classList.add("row-hit");
}

function scrollToFirstComuna() {
  const table = document.getElementById("tbl-com");
  const first = table ? table.querySelector("tbody tr.row-hit, tbody tr") : null;
  if (first) first.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "center" });
}

function applyUvFilter() {
  state.filteredUv = activeRegionRows(state.uv);
  document.getElementById("uv-count").textContent = `${nf.format(state.filteredUv.length)} UV C1/C4`;
  renderTable("tbl-uv", "uv", state.filteredUv);
}

function renderRegionButtons() {
  const container = document.getElementById("region-buttons");
  const nationalActive = state.selectedRegion === "";
  const buttons = [
    `<button type="button" class="region-btn${nationalActive ? " active" : ""}" data-region="" aria-pressed="${nationalActive}">Nacional</button>`,
    ...state.regionList.map((region) => {
      const active = state.selectedRegion === region;
      return `<button type="button" class="region-btn${active ? " active" : ""}" data-region="${escapeHTML(region)}" aria-pressed="${active}">${escapeHTML(displayRegion(region))}</button>`;
    })
  ];
  container.innerHTML = buttons.join("");
  container.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => setSelectedRegion(button.dataset.region || ""));
  });
}

function renderMapLegend() {
  const legend = document.getElementById("map-legend");
  const data = state.mapData;
  if (!data) return;
  const items = [];
  for (let q = 1; q <= 4; q += 1) {
    const label = q === 1 ? "C1 (+ vuln.)" : q === 4 ? "C4 (- vuln.)" : `C${q}`;
    const low = data.colors[(q - 1) * 2];
    const high = data.colors[(q - 1) * 2 + 1];
    items.push(
      `<div class="legend-item">` +
      `<span class="legend-q">${label}</span>` +
      `<span class="legend-duo">` +
      `<span class="legend-swatch" role="img" aria-label="${label}, bajo mediana" title="${label}, bajo mediana" style="background:${low}"></span>` +
      `<span class="legend-swatch" role="img" aria-label="${label}, sobre mediana" title="${label}, sobre mediana" style="background:${high}"></span>` +
      `</span>` +
      `</div>`
    );
  }
  legend.innerHTML = `<div class="legend-guide" aria-hidden="true"><span>Bajo mediana</span><span>Sobre mediana</span></div><div class="legend-items">${items.join("")}</div>`;
  document.getElementById("map-pop-median").textContent = `Mediana comunal de población RSH: ${formatNumber(data.pop_median_rsh_comunal)} personas.`;
}

function renderMap() {
  const svg = document.getElementById("bivariado-map");
  const data = state.mapData;
  if (!data) return;
  svg.setAttribute("viewBox", data.viewBox);
  const selected = state.selectedRegion;
  const intro = !mapIntroDone && !prefersReduced;
  const total = data.features.length;
  svg.innerHTML = data.features
    .map((feature, index) => {
      const color = data.colors[feature.biv] || "#eef0f2";
      const isSelected = selected && sameRegion(feature.region, selected);
      const dimmed = selected && !isSelected;
      const classes = ["map-feature", isSelected ? "selected" : "", dimmed ? "dimmed" : ""].filter(Boolean).join(" ");
      const title = `${feature.comuna}, ${displayRegion(feature.region)} · C${feature.q} · ${formatNumber(feature.pob_rsh)} personas RSH`;
      const delay = intro ? ` style="animation-delay:${Math.round((index / total) * 620)}ms"` : "";
      return `<path class="${classes}"${delay} data-region="${escapeHTML(feature.region)}" data-comuna="${escapeHTML(feature.comuna)}" data-q="${escapeHTML(feature.q)}" data-pob="${escapeHTML(feature.pob_rsh)}" data-color="${color}" d="${feature.d}" fill="${color}" fill-rule="evenodd"><title>${escapeHTML(title)}</title></path>`;
    })
    .join("");

  if (intro) {
    svg.classList.add("intro");
    mapIntroDone = true;
    window.setTimeout(() => svg.classList.remove("intro"), 1400);
  }

  svg.querySelectorAll(".map-feature").forEach((path) => {
    path.addEventListener("click", () => setSelectedRegion(path.dataset.region || ""));
  });
}

function ensureMapTip() {
  if (mapTip) return mapTip;
  mapTip = document.createElement("div");
  mapTip.className = "map-tip";
  mapTip.setAttribute("role", "presentation");
  document.body.appendChild(mapTip);
  return mapTip;
}

function showMapTip(path, clientX, clientY) {
  const tip = ensureMapTip();
  const comuna = path.dataset.comuna || "";
  const region = displayRegion(path.dataset.region || "");
  const q = path.dataset.q || "";
  const pob = formatNumber(path.dataset.pob);
  const color = path.dataset.color || "#cccccc";
  tip.innerHTML =
    `<div class="tip-comuna">${escapeHTML(comuna)}</div>` +
    `<div class="tip-region">${escapeHTML(region)}</div>` +
    `<div class="tip-row"><span class="tip-sw" style="background:${escapeHTML(color)}"></span>` +
    `<span class="tip-k">Cuartil</span><span class="tip-v">C${escapeHTML(q)}</span></div>` +
    `<div class="tip-row"><span class="tip-k">Personas en RSH</span><span class="tip-v">${pob}</span></div>`;
  positionMapTip(clientX, clientY);
  tip.classList.add("show");
}

function positionMapTip(clientX, clientY) {
  if (!mapTip) return;
  const pad = 16;
  const rect = mapTip.getBoundingClientRect();
  let x = clientX + pad;
  let y = clientY + pad;
  if (x + rect.width > window.innerWidth - 8) x = clientX - rect.width - pad;
  if (y + rect.height > window.innerHeight - 8) y = clientY - rect.height - pad;
  mapTip.style.left = `${Math.max(8, x)}px`;
  mapTip.style.top = `${Math.max(8, y)}px`;
}

function hideMapTip() {
  if (mapTip) mapTip.classList.remove("show");
}

function setupMapTooltip() {
  const svg = document.getElementById("bivariado-map");
  if (!svg) return;
  svg.addEventListener("pointermove", (event) => {
    const path = event.target.closest ? event.target.closest(".map-feature") : null;
    if (path) showMapTip(path, event.clientX, event.clientY);
    else hideMapTip();
  });
  svg.addEventListener("pointerleave", hideMapTip);
  window.addEventListener("scroll", hideMapTip, { passive: true });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") hideMapTip();
  });
}

function updateRegionContext() {
  const selected = state.selectedRegion;
  const mapStatus = document.getElementById("map-status");
  const note = document.getElementById("region-filter-note");
  if (selected) {
    mapStatus.textContent = `${displayRegion(selected)} · ${nf.format(state.filteredComunal.length)} comunas · ${nf.format(state.filteredUv.length)} UV C1/C4`;
    note.textContent = `Filtro activo: ${displayRegion(selected)}. El ranking regional muestra solo la región seleccionada; usa Nacional en el mapa para volver al total país.`;
  } else {
    mapStatus.textContent = `Nacional · ${nf.format(state.comunal.length)} comunas · ${nf.format(state.uv.length)} UV C1/C4`;
    note.textContent = "Ordenado por vulnerabilidad (rank nacional, 1 = mayor vulnerabilidad relativa). Haz clic en los encabezados para reordenar.";
  }
}

function setSelectedRegion(region) {
  state.selectedRegion = region;
  renderRegionButtons();
  applyRegionalFilter();
  applyComunalFilters();
  applyUvFilter();
  renderMap();
  updateRegionContext();
}

function bindControls() {
  const finder = document.getElementById("f-com");
  finder.addEventListener("input", applyComunalFilters);
  finder.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      scrollToFirstComuna();
    }
  });
}

/* Carga en dos fases. El mapa es el recurso más pesado (~760 KB) y el menos
   esencial: si falla o tarda, los KPIs y las tablas ya deben estar en pantalla.
   Por eso no comparte un Promise.all con el resto, donde un solo 404 dejaba la
   página entera vacía. */
async function init() {
  try {
    const [metadata, regional, comunal, uv] = await Promise.all([
      loadJSON("data/metadata.json"),
      loadCSV("data/resumen_regional.csv"),
      loadCSV("data/resumen_comunal.csv"),
      loadCSV("data/uv_cuartiles_extremos.csv")
    ]);

    state.regional = regional;
    state.comunal = comunal;
    state.uv = uv;
    state.regionList = [...new Set(comunal.map((row) => row.Region).filter(Boolean))]
      .sort((a, b) => normalize(a).localeCompare(normalize(b), "es"));

    updateKpis(metadata);
    bindControls();
    setSelectedRegion("");
  } catch (error) {
    console.error(error);
    showNotice(`No se pudieron cargar los datos del visor. ${error.message}`);
  } finally {
    setupReveal();
  }

  try {
    state.mapData = await loadJSON("data/mapa_comunal_bivariado.json");
    renderMapLegend();
    renderMap();
    setupMapTooltip();
    updateRegionContext();
  } catch (error) {
    console.error(error);
    const status = document.getElementById("map-status");
    if (status) status.textContent = "El mapa no está disponible; las tablas sí.";
  }
}

setupThemeToggle();
init();
