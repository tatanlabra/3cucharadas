/* Cargador estable del minivisor territorial del Post II. */
(() => {
  "use strict";

  const host = document.querySelector("[data-thesis-market-map]");
  if (!host) return;
  const base = new URL("/assets/dist/thesis_post2_map/", window.location.origin);

  async function prepareEntry() {
    const response = await fetch(new URL("manifest.json", base), { cache: "no-cache" });
    if (!response.ok) throw new Error(`manifest no disponible (${response.status})`);
    const manifest = await response.json();
    const entry = manifest["assets/src/thesis_post2_map/main.ts"];
    if (!entry?.file) throw new Error("entrada Vite del minivisor ausente");
    for (const file of entry.css || []) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = new URL(file, base).href;
      document.head.append(link);
    }
    return entry;
  }

  const entryPromise = prepareEntry();

  async function load() {
    const entry = await entryPromise;
    const script = document.createElement("script");
    script.type = "module";
    script.src = new URL(entry.file, base).href;
    script.addEventListener("error", fallback, { once: true });
    document.body.append(script);
  }

  const fallback = () => {
    host.dataset.mapState = "fallback";
    const tabs = host.querySelector(".thesis-market-map__tabs");
    if (tabs) tabs.hidden = true;
    host.querySelectorAll("[data-market-map-tab]").forEach((button) => {
      button.disabled = true;
      button.tabIndex = -1;
    });
    const canvas = host.querySelector("[data-market-map-canvas]");
    if (canvas) canvas.hidden = true;
    const aside = host.querySelector("[data-market-map-aside]");
    if (aside) aside.hidden = true;
    const status = host.querySelector("[data-market-map-status]");
    if (status) status.textContent = host.dataset.fallbackMessage || "Mapa interactivo no disponible; se conserva la lámina estática.";
  };
  host.addEventListener("thesis-post2-map:fallback", fallback);
  entryPromise.catch(fallback);
  const start = () => load().catch(fallback);
  if (!("IntersectionObserver" in window)) return void start();
  const observer = new IntersectionObserver((entries) => {
    if (!entries.some((entry) => entry.isIntersecting)) return;
    observer.disconnect();
    start();
  }, { rootMargin: "420px" });
  observer.observe(host);
})();
