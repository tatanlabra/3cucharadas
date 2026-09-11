(() => {
  const log = window.__mapTrace = { events: [], milestones: {}, longTasks: [] };
  const event = (type, detail = {}) => { const value = { type, ms: performance.now(), ...detail }; log.events.push(value); performance.mark('catastro:' + type); };
  const mark = (key) => { if (log.milestones[key] == null) { log.milestones[key] = performance.now(); event(key); } };
  const fetch = window.fetch;
  window.fetch = async function(input, options) {
    const url = typeof input === 'string' ? input : input.url || String(input);
    const started = performance.now();
    if (/style\.json|manifest\.json|chile-selector/.test(url)) event('fetch-start', { url });
    try {
      const response = await fetch.call(this, input, options);
      if (/style\.json|manifest\.json|chile-selector/.test(url)) event('fetch-end', { url, duration: performance.now() - started, status: response.status });
      return response;
    } catch (error) {
      event('fetch-error', { url, duration: performance.now() - started, message: error.message });
      throw error;
    }
  };
  const Worker = window.Worker;
  window.Worker = class extends Worker {
    constructor(url, options) {
      event('worker-create-start', { url: String(url) });
      super(url, options);
      event('worker-create-end', { url: String(url) });
      let messages = 0;
      this.addEventListener('message', e => { if (messages++ < 6) event('worker-message', { messageType: e.data?.type, keys: Object.keys(e.data || {}).slice(0, 8) }); });
      this.addEventListener('error', e => event('worker-error', { message: e.message }));
    }
  };
  const getContext = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function(type, ...args) {
    if (!String(type).includes('webgl')) return getContext.call(this, type, ...args);
    const started = performance.now(); event('webgl-start', { canvas: this.className });
    const context = getContext.call(this, type, ...args);
    event('webgl-end', { canvas: this.className, duration: performance.now() - started });
    return context;
  };
  for (const method of ['compileShader', 'linkProgram', 'getProgramParameter', 'getShaderParameter', 'getExtension', 'drawElements']) {
    const original = WebGL2RenderingContext.prototype[method];
    WebGL2RenderingContext.prototype[method] = function(...args) {
      const started = performance.now(); const result = original.apply(this, args); const duration = performance.now() - started;
      if (duration > 50) event('webgl-slow', { method, duration });
      return result;
    };
  }
  const frame = window.requestAnimationFrame;
  window.requestAnimationFrame = function(callback) {
    const started = performance.now();
    return frame.call(this, timestamp => {
      const entered = performance.now();
      if (entered - started > 250) event('frame-wait', { duration: entered - started });
      callback(timestamp);
      const duration = performance.now() - entered;
      if (duration > 100) event('frame-work', { duration });
    });
  };
  new MutationObserver(() => {
    if (document.querySelector('#bivariate-chile-selector path')) mark('selector');
    if (document.querySelector('#bivariate-map canvas')) mark('canvas');
    const map = document.querySelector('#bivariate-map');
    if (map?.closest('.map-ready')) mark('style-controller');
    if (map?.dataset.basemapState === 'ready') mark('basemap-load');
  }).observe(document, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'data-basemap-state'] });
  try { new PerformanceObserver(list => { for (const e of list.getEntries()) log.longTasks.push({ start: e.startTime, duration: e.duration }); }).observe({ type: 'longtask', buffered: true }); } catch {}
})();
