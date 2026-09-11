/* Read-only browser instrumentation. Use with agent-browser --init-script.
 * Read window.__catastroPerf after the map reaches its final state. */
(() => {
  window.__catastroPerf = { selectorMs: null, canvasMs: null, mapReadyMs: null, basemapReadyMs: null };
  const observer = new MutationObserver(() => {
    const state = window.__catastroPerf;
    if (state.selectorMs === null && document.querySelector('#bivariate-chile-selector path')) state.selectorMs = performance.now();
    if (state.canvasMs === null && document.querySelector('#bivariate-map canvas')) state.canvasMs = performance.now();
    if (state.mapReadyMs === null && document.querySelector('#bivariate-map')?.closest('.map-ready')) state.mapReadyMs = performance.now();
    if (state.basemapReadyMs === null && document.querySelector('#bivariate-map')?.dataset.basemapState === 'ready') state.basemapReadyMs = performance.now();
  });
  observer.observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['class', 'data-basemap-state'] });
})();
