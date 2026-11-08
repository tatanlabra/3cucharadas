import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import test from 'node:test';
import { expectedFigureLinks, figureLinksComplete,
  resetGateVerdict } from '../scripts/verify_thesis_series_browser.mjs';

const root = resolve(import.meta.dirname, '..');
const script = resolve(root, 'scripts/verify_thesis_post3_browser.mjs');
const script4 = resolve(root, 'scripts/verify_thesis_post4_browser.mjs');
const visual = resolve(root, 'scripts/verify_thesis_visual_quality.mjs');
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const run = (file, args) => {
  const result = spawnSync('node', [file, ...args], { cwd: root, encoding: 'utf8' });
  assert.equal(result.error, undefined);
  return { status: result.status, data: JSON.parse(result.stdout.trim() || result.stderr.trim()) };
};

test('public CI passes only its public scope; local exact interval check remains separate', () => {
  assert.deepEqual(resetGateVerdict(3, true, false),
    { status: 'PASS_PUBLIC_SCOPE', exitCode: 0 });
  assert.deepEqual(resetGateVerdict(3, true, null),
    { status: 'PASS_PUBLIC_SCOPE', exitCode: 0 });
  assert.deepEqual(resetGateVerdict(3, true, true),
    { status: 'PASS', exitCode: 0 });
  assert.deepEqual(resetGateVerdict(3, false, false),
    { status: 'FAIL', exitCode: 1 });
  assert.deepEqual(resetGateVerdict(4, true, null),
    { status: 'PASS', exitCode: 0 });
});

function syntheticManifest(folder) {
  const stem = 'post3-progression-historical';
  const header = 'outcome,era,cohort_year,cohort_range,estimand,estimation_status,identification_status,estimate_pp,n_treated,limitation\n';
  const row = 'progression,historical,2005,,descriptive,ESTIMABLE_DESCRIPTIVE,DESCRIPTIVE_ONLY,5.7,100,No causal claim\n';
  const files = [];
  for (const name of ['results-all.csv', `${stem}.csv`]) {
    const bytes = Buffer.from(header + row);
    writeFileSync(resolve(folder, name), bytes);
    files.push({ name, sha256: sha256(bytes) });
  }
  for (const lang of ['es', 'en']) for (const theme of ['light', 'dark'])
    for (const layout of ['desktop', 'mobile']) for (const format of ['svg', 'png']) {
      const name = `${stem}-${lang}-${theme}-${layout}.${format}`;
      const bytes = Buffer.from(`${name}\n`);
      writeFileSync(resolve(folder, name), bytes);
      files.push({ name, sha256: sha256(bytes) });
    }
  const manifest = { f2_complete: false, publication_authorized: false,
    figures: [{ outcome: 'progression', era: 'historical',
      caption_es: 'Cohorte 2005; sin lectura causal.', caption_en: '2005 cohort; no causal reading.',
      source_rows: [{ cohort_year: 2005, estimand: 'descriptive',
        estimation_status: 'ESTIMABLE_DESCRIPTIVE', estimate_pp: 5.7,
        n_treated: 100, limitation: 'No causal claim' }] }], files };
  const path = resolve(folder, 'manifest.json');
  writeFileSync(path, JSON.stringify(manifest));
  return { path, stem };
}

function syntheticAnticipation(folder) {
  const sourceRoot = resolve(folder, 'source-json');
  mkdirSync(sourceRoot);
  const files = [], figures = [], rows = [], sourceFiles = [];
  const columns = ['outcome', 'era', 'cohort_year', 'baseline_year', 'transition_year',
    'arm', 'n', 'schools', 'rate_pp', 'display_status', 'reason_es', 'reason_en'];
  const writeAsset = (name, contents) => {
    const bytes = Buffer.from(contents);
    writeFileSync(resolve(folder, name), bytes);
    files.push({ name, sha256: sha256(bytes) });
  };
  const outcomes = ['grade_progression_or_lag', 'persistent_nonenrollment_two_years'];
  const cohorts = outcomes.flatMap((outcome, index) =>
    Array.from({ length: index === 0 ? 20 : 19 }, (_, i) => ({ outcome, year: 2005 + i })));
  for (let i = 0; i < cohorts.length; i += 1) {
    const { outcome, year } = cohorts[i];
    const name = `${year}_${outcome}.json`;
    const bytes = Buffer.from(JSON.stringify({ outcome, year }));
    writeFileSync(resolve(sourceRoot, name), bytes);
    sourceFiles.push({ name, sha256: sha256(bytes) });
    for (const arm of ['treated', 'control']) {
      const display_status = year === 2005 ? 'NOT_ESTIMABLE_PANEL_BOUNDARY'
        : i >= 2 && i <= 4 ? 'PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY'
          : i === 5 ? 'PRIVACY_SUPPRESSED_SMALL_SCHOOL_GROUP' : 'OBSERVED';
      const observed = display_status === 'OBSERVED';
      rows.push({ outcome, era: year <= 2015 ? 'historical' : 'modern',
        cohort_year: year,
        baseline_year: year === 2005 ? null : year - 2,
        transition_year: year === 2005 ? null : year - 1,
        arm, n: observed ? 100 : null, schools: observed ? 20 : null,
        rate_pp: observed ? 75.1 : null, display_status,
        reason_es: observed ? '' : 'Dato protegido',
        reason_en: observed ? '' : 'Suppressed datum' });
    }
  }
  assert.equal(rows.length, 78);
  assert.equal(rows.filter((row) => row.display_status === 'OBSERVED').length, 66);
  const csv = (selection) => `${columns.join(',')}\n${selection.map((row) =>
    columns.map((column) => row[column] ?? '').join(',')).join('\n')}\n`;
  writeAsset('anticipation-all.csv', csv(rows));
  for (const outcome of outcomes) for (const era of ['historical', 'modern']) {
    const source_rows = rows.filter((row) => row.outcome === outcome && row.era === era);
    const stem = `post3-anticipation-${outcome}-${era}`;
    writeAsset(`${stem}.csv`, csv(source_rows));
    for (const lang of ['es', 'en']) for (const theme of ['light', 'dark'])
      for (const layout of ['desktop', 'mobile']) for (const format of ['svg', 'png'])
        writeAsset(`${stem}-${lang}-${theme}-${layout}.${format}`, `${stem}-${lang}-${theme}-${layout}.${format}`);
    figures.push({ family: 'anticipation', outcome, era, stem,
      axis_min_pct: 0, axis_max_pct: 100,
      caption: { es: 'Registro previo descriptivo.', en: 'Descriptive prior enrollment.' },
      alt: { es: 'Tasas por brazo.', en: 'Rates by arm.' },
      source_citation: { es: 'Fuente agregada.', en: 'Aggregate source.' },
      source_rows });
  }
  sourceFiles.sort((a, b) => a.name.localeCompare(b.name));
  const status_counts = Object.fromEntries(['OBSERVED',
    'PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY', 'PRIVACY_SUPPRESSED_SMALL_SCHOOL_GROUP',
    'NOT_ESTIMABLE_PANEL_BOUNDARY'].map((status) =>
    [status, rows.filter((row) => row.display_status === status).length]));
  const manifest = { family: 'anticipation', f2_complete: false,
    publication_authorized: false, rows: 78, observed_rows: status_counts.OBSERVED,
    status_counts,
    source_files: sourceFiles, source_sha256: sha256(JSON.stringify(sourceFiles)),
    figures, files };
  const path = resolve(folder, 'anticipation-manifest.json');
  writeFileSync(path, JSON.stringify(manifest));
  return { path, sourceRoot, manifest, figures };
}

function syntheticSensitivity(folder) {
  const files = [], figures = [];
  const sourceSha = 'a'.repeat(64);
  const writeAsset = (name, contents) => {
    const bytes = Buffer.from(contents);
    writeFileSync(resolve(folder, name), bytes);
    files.push({ name, sha256: sha256(bytes) });
  };
  const csv = (rows) => {
    const columns = [...new Set(rows.flatMap((row) => Object.keys(row)))].sort();
    const cell = (value) => value == null ? '' : typeof value === 'boolean'
      ? value ? 'True' : 'False' : String(value);
    return `${columns.join(',')}\n${rows.map((row) => columns.map((column) =>
      cell(row[column])).join(',')).join('\n')}\n`;
  };
  const outcomes = ['grade_progression_or_lag','persistent_nonenrollment_two_years'];
  const pairs = outcomes.flatMap((outcome) => ['historical','modern'].map((era) => ({ outcome, era })));
  const periods = (outcome, era, did = false) => [era === 'historical' ? did ? 2008 : 2005 : 2016,
    era === 'historical' ? 2015 : outcome === outcomes[0] ? 2024 : 2023];
  const did = pairs.map(({ outcome, era }, index) => {
    const [cohort_start, cohort_end] = periods(outcome, era, true);
    return { outcome, era, cohort_start, cohort_end, estimate_pp: index + 1,
      school_ci_low_pp: index, school_ci_high_pp: index + 2,
      two_way_ci_low_pp: index - 0.5, two_way_ci_high_pp: index + 2.5,
      confidence_level: 0.95, school_precision_flag: 'SCHOOL_CLUSTER_CI',
      two_way_status: 'TWO_WAY_ASYMPTOTIC_DIAGNOSTIC_WEAK_CLUSTER_PRECISION',
      status: 'ESTIMABLE_DESCRIPTIVE' };
  });
  const bounds = pairs.map(({ outcome, era }, index) => {
    const [cohort_start, cohort_end] = periods(outcome, era);
    return { outcome, era, cohort_start, cohort_end, lower_pp: index - 1,
      upper_pp: index + 2, status: 'PARTIAL_IDENTIFICATION_DESCRIPTIVE',
      target_population: 'fixed_baseline_cells_before_outcome_missingness',
      bound_interpretation: outcome === outcomes[0] ? 'Unknown grades' : 'True non-schooling',
      directly_comparable_to_primary_point: false };
  });
  const d1 = outcomes.flatMap((outcome) => {
    const historical = { outcome, era: 'historical', contrast: null,
      cohort_start: 2005, cohort_end: 2015, estimate_pp: null,
      ci_low_pp: null, ci_high_pp: null,
      status: 'NON_DISCRIMINATING_IDENTICAL_EXPOSURE_FLAGS' };
    const modern = ['main_full','main_common','alternative_common','alternative_full']
      .map((contrast, index) => ({ outcome, era: 'modern', contrast,
        cohort_start: 2016, cohort_end: outcome === outcomes[0] ? 2024 : 2023,
        estimate_pp: 4 - index, ci_low_pp: 3 - index, ci_high_pp: 5 - index,
        confidence_level: index === 0 ? 0.9875 : 0.95,
        status: 'ESTIMABLE_DESCRIPTIVE', main_sample_shift_pp: -0.1,
        definition_on_common_sample_shift_pp: 0,
        alternative_sample_shift_pp: -2.9, overall_alternative_minus_main_pp: -3 }));
    return [historical, ...modern];
  });
  const units = {
    did: Object.fromEntries(['estimate_pp','school_ci_low_pp','school_ci_high_pp',
      'two_way_ci_low_pp','two_way_ci_high_pp'].map((key) => [key,'percentage_points'])),
    bounds: { lower_pp: 'percentage_points', upper_pp: 'percentage_points' },
    d1_d2: Object.fromEntries(['estimate_pp','ci_low_pp','ci_high_pp','main_sample_shift_pp',
      'definition_on_common_sample_shift_pp','alternative_sample_shift_pp',
      'overall_alternative_minus_main_pp'].map((key) => [key,'percentage_points']))
  };
  writeAsset('sensitivity-inventory-all.csv', csv(Array.from({ length: 49 }, (_, index) =>
    ({ name: `source_${index}`, outcome: '', metric: '', era: 'historical', status: 'OBSERVED' }))));
  writeAsset('sensitivity-did-all.csv', csv(Array.from({ length: 37 }, (_, index) =>
    ({ outcome: outcomes[index % 2], era: index < 19 ? 'historical' : 'modern',
      cohort_year: 2005 + index, estimate_pp: 1 }))));
  for (const [kind, source_rows, stem, interval_type] of [
    ['did',did,'post3-sensitivity-did','two_nominal_95pct_methods'],
    ['bounds',bounds,'post3-sensitivity-bounds','partial_identification_not_ci'],
    ['d1_d2',d1,'post3-sensitivity-d1-d2','nominal_98_75pct_full_d2_otherwise_95pct']]) {
    writeAsset(`${stem}.csv`, csv(source_rows));
    for (const lang of ['es','en']) for (const theme of ['light','dark'])
      for (const layout of ['desktop','mobile']) for (const format of ['svg','png'])
        writeAsset(`${stem}-${lang}-${theme}-${layout}.${format}`,
          `${stem}-${lang}-${theme}-${layout}.${format}`);
    figures.push({ family: 'sensitivity', kind, stem, source_rows, units: units[kind],
      interval_type, axis_bound_pp: 10,
      caption: { es: 'Cotas de no escolarización real, descriptivas.',
        en: 'Descriptive bounds for actual non-enrollment.' },
      alt: { es: 'No escolarización real; cotas, no intervalos.',
        en: 'Actual non-enrollment; bounds, not intervals.' },
      source_citation: { es: `Fuente ${sourceSha}`, en: `Source ${sourceSha}` } });
  }
  const path = resolve(folder,'sensitivity-manifest.json');
  writeFileSync(path, JSON.stringify({ family: 'sensitivity', all_source_rows: 49,
    source_sha256: sourceSha, f2_complete: false, publication_authorized: false,
    units, figures, files }));
  return { path, figures };
}

function syntheticIvPublic(folder) {
  const writeAsset = (name, value, files) => {
    const bytes = Buffer.from(value);
    writeFileSync(resolve(folder,name),bytes);
    files.push({ name, sha256: sha256(bytes) });
  };
  const saveManifest = (name, payload) => {
    const path = resolve(folder,name);
    writeFileSync(path,JSON.stringify(payload));
    return path;
  };
  const primaryFiles = [], primaryFigures = [], primaryRows = [];
  const primaryHeader = ['outcome','era','cohort','estimand','estimation_status',
    'identification_status','estimate_pp','n_treated','n_control','rates','limitation'];
  const primaryCsv = (rows) => `${primaryHeader.join(',')}\n${rows.map((row) =>
    primaryHeader.map((key) => row[key] ?? '').join(',')).join('\n')}\n`;
  for (const era of ['historical','modern']) {
    const row = { outcome:'any_he_2yr',era,cohort:'',estimand:'descriptive',
      estimation_status:'ESTIMABLE_DESCRIPTIVE',identification_status:'DESCRIPTIVE_ONLY',
      estimate_pp:1.5,n_treated:100,n_control:200,rates:'50',limitation:'No causal claim' };
    primaryRows.push(row);
    const stem = `post4-access-${era}`;
    writeAsset(`${stem}.csv`,primaryCsv([row]),primaryFiles);
    for (const lang of ['es','en']) for (const theme of ['light','dark'])
      for (const layout of ['desktop','mobile']) for (const format of ['svg','png'])
        writeAsset(`${stem}-${lang}-${theme}-${layout}.${format}`,
          format === 'svg' ? '<svg><text>Safe</text></svg>' : 'PNG',primaryFiles);
    primaryFigures.push({ kind:'access',era,source_rows:[row],
      caption_es:'Acceso descriptivo.',caption_en:'Descriptive access.' });
  }
  writeAsset('results-all.csv',primaryCsv(primaryRows),primaryFiles);
  const primary = { family:'post4_primary_projected',source_sha256:'a'.repeat(64),
    f2_complete:false,publication_authorized:false,
    figures:primaryFigures,files:primaryFiles };
  const primaryPath = saveManifest('iv-primary-manifest.json',primary);
  const sensitivityFiles = [], sensitivityFigures = [];
  const columns = ['variant','outcome','era','cohort_start','cohort_end','estimand',
    'estimate_pp','ci_low_pp','ci_high_pp','confidence_level','treated_schools',
    'control_schools','estimation_status','identification_status','limitation'];
  const csv = (rows, fields = columns) => `${fields.join(',')}\n${rows.map((row) =>
    fields.map((key) => row[key] ?? '').join(',')).join('\n')}\n`;
  const comparison = ['primary','stable_attributes','other_commune',
    'common_grade_year_support','age_gender_treated_post_standardized',
    'never_plus_future_school_exposure','never_plus_future_outcome',
    'future_only_school_exposure','future_only_outcome',
    'school_student_two_way_variance','fixed_effects_diagnostic'];
  const calendar = ['pretrend_placebo_late','late_strict_pre',
    'pretrend_placebo_early','early_strict_pre'];
  const all = { comparison:[],calendar:[] };
  for (const kind of ['comparison','calendar']) for (const era of ['historical','modern']) {
    const variants = kind === 'comparison' ? comparison : calendar;
    const source_rows = variants.map((variant,index) => ({ variant,outcome:'any_he_2yr',era,
      cohort_start:era === 'historical' ? 2009 : 2016,
      cohort_end:era === 'historical' ? 2015 : 2022,
      estimand:'descriptive',estimate_pp:1+index,ci_low_pp:index,ci_high_pp:2+index,
      confidence_level:variant === 'fixed_effects_diagnostic' ? 0.95 : 0.975,
      treated_schools:1561,control_schools:2050,
      estimation_status:'ESTIMABLE_DESCRIPTIVE',identification_status:
        variant === 'school_student_two_way_variance'
          ? 'DESCRIPTIVE_PRECISION_SENSITIVITY_ONLY' : 'DESCRIPTIVE_ONLY',
      limitation:'No causal claim' }));
    all[kind].push(...source_rows);
    const stem = `post4-sensitivity-${kind}-${era}`;
    for (const lang of ['es','en']) for (const theme of ['light','dark'])
      for (const layout of ['desktop','mobile']) for (const format of ['svg','png'])
        writeAsset(`${stem}-${lang}-${theme}-${layout}.${format}`,
          format === 'svg' ? '<svg><text>Safe</text></svg>' : 'PNG',sensitivityFiles);
    sensitivityFigures.push({ family:'sensitivity',kind,era,stem,axis_bound_pp:20,
      csv_file:`post4-sensitivity-${kind}-all.csv`,
      source_rows,caption:{es:'Contrastes descriptivos.',en:'Descriptive contrasts.'},
      alt:{es:'Puntos e intervalos.',en:'Points and intervals.'},
      source_citation:{es:'Fuente proyectada.',en:'Projected source.'} });
  }
  writeAsset('post4-sensitivity-comparison-all.csv',csv(all.comparison),sensitivityFiles);
  writeAsset('post4-sensitivity-calendar-all.csv',csv(all.calendar),sensitivityFiles);
  const matrix = ['any_he_2yr','persistence_3yr','graduation_6yr'].flatMap((outcome) =>
    [1,2,3].flatMap((grade) => ['late','early'].map((comparison) =>
      ({ outcome,grade,comparison }))));
  writeAsset('post4-sensitivity-calendar-window-matrix.csv',
    csv(matrix,['outcome','grade','comparison']),sensitivityFiles);
  for (const kind of ['comparison','calendar']) for (const lang of ['es','en']) {
    const decimal = (value) => value.toFixed(1).replace('.',lang === 'es' ? ',' : '.');
    const count = (value) => value.toLocaleString(lang === 'es' ? 'es-CL' : 'en-US');
    const rows = all[kind].map((row) => `<tr><td>${row.era}</td><th>${row.variant}</th>`
      + `<td>${row.cohort_start}–${row.cohort_end}</td><td>${decimal(row.estimate_pp)}</td>`
      + `<td>[${decimal(row.ci_low_pp)}, ${decimal(row.ci_high_pp)}]</td>`
      + `<td>${decimal(row.confidence_level*100)} %</td>`
      + `<td>${count(row.treated_schools)}</td><td>${count(row.control_schools)}</td>`
      + '<td>Safe</td></tr>');
    writeAsset(`post4-sensitivity-${kind}-table-${lang}.html`,
      `<table><tbody>${rows.join('')}</tbody></table>`,sensitivityFiles);
  }
  for (const lang of ['es','en']) writeAsset(
    `post4-sensitivity-calendar-window-matrix-${lang}.html`,
    '<table><tr><td>Safe</td></tr></table>',sensitivityFiles);
  const projectionRows = [...primaryRows.map((row) => ({ ...row,variant:'primary',
    estimate_pp:1,ci_low_pp:0,ci_high_pp:2,confidence_level:0.975,
    treated_schools:1561,control_schools:2050,
    cohort:null,cohort_range:[row.era === 'historical' ? 2009 : 2016,
      row.era === 'historical' ? 2015 : 2022] })),
  ...[...all.comparison.filter((row) => row.variant !== 'primary'),...all.calendar]
    .map((row) => ({ ...row,cohort:null,
      cohort_range:[row.cohort_start,row.cohort_end] }))];
  while (projectionRows.length < 2075) projectionRows.push({ variant:'filler',
    outcome:'filler',era:'historical',cohort:projectionRows.length,
    rates:null,n_treated:null,n_control:null });
  const projectedBytes = JSON.stringify({
    status:'PUBLIC_POST4_DESCRIPTIVE_PROJECTION',
    results:projectionRows,coverage:Array.from({ length:5040 },() => ({})) });
  const projectedSha = sha256(projectedBytes);
  writeAsset('public-combined-projection.json',projectedBytes,primaryFiles);
  primary.source_sha256 = projectedSha;
  primary.source_file = 'public-combined-projection.json';
  saveManifest('iv-primary-manifest.json',primary);
  const sensitivity = { family:'sensitivity',series:'IV',source_sha256:projectedSha,
    source_file:'public-combined-projection.json',
    f2_complete:false,publication_authorized:false,figures:sensitivityFigures,
    files:sensitivityFiles };
  writeAsset('public-combined-projection.json',projectedBytes,sensitivityFiles);
  const sensitivityPath = saveManifest('iv-sensitivity-manifest.json',sensitivity);
  return { primaryPath,sensitivityPath,primary,sensitivity,saveManifest,primaryCsv,csv };
}

test('reset manifest binds every variant and exact CSV rows without old golden', () => {
  const folder = mkdtempSync(resolve(tmpdir(), 'thesis-reset-browser-test-'));
  try {
    const { path, stem } = syntheticManifest(folder);
    const anticipation = syntheticAnticipation(folder);
    const sensitivity = syntheticSensitivity(folder);
    const args = ['--reset-manifest', path, '--reset-manifest', anticipation.path,
      '--reset-manifest', sensitivity.path,
      '--anticipation-source-root', anticipation.sourceRoot];
    const baseline = run(script, args);
    assert.equal(baseline.status, 1);
    assert.deepEqual(baseline.data.failures, []);
    assert.equal(baseline.data.scientificReady, false);
    assert.equal(baseline.data.figures, 8);
    assert.equal(baseline.data.files, 140);
    assert.equal(baseline.data.sourceVerification, 'local_sha256_39_files');
    assert.equal(baseline.data.sensitivitySourceVerification, 'unbound');
    for (const fixture of ['wrong-estimate', 'wrong-denominator', 'wrong-reason']) {
      const red = run(script, [...args, '--reset-fixture', fixture]);
      assert.equal(red.status, 1);
      assert.equal(red.data.status, 'EXPECTED_FAIL');
      assert.deepEqual(red.data.baselineFailures, []);
      assert.ok(red.data.mutantFailures.includes(`figure-csv-master:${stem}:0`));
    }
    for (const fixture of ['wrong-rate', 'wrong-arm', 'wrong-cohort', 'privacy-leak']) {
      const red = run(script, [...args, '--reset-fixture', fixture]);
      assert.equal(red.status, 1, fixture);
      assert.equal(red.data.status, 'EXPECTED_FAIL', fixture);
      assert.deepEqual(red.data.baselineFailures, [], fixture);
      assert.ok(red.data.mutantFailures.includes(red.data.expected), fixture);
    }
    for (const fixture of ['sensitivity-wrong-did-school-ci',
      'sensitivity-wrong-bound','sensitivity-wrong-d1-period']) {
      const red = run(script, [...args, '--reset-fixture', fixture]);
      assert.equal(red.status, 1, fixture);
      assert.equal(red.data.status, 'EXPECTED_FAIL', fixture);
      assert.deepEqual(red.data.baselineFailures, [], fixture);
      assert.ok(red.data.mutantFailures.includes(red.data.expected), fixture);
    }
    const asset = resolve(folder, `${stem}-es-light-mobile.svg`);
    const before = readFileSync(asset);
    writeFileSync(asset, 'tampered');
    const hashRed = run(script, args);
    assert.equal(hashRed.status, 1);
    assert.ok(hashRed.data.failures.includes('manifest-source-hash'));
    assert.deepEqual(hashRed.data.manifests[0].sourceMismatches, [`${stem}-es-light-mobile.svg`]);
    writeFileSync(asset, before);
    const recovered = run(script, args);
    assert.deepEqual(recovered.data.failures, []);
    const primaryOnly = run(script, ['--reset-manifest', path]);
    assert.ok(primaryOnly.data.failures.includes('manifest-family-inventory'));
    const custodyOnly = run(script, args.filter((arg, index) =>
      arg !== '--anticipation-source-root' && args[index - 1] !== '--anticipation-source-root'));
    assert.deepEqual(custodyOnly.data.failures, []);
    assert.equal(custodyOnly.data.sourceVerification, 'public_custody_only_requires_local_f2_receipt');
    const source = resolve(anticipation.sourceRoot, anticipation.manifest.source_files[0].name);
    const originalSource = readFileSync(source);
    writeFileSync(source, 'tampered');
    const sourceRed = run(script, args);
    assert.ok(sourceRed.data.failures.includes('anticipation-source-hash'));
    writeFileSync(source, originalSource);
    assert.deepEqual(run(script, args).data.failures, []);
  } finally { rmSync(folder, { recursive: true, force: true }); }
});

test('SVG geometry fixtures observe a healthy baseline then red', () => {
  for (const fixture of ['missing-mark', 'small-text', 'low-contrast', 'text-overlap',
    'text-mark', 'anticipation-missing-mark', 'anticipation-private-mark',
    'anticipation-wrong-rate-mark', 'anticipation-description-leak',
    'sensitivity-wrong-ci-geometry', 'sensitivity-missing-zero-reference',
    'sensitivity-bounds-false-point', 'sensitivity-bounds-wrong-label',
    'sensitivity-d1-wrong-period', 'iv-sensitivity-wrong-ci',
    'iv-sensitivity-missing-zero', 'iv-sensitivity-private-label']) {
    const result = run(visual, ['--reset-fixture', fixture]);
    assert.equal(result.status, 1);
    assert.equal(result.data.status, 'EXPECTED_FAIL');
    assert.deepEqual(result.data.baseline.failures, []);
    assert.ok(result.data.mutated.failures.some((failure) =>
      failure.startsWith(result.data.expected)));
  }
});

test('IV public derivatives reject reinserted person counts and arm rates after hash update', () => {
  const folder = mkdtempSync(resolve(tmpdir(), 'thesis-iv-public-browser-test-'));
  try {
    const fixture = syntheticIvPublic(folder);
    const args = ['--reset-manifest',fixture.primaryPath,'--reset-manifest',fixture.sensitivityPath];
    const baseline = run(script4,args);
    assert.equal(baseline.status,1);
    assert.deepEqual(baseline.data.failures,[]);
    assert.equal(baseline.data.ivPublicProjectionBound,true);
    const mutate = (manifest,path,name,contents,expected) => {
      const file = resolve(folder,name), before = readFileSync(file);
      const oldHash = manifest.files.find((entry) => entry.name === name).sha256;
      writeFileSync(file,contents);
      manifest.files.find((entry) => entry.name === name).sha256 = sha256(contents);
      writeFileSync(path,JSON.stringify(manifest));
      const red = run(script4,args);
      assert.equal(red.status,1,name);
      assert.ok(red.data.failures.some((failure) => failure.startsWith(expected)),
        `${name}: ${red.data.failures.join(',')}`);
      assert.ok(!red.data.failures.includes('manifest-source-hash'),name);
      writeFileSync(file,before);
      manifest.files.find((entry) => entry.name === name).sha256 = oldHash;
      writeFileSync(path,JSON.stringify(manifest));
      assert.deepEqual(run(script4,args).data.failures,[],name);
    };
    for (const key of ['n_treated','rates']) {
      const name = 'post4-sensitivity-comparison-all.csv';
      const lines = readFileSync(resolve(folder,name),'utf8').trimEnd().split('\n');
      const changed = `${lines.map((line,index) => `${line},${index ? '7' : key}`).join('\n')}\n`;
      mutate(fixture.sensitivity,fixture.sensitivityPath,name,changed,
        'iv-sensitivity-person-column');
    }
    const html = 'post4-sensitivity-comparison-table-es.html';
    mutate(fixture.sensitivity,fixture.sensitivityPath,html,
      '<table><tr><td>N=7</td></tr></table>','iv-public-text-person-field');
    mutate(fixture.sensitivity,fixture.sensitivityPath,html,
      '<table><tr><td>tasa=50</td></tr></table>','iv-public-text-person-field');
    const tableBefore = readFileSync(resolve(folder,html),'utf8');
    for (const [oldCell,newCell] of [
      ['<td>1,0</td>','<td>9,0</td>'],
      ['<td>1,0</td>','<td></td>'],
      ['<td>1,0</td>','<td>NaN</td>'],
      ['<td>1,0</td>','<td>Infinity</td>'],
      ['<td>[0,0, 2,0]</td>','<td>NaN [0,0, 2,0]</td>'],
      ['<td>97,5 %</td>','<td></td>'],
      ['<td>1.561</td>','<td>1.562</td>'],
      ['<td>1.561</td>','<td>1.56</td>'],
      ['<td>1.561</td>','<td>1,561</td>'],
    ]) {
      assert.ok(tableBefore.includes(oldCell),oldCell);
      mutate(fixture.sensitivity,fixture.sensitivityPath,html,
        tableBefore.replace(oldCell,newCell),'iv-sensitivity-table-values');
    }
    const enTable = 'post4-sensitivity-comparison-table-en.html';
    const enBefore = readFileSync(resolve(folder,enTable),'utf8');
    assert.ok(enBefore.includes('<td>1,561</td>'));
    for (const bad of ['1,562','1,56','1.561'])
      mutate(fixture.sensitivity,fixture.sensitivityPath,enTable,
        enBefore.replace('<td>1,561</td>',`<td>${bad}</td>`),
        'iv-sensitivity-table-values');
    const svg = 'post4-sensitivity-comparison-historical-es-light-mobile.svg';
    mutate(fixture.sensitivity,fixture.sensitivityPath,svg,
      '<svg><text>N=7</text></svg>','iv-public-text-person-field');
    mutate(fixture.sensitivity,fixture.sensitivityPath,svg,
      '<svg><text>rate=50</text></svg>','iv-public-text-person-field');
    const primaryCsv = 'results-all.csv';
    const before = readFileSync(resolve(folder,primaryCsv),'utf8');
    const injected = before + 'persistence_3yr,historical,,descriptive,ESTIMABLE_DESCRIPTIVE,DESCRIPTIVE_ONLY,1.5,7,200,50,No causal claim\n';
    mutate(fixture.primary,fixture.primaryPath,primaryCsv,injected,
      'iv-public-person-field');
    const first = fixture.sensitivity.figures[0].source_rows[0];
    const savedCi = first.ci_low_pp;
    first.ci_low_pp += 0.5;
    writeFileSync(fixture.sensitivityPath,JSON.stringify(fixture.sensitivity));
    const ciRed = run(script4,args);
    assert.ok(ciRed.data.failures.some((failure) =>
      failure.startsWith('iv-sensitivity-figure-csv:')));
    assert.ok(ciRed.data.failures.some((failure) =>
      failure.startsWith('iv-sensitivity-projection-values:')));
    first.ci_low_pp = savedCi;
    writeFileSync(fixture.sensitivityPath,JSON.stringify(fixture.sensitivity));
    assert.deepEqual(run(script4,args).data.failures,[]);
  } finally { rmSync(folder,{ recursive:true,force:true }); }
});

test('artifact manifest discovery binds nested route and rejects drift or duplicate SHA', () => {
  const folder = mkdtempSync(resolve(tmpdir(), 'thesis-iv-artifact-route-test-'));
  try {
    const fixture = syntheticIvPublic(folder);
    const artifactRoot = resolve(folder,'site');
    const locations = [
      { manifest:fixture.primary, path:fixture.primaryPath,
        base:'assets/images/tesis-post4/scientific-reset' },
      { manifest:fixture.sensitivity, path:fixture.sensitivityPath,
        base:'assets/images/tesis-post4/scientific-reset/sensitivity' }
    ];
    for (const item of locations) {
      const destination = resolve(artifactRoot,item.base);
      mkdirSync(destination,{ recursive:true });
      writeFileSync(resolve(destination,'manifest.json'),readFileSync(item.path));
      for (const file of item.manifest.files)
        writeFileSync(resolve(destination,file.name),readFileSync(resolve(folder,file.name)));
    }
    const args = ['--reset-manifest',fixture.primaryPath,'--reset-manifest',
      fixture.sensitivityPath,'--artifact-root',artifactRoot];
    const baseline = run(script4,args);
    assert.deepEqual(baseline.data.failures,[]);
    assert.deepEqual(baseline.data.manifests.map((entry) => entry.assetBase),
      locations.map((item) => `/${item.base}`));
    assert.ok(baseline.data.manifests.every((entry) => entry.manifestBound));
    const drift = resolve(artifactRoot,locations[0].base,'results-all.csv');
    const original = readFileSync(drift);
    writeFileSync(drift,'changed');
    assert.ok(run(script4,args).data.failures.includes('manifest-artifact-hash'));
    writeFileSync(drift,original);
    assert.deepEqual(run(script4,args).data.failures,[]);
    const duplicate = resolve(artifactRoot,'assets/images/tesis-post4/duplicate');
    mkdirSync(duplicate,{ recursive:true });
    writeFileSync(resolve(duplicate,'manifest.json'),readFileSync(fixture.primaryPath));
    const ambiguous = run(script4,args);
    assert.ok(ambiguous.data.failures.includes('manifest-artifact-binding'));
    assert.equal(ambiguous.data.manifests[0].assetBase,null);
    rmSync(duplicate,{ recursive:true,force:true });
    assert.deepEqual(run(script4,args).data.failures,[]);
  } finally { rmSync(folder,{ recursive:true,force:true }); }
});

test('IV sensitivity figure links require shared CSV and both fallback formats', () => {
  const figure = { family:'sensitivity',kind:'comparison',era:'historical',
    assetBase:'/assets/images/tesis-post4/scientific-reset/sensitivity',
    csv_file:'post4-sensitivity-comparison-all.csv' };
  const expected = expectedFigureLinks(4,figure,'post4-sensitivity-comparison-historical',
    'es','light');
  assert.deepEqual(expected,[
    '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-all.csv',
    '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-historical-es-light-desktop.svg',
    '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-historical-es-light-desktop.png'
  ]);
  assert.equal(figureLinksComplete(expected,expected),true);
  assert.equal(figureLinksComplete(expected.slice(1),expected),false);
  assert.equal(figureLinksComplete([expected[0].replace('comparison-all','calendar-all'),
    ...expected.slice(1)],expected),false);
  const post3 = expectedFigureLinks(3,{ family:'primary',
    assetBase:'/assets/images/tesis-post3/scientific-reset' },
  'post3-grade_progression_or_lag-historical','es','light');
  assert.equal(post3[0],'/assets/images/tesis-post3/scientific-reset/'
    + 'post3-grade_progression_or_lag-historical.csv');
  assert.equal(figureLinksComplete(post3,post3),true);
});

test('legacy live gates cannot return a green release verdict', () => {
  const series = run(script, ['--artifact-root', '/tmp']);
  assert.equal(series.status, 2);
  assert.match(series.data.error, /reset-manifest is required/);
  const svg = run(visual, []);
  assert.equal(svg.status, 2);
  assert.match(svg.data.error, /reset-manifest is required/);
});
