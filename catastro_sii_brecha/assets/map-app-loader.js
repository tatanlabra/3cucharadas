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

  // The residential diagnostic has no geometry prerequisite.
  const fiscalHost = document.getElementById("brecha-contribuciones");
  if (fiscalHost) {
    const loadDiagnostic = () => load().catch(() => {
      loaded = false; // Static figure/table remain readable; a later event may retry.
    });
    if (window.location.hash === "#brecha-contribuciones" || !("IntersectionObserver" in window)) {
      loadDiagnostic();
    } else {
      const observer = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting)) return;
        observer.disconnect();
        loadDiagnostic();
      }, { rootMargin: "420px" });
      observer.observe(fiscalHost);
    }
  }

  window.addEventListener("catastro:map-eligibility", (event) => {
    if (!event.detail?.eligible) return;
    load().catch(() => {
      loaded = false;
      const status = document.getElementById("bivariate-map-status") || document.getElementById("status");
      if (status) status.textContent = "No fue posible iniciar el mapa UV publicado.";
    });
  });
})();
