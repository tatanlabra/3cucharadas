import fs from "node:fs";
import { describe, expect, it } from "vitest";

const html = fs.readFileSync("catastro_sii_brecha/index.html", "utf8");
const legacyApp = fs.readFileSync("catastro_sii_brecha/app.js", "utf8");
const entry = fs.readFileSync("assets/src/catastro_sii/main.ts", "utf8");
const mapApplication = fs.readFileSync("assets/src/catastro_sii/app.ts", "utf8");
const analytics = fs.readFileSync("assets/src/catastro_sii/analytics.ts", "utf8");
const chartTheme = fs.readFileSync("assets/src/catastro_sii/chart-theme.ts", "utf8");
const dictionary = JSON.parse(fs.readFileSync("catastro_sii_brecha/data/diccionario_metricas_comunales.json", "utf8"));

describe("laboratorio accesible y perezoso", () => {
  it("declara cinco tabs, paneles y tablas alternativas", () => {
    for (const view of ["flujo", "avaluos", "distribuciones", "sensibilidad", "comunas"]) {
      expect(html).toContain(`data-lab-tab="${view}"`);
      expect(html).toContain(`data-lab-panel="${view}"`);
    }
    expect(html.match(/class="[^"]*\blab-table-scroll\b/g)).toHaveLength(8);
    expect(html.match(/class="[^"]*\blab-chart-scroll\b[^"]*"/g)).toHaveLength(8);
    expect(html).toContain('class="lab-chart-scroll lab-chart-scroll--wide"');
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
    expect(chartTheme).toContain("currencySmall.format(value)");
  });
});

describe("recorrido narrativo de lo general a lo particular", () => {
  const at = (needle: string) => {
    const index = html.indexOf(needle);
    expect(index, `marcador ausente en index.html: ${needle}`).toBeGreaterThan(-1);
    return index;
  };

  it("ordena las secciones contrato → país → selector → comuna → UV → laboratorio → datos", () => {
    const orden = [
      'id="metodologia-resumen"',
      'id="metric-scope"',
      'id="coverage-teaser"',
      'id="explorar"',
      'id="territory-detail"',
      'id="bivariate-card"',
      'id="denominator-lab"',
      'id="descargas-parquet"',
      'id="catastro-anexo"'
    ].map(at);
    expect(orden).toEqual([...orden].sort((a, b) => a - b));
  });

  it("declara la tesis paraguas del post y enlaza de vuelta a él", () => {
    expect(html).toContain("El denominador, el universo y la escala forman parte del resultado.");
    expect(html).toContain("avaluo-vulnerabilidad-unidad-vecinal/");
  });

  it("fusiona la lectura de agregados dentro de la ficha comunal, sin tarjeta suelta", () => {
    expect(html).toContain('class="finding-inline"');
    expect(html).not.toContain('class="card finding-card reveal"');
    expect(at('class="finding-inline"')).toBeGreaterThan(at('id="territory-detail"'));
    expect(at('class="finding-inline"')).toBeLessThan(at('id="bivariate-card"'));
  });

  it("absorbe cautelas y recorrido en el contrato de lectura, sin duplicar bloques", () => {
    expect(html).toContain('class="contract-grid"');
    expect(html).not.toContain('class="card caution-card reveal"');
    expect(html).not.toContain('class="card steps-card reveal"');
    expect(at('class="callout-grid"')).toBeLessThan(at('id="metric-scope"'));
    // El texto obsoleto de "equivalencia estadística" salió con el cambio de método.
    expect(html).not.toContain("Es una equivalencia estadística");
  });

  it("no deja rastros de la comuna que antes se auto-seleccionaba", () => {
    expect(html).not.toContain("Reset Diego");
    expect(html).not.toContain('id="territory-detail-name">Diego de Almagro');
    expect(html).not.toContain("<td>Diego de Almagro, Atacama</td>");
    expect(html).not.toContain('id="national-records"');
  });

  it("deja la nota técnica de UV en un bloque visible sin JavaScript", () => {
    // #bivariate-card nace con `hidden` y lo destapa el bundle: alojar ahí la nota
    // la volvía invisible en modo degradado. Vive en el laboratorio, que contrasta
    // justamente esos dos universos (6.891 tabulares vs 6.888 cartográficas).
    expect(at('id="nota-universo-uv"')).toBeGreaterThan(at('id="denominator-lab"'));
    expect(at('id="nota-universo-uv"')).toBeLessThan(at('id="descargas-parquet"'));
    expect(html).not.toMatch(/id="bivariate-card"[\s\S]*?id="nota-universo-uv"[\s\S]*?<\/section>\s*<section[^>]*id="denominator-lab"/);
  });

  it("no atenúa el avalúo total, que sí es sumable en los tres niveles", () => {
    // El percentil nacional vive en el mismo .metric-chip que el avalúo: atenuar la
    // tarjeta apagaba una cifra válida. Se reescribe la nota, no se apaga el chip.
    expect(html).toContain('id="assessment-note"');
    expect(legacyApp).toContain('for (const id of ["#historical", "#casen"])');
    expect(legacyApp).not.toContain('"#assessment-percentile", "#historical"');
    expect(legacyApp).toContain("el percentil nacional aplica sólo a nivel comunal");
  });

  it("acepta ?region= tanto por nombre como por el código de 2 dígitos que escribe el visor", () => {
    // state.ts::replaceUrl serializa `region=<código>`; el <select> usa el nombre.
    expect(legacyApp).toContain("regionCodeOf(region.region) === urlRegion.padStart(2");
    expect(legacyApp).toContain("region.region === urlRegion");
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
    expect(html).toContain('href="#denominator-lab">Laboratorio nacional</a>');
    expect(html).toContain('href="#territory-detail">Tu comuna</a>');
    expect(html).toContain('href="#descargas-parquet">Parquet y diccionario</a>');
    expect(html.indexOf('href="#catastro-anexo">Anexo</a>')).toBeGreaterThan(html.indexOf('href="#descargas-parquet">Parquet y diccionario</a>'));
    // El dock sticky de selección se eliminó: el buscador principal es el único hub.
    expect(html).not.toContain('id="selection-dock"');
    expect(html).not.toContain('id="selection-reset"');
    expect(html).not.toContain('id="cartographic-map"');
    expect(html).not.toContain('id="map" aria-label=');
    expect(html).toContain('id="bivariate-map-tilt"');
    expect(html).toContain('id="bivariate-card"');
    expect(html).toContain('id="bivariate-chile-selector"');
    expect(html).toContain('id="bivariate-selector-status"');
    expect(html).not.toContain('id="bivariate-region"');
    expect(html).not.toContain('id="bivariate-comuna"');
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
    expect(mapApplication).not.toContain("DEFAULT_COMMUNE_CODE");
    expect(mapApplication).not.toContain("bindSelectionDock");
    expect(mapApplication).not.toContain("updateSelectionDock");
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

  it("abre en contexto nacional real, sin auto-seleccionar una comuna por defecto", () => {
    expect(legacyApp).toContain('regionPlaceholder.textContent = "Elige una región"');
    expect(legacyApp).toContain('placeholder.textContent = rows.length ? "Elige una comuna"');
    // Sin ?comuna= ni ?region=, `initial` queda nulo y populateCommunes("") deja el
    // visor en nacional; ninguna comuna se cuela como default silencioso.
    expect(legacyApp).not.toContain("DEFAULT_COMMUNE_CODE");
    expect(legacyApp).toContain("const initial = requested || null");
    expect(legacyApp).not.toContain("rows[0].codigo_comuna");
  });

  it("restaura la comuna o la región pedidas por URL", () => {
    expect(legacyApp).toContain('params.get("comuna")');
    expect(legacyApp).toContain('params.get("region")');
    expect(legacyApp).toContain("populateCommunes(initial.region, initial.codigo_comuna)");
    expect(legacyApp).toContain("populateCommunes(requestedRegion.region)");
  });

  it("agrega los indicadores por nivel sumando antes de dividir", () => {
    expect(legacyApp).toContain("function buildScopeAggregate(rows, scope, label, region)");
    expect(legacyApp).toContain('viviendas ? (records / viviendas) * 100 : null');
    expect(legacyApp).toContain("renderNationalMetrics()");
    expect(legacyApp).toContain("renderRegionalMetrics(region)");
    expect(legacyApp).toContain("catastro:region-selection");
    // Sin componentes crudos no se promedian porcentajes ya calculados.
    expect(legacyApp).toContain('"No aplica a este nivel"');
    expect(legacyApp).not.toContain("updateNationalSummary");
  });

  it("deja el bivariado en espera explícita cuando no hay comuna", () => {
    expect(mapApplication).not.toContain("activateDefaultParcelPilot");
    const initialBranch = mapApplication.slice(mapApplication.indexOf("if (!selectedCode)"), mapApplication.indexOf("const row =", mapApplication.indexOf("if (!selectedCode)")));
    expect(initialBranch).not.toContain("setParcelLayer");
    expect(initialBranch).not.toContain("selectFromMap");
    expect(initialBranch).toContain("parcelLayerVisible = false");
    expect(initialBranch).toContain("uvLayerVisible = true");
    expect(initialBranch).toContain('mapScale = "uv"');
  });

  it("publica diccionario del Parquet comunal sin campos prediales individuales", () => {
    expect(dictionary).toMatchObject({ schema_version: 1, dataset: "metricas_comunales.parquet", rows: 346, top_level_columns: 43 });
    expect(dictionary.fields).toHaveLength(43);
    const names = dictionary.fields.map((field: { name: string }) => field.name);
    expect(names).toContain("codigo_comuna");
    expect(names).toContain("cobertura_censo_pct");
    expect(names).toContain("mapa");
    expect(names.join("\n")).not.toMatch(/(^|_)(pred_uid|rol|rut|run|direccion|geometry|coordinates)($|_)/);
  });
});
