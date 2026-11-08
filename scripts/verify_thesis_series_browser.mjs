#!/usr/bin/env node

// Browser contract for the article and its separate methods annex. The Ruby gates
// protect scientific content; this gate binds the rendered routes to a fresh build
// and checks that readers can actually reach and use both pages.
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, symlinkSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(scriptDir, '..');
const prefix = '/datos/educacion/politica-publica/';
const configs = {
  3: {
    slug: 'costos-cierre-escolar-trayectorias',
    post: '_posts/2026-10-23-costos-cierre-escolar-trayectorias',
    annex: '_pages/tesis-post3-anexo-metodologico',
    figures: { article: 2, annex: 2 },
    totalFigures: 4,
    totalTables: 7,
    referenceKeys: 18,
    current: 3
  },
  4: {
    slug: 'cierre-escolar-educacion-superior-causal-ml',
    post: '_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml',
    annex: '_pages/tesis-post4-anexo-metodologico',
    figures: { article: 1, annex: 2 },
    totalFigures: 3,
    totalTables: 6,
    referenceKeys: 27,
    current: 4
  }
};
const viewports = [
  { width: 320, height: 800 },
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 1440, height: 1000 }
];
const themes = ['light', 'academic-night'];
const post4CsvContracts = {
  'selection-ladder-data.csv': {
    columns: ['education_level', 'step', 'estimator', 'estimate_pp', 'se_pp', 'ci95_low_pp', 'ci95_high_pp'],
    rows: 8,
    sample: { education_level: 'secondary', step: 'step1_demographics_only', estimate_pp: '-13.24' }
  },
  'longitudinal-regimes-data.csv': {
    columns: ['regime', 'education_level', 'treated_post_students', 'raw_post_gap_pp',
      'pre_g5_gap_pp', 'did_any_he_pp', 'did_univ_pp', 'did_ipcft_pp', 'did_persist_2yr_pp'],
    rows: 6,
    sample: { regime: '2009_2015_pre_gratuidad', education_level: 'secondary', did_any_he_pp: '0.55' }
  },
  'causal-ml-heterogeneity-paes-data.csv': {
    columns: ['panel', 'outcome', 'group_or_spec', 'estimate_pp', 'se_pp', 'ci95_low_pp', 'ci95_high_pp'],
    rows: 32,
    sample: { panel: 'GATE_quintile', outcome: 'any_he_two_year',
      group_or_spec: 'G1_most_harmed', estimate_pp: '-12.26' }
  }
};
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const option = (args, flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};
const sourcePath = (config, locale, kind) => resolve(siteRoot,
  `${kind === 'article' ? config.post : config.annex}${locale === 'en' ? '-en' : ''}.md`);
const route = (config, locale, kind) =>
  `${locale === 'en' ? '/en' : ''}${prefix}${config.slug}/${kind === 'annex' ? 'anexo-metodologico/' : ''}`;
const sourceTitle = (path) => {
  const match = readFileSync(path, 'utf8').match(/^title:\s*["']?(.*?)["']?\s*$/m);
  return match?.[1] || '';
};
const manifestBinding = (number, artifactRoot) => {
  const folder = `assets/images/tesis-post${number}`;
  const manifestPath = resolve(siteRoot, folder, 'manifest.json');
  if (!existsSync(manifestPath)) return { valid: false, error: 'manifest missing' };
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const files = manifest.files || [];
  const expected = number === 3 ? 77 : 51;
  const visual = files.filter((entry) => ['svg', 'png'].includes(entry.format));
  const csv = files.filter((entry) => entry.format === 'csv');
  const visualPaths = number === 4 ? ['selection-ladder', 'longitudinal-regimes', 'causal-ml-heterogeneity-paes']
    .flatMap((figure) => ['es', 'en'].flatMap((lang) => ['light', 'dark']
      .flatMap((theme) => ['desktop', 'mobile'].flatMap((layout) => ['svg', 'png']
        .map((format) => `${figure}-${lang}-${theme}${layout === 'mobile' ? '-mobile' : ''}.${format}`))))) : [];
  const expectedCsvPaths = Object.keys(post4CsvContracts).sort();
  const structureValid = number === 3 ? files.length === expected
    : files.length === expected && visual.length === 48 && csv.length === 3
      && visual.map((entry) => entry.path).sort().join('\n') === visualPaths.sort().join('\n')
      && csv.map((entry) => entry.path).sort().join('\n') === expectedCsvPaths.join('\n');
  const mismatches = [];
  const artifactMismatches = [];
  for (const entry of files) {
    const safePath = /^[a-z0-9-]+\.(?:svg|png|csv)$/.test(entry.path)
      || (number === 3 && /^[a-z0-9-]+\.visual-manifest\.json$/.test(entry.path));
    if (!safePath) {
      mismatches.push(entry.path);
      continue;
    }
    const path = resolve(siteRoot, folder, entry.path);
    if (!existsSync(path) || statSync(path).size !== entry.bytes
      || sha256(readFileSync(path)) !== entry.sha256) mismatches.push(entry.path);
    const artifactPath = resolve(artifactRoot, folder, entry.path);
    if (!existsSync(artifactPath) || statSync(artifactPath).size !== entry.bytes
      || sha256(readFileSync(artifactPath)) !== entry.sha256)
      artifactMismatches.push(entry.path);
  }
  const artifactManifest = resolve(artifactRoot, folder, 'manifest.json');
  const manifestBound = existsSync(artifactManifest)
    && sha256(readFileSync(artifactManifest)) === sha256(readFileSync(manifestPath));
  return { valid: structureValid && mismatches.length === 0 && artifactMismatches.length === 0
      && manifestBound,
    count: files.length, expected, mismatches, artifactMismatches,
    visualCount: visual.length, csvCount: csv.length, structureValid, manifestBound,
    sha256: sha256(readFileSync(manifestPath)) };
};

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
  if (!row.naturalTextFlowValid) errors.push('unnatural-text-flow');
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
    themeSurfaceValid: true, editorialGeometryValid: true, naturalTextFlowValid: true,
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
    'off-theme-panel': 'dark-panel-tone-mismatch',
    'missing-he-agenda': 'series-navigation', 'he-blocker': 'public-content-safety',
    'missing-footnote': 'missing-references', 'missing-annex': 'route-artifact-binding',
    'missing-series-link': 'series-navigation', 'stale-build': 'route-artifact-binding'
  }[name];
  const exact = failures.length === 1 && failures[0] === expected;
  console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture: name, failures, expected }));
  process.exitCode = exact ? 1 : 2;
}

async function inspectPage(browser, config, locale, kind, theme, viewport, baseUrl, artifactRoot,
  screenshotDir, liveFixture = null) {
  const pageRoute = route(config, locale, kind);
  const source = sourcePath(config, locale, kind);
  const artifact = resolve(artifactRoot, pageRoute.replace(/^\//, ''), 'index.html');
  const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
  await context.addInitScript((mode) => localStorage.setItem('3cucharadas-theme', mode), theme);
  const page = await context.newPage();
  if (liveFixture === 'missing-annex' && kind === 'annex') {
    await page.route(`${baseUrl}${pageRoute}`, (intercepted) => intercepted.fulfill({
      status: 404, contentType: 'text/html', body: '<!doctype html><title>Missing annex</title><main>Missing annex</main>'
    }));
  }
  const criticalErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error' && !message.text().includes('favicon')) criticalErrors.push(`console:${message.text()}`);
  });
  page.on('requestfailed', (request) => {
    if (request.url().startsWith(baseUrl) && !request.url().includes('favicon'))
      criticalErrors.push(`request:${request.url()}`);
  });
  try {
    const response = await page.goto(baseUrl + pageRoute, { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.evaluate(() => document.fonts.ready);
    if (liveFixture === 'overflow') {
      await page.evaluate(() => {
        const probe = document.createElement('div');
        probe.id = 'browser-gate-overflow-probe';
        probe.style.cssText = 'position:absolute;left:0;top:0;width:10000px;height:1px;';
        document.body.append(probe);
      });
    }
    const html = response?.ok() ? await response.text() : '';
    const built = existsSync(artifact) ? readFileSync(artifact, 'utf8') : '';
    const sourceText = readFileSync(source, 'utf8');
    const sourceFresh = existsSync(artifact) && statSync(artifact).mtimeMs >= statSync(source).mtimeMs;
    const markers = kind === 'article'
      ? [...sourceText.matchAll(/<!--\s*(?:scientific-state|publication-readiness):.*?-->/g)].map((m) => m[0])
      : [];
    const sourceMarkerBound = kind === 'annex' || (markers.length === 2
      && markers.every((marker) => html.includes(marker)));
    const figures = page.locator('.page__content figure.post3-figure');
    for (let i = 0; i < await figures.count(); i += 1) {
      await figures.nth(i).scrollIntoViewIfNeeded();
      await figures.nth(i).locator('img.post3-theme-image').waitFor({ state: 'visible' });
      await figures.nth(i).locator('img.post3-theme-image').evaluate((image) => {
        image.loading = 'eager';
        if (!image.complete) return new Promise((done) => {
          image.addEventListener('load', done, { once: true });
          image.addEventListener('error', done, { once: true });
        });
        return null;
      });
    }
    const focusRows = [];
    for (let i = 0; i < await figures.count(); i += 1) {
      const link = figures.nth(i).locator('a.post3-theme-link');
      await link.focus();
      const visible = await link.evaluate((anchor) => {
        const style = getComputedStyle(anchor);
        return document.activeElement === anchor && style.outlineStyle !== 'none'
          && parseFloat(style.outlineWidth) >= 3;
      });
      await page.keyboard.press('Tab');
      const fallback = await page.evaluate((id) => document.activeElement?.closest('figure')?.id === id
        && Boolean(document.activeElement?.closest('.figure-data')), await figures.nth(i).getAttribute('id'));
      focusRows.push(visible && fallback);
    }
    const row = await page.evaluate(async (payload) => {
      const article = document.querySelector('.page__content');
      const articleBox = article?.getBoundingClientRect();
      const body = article?.innerText || '';
      const headingText = [...(article?.querySelectorAll('h2') || [])].map((h) => h.textContent.trim());
      const tables = [...(article?.querySelectorAll('table') || [])];
      const wrappers = [...(article?.querySelectorAll('.tabla-desliza') || [])];
      const tableFonts = tables.flatMap((table) => [...table.querySelectorAll('th, td')]
        .map((cell) => parseFloat(getComputedStyle(cell).fontSize)));
      const footnotes = [...(article?.querySelectorAll('.footnotes li') || [])];
      const referenceFonts = footnotes.map((note) => parseFloat(getComputedStyle(note).fontSize));
      const figureRows = await Promise.all([...(article?.querySelectorAll('figure.post3-figure') || [])]
        .map(async (figure) => {
          const image = figure.querySelector('img.post3-theme-image');
          const captionText = figure.querySelector('figcaption')?.textContent.trim() || '';
          const altText = image?.getAttribute('alt') || '';
          const normalizedAlt = altText.replace(/,/g, '.');
          const normalizedCaption = captionText.replace(/,/g, '.');
          const hasNumbers = (text, values) => values.every((value) => text.includes(value));
          let semanticValid = true;
          if (payload.number === 4) {
            if (figure.id === 'fig-post4-1') {
              semanticValid = hasNumbers(normalizedAlt, ['13.24', '2.09'])
                && hasNumbers(normalizedCaption, ['13.24', '1.21', '1.02'])
                && /incluyen cero|include zero/i.test(captionText);
            } else if (figure.id === 'fig-post4-2') {
              semanticValid = hasNumbers(normalizedAlt, ['0.55', '2.64', '3.79'])
                && /D1/.test(captionText) && /D2/.test(captionText)
                && /jurídic|legal/i.test(captionText);
            } else if (figure.id === 'fig-post4-3') {
              semanticValid = hasNumbers(normalizedAlt, ['12.26', '0.26'])
                && hasNumbers(normalizedCaption, ['12.26', '0.26'])
                && /no aparece|not (?:shown|displayed|plotted|in)|absent from panel/i.test(captionText);
            } else semanticValid = false;
          }
          const imageBox = image?.getBoundingClientRect();
          const box = figure.getBoundingClientRect();
          const style = getComputedStyle(figure);
          const links = [...figure.querySelectorAll('.figure-data a')];
          const dataResponses = await Promise.all(links.map(async (link) => {
            try {
              const target = new URL(link.href);
              const assetPath = target.pathname.replace(/^\/en(?=\/assets\/)/, '');
              if (target.origin !== location.origin) return false;
              const response = await fetch(link.href);
              if (assetPath === '/assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json'
                && payload.number === 4) {
                const data = await response.json();
                const sample = data?.track_c_causal_ml?.orthogonal_r_learner_heterogeneity
                  ?.full_student_and_school_g5_controls?.any_he_two_year
                  ?.gates_by_quintile?.G1_most_harmed;
                return response.ok && sample?.gate_pp === -0.26
                  && sample?.ci95_pp?.[0] === -2.73 && sample?.ci95_pp?.[1] === 2.21;
              }
              if (!assetPath.startsWith(`/assets/images/tesis-post${payload.number}/`)
                || !assetPath.endsWith('.csv')) return false;
              const csv = await response.text();
              const lines = csv.trim().split(/\r?\n/);
              const header = lines[0].split(',');
              if (!response.ok || lines.length < 2) return false;
              if (payload.number === 3) return ['reading_limit_es', 'reading_limit_en']
                .every((column) => header.includes(column));
              const filename = new URL(link.href).pathname.split('/').pop();
              const contract = payload.post4CsvContracts[filename];
              const rows = lines.slice(1).map((line) => line.split(','));
              return Boolean(contract && lines.length === contract.rows + 1
                && header.length === contract.columns.length
                && contract.columns.every((column, index) => header[index] === column)
                && rows.every((row) => row.length === header.length)
                && rows.some((row) => Object.entries(contract.sample)
                  .every(([column, value]) => row[header.indexOf(column)] === value)));
            } catch { return false; }
          }));
          let svgTextPx = 0;
          try {
            const svg = await (await fetch(image.currentSrc)).text();
            const width = Number(svg.match(/viewBox="[^\"]*?\s([0-9.]+)\s[0-9.]+"/)?.[1] || 0);
            const declared = [...svg.matchAll(/font-size:\s*([0-9.]+)px/g)].map((m) => Number(m[1]));
            if (width && declared.length && imageBox) svgTextPx = Math.min(...declared) * imageBox.width / width;
          } catch { svgTextPx = 0; }
          return {
            src: image?.currentSrc || '',
            complete: image?.complete && image?.naturalWidth > 0 && image?.naturalHeight > 0,
            named: Boolean(image?.getAttribute('alt')?.trim()),
            sized: Boolean(imageBox && imageBox.width > 0 && imageBox.height > 180),
            contained: Boolean(articleBox) && box.left >= articleBox.left - 2 && box.right <= articleBox.right + 2,
            caption: Boolean(figure.querySelector('figcaption .figure-source'))
              && captionText.length >= 80,
            semanticValid,
            identity: figure.classList.contains('data-visualization') && style.fontFamily.includes('Fira Sans')
              && Boolean(style.getPropertyValue('--c3-viz-canvas').trim()),
            surface: style.backgroundColor,
            canvasToken: style.getPropertyValue('--c3-viz-canvas').trim().toLowerCase(),
            surfaceToken: style.getPropertyValue('--c3-viz-surface').trim().toLowerCase(),
            dataLinks: links.length,
            dataResponses,
            svgTextPx
          };
        }));
      const rootStyle = getComputedStyle(document.documentElement);
      const rootBackground = rootStyle.backgroundColor;
      const nightBackground = rootStyle.getPropertyValue('--night-bg').trim().toLowerCase();
      const nightLayer = rootStyle.getPropertyValue('--night-layer').trim().toLowerCase();
      const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
      const nav = article?.querySelector('nav.thesis-series-nav');
      const navLinks = [...(nav?.querySelectorAll('a') || [])];
      const current = navLinks.filter((link) => link.hasAttribute('aria-current'));
      const expectedTheme = payload.theme === 'academic-night' ? '-dark' : '-light';
      const expectedLayout = payload.viewport.width < 768 ? '-mobile.svg' : '.svg';
      const firstPara = article?.querySelector(':scope > p:not(.table-caption)');
      const firstBox = firstPara?.getBoundingClientRect();
      const firstParaStyle = firstPara ? getComputedStyle(firstPara) : null;
      return {
        locale: payload.locale, kind: payload.kind, theme: payload.theme,
        viewportWidth: payload.viewport.width,
        titleMatches: document.title.includes(payload.title),
        structureValid: payload.kind === 'article'
          ? [1, 2, 3].every((n) => headingText.some((h) => h.includes(payload.locale === 'es'
            ? `Cucharada ${n}` : `Spoonful ${n}`)))
            && headingText.some((h) => /Cierre|Closing/.test(h))
            && Boolean(article?.querySelector('.notice--primary'))
            && !body.includes('ELI5')
          : headingText.some((h) => /Referencias|References/.test(h)) && !body.includes('ELI5'),
        navValid: Boolean(nav?.getAttribute('aria-label')) && navLinks.length === 4
          && navLinks.every((link) => link.href.startsWith(location.origin) && link.textContent.trim())
          && current.length === 1
          && current[0].getAttribute('aria-current') === (payload.kind === 'annex' ? 'step' : 'page')
          && current[0].href.includes(payload.slug),
        ivLinkPresent: payload.number === 4 || payload.kind === 'annex'
          || Boolean(article?.querySelector('p a[href*="cierre-escolar-educacion-superior-causal-ml/"]')),
        documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
        bodyFontPx: article ? parseFloat(getComputedStyle(article).fontSize) : 0,
        tableCount: tables.length,
        tableMinFontPx: tableFonts.length ? Math.min(...tableFonts) : 14,
        referenceCount: footnotes.length,
        referenceKeys: footnotes.map((note) => note.id.replace(/^fn:/, '')),
        referenceMinFontPx: referenceFonts.length ? Math.min(...referenceFonts) : 14,
        figureCount: figureRows.length,
        figuresValid: figureRows.every((figure) => figure.complete && figure.named && figure.sized
          && figure.contained && figure.caption),
        figureSemanticValid: figureRows.every((figure) => figure.semanticValid),
        figureThemeValid: figureRows.every((figure) => figure.src.includes(expectedTheme)
          && figure.src.endsWith(expectedLayout)),
        visualIdentityValid: figureRows.every((figure) => figure.identity),
        dataFallbackValid: figureRows.every((figure) => figure.dataLinks >= 1
          && figure.dataResponses.every(Boolean)),
        svgTextMinPx: figureRows.length ? Math.min(...figureRows.map((figure) => figure.svgTextPx)) : 10,
        tableWrappersValid: wrappers.length === tables.length && wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return wrapper.getAttribute('role') === 'region'
            && wrapper.getAttribute('data-table-contract') === 'explicit-v1'
            && wrapper.getAttribute('tabindex') === '0'
            && Boolean(wrapper.getAttribute('aria-label'))
            && ['auto', 'scroll'].includes(getComputedStyle(wrapper).overflowX)
            && box.left >= -2 && box.right <= document.documentElement.clientWidth + 2;
        }),
        tableHeadersScoped: tables.every((table) => [...table.querySelectorAll('thead th')]
          .every((cell) => cell.getAttribute('scope') === 'col')),
        idsUnique: new Set(ids).size === ids.length,
        imagesNamed: [...(article?.querySelectorAll('img') || [])]
          .every((image) => Boolean(image.getAttribute('alt')?.trim())),
        publicContentSafe: !/(?:\/home\/|\/mnt\/|\bMRUN\s*\d|\bRBD\s*\d|no está listo para publicación|not publication-ready)/i.test(body),
        themeSurfaceValid: payload.theme === 'academic-night'
          ? /rgb\((1[0-9]|2[0-9]|3[0-9]),/.test(rootBackground)
          : /rgb\((24[0-9]|25[0-5]),/.test(rootBackground),
        editorialGeometryValid: Boolean(firstBox) && wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return Math.abs(box.left - firstBox.left) <= 2 && Math.abs(box.width - firstBox.width) <= 2;
        }),
        naturalTextFlowValid: Boolean(firstParaStyle)
          && ['start', 'left'].includes(firstParaStyle.textAlign)
          && firstParaStyle.hyphens === 'none',
        darkPanelToneValid: payload.theme !== 'academic-night' || figureRows.every((figure) =>
          figure.canvasToken === nightBackground && figure.surfaceToken === nightLayer
            && figure.surface === rootBackground),
        figureRows
      };
    }, {
      locale, kind, theme, viewport, title: sourceTitle(source), slug: config.slug,
      number: config.current, post4CsvContracts
    });
    Object.assign(row, {
      route: pageRoute, httpStatus: response?.status() || 0,
      artifactBound: Boolean(html && built && html === built), sourceFresh, sourceMarkerBound,
      artifactSha256: built ? sha256(built) : null, servedSha256: html ? sha256(html) : null,
      sourceSha256: sha256(sourceText), expectedFigures: config.figures[kind],
      keyboardFocusValid: focusRows.length === row.figureCount && focusRows.every(Boolean),
      tableContractValid: true, criticalErrors
    });
    row.failures = evaluate(row);
    if (screenshotDir && [390, 1440].includes(viewport.width)) {
      mkdirSync(screenshotDir, { recursive: true });
      await page.screenshot({ path: resolve(screenshotDir,
        `post${config.current}-${locale}-${kind}-${theme}-${viewport.width}.png`), fullPage: true });
    }
    return row;
  } finally {
    await context.close();
  }
}

async function inspectNoJs(browser, config, locale, kind, baseUrl) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route(config, locale, kind), { waitUntil: 'domcontentloaded' });
    const rows = page.locator('.page__content figure.post3-figure img.post3-theme-image');
    for (let i = 0; i < await rows.count(); i += 1) await rows.nth(i).scrollIntoViewIfNeeded();
    return await page.evaluate((payload) => ({
      locale: payload.locale, kind: payload.kind, httpStatus: payload.status,
      noOverflow: document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2,
      navLinks: document.querySelectorAll('.page__content nav.thesis-series-nav a').length,
      figures: [...document.querySelectorAll('.page__content figure.post3-figure img.post3-theme-image')]
        .every((image) => image.currentSrc.includes('-light-mobile.svg')
          && image.complete && image.naturalWidth > 0)
    }), { locale, kind, status: response?.status() || 0 });
  } finally { await context.close(); }
}

async function inspectPrint(browser, config, locale, kind, baseUrl) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route(config, locale, kind), { waitUntil: 'domcontentloaded' });
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
  const config = configs[number];
  if (!config) throw new Error(`unknown thesis post: ${number}`);
  const args = process.argv.slice(2);
  const fixture = option(args, '--fixture');
  if (fixture) return runFixture(fixture);
  const artifactRoot = option(args, '--artifact-root');
  if (!artifactRoot) {
    console.error(JSON.stringify({ status: 'ERROR', error: '--artifact-root is required for an artifact-bound PASS' }));
    process.exitCode = 2;
    return;
  }
  if (!existsSync(artifactRoot)) {
    console.error(JSON.stringify({ status: 'ERROR', error: `artifact root does not exist: ${artifactRoot}` }));
    process.exitCode = 2;
    return;
  }
  const manifestFixture = option(args, '--manifest-fixture');
  if (manifestFixture) {
    if (number !== 4 || manifestFixture !== 'missing-csv') {
      console.error(JSON.stringify({ status: 'ERROR', error: `unknown manifest fixture: ${manifestFixture}` }));
      process.exitCode = 2;
      return;
    }
    const baseline = manifestBinding(number, artifactRoot);
    const scratch = mkdtempSync(resolve(tmpdir(), 'thesis-manifest-'));
    const folder = 'assets/images/tesis-post4';
    const omitted = 'selection-ladder-data.csv';
    try {
      mkdirSync(resolve(scratch, folder), { recursive: true });
      const names = JSON.parse(readFileSync(resolve(siteRoot, folder, 'manifest.json'), 'utf8'))
        .files.map((entry) => entry.path).concat('manifest.json');
      for (const name of names.filter((entry) => entry !== omitted))
        symlinkSync(resolve(artifactRoot, folder, name), resolve(scratch, folder, name));
      const mutated = manifestBinding(number, scratch);
      const discriminates = baseline.valid && !mutated.valid && mutated.structureValid
        && mutated.manifestBound && mutated.mismatches.length === 0
        && mutated.artifactMismatches.length === 1 && mutated.artifactMismatches[0] === omitted;
      console.log(JSON.stringify({ status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE',
        manifestFixture, baseline, mutated, omitted }));
      process.exitCode = discriminates ? 1 : 2;
    } finally { rmSync(scratch, { recursive: true, force: true }); }
    return;
  }
  const baseUrl = (option(args, '--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
  const requestedLanguage = option(args, '--lang');
  if (requestedLanguage && !['es', 'en'].includes(requestedLanguage)) {
    console.error(JSON.stringify({ status: 'ERROR', error: `unknown language: ${requestedLanguage}` }));
    process.exitCode = 2;
    return;
  }
  const locales = requestedLanguage ? [requestedLanguage] : ['es', 'en'];
  const liveFixture = option(args, '--live-fixture');
  if (liveFixture && !['missing-annex', 'overflow'].includes(liveFixture)) {
    console.error(JSON.stringify({ status: 'ERROR', error: `unknown live fixture: ${liveFixture}` }));
    process.exitCode = 2;
    return;
  }
  const receiptPath = option(args, '--receipt');
  const screenshotDir = option(args, '--screenshot-dir');
  const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
    || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
  if (!existsSync(playwrightPath)) {
    console.error(JSON.stringify({ status: 'ERROR', error: `Playwright not found at ${playwrightPath}` }));
    process.exitCode = 2;
    return;
  }
  const playwright = createRequire(import.meta.url)(playwrightPath);
  const browserExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
    || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);
  const browser = await playwright.chromium.launch({ headless: true,
    ...(browserExecutable ? { executablePath: browserExecutable } : {}), args: ['--no-sandbox'] });
  if (liveFixture) {
    try {
      const kind = liveFixture === 'missing-annex' ? 'annex' : 'article';
      const viewport = { width: 390, height: 844 };
      const baseline = await inspectPage(browser, config, 'es', kind, 'light', viewport,
        baseUrl, artifactRoot, null);
      const mutated = await inspectPage(browser, config, 'es', kind, 'light', viewport,
        baseUrl, artifactRoot, null, liveFixture);
      const expected = liveFixture === 'missing-annex' ? 'route-artifact-binding' : 'document-overflow';
      const discriminates = baseline.failures.length === 0 && mutated.failures.includes(expected)
        && (liveFixture === 'missing-annex' ? mutated.httpStatus === 404 : mutated.documentOverflow);
      console.log(JSON.stringify({ status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE',
        liveFixture, baseline: { httpStatus: baseline.httpStatus, failures: baseline.failures,
          tableCount: baseline.tableCount, tableWrappersValid: baseline.tableWrappersValid,
          tableHeadersScoped: baseline.tableHeadersScoped, sourceFresh: baseline.sourceFresh },
        mutated: { httpStatus: mutated.httpStatus, failures: mutated.failures,
          documentOverflow: mutated.documentOverflow }, expected }));
      process.exitCode = discriminates ? 1 : 2;
    } finally { await browser.close(); }
    return;
  }
  const rows = [], noJs = [], print = [];
  try {
    for (const locale of locales) for (const kind of ['article', 'annex']) {
      for (const theme of themes) for (const viewport of viewports)
        rows.push(await inspectPage(browser, config, locale, kind, theme, viewport,
          baseUrl, artifactRoot, screenshotDir));
      noJs.push(await inspectNoJs(browser, config, locale, kind, baseUrl));
      print.push(await inspectPrint(browser, config, locale, kind, baseUrl));
    }
  } finally { await browser.close(); }
  const groups = new Map();
  for (const row of rows.filter((entry) => entry.theme === 'light' && entry.viewportWidth === 1440)) {
    const group = groups.get(row.locale) || { figures: 0, tables: 0, referenceKeys: new Set() };
    group.figures += row.figureCount;
    group.tables += row.tableCount;
    row.referenceKeys.forEach((key) => group.referenceKeys.add(key));
    groups.set(row.locale, group);
  }
  const groupFailures = [...groups].filter(([, group]) => group.figures !== config.totalFigures
    || group.tables !== config.totalTables || group.referenceKeys.size !== config.referenceKeys)
    .map(([locale, group]) => ({ locale, figures: group.figures, tables: group.tables,
      references: group.referenceKeys.size }));
  const noJsFailures = noJs.filter((row) => row.httpStatus !== 200 || !row.noOverflow
    || row.navLinks !== 4 || !row.figures);
  const printFailures = print.filter((row) => row.httpStatus !== 200 || !row.figuresVisible);
  const cssArtifact = resolve(artifactRoot, 'assets/css/main.css');
  const cssResponse = await fetch(`${baseUrl}/assets/css/main.css`);
  const cssServed = cssResponse.ok ? Buffer.from(await cssResponse.arrayBuffer()) : null;
  const cssBound = Boolean(cssServed && existsSync(cssArtifact)
    && sha256(cssServed) === sha256(readFileSync(cssArtifact)));
  const visualManifest = manifestBinding(number, artifactRoot);
  const status = rows.some((row) => row.failures.length) || noJsFailures.length
    || printFailures.length || groupFailures.length || !cssBound || !visualManifest.valid ? 'FAIL' : 'PASS';
  const payload = { status, post: number, locales, contractVersion: 'thesis-series-split-v1',
    testedAt: new Date().toISOString(), baseUrl, artifactRoot, cssBound, visualManifest,
    rows, noJs, print, groupFailures, noJsFailures, printFailures };
  if (receiptPath) {
    mkdirSync(dirname(resolve(receiptPath)), { recursive: true });
    writeFileSync(receiptPath, `${JSON.stringify(payload, null, 2)}\n`);
  }
  console.log(JSON.stringify(args.includes('--summary') ? {
    status, post: number, locales, rows: rows.length, failedRows: rows.filter((row) => row.failures.length).length,
    rowFailures: rows.filter((row) => row.failures.length).map((row) => ({
      route: row.route, theme: row.theme, width: row.viewportWidth, failures: row.failures
    })),
    groupFailures, noJsFailures, printFailures, cssBound, visualManifest
  } : payload));
  process.exitCode = status === 'PASS' ? 0 : 1;
}
