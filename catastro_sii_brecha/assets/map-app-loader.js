/* Cargador estable para el artefacto Vite hasheado. No contiene lógica cartográfica. */
(() => {
  "use strict";

  const base = new URL("/assets/dist/catastro_sii/", window.location.origin);
  const manifestUrl = new URL("manifest.json", base);

  let loaded = false;

  async function load() {
    if (loaded) return;
    loaded = true;
    const response = await fetch(manifestUrl, { cache: "no-cache" });
    if (!response.ok) throw new Error(`manifest Vite no disponible (${response.status})`);
    const manifest = await response.json();
    const entry = manifest["assets/src/catastro_sii/main.ts"];
    if (!entry?.file) throw new Error("entrada Vite Catastro SII ausente");

    for (const file of entry.css || []) {
      const stylesheet = document.createElement("link");
      stylesheet.rel = "stylesheet";
      stylesheet.href = new URL(file, base).href;
      stylesheet.dataset.catastroMapCss = "true";
      document.head.append(stylesheet);
    }

    const script = document.createElement("script");
    script.type = "module";
    script.src = new URL(entry.file, base).href;
    document.body.append(script);
  }

  window.addEventListener("catastro:map-eligibility", (event) => {
    if (!event.detail?.eligible) return;
    load().catch(() => {
      loaded = false;
      const status = document.getElementById("map-status");
      if (status) status.textContent = "No fue posible iniciar el mapa cartográfico publicado.";
    });
  });
})();
