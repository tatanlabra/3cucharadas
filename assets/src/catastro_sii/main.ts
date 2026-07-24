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
  const container = document.getElementById("map");
  if (!container) return;
  const start = () => {
    import("./app")
      .then(({ CatastroMapApplication }) => CatastroMapApplication.start())
      .then((application) => application.mount())
      .catch(() => {
        const status = document.getElementById("map-status");
        if (status) status.textContent = "La vista agregada sigue disponible; no fue posible iniciar el mapa vectorial.";
      });
  };
  const requested = new URLSearchParams(window.location.search);
  const needsImmediateMap = requested.get("vista") === "mapa" || requested.has("comuna") || window.location.hash === "#cartographic-map";
  if (isLocalPreviewLocation(window.location.hostname, window.location.search) || needsImmediateMap) {
    start();
    return;
  }
  onceNearViewport(container, start, "320px");
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
beginLaboratory();
