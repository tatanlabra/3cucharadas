/* Symmetric observer for isolated benchmark builds. No product state is edited. */
(() => {
  const now = () => performance.now();
  const state = () => ({ ms: now(), visible: document.visibilityState === 'visible', focused: document.hasFocus() });
  const probe = window.__catastroBenchmark = {
    events: [], focus: [state()], failures: [], milestones: {}, idleCandidates: [],
    viewport: [innerWidth, innerHeight], timeOrigin: performance.timeOrigin, initialUrl: location.href,
  };
  for (const name of ['focus', 'blur']) window.addEventListener(name, () => probe.focus.push({ event: name, ...state() }));
  document.addEventListener('visibilitychange', () => probe.focus.push({ event: 'visibilitychange', ...state() }));
  document.addEventListener('DOMContentLoaded', () => { probe.domReady = now(); probe.focus.push({ event: 'dom-ready', ...state() }); });
  window.addEventListener('error', e => probe.failures.push({ type: 'error', ms: now(), message: e.message || 'resource error' }));
  window.addEventListener('unhandledrejection', e => probe.failures.push({ type: 'rejection', ms: now(), message: String(e.reason) }));
  const interval = setInterval(() => probe.focus.push(state()), 50);
  setTimeout(() => clearInterval(interval), 30000);
  const mark = name => {
    if (probe.milestones[name] === undefined) {
      probe.milestones[name] = now();
      probe.events.push({ event: name, ...state() });
    }
  };
  const paths = () => document.querySelectorAll('#bivariate-chile-selector path').length;
  new MutationObserver(() => {
    if (paths() === 343) mark('selector');
    if (document.querySelector('#bivariate-map canvas')) mark('canvas');
  }).observe(document, { subtree: true, childList: true });
  probe.registerMap = (map, container, style, manifest) => {
    mark('map-created');
    probe.initialStyle = JSON.parse(JSON.stringify(style));
    probe.manifest = JSON.parse(JSON.stringify(manifest));
    const camera = () => ({
      center: map.getCenter().toArray(), zoom: map.getZoom(), bearing: map.getBearing(), pitch: map.getPitch(),
      bounds: map.getBounds().toArray(), size: [container.clientWidth, container.clientHeight],
    });
    map.once('style.load', () => mark('style-load'));
    map.once('load', () => { mark('load'); probe.loadCamera = camera(); });
    map.on('error', e => probe.failures.push({ type: 'map', ms: now(), message: String(e.error?.message ?? e.error) }));
    map.on('idle', () => {
      const candidate = { ...state(), paths: paths(), loaded: map.loaded(), tilesLoaded: map.areTilesLoaded(), moving: map.isMoving(), camera: camera() };
      probe.idleCandidates.push(candidate);
      if (candidate.paths !== 343 || !candidate.loaded || !candidate.tilesLoaded || candidate.moving || probe.milestones.useful !== undefined) return;
      mark('useful');
      probe.finalCamera = candidate.camera;
      probe.finalStyle = JSON.parse(JSON.stringify(map.getStyle()));
    });
  };
})();
