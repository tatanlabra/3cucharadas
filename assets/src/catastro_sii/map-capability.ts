type WebGL2Canvas = {
  getContext(contextId: "webgl2"): WebGL2RenderingContext | null;
};

const UNAVAILABLE_MESSAGE = "Este navegador no puede iniciar el mapa vectorial 3D. El selector territorial, las tablas y la metodología siguen disponibles.";

/**
 * MapLibre GL JS 6 requires WebGL2. Check it before loading the map chunk so
 * browsers without that capability retain the non-cartographic evidence path.
 */
export function supportsWebGL2(
  createCanvas: () => WebGL2Canvas = () => document.createElement("canvas")
): boolean {
  try {
    return createCanvas().getContext("webgl2") !== null;
  } catch {
    return false;
  }
}

export function showMapCapabilityFallback(container: HTMLElement, status: HTMLElement | null): void {
  container.replaceChildren();
  container.dataset.mapState = "webgl2-unavailable";

  const message = document.createElement("p");
  message.className = "map-unavailable";
  message.setAttribute("role", "note");
  message.textContent = UNAVAILABLE_MESSAGE;
  container.append(message);

  const note = document.getElementById("bivariate-map-note");
  if (note) note.textContent = "Mapa vectorial no disponible en este navegador.";
  if (status) status.textContent = UNAVAILABLE_MESSAGE;

  for (const id of ["bivariate-map-reset", "bivariate-map-tilt"]) {
    const control = document.getElementById(id);
    if (!(control instanceof HTMLButtonElement)) continue;
    control.disabled = true;
    control.setAttribute("aria-disabled", "true");
  }
}
