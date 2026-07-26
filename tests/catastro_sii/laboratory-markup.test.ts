import fs from "node:fs";
import { describe, expect, it } from "vitest";

const html = fs.readFileSync("catastro_sii_brecha/index.html", "utf8");
const legacyApp = fs.readFileSync("catastro_sii_brecha/app.js", "utf8");
const entry = fs.readFileSync("assets/src/catastro_sii/main.ts", "utf8");
const mapApplication = fs.readFileSync("assets/src/catastro_sii/app.ts", "utf8");
const analytics = fs.readFileSync("assets/src/catastro_sii/analytics.ts", "utf8");
const dictionary = JSON.parse(fs.readFileSync("catastro_sii_brecha/data/diccionario_metricas_comunales.json", "utf8"));

describe("laboratorio accesible y perezoso", () => {
  it("declara cinco tabs, paneles y tablas alternativas", () => {
    for (const view of ["flujo", "avaluos", "distribuciones", "sensibilidad", "comunas"]) {
      expect(html).toContain(`data-lab-tab="${view}"`);
      expect(html).toContain(`data-lab-panel="${view}"`);
    }
    expect(html.match(/class="[^"]*\blab-table-scroll\b/g)).toHaveLength(7);
    expect(html.match(/class="lab-chart-scroll"/g)).toHaveLength(7);
    expect(html).toContain('id="lab-violin-summary-chart"');
    expect(html).toContain('id="lab-ranking-unit"');
    expect(html).toContain('id="lab-commune-filter-note"');
    expect(html).toContain('id="lab-commune-reset"');
    expect(html.match(/class="lab-scale-note"/g)).toHaveLength(3);
    expect(html).toContain("Lectura log10");
    expect(html).toContain("multiplicar por 10");
    expect(html).toContain('aria-live="polite"');
    expect(html).toContain('id="territory-detail-table"');
    expect(html).toContain('id="territory-detail-table-body"');
  });

  it("carga el módulo analítico con import dinámico e IntersectionObserver", () => {
    expect(entry).toContain('import("./analytics")');
    expect(entry).toContain("onceNearViewport(host");
    expect(entry).not.toMatch(/^import .*analytics/m);
  });

  it("carga el mapa de inmediato cuando la URL apunta al visor cartográfico", () => {
    expect(entry).toContain('requested.get("vista") === "mapa"');
    expect(entry).toContain('requested.has("comuna")');
    expect(entry).toContain('window.location.hash === "#bivariate-card"');
  });

  it("mantiene ejes de avalúo en log10 con etiquetas en pesos originales", () => {
    expect(analytics.match(/type: "log"/g)).toHaveLength(3);
    expect(analytics).toContain('name: "Avalúo total (log10; etiquetas CLP)"');
    expect(analytics).toContain('name: "Mediana en escala log10"');
    expect(analytics).toContain('name: `${METRICS[metric].label} (log10)`');
    expect(analytics).toContain("formatCurrencyTick(original)");
    expect(analytics).toContain("logAxisBounds(regions.map((region) => region.value))");
    expect(analytics).toContain("logAxisBounds(eligible.map((record) => metricValue(record, metric)))");
    expect(analytics).toContain("currencySmall.format(value)");
  });
});

describe("disponibilidad cartográfica nacional", () => {
  it("mantiene sólo el fondo como control del mapa UV principal", () => {
    expect(html).toContain('<html lang="es" data-theme="light">');
    expect(html).toContain('id="bivariate-map-layer-basemap" type="checkbox" checked');
    expect(html).not.toContain('id="map-layer-parcels"');
    expect(html).not.toContain('id="map-layer-uv"');
  });

  it("no expone selector para apagar la DPA comunal de contexto", () => {
    expect(html).not.toContain('id="map-layer-communes"');
    expect(mapApplication).not.toContain('getElementById("map-layer-communes")');
    expect(mapApplication).not.toContain("setCommunesVisible(communes.checked)");
  });

  it("declara navegación por pestañas, mapa analítico único, leyenda 2x4 y anexo visual final", () => {
    expect(html).toContain('class="story-tabs reveal"');
    expect(html).toContain('href="#denominator-lab">Descriptivos nacionales</a>');
    expect(html).toContain('href="#territory-detail">Comunal · regional · UV</a>');
    expect(html).toContain('href="#descargas-parquet">Parquet y diccionario</a>');
    expect(html.indexOf('href="#catastro-anexo">Anexo</a>')).toBeGreaterThan(html.indexOf('href="#descargas-parquet">Parquet y diccionario</a>'));
    expect(html).toContain('id="selection-dock"');
    expect(html).toContain('id="selection-reset"');
    expect(html).not.toContain('id="cartographic-map"');
    expect(html).not.toContain('id="map" aria-label=');
    expect(html).toContain('id="bivariate-map-tilt"');
    expect(html).toContain('id="bivariate-card"');
    expect(html).toContain('id="bivariate-chile-selector"');
    expect(html).toContain('id="bivariate-selector-status"');
    expect(html).toContain('id="bivariate-region"');
    expect(html).toContain('id="bivariate-comuna"');
    expect(html).toContain('id="bivariate-map"');
    expect(html).toContain('id="bivariate-uv-legend"');
    expect(html).toContain('Matriz de 8 combinaciones');
    expect(html).toContain('Bajo/igual región');
    expect(html).toContain('Nota técnica sobre las UV');
    expect(html).not.toContain('class="c13"');
    expect(html).toContain('id="catastro-anexo"');
    expect(html.lastIndexOf('id="catastro-anexo"')).toBeGreaterThan(html.lastIndexOf('id="descargas-parquet"'));
    expect(html).toContain('assets/images/catastro-anexo/diego_de_almagro_03202_geom.png');
    expect(html).toContain('data/agregados_territoriales.json');
    expect(html).toContain('data/diccionario_metricas_comunales.json');
    expect(html).not.toContain('id="uv-valuation-mode"');
    expect(mapApplication).toContain("chileSelectorUrl");
    expect(mapApplication).toContain("loadTerritorialAggregates()");
    expect(mapApplication).toContain('const DEFAULT_COMMUNE_CODE = "3202"');
    expect(mapApplication).toContain("bindSelectionDock()");
    expect(mapApplication).toContain("updateTerritoryTable(row");
    expect(mapApplication).toContain("bindUvClick((properties) => uvHoverContent(properties, this.currentRegionalMedianAvm2()))");
    expect(mapApplication).toContain("renderChileSelector()");
    expect(mapApplication).toContain("catastro:region-selection");
    expect(mapApplication).toContain("regionalMedianAvm2");
    expect(mapApplication).toContain('document.getElementById("bivariate-map")');
    expect(mapApplication).toContain('setUvLayer(shardUrl, this.currentTheme(), regionalMedianAvm2, focusLocal, "bivariate")');
    expect(mapApplication).not.toContain('"simple"');
  });

  it("no usa el asterisco para ocultar mapas UV", () => {
    expect(legacyApp).toContain("const eligible = true");
    expect(legacyApp).toContain("hasPredial");
    expect(legacyApp).toContain("el visor principal mantiene UV agregadas");
  });

  it("selecciona Diego de Almagro por defecto sin caer en la primera comuna", () => {
    expect(legacyApp).toContain('regionPlaceholder.textContent = "Elige una región"');
    expect(legacyApp).toContain('placeholder.textContent = rows.length ? "Elige una comuna"');
    expect(legacyApp).toContain('const DEFAULT_COMMUNE_CODE = "3202"');
    expect(legacyApp).toContain("const initial = requested || defaultCommune");
    expect(legacyApp).not.toContain("rows[0].codigo_comuna");
  });

  it("inicia Diego como vista analítica UV explícita", () => {
    expect(mapApplication).not.toContain("activateDefaultParcelPilot");
    expect(mapApplication).toContain("DEFAULT_COMMUNE_CODE");
    const initialBranch = mapApplication.slice(mapApplication.indexOf("if (!selectedCode)"), mapApplication.indexOf("const row =", mapApplication.indexOf("if (!selectedCode)")));
    expect(initialBranch).not.toContain("setParcelLayer");
    expect(initialBranch).toContain("parcelLayerVisible = false");
    expect(initialBranch).toContain("uvLayerVisible = true");
    expect(initialBranch).toContain('mapScale = "uv"');
  });

  it("publica diccionario del Parquet comunal sin campos prediales individuales", () => {
    expect(dictionary).toMatchObject({ schema_version: 1, dataset: "metricas_comunales.parquet", rows: 346, top_level_columns: 39 });
    expect(dictionary.fields).toHaveLength(39);
    const names = dictionary.fields.map((field: { name: string }) => field.name);
    expect(names).toContain("codigo_comuna");
    expect(names).toContain("cobertura_censo_pct");
    expect(names).toContain("mapa");
    expect(names.join("\n")).not.toMatch(/(^|_)(pred_uid|rol|rut|run|direccion|geometry|coordinates)($|_)/);
  });
});
