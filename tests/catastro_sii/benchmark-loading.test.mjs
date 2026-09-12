import { strict as assert } from 'node:assert';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { evaluate, focusValid } from '../../scripts/catastro_sii/benchmark_loading.mjs';

const protocol = JSON.parse(readFileSync(new URL('../../docs/catastro-paired-loading-20260911-protocol.json', import.meta.url)));
function fixture() {
  const observations = [];
  for (const variant of ['baseline', 'candidate']) for (const mode of ['cold', 'warm']) {
    for (let i = 0; i < (mode === 'cold' ? 3 : 2); i++) observations.push({
      id: `${variant}-${mode}${i}`, variant, mode, focus_valid: true, paths: 343, timeout: false, network: [],
      signatures: { initial_style: 'identical', manifest: 'identical', final_layers: 'identical' },
      probe: { failures: [], viewport: [1280, 577],
        manifest: { tiles_base: '/assets/local', basemap: { available: true }, communes: { available: true } },
        initialStyle: { sources: { protomaps: {} }, layers: [{ id: 'base', type: 'fill', source: 'protomaps' }] },
        finalStyle: { sources: { protomaps: {} }, layers: [{ id: 'base', type: 'fill', source: 'protomaps' }] },
        milestones: { useful: variant === 'candidate' ? 800 : 1000, selector: 500, load: 750 },
        finalCamera: { center: [-71, -37], zoom: 3, bearing: 0, pitch: 0, size: [750, 558] } },
    });
  }
  return observations;
}
test('empty evidence cannot satisfy counts or performance', () => assert.equal(evaluate([], protocol).pass, false));
test('a synthetic equivalent20%improvement passes declared contract only', () => assert.equal(evaluate(fixture(), protocol).pass, true));
test('a9%improvement fails fixed10%threshold', () => {
  const samples = fixture();
  for (const sample of samples) if (sample.variant === 'candidate' && sample.mode === 'cold') sample.probe.milestones.useful = 910;
  assert.equal(evaluate(samples, protocol).pass, false);
});
test('slow observation stays in sample and blocks if cold median fails', () => {
  const samples = fixture();
  samples.filter(s => s.variant === 'candidate' && s.mode === 'cold').slice(0, 2).forEach(s => { s.probe.milestones.useful = 12000; });
  assert.equal(evaluate(samples, protocol).pass, false);
  assert.equal(evaluate(samples, protocol).excluded_focus.length, 0);
});
test('warm regression above10%blocks even with fast cold', () => {
  const samples = fixture();
  samples.filter(s => s.variant === 'candidate' && s.mode === 'warm').forEach(s => { s.probe.milestones.useful = 1101; });
  assert.equal(evaluate(samples, protocol).pass, false);
});
test('camera and style mismatch each block comparison', () => {
  const cameras = fixture(); cameras[0].probe.finalCamera.zoom += 0.01;
  assert.equal(evaluate(cameras, protocol).pass, false);
  const styles = fixture(); styles[0].probe.initialStyle.layers[0].id = 'different';
  assert.equal(evaluate(styles, protocol).pass, false);
});
test('HTTP errors and timeout cannot be filtered away as slow runs', () => {
  const http = fixture(); http[0].network.push({ event: 'response', status: 404, url: 'http://127.0.0.1:4004/style.json' });
  assert.equal(evaluate(http, protocol).pass, false);
  const timeout = fixture(); timeout[0].timeout = true;
  assert.equal(evaluate(timeout, protocol).pass, false);
});
test('focus rule checks milestones, visibility and continuous loss', () => {
  const focused = { domReady: 10, events: [{ focused: true, visible: true }], focus: [{ ms: 10, focused: true, visible: true }] };
  assert.equal(focusValid(focused), true);
  assert.equal(focusValid({ ...focused, events: [{ focused: false, visible: true }] }), false);
  assert.equal(focusValid({ ...focused, focus: [{ ms: 10, focused: true, visible: false }] }), false);
  assert.equal(focusValid({ ...focused, focus: [{ ms: 10, focused: false, visible: true }, { ms: 111, focused: false, visible: true }] }), false);
});
test('a replaced unfocused timeout remains a hard failure', () => {
  const samples = fixture();
  const failed = structuredClone(samples[0]); failed.id = 'excluded-timeout'; failed.focus_valid = false; failed.timeout = true;
  samples.push(failed);
  assert.ok(evaluate(samples, protocol).failures.includes('excluded-timeout:timeout/no-useful'));
});
test('equal missing styles or manifest never establish equivalence', () => {
  for (const key of ['initialStyle', 'finalStyle', 'manifest']) {
    const samples = fixture(); samples.forEach(s => { delete s.probe[key]; });
    assert.equal(evaluate(samples, protocol).pass, false);
  }
});
test('empty style objects fail closed without throwing', () => {
  const samples = fixture(); samples.forEach(s => { s.probe.finalStyle = {}; });
  assert.equal(evaluate(samples, protocol).pass, false);
});
