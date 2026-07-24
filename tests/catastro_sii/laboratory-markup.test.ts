import fs from "node:fs";
import { describe, expect, it } from "vitest";

const html = fs.readFileSync("catastro_sii_brecha/index.html", "utf8");
const legacyApp = fs.readFileSync("catastro_sii_brecha/app.js", "utf8");
const entry = fs.readFileSync("assets/src/catastro_sii/main.ts", "utf8");
const mapApplication = fs.readFileSync("assets/src/catastro_sii/app.ts", "utf8");

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
    expect(entry).toContain('window.location.hash === "#cartographic-map"');
  });
});

describe("disponibilidad cartográfica nacional", () => {
  it("deja UV activa y predios inactivos por defecto", () => {
    expect(html).toContain('<html lang="es" data-theme="light">');
    expect(html).toContain('id="map-layer-parcels" type="checkbox"');
    expect(html).not.toContain('id="map-layer-parcels" type="checkbox" checked');
    expect(html).toContain('id="map-layer-uv" type="checkbox" checked');
  });

  it("no expone selector para apagar la DPA comunal de contexto", () => {
    expect(html).not.toContain('id="map-layer-communes"');
    expect(mapApplication).not.toContain('getElementById("map-layer-communes")');
    expect(mapApplication).not.toContain("setCommunesVisible(communes.checked)");
  });

  it("separa el mapa de capas del bivariado UV-only", () => {
    expect(html).toContain('id="selection-dock"');
    expect(html).toContain('id="selection-reset"');
    expect(html).toContain('id="map-tilt"');
    expect(html).toContain('id="bivariate-card"');
    expect(html).toContain('id="bivariate-chile-selector"');
    expect(html).toContain('id="bivariate-selector-status"');
    expect(html).toContain('id="bivariate-region"');
    expect(html).toContain('id="bivariate-comuna"');
    expect(html).toContain('id="bivariate-map"');
    expect(html).toContain('id="bivariate-uv-legend"');
    expect(html).not.toContain('id="uv-valuation-mode"');
    expect(mapApplication).toContain("chileSelectorUrl");
    expect(mapApplication).toContain('const DEFAULT_COMMUNE_CODE = "3202"');
    expect(mapApplication).toContain("bindSelectionDock()");
    expect(mapApplication).toContain("updateTerritoryTable(row");
    expect(mapApplication).toContain("bindUvClick(uvHoverContent)");
    expect(mapApplication).toContain("renderChileSelector()");
    expect(mapApplication).toContain("catastro:region-selection");
    expect(mapApplication).toContain('setUvLayer(shardUrl, this.currentTheme(), "m2", focusLocal, "bivariate")');
    expect(mapApplication).toContain('"simple"');
  });

  it("no usa el asterisco para ocultar mapas UV", () => {
    expect(legacyApp).toContain("const eligible = true");
    expect(legacyApp).toContain("hasPredial");
    expect(legacyApp).toContain("todas las comunas mantienen su mapa UV agregado");
  });

  it("selecciona Diego de Almagro por defecto sin caer en la primera comuna", () => {
    expect(legacyApp).toContain('regionPlaceholder.textContent = "Elige una región"');
    expect(legacyApp).toContain('placeholder.textContent = rows.length ? "Elige una comuna"');
    expect(legacyApp).toContain('const DEFAULT_COMMUNE_CODE = "3202"');
    expect(legacyApp).toContain("const initial = requested || defaultCommune");
    expect(legacyApp).not.toContain("rows[0].codigo_comuna");
  });

  it("inicia Diego como vista mixta explícita", () => {
    expect(mapApplication).not.toContain("activateDefaultParcelPilot");
    expect(mapApplication).toContain("DEFAULT_COMMUNE_CODE");
    const initialBranch = mapApplication.slice(mapApplication.indexOf("if (!selectedCode)"), mapApplication.indexOf("const row =", mapApplication.indexOf("if (!selectedCode)")));
    expect(initialBranch).not.toContain("setParcelLayer");
    expect(initialBranch).toContain("parcelLayerVisible = true");
    expect(initialBranch).toContain("uvLayerVisible = true");
    expect(initialBranch).toContain('mapScale = "mixta"');
  });
});
