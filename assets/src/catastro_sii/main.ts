import "./styles.scss";
import { isLocalPreviewLocation } from "./preview";

function onceNearViewport(element: Element, start: () => void, rootMargin: string): void {
  if (!("IntersectionObserver" in window)) {
    start();
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    if (!entries.some((entry) => entry.isIntersecting)) return;
    observer.disconnect();
    start();
  }, { rootMargin });
  observer.observe(element);
}

function beginMap(): void {
  const container = document.getElementById("bivariate-map");
  if (!container) return;
  const start = () => {
    let moduleLoaded = false;
    const status = document.getElementById("bivariate-map-status") ?? document.getElementById("status");
    container.setAttribute("aria-busy", "true");
    document.getElementById("bivariate-chile-selector")?.setAttribute("aria-busy", "true");
    if (status) status.textContent = "Preparando el selector de Chile y los datos comunales…";
    import("./app")
      .then(({ CatastroMapApplication }) => { moduleLoaded = true; return CatastroMapApplication.start(); })
      .then((application) => application.mount())
      .catch(() => {
        container.setAttribute("aria-busy", "false");
        document.getElementById("bivariate-chile-selector")?.setAttribute("aria-busy", "false");
        if (status) {
          status.replaceChildren(document.createTextNode("No fue posible cargar los datos del mapa. "));
          const retry = document.createElement("button");
          retry.type = "button";
          retry.textContent = moduleLoaded ? "Reintentar" : "Recargar visor";
          retry.addEventListener("click", () => { if (moduleLoaded) start(); else window.location.reload(); }, { once: true });
          status.append(retry);
        }
      });
  };
  const requested = new URLSearchParams(window.location.search);
  const needsImmediateMap = requested.get("vista") === "mapa" || requested.has("comuna") || window.location.hash === "#bivariate-card";
  if (isLocalPreviewLocation(window.location.hostname, window.location.search) || needsImmediateMap) {
    start();
    return;
  }
  const saveData = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData;
  // Start at the selector/card, not the map situated several paragraphs below.
  onceNearViewport(document.getElementById("bivariate-card") ?? container, start, saveData ? "0px" : "640px");
}

function beginCoverageTeaser(): void {
  const container = document.getElementById("coverage-teaser-chart");
  if (!container) return;
  const start = () => {
    import("./coverage-teaser")
      .then(({ mountCoverageTeaser }) => mountCoverageTeaser())
      .catch(() => {
        const status = document.getElementById("coverage-teaser-status");
        if (status) status.textContent = "No fue posible cargar este gráfico introductorio; el resto del visor sigue disponible.";
      });
  };
  onceNearViewport(container, start, "480px");
}

function beginLaboratory(): void {
  const host = document.getElementById("denominator-lab");
  if (!host) return;
  const start = () => {
    import("./analytics")
      .then(({ mountDenominatorLaboratory }) => mountDenominatorLaboratory())
      .catch(() => {
        host.dataset.state = "error";
        const status = document.getElementById("lab-status");
        if (status) status.textContent = "No fue posible iniciar el laboratorio. El mapa y las tablas comunales siguen disponibles.";
      });
  };
  const requestedView = new URLSearchParams(window.location.search).get("vista");
  if (["flujo", "avaluos", "distribuciones", "sensibilidad", "comunas"].includes(requestedView ?? "")) start();
  else onceNearViewport(host, start, "420px");
}

beginMap();
beginCoverageTeaser();
beginLaboratory();

function beginFiscalGap(): void {
  const host = document.getElementById("brecha-contribuciones");
  if (!host) return;
  const start = () => import("./fiscal-gap").then(m => m.mountFiscalGap()).catch(() => {
    const status = document.getElementById("fiscal-gap-selection");
    if (status) status.textContent = "Vista interactiva no disponible; el gráfico estático y la tabla conservan el diagnóstico nacional.";
    const chart = document.getElementById("fiscal-gap-chart");
    if (chart) chart.hidden = true;
    const fallback = document.getElementById("fiscal-gap-static");
    if (fallback) fallback.hidden = false;
    for (const id of ["modeled-tax-chart", "modeled-tax-current"]) {
      const element = document.getElementById(id);
      if (element) element.hidden = true;
    }
    const modelStatus = document.getElementById("modeled-tax-status");
    if (modelStatus) modelStatus.textContent = "Vista interactiva no disponible. La tabla de las 15 comunas conserva los escenarios nacionales y su sensibilidad.";
    const q = document.getElementById("modeled-tax-q");
    if (q instanceof HTMLSelectElement) q.disabled = true;
  });
  if (window.location.hash === "#brecha-contribuciones") void start();
  else onceNearViewport(host, () => { void start(); }, "420px");
}
beginFiscalGap();
