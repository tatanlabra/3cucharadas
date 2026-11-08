#!/usr/bin/env node

// Browser contract for the article and its separate methods annex. The Ruby gates
// protect scientific content; this gate binds the rendered routes to a fresh build
// and checks that readers can actually reach and use both pages.
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(scriptDir, '..');
const prefix = '/datos/educacion/politica-publica/';
const configs = {
  3: {
    slug: 'costos-cierre-escolar-trayectorias',
    post: '_posts/2026-10-23-costos-cierre-escolar-trayectorias',
    annex: '_pages/tesis-post3-anexo-metodologico',
    current: 3
  },
  4: {
    slug: 'cierre-escolar-educacion-superior-causal-ml',
    post: '_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml',
    annex: '_pages/tesis-post4-anexo-metodologico',
    current: 4
  }
};
const viewports = [
  { width: 320, height: 800 },
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 1024, height: 900 },
  { width: 1440, height: 1000 }
];
const themes = ['light', 'academic-night'];
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const option = (args, flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};
const options = (args, flag) => args.flatMap((arg, index) =>
  arg === flag && args[index + 1] ? [args[index + 1]] : []);
const bounded = async (promise, milliseconds, label) => {
  let timer;
  try {
    return await Promise.race([promise, new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(label)), milliseconds);
    })]);
  } finally { clearTimeout(timer); }
};
const sourcePath = (config, locale, kind) => resolve(siteRoot,
  `${kind === 'article' ? config.post : config.annex}${locale === 'en' ? '-en' : ''}.md`);
const route = (config, locale, kind) =>
  `${locale === 'en' ? '/en' : ''}${prefix}${config.slug}/${kind === 'annex' ? 'anexo-metodologico/' : ''}`;
function normalizeObservedCloudflareHtml(served) {
  let decodedEmails = 0;
  let html = served.replace(/href="\/cdn-cgi\/l\/email-protection#([0-9a-f]{4,})"/gi, (match, hex) => {
    if (hex.length % 2) return match;
    const bytes = Buffer.from(hex, 'hex');
    const address = [...bytes.subarray(1)].map((byte) => String.fromCharCode(byte ^ bytes[0])).join('');
    if (!/^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']+$/.test(address)) return match;
    decodedEmails += 1;
    return `href="mailto:${address}"`;
  });
  const decodeScript = '<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>';
  const decodeScripts = html.split(decodeScript).length - 1;
  if (decodeScripts === 1) html = html.replace(decodeScript, '');
  const beaconTag = /<script type="module" src="https:\/\/static\.cloudflareinsights\.com\/beacon\.min\.js\/[a-z0-9]+" integrity="sha512-[A-Za-z0-9+/=]+" data-cf-beacon='[^']+' crossorigin="anonymous"><\/script>/g;
  const beacons = (html.match(beaconTag) || []).length;
  if (beacons === 1) html = html.replace(/<script type="module" src="https:\/\/static\.cloudflareinsights\.com\/beacon\.min\.js\/[a-z0-9]+" integrity="sha512-[A-Za-z0-9+/=]+" data-cf-beacon='[^']+' crossorigin="anonymous"><\/script>\r?\n(?=<\/body>)/, '');
  return { html, safe: decodeScripts <= 1 && beacons <= 1,
    transformations: { decodedEmails, decodeScripts, beacons } };
}

function evaluate(row) {
  const errors = [];
  if (row.httpStatus !== 200 || !row.artifactBound || !row.sourceFresh || !row.sourceMarkerBound)
    errors.push('route-artifact-binding');
  if (!row.titleMatches || !row.structureValid) errors.push('reading-structure');
  if (!row.navValid || !row.ivLinkPresent) errors.push('series-navigation');
  if (row.referenceCount === 0) errors.push('missing-references');
  if (row.documentOverflow) errors.push('document-overflow');
  if (row.bodyFontPx < 16 || (row.tableCount && row.tableMinFontPx < 13)
    || (row.referenceCount && row.referenceMinFontPx < 14)) errors.push('text-size');
  if (row.figureCount !== row.expectedFigures || !row.figuresValid) errors.push('figure-contract');
  if (!row.figureSemanticValid) errors.push('figure-semantic-contract');
  if (!row.figureThemeValid) errors.push('figure-theme-contract');
  if (!row.visualIdentityValid) errors.push('visual-identity-contract');
  if (!row.dataFallbackValid) errors.push('figure-data-fallback');
  if (!row.keyboardFocusValid) errors.push('figure-keyboard-focus');
  if (row.figureCount && row.svgTextMinPx < 9) errors.push('svg-text-too-small');
  if (!row.tableWrappersValid || !row.tableHeadersScoped || !row.tableContractValid) errors.push('table-contract');
  if (!row.idsUnique || !row.imagesNamed) errors.push('basic-a11y');
  if (!row.publicContentSafe) errors.push('public-content-safety');
  if (!row.themeSurfaceValid) errors.push('theme-surface');
  if (!row.editorialGeometryValid) errors.push('editorial-width-mismatch');
  if (!row.paragraphJustificationValid) errors.push('paragraph-justification');
  if (!row.figureOneWidthValid) errors.push('figure-one-width');
  if (!row.darkPanelToneValid) errors.push('dark-panel-tone-mismatch');
  if (row.criticalErrors.length) errors.push('critical-resource-or-console-error');
  return errors;
}

function runFixture(name) {
  const baseline = {
    httpStatus: 200, artifactBound: true, sourceFresh: true, sourceMarkerBound: true, titleMatches: true,
    structureValid: true, navValid: true, ivLinkPresent: true,
    documentOverflow: false, bodyFontPx: 18, tableCount: 1, tableMinFontPx: 14,
    referenceCount: 1, referenceMinFontPx: 15, expectedFigures: 2, figureCount: 2,
    figuresValid: true, figureSemanticValid: true, figureThemeValid: true, visualIdentityValid: true,
    dataFallbackValid: true, keyboardFocusValid: true, svgTextMinPx: 10,
    tableWrappersValid: true, tableHeadersScoped: true, tableContractValid: true,
    idsUnique: true, imagesNamed: true, publicContentSafe: true,
    themeSurfaceValid: true, editorialGeometryValid: true, paragraphJustificationValid: true,
    figureOneWidthValid: true,
    darkPanelToneValid: true,
    criticalErrors: []
  };
  const mutations = {
    overflow: { documentOverflow: true },
    'missing-figure': { figureCount: 1 },
    'wrong-figure-limit': { figureSemanticValid: false },
    'wrong-theme': { figureThemeValid: false },
    'zero-size': { figuresValid: false },
    'private-content': { publicContentSafe: false },
    'missing-table': { tableContractValid: false },
    'missing-visual-identity': { visualIdentityValid: false },
    'mismatched-editorial-width': { editorialGeometryValid: false },
    'unjustified-paragraph': { paragraphJustificationValid: false },
    'narrow-figure': { figureOneWidthValid: false },
    'off-theme-panel': { darkPanelToneValid: false },
    'missing-he-agenda': { ivLinkPresent: false },
    'he-blocker': { publicContentSafe: false },
    'missing-footnote': { referenceCount: 0 },
    'missing-annex': { httpStatus: 404 },
    'missing-series-link': { navValid: false },
    'stale-build': { sourceFresh: false }
  };
  if (!Object.hasOwn(mutations, name)) {
    console.error(JSON.stringify({ status: 'ERROR', fixture: name, error: 'unknown fixture' }));
    process.exitCode = 2;
    return;
  }
  const failures = evaluate({ ...baseline, ...mutations[name] });
  const expected = {
    overflow: 'document-overflow', 'missing-figure': 'figure-contract',
    'wrong-figure-limit': 'figure-semantic-contract',
    'wrong-theme': 'figure-theme-contract', 'zero-size': 'figure-contract',
    'private-content': 'public-content-safety', 'missing-table': 'table-contract',
    'missing-visual-identity': 'visual-identity-contract',
    'mismatched-editorial-width': 'editorial-width-mismatch',
    'unjustified-paragraph': 'paragraph-justification',
    'narrow-figure': 'figure-one-width',
    'off-theme-panel': 'dark-panel-tone-mismatch',
    'missing-he-agenda': 'series-navigation', 'he-blocker': 'public-content-safety',
    'missing-footnote': 'missing-references', 'missing-annex': 'route-artifact-binding',
    'missing-series-link': 'series-navigation', 'stale-build': 'route-artifact-binding'
  }[name];
  const exact = failures.length === 1 && failures[0] === expected;
  console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture: name, failures, expected }));
  process.exitCode = exact ? 1 : 2;
}

function parseResetCsv(contents) {
  const records = [];
  let row = [], field = '', quoted = false;
  for (let i = 0; i < contents.length; i += 1) {
    const char = contents[i];
    if (quoted && char === '"' && contents[i + 1] === '"') { field += '"'; i += 1; }
    else if (char === '"') quoted = !quoted;
    else if (char === ',' && !quoted) { row.push(field); field = ''; }
    else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && contents[i + 1] === '\n') i += 1;
      row.push(field); field = '';
      if (row.some((cell) => cell !== '')) records.push(row);
      row = [];
    } else field += char;
  }
  if (quoted) throw new Error('unterminated CSV quote');
  if (field || row.length) { row.push(field); records.push(row); }
  if (!records.length || records[0].length === 0) throw new Error('empty CSV');
  const header = records.shift();
  if (new Set(header).size !== header.length || records.some((cells) => cells.length !== header.length))
    throw new Error('invalid CSV width or duplicate column');
  return records.map((cells) => Object.fromEntries(header.map((key, index) => [key, cells[index]])));
}

const sensitivityStems = { did: 'post3-sensitivity-did', bounds: 'post3-sensitivity-bounds',
  d1_d2: 'post3-sensitivity-d1-d2' };
const resetStem = (number, figure, family = 'primary') => family === 'anticipation'
  ? `post3-anticipation-${figure.outcome}-${figure.era}`
  : family === 'sensitivity' ? number === 4
    ? `post4-sensitivity-${figure.kind}-${figure.era}` : sensitivityStems[figure.kind]
    : number === 3 ? `post3-${figure.outcome}-${figure.era}` : `post4-${figure.kind}-${figure.era}`;
const resetCaption = (figure, locale) => figure.caption?.[locale] || figure[`caption_${locale}`];
const normalizeText = (value) => String(value || '').replace(/\s+/g, ' ').trim();
const resetKey = (row) => [row.outcome, row.era, row.cohort_year || row.cohort || '',
  row.cohort_range || '', row.estimand, row.estimation_status].join('|');
const anticipationKey = (row) => [row.outcome, row.era, row.cohort_year, row.arm].join('|');
const anticipationStatuses = ['OBSERVED', 'PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY',
  'PRIVACY_SUPPRESSED_SMALL_SCHOOL_GROUP', 'NOT_ESTIMABLE_PANEL_BOUNDARY'];
const anticipationColumns = ['outcome', 'era', 'cohort_year', 'baseline_year',
  'transition_year', 'arm', 'n', 'schools', 'rate_pp', 'display_status', 'reason_es', 'reason_en'];
const csvValue = (value, column) => value == null ? ''
  : column === 'rate_pp' ? Number(value).toFixed(1) : String(value);
const sensitivityCellEqual = (cell, value) => value == null ? cell === ''
  : typeof value === 'boolean' ? cell === (value ? 'True' : 'False')
    : typeof value === 'number' ? cell !== '' && Number.isFinite(Number(cell))
      && Number(cell) === value : cell === value;
const ivCellEqual = (cell, value) => {
  if (Array.isArray(value) || value && typeof value === 'object') {
    try { return JSON.stringify(JSON.parse(cell)) === JSON.stringify(value); }
    catch { return false; }
  }
  return sensitivityCellEqual(cell,value);
};
const sensitivityKey = (row) => [row.outcome, row.era, row.contrast || ''].join('|');
const ivComparisonVariants = ['primary','stable_attributes','other_commune',
  'common_grade_year_support','age_gender_treated_post_standardized',
  'never_plus_future_school_exposure','never_plus_future_outcome',
  'future_only_school_exposure','future_only_outcome',
  'school_student_two_way_variance','fixed_effects_diagnostic'];
const ivCalendarVariants = ['pretrend_placebo_late','late_strict_pre',
  'pretrend_placebo_early','early_strict_pre'];

const ivPublicPooledAccess = (row) => row.outcome === 'any_he_2yr'
  && ['historical', 'modern'].includes(row.era)
  && (row.cohort == null || row.cohort === '')
  && (row.variant == null || row.variant === '' || row.variant === 'primary');
const ivPrivatePersonField = (key) => /^(?:n|n_treated|n_control|rates|rate_pp|rate_pct|arm_rate|(?:treated|control)_(?:pre|post)|(?:student|person|learner).*(?:rows|count|clusters)|.*student_cohort_rows|retained_future_student_cohort_rows)$/i.test(key);
const ivFilled = (value) => value != null && value !== '' && value !== 'null';
const ivTableRows = (markup) => {
  const body = markup.match(/<tbody>([\s\S]*?)<\/tbody>/i)?.[1] || '';
  return [...body.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi)].map((match) =>
    [...match[1].matchAll(/<(?:td|th)\b[^>]*>([\s\S]*?)<\/(?:td|th)>/gi)]
      .map((cell) => cell[1].replace(/<[^>]+>/g,'').replace(/&nbsp;/g,' ').trim()));
};
const ivTableDecimal = (cell, locale, percent = false) => {
  const decimal = locale === 'es' ? ',' : '\\.';
  const pattern = new RegExp(`^[+−-]?\\d+(?:${decimal}\\d+)?${percent ? '\\s*%' : ''}$`);
  const raw = String(cell ?? '').trim();
  if (!pattern.test(raw)) return NaN;
  const value = Number(raw.replace(/−/g,'-').replace(/,/g,'.').replace(/\s*%$/,''));
  return Number.isFinite(value) ? value : NaN;
};
const ivTableInterval = (cell, locale) => {
  const decimal = locale === 'es' ? ',' : '\\.';
  const number = `[+−-]?\\d+(?:${decimal}\\d+)?`;
  const match = String(cell ?? '').trim().match(new RegExp(`^\\[\\s*(${number})\\s*,\\s*(${number})\\s*\\]$`));
  return match ? [ivTableDecimal(match[1],locale),ivTableDecimal(match[2],locale)] : [];
};
const ivTableCount = (cell, locale) => {
  const separator = locale === 'es' ? '\\.' : ',';
  const pattern = new RegExp(`^(?:0|[1-9]\\d*|[1-9]\\d{0,2}(?:${separator}\\d{3})+)$`);
  const raw = String(cell ?? '').trim();
  if (!pattern.test(raw)) return NaN;
  const value = Number(raw.replace(locale === 'es' ? /\./g : /,/g,''));
  return Number.isSafeInteger(value) ? value : NaN;
};
function locateArtifactManifest(artifactRoot, number, digest) {
  if (!artifactRoot) return { path: null, base: null, matches: 0 };
  const top = resolve(artifactRoot, `assets/images/tesis-post${number}`);
  if (!existsSync(top)) return { path: null, base: null, matches: 0 };
  const matches = [], pending = [{ folder: top, depth: 0 }];
  while (pending.length) {
    const { folder, depth } = pending.pop();
    for (const entry of readdirSync(folder,{ withFileTypes:true })) {
      const path = resolve(folder,entry.name);
      if (entry.isDirectory() && depth < 4) pending.push({ folder:path, depth:depth+1 });
      else if (entry.isFile() && entry.name === 'manifest.json'
        && sha256(readFileSync(path)) === digest) matches.push(path);
    }
  }
  if (matches.length !== 1) return { path:null, base:null, matches:matches.length };
  return { path:matches[0],base:`/${relative(artifactRoot,dirname(matches[0])).split(sep).join('/')}`,
    matches:1 };
}

function auditIvPublicSurface(manifest, folder, family, failures) {
  const primaryFamily = ['primary','post4_primary_projected'].includes(family);
  const figureRows = manifest.figures?.flatMap((figure) => figure.source_rows || []) || [];
  const check = (row, where) => {
    const allowed = primaryFamily && ivPublicPooledAccess(row);
    for (const [key, value] of Object.entries(row)) {
      if (!ivPrivatePersonField(key) || !ivFilled(value)) continue;
      if (!allowed || !['n_treated','n_control','rates'].includes(key))
        failures.push(`iv-public-person-field:${where}:${key}`);
    }
    if (!primaryFamily && Object.keys(row).some(ivPrivatePersonField))
      failures.push(`iv-sensitivity-person-column:${where}`);
  };
  for (const row of figureRows) check(row, 'manifest');
  const csvNames = (manifest.files || []).map((item) => item.name).filter((name) => name.endsWith('.csv'));
  for (const name of csvNames) {
    let rows;
    try { rows = parseResetCsv(readFileSync(resolve(folder, name), 'utf8')); }
    catch { failures.push(`iv-public-csv-invalid:${name}`); continue; }
    if (!primaryFamily && rows.some((row) => Object.keys(row).some(ivPrivatePersonField)))
      failures.push(`iv-sensitivity-person-column:${name}`);
    for (const row of rows) check(row, name);
    if (primaryFamily && name === 'results-all.csv') {
      const exposed = rows.filter((row) => ['n_treated','n_control','rates']
        .some((key) => ivFilled(row[key])));
      if (exposed.length !== 2 || new Set(exposed.map((row) => row.era)).size !== 2
        || exposed.some((row) => !ivPublicPooledAccess(row)
          || !['n_treated','n_control','rates'].every((key) => ivFilled(row[key]))))
        failures.push('iv-public-two-pooled-rates-only');
    }
  }
  for (const name of (manifest.files || []).map((item) => item.name).filter((item) =>
    /\.(?:svg|html)$/.test(item))) {
    if (!existsSync(resolve(folder,name))) {
      failures.push(`iv-public-text-file-missing:${name}`); continue;
    }
    const value = readFileSync(resolve(folder, name), 'utf8');
    if (/\b(?:n_treated|n_control|treated_post|control_post|treated_pre|control_pre)\b|\bN\s*[=:]\s*\d|(?:student|student.cohort|alumno.cohorte)\s*(?:rows|filas)\s*[=:]\s*\d/i.test(value)
      || !primaryFamily && /\b(?:rate|tasa)\s*[=:]\s*[-+]?\d/i.test(value))
      failures.push(`iv-public-text-person-field:${name}`);
  }
}

function auditIvSensitivityRows(manifest, folder, failures, projectedPath) {
  const figures = manifest.figures || [];
  const identity = figures.map((figure) => `${figure.kind}|${figure.era}`);
  if (figures.length !== 4 || new Set(identity).size !== 4
    || ['comparison','calendar'].some((kind) => ['historical','modern'].some((era) =>
      !identity.includes(`${kind}|${era}`)))) failures.push('iv-sensitivity-figure-inventory');
  const projectedHash = manifest.source_sha256;
  if (!/^[a-f0-9]{64}$/.test(projectedHash || '')) failures.push('iv-sensitivity-projection-contract');
  const bundledPath = resolve(folder, manifest.source_file || '');
  const bundledBound = manifest.source_file === 'public-combined-projection.json'
    && existsSync(bundledPath) && sha256(readFileSync(bundledPath)) === projectedHash;
  const externalBound = !projectedPath || existsSync(projectedPath)
    && sha256(readFileSync(projectedPath)) === projectedHash;
  const sourceBound = Boolean(bundledBound && externalBound);
  if (!sourceBound) failures.push('iv-sensitivity-projection-hash');
  let projected = null;
  if (sourceBound) {
    try { projected = JSON.parse(readFileSync(bundledPath, 'utf8')); }
    catch { failures.push('iv-sensitivity-projection-json'); }
    if (projected && (projected.status !== 'PUBLIC_POST4_DESCRIPTIVE_PROJECTION'
      || projected.results?.length !== 2075 || projected.coverage?.length !== 5040))
      failures.push('iv-sensitivity-projection-inventory');
    if (projected?.results) {
      const exposed = projected.results.filter((row) =>
        ['rates','n_treated','n_control'].some((key) => ivFilled(row[key])));
      if (exposed.length !== 2 || new Set(exposed.map((row) => row.era)).size !== 2
        || exposed.some((row) => !ivPublicPooledAccess(row)
          || !['rates','n_treated','n_control'].every((key) => ivFilled(row[key]))))
        failures.push('iv-sensitivity-projection-privacy');
    }
  }
  const csvByKind = {};
  for (const [kind, count] of [['comparison',22],['calendar',8]]) {
    const name = `post4-sensitivity-${kind}-all.csv`;
    try { csvByKind[kind] = parseResetCsv(readFileSync(resolve(folder, name), 'utf8')); }
    catch { csvByKind[kind] = []; failures.push(`iv-sensitivity-csv-invalid:${name}`); }
    if (csvByKind[kind].length !== count) failures.push(`iv-sensitivity-csv-count:${name}`);
  }
  let matrix = [];
  try { matrix = parseResetCsv(readFileSync(resolve(folder,
    'post4-sensitivity-calendar-window-matrix.csv'), 'utf8')); }
  catch { failures.push('iv-sensitivity-calendar-matrix-invalid'); }
  if (matrix.length !== 18 || new Set(matrix.map((row) =>
    `${row.outcome}|${row.grade}|${row.comparison}`)).size !== 18)
    failures.push('iv-sensitivity-calendar-matrix-count');
  if (projected?.temporal_window_metadata?.length === 144) for (const row of matrix) {
    const pair = ['older','newer'].map((slot) => projected.temporal_window_metadata.filter((item) =>
      item.outcome === row.outcome && String(item.grade) === row.grade
      && item.comparison === row.comparison && item.slot === slot));
    if (pair.some((items) => items.length !== 1)) {
      failures.push('iv-sensitivity-calendar-matrix-source'); continue;
    }
    const older = pair[0][0].window_end_rel_G, newer = pair[1][0].window_end_rel_G;
    if (!ivCellEqual(row.older_end_rel_G,older) || !ivCellEqual(row.newer_end_rel_G,newer)
      || !ivCellEqual(row.both_windows_end_before_G,older < 0 && newer < 0)
      || !ivCellEqual(row.only_older_window_ends_before_G,older < 0 && newer >= 0)
      || !ivCellEqual(row.strict_pre_included_by_calendar,older < 0 && newer < 0))
      failures.push('iv-sensitivity-calendar-matrix-source');
  }
  for (const figure of figures) {
    const variants = figure.kind === 'comparison' ? ivComparisonVariants : ivCalendarVariants;
    const rows = figure.source_rows || [];
    if (!['comparison','calendar'].includes(figure.kind)
      || !['historical','modern'].includes(figure.era)
      || figure.stem !== resetStem(4,figure,'sensitivity')
      || figure.csv_file !== `post4-sensitivity-${figure.kind}-all.csv`
      || rows.length !== variants.length
      || rows.some((row,index) => row.variant !== variants[index]
        || row.outcome !== 'any_he_2yr' || row.era !== figure.era
        || !Number.isFinite(row.estimate_pp) || !Number.isFinite(row.ci_low_pp)
        || !Number.isFinite(row.ci_high_pp) || row.ci_low_pp > row.estimate_pp
        || row.estimate_pp > row.ci_high_pp
        || row.confidence_level !== (row.variant === 'fixed_effects_diagnostic' ? 0.95 : 0.975)
        || row.estimation_status !== 'ESTIMABLE_DESCRIPTIVE'
        || row.identification_status !== (row.variant === 'school_student_two_way_variance'
          ? 'DESCRIPTIVE_PRECISION_SENSITIVITY_ONLY' : 'DESCRIPTIVE_ONLY')
        || !Number.isInteger(row.cohort_start) || !Number.isInteger(row.cohort_end)
        || row.cohort_start > row.cohort_end)
      || !(Number.isFinite(figure.axis_bound_pp) && figure.axis_bound_pp > 0))
      failures.push(`iv-sensitivity-figure-contract:${figure.stem}`);
    for (const row of rows) {
      const csv = csvByKind[figure.kind]?.filter((item) => item.variant === row.variant
        && item.outcome === row.outcome && item.era === row.era) || [];
      if (csv.length !== 1 || Object.keys(csv[0]).length !== Object.keys(row).length
        || Object.entries(row).some(([key,value]) => !Object.hasOwn(csv[0],key)
          || !ivCellEqual(csv[0][key],value)))
        failures.push(`iv-sensitivity-figure-csv:${figure.stem}:${row.variant}`);
      const source = projected?.results?.filter((item) => item.variant === row.variant
        && item.outcome === row.outcome && item.era === row.era && item.cohort == null) || [];
      const sourcePeriod = source[0]?.cohort_range
        ?? (row.period_inherited_from_primary ? projected?.results?.find((item) =>
          item.variant === 'primary' && item.outcome === row.outcome
          && item.era === row.era && item.cohort == null)?.cohort_range : null);
      if (projected && (source.length !== 1 || ['estimate_pp','ci_low_pp','ci_high_pp',
        'confidence_level','estimand','estimation_status','identification_status',
        'limitation','treated_schools','control_schools','flags'].some((key) =>
          key in row && JSON.stringify(source[0]?.[key]) !== JSON.stringify(row[key]))
        || JSON.stringify(sourcePeriod) !== JSON.stringify([
          row.cohort_start,row.cohort_end])))
        failures.push(`iv-sensitivity-projection-values:${figure.stem}:${row.variant}`);
    }
    for (const locale of ['es','en']) if (!normalizeText(resetCaption(figure,locale))
      || !normalizeText(figure.alt?.[locale]) || !normalizeText(figure.source_citation?.[locale]))
      failures.push(`iv-sensitivity-language:${figure.stem}:${locale}`);
  }
  for (const kind of ['comparison','calendar']) for (const locale of ['es','en']) {
    const name = `post4-sensitivity-${kind}-table-${locale}.html`;
    let tableRows = [];
    try { tableRows = ivTableRows(readFileSync(resolve(folder,name),'utf8')); }
    catch { failures.push(`iv-sensitivity-table-invalid:${name}`); continue; }
    const expectedRows = figures.filter((figure) => figure.kind === kind)
      .flatMap((figure) => figure.source_rows);
    if (tableRows.length !== expectedRows.length) {
      failures.push(`iv-sensitivity-table-count:${name}`); continue;
    }
    for (const [index, expected] of expectedRows.entries()) {
      const cells = tableRows[index], interval = ivTableInterval(cells?.[4],locale);
      const point = ivTableDecimal(cells?.[3],locale);
      const level = ivTableDecimal(cells?.[5],locale,true);
      const treatedSchools = ivTableCount(cells?.[6],locale);
      const controlSchools = ivTableCount(cells?.[7],locale);
      if (cells.length !== 9 || cells[2] !== `${expected.cohort_start}–${expected.cohort_end}`
        || !Number.isFinite(point) || Math.abs(point-expected.estimate_pp) > 0.051
        || interval.length !== 2 || interval.some((value) => !Number.isFinite(value))
        || Math.abs(interval[0]-expected.ci_low_pp) > 0.051
        || Math.abs(interval[1]-expected.ci_high_pp) > 0.051
        || !Number.isFinite(level) || Math.abs(level-100*expected.confidence_level) > 0.051
        || !Number.isFinite(treatedSchools) || treatedSchools !== expected.treated_schools
        || !Number.isFinite(controlSchools) || controlSchools !== expected.control_schools)
        failures.push(`iv-sensitivity-table-values:${name}:${index}`);
    }
  }
  return { csvRows: 48, sourceBound, sourceRows: projected?.results?.length || null };
}

export function expectedFigureLinks(number, contract, stem, locale, theme) {
  if (!contract.assetBase) return null;
  const csvName = number === 4 && contract.family === 'sensitivity'
    ? contract.csv_file : `${stem}.csv`;
  if (!csvName || !/^[a-z0-9_-]+\.csv$/.test(csvName)) return null;
  return [
    `${contract.assetBase}/${csvName}`,
    `${contract.assetBase}/${stem}-${locale}-${theme}-desktop.svg`,
    `${contract.assetBase}/${stem}-${locale}-${theme}-desktop.png`
  ];
}

export function figureLinksComplete(links, expected) {
  return Array.isArray(expected) && expected.every((path) => links.includes(path));
}

export function resetGateVerdict(number, publicReady, privateSourceBound) {
  if (!publicReady) return { status: 'FAIL', exitCode: 1 };
  if (number === 3 && privateSourceBound !== true)
    return { status: 'PASS_PUBLIC_SCOPE', exitCode: 0 };
  return { status: 'PASS', exitCode: 0 };
}

function auditSensitivityRows(manifest, folder, mutation, failures, sourcePath, privateSourcePath = null) {
  const specs = { did: { rows: 4 }, bounds: { rows: 4 }, d1_d2: { rows: 10 } };
  const figures = manifest.figures || [];
  const kinds = figures.map((figure) => figure.kind);
  if (figures.length !== 3 || new Set(kinds).size !== 3
    || Object.keys(specs).some((kind) => !kinds.includes(kind)))
    failures.push('sensitivity-figure-inventory');
  if (manifest.all_source_rows !== 49 || !/^[a-f0-9]{64}$/.test(manifest.source_sha256 || ''))
    failures.push('sensitivity-source-contract');
  const unitKeys = {
    did: ['estimate_pp','school_ci_low_pp','school_ci_high_pp','two_way_ci_low_pp','two_way_ci_high_pp'],
    bounds: ['lower_pp','upper_pp'],
    d1_d2: ['estimate_pp','ci_low_pp','ci_high_pp','main_sample_shift_pp',
      'definition_on_common_sample_shift_pp','alternative_sample_shift_pp',
      'overall_alternative_minus_main_pp']
  };
  if (Object.entries(unitKeys).some(([kind, keys]) => keys.some((key) =>
    manifest.units?.[kind]?.[key] !== 'percentage_points')))
    failures.push('sensitivity-unit-contract');
  const sourceBound = Boolean(sourcePath && existsSync(sourcePath)
    && sha256(readFileSync(sourcePath)) === manifest.source_sha256);
  if (sourcePath && !sourceBound) failures.push('sensitivity-source-hash');
  let aggregate = null;
  if (sourceBound) {
    try { aggregate = JSON.parse(readFileSync(sourcePath, 'utf8')); }
    catch { failures.push('sensitivity-source-json'); }
    if (aggregate?.sensitivities?.length !== 49) failures.push('sensitivity-source-rows');
  }
  // The public projection omits student-dependence coverage because it contains
  // person counts. The two-way confidence limits in the public figure still need
  // an exact local check against the approved private source, without exporting
  // those counts into this receipt or the site.
  let diagnosticAggregate = aggregate;
  let privateSourceBound = null;
  if (aggregate?.projection?.source_sha256) {
    // Public CI has no access to the private source. Its verdict covers public
    // projection, CSV, SVG and geometry; exact two-way limits require local QA.
    diagnosticAggregate = null;
    privateSourceBound = false;
    if (privateSourcePath) {
      privateSourceBound = Boolean(existsSync(privateSourcePath)
        && sha256(readFileSync(privateSourcePath)) === aggregate.projection.source_sha256);
      if (!privateSourceBound) failures.push('sensitivity-private-source-hash');
    }
    if (privateSourceBound) {
      try { diagnosticAggregate = JSON.parse(readFileSync(privateSourcePath, 'utf8')); }
      catch { failures.push('sensitivity-private-source-json'); diagnosticAggregate = null; }
      if (diagnosticAggregate?.sensitivities?.length !== 49)
        failures.push('sensitivity-private-source-rows');
    }
  }
  const sourceRow = (name, outcome, era) => {
    const rows = aggregate?.sensitivities?.filter((row) => row.name === name
      && row.outcome === outcome && row.era === era) || [];
    return rows.length === 1 ? rows[0] : null;
  };
  const diagnosticRow = (name, outcome, era) => {
    const rows = diagnosticAggregate?.sensitivities?.filter((row) => row.name === name
      && row.outcome === outcome && row.era === era) || [];
    return rows.length === 1 ? rows[0] : null;
  };
  let inventory = [], didInventory = [];
  try { inventory = parseResetCsv(readFileSync(resolve(folder, 'sensitivity-inventory-all.csv'), 'utf8')); }
  catch { failures.push('sensitivity-inventory-invalid'); }
  try { didInventory = parseResetCsv(readFileSync(resolve(folder, 'sensitivity-did-all.csv'), 'utf8')); }
  catch { failures.push('sensitivity-did-inventory-invalid'); }
  if (inventory.length !== 49) failures.push('sensitivity-inventory-count');
  if (didInventory.length !== 37) failures.push('sensitivity-did-inventory-count');
  if (aggregate?.sensitivities?.length === 49) {
    const keys = aggregate.sensitivities.map((row) => [row.name, row.outcome || row.metric || '',
      row.era || ''].join('|'));
    const csvKeys = inventory.map((row) => [row.name, row.outcome || row.metric || '',
      row.era || ''].join('|'));
    if (new Set(csvKeys).size !== 49 || keys.some((key) => !csvKeys.includes(key)))
      failures.push('sensitivity-inventory-source-identity');
    const expectedDid = aggregate.sensitivities.filter((row) => row.name === 'symmetric_repeated_cohort_did')
      .flatMap((row) => row.results.map((result) => [result.outcome, result.era,
        result.cohort_year == null ? '' : String(result.cohort_year)].join('|')));
    const actualDid = didInventory.map((row) => [row.outcome, row.era,
      row.cohort_year || ''].join('|'));
    if (expectedDid.length !== 37 || new Set(actualDid).size !== 37
      || expectedDid.some((key) => !actualDid.includes(key)))
      failures.push('sensitivity-did-inventory-source-identity');
    for (const row of inventory) {
      const src = aggregate.sensitivities.find((item) => item.name === row.name
        && (item.outcome || '') === row.outcome && (item.metric || '') === row.metric
        && (item.era || '') === row.era);
      if (!src || src.status !== row.status) failures.push('sensitivity-inventory-source-status');
    }
    for (const row of didInventory) {
      const src = aggregate.sensitivities.find((item) => item.name === 'symmetric_repeated_cohort_did'
        && item.outcome === row.outcome && item.era === row.era);
      const diagnostic = diagnosticRow('symmetric_repeated_cohort_did', row.outcome, row.era);
      const pooled = src?.results?.find((item) => String(item.cohort_year ?? '') === row.cohort_year);
      const diagnosticPooled = diagnostic?.results?.find((item) =>
        String(item.cohort_year ?? '') === row.cohort_year);
      const twoWay = diagnostic?.coverage?.student_dependence?.find((item) =>
        String(item.cohort_year ?? '') === row.cohort_year);
      if (!pooled || !sensitivityCellEqual(row.estimate_pp, pooled.estimate_pp)
        || !sensitivityCellEqual(row.school_ci_low_pp, pooled.ci_low_pp)
        || !sensitivityCellEqual(row.school_ci_high_pp, pooled.ci_high_pp)
        || (privateSourceBound && (!diagnosticPooled || !twoWay
          || !sensitivityCellEqual(pooled.estimate_pp, diagnosticPooled.estimate_pp)
          || !sensitivityCellEqual(pooled.ci_low_pp, diagnosticPooled.ci_low_pp)
          || !sensitivityCellEqual(pooled.ci_high_pp, diagnosticPooled.ci_high_pp)
          || !sensitivityCellEqual(row.two_way_ci_low_pp, twoWay.ci_low_pp)
          || !sensitivityCellEqual(row.two_way_ci_high_pp, twoWay.ci_high_pp)
          || row.two_way_status !== twoWay.status)))
        failures.push('sensitivity-did-inventory-source-values');
    }
  }
  let csvRows = 0;
  for (const figure of figures) {
    const { kind, stem, source_rows: expected } = figure;
    if (!specs[kind] || stem !== sensitivityStems[kind] || figure.family !== 'sensitivity'
      || !Number.isFinite(figure.axis_bound_pp) || figure.axis_bound_pp <= 0)
      failures.push(`sensitivity-figure-contract:${stem}`);
    const intervalTypes = { did: 'two_nominal_95pct_methods', bounds: 'partial_identification_not_ci',
      d1_d2: 'nominal_98_75pct_full_d2_otherwise_95pct' };
    if (figure.interval_type !== intervalTypes[kind]
      || unitKeys[kind]?.some((key) => figure.units?.[key] !== 'percentage_points'))
      failures.push(`sensitivity-figure-units:${stem}`);
    let rows = [];
    try { rows = parseResetCsv(readFileSync(resolve(folder, `${stem}.csv`), 'utf8')); }
    catch { failures.push(`sensitivity-figure-csv-invalid:${stem}`); continue; }
    if (mutation?.stem === stem && rows[mutation.index ?? 0])
      rows[mutation.index ?? 0][mutation.column] = mutation.value;
    csvRows += rows.length;
    if (rows.length !== specs[kind]?.rows || expected?.length !== specs[kind]?.rows)
      failures.push(`sensitivity-figure-row-count:${stem}`);
    const keys = rows.map(sensitivityKey);
    if (new Set(keys).size !== rows.length) failures.push(`sensitivity-figure-duplicate:${stem}`);
    for (let index = 0; index < rows.length; index += 1) {
      const row = rows[index], exp = expected?.[index];
      const columns = [...new Set((expected || []).flatMap((item) => Object.keys(item)))];
      if (!exp || Object.keys(row).length !== columns.length
        || columns.some((column) => !Object.hasOwn(row, column)
          || !sensitivityCellEqual(row[column], exp[column]))) {
        failures.push(`sensitivity-figure-manifest:${stem}:${index}`); continue;
      }
      const outcome = exp.outcome, era = exp.era;
      if (!['grade_progression_or_lag', 'persistent_nonenrollment_two_years'].includes(outcome)
        || !['historical', 'modern'].includes(era))
        failures.push(`sensitivity-row-identity:${stem}:${index}`);
      if (kind === 'did') {
        const src = sourceRow('symmetric_repeated_cohort_did', outcome, era);
        const diagnostic = diagnosticRow('symmetric_repeated_cohort_did', outcome, era);
        const pooled = src?.results?.find((item) => item.cohort_year == null);
        const diagnosticPooled = diagnostic?.results?.find((item) => item.cohort_year == null);
        const twoWay = diagnostic?.coverage?.student_dependence?.find((item) => item.cohort_year == null);
        if (exp.status !== 'ESTIMABLE_DESCRIPTIVE' || exp.confidence_level !== 0.95
          || !(exp.school_ci_low_pp <= exp.estimate_pp && exp.estimate_pp <= exp.school_ci_high_pp)
          || !(exp.two_way_ci_low_pp <= exp.estimate_pp && exp.estimate_pp <= exp.two_way_ci_high_pp)
          || exp.two_way_status !== 'TWO_WAY_ASYMPTOTIC_DIAGNOSTIC_WEAK_CLUSTER_PRECISION'
          || (src && (!pooled || exp.estimate_pp !== pooled.estimate_pp
            || exp.school_ci_low_pp !== pooled.ci_low_pp || exp.school_ci_high_pp !== pooled.ci_high_pp
            || exp.cohort_start !== pooled.cohort_range[0] || exp.cohort_end !== pooled.cohort_range[1]
            || (privateSourceBound && (!diagnosticPooled || !twoWay
              || pooled.estimate_pp !== diagnosticPooled.estimate_pp
              || pooled.ci_low_pp !== diagnosticPooled.ci_low_pp
              || pooled.ci_high_pp !== diagnosticPooled.ci_high_pp
              || exp.two_way_ci_low_pp !== twoWay.ci_low_pp
              || exp.two_way_ci_high_pp !== twoWay.ci_high_pp)))))
          failures.push(`sensitivity-did-values:${index}`);
      } else if (kind === 'bounds') {
        const src = sourceRow('fixed_baseline_partial_identification', outcome, era);
        const expectedStart = era === 'historical' ? 2005 : 2016;
        const expectedEnd = era === 'historical' ? 2015
          : outcome === 'grade_progression_or_lag' ? 2024 : 2023;
        if (exp.status !== 'PARTIAL_IDENTIFICATION_DESCRIPTIVE'
          || exp.target_population !== 'fixed_baseline_cells_before_outcome_missingness'
          || exp.directly_comparable_to_primary_point !== false
          || exp.cohort_start !== expectedStart || exp.cohort_end !== expectedEnd
          || !(exp.lower_pp <= exp.upper_pp)
          || (src && (exp.lower_pp !== src.lower_pp || exp.upper_pp !== src.upper_pp
            || exp.bound_interpretation !== src.bound_interpretation)))
          failures.push(`sensitivity-bound-values:${index}`);
      } else if (kind === 'd1_d2') {
        const src = sourceRow('d1_event', outcome, era);
        if (era === 'historical') {
          if (exp.status !== 'NON_DISCRIMINATING_IDENTICAL_EXPOSURE_FLAGS'
            || exp.contrast != null || exp.estimate_pp != null || exp.ci_low_pp != null
            || exp.ci_high_pp != null || exp.cohort_start !== 2005 || exp.cohort_end !== 2015
            || (src && src.status !== exp.status))
            failures.push(`sensitivity-d1-historical:${index}`);
        } else {
          const expectedConfidence = exp.contrast === 'main_full' ? 0.9875 : 0.95;
          const srcResult = src?.results?.[exp.contrast];
          if (!['main_full','main_common','alternative_common','alternative_full'].includes(exp.contrast)
            || exp.status !== 'ESTIMABLE_DESCRIPTIVE' || exp.confidence_level !== expectedConfidence
            || !(exp.ci_low_pp <= exp.estimate_pp && exp.estimate_pp <= exp.ci_high_pp)
            || (src && (!srcResult || exp.estimate_pp !== srcResult.estimate_pp
              || exp.ci_low_pp !== srcResult.ci_low_pp || exp.ci_high_pp !== srcResult.ci_high_pp
              || exp.cohort_start !== srcResult.cohort_range[0]
              || exp.cohort_end !== srcResult.cohort_range[1]
              || exp.main_sample_shift_pp !== src.main_sample_shift_pp
              || exp.definition_on_common_sample_shift_pp !== src.variant_on_common_sample_shift_pp
              || exp.alternative_sample_shift_pp !== src.alternative_sample_shift_pp
              || exp.overall_alternative_minus_main_pp !== src.overall_alternative_minus_main_pp)))
            failures.push(`sensitivity-d1-values:${index}`);
        }
      }
    }
    for (const locale of ['es', 'en']) {
      const caption = normalizeText(resetCaption(figure, locale));
      const alt = normalizeText(figure.alt?.[locale]);
      const citation = normalizeText(figure.source_citation?.[locale]);
      if (!caption || !alt || !citation)
        failures.push(`sensitivity-language-contract:${stem}:${locale}`);
      if (kind === 'bounds' && (locale === 'es'
        ? !/escolarizaci[oó]n real/i.test(`${caption} ${alt}`)
        : !/true non.schooling|actual non.schooling|actual non.enrollment/i.test(`${caption} ${alt}`)))
        failures.push(`sensitivity-true-schooling-label:${stem}:${locale}`);
    }
  }
  if (csvRows !== 18) failures.push('sensitivity-figure-coverage');
  return { csvRows, sourceBound, privateSourceBound,
    sourceRows: aggregate?.sensitivities?.length || null };
}

function auditAnticipationRows(manifest, folder, mutation, failures) {
  const counts = Object.fromEntries(anticipationStatuses.map((key) => [key, 0]));
  const figureStems = (manifest.figures || []).map((figure) => resetStem(3, figure, 'anticipation'));
  const expectedCombos = new Set([
    'grade_progression_or_lag|historical', 'grade_progression_or_lag|modern',
    'persistent_nonenrollment_two_years|historical',
    'persistent_nonenrollment_two_years|modern'
  ]);
  const actualCombos = new Set((manifest.figures || []).map((figure) =>
    `${figure.outcome}|${figure.era}`));
  if (actualCombos.size !== 4 || [...expectedCombos].some((key) => !actualCombos.has(key))
    || manifest.figures?.length !== 4) failures.push('anticipation-figure-inventory');
  if (manifest.rows !== 78) failures.push('anticipation-row-contract');
  let masterRows = [];
  try { masterRows = parseResetCsv(readFileSync(resolve(folder, 'anticipation-all.csv'), 'utf8')); }
  catch { failures.push('anticipation-master-invalid'); }
  if (masterRows.length !== 78) failures.push('anticipation-master-count');
  const master = new Map();
  const armsByCohort = new Map();
  for (const row of masterRows) {
    const key = anticipationKey(row);
    if (master.has(key)) failures.push('anticipation-master-duplicate');
    master.set(key, row);
    const cohortKey = [row.outcome, row.era, row.cohort_year].join('|');
    if (!armsByCohort.has(cohortKey)) armsByCohort.set(cohortKey, new Set());
    armsByCohort.get(cohortKey).add(row.arm);
    if (Object.keys(row).length !== anticipationColumns.length
      || anticipationColumns.some((column) => !Object.hasOwn(row, column)))
      failures.push('anticipation-columns');
    const boundary = row.display_status === 'NOT_ESTIMABLE_PANEL_BOUNDARY';
    if (!['treated', 'control'].includes(row.arm)
      || !/^\d{4}$/.test(row.cohort_year)
      || (boundary && (row.baseline_year !== '' || row.transition_year !== ''))
      || (!boundary && (Number(row.baseline_year) !== Number(row.cohort_year) - 2
        || Number(row.transition_year) !== Number(row.cohort_year) - 1)))
      failures.push(`anticipation-row-identity:${key}`);
    if (!Object.hasOwn(counts, row.display_status)) {
      failures.push(`anticipation-status:${key}`); continue;
    }
    counts[row.display_status] += 1;
    if (row.display_status === 'OBSERVED') {
      if (!/^\d+$/.test(row.n) || !/^\d+$/.test(row.schools)
        || Number(row.n) < 10 || Number(row.schools) < 10
        || row.rate_pp === '' || !Number.isFinite(Number(row.rate_pp))
        || Number(row.rate_pp) < 0 || Number(row.rate_pp) > 100)
        failures.push(`anticipation-observed-value:${key}`);
    } else if (row.n !== '' || row.schools !== '' || row.rate_pp !== ''
      || !normalizeText(row.reason_es) || !normalizeText(row.reason_en)) {
      failures.push(`anticipation-privacy:${key}`);
    }
  }
  if (armsByCohort.size !== 39 || [...armsByCohort.values()].some((arms) =>
    arms.size !== 2 || !arms.has('treated') || !arms.has('control')))
    failures.push('anticipation-arm-pairs');
  if (!manifest.status_counts || anticipationStatuses.some((key) =>
    (manifest.status_counts[key] ?? 0) !== counts[key])
    || Object.keys(manifest.status_counts).some((key) => !anticipationStatuses.includes(key))
    || manifest.observed_rows !== counts.OBSERVED
    || Object.values(counts).reduce((sum, count) => sum + count, 0) !== 78)
    failures.push('anticipation-status-counts');
  let csvRows = 0;
  const seen = new Set();
  for (const figure of manifest.figures || []) {
    const stem = resetStem(3, figure, 'anticipation');
    if (figure.family !== 'anticipation' || figure.stem !== stem
      || figure.axis_min_pct !== 0 || figure.axis_max_pct !== 100)
      failures.push(`anticipation-figure-contract:${stem}`);
    let rows = [];
    try { rows = parseResetCsv(readFileSync(resolve(folder, `${stem}.csv`), 'utf8')); }
    catch { failures.push(`anticipation-figure-csv-invalid:${stem}`); continue; }
    if (mutation?.stem === stem && rows[mutation.index ?? 0])
      rows[mutation.index ?? 0][mutation.column] = mutation.value;
    csvRows += rows.length;
    if (rows.length !== figure.source_rows?.length || rows.length === 0)
      failures.push(`anticipation-figure-csv-count:${stem}`);
    for (let index = 0; index < rows.length; index += 1) {
      const row = rows[index];
      const key = anticipationKey(row);
      if (row.display_status !== 'OBSERVED' && (row.n !== '' || row.schools !== ''
        || row.rate_pp !== '')) failures.push(`anticipation-privacy:${stem}:${index}`);
      if (row.display_status === 'OBSERVED' && (row.rate_pp === ''
        || !Number.isFinite(Number(row.rate_pp)) || Number(row.rate_pp) < 0
        || Number(row.rate_pp) > 100)) failures.push(`anticipation-observed-value:${stem}:${index}`);
      const masterRow = master.get(key);
      const expected = figure.source_rows?.[index];
      if (seen.has(key)) failures.push(`anticipation-figure-duplicate:${stem}:${index}`);
      seen.add(key);
      if (!masterRow || anticipationColumns.some((column) => row[column] !== masterRow[column])
        || Object.keys(row).length !== anticipationColumns.length)
        failures.push(`anticipation-figure-master:${stem}:${index}`);
      if (!expected || Object.keys(expected).length !== anticipationColumns.length
        || anticipationColumns.some((column) => csvValue(expected[column], column) !== row[column]
          || (column === 'rate_pp' && expected[column] != null
            && Math.abs(Number(expected[column]) * 10
              - Math.round(Number(expected[column]) * 10)) > 1e-8)))
        failures.push(`anticipation-figure-manifest:${stem}:${index}`);
      if (row.outcome !== figure.outcome || row.era !== figure.era)
        failures.push(`anticipation-figure-identity:${stem}:${index}`);
    }
    for (const locale of ['es', 'en']) {
      if (!normalizeText(resetCaption(figure, locale)) || !normalizeText(figure.alt?.[locale])
        || !normalizeText(figure.source_citation?.[locale]))
        failures.push(`anticipation-language-contract:${stem}:${locale}`);
    }
  }
  if (seen.size !== masterRows.length || csvRows !== 78)
    failures.push('anticipation-figure-coverage');
  return { csvRows, counts, figureStems };
}

function auditAnticipationSources(manifest, sourceRoot, failures) {
  const sourceFiles = manifest.source_files || [];
  const names = sourceFiles.map((entry) => entry.name);
  if (sourceFiles.length !== 39 || new Set(names).size !== 39
    || sourceFiles.some((entry) => !/^\d{4}_[a-z0-9_]+\.json$/.test(entry.name)
      || !/^[a-f0-9]{64}$/.test(entry.sha256 || ''))
    || !/^[a-f0-9]{64}$/.test(manifest.source_sha256 || '')) {
    failures.push('anticipation-source-inventory');
    return { bound: false, mismatches: names };
  }
  const canonical = [...sourceFiles].sort((a, b) => a.name.localeCompare(b.name))
    .map(({ name, sha256: digest }) => ({ name, sha256: digest }));
  if (sha256(JSON.stringify(canonical)) !== manifest.source_sha256)
    failures.push('anticipation-source-inventory-hash');
  if (!sourceRoot) return { bound: false, mismatches: [] };
  const actualNames = existsSync(sourceRoot)
    ? readdirSync(sourceRoot).filter((name) => name.endsWith('.json')).sort() : [];
  if (actualNames.length !== 39 || actualNames.some((name, index) =>
    name !== [...names].sort()[index])) failures.push('anticipation-source-dir-inventory');
  const mismatches = sourceFiles.filter((entry) => {
    const path = resolve(sourceRoot, entry.name);
    return !existsSync(path) || sha256(readFileSync(path)) !== entry.sha256;
  }).map((entry) => entry.name);
  if (mismatches.length) failures.push('anticipation-source-hash');
  return { bound: mismatches.length === 0
    && !failures.includes('anticipation-source-dir-inventory'), mismatches };
}

function auditResetManifest(number, manifestPath, artifactRoot = null, mutation = null,
  anticipationSourceRoot = null, sensitivitySourcePath = null, sensitivityPrivateSourcePath = null) {
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const manifestSha256 = sha256(readFileSync(manifestPath));
  const family = manifest.family || 'primary';
  const folder = dirname(resolve(manifestPath));
  const names = (manifest.files || []).map((entry) => entry.name);
  const failures = [];
  const artifactLocation = locateArtifactManifest(artifactRoot,number,manifestSha256);
  const assetBase = artifactLocation.base;
  if (!['primary', 'anticipation', 'sensitivity', 'post4_primary_projected'].includes(family)
    || (number === 3 && family === 'post4_primary_projected')
    || (number === 4 && !['primary', 'post4_primary_projected', 'sensitivity'].includes(family))
    || (family === 'sensitivity' && number === 4 && manifest.series !== 'IV')
    || (family === 'sensitivity' && number === 3 && manifest.series === 'IV'))
    failures.push('manifest-family');
  if (!Array.isArray(manifest.figures) || manifest.figures.length === 0
    || !Array.isArray(manifest.files) || manifest.files.length === 0) failures.push('manifest-empty');
  if (new Set(names).size !== names.length || names.some((name) =>
    !/^[a-z0-9_]+(?:-[a-z0-9_]+)*\.(?:csv|svg|png|json|html)$/.test(name))) failures.push('manifest-file-inventory');
  const figureStems = (manifest.figures || []).map((figure) => resetStem(number, figure, family));
  if (new Set(figureStems).size !== figureStems.length) failures.push('manifest-figure-duplicate');
  const expectedVisual = new Set(figureStems.flatMap((stem) => ['es', 'en'].flatMap((lang) =>
    ['light', 'dark'].flatMap((theme) => ['desktop', 'mobile'].flatMap((layout) =>
      ['svg', 'png'].map((format) => `${stem}-${lang}-${theme}-${layout}.${format}`))))));
  const actualVisual = new Set(names.filter((name) => /\.(?:svg|png)$/.test(name)));
  if (expectedVisual.size !== actualVisual.size || [...expectedVisual].some((name) => !actualVisual.has(name)))
    failures.push('manifest-visual-variants');
  if (family === 'anticipation') {
    const expectedFiles = new Set(['anticipation-all.csv', ...figureStems.map((stem) => `${stem}.csv`),
      ...expectedVisual]);
    if (names.length !== expectedFiles.size || names.some((name) => !expectedFiles.has(name)))
      failures.push('anticipation-file-inventory');
  }
  if (family === 'sensitivity' && number === 3) {
    const expectedFiles = new Set(['sensitivity-inventory-all.csv','sensitivity-did-all.csv',
      ...figureStems.map((stem) => `${stem}.csv`), ...expectedVisual]);
    if (names.length !== expectedFiles.size || names.some((name) => !expectedFiles.has(name)))
      failures.push('sensitivity-file-inventory');
  }
  if (family === 'sensitivity' && number === 4) {
    const csvNames = ['post4-sensitivity-comparison-all.csv',
      'post4-sensitivity-calendar-all.csv',
      'post4-sensitivity-calendar-window-matrix.csv','public-combined-projection.json'];
    const htmlNames = names.filter((name) => name.endsWith('.html'));
    const expectedHtml = ['comparison','calendar'].flatMap((kind) => ['es','en']
      .map((lang) => `post4-sensitivity-${kind}-table-${lang}.html`))
      .concat(['es','en'].map((lang) =>
        `post4-sensitivity-calendar-window-matrix-${lang}.html`));
    const expectedFiles = new Set([...csvNames, ...expectedHtml, ...expectedVisual]);
    if (htmlNames.length !== 6 || names.length !== 74
      || names.length !== expectedFiles.size || names.some((name) => !expectedFiles.has(name)))
      failures.push('iv-sensitivity-file-inventory');
  }
  const sourceMismatches = [], artifactMismatches = [];
  for (const entry of manifest.files || []) {
    if (!names.includes(entry.name) || !/^[a-f0-9]{64}$/.test(entry.sha256 || '')) {
      sourceMismatches.push(entry.name); continue;
    }
    const source = resolve(folder, entry.name);
    const sourceBytes = existsSync(source) ? readFileSync(source) : null;
    if (!sourceBytes || sha256(sourceBytes) !== entry.sha256) sourceMismatches.push(entry.name);
    if (artifactRoot && !(family === 'sensitivity' && number === 4 && entry.name.endsWith('.html'))) {
      const artifact = assetBase ? resolve(artifactRoot,assetBase.slice(1),entry.name) : null;
      const artifactBytes = artifact && existsSync(artifact) ? readFileSync(artifact) : null;
      if (!artifactBytes || sha256(artifactBytes) !== entry.sha256) artifactMismatches.push(entry.name);
    }
  }
  if (sourceMismatches.length) failures.push('manifest-source-hash');
  if (artifactMismatches.length) failures.push('manifest-artifact-hash');
  if (number === 4 && manifest.source_file === 'public-combined-projection.json'
    && (manifest.files || []).find((item) => item.name === manifest.source_file)?.sha256
      !== manifest.source_sha256)
    failures.push('iv-public-projection-file-hash');
  const manifestBound = Boolean(artifactRoot && artifactLocation.matches === 1);
  if (artifactRoot && !manifestBound) failures.push('manifest-artifact-binding');
  if (number === 4 && ['primary', 'post4_primary_projected', 'sensitivity'].includes(family))
    auditIvPublicSurface(manifest, folder, family, failures);
  if (family === 'anticipation') {
    const { csvRows, counts } = auditAnticipationRows(manifest, folder, mutation, failures);
    const sources = auditAnticipationSources(manifest, anticipationSourceRoot, failures);
    return { failures: [...new Set(failures)], sourceMismatches, artifactMismatches,
      manifestBound, files: names.length, figures: figureStems.length, csvRows,
      statusCounts: counts, sourceFilesBound: sources.bound,
      sourceFileMismatches: sources.mismatches,
      manifestSha256, manifest, family, assetBase };
  }
  if (family === 'sensitivity' && number === 3) {
    const { csvRows, sourceBound, privateSourceBound, sourceRows } = auditSensitivityRows(
      manifest, folder, mutation, failures, sensitivitySourcePath, sensitivityPrivateSourcePath);
    return { failures: [...new Set(failures)], sourceMismatches, artifactMismatches,
      manifestBound, files: names.length, figures: figureStems.length, csvRows,
      sourceFilesBound: sourceBound, privateSourceBound, sourceRows,
      manifestSha256, manifest, family, assetBase };
  }
  if (family === 'sensitivity' && number === 4) {
    const { csvRows, sourceBound, sourceRows } = auditIvSensitivityRows(manifest, folder,
      failures, sensitivitySourcePath);
    return { failures: [...new Set(failures)], sourceMismatches, artifactMismatches,
      manifestBound, files: names.length, figures: figureStems.length, csvRows,
      sourceFilesBound: sourceBound, sourceRows,
      manifestSha256, manifest, family, assetBase };
  }
  const masterName = 'results-all.csv';
  const masterFile = resolve(folder, masterName);
  let masterRows = [], csvRows = 0;
  try { masterRows = parseResetCsv(readFileSync(masterFile, 'utf8')); }
  catch { failures.push('master-csv-invalid'); }
  const master = new Map(masterRows.map((row) => [resetKey(row), row]));
  if (master.size !== masterRows.length || masterRows.length === 0) failures.push('master-row-identity');
  for (const figure of manifest.figures || []) {
    const stem = resetStem(number, figure);
    const path = resolve(folder, `${stem}.csv`);
    let rows = [];
    try { rows = parseResetCsv(readFileSync(path, 'utf8')); }
    catch { failures.push(`figure-csv-invalid:${stem}`); continue; }
    if (mutation?.stem === stem && rows[0]) rows[0][mutation.column] = mutation.value;
    csvRows += rows.length;
    if (rows.length !== figure.source_rows?.length || rows.length === 0)
      failures.push(`figure-csv-count:${stem}`);
    for (let index = 0; index < rows.length; index += 1) {
      const row = rows[index];
      const expected = figure.source_rows?.[index];
      const masterRow = master.get(resetKey(row));
      if (!masterRow || Object.keys(row).some((key) => masterRow[key] !== row[key])
        || Object.keys(masterRow).some((key) => !Object.hasOwn(row, key) && key !== 'linkage_bounds')) {
        failures.push(`figure-csv-master:${stem}:${index}`);
        continue;
      }
      if (!expected || (expected.outcome && expected.outcome !== row.outcome)
        || (expected.era && expected.era !== row.era)
        || expected.estimand !== row.estimand || expected.estimation_status !== row.estimation_status
        || (expected.identification_status && expected.identification_status !== row.identification_status)
        || (expected.cohort_year != null && String(expected.cohort_year) !== row.cohort_year)
        || (expected.cohort_range && JSON.stringify(expected.cohort_range)
          !== JSON.stringify(JSON.parse(row.cohort_range || 'null')))
        || (expected.estimate_pp != null && Number(expected.estimate_pp) !== Number(row.estimate_pp))
        || (expected.ci_low_pp != null && Number(expected.ci_low_pp) !== Number(row.ci_low_pp))
        || (expected.ci_high_pp != null && Number(expected.ci_high_pp) !== Number(row.ci_high_pp))
        || (expected.n_treated != null && Number(expected.n_treated) !== Number(row.n_treated))
        || (expected.n_control != null && Number(expected.n_control) !== Number(row.n_control))
        || (expected.limitation && expected.limitation !== row.limitation))
        failures.push(`figure-csv-manifest:${stem}:${index}`);
    }
    for (const locale of ['es', 'en']) if (!normalizeText(resetCaption(figure, locale)))
      failures.push(`figure-caption-missing:${stem}:${locale}`);
  }
  return { failures: [...new Set(failures)], sourceMismatches, artifactMismatches,
    manifestBound, files: names.length, figures: figureStems.length, csvRows,
    manifestSha256, manifest, family, assetBase };
}

async function inspectResetPage(browser, number, config, manifests, locale, kind, theme,
  viewport, baseUrl, artifactRoot) {
  const pageRoute = route(config, locale, kind);
  const source = sourcePath(config, locale, kind);
  const artifact = resolve(artifactRoot, pageRoute.replace(/^\//, ''), 'index.html');
  const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
  await context.addInitScript((mode) => localStorage.setItem('3cucharadas-theme', mode), theme);
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(`pageerror:${error.message}`));
  page.on('requestfailed', (request) => {
    if (request.url().startsWith(baseUrl) && !request.url().includes('favicon'))
      errors.push(`request:${request.url()}`);
  });
  try {
    const response = await page.goto(baseUrl + pageRoute,
      { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.evaluate(() => document.fonts.ready);
    const html = response?.ok() ? await response.text() : '';
    const built = existsSync(artifact) ? readFileSync(artifact, 'utf8') : '';
    const normalized = normalizeObservedCloudflareHtml(html);
    const sourceText = existsSync(source) ? readFileSync(source, 'utf8') : '';
    const markers = kind === 'article'
      ? [...sourceText.matchAll(/<!--\s*(?:scientific-state|publication-readiness):.*?-->/g)]
        .map((match) => match[0]) : [];
    const sourceMarkerBound = kind === 'annex' || (markers.length === 2
      && markers.every((marker) => html.includes(marker)));
    const figures = page.locator('.page__content figure.post3-figure');
    for (let i = 0; i < await figures.count(); i += 1) {
      const image = figures.nth(i).locator('img.post3-theme-image');
      await image.evaluate((node) => { node.loading = 'eager'; });
    }
    const keyboard = [];
    for (let i = 0; i < await figures.count(); i += 1) {
      const figure = figures.nth(i);
      const link = figure.locator('a.post3-theme-link');
      if (await link.count() !== 1) { keyboard.push(false); continue; }
      await link.focus();
      const focus = await link.evaluate((node) => {
        const style = getComputedStyle(node);
        return document.activeElement === node && style.outlineStyle !== 'none'
          && parseFloat(style.outlineWidth) >= 3;
      });
      await page.keyboard.press('Tab');
      const fallback = await figure.evaluate((node) => node.contains(document.activeElement)
        && Boolean(document.activeElement?.closest('.figure-data')));
      keyboard.push(focus && fallback);
    }
    const observed = await page.evaluate(({ locale, theme, viewportWidth }) => {
      const content = document.querySelector('.page__content');
      const para = content?.querySelector(':scope > p:not(.table-caption)');
      const paragraphBox = para?.getBoundingClientRect();
      const tables = [...(content?.querySelectorAll('table') || [])];
      const wrappers = [...(content?.querySelectorAll('.tabla-desliza') || [])];
      const figureRows = [...(content?.querySelectorAll('figure.post3-figure') || [])].map((figure) => {
        const image = figure.querySelector('img.post3-theme-image');
        const caption = figure.querySelector('figcaption');
        const expectedSuffix = `-${locale}-${theme === 'academic-night' ? 'dark' : 'light'}-`
          + `${viewportWidth < 768 ? 'mobile' : 'desktop'}.svg`;
        const actual = new URL(image?.currentSrc || 'about:blank').pathname.split('/').pop();
        const stem = actual?.endsWith(expectedSuffix) ? actual.slice(0, -expectedSuffix.length) : null;
          const figureBox = figure.getBoundingClientRect();
          const imageBox = image?.getBoundingClientRect();
          return { id: figure.id, stem, src: image?.currentSrc || '', alt: image?.getAttribute('alt') || '',
          complete: Boolean(image?.complete && image.naturalWidth > 0),
          caption: caption?.textContent || '',
          source: caption?.querySelector('.figure-source')?.textContent || '',
          links: [...figure.querySelectorAll('a.post3-theme-link,.figure-data a')].map((link) =>
            new URL(link.href).pathname.replace(/^\/en(?=\/assets\/)/, '')),
          widthRatio: paragraphBox?.width ? figureBox.width / paragraphBox.width : 0,
          imagePx: imageBox?.width || 0,
          visible: figureBox.width > 0 && figureBox.height > 0 };
      });
      const paraStyles = [...(content?.querySelectorAll('p') || [])]
        .map((node) => getComputedStyle(node));
      const tableFonts = tables.flatMap((table) => [...table.querySelectorAll('th,td')]
        .map((cell) => parseFloat(getComputedStyle(cell).fontSize)));
      const sensitivityTables = tables.filter((table) =>
        (table.getAttribute('data-visual-family') || '').startsWith('post4-sensitivity-'))
        .map((table) => ({ family: table.getAttribute('data-visual-family'),
          text: table.textContent.replace(/\s+/g,' ').trim() }));
      return { title: document.title, theme: document.documentElement.getAttribute('data-theme') || 'light',
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
        paragraphJustified: paraStyles.length > 0 && paraStyles.every((style) =>
          style.textAlign === 'justify' && style.hyphens === 'auto'),
        tableCount: tables.length, tableMinPx: Math.min(...tableFonts),
        tablesAccessible: wrappers.length === tables.length && wrappers.every((node) =>
          node.getAttribute('role') === 'region' && node.getAttribute('tabindex') === '0'
            && Boolean(node.getAttribute('aria-label'))),
        figureRows, sensitivityTables };
    }, { locale, theme, viewportWidth: viewport.width });
    const expectedStems = new Map(manifests.flatMap((entry) => entry.manifest.figures.map((figure) =>
      [resetStem(number, figure, entry.family), { ...figure, family: entry.family,
        assetBase: entry.assetBase }])));
    const failures = [];
    if (response?.status() !== 200 || !html || !built || !normalized.safe || normalized.html !== built
      || !sourceText || !sourceMarkerBound) failures.push('route-artifact-binding');
    if (observed.theme !== theme || observed.overflow) failures.push('theme-or-overflow');
    if (!observed.paragraphJustified) failures.push('paragraph-justification');
    if (!observed.tablesAccessible || observed.tableMinPx < 14) failures.push('table-accessibility');
    if (keyboard.some((value) => !value)) failures.push('figure-keyboard-focus');
    for (const figure of observed.figureRows) {
      const contract = expectedStems.get(figure.stem);
      if (!contract || !figure.complete || !figure.visible || figure.widthRatio < 0.98
        || figure.imagePx < (viewport.width < 768 ? 294 : 672))
        failures.push(`figure-variant-or-layout:${figure.id}`);
      if (!contract) continue;
      const base = contract.assetBase;
      if (!base) { failures.push(`figure-asset-base-unbound:${figure.id}`); continue; }
      const activeTheme = theme === 'academic-night' ? 'dark' : 'light';
      const expectedLinks = expectedFigureLinks(number,contract,figure.stem,locale,activeTheme);
      if (!figureLinksComplete(figure.links,expectedLinks))
        failures.push(`figure-fallback-links:${figure.id}`);
      const expectedCaption = resetCaption(contract, locale);
      if (!expectedCaption || !normalizeText(figure.caption).includes(normalizeText(expectedCaption)))
        failures.push(`figure-caption-contract:${figure.id}`);
      const expectedAlt = contract.alt?.[locale] || contract[`alt_${locale}`];
      if (!expectedAlt || normalizeText(figure.alt) !== normalizeText(expectedAlt))
        failures.push(`figure-alt-contract:${figure.id}`);
      const expectedSource = contract.source_citation?.[locale]
        || contract[`source_citation_${locale}`];
      if (!expectedSource || normalizeText(figure.source) !== normalizeText(expectedSource))
        failures.push(`figure-source-contract:${figure.id}`);
    }
    if (errors.length) failures.push('browser-resource-error');
    return { locale, kind, theme, width: viewport.width, route: pageRoute,
      httpStatus: response?.status() || 0, sourceSha256: sourceText ? sha256(sourceText) : null,
      artifactSha256: built ? sha256(built) : null, observed, keyboard,
      errors, failures: [...new Set(failures)] };
  } finally { await context.close(); }
}

async function runScientificReset(number, args) {
  const manifestPaths = options(args, '--reset-manifest');
  const artifactRoot = option(args, '--artifact-root');
  const anticipationSourceRoot = option(args, '--anticipation-source-root');
  const sensitivitySourcePath = option(args, '--sensitivity-source');
  const sensitivityPrivateSourcePath = option(args, '--sensitivity-private-source');
  const ivPublicProjectionPath = option(args, '--iv-public-projection');
  const fixture = option(args, '--reset-fixture');
  const receiptPath = option(args, '--receipt');
  if (!manifestPaths.length || manifestPaths.some((path) => !existsSync(path)))
    throw new Error('--reset-manifest is required for each family');
  const audits = manifestPaths.map((path) => auditResetManifest(number, path, artifactRoot,
    null, anticipationSourceRoot, number === 4 ? ivPublicProjectionPath : sensitivitySourcePath,
    number === 3 ? sensitivityPrivateSourcePath : null));
  const familyCounts = audits.reduce((counts, entry) => {
    counts[entry.family] = (counts[entry.family] || 0) + 1;
    return counts;
  }, {});
  const familyFailures = [];
  if ((number === 3 && (familyCounts.primary !== 1 || familyCounts.anticipation !== 1
      || familyCounts.sensitivity !== 1 || familyCounts.post4_primary_projected))
    || (number === 4 && (familyCounts.post4_primary_projected !== 1
      || familyCounts.sensitivity !== 1 || familyCounts.primary || familyCounts.anticipation)))
    familyFailures.push('manifest-family-inventory');
  if (number === 4 && audits.length === 2 && audits.some((entry) =>
    entry.manifest.source_sha256 !== audits[0].manifest.source_sha256))
    familyFailures.push('iv-public-projection-shared-source');
  if (fixture) {
    const isAnticipation = ['wrong-rate', 'wrong-arm', 'wrong-cohort',
      'privacy-leak'].includes(fixture);
    const isSensitivity = fixture.startsWith('sensitivity-');
    const target = audits.find((entry) => entry.family === (isSensitivity ? 'sensitivity'
      : isAnticipation ? 'anticipation' : 'primary'));
    if (!target) throw new Error(`fixture family missing: ${fixture}`);
    const sensitivityKind = fixture.includes('did') ? 'did'
      : fixture.includes('bound') ? 'bounds' : 'd1_d2';
    const figure = isSensitivity ? target.manifest.figures.find((item) => item.kind === sensitivityKind)
      : target.manifest.figures.find((item) => item.source_rows?.some((row) =>
      row.display_status === (fixture === 'privacy-leak'
        ? 'PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY' : 'OBSERVED')))
      || target.manifest.figures[0];
    const stem = resetStem(number, figure, target.family);
    const targetStatus = fixture === 'privacy-leak' ? 'PRIVACY_SUPPRESSED_CROSS_ELIGIBILITY' : 'OBSERVED';
    const index = isAnticipation ? figure.source_rows.findIndex((row) =>
      row.display_status === targetStatus) : isSensitivity && sensitivityKind === 'd1_d2' ? 1 : 0;
    const mutations = {
      'wrong-estimate': { stem, column: 'estimate_pp', value: '999.999' },
      'wrong-denominator': { stem, column: 'n_treated', value: '999999999' },
      'wrong-reason': { stem, column: 'limitation', value: 'reason deliberately changed' },
      'wrong-rate': { stem, index, column: 'rate_pp', value: '999.9' },
      'wrong-arm': { stem, index, column: 'arm', value:
        figure.source_rows[index]?.arm === 'treated' ? 'control' : 'treated' },
      'wrong-cohort': { stem, index, column: 'cohort_year', value: '2999' },
      'privacy-leak': { stem, index, column: 'rate_pp', value: '77.7' },
      'sensitivity-wrong-did-school-ci': { stem, index, column: 'school_ci_high_pp', value: '999.9' },
      'sensitivity-wrong-bound': { stem, index, column: 'upper_pp', value: '-999.9' },
      'sensitivity-wrong-d1-period': { stem, index, column: 'cohort_end', value: '2019' }
    };
    const mutation = mutations[fixture];
    if (!mutation || index < 0) throw new Error(`unknown or inapplicable reset fixture: ${fixture}`);
    const mutant = auditResetManifest(number, manifestPaths[audits.indexOf(target)],
      artifactRoot, mutation, anticipationSourceRoot,
      number === 4 ? ivPublicProjectionPath : sensitivitySourcePath,
      number === 3 ? sensitivityPrivateSourcePath : null);
    const expected = isSensitivity ? `sensitivity-figure-manifest:${stem}:${index}`
      : fixture === 'wrong-arm' ? `anticipation-figure-manifest:${stem}:${index}`
      : isAnticipation ? `anticipation-figure-master:${stem}:${index}`
        : `figure-csv-master:${stem}:0`;
    const discriminates = audits.every((entry) => entry.failures.length === 0)
      && mutant.failures.includes(expected)
      && (fixture !== 'privacy-leak' || mutant.failures.includes(`anticipation-privacy:${stem}:${index}`));
    const result = { status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture,
      baselineFailures: audits.flatMap((entry) => entry.failures),
      mutantFailures: mutant.failures, expected };
    console.log(JSON.stringify(result));
    process.exitCode = discriminates ? 1 : 2;
    return;
  }
  const scientificReady = audits.length > 0 && audits.every((entry) =>
    entry.manifest.f2_complete === true && entry.manifest.publication_authorized === true);
  const baseUrl = option(args, '--base-url')?.replace(/\/$/, '');
  const rows = [], noJs = [], print = [], browserFailures = [];
  let cssBound = false;
  if (baseUrl && artifactRoot) {
    if (!/^https?:\/\//.test(baseUrl)) throw new Error('invalid base URL');
    const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
      || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
    if (!existsSync(playwrightPath)) throw new Error(`Playwright missing: ${playwrightPath}`);
    const playwright = createRequire(import.meta.url)(playwrightPath);
    const executable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
      || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);
    const browser = await playwright.chromium.launch({ headless: true,
      ...(executable ? { executablePath: executable } : {}), args: ['--no-sandbox'] });
    try {
      for (const locale of ['es', 'en']) for (const kind of ['article', 'annex']) {
        for (const theme of themes) for (const viewport of viewports) {
          rows.push(await inspectResetPage(browser, number, configs[number], audits,
            locale, kind, theme, viewport, baseUrl, artifactRoot));
        }
        for (const width of [320, 390])
          noJs.push(await inspectNoJs(browser, configs[number], locale, kind, baseUrl, width));
        print.push(await inspectPrint(browser, configs[number], locale, kind, baseUrl));
      }
      if (number === 4) {
        const sensitivity = audits.find((entry) => entry.family === 'sensitivity');
        if (!sensitivity) browserFailures.push('iv-sensitivity-table-source-inventory');
        else {
        for (const locale of ['es','en']) {
          const sourceTables = (sensitivity?.manifest.files || []).map((item) => item.name)
            .filter((name) => name.endsWith(`-${locale}.html`));
          if (sourceTables.length !== 3) {
            browserFailures.push(`iv-sensitivity-table-source-inventory:${locale}`); continue;
          }
          const probe = await browser.newPage();
          try {
            const expected = [];
            for (const name of sourceTables) {
              const markup = readFileSync(resolve(dirname(manifestPaths[audits.indexOf(sensitivity)]),
                name),'utf8');
              await probe.setContent(markup);
              expected.push(await probe.locator('table').evaluate((table) =>
                table.textContent.replace(/\s+/g,' ').trim()));
            }
            const rendered = rows.filter((row) => row.locale === locale
              && row.theme === 'light' && row.width === 1440)
              .flatMap((row) => row.observed.sensitivityTables || []).map((table) => table.text);
            if (expected.some((text) => rendered.filter((value) => value === text).length !== 1)
              || rendered.length !== 3)
              browserFailures.push(`iv-sensitivity-table-dom-binding:${locale}`);
          } finally { await probe.close(); }
        }
        }
      }
    } finally { await browser.close(); }
    const cssArtifact = resolve(artifactRoot, 'assets/css/main.css');
    const response = await fetch(`${baseUrl}/assets/css/main.css`,
      { signal: AbortSignal.timeout(15_000) });
    cssBound = Boolean(response.ok && existsSync(cssArtifact)
      && sha256(Buffer.from(await response.arrayBuffer())) === sha256(readFileSync(cssArtifact)));
    if (!cssBound) browserFailures.push('css-artifact-binding');
    for (const locale of ['es', 'en']) {
      const published = rows.filter((row) => row.locale === locale && row.theme === 'light'
        && row.width === 1440).flatMap((row) => row.observed.figureRows.map((figure) => figure.stem));
      const expected = audits.flatMap((entry) => entry.manifest.figures.map((figure) =>
        resetStem(number, figure, entry.family)));
      if (published.length !== expected.length || new Set(published).size !== expected.length
        || expected.some((stem) => !published.includes(stem)))
        browserFailures.push(`figure-inventory:${locale}`);
      const jsTables = rows.filter((row) => row.locale === locale && row.theme === 'light'
        && row.width === 1440).reduce((sum, row) => sum + row.observed.tableCount, 0);
      if (jsTables === 0) browserFailures.push(`table-inventory-empty:${locale}`);
      const noJsCount = noJs.filter((row) => row.locale === locale)
        .reduce((sum, row) => sum + row.figureCount, 0);
      const printCount = print.filter((row) => row.locale === locale)
        .reduce((sum, row) => sum + row.figureCount, 0);
      if (noJsCount !== expected.length * 2 || printCount !== expected.length)
        browserFailures.push(`fallback-figure-inventory:${locale}`);
    }
    if (noJs.some((row) => row.httpStatus !== 200 || !row.noOverflow
      || !row.openedNoOverflow || row.detailsOpened !== row.detailsCount
      || !row.openedTablesVisible || row.navLinks !== 4 || !row.figures))
      browserFailures.push('nojs-fallback');
    if (print.some((row) => row.httpStatus !== 200 || !row.figuresVisible))
      browserFailures.push('print-fallback');
  }
  if (rows.some((row) => row.failures.length)) browserFailures.push('rendered-route-failures');
  const pending = [];
  if (!scientificReady) pending.push('F2 final scientific review');
  if (familyFailures.length) pending.push('complementary manifest family');
  if (!baseUrl || !artifactRoot) pending.push('F3 rendered routes and source/artifact binding');
  const failures = [...familyFailures, ...audits.flatMap((entry) => entry.failures)];
  const sourceFilesBound = number === 3 ? audits.some((entry) =>
    entry.family === 'anticipation' && entry.sourceFilesBound) : null;
  const sensitivitySourceBound = number === 3 ? audits.some((entry) =>
    entry.family === 'sensitivity' && entry.sourceFilesBound) : null;
  const sensitivityPrivateSourceBound = number === 3
    ? audits.find((entry) => entry.family === 'sensitivity')?.privateSourceBound ?? null : null;
  const ivPublicProjectionBound = number === 4 ? audits.some((entry) =>
    entry.family === 'sensitivity' && entry.sourceFilesBound) : null;
  if (number === 3 && !sensitivitySourceBound)
    pending.push('F2 sensitivity source SHA-256 binding');
  const localPending = number === 3 && sensitivityPrivateSourceBound === false
    ? ['Exact two-way interval comparison requires local private source SHA-256 binding'] : [];
  if (number === 4 && !ivPublicProjectionBound)
    pending.push('F2 IV public projection SHA-256 binding');
  const publicReady = failures.length === 0 && scientificReady
      && (number !== 3 || sensitivitySourceBound)
      && (number !== 4 || ivPublicProjectionBound)
      && artifactRoot && baseUrl && browserFailures.length === 0;
  const verdict = resetGateVerdict(number, publicReady, sensitivityPrivateSourceBound);
  const result = { status: verdict.status,
    verificationScope: number !== 3 ? 'PUBLIC_PROJECTION'
      : sensitivityPrivateSourcePath ? 'LOCAL_FULL' : 'PUBLIC_CI',
    exactTwoWayIntervalsVerified: number === 3 ? sensitivityPrivateSourceBound === true : null,
    scientificReady, manifest: manifestPaths.map((path) => resolve(path)),
    manifests: audits.map((entry) => ({ family: entry.family,
      manifest: resolve(manifestPaths[audits.indexOf(entry)]),
      manifestSha256: entry.manifestSha256, files: entry.files, figures: entry.figures,
      assetBase: entry.assetBase || null,
      csvRows: entry.csvRows, statusCounts: entry.statusCounts || null,
      sourceFilesBound: entry.sourceFilesBound ?? null,
      privateSourceBound: entry.privateSourceBound ?? null,
      sourceRows: entry.sourceRows ?? null,
      sourceFileMismatches: entry.sourceFileMismatches || [],
      failures: entry.failures, sourceMismatches: entry.sourceMismatches,
      artifactMismatches: entry.artifactMismatches, manifestBound: entry.manifestBound })),
    files: audits.reduce((sum, entry) => sum + entry.files, 0),
    figures: audits.reduce((sum, entry) => sum + entry.figures, 0),
    csvRows: audits.reduce((sum, entry) => sum + entry.csvRows, 0), failures,
    sourceFilesBound,
    sensitivitySourceBound,
    sensitivityPrivateSourceBound,
    ivPublicProjectionBound,
    sourceVerification: number !== 3 ? 'not_applicable' : sourceFilesBound
      ? 'local_sha256_39_files' : 'public_custody_only_requires_local_f2_receipt',
    sensitivitySourceVerification: number !== 3 ? 'not_applicable'
      : sensitivitySourceBound && sensitivityPrivateSourceBound === true
        ? 'public_projection_sha256_49_rows_plus_private_two_way_sha256'
      : sensitivitySourceBound && sensitivityPrivateSourcePath ? 'private_source_invalid'
        : sensitivitySourceBound ? 'public_projection_sha256_49_rows_no_exact_two_way_ci' : 'unbound',
    cssBound, rows, noJs, print,
    browserFailures: [...new Set(browserFailures)], pending, localPending };
  if (receiptPath) { mkdirSync(dirname(resolve(receiptPath)), { recursive: true });
    writeFileSync(receiptPath, `${JSON.stringify(result, null, 2)}\n`); }
  console.log(JSON.stringify(result));
  process.exitCode = verdict.exitCode;
}

export async function waitForImageCompleteNoJs(image, timeoutMs = 15_000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const remaining = deadline - Date.now();
    let complete;
    try {
      complete = await bounded(image.evaluate((node) => node.complete), remaining,
        'nojs-image-poll-timeout');
    } catch { return false; }
    if (complete) return true;
    await new Promise((done) => setTimeout(done, Math.min(250, Math.max(1, deadline - Date.now()))));
  }
  return false;
}

async function inspectNoJs(browser, config, locale, kind, baseUrl, width) {
  const context = await browser.newContext({ viewport: { width, height: 844 }, javaScriptEnabled: false });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route(config, locale, kind),
      { waitUntil: 'domcontentloaded', timeout: 30_000 });
    const rows = page.locator('.page__content figure.post3-figure img.post3-theme-image');
    for (let i = 0; i < await rows.count(); i += 1) {
      const image = rows.nth(i);
      await image.scrollIntoViewIfNeeded();
      await image.evaluate((node) => { node.loading = 'eager'; });
      await waitForImageCompleteNoJs(image);
    }
    const noOverflow = await page.evaluate(() =>
      document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    const summaries = page.locator('.page__content details.post3-methods > summary');
    const detailsCount = await summaries.count();
    for (let i = 0; i < detailsCount; i += 1) {
      await summaries.nth(i).focus();
      await page.keyboard.press('Enter');
    }
    return await page.evaluate((payload) => {
      const details = [...document.querySelectorAll('.page__content details.post3-methods')];
      return {
        locale: payload.locale, kind: payload.kind, width: payload.width,
        httpStatus: payload.status, noOverflow: payload.noOverflow,
        openedNoOverflow: document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2,
        detailsCount: details.length,
        detailsOpened: details.filter((detail) => detail.open).length,
        openedTablesVisible: details.every((detail) => [...detail.querySelectorAll('table')]
          .every((table) => table.getBoundingClientRect().height > 0)),
        navLinks: document.querySelectorAll('.page__content nav.thesis-series-nav a').length,
        figureCount: document.querySelectorAll('.page__content figure.post3-figure img.post3-theme-image').length,
        figures: [...document.querySelectorAll('.page__content figure.post3-figure img.post3-theme-image')]
          .every((image) => image.currentSrc.includes('-light-mobile.svg')
            && image.complete && image.naturalWidth > 0)
      };
    }, { locale, kind, width, status: response?.status() || 0, noOverflow });
  } finally { await context.close(); }
}

async function inspectPrint(browser, config, locale, kind, baseUrl) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route(config, locale, kind),
      { waitUntil: 'domcontentloaded', timeout: 30_000 });
    const images = page.locator('.page__content img.post3-theme-image');
    await images.evaluateAll((nodes) => nodes.forEach((image) => { image.loading = 'eager'; }));
    for (let i = 0; i < await images.count(); i += 1) await images.nth(i).scrollIntoViewIfNeeded();
    await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
    await page.emulateMedia({ media: 'print', colorScheme: 'light' });
    let imagesReady = true;
    try {
      await page.waitForFunction(() => [...document.querySelectorAll('.page__content img.post3-theme-image')]
        .every((image) => image.complete && image.naturalWidth > 0 && image.currentSrc.includes('-light')),
      null, { timeout: 15_000 });
    } catch { imagesReady = false; }
    return await page.evaluate((payload) => {
      const figures = [...document.querySelectorAll('.page__content figure.post3-figure')];
      return {
        locale: payload.locale, kind: payload.kind, httpStatus: payload.status,
        figureCount: figures.length,
        figuresVisible: payload.imagesReady && figures.every((figure) => {
          const image = figure.querySelector('img.post3-theme-image');
          return figure.getBoundingClientRect().width > 0
            && getComputedStyle(figure).display !== 'none'
            && image?.currentSrc.includes('-light');
        }),
        imageSources: figures.map((figure) => figure.querySelector('img.post3-theme-image')?.currentSrc || '')
      };
    }, { locale, kind, status: response?.status() || 0, imagesReady });
  } finally { await context.close(); }
}

export async function main(number) {
  if (!configs[number]) throw new Error(`unknown thesis post: ${number}`);
  const args = process.argv.slice(2);
  const fixture = option(args, '--fixture');
  if (fixture) return runFixture(fixture); // Historical unit probes; never a release verdict.
  if (option(args, '--reset-manifest')) return runScientificReset(number, args);
  console.error(JSON.stringify({ status: 'ERROR', error: option(args, '--artifact-root')
    ? '--reset-manifest is required; legacy III/IV golden are obsolete'
    : '--artifact-root is required for an artifact-bound PASS' }));
  process.exitCode = 2;
}
