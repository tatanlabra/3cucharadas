#!/usr/bin/env node
import { createRequire } from 'node:module';
import { existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const valueAfter = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};
const baseUrl = (valueAfter('--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
const screenshotDir = valueAfter('--screenshot-dir') || '/tmp/thesis-post2-browser-gate';
const fixture = valueAfter('--fixture');
const summaryOnly = args.includes('--summary');
const tolerance = 2;

const routes = {
  es: '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/',
  en: '/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/'
};
const postIRoutes = {
  es: '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/',
  en: '/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/'
};
const postITitles = {
  es: 'Replicar mi tesis en 3 cucharadas (parte I)',
  en: 'Replicating my thesis in three spoonfuls (part I)'
};
const titles = {
  es: 'Extender mi tesis en 3 cucharadas (parte II)',
  en: 'Extending my thesis in three spoonfuls (part II)'
};
const headingNeedles = {
  es: ['Cucharada 1', 'Cucharada 2', 'Cucharada 3', 'Qué tendría que ocurrir para hablar de causalidad', 'Referencias'],
  en: ['Spoonful 1', 'Spoonful 2', 'Spoonful 3', 'What would need to happen for causal inference', 'References']
};
const viewports = [
  { width: 320, height: 800 },
  { width: 360, height: 800 },
  { width: 430, height: 900 },
  { width: 768, height: 1024 },
  { width: 1280, height: 900 },
  { width: 1440, height: 900 }
];
const themes = ['light', 'academic-night'];

function evaluate(row) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('route-not-200');
  if (!row.titleMatches) failures.push('wrong-title');
  if (!row.headingsPresent) failures.push('missing-structure');
  if (row.documentOverflow) failures.push('document-overflow');
  if (!row.componentInsideArticle) failures.push('component-overflow');
  if (row.bodyFontPx < 16) failures.push('body-font-too-small');
  if (row.tableMinFontPx < 13) failures.push('table-font-too-small');
  if (row.referenceMinFontPx < 14) failures.push('references-font-too-small');
  if (row.viewportWidth >= 1024 && row.proseBlocks < 1) failures.push('prose-measure-empty');
  if (row.viewportWidth >= 1024 && row.proseMaxPx > 720 + tolerance) failures.push('prose-measure-too-wide');
  // El techo de 4.200 es meta editorial flexible (INV-08 del contrato de publicación):
  // superarlo solo avisa, en softWarnings. El piso sí rechaza.
  if (row.wordCount < 3000) failures.push('visible-word-target');
  if (row.retiredComponents !== 0) failures.push('retired-component-present');
  if (row.mapState !== 'ready' || !row.mapLoaded) failures.push('market-map-not-ready');
  if (row.tabCount !== 0 || row.selectedTabCount !== 0 || !row.panelLabelled) failures.push('single-case-contract');
  if (!row.canvasAccessible || !row.attributionPresent) failures.push('map-accessibility');
  if (row.attributionCount !== 1 || !row.attributionIncludesOsm) failures.push('map-attribution-contract');
  if (row.staticCaseCount !== 1 || !row.staticCasesHiddenWhenReady) failures.push('static-case-contract');
  if (row.visibleStaticSheetLinks !== 0 || row.fallbackImages !== 0) failures.push('static-fallback-contract');
  if (!row.tableWrappersValid) failures.push('table-wrapper-contract');
  if (!row.tableHeadersScoped) failures.push('table-header-scope');
  if (!row.touchTargetsValid) failures.push('touch-target-too-small');
  if (!row.idsUnique || !row.imagesNamed) failures.push('basic-a11y');
  if (!row.themeSurfaceValid) failures.push('theme-surface');
  if (row.criticalErrors.length) failures.push('critical-resource-or-console-error');
  return failures;
}

function softWarnings(row) {
  return row.wordCount > 4200 ? ['visible-word-above-target'] : [];
}

function runFixture(name) {
  const baseline = {
    httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: false,
    componentInsideArticle: true, bodyFontPx: 16, tableMinFontPx: 13, referenceMinFontPx: 15,
    viewportWidth: 1440, proseBlocks: 8, proseMaxPx: 700, wordCount: 3600,
    retiredComponents: 0, mapState: 'ready', mapLoaded: true, tabCount: 0,
    selectedTabCount: 0, panelLabelled: true,
    canvasAccessible: true, attributionPresent: true, attributionCount: 1,
    attributionIncludesOsm: true, staticCaseCount: 1,
    staticCasesHiddenWhenReady: true, visibleStaticSheetLinks: 0,
    fallbackImages: 0, tableWrappersValid: true, tableHeadersScoped: true,
    touchTargetsValid: true, idsUnique: true, imagesNamed: true, themeSurfaceValid: true,
    criticalErrors: []
  };
  const mutations = {
    overflow: { documentOverflow: true },
    'fallback-resilience': { mapState: 'fallback', mapLoaded: false, staticCaseCount: 0 },
    'poster-utility': { visibleStaticSheetLinks: 1 },
    'prose-measure-empty': { proseBlocks: 0 },
    'glyph-template': { criticalErrors: ['glyph-template-encoded:%7Bfontstack%7D'] },
    'word-floor': { wordCount: 2999 },
    'word-above-target': { wordCount: 4800 }
  };
  if (!mutations[name]) {
    console.error(JSON.stringify({ status: 'ERROR', error: `unknown fixture: ${name}` }));
    process.exit(2);
  }
  const row = { ...baseline, ...mutations[name] };
  const failures = evaluate(row);
  const warnings = softWarnings(row);
  const expected = {
    overflow: ['document-overflow'],
    'fallback-resilience': ['market-map-not-ready', 'static-case-contract'],
    'poster-utility': ['static-fallback-contract'],
    'prose-measure-empty': ['prose-measure-empty'],
    'glyph-template': ['critical-resource-or-console-error'],
    'word-floor': ['visible-word-target'],
    'word-above-target': []
  }[name];
  const expectedWarnings = { 'word-above-target': ['visible-word-above-target'] }[name] || [];
  const exact = JSON.stringify(failures) === JSON.stringify(expected)
    && JSON.stringify(warnings) === JSON.stringify(expectedWarnings);
  // Un fixture sin fallos esperados prueba que el techo avisa sin rechazar: sale 0.
  const soft = expected.length === 0;
  console.log(JSON.stringify({ status: exact ? (soft ? 'EXPECTED_WARN' : 'EXPECTED_FAIL') : 'WRONG_FAILURE', fixture: name, failures, expected, warnings, expectedWarnings }, null, 2));
  process.exit(exact ? (soft ? 0 : 1) : 2);
}

if (fixture) runFixture(fixture);

const scriptDir = dirname(fileURLToPath(import.meta.url));
const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
if (!existsSync(playwrightPath)) {
  console.error(JSON.stringify({ status: 'ERROR', error: `Playwright not found at ${playwrightPath}` }));
  process.exit(2);
}
const { chromium } = createRequire(import.meta.url)(playwrightPath);
const browserExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);

async function measurePage(browser, locale, route, theme, viewport) {
  const context = await browser.newContext({ viewport });
  await context.addInitScript((selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme), theme);
  const page = await context.newPage();
  const criticalErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') criticalErrors.push(`console:${message.text()}`);
  });
  page.on('requestfailed', (request) => {
    const url = request.url();
    if (url.startsWith(baseUrl) || url.includes('tiles.3cucharadas.cl')) {
      criticalErrors.push(`request:${url}:${request.failure()?.errorText || 'failed'}`);
    }
  });
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.locator('[data-thesis-market-map]').scrollIntoViewIfNeeded();
    await page.waitForFunction(
      () => ['ready', 'fallback'].includes(document.querySelector('[data-thesis-market-map]')?.dataset.mapState || ''),
      undefined,
      { timeout: 35_000 }
    );
    await page.evaluate(() => document.fonts.ready);

    const row = await page.evaluate(({ locale, theme, viewport, status, title, headings, tolerance, errors }) => {
      const article = document.querySelector('.page__content');
      const component = article?.querySelector('[data-thesis-market-map]');
      const articleBox = article?.getBoundingClientRect();
      const componentBox = component?.getBoundingClientRect();
      const headingText = [...(article?.querySelectorAll('h2, h3') || [])].map((node) => node.textContent?.trim() || '');
      const tables = [...(article?.querySelectorAll('table') || [])];
      const references = [...(article?.querySelectorAll('.footnotes li, .post-references p') || [])];
      const tabs = [...(component?.querySelectorAll('[data-market-map-tab]') || [])];
      const panel = component?.querySelector('[data-market-map-panel]');
      const canvas = component?.querySelector('[data-market-map-canvas]');
      const wrappers = [...(article?.querySelectorAll('.tabla-desliza') || [])];
      const controls = [...(component?.querySelectorAll('button, .territorial-evidence__poster-link') || [])].filter((node) => {
        const style = getComputedStyle(node);
        const box = node.getBoundingClientRect();
        return style.display !== 'none' && style.visibility !== 'hidden' && box.width > 0 && box.height > 0;
      });
      const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
      const prose = [...(article?.querySelectorAll(':scope > :is(p, ul, ol)') || [])]
        .filter((node) => node.getBoundingClientRect().width > 0)
        .map((node) => node.getBoundingClientRect().width);
      // La cápsula de audio es un aviso de plataforma, no relato: la meta se calibró sin ella.
      const words = (node) => (node?.innerText.match(/\S+/g) || []).length;
      const wordCount = words(article) - words(article?.querySelector('.capsula-audio'));
      const tableFonts = tables.flatMap((table) => [...table.querySelectorAll('th, td')]
        .map((cell) => parseFloat(getComputedStyle(cell).fontSize)));
      const referenceFonts = references.map((node) => parseFloat(getComputedStyle(node).fontSize));
      const rootBackground = component ? getComputedStyle(component).backgroundColor : '';
      const lightSurface = /rgb\((24[0-9]|25[0-5]),/.test(rootBackground);
      const darkSurface = /rgb\((1[0-9]|2[0-9]|3[0-9]),/.test(rootBackground);
      return {
        locale, theme, viewportWidth: viewport.width, httpStatus: status,
        titleMatches: document.title.includes(title),
        headingsPresent: headings.every((needle) => headingText.some((heading) => heading.includes(needle))),
        documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + tolerance,
        componentInsideArticle: Boolean(articleBox && componentBox)
          && componentBox.left >= articleBox.left - tolerance && componentBox.right <= articleBox.right + tolerance,
        bodyFontPx: article ? parseFloat(getComputedStyle(article).fontSize) : 0,
        tableMinFontPx: tableFonts.length ? Math.min(...tableFonts) : 0,
        referenceMinFontPx: referenceFonts.length ? Math.min(...referenceFonts) : 0,
        proseBlocks: prose.length,
        proseMaxPx: prose.length ? Math.max(...prose) : 0,
        wordCount,
        retiredComponents: article?.querySelectorAll('.evidence-carousel--stylized, .thesis-author-case, [data-evidence-carousel]').length || 0,
        mapState: component?.dataset.mapState || '',
        mapLoaded: component?.dataset.mapLoaded === 'true',
        tabCount: tabs.length,
        selectedTabCount: tabs.filter((tab) => tab.getAttribute('aria-selected') === 'true').length,
        panelLabelled: Boolean(panel?.getAttribute('aria-labelledby'))
          && Boolean(document.getElementById(panel.getAttribute('aria-labelledby'))),
        canvasAccessible: canvas?.getAttribute('role') === 'region'
          && canvas?.getAttribute('tabindex') === '0' && Boolean(canvas?.getAttribute('aria-label')),
        attributionPresent: Boolean(component?.querySelector('.maplibregl-ctrl-attrib')),
        attributionCount: component?.querySelectorAll('.maplibregl-ctrl-attrib').length || 0,
        attributionIncludesOsm: /openstreetmap/i.test(component?.querySelector('.maplibregl-ctrl-attrib')?.textContent || ''),
        staticCaseCount: component?.querySelectorAll('[data-market-map-fallback-grid] .territorial-evidence__case-card').length || 0,
        fallbackImages: component?.querySelectorAll('[data-market-map-fallback-grid] img').length || 0,
        visibleStaticSheetLinks: [...(component?.querySelectorAll('a') || [])].filter((link) => /lámina|sheet/i.test(link.textContent || '') && getComputedStyle(link).display !== 'none').length,
        staticCasesHiddenWhenReady: component?.dataset.mapState !== 'ready'
          || getComputedStyle(component.querySelector('[data-market-map-fallback-grid]')).display === 'none',
        tableWrappersValid: wrappers.length > 0 && wrappers.every((wrapper) => {
          const wrapperBox = wrapper.getBoundingClientRect();
          const nested = wrapper.querySelectorAll('.tabla-desliza').length;
          return nested === 0 && wrapperBox.left >= -tolerance
            && wrapperBox.right <= document.documentElement.clientWidth + tolerance
            && wrapper.getAttribute('role') === 'region'
            && wrapper.getAttribute('tabindex') === '0'
            && Boolean(wrapper.getAttribute('aria-label'))
            && ['auto', 'scroll'].includes(getComputedStyle(wrapper).overflowX);
        }),
        tableHeadersScoped: tables.every((table) => [...table.querySelectorAll('thead th')]
          .every((cell) => cell.getAttribute('scope') === 'col')),
        touchTargetsValid: controls.every((node) => {
          const box = node.getBoundingClientRect();
          return box.width >= 44 && box.height >= 44;
        }),
        idsUnique: new Set(ids).size === ids.length,
        imagesNamed: [...(article?.querySelectorAll('img') || [])].every((image) => Boolean(image.getAttribute('alt')?.trim())),
        themeSurfaceValid: theme === 'academic-night' ? darkSurface : lightSurface,
        criticalErrors: errors.filter((error) => !error.includes('favicon'))
      };
    }, {
      locale, theme, viewport, status: response?.status() || 0, title: titles[locale],
      headings: headingNeedles[locale], tolerance, errors: criticalErrors
    });
    row.failures = evaluate(row);
    row.softWarnings = softWarnings(row);
    if ([430, 1280].includes(viewport.width)) {
      mkdirSync(screenshotDir, { recursive: true });
      await page.screenshot({ path: `${screenshotDir}/${locale}-${theme}-${viewport.width}.png`, fullPage: true });
    }
    return row;
  } finally {
    await context.close();
  }
}

async function auditFallback(browser, locale, route, theme) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await context.addInitScript((selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme), theme);
  const page = await context.newPage();
  await page.route('**/assets/dist/thesis_post2_map/manifest.json', (request) => request.abort());
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    await page.locator('[data-thesis-market-map]').scrollIntoViewIfNeeded();
    await page.waitForFunction(
      () => document.querySelector('[data-thesis-market-map]')?.dataset.mapState === 'fallback',
      undefined,
      { timeout: 15_000 }
    );
    return await page.locator('[data-thesis-market-map]').evaluate((node, payload) => {
      const firstLink = node.querySelector('a');
      const surface = getComputedStyle(node);
      const link = firstLink ? getComputedStyle(firstLink) : null;
      return ({
      locale: payload.locale,
      theme: payload.theme,
      status: payload.status,
      state: node.dataset.mapState,
      cases: node.querySelectorAll('[data-market-map-fallback-grid] .territorial-evidence__case-card').length,
      fallbackImages: node.querySelectorAll('[data-market-map-fallback-grid] img').length,
      staticSheetLinks: [...node.querySelectorAll('a')].filter((link) => /lámina|sheet/i.test(link.textContent || '')).length,
      gridVisible: getComputedStyle(node.querySelector('[data-market-map-fallback-grid]')).display !== 'none',
      tabsAbsent: !node.querySelector('[data-market-map-tabs]'),
      panelHidden: node.querySelector('[data-market-map-panel]')?.hidden === true,
      statusResolved: !/carga|loads/i.test(node.querySelector('[data-market-map-status]')?.textContent || ''),
      themeValid: payload.theme !== 'academic-night' || (
        surface.backgroundColor === 'rgb(18, 23, 36)' && link?.color === 'rgb(100, 216, 233)'
      )
    });
    }, { locale, theme, status: response?.status() || 0 });
  } finally {
    await context.close();
  }
}

async function auditDeepLink(browser, locale, route) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  try {
    const response = await page.goto(`${baseUrl}${route}#territorial-case-el-salvador`, { waitUntil: 'domcontentloaded' });
    await page.locator('[data-thesis-market-map]').scrollIntoViewIfNeeded();
    await page.waitForFunction(
      () => document.querySelector('[data-thesis-market-map]')?.dataset.mapState === 'ready',
      undefined,
      { timeout: 35_000 }
    );
    return await page.locator('[data-thesis-market-map]').evaluate((node, payload) => {
      const [latitude] = (node.dataset.mapCenter || '').split(',').map(Number);
      return {
        locale: payload.locale,
        status: payload.status,
        activeCase: node.dataset.activeCase,
        latitude,
        hash: location.hash,
        pointCount: Number(node.dataset.mapPointCount),
        framed: node.dataset.activeCase === 'el-salvador' && Number(node.dataset.mapPointCount) === 3
          && Number.isFinite(latitude) && Math.abs(latitude + 26.243802) < 0.02
      };
    }, { locale, status: response?.status() || 0 });
  } finally {
    await context.close();
  }
}

async function auditNoJs(browser, locale, route) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
  const page = await context.newPage();
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
    return await page.locator('[data-thesis-market-map]').evaluate((node, payload) => ({
      locale: payload.locale,
      status: payload.status,
      cases: node.querySelectorAll('[data-market-map-fallback-grid] .territorial-evidence__case-card').length,
      fallbackImages: node.querySelectorAll('[data-market-map-fallback-grid] img').length,
      staticSheetLinks: [...node.querySelectorAll('a')].filter((link) => /lámina|sheet/i.test(link.textContent || '')).length,
      gridVisible: getComputedStyle(node.querySelector('[data-market-map-fallback-grid]')).display !== 'none',
      tabsAbsent: !node.querySelector('[data-market-map-tabs]'),
      panelHidden: node.querySelector('[data-market-map-panel]')?.hidden === true
    }), { locale, status: response?.status() || 0 });
  } finally {
    await context.close();
  }
}

async function auditPostI(browser, locale, route, theme, viewport) {
  const context = await browser.newContext({ viewport });
  await context.addInitScript((selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme), theme);
  const page = await context.newPage();
  const criticalErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') criticalErrors.push(`console:${message.text()}`);
  });
  page.on('requestfailed', (request) => {
    if (request.url().startsWith(baseUrl)) criticalErrors.push(`request:${request.url()}:${request.failure()?.errorText || 'failed'}`);
  });
  try {
    const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.evaluate(() => document.fonts.ready);
    const row = await page.evaluate(({ locale, theme, viewport, status, title, tolerance, errors }) => {
      const article = document.querySelector('.page__content');
      const tables = [...(article?.querySelectorAll('table') || [])];
      const wrappers = [...(article?.querySelectorAll('.tabla-desliza') || [])];
      const references = [...(article?.querySelectorAll('.footnotes li, .post-references p') || [])];
      const tableFonts = tables.flatMap((table) => [...table.querySelectorAll('th, td')].map((cell) => parseFloat(getComputedStyle(cell).fontSize)));
      const referenceFonts = references.map((node) => parseFloat(getComputedStyle(node).fontSize));
      const prose = [...(article?.querySelectorAll(':scope > :is(p, ul, ol)') || [])]
        .filter((node) => node.getBoundingClientRect().width > 0)
        .map((node) => node.getBoundingClientRect().width);
      const headings = [...(article?.querySelectorAll('h2') || [])].map((node) => node.textContent || '');
      return {
        locale, theme, viewportWidth: viewport.width, httpStatus: status,
        titleMatches: document.title.includes(title),
        threeSpoonfuls: ['1', '2', '3'].every((number) => headings.some((heading) => heading.includes(locale === 'es' ? `Cucharada ${number}` : `Spoonful ${number}`))),
        closingPresent: headings.some((heading) => /de replicar a extender|from replication to extension/i.test(heading)),
        documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + tolerance,
        bodyFontPx: article ? parseFloat(getComputedStyle(article).fontSize) : 0,
        tableCount: tables.length,
        wrapperCount: wrappers.length,
        wrappersValid: wrappers.every((wrapper) => {
          const box = wrapper.getBoundingClientRect();
          return wrapper.getAttribute('role') === 'region' && wrapper.getAttribute('tabindex') === '0'
            && box.left >= -tolerance && box.right <= document.documentElement.clientWidth + tolerance;
        }),
        tableMinFontPx: tableFonts.length ? Math.min(...tableFonts) : 0,
        referenceMinFontPx: referenceFonts.length ? Math.min(...referenceFonts) : 0,
        proseMaxPx: prose.length ? Math.max(...prose) : 0,
        themeApplied: document.documentElement.dataset.theme === theme,
        criticalErrors: errors.filter((error) => !error.includes('favicon'))
      };
    }, { locale, theme, viewport, status: response?.status() || 0, title: postITitles[locale], tolerance, errors: criticalErrors });
    row.failures = [];
    if (row.httpStatus !== 200) row.failures.push('route-not-200');
    if (!row.titleMatches || !row.threeSpoonfuls || !row.closingPresent) row.failures.push('post-i-structure');
    if (row.documentOverflow) row.failures.push('document-overflow');
    if (row.bodyFontPx < 16 || row.tableMinFontPx < 13 || row.referenceMinFontPx < 14) row.failures.push('legibility');
    if (row.tableCount !== 3 || row.wrapperCount !== 3 || !row.wrappersValid) row.failures.push('table-wrapper-contract');
    if (row.viewportWidth >= 1024 && row.proseMaxPx > 720 + tolerance) row.failures.push('prose-measure-too-wide');
    if (!row.themeApplied) row.failures.push('theme-not-applied');
    if (row.criticalErrors.length) row.failures.push('critical-resource-or-console-error');
    if ([430, 1280].includes(viewport.width)) {
      mkdirSync(screenshotDir, { recursive: true });
      await page.screenshot({ path: `${screenshotDir}/post-i-${locale}-${theme}-${viewport.width}.png`, fullPage: true });
    }
    return row;
  } finally {
    await context.close();
  }
}

const browser = await chromium.launch({
  headless: true,
  ...(browserExecutable ? { executablePath: browserExecutable } : {})
});
const rows = [];
const fallbacks = [];
const noJsRows = [];
const deepLinks = [];
const postIRows = [];
try {
  for (const [locale, route] of Object.entries(routes)) {
    for (const theme of themes) {
      for (const viewport of viewports) rows.push(await measurePage(browser, locale, route, theme, viewport));
    }
    for (const theme of themes) fallbacks.push(await auditFallback(browser, locale, route, theme));
    noJsRows.push(await auditNoJs(browser, locale, route));
    deepLinks.push(await auditDeepLink(browser, locale, route));
  }
  for (const [locale, route] of Object.entries(postIRoutes)) {
    for (const theme of themes) {
      for (const viewport of viewports) postIRows.push(await auditPostI(browser, locale, route, theme, viewport));
    }
  }
} finally {
  await browser.close();
}

const failures = rows.flatMap((row) => row.failures.map((failure) => ({
  surface: 'page', locale: row.locale, theme: row.theme, viewport: row.viewportWidth, failure,
  detail: failure === 'critical-resource-or-console-error' ? row.criticalErrors : undefined,
  wordCount: failure === 'visible-word-target' ? row.wordCount : undefined
})));
for (const row of fallbacks) {
  if (row.status !== 200 || row.state !== 'fallback' || row.cases !== 1 || row.fallbackImages !== 0 || row.staticSheetLinks !== 0 || !row.gridVisible || !row.tabsAbsent || !row.panelHidden || !row.statusResolved || !row.themeValid) {
    failures.push({ surface: 'fallback', ...row, failure: 'fallback-contract' });
  }
}
for (const row of noJsRows) {
  if (row.status !== 200 || row.cases !== 1 || row.fallbackImages !== 0 || row.staticSheetLinks !== 0 || !row.gridVisible || !row.tabsAbsent || !row.panelHidden) {
    failures.push({ surface: 'no-js', ...row, failure: 'no-js-contract' });
  }
}
for (const row of deepLinks) {
  if (row.status !== 200 || row.activeCase !== 'el-salvador' || row.pointCount !== 3 || row.hash !== '#territorial-case-el-salvador' || !row.framed) {
    failures.push({ surface: 'deep-link', ...row, failure: 'deep-link-contract' });
  }
}
for (const row of postIRows) {
  row.failures.forEach((failure) => failures.push({ surface: 'post-i', locale: row.locale, theme: row.theme, viewport: row.viewportWidth, failure, detail: row.criticalErrors }));
}

const summary = {
  status: failures.length ? 'FAIL' : 'PASS',
  pages: `${rows.filter((row) => row.failures.length === 0).length}/${rows.length}`,
  fallback: `${fallbacks.length - failures.filter((row) => row.surface === 'fallback').length}/${fallbacks.length}`,
  noJs: `${noJsRows.length - failures.filter((row) => row.surface === 'no-js').length}/${noJsRows.length}`,
  deepLinks: `${deepLinks.length - failures.filter((row) => row.surface === 'deep-link').length}/${deepLinks.length}`,
  postI: `${postIRows.filter((row) => row.failures.length === 0).length}/${postIRows.length}`,
  screenshots: screenshotDir,
  failures,
  softWarnings: rows.flatMap((row) => row.softWarnings.map((code) => ({
    locale: row.locale, theme: row.theme, viewport: row.viewportWidth, code, observedWords: row.wordCount, targetWords: 4200
  })))
};
console.log(JSON.stringify(summaryOnly ? summary : { ...summary, rows, fallbacks, noJsRows, deepLinks, postIRows }, null, 2));
process.exit(failures.length ? 1 : 0);
