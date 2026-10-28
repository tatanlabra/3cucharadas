#!/usr/bin/env node

import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const valueAfter = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};

const baseUrl = (valueAfter('--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
const screenshotDir = valueAfter('--screenshot-dir') || '/tmp/thesis-post3-browser-gate';
const artifactRoot = valueAfter('--artifact-root');
const fixture = valueAfter('--fixture');
const receiptPath = valueAfter('--receipt');
const summaryOnly = args.includes('--summary');
const tolerance = 2;

const routes = {
  es: '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/',
  en: '/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/'
};
const titles = {
  es: 'Extender mi tesis en 3 cucharadas (parte III)',
  en: 'Extending my thesis in three spoonfuls (part III)'
};
const headingNeedles = {
  es: ['Cucharada 1', 'Cucharada 2', '¿Estamos comparando peras con peras?', 'Educación superior: una pregunta que queda abierta', 'Cucharada 3', 'Referencias'],
  en: ['Spoonful 1', 'Spoonful 2', 'Are we comparing like with like?', 'Higher education: an open question', 'Spoonful 3', 'References']
};
const viewports = [
  { width: 320, height: 800 },
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 1440, height: 1000 }
];
const themes = ['light', 'academic-night'];

function evaluate(row) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('route-not-200');
  if (!row.titleMatches) failures.push('wrong-title');
  if (!row.headingsPresent) failures.push('missing-structure');
  if (row.documentOverflow) failures.push('document-overflow');
  if (row.bodyFontPx < 16) failures.push('body-font-too-small');
  if (row.tableMinFontPx < 13) failures.push('table-font-too-small');
  if (row.referenceMinFontPx < 14) failures.push('references-font-too-small');
  if (row.figureCount !== 4 || !row.figuresValid) failures.push('figure-contract');
  if (!row.figureThemeValid) failures.push('figure-theme-contract');
  if (!row.visualIdentityValid) failures.push('visual-identity-contract');
  if (!row.dataFallbackValid) failures.push('figure-data-fallback');
  if (!row.keyboardFocusValid) failures.push('figure-keyboard-focus');
  if (row.svgTextMinPx < 9) failures.push('svg-text-too-small');
  if (row.tableCount !== 7 || !row.tableWrappersValid || !row.tableHeadersScoped) failures.push('table-contract');
  if (!row.idsUnique || !row.imagesNamed) failures.push('basic-a11y');
  if (!row.higherEducationAgenda) failures.push('higher-education-agenda');
  if (!row.noHigherEducationBlocker) failures.push('higher-education-blocker');
  if (!row.historicalCapsule) failures.push('historical-capsule-contract');
  if (!row.publicContentSafe) failures.push('public-content-safety');
  if (!row.themeSurfaceValid) failures.push('theme-surface');
  if (!row.editorialGeometryValid) failures.push('editorial-width-mismatch');
  if (!row.darkPanelToneValid) failures.push('dark-panel-tone-mismatch');
  if (row.criticalErrors.length) failures.push('critical-resource-or-console-error');
  return failures;
}

function runFixture(name) {
  const baseline = {
    httpStatus: 200,
    titleMatches: true,
    headingsPresent: true,
    documentOverflow: false,
    bodyFontPx: 18,
    tableMinFontPx: 14,
    referenceMinFontPx: 15,
    tableCount: 7,
    figureCount: 4,
    figuresValid: true,
    figureThemeValid: true,
    visualIdentityValid: true,
    dataFallbackValid: true,
    keyboardFocusValid: true,
    svgTextMinPx: 10,
    tableWrappersValid: true,
    tableHeadersScoped: true,
    idsUnique: true,
    imagesNamed: true,
    higherEducationAgenda: true,
    noHigherEducationBlocker: true,
    historicalCapsule: true,
    publicContentSafe: true,
    themeSurfaceValid: true,
    editorialGeometryValid: true,
    darkPanelToneValid: true,
    criticalErrors: []
  };
  const mutations = {
    overflow: { documentOverflow: true },
    'missing-figure': { figureCount: 3 },
    'wrong-theme': { figureThemeValid: false },
    'zero-size': { figuresValid: false },
    'private-content': { publicContentSafe: false },
    'missing-table': { tableCount: 6 },
    'missing-visual-identity': { visualIdentityValid: false },
    'mismatched-editorial-width': { editorialGeometryValid: false },
    'off-theme-panel': { darkPanelToneValid: false },
    'missing-he-agenda': { higherEducationAgenda: false },
    'he-blocker': { noHigherEducationBlocker: false }
  };
  const expected = {
    overflow: ['document-overflow'],
    'missing-figure': ['figure-contract'],
    'wrong-theme': ['figure-theme-contract'],
    'zero-size': ['figure-contract'],
    'private-content': ['public-content-safety'],
    'missing-table': ['table-contract'],
    'missing-visual-identity': ['visual-identity-contract'],
    'mismatched-editorial-width': ['editorial-width-mismatch'],
    'off-theme-panel': ['dark-panel-tone-mismatch'],
    'missing-he-agenda': ['higher-education-agenda'],
    'he-blocker': ['higher-education-blocker']
  };
  if (!mutations[name]) {
    console.error(JSON.stringify({ status: 'ERROR', error: `unknown fixture: ${name}` }));
    process.exit(2);
  }
  const failures = evaluate({ ...baseline, ...mutations[name] });
  const exact = JSON.stringify(failures) === JSON.stringify(expected[name]);
  console.log(JSON.stringify({
    status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE',
    fixture: name,
    failures,
    expected: expected[name]
  }));
  process.exit(exact ? 1 : 2);
}

if (fixture) runFixture(fixture);

if (!artifactRoot) {
  console.error(JSON.stringify({ status: 'ERROR', error: '--artifact-root is required for an artifact-bound PASS' }));
  process.exit(2);
}
if (!existsSync(artifactRoot)) {
  console.error(JSON.stringify({ status: 'ERROR', error: `artifact root does not exist: ${artifactRoot}` }));
  process.exit(2);
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(scriptDir, '..');
const workspaceRoot = resolve(siteRoot, '../..');
const tokenPath = resolve(siteRoot, 'assets/data/tesis-post3/visual_identity_tokens_v1.json');
const tokenDocument = JSON.parse(readFileSync(tokenPath, 'utf8'));
const hexToRgb = (hex) => `rgb(${[1, 3, 5].map((index) => parseInt(hex.slice(index, index + 2), 16)).join(', ')})`;
const colorNames = ['canvas', 'surface', 'ink', 'muted', 'grid', 'accent', 'focus', 'positive', 'negative', 'warning'];
const seriesNames = ['one', 'two', 'three', 'four', 'five', 'six'];
const expectedIdentity = Object.fromEntries(['light', 'dark'].map((mode) => [mode, {
  surface: hexToRgb(tokenDocument.color[mode].surface.$value.hex),
  focus: tokenDocument.color[mode].focus.$value.hex,
  variables: Object.fromEntries([
    ...colorNames.map((name) => [`--c3-viz-${name}`, tokenDocument.color[mode][name].$value.hex]),
    ...seriesNames.map((name) => [`--c3-viz-series-${name}`, tokenDocument.color[mode].series[name].$value.hex])
  ])
}]));
const sha256 = (buffer) => createHash('sha256').update(buffer).digest('hex');

const matchCount = (text, pattern) => [...text.matchAll(pattern)].length;
const criticalClaimCounts = (text, locale) => ({
  progression: matchCount(text, locale === 'es' ? /5,29/g : /5\.29/g),
  lowerBound: matchCount(text, locale === 'es' ? /(?:−|-|menos\s+)1,15/g : /(?:−|-|minus\s+)1\.15/g),
  upperBound: matchCount(text, locale === 'es' ? /10,98/g : /10\.98/g)
});

async function bindServedArtifact() {
  const bindings = [];
  for (const [locale, route] of Object.entries(routes)) {
    const relative = route.replace(/^\/+|\/+$/g, '');
    const artifactHtmlPath = resolve(artifactRoot, relative, 'index.html');
    const sourcePostPath = resolve(
      siteRoot,
      locale === 'es'
        ? '_posts/2026-10-23-costos-cierre-escolar-trayectorias.md'
        : '_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md'
    );
    const response = await fetch(`${baseUrl}${route}`);
    const served = response.ok ? await response.text() : '';
    const artifact = existsSync(artifactHtmlPath) ? readFileSync(artifactHtmlPath, 'utf8') : '';
    const source = readFileSync(sourcePostPath, 'utf8');
    const marker = '<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->';
    const readiness = '<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->';
    const sourceClaims = criticalClaimCounts(source, locale);
    const servedClaims = criticalClaimCounts(served, locale);
    bindings.push({
      locale,
      route,
      artifactHtmlPath,
      httpStatus: response.status,
      servedSha256: served ? sha256(Buffer.from(served)) : null,
      artifactSha256: artifact ? sha256(Buffer.from(artifact)) : null,
      exactArtifact: Boolean(served && artifact && served === artifact),
      stateMarker: served.includes(marker),
      readinessMarker: served.includes(readiness),
      sourceClaims,
      servedClaims,
      criticalClaimsBound: JSON.stringify(sourceClaims) === JSON.stringify(servedClaims)
        && sourceClaims.progression > 0
        && sourceClaims.lowerBound > 0
        && sourceClaims.upperBound > 0
    });
  }
  return bindings;
}

function sourceHashes() {
  const paths = [
    'assets/data/tesis-post3/visual_identity_tokens_v1.json',
    '_sass/_post3-data-viz-tokens.scss',
    'assets/css/main.scss',
    '_posts/2026-10-23-costos-cierre-escolar-trayectorias.md',
    '_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md',
    'scripts/build_post3_visual_tokens.py',
    'scripts/verify_thesis_post3_browser.mjs',
    'assets/images/tesis-post3/manifest.json'
  ];
  const files = paths.map((path) => ({ path, sha256: sha256(readFileSync(resolve(siteRoot, path))) }));
  const externalScripts = [
    'incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py',
    'penta-agent/skills/3cucharadas-visualizacion-datos/scripts/dtcg_format.py',
    'penta-agent/skills/3cucharadas-visualizacion-datos/assets/dtcg/2025.10/format.json'
  ];
  for (const path of externalScripts) files.push({ path, sha256: sha256(readFileSync(resolve(workspaceRoot, path))) });
  const manifest = JSON.parse(readFileSync(resolve(siteRoot, 'assets/images/tesis-post3/manifest.json'), 'utf8'));
  const mismatches = [];
  for (const entry of manifest.files) {
    if (basename(entry.path) !== entry.path) throw new Error(`unsafe asset path: ${entry.path}`);
    const path = `assets/images/tesis-post3/${entry.path}`;
    const actual = sha256(readFileSync(resolve(siteRoot, path)));
    files.push({ path, sha256: actual });
    if (actual !== entry.sha256) mismatches.push(path);
  }
  return { files, assetCount: manifest.files.length, mismatches };
}

const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
if (!existsSync(playwrightPath)) {
  console.error(JSON.stringify({ status: 'ERROR', error: `Playwright not found at ${playwrightPath}` }));
  process.exit(2);
}
const playwright = createRequire(import.meta.url)(playwrightPath);
const browserExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);

async function inspectPage(browser, locale, route, theme, viewport) {
  const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
  await context.addInitScript(
    (selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme),
    theme
  );
  const page = await context.newPage();
  const criticalErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') criticalErrors.push(`console:${message.text()}`);
  });
  page.on('requestfailed', (request) => {
    if (request.url().startsWith(baseUrl)) {
      criticalErrors.push(`request:${request.url()}:${request.failure()?.errorText || 'failed'}`);
    }
  });
  try {
    const response = await page.goto(baseUrl + route, {
      waitUntil: 'domcontentloaded',
      timeout: 30_000
    });
    await page.evaluate(() => document.fonts.ready);
    const figures = page.locator('figure.post3-figure');
    for (let index = 0; index < await figures.count(); index += 1) {
      await figures.nth(index).scrollIntoViewIfNeeded();
      await figures.nth(index).locator('img.post3-theme-image').waitFor({ state: 'visible' });
      await figures.nth(index).locator('img.post3-theme-image').evaluate((image) => {
        image.loading = 'eager';
        if (!image.complete || image.naturalWidth === 0) {
          return new Promise((resolveImage) => {
            image.addEventListener('load', resolveImage, { once: true });
            image.addEventListener('error', resolveImage, { once: true });
          });
        }
        return null;
      });
    }
    const keyboardRows = [];
    for (let index = 0; index < await figures.count(); index += 1) {
      const figure = figures.nth(index);
      const figureLink = figure.locator('a.post3-theme-link');
      await figureLink.focus();
      const focusOutlineVisible = await figureLink.evaluate((link) => {
        const style = getComputedStyle(link);
        return document.activeElement === link
          && style.outlineStyle !== 'none'
          && parseFloat(style.outlineWidth) >= 3;
      });
      await page.keyboard.press('Tab');
      const tabMovesToFallback = await page.evaluate((figureId) =>
        document.activeElement?.closest('figure')?.id === figureId
        && Boolean(document.activeElement?.closest('.figure-data')), await figure.getAttribute('id'));
      keyboardRows.push({ focusOutlineVisible, tabMovesToFallback });
    }

    const row = await page.evaluate(async (payload) => {
      const article = document.querySelector('.page__content');
      const articleBox = article?.getBoundingClientRect();
      const headingText = [...(article?.querySelectorAll('h2, h3') || [])]
        .map((node) => node.textContent?.trim() || '');
      const tables = [...(article?.querySelectorAll('table') || [])];
      const wrappers = [...(article?.querySelectorAll('.tabla-desliza') || [])];
      const anchorParagraph = article?.querySelector(':scope > p:not(.table-caption)');
      const anchorParagraphBox = anchorParagraph?.getBoundingClientRect();
      const references = [...(article?.querySelectorAll('.post-references p') || [])];
      const tableFonts = tables.flatMap((table) => [...table.querySelectorAll('th, td')]
        .map((cell) => parseFloat(getComputedStyle(cell).fontSize)));
      const referenceFonts = references.map((node) => parseFloat(getComputedStyle(node).fontSize));
      const figureRows = await Promise.all([...(article?.querySelectorAll('figure.post3-figure') || [])].map(async (figure) => {
        const image = figure.querySelector('img.post3-theme-image');
        const box = figure.getBoundingClientRect();
        const imageBox = image?.getBoundingClientRect();
        const style = getComputedStyle(figure);
        const dataLinks = [...figure.querySelectorAll('.figure-data a')];
        const dataResponses = await Promise.all(dataLinks.map(async (link) => {
          try {
            const response = await fetch(link.href);
            const text = await response.text();
            const semanticColumns = ['reading_limit_es', 'reading_limit_en'];
            if (link.pathname.endsWith('sample-flow-data.csv')) {
              semanticColumns.push('sample_scope_es', 'sample_scope_en');
            } else if (link.pathname.endsWith('post-pilot-reestimation-data.csv')) {
              semanticColumns.push('uncertainty_type_es', 'uncertainty_type_en', 'sample_scope_es', 'sample_scope_en');
            } else if (link.pathname.endsWith('missingness-bounds-data.csv')) {
              semanticColumns.push('uncertainty_type_es', 'uncertainty_type_en', 'sample_scope_es', 'sample_scope_en');
            } else if (link.pathname.endsWith('cohort-series-infographic-data.csv')) {
              semanticColumns.push('sample_scope_es', 'sample_scope_en');
            } else if (link.pathname.endsWith('territorial-audit-data.csv')) {
              semanticColumns.push('maximum_automatic_level', 'blocking_gaps');
            }
            return response.ok && semanticColumns.every((column) => text.split('\n', 1)[0].includes(column));
          } catch {
            return false;
          }
        }));
        let svgRenderedMinPx = 0;
        try {
          const svg = await (await fetch(image.currentSrc)).text();
          const viewBox = svg.match(/viewBox="([^"]+)"/);
          const viewBoxWidth = viewBox
            ? Number(viewBox[1].trim().split(/\s+/)[2])
            : 0;
          const declared = [...svg.matchAll(/font-size:\s*([0-9.]+)px/g)]
            .map((match) => Number(match[1]));
          if (viewBoxWidth > 0 && declared.length && imageBox) {
            svgRenderedMinPx = Math.min(...declared) * imageBox.width / viewBoxWidth;
          }
        } catch {
          svgRenderedMinPx = 0;
        }
        return {
          src: image?.currentSrc || '',
          complete: image?.complete === true && image?.naturalWidth > 0 && image?.naturalHeight > 0,
          named: Boolean(image?.getAttribute('alt')?.trim()),
          sized: Boolean(imageBox && imageBox.width > 0 && imageBox.height > 180),
          insideArticle: Boolean(articleBox)
            && box.left >= articleBox.left - payload.tolerance
            && box.right <= articleBox.right + payload.tolerance,
          hasCaption: Boolean(figure.querySelector('figcaption .figure-source')),
          identityClass: figure.classList.contains('data-visualization'),
          identitySurface: style.backgroundColor,
          identityCanvasToken: style.getPropertyValue('--c3-viz-canvas').trim().toLowerCase(),
          identitySurfaceToken: style.getPropertyValue('--c3-viz-surface').trim().toLowerCase(),
          identityFont: style.fontFamily,
          identityFocus: style.getPropertyValue('--c3-viz-focus').trim(),
          identityVariablesValid: Object.entries(payload.expectedIdentity.variables).every(
            ([name, hex]) => style.getPropertyValue(name).trim().toLowerCase() === hex),
          dataLinks: dataLinks.length,
          dataResponses,
          svgRenderedMinPx
        };
      }));
      const body = article?.innerText || '';
      const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
      const rootBackground = getComputedStyle(document.documentElement).backgroundColor;
      const rootStyle = getComputedStyle(document.documentElement);
      const nightBackground = rootStyle.getPropertyValue('--night-bg').trim().toLowerCase();
      const nightLayer = rootStyle.getPropertyValue('--night-layer').trim().toLowerCase();
      const isDarkSurface = /rgb\((1[0-9]|2[0-9]|3[0-9]),/.test(rootBackground);
      const isLightSurface = /rgb\((24[0-9]|25[0-5]),/.test(rootBackground);
      const expectedTheme = payload.theme === 'academic-night' ? '-dark' : '-light';
      const expectedLayout = payload.viewport.width < 768 ? '-mobile.svg' : '.svg';
      return {
        locale: payload.locale,
        theme: payload.theme,
        viewportWidth: payload.viewport.width,
        httpStatus: payload.httpStatus,
        titleMatches: document.title.includes(payload.title),
        headingsPresent: payload.headings.every((needle) =>
          headingText.some((heading) => heading.includes(needle))),
        documentOverflow: document.documentElement.scrollWidth
          > document.documentElement.clientWidth + payload.tolerance,
        bodyFontPx: article ? parseFloat(getComputedStyle(article).fontSize) : 0,
        tableMinFontPx: tableFonts.length ? Math.min(...tableFonts) : 0,
        referenceMinFontPx: referenceFonts.length ? Math.min(...referenceFonts) : 0,
        tableCount: tables.length,
        figureCount: figureRows.length,
        figuresValid: figureRows.every((figure) =>
          figure.complete && figure.named && figure.sized && figure.insideArticle && figure.hasCaption),
        figureThemeValid: figureRows.every((figure) =>
          figure.src.includes(expectedTheme) && figure.src.endsWith(expectedLayout)),
        visualIdentityValid: figureRows.every((figure) =>
          figure.identityClass
          && figure.identityFont.includes('Fira Sans')
          && figure.identityVariablesValid
          && (payload.theme === 'academic-night'
            || figure.identitySurface === payload.expectedIdentity.surface)
          && figure.identityFocus === payload.expectedIdentity.focus),
        dataFallbackValid: figureRows.map((figure) => figure.dataLinks).join(',') === '1,2,1,1'
          && figureRows.every((figure) => figure.dataResponses.every(Boolean)),
        keyboardFocusValid: payload.keyboardRows.length === figureRows.length
          && payload.keyboardRows.every((item) => item.focusOutlineVisible && item.tabMovesToFallback),
        svgTextMinPx: Math.min(...figureRows.map((figure) => figure.svgRenderedMinPx)),
        tableWrappersValid: wrappers.length === tables.length && wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return wrapper.getAttribute('role') === 'region'
            && wrapper.getAttribute('tabindex') === '0'
            && Boolean(wrapper.getAttribute('aria-label'))
            && ['auto', 'scroll'].includes(getComputedStyle(wrapper).overflowX)
            && box.left >= -payload.tolerance
            && box.right <= document.documentElement.clientWidth + payload.tolerance;
        }),
        tableHeadersScoped: tables.every((table) => [...table.querySelectorAll('thead th')]
          .every((cell) => cell.getAttribute('scope') === 'col')),
        idsUnique: new Set(ids).size === ids.length,
        imagesNamed: [...(article?.querySelectorAll('img') || [])]
          .every((image) => Boolean(image.getAttribute('alt')?.trim())),
        higherEducationAgenda: payload.locale === 'es'
          ? body.includes('Educación superior: una pregunta que queda abierta')
            && body.includes('aquí no se estiman ni se sugieren efectos postsecundarios')
            && body.includes('no condiciona la publicación')
          : body.includes('Higher education: an open question')
            && body.includes('neither estimates nor suggests postsecondary effects')
            && body.includes('does not condition publication'),
        noHigherEducationBlocker: !/BLOCKED_MISSING_INDIVIDUAL_SIES|no está listo para publicación|not publication-ready|required outcome|resultado obligatorio/i.test(body),
        historicalCapsule: payload.locale === 'es'
          ? ['+1,46', '682.217', '+1,74', '2.361', '+1,08', '906.629', 'no comparables']
            .every((needle) => body.includes(needle))
          : ['+1.46', '682,217', '+1.74', '2,361', '+1.08', '906,629', 'not comparable']
            .every((needle) => body.includes(needle)),
        publicContentSafe: !/(?:\/home\/|\/mnt\/|\bMRUN\s*\d|\bRBD\s*\d)/i.test(body),
        themeSurfaceValid: payload.theme === 'academic-night' ? isDarkSurface : isLightSurface,
        editorialGeometryValid: Boolean(anchorParagraphBox) && wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return Math.abs(box.left - anchorParagraphBox.left) <= payload.tolerance
            && Math.abs(box.width - anchorParagraphBox.width) <= payload.tolerance;
        }),
        darkPanelToneValid: payload.theme !== 'academic-night' || figureRows.every((figure) =>
          figure.identityCanvasToken === nightBackground
          && figure.identitySurfaceToken === nightLayer
          && figure.identitySurface === rootBackground),
        criticalErrors: payload.errors.filter((error) => !error.includes('favicon'))
      };
    }, {
      locale,
      theme,
      viewport,
      httpStatus: response?.status() || 0,
      title: titles[locale],
      headings: headingNeedles[locale],
      tolerance,
      errors: criticalErrors,
      keyboardRows,
      expectedIdentity: expectedIdentity[theme === 'academic-night' ? 'dark' : 'light']
    });
    row.failures = evaluate(row);
    if ([390, 1440].includes(viewport.width)) {
      mkdirSync(screenshotDir, { recursive: true });
      await page.screenshot({
        path: `${screenshotDir}/chromium-${locale}-${theme}-${viewport.width}.png`,
        fullPage: true
      });
    }
    return row;
  } finally {
    await context.close();
  }
}

async function inspectNoJs(browser, locale, route) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    javaScriptEnabled: false
  });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    const figures = page.locator('figure.post3-figure');
    for (let index = 0; index < await figures.count(); index += 1) {
      await figures.nth(index).scrollIntoViewIfNeeded();
    }
    return await page.evaluate((payload) => {
      const rows = [...document.querySelectorAll('figure.post3-figure img.post3-theme-image')];
      return {
        locale: payload.locale,
        httpStatus: payload.httpStatus,
        figureCount: rows.length,
        lightMobileFallbacks: rows.every((image) =>
          image.currentSrc.includes('-light-mobile.svg')
          && image.complete && image.naturalWidth > 0 && image.naturalHeight > 0),
        documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
        tableCount: document.querySelectorAll('.page__content table').length
      };
    }, { locale, httpStatus: response?.status() || 0 });
  } finally {
    await context.close();
  }
}

async function inspectPrint(browser, locale, route, theme) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  await context.addInitScript(
    (selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme),
    theme
  );
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelectorAll('figure.post3-figure').length === 4);
    const printFigures = page.locator('figure.post3-figure');
    for (let index = 0; index < await printFigures.count(); index += 1) {
      await printFigures.nth(index).scrollIntoViewIfNeeded();
    }
    await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
    await page.waitForFunction(() => [...document.querySelectorAll('img.post3-theme-image')]
      .every((image) => image.getAttribute('src')?.includes('-light')
        && image.getAttribute('srcset')?.includes('-light')));
    await page.waitForFunction(() => [...document.querySelectorAll('img.post3-theme-image')]
      .every((image) => image.complete && image.naturalWidth > 0 && image.currentSrc.includes('-light')));
    await page.emulateMedia({ media: 'print', colorScheme: 'light' });
    const rows = await page.locator('figure.post3-figure').evaluateAll((figures) => figures.map((figure) => {
      const image = figure.querySelector('img.post3-theme-image');
      const style = getComputedStyle(figure);
      const imageStyle = image ? getComputedStyle(image) : null;
      return {
        visible: style.display !== 'none' && style.visibility !== 'hidden',
        imageVisible: Boolean(imageStyle)
          && imageStyle.display !== 'none' && imageStyle.visibility !== 'hidden',
        width: figure.getBoundingClientRect().width,
        backgroundColor: style.backgroundColor,
        color: style.color,
        currentSrc: image?.currentSrc || '',
        lightVariant: Boolean(image?.currentSrc.includes('-light'))
      };
    }));
    mkdirSync(screenshotDir, { recursive: true });
    if (locale === 'es' && theme === 'light') {
      await page.pdf({ path: `${screenshotDir}/chromium-post3-es-print.pdf`, format: 'A4', printBackground: true });
    }
    return {
      locale,
      theme,
      httpStatus: response?.status() || 0,
      figureCount: rows.length,
      figuresVisible: rows.every((row) => row.visible && row.imageVisible && row.width > 0),
      lightVariants: rows.every((row) => row.lightVariant),
      printPaletteValid: rows.every((row) =>
        row.backgroundColor === 'rgb(255, 255, 255)' && row.color === 'rgb(0, 0, 0)')
    };
  } finally {
    await context.close();
  }
}

async function inspectTextResize(browser, locale, route) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    const baseline = await page.evaluate(() => {
      const article = document.querySelector('.page__content');
      if (!article) return [];
      return [...article.querySelectorAll('*')]
        .filter((element) => !element.closest('.sr-only'))
        .filter((element) => [...element.childNodes]
          .some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim()))
        .filter((element) => {
          const style = getComputedStyle(element);
          return style.display !== 'none' && style.visibility !== 'hidden';
        })
        .map((element, index) => {
          element.dataset.textResizeProbe = String(index);
          return {
            index,
            fontPx: parseFloat(getComputedStyle(element).fontSize)
          };
        });
    });
    await page.evaluate((rows) => {
      for (const row of rows) {
        const element = document.querySelector(`[data-text-resize-probe="${row.index}"]`);
        element?.style.setProperty('font-size', `${row.fontPx * 2}px`, 'important');
      }
    }, baseline);
    return await page.evaluate((payload) => {
      const figures = [...document.querySelectorAll('figure.post3-figure')];
      const wrappers = [...document.querySelectorAll('.page__content .tabla-desliza')];
      const article = document.querySelector('.page__content');
      const textRows = payload.baseline.map((row) => {
        const element = document.querySelector(`[data-text-resize-probe="${row.index}"]`);
        const style = element ? getComputedStyle(element) : null;
        const clippedHorizontally = Boolean(element && style)
          && ['hidden', 'clip'].includes(style.overflowX)
          && element.scrollWidth > element.clientWidth + 2;
        const clippedVertically = Boolean(element && style)
          && ['hidden', 'clip'].includes(style.overflowY)
          && element.scrollHeight > element.clientHeight + 2;
        return {
          scale: style ? parseFloat(style.fontSize) / row.fontPx : 0,
          clipped: clippedHorizontally || clippedVertically
        };
      });
      return {
        locale: payload.locale,
        httpStatus: payload.httpStatus,
        textNodesMeasured: textRows.length,
        minimumTextScale: Math.min(...textRows.map((row) => row.scale)),
        clippedTextElements: textRows.filter((row) => row.clipped).length,
        figureCount: figures.length,
        tableCount: document.querySelectorAll('.page__content table').length,
        figuresVisible: figures.every((figure) => {
          const box = figure.getBoundingClientRect();
          return box.width > 0 && box.height > 0;
        }),
        contentPresent: Boolean(article?.innerText.includes(payload.locale === 'es'
          ? 'seguir trayectorias cambia la pregunta pública'
          : 'following trajectories changes the policy question')),
        documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
        wrappersContained: wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return box.left >= -2 && box.right <= document.documentElement.clientWidth + 2;
        })
      };
    }, { locale, httpStatus: response?.status() || 0, baseline });
  } finally {
    await context.close();
  }
}

async function inspectPreference(browser, locale, route, theme, preference) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    ...(preference === 'forced-colors' ? { forcedColors: 'active' } : { contrast: 'more' })
  });
  await context.addInitScript(
    (selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme),
    theme
  );
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelectorAll('figure.post3-figure').length === 4);
    await page.locator('figure.post3-figure a.post3-theme-link').first().focus();
    return await page.evaluate((payload) => {
      const figures = [...document.querySelectorAll('figure.post3-figure')];
      const links = [...document.querySelectorAll('figure.post3-figure a')];
      const images = [...document.querySelectorAll('figure.post3-figure img.post3-theme-image')];
      const activeStyle = document.activeElement ? getComputedStyle(document.activeElement) : null;
      const preferenceMatches = payload.preference === 'forced-colors'
        ? matchMedia('(forced-colors: active)').matches
        : matchMedia('(prefers-contrast: more)').matches;
      return {
        locale: payload.locale,
        theme: payload.theme,
        preference: payload.preference,
        httpStatus: payload.httpStatus,
        preferenceMatches,
        figureCount: figures.length,
        figuresVisible: figures.every((figure) => {
          const box = figure.getBoundingClientRect();
          const style = getComputedStyle(figure);
          return box.width > 0 && box.height > 0
            && style.display !== 'none' && style.visibility !== 'hidden';
        }),
        strongPanelBorders: figures.every((figure) => {
          const style = getComputedStyle(figure);
          return style.borderTopStyle !== 'none' && parseFloat(style.borderTopWidth) >= 2;
        }),
        noPanelShadows: figures.every((figure) => getComputedStyle(figure).boxShadow === 'none'),
        linksUnderlined: links.length === 9
          && links.every((link) => getComputedStyle(link).textDecorationLine.includes('underline')),
        imagesFramed: payload.preference !== 'forced-colors'
          || images.every((image) => parseFloat(getComputedStyle(image).borderTopWidth) >= 1),
        focusVisible: Boolean(activeStyle)
          && activeStyle.outlineStyle !== 'none'
          && parseFloat(activeStyle.outlineWidth) >= (payload.preference === 'prefers-contrast' ? 4 : 3),
        documentOverflow: document.documentElement.scrollWidth
          > document.documentElement.clientWidth + 2
      };
    }, {
      locale,
      theme,
      preference,
      httpStatus: response?.status() || 0
    });
  } finally {
    await context.close();
  }
}

const launchOptions = { headless: true };
if (browserExecutable) launchOptions.executablePath = browserExecutable;
launchOptions.args = ['--no-sandbox'];
const browser = await playwright.chromium.launch(launchOptions);
const rows = [];
const noJs = [];
const print = [];
const textResize = [];
const preferences = [];
try {
  for (const [locale, route] of Object.entries(routes)) {
    for (const theme of themes) {
      for (const viewport of viewports) {
        rows.push(await inspectPage(browser, locale, route, theme, viewport));
      }
    }
    noJs.push(await inspectNoJs(browser, locale, route));
    for (const theme of themes) {
      print.push(await inspectPrint(browser, locale, route, theme));
      preferences.push(await inspectPreference(browser, locale, route, theme, 'forced-colors'));
      preferences.push(await inspectPreference(browser, locale, route, theme, 'prefers-contrast'));
    }
    textResize.push(await inspectTextResize(browser, locale, route));
  }
} finally {
  await browser.close();
}

const liveFailures = rows.filter((row) => row.failures.length > 0);
const noJsFailures = noJs.filter((row) =>
  row.httpStatus !== 200 || row.figureCount !== 4 || !row.lightMobileFallbacks
  || row.documentOverflow || row.tableCount !== 7);
const printFailures = print.filter((row) =>
  row.httpStatus !== 200 || row.figureCount !== 4 || !row.figuresVisible
  || !row.lightVariants || !row.printPaletteValid);
const textResizeFailures = textResize.filter((row) =>
  row.httpStatus !== 200 || row.textNodesMeasured === 0 || row.minimumTextScale < 1.95
  || row.clippedTextElements !== 0 || row.figureCount !== 4
  || row.tableCount !== 7 || !row.figuresVisible || !row.contentPresent
  || row.documentOverflow || !row.wrappersContained);
const preferenceFailures = preferences.filter((row) =>
  row.httpStatus !== 200 || !row.preferenceMatches || row.figureCount !== 4
  || !row.figuresVisible || !row.strongPanelBorders || !row.noPanelShadows
  || !row.linksUnderlined || !row.imagesFramed || !row.focusVisible
  || row.documentOverflow);
const inputs = sourceHashes();
const artifactBindings = await bindServedArtifact();
const publishedCssResponse = await fetch(`${baseUrl}/assets/css/main.css`);
const publishedCss = publishedCssResponse.ok ? sha256(Buffer.from(await publishedCssResponse.arrayBuffer())) : null;
const artifactCssPath = resolve(artifactRoot, 'assets/css/main.css');
const artifactCss = artifactCssPath && existsSync(artifactCssPath)
  ? sha256(readFileSync(artifactCssPath))
  : null;
const artifactBound = Boolean(artifactCss && publishedCss === artifactCss)
  && artifactBindings.every((binding) => binding.httpStatus === 200
    && binding.exactArtifact
    && binding.stateMarker
    && binding.readinessMarker
    && binding.criticalClaimsBound);
const status = liveFailures.length || noJsFailures.length || printFailures.length
  || textResizeFailures.length || preferenceFailures.length
  || inputs.mismatches.length || !publishedCss || !artifactBound ? 'FAIL' : 'PASS';
const payload = {
  status,
  engine: 'playwright-local-chromium',
  contractVersion: 'post3-visual-ux-v5',
  testedAt: new Date().toISOString(),
  baseUrl,
  inputs: {
    ...inputs,
    publishedCss: { path: '/assets/css/main.css', sha256: publishedCss },
    artifactCss: { path: artifactCssPath, sha256: artifactCss },
    artifactBound,
    artifactBindings
  },
  reflow320: {
    rows: rows.filter((row) => row.viewportWidth === 320).length,
    noDocumentOverflow: rows.filter((row) => row.viewportWidth === 320)
      .every((row) => !row.documentOverflow)
  },
  rows,
  no_js: noJs,
  print,
  text_resize_200: textResize,
  preferences,
  failures: {
    live: liveFailures,
    no_js: noJsFailures,
    print: printFailures,
    text_resize_200: textResizeFailures,
    preferences: preferenceFailures,
    asset_hash_mismatches: inputs.mismatches,
    published_css_missing: !publishedCss,
    artifact_not_bound: !artifactBound
  }
};
if (receiptPath) {
  mkdirSync(dirname(receiptPath), { recursive: true });
  writeFileSync(receiptPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}
console.log(JSON.stringify(summaryOnly ? {
  status,
  engine: payload.engine,
  measuredRows: rows.length,
  noJsRows: noJs.length,
  printRows: print.length,
  textResize200Rows: textResize.length,
  preferenceRows: preferences.length,
  reflow320Rows: rows.filter((row) => row.viewportWidth === 320).length,
  minSvgTextPx: Math.min(...rows.map((row) => row.svgTextMinPx)),
  failureCounts: {
    live: liveFailures.length,
    no_js: noJsFailures.length,
    print: printFailures.length,
    text_resize_200: textResizeFailures.length,
    preferences: preferenceFailures.length,
    asset_hash_mismatches: inputs.mismatches.length,
    published_css_missing: !publishedCss,
    artifact_not_bound: !artifactBound
  }
} : payload, null, 2));
process.exit(status === 'PASS' ? 0 : 1);
