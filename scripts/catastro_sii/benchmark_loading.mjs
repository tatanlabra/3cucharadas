import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map(k => [k, canonical(value[k])])) : value;
const hash = value => createHash('sha256').update(typeof value === 'string' ? value : JSON.stringify(canonical(value))).digest('hex');
const median = values => { const sorted = [...values].sort((a, b) => a - b); return sorted.length % 2 ? sorted[(sorted.length - 1) / 2] : (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2; };
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

export function focusValid(probe) {
  if (!probe || probe.events.some(e => !e.focused || !e.visible)) return false;
  const samples = probe.focus.filter(e => e.ms >= (probe.domReady ?? 0));
  if (!samples.length || samples.some(e => !e.visible)) return false;
  let start = null;
  for (const sample of samples) {
    if (!sample.focused && start === null) start = sample.ms;
    if (sample.focused) start = null;
    if (start !== null && sample.ms - start > 100) return false;
  }
  return true;
}

export function evaluate(samples, protocol) {
  const measured = samples.filter(s => s.mode !== 'prime');
  const retained = measured.filter(s => s.focus_valid);
  const failures = [];
  for (const variant of ['baseline', 'candidate']) for (const mode of ['cold', 'warm']) {
    const count = retained.filter(s => s.variant === variant && s.mode === mode).length;
    if (count !== (mode === 'cold' ? 3 : 2)) failures.push(`${variant}/${mode}:expected${mode === 'cold' ? 3 : 2},got${count}`);
  }
  // A focus exclusion may remove timing bias, never hide a functional failure.
  for (const sample of measured) {
    if (sample.timeout || !Number.isFinite(sample.probe?.milestones.useful)) failures.push(`${sample.id}:timeout/no-useful`);
    if (sample.paths !== 343) failures.push(`${sample.id}:selector-paths`);
    if (!Array.isArray(sample.probe?.viewport) || sample.probe.viewport.some((v, i) => v !== protocol.viewport_px[i])) failures.push(`${sample.id}:viewport`);
    if (sample.probe?.failures.length) failures.push(`${sample.id}:runtime-error`);
    if (sample.network.some(e => e.event === 'failed' && !e.canceled)) failures.push(`${sample.id}:network-error`);
    if (sample.network.some(e => e.event === 'response' && e.status >= 400 && /\.(json|js|css|pbf|pmtiles)(?:\?|$)/.test(e.url))) failures.push(`${sample.id}:required-http-error`);
    for (const key of ['initialStyle', 'finalStyle']) {
      const style = sample.probe?.[key];
      if (!style || !style.sources || !Object.keys(style.sources).length || !Array.isArray(style.layers) || !style.layers.length) failures.push(`${sample.id}:missing-${key}`);
    }
    const manifest = sample.probe?.manifest;
    if (!manifest?.tiles_base || manifest.basemap?.available !== true || manifest.communes?.available !== true) failures.push(`${sample.id}:missing-manifest`);
  }
  const complete = retained.filter(s => Number.isFinite(s.probe?.milestones.useful));
  const signatures = ['initial_style', 'manifest', 'final_layers'];
  for (const key of signatures) if (new Set(complete.map(s => {
    if (key === 'initial_style') return hash(s.probe.initialStyle ?? null);
    if (key === 'manifest') return hash(s.probe.manifest ?? null);
    const style = s.probe.finalStyle;
    return hash(style && Array.isArray(style.layers) ? { sources: style.sources, layers: style.layers.map(l => ({ id: l.id, type: l.type, source: l.source, sourceLayer: l['source-layer'] })) } : null);
  })).size !== 1) failures.push(`incomparable:${key}`);
  if (complete.some(s => s.probe.initialStyle?.sources?.['osm-raster'])) failures.push('fallback-style');
  const first = complete[0]?.probe.finalCamera;
  const tolerance = protocol.camera_equivalence_tolerance;
  for (const sample of complete) {
    const camera = sample.probe.finalCamera;
    if (!first || !camera || camera.center.some((v, i) => Math.abs(v - first.center[i]) > tolerance.center_degrees)
      || Math.abs(camera.zoom - first.zoom) > tolerance.zoom
      || Math.abs(camera.bearing - first.bearing) > tolerance.bearing_degrees
      || Math.abs(camera.pitch - first.pitch) > tolerance.pitch_degrees
      || camera.size.some((v, i) => Math.abs(v - protocol.standardized_map_canvas_px[i]) > tolerance.canvas_px)) failures.push(`${sample.id}:incomparable-camera`);
  }
  const medians = {};
  for (const variant of ['baseline', 'candidate']) {
    medians[variant] = {};
    for (const mode of ['cold', 'warm']) {
      const group = complete.filter(s => s.variant === variant && s.mode === mode);
      medians[variant][mode] = Object.fromEntries(['useful', 'selector', 'load'].map(key => [key, group.length ? median(group.map(s => s.probe.milestones[key])) : null]));
    }
  }
  const ratios = {
    cold_primary: medians.candidate.cold.useful / medians.baseline.cold.useful,
    cold_selector: medians.candidate.cold.selector / medians.baseline.cold.selector,
    warm_primary: medians.candidate.warm.useful / medians.baseline.warm.useful,
    warm_selector: medians.candidate.warm.selector / medians.baseline.warm.selector,
  };
  for (const [key, ratio] of Object.entries(ratios)) {
    const maximum = protocol.acceptance[`${key}_median_candidate_over_baseline_max`];
    if (!Number.isFinite(ratio) || ratio > maximum) failures.push(`${key}:ratio${ratio}>${maximum}`);
  }
  return { pass: failures.length === 0, failures, medians, ratios, excluded_focus: samples.filter(s => s.mode !== 'prime' && !s.focus_valid).map(s => s.id) };
}

async function browser(session, probeSource) {
  const cli = (...args) => execFileSync('agent-browser', ['--session', session, ...args], { encoding: 'utf8', timeout: 20000 });
  // Pin the launch mode: desktop/window-manager focus must not vary by config.
  cli('open', 'about:blank', '--headed', 'false');
  cli('set', 'viewport', '1280', '577');
  const endpoint = cli('get', 'cdp-url').trim();
  const socket = new WebSocket(endpoint);
  await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
  let seq = 0, sessionId;
  const pending = new Map(), urls = new Map();
  let network = [];
  const send = (method, params = {}, sessionOverride = sessionId) => new Promise((resolve, reject) => {
    const id = ++seq;
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout:${method}`)); }, 35000);
    pending.set(id, { resolve, reject, timer });
    socket.send(JSON.stringify({ id, method, params, ...(sessionOverride ? { sessionId: sessionOverride } : {}) }));
  });
  socket.addEventListener('message', ({ data }) => {
    const e = JSON.parse(data);
    if (e.id) {
      const p = pending.get(e.id); if (!p) return;
      pending.delete(e.id); clearTimeout(p.timer);
      e.error ? p.reject(new Error(JSON.stringify(e.error))) : p.resolve(e.result);
      return;
    }
    const p = e.params ?? {};
    if (e.method === 'Network.requestWillBeSent') urls.set(p.requestId, p.request.url);
    const url = urls.get(p.requestId);
    if (!url || !/127\.0\.0\.1:4004|tiles\.3cucharadas|tile\.openstreetmap/.test(url)) return;
    if (e.method === 'Network.responseReceived') network.push({ event: 'response', url, status: p.response.status, fromDiskCache: Boolean(p.response.fromDiskCache), timestamp: p.timestamp });
    if (e.method === 'Network.loadingFailed') network.push({ event: 'failed', url, error: p.errorText, canceled: Boolean(p.canceled), cors: p.corsErrorStatus, timestamp: p.timestamp });
  });
  const browserVersion = await send('Browser.getVersion', {}, null);
  if (!browserVersion.userAgent.includes('HeadlessChrome/')) throw new Error('Benchmark requires confirmed headless Chromium');
  const { targetInfos } = await send('Target.getTargets', {}, null);
  const target = targetInfos.find(t => t.type === 'page' && t.url === 'about:blank');
  if (!target) throw new Error('No unique about:blank benchmark target');
  ({ sessionId } = await send('Target.attachToTarget', { targetId: target.targetId, flatten: true }, null));
  await send('Page.enable'); await send('Network.enable');
  await send('Network.setCacheDisabled', { cacheDisabled: false });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'no-preference' }, { name: 'prefers-color-scheme', value: 'light' }] });
  await send('Page.addScriptToEvaluateOnNewDocument', { source: probeSource });
  const evaluateJS = async expression => {
    const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
    return result.result.value;
  };
  return {
    async navigate(url, id, reload = false) {
      await send('Page.bringToFront');
      const before = await evaluateJS(`new Promise(resolve => {const frames=[];const tick=ms=>{frames.push(ms);if(frames.length<10)requestAnimationFrame(tick);else resolve({visible:document.visibilityState==='visible',focused:document.hasFocus(),frames})};requestAnimationFrame(tick)})`);
      if (!before.visible || !before.focused || before.frames.some((v, i, a) => i && v - a[i - 1] > 100)) throw new Error(`Foreground preparation failed:${id}`);
      const previousTimeOrigin = await evaluateJS('performance.timeOrigin');
      network = []; urls.clear();
      const navigated = reload ? await send('Page.reload', { ignoreCache: false }) : await send('Page.navigate', { url });
      if (navigated.errorText) throw new Error(navigated.errorText);
      const started = Date.now(); let snapshot;
      while (Date.now() - started < 30000) {
        await sleep(100);
        snapshot = await evaluateJS(`window.__catastroBenchmark ? ({probe:window.__catastroBenchmark, paths:document.querySelectorAll('#bivariate-chile-selector path').length, now:performance.now(), paints:performance.getEntriesByType('paint').map(e=>({name:e.name,ms:e.startTime})), resources:performance.getEntriesByType('resource').map(e=>({url:e.name,ms:e.startTime,duration:e.duration,transfer:e.transferSize,status:e.responseStatus}))}) : null`);
        if (snapshot?.probe?.timeOrigin !== previousTimeOrigin && snapshot?.probe?.milestones.useful !== undefined && snapshot.now - snapshot.probe.milestones.useful >= 150) break;
      }
      if (!snapshot || snapshot.probe.timeOrigin === previousTimeOrigin) throw new Error('Navigation produced no new document probe');
      const style = snapshot.probe.finalStyle;
      const result = { id, ...snapshot, before, browserVersion, network: [...network], timeout: !Number.isFinite(snapshot.probe.milestones.useful), focus_valid: focusValid(snapshot.probe), signatures: {
        initial_style: hash(snapshot.probe.initialStyle ?? null), manifest: hash(snapshot.probe.manifest ?? null),
        final_layers: hash(style ? { sources: style.sources, layers: style.layers.map(l => ({ id: l.id, type: l.type, source: l.source, sourceLayer: l['source-layer'] })) } : null),
      } };
      return result;
    },
    close() { socket.close(); cli('close'); },
  };
}

async function run(root, freezeFile, protocolPath = join(repo, 'docs/catastro-paired-loading-20260911-protocol.json')) {
  if (existsSync(join(root, 'results.json'))) throw new Error('Refusing to overwrite prior benchmark observations; choose a new result directory');
  const protocolText = readFileSync(protocolPath, 'utf8'), protocol = JSON.parse(protocolText);
  const freeze = readFileSync(freezeFile, 'utf8');
  if (!freeze.includes('FREEZE')) throw new Error('Parent FREEZE receipt required before navigation');
  const probeSource = readFileSync(join(repo, 'scripts/catastro_sii/benchmark_loading_probe.js'), 'utf8');
  const samples = [], warm = new Map(), exclusions = new Map();
  let runError = null;
  const persist = () => writeFileSync(join(root, 'results.json'), JSON.stringify({ protocol_sha256: hash(protocolText), runner_sha256: hash(readFileSync(fileURLToPath(import.meta.url), 'utf8')), run_error: runError, freeze, samples, evaluation: evaluate(samples, protocol) }, null, 2) + '\n');
  try {
    for (const id of protocol.order) {
      const [variant, suffix] = id.split('-'), mode = suffix.startsWith('cold') ? 'cold' : suffix.startsWith('warm') ? 'warm' : 'prime';
      const revision = protocol[variant]; let attempt = 0;
      while (true) {
        attempt++;
        let instance;
        // Closing the CLI daemon and reopening its socket under the same name
        // can race. Each cold observation requires a new process regardless.
        if (mode === 'cold') instance = await browser(`perf-paired-${process.pid}-${id}-${attempt}`, probeSource);
        else {
          if (!warm.has(variant)) warm.set(variant, await browser(`perf-paired-${process.pid}-${variant}`, probeSource));
          instance = warm.get(variant);
        }
        let observation;
        try { observation = await instance.navigate(protocol.server + protocol.route.replace('{revision}', revision), `${id}-attempt${attempt}`, mode === 'warm'); }
        finally { if (mode === 'cold') instance.close(); }
        Object.assign(observation, { variant, mode, ordinal: suffix, revision }); samples.push(observation); persist();
        console.log(JSON.stringify({ id: observation.id, focus_valid: observation.focus_valid, milestones: observation.probe.milestones, failures: observation.probe.failures }));
        if (observation.focus_valid) break;
        const key = `${variant}/${mode}`, count = (exclusions.get(key) ?? 0) + 1;
        exclusions.set(key, count);
        if (count > protocol.invalid_focus_replacement_limit_per_version_mode) throw new Error(`Focus replacement budget exhausted:${key}`);
      }
    }
    persist();
    const verdict = evaluate(samples, protocol); console.log(JSON.stringify(verdict));
    if (!verdict.pass) process.exitCode = 1;
  } catch (error) {
    runError = String(error.message ?? error); persist(); throw error;
  } finally { for (const instance of warm.values()) instance.close(); }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [mode, root, freeze, protocol] = process.argv.slice(2);
  if (mode !== '--run' || !root || !freeze) throw new Error('Usage: benchmark_loading.mjs --run ROOT FREEZE_RECEIPT [PROTOCOL_JSON]');
  await run(resolve(root), resolve(freeze), protocol ? resolve(protocol) : undefined);
}
