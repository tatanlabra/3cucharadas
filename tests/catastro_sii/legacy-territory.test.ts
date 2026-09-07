import fs from "node:fs";
import vm from "node:vm";
import { describe, expect, it } from "vitest";

class Element {
  value = "";
  children: Element[] = [];
  handlers: Record<string, (event: { target: Element }) => void> = {};
  ownText = "";
  classList = { add() {}, remove() {}, toggle() {} };
  get textContent(): string { return this.ownText + this.children.map(e => e.textContent).join(" "); }
  set textContent(value: string) { this.ownText = value; this.children = []; }
  set innerHTML(_value: string) { this.children = []; }
  append(...elements: Element[]) { this.children.push(...elements); }
  replaceChildren(...elements: Element[]) { this.ownText = ""; this.children = elements; }
  closest() { return null; }
  addEventListener(name: string, handler: (event: { target: Element }) => void) { this.handlers[name] = handler; }
  change(value: string) { this.value = value; this.handlers.change({ target: this }); }
}

async function boot() {
  const elements = new Map<string, Element>();
  const get = (selector: string) => {
    if (!elements.has(selector)) elements.set(selector, new Element());
    return elements.get(selector)!;
  };
  get("#territory-detail-summary").textContent = "Elige una comuna para cargar su ficha territorial.";
  get("#territory-detail-table-body").textContent = "Sin comuna seleccionada";
  const row = { codigo_comuna: "3102", comuna: "Caldera", region: "Atacama", predios_habitacionales: 8477, poblacion_censo_2024: 18000, superficie_total_m2: 10000, avaluo_total_clp: 1000000, hallazgo: "Registro público agregado" };
  const second = { ...row, codigo_comuna: "3101", comuna: "Copiapó", avaluo_total_clp: null };
  const events: string[] = [];
  vm.runInNewContext(fs.readFileSync("catastro_sii_brecha/app.js", "utf8"), {
    document: { querySelector: get, createElement: () => new Element() },
    window: { location: { search: "" }, matchMedia: () => ({ matches: true }), dispatchEvent: (event: { type: string }) => events.push(event.type) },
    CustomEvent: class { constructor(public type: string, public detail: unknown) {} },
    URLSearchParams, Intl,
    fetch: async (url: string) => ({ ok: true, json: async () => url === "data/comunas.json" ? [row, second] : url === "data/regiones.json" ? [{ region: "Atacama", comunas: 2 }] : {} })
  });
  for (let i = 0; i < 30 && !events.includes("catastro:legacy-ready"); i++) await Promise.resolve();
  expect(events).toContain("catastro:legacy-ready");
  return get;
}

describe("ficha básica independiente del renderer opcional", () => {
  it("selección, cambio y borrado actualizan texto y tabla sin importar el bundle del mapa", async () => {
    const get = await boot();
    get("#region").change("Atacama");
    get("#comuna").change("3102");
    expect(get("#territory-detail-summary").textContent).toContain("Caldera");
    expect(get("#territory-detail-table-body").textContent).toContain("8.477");
    get("#comuna").change("3101");
    expect(get("#territory-detail-table-body").textContent).toContain("Copiapó");
    expect(get("#territory-detail-table-body").textContent).toContain("No disponible");
    expect(get("#territory-detail-table-body").textContent).not.toContain("Caldera");
    get("#comuna").change("");
    expect(get("#territory-detail-summary").textContent).toContain("Atacama");
    expect(get("#territory-detail-table-body").textContent).not.toContain("Copiapó");
    expect(get("#finding").textContent).toContain("Atacama");
    get("#region").change("");
    expect(get("#territory-detail-table-body").textContent).toBe("Selección Sin comuna seleccionada");
  });
});
