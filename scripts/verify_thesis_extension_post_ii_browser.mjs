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
const fixture = valueAfter('--fixture');
const summaryOnly = args.includes('--summary');
const baseUrl = (valueAfter('--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
const screenshotDir = valueAfter('--screenshot-dir') || '/tmp/thesis-post2-browser-gate';

const thresholds = {
  geometryTolerancePx: 2,
  bodyMinPx: 16,
  captionMinPx: 12,
  articleViewportFillMin: 0.43,
  desktopArticleWidthMinPx: 820,
  mapTitleMobileMaxPx: 20,
  mapTitleDesktopMaxPx: 24,
  expectedStylizedFigures: 5,
  expectedNamedTabs: 5,
  expectedMapsFirst: 2,
  expectedInteractiveMapTabs: 3,
  componentMinPx: 12,
  proseMeasureDesktopMaxPx: 720,
  initializationScrollTolerancePx: 2,
  // Editorial signal only: source-backed substance may justify exceeding it.
  // Length is reported but does not fail the visual or release gate.
  targetVisibleWordsSoft: 2500,
  svgMinFontPx: 11
};

function evaluateMarketMapInitialization(row = {}) {
  const visualShift = Number(row.initializationVisualShiftPx ?? row.initializationScrollDeltaPx);
  return visualShift <= thresholds.initializationScrollTolerancePx
    ? []
    : ['market-map-initialization-scroll-jump'];
}

function evaluateFallback(row = {}) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('fallback-route-not-200');
  if (row.state !== 'fallback') failures.push('fallback-state-missing');
  if (!row.tabListHidden || !row.tabsDisabled) failures.push('fallback-tabs-interactive');
  if (!row.canvasHidden || !row.asideHidden) failures.push('fallback-loading-ui-visible');
  if (!row.statusResolved || !row.posterAvailable) failures.push('fallback-poster-unavailable');
  return failures;
}

function evaluateMeasurement(row) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('route-not-200');
  if (!row.titleMatches) failures.push('wrong-title');
  if (!row.headingsPresent) failures.push('missing-structure');
  if (row.documentOverflow) failures.push('document-overflow');
  if (!row.article.present) failures.push('article-missing');
  if (row.article.width < row.viewport.width * thresholds.articleViewportFillMin) failures.push('article-too-narrow');
  if (row.viewport.width >= 1800 && row.article.width < thresholds.desktopArticleWidthMinPx) failures.push('article-not-widened-on-desktop');
  if (row.fonts.body < thresholds.bodyMinPx) failures.push('body-font-too-small');
  if (row.fonts.caption < thresholds.captionMinPx) failures.push('caption-font-too-small');
  if (row.viewport.width >= 1024 && row.proseMeasure.measuredBlocks < 1) failures.push('prose-measure-missing');
  if (row.viewport.width >= 1024 && row.proseMeasure.maxBlockWidth > thresholds.proseMeasureDesktopMaxPx) failures.push('prose-measure-too-wide');
  if (row.retiredCarouselCount !== 0) failures.push('redundant-results-carousel-present');
  if (row.stylizedCarousel.count !== 1) failures.push('stylized-carousel-count');
  if (!row.stylizedCarousel.enhanced) failures.push('stylized-carousel-not-enhanced');
  if (row.stylizedCarousel.slideCount !== thresholds.expectedStylizedFigures) failures.push('stylized-figure-count');
  if (row.stylizedCarousel.tabCount !== thresholds.expectedNamedTabs) failures.push('stylized-tab-count');
  if (!row.stylizedCarousel.tabsNamed) failures.push('stylized-tabs-not-named');
  if (!row.stylizedCarousel.mapsFirst) failures.push('stylized-maps-not-first');
  if (!row.stylizedCarousel.controlsAccessible) failures.push('stylized-controls-inaccessible');
  if (!row.stylizedCarousel.viewportContained) failures.push('stylized-viewport-overflow');
  if (!row.stylizedCarousel.rootInsideArticle) failures.push('stylized-root-overflow');
  if (!row.stylizedCarousel.statusUpdated) failures.push('stylized-status-stale');
  if (!row.stylizedCarousel.keyboardAdvanced) failures.push('stylized-keyboard-broken');
  if (!row.stylizedFigures.every((figure) => figure.loaded)) failures.push('stylized-figure-not-loaded');
  if (!row.stylizedFigures.every((figure) => figure.visibleWhenSelected)) failures.push('stylized-figure-not-visible');
  if (!row.stylizedFigures.every((figure) => figure.insideSlide && figure.insideArticle)) failures.push('stylized-figure-clipped');
  if (!row.stylizedFigures.every((figure) => figure.aspectSafe)) failures.push('stylized-figure-aspect-distorted');
  if (!row.stylizedFigures.every((figure) => figure.clickable && figure.vectorTarget)) failures.push('stylized-figure-not-clickable-vector');
  if (!row.stylizedFigures.every((figure) => figure.hdLink && figure.hdVectorTarget)) failures.push('stylized-hd-link-missing');
  if (!row.stylizedFigures.every((figure) => figure.altPresent)) failures.push('stylized-figure-alt-missing');
  if (!row.stylizedFigures.every((figure) => figure.textNotClipped)) failures.push('stylized-text-clipped');
  if (!row.stylizedFigures.every((figure) => !figure.textMediaOverlap)) failures.push('stylized-text-media-overlap');
  if (!row.stylizedFigures.slice(0, thresholds.expectedMapsFirst).every((figure) => figure.factCount === 4)) failures.push('map-facts-missing');
  if (!row.stylizedPopup.opened || !row.stylizedPopup.imageLoaded || !row.stylizedPopup.closed) failures.push('stylized-popup-broken');
  if (row.marketMap.state !== 'ready') failures.push('market-map-not-ready');
  if (!row.marketMap.canvasVisible) failures.push('market-map-canvas-not-visible');
  if (!row.marketMap.canvasAccessible) failures.push('market-map-canvas-inaccessible');
  if (row.marketMap.tabCount !== thresholds.expectedInteractiveMapTabs) failures.push('market-map-tab-count');
  if (!row.marketMap.tabsNamed) failures.push('market-map-tabs-not-named');
  if (!row.marketMap.labelsLocalized) failures.push('market-map-labels-not-localized');
  if (!row.marketMap.academicOutcomesAbsent) failures.push('market-map-academic-anecdote-visible');
  if (!row.marketMap.casesWorked) failures.push('market-map-case-switch-broken');
  if (!row.marketMap.posterWorked) failures.push('market-map-poster-switch-broken');
  if (!row.marketMap.insideArticle) failures.push('market-map-overflow');
  if (!row.marketMap.attributionPresent) failures.push('market-map-attribution-missing');
  if (!row.marketMap.firaApplied) failures.push('market-map-fira-missing');
  if (row.marketMap.titleFontPx > (row.viewport.width <= 440 ? thresholds.mapTitleMobileMaxPx : thresholds.mapTitleDesktopMaxPx)) failures.push('market-map-title-too-large');
  if (!row.marketMap.themeSurfaceValid) failures.push('market-map-theme-surface');
  if (row.marketMap.asideMinFontPx < thresholds.componentMinPx) failures.push('market-map-font-too-small');
  failures.push(...evaluateMarketMapInitialization(row.marketMap));
  if (!row.authorCase.present || !row.authorCase.insideArticle) failures.push('author-case-missing-or-overflow');
  if (!row.authorCase.imageLoaded || !row.authorCase.vectorTarget || !row.authorCase.altPresent) failures.push('author-case-fallback-broken');
  if (row.authorCase.minFontPx < thresholds.componentMinPx) failures.push('author-case-font-too-small');
  if (!row.tables.detailsOpen) failures.push('table-details-closed');
  if (!row.tables.contained) failures.push('table-page-overflow');
  if (!row.referencesPresent) failures.push('references-missing');
  failures.push(...evaluateSemanticStructure(row.semanticStructure));
  return failures;
}

function evaluateSemanticStructure(row = {}) {
  const failures = [];
  if ((row.invalidCarouselArticleRoles || 0) > 0) failures.push('carousel-slide-role-invalid');
  if ((row.invalidDefinitionChildren || 0) > 0) failures.push('author-definition-list-invalid');
  return failures;
}

function evaluateSvgAudit(row) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('svg-route-not-200');
  if (!row.hasAccessibleName) failures.push('svg-accessible-name-missing');
  if (!row.textInsideViewBox) failures.push('svg-text-outside-viewbox');
  if (row.textOverlaps.length) failures.push('svg-text-overlap');
  if (row.minimumFontPx < thresholds.svgMinFontPx) failures.push('svg-font-too-small');
  return failures;
}

if (fixture) {
  if (!['overflow', 'svg-overlap', 'visual-style', 'semantic-a11y', 'academic-anecdote', 'scroll-jump', 'fallback-resilience', 'prose-measure', 'prose-measure-empty'].includes(fixture)) {
    console.error(JSON.stringify({ status: 'ERROR', error: `Unknown fixture: ${fixture}` }));
    process.exit(2);
  }
  if (fixture === 'svg-overlap') {
    const row = {
      httpStatus: 200,
      hasAccessibleName: true,
      textInsideViewBox: true,
      textOverlaps: [['title', 'metric']],
      minimumFontPx: 14
    };
    const failures = evaluateSvgAudit(row);
    const expectedFailures = ['svg-text-overlap'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'semantic-a11y') {
    const failures = evaluateSemanticStructure({
      invalidCarouselArticleRoles: 6,
      invalidDefinitionChildren: 4
    });
    const expectedFailures = ['carousel-slide-role-invalid', 'author-definition-list-invalid'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'academic-anecdote') {
    const row = {
      locale: 'es', theme: 'light', viewport: { width: 390, height: 844 },
      httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: false,
      article: { present: true, width: 350 }, fonts: { body: 17, caption: 14 },
      content: { visibleWords: 2200 }, retiredCarouselCount: 0,
      stylizedCarousel: {
        count: 1, enhanced: true, slideCount: 5, tabCount: 5, tabsNamed: true,
        mapsFirst: true, controlsAccessible: true, viewportContained: true,
        rootInsideArticle: true, statusUpdated: true, keyboardAdvanced: true
      },
      stylizedFigures: Array.from({ length: 5 }, (_, index) => ({
        loaded: true, visibleWhenSelected: true, insideSlide: true, insideArticle: true,
        aspectSafe: true, clickable: true, vectorTarget: true, hdLink: true,
        hdVectorTarget: true, altPresent: true, textNotClipped: true,
        textMediaOverlap: false, factCount: index < 2 ? 4 : 0
      })),
      stylizedPopup: { opened: true, imageLoaded: true, closed: true },
      marketMap: {
        state: 'ready', canvasVisible: true, canvasAccessible: true,
        tabCount: thresholds.expectedInteractiveMapTabs,
        tabsNamed: true, labelsLocalized: true, academicOutcomesAbsent: false,
        casesWorked: true, posterWorked: true, insideArticle: true,
        attributionPresent: true, firaApplied: true, titleFontPx: 18,
        themeSurfaceValid: true, asideMinFontPx: 12, initializationScrollDeltaPx: 0
      },
      authorCase: {
        present: true, insideArticle: true, imageLoaded: true,
        vectorTarget: true, altPresent: true, minFontPx: 12
      },
      tables: { detailsOpen: true, contained: true },
      referencesPresent: true,
      semanticStructure: { invalidCarouselArticleRoles: 0, invalidDefinitionChildren: 0 }
    };
    const failures = evaluateMeasurement(row);
    const expectedFailures = ['market-map-academic-anecdote-visible'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'scroll-jump') {
    const failures = evaluateMarketMapInitialization({
      initializationVisualShiftPx: 577,
      initializationScrollDeltaPx: 0
    });
    const expectedFailures = ['market-map-initialization-scroll-jump'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'prose-measure') {
    const failures = evaluateMeasurement({
      locale: 'es', theme: 'light', viewport: { width: 1440, height: 1000 },
      httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: false,
      article: { present: true, width: 796 }, fonts: { body: 18, caption: 14 },
      proseMeasure: { measuredBlocks: 1, maxBlockWidth: 796 }, content: { visibleWords: 2200 }, retiredCarouselCount: 0,
      stylizedCarousel: { count: 1, enhanced: true, slideCount: 5, tabCount: 5, tabsNamed: true, mapsFirst: true, controlsAccessible: true, viewportContained: true, rootInsideArticle: true, statusUpdated: true, keyboardAdvanced: true },
      stylizedFigures: Array.from({ length: 5 }, (_, index) => ({ loaded: true, visibleWhenSelected: true, insideSlide: true, insideArticle: true, aspectSafe: true, clickable: true, vectorTarget: true, hdLink: true, hdVectorTarget: true, altPresent: true, textNotClipped: true, textMediaOverlap: false, factCount: index < 2 ? 4 : 0 })),
      stylizedPopup: { opened: true, imageLoaded: true, closed: true },
      marketMap: { state: 'ready', canvasVisible: true, canvasAccessible: true, tabCount: 3, tabsNamed: true, labelsLocalized: true, academicOutcomesAbsent: true, casesWorked: true, posterWorked: true, insideArticle: true, attributionPresent: true, firaApplied: true, titleFontPx: 20, themeSurfaceValid: true, asideMinFontPx: 12, initializationScrollDeltaPx: 0 },
      authorCase: { present: true, insideArticle: true, imageLoaded: true, vectorTarget: true, altPresent: true, minFontPx: 12 },
      tables: { detailsOpen: true, contained: true }, referencesPresent: true,
      semanticStructure: { invalidCarouselArticleRoles: 0, invalidDefinitionChildren: 0 }
    });
    const expectedFailures = ['prose-measure-too-wide'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'fallback-resilience') {
    const failures = evaluateFallback({
      httpStatus: 200, state: 'loading', tabListHidden: false, tabsDisabled: false,
      canvasHidden: false, asideHidden: false, statusResolved: false, posterAvailable: false
    });
    const expectedFailures = [
      'fallback-state-missing', 'fallback-tabs-interactive',
      'fallback-loading-ui-visible', 'fallback-poster-unavailable'
    ];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'prose-measure-empty') {
    const failures = evaluateMeasurement({
      locale: 'es', theme: 'light', viewport: { width: 1440, height: 1000 },
      httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: false,
      article: { present: true, width: 796 }, fonts: { body: 18, caption: 14 },
      proseMeasure: { measuredBlocks: 0, maxBlockWidth: 0 }, content: { visibleWords: 2200 }, retiredCarouselCount: 0,
      stylizedCarousel: { count: 1, enhanced: true, slideCount: 5, tabCount: 5, tabsNamed: true, mapsFirst: true, controlsAccessible: true, viewportContained: true, rootInsideArticle: true, statusUpdated: true, keyboardAdvanced: true },
      stylizedFigures: Array.from({ length: 5 }, (_, index) => ({ loaded: true, visibleWhenSelected: true, insideSlide: true, insideArticle: true, aspectSafe: true, clickable: true, vectorTarget: true, hdLink: true, hdVectorTarget: true, altPresent: true, textNotClipped: true, textMediaOverlap: false, factCount: index < 2 ? 4 : 0 })),
      stylizedPopup: { opened: true, imageLoaded: true, closed: true },
      marketMap: { state: 'ready', canvasVisible: true, canvasAccessible: true, tabCount: 3, tabsNamed: true, labelsLocalized: true, academicOutcomesAbsent: true, casesWorked: true, posterWorked: true, insideArticle: true, attributionPresent: true, firaApplied: true, titleFontPx: 20, themeSurfaceValid: true, asideMinFontPx: 12, initializationScrollDeltaPx: 0 },
      authorCase: { present: true, insideArticle: true, imageLoaded: true, vectorTarget: true, altPresent: true, minFontPx: 12 },
      tables: { detailsOpen: true, contained: true }, referencesPresent: true,
      semanticStructure: { invalidCarouselArticleRoles: 0, invalidDefinitionChildren: 0 }
    });
    const expectedFailures = ['prose-measure-missing'];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  if (fixture === 'visual-style') {
    const row = {
      locale: 'es', theme: 'light', viewport: { width: 1920, height: 1080 },
      httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: false,
      article: { present: true, width: 840 }, fonts: { body: 18, caption: 14 },
      proseMeasure: { measuredBlocks: 1, maxBlockWidth: 680 }, content: { visibleWords: 2200 }, retiredCarouselCount: 0,
      stylizedCarousel: {
        count: 1, enhanced: true, slideCount: 5, tabCount: 5, tabsNamed: true,
        mapsFirst: true, controlsAccessible: true, viewportContained: true,
        rootInsideArticle: true, statusUpdated: true, keyboardAdvanced: true
      },
      stylizedFigures: Array.from({ length: 5 }, (_, index) => ({
        loaded: true, visibleWhenSelected: true, insideSlide: true, insideArticle: true,
        aspectSafe: true, clickable: true, vectorTarget: true, hdLink: true,
        hdVectorTarget: true, altPresent: true, textNotClipped: true,
        textMediaOverlap: false, factCount: index < 2 ? 4 : 0
      })),
      stylizedPopup: { opened: true, imageLoaded: true, closed: true },
      marketMap: {
        state: 'ready', canvasVisible: true, canvasAccessible: true,
        tabCount: thresholds.expectedInteractiveMapTabs,
        tabsNamed: true, labelsLocalized: false, academicOutcomesAbsent: true,
        casesWorked: true, posterWorked: true, insideArticle: true,
        attributionPresent: true, firaApplied: false, titleFontPx: 32, themeSurfaceValid: false,
        asideMinFontPx: 9, initializationScrollDeltaPx: 0
      },
      authorCase: { present: false, insideArticle: false, imageLoaded: false, vectorTarget: false, altPresent: false, minFontPx: 10 },
      tables: { detailsOpen: true, contained: true }, referencesPresent: true
    };
    const failures = evaluateMeasurement(row);
    const expectedFailures = [
      'market-map-labels-not-localized', 'market-map-fira-missing', 'market-map-title-too-large', 'market-map-theme-surface',
      'market-map-font-too-small', 'author-case-missing-or-overflow',
      'author-case-fallback-broken', 'author-case-font-too-small'
    ];
    const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
    console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
    process.exit(exact ? 1 : 2);
  }
  const row = {
    locale: 'es', theme: 'light', viewport: { width: 390, height: 844 },
    httpStatus: 200, titleMatches: true, headingsPresent: true, documentOverflow: true,
    article: { present: true, width: 350 }, fonts: { body: 17, caption: 14 },
    proseMeasure: { measuredBlocks: 1, maxBlockWidth: 350 }, content: { visibleWords: 2600 }, retiredCarouselCount: 1,
    stylizedCarousel: {
      count: 1, enhanced: true, slideCount: 5, tabCount: 5, tabsNamed: false,
      mapsFirst: true, controlsAccessible: true, viewportContained: false,
      rootInsideArticle: false, statusUpdated: true, keyboardAdvanced: true
    },
    stylizedFigures: Array.from({ length: 5 }, (_, index) => ({
      loaded: true, visibleWhenSelected: true, insideSlide: index !== 2, insideArticle: true,
      aspectSafe: true, clickable: true, vectorTarget: true, hdLink: true,
      hdVectorTarget: true, altPresent: true, textNotClipped: index !== 4,
      textMediaOverlap: index === 1, factCount: index < 2 ? 4 : 0
    })),
    stylizedPopup: { opened: true, imageLoaded: true, closed: true },
    marketMap: {
      state: 'ready', canvasVisible: true, canvasAccessible: true,
      tabCount: thresholds.expectedInteractiveMapTabs,
      tabsNamed: true, labelsLocalized: true, academicOutcomesAbsent: true,
      casesWorked: true, posterWorked: true, insideArticle: true,
      attributionPresent: true, firaApplied: true, titleFontPx: 18, themeSurfaceValid: true,
      asideMinFontPx: 12, initializationScrollDeltaPx: 0
    },
    authorCase: { present: true, insideArticle: true, imageLoaded: true, vectorTarget: true, altPresent: true, minFontPx: 12 },
    tables: { detailsOpen: false, contained: false }, referencesPresent: true
  };
  const failures = evaluateMeasurement(row);
  const expectedFailures = [
    'document-overflow', 'redundant-results-carousel-present',
    'stylized-tabs-not-named', 'stylized-viewport-overflow', 'stylized-root-overflow',
    'stylized-figure-clipped', 'stylized-text-clipped', 'stylized-text-media-overlap',
    'table-details-closed', 'table-page-overflow'
  ];
  const exact = JSON.stringify(failures) === JSON.stringify(expectedFailures);
  console.log(JSON.stringify({ status: exact ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture, failures, expectedFailures }, null, 2));
  process.exit(exact ? 1 : 2);
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
if (!existsSync(playwrightPath)) {
  console.error(JSON.stringify({ status: 'ERROR', error: `Playwright not found at ${playwrightPath}` }));
  process.exit(2);
}
const { chromium } = createRequire(import.meta.url)(playwrightPath);

const routes = {
  es: '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/',
  en: '/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/'
};
const expectedTitle = {
  es: 'Extender mi tesis en 3 cucharadas (parte II)',
  en: 'Extending my thesis in three spoonfuls (part II)'
};
const expectedHeadings = {
  es: ['Seis respuestas antes del método', 'Cucharada 1', 'Cucharada 2', 'Cucharada 3', 'Qué falta para hablar de causalidad', 'Referencias'],
  en: ['Six answers before methods', 'Spoonful 1', 'Spoonful 2', 'Spoonful 3', 'What is missing for causal inference', 'References']
};
const viewports = [
  { width: 360, height: 800 },
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 1280, height: 800 },
  { width: 1440, height: 900 },
  { width: 1920, height: 1080 }
];
const svgNames = [
  'mapa-lo-barnechea', 'mapa-lo-prado', 'mapa-el-salvador',
  'demografia', 'trayectoria-simce', 'trayectoria-admission'
];

function boxesIntersect(a, b, tolerance = 0) {
  return a.left < b.right - tolerance && a.right > b.left + tolerance
    && a.top < b.bottom - tolerance && a.bottom > b.top + tolerance;
}

async function exerciseCarousel(page, locale) {
  const rootSelector = '.evidence-carousel--stylized';
  const root = page.locator(`.page__content ${rootSelector}`);
  await root.waitFor({ state: 'visible', timeout: 15_000 });
  await page.waitForFunction(
    (selector) => document.querySelector(selector)?.classList.contains('is-enhanced'),
    rootSelector
  );
  const dots = root.locator('[data-carousel-dot]');
  const initialKinds = await root.locator('[data-carousel-slide]').evaluateAll(
    (nodes) => nodes.map((node) => node.getAttribute('data-slide-kind'))
  );
  const figures = [];
  for (let index = 0; index < thresholds.expectedStylizedFigures; index += 1) {
    await dots.nth(index).click();
    await page.waitForFunction(({ selector, selected }) => {
      const dot = document.querySelectorAll(`${selector} [data-carousel-dot]`)[selected];
      return dot?.getAttribute('aria-current') === 'true';
    }, { selector: rootSelector, selected: index });
    const slide = root.locator('[data-carousel-slide]').nth(index);
    const image = slide.locator('a[data-carousel-popup] img');
    await image.evaluate((node) => { node.loading = 'eager'; });
    await image.scrollIntoViewIfNeeded();
    await image.waitFor({ state: 'visible', timeout: 10_000 });
    await page.waitForFunction(({ selector, selected }) => {
      const node = document.querySelectorAll(`${selector} [data-carousel-slide] img`)[selected];
      return node?.complete && node.naturalWidth > 0;
    }, { selector: rootSelector, selected: index });
    figures.push(await slide.evaluate((slideNode, { selectedLocale, tolerance }) => {
      const imageNode = slideNode.querySelector('a[data-carousel-popup] img');
      const mediaNode = imageNode.closest('a');
      const hdNode = slideNode.querySelector('[data-carousel-hd-link]');
      const articleNode = slideNode.closest('.page__content');
      const viewportNode = slideNode.closest('[data-carousel-viewport]');
      const imageBox = imageNode.getBoundingClientRect();
      const mediaBox = mediaNode.getBoundingClientRect();
      const slideBox = slideNode.getBoundingClientRect();
      const articleBox = articleNode.getBoundingClientRect();
      const viewportBox = viewportNode.getBoundingClientRect();
      const inside = (inner, outer) => inner.left >= outer.left - tolerance
        && inner.right <= outer.right + tolerance
        && inner.top >= outer.top - tolerance
        && inner.bottom <= outer.bottom + tolerance;
      const textNodes = [...slideNode.querySelectorAll('.thesis-stylized__slide-header, .thesis-stylized__facts, figcaption')];
      const overlaps = textNodes.filter((node) => {
        const box = node.getBoundingClientRect();
        return box.left < mediaBox.right - tolerance && box.right > mediaBox.left + tolerance
          && box.top < mediaBox.bottom - tolerance && box.bottom > mediaBox.top + tolerance;
      });
      const renderedRatio = imageBox.width / imageBox.height;
      const naturalRatio = imageNode.naturalWidth / imageNode.naturalHeight;
      return {
        loaded: imageNode.complete && imageNode.naturalWidth > 0,
        visibleWhenSelected: imageBox.width > 0 && imageBox.height > 0 && inside(slideBox, viewportBox),
        insideSlide: inside(imageBox, slideBox) && inside(imageBox, mediaBox),
        insideArticle: imageBox.left >= articleBox.left - tolerance && imageBox.right <= articleBox.right + tolerance,
        aspectSafe: Number.isFinite(naturalRatio) && naturalRatio > 0
          && Math.abs(renderedRatio - naturalRatio) / naturalRatio < 0.01,
        clickable: mediaNode.classList.contains('image-popup'),
        vectorTarget: mediaNode.href.endsWith(`-${selectedLocale}.svg`),
        hdLink: Boolean(hdNode) && hdNode.target === '_blank' && hdNode.relList.contains('noopener'),
        hdVectorTarget: Boolean(hdNode?.href.endsWith(`-${selectedLocale}.svg`)),
        altPresent: Boolean(imageNode.getAttribute('alt')?.trim()),
        textNotClipped: textNodes.every((node) => node.scrollWidth <= node.clientWidth + tolerance
          && node.scrollHeight <= node.clientHeight + tolerance),
        textMediaOverlap: overlaps.length > 0,
        factCount: slideNode.querySelectorAll('.thesis-stylized__facts > div').length
      };
    }, { selectedLocale: locale, tolerance: thresholds.geometryTolerancePx }));
  }

  await dots.nth(0).click();
  await root.locator('[data-carousel-slide]').nth(0).locator('[data-carousel-popup]').click();
  const popup = page.locator('.mfp-wrap');
  await popup.waitFor({ state: 'visible', timeout: 5_000 });
  const popupOpened = await popup.isVisible();
  const popupImageLoaded = await page.locator('.mfp-img').evaluate(
    (image) => image.complete && image.naturalWidth > 0
  );
  await page.keyboard.press('Escape');
  await popup.waitFor({ state: 'hidden', timeout: 5_000 });
  const popupClosed = !(await popup.isVisible());

  await root.locator('[data-carousel-viewport]').focus();
  await page.keyboard.press('ArrowRight');
  await page.waitForFunction(
    (selector) => document.querySelector(`${selector} [data-carousel-dot="1"]`)?.getAttribute('aria-current') === 'true',
    rootSelector
  );
  return {
    figures,
    initialKinds,
    popup: { opened: popupOpened, imageLoaded: popupImageLoaded, closed: popupClosed }
  };
}

async function exerciseMarketMap(page, locale) {
  const root = page.locator('.page__content [data-thesis-market-map]');
  await root.waitFor({ state: 'visible', timeout: 15_000 });
  await root.scrollIntoViewIfNeeded();
  await page.evaluate(async () => {
    await document.fonts.ready;
    const map = document.querySelector('.page__content [data-thesis-market-map]');
    const mapTop = map ? map.getBoundingClientRect().top + window.scrollY : 0;
    const precedingImages = [...document.querySelectorAll('.page__content img')]
      .filter((image) => image.getBoundingClientRect().top + window.scrollY < mapTop);
    precedingImages.forEach((image) => { image.loading = 'eager'; });
    await Promise.all(precedingImages.map((image) => image.decode().catch(() => {})));
  });
  const positionBeforeInitialization = await root.evaluate((node) => {
    document.documentElement.style.scrollBehavior = 'auto';
    const absoluteTop = node.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({ top: Math.max(0, absoluteTop - 300), behavior: 'instant' });
    return { scrollY: window.scrollY, viewportTop: node.getBoundingClientRect().top };
  });
  await page.waitForFunction(
    () => ['ready', 'fallback'].includes(document.querySelector('[data-thesis-market-map]')?.dataset.mapState || ''),
    undefined,
    { timeout: 35_000 }
  );
  await page.waitForTimeout(100);
  const positionAfterInitialization = await root.evaluate((node) => ({
    scrollY: window.scrollY,
    viewportTop: node.getBoundingClientRect().top
  }));
  const initializationScrollDeltaPx = Math.abs(
    positionAfterInitialization.scrollY - positionBeforeInitialization.scrollY
  );
  const initializationVisualShiftPx = Math.abs(
    positionAfterInitialization.viewportTop - positionBeforeInitialization.viewportTop
  );
  await root.scrollIntoViewIfNeeded();
  const tabs = root.locator('[data-market-map-tab]');
  const expectedCases = ['Lo Barnechea', 'Lo Prado', 'El Salvador'];
  const expectedSegments = locale === 'es'
    ? ['Transición inicial', 'Educación básica', 'Educación básica']
    : ['Pre-primary', 'Primary', 'Primary'];
  const selectedCases = [];
  const localizedCases = [];
  for (let index = 0; index < expectedCases.length; index += 1) {
    await tabs.nth(index).click();
    await page.waitForFunction(({ selected, expected }) => {
      const host = document.querySelector('[data-thesis-market-map]');
      const tab = host?.querySelectorAll('[data-market-map-tab]')[selected];
      const aside = host?.querySelector('[data-market-map-aside]');
      return tab?.getAttribute('aria-selected') === 'true' && aside?.textContent?.includes(expected);
    }, { selected: index, expected: expectedCases[index] });
    selectedCases.push(await root.locator('[data-market-map-aside] h4').textContent());
    localizedCases.push(await root.locator('[data-market-map-aside]').evaluate(
      (node, expectedSegment) => {
        const text = node.textContent || '';
        const rawSegmentsAbsent = !text.includes('initial:transicion');
        const spanishBranchesAbsent = document.documentElement.lang.startsWith('en')
          || (!text.includes('Sale') && !text.includes('Entra'));
        return text.includes(expectedSegment) && rawSegmentsAbsent && spanishBranchesAbsent;
      },
      expectedSegments[index]
    ));
  }
  const posterHref = await root.locator('[data-market-map-poster]').getAttribute('href');
  await tabs.nth(2).focus();
  await page.keyboard.press('ArrowLeft');
  await page.waitForFunction(
    () => document.querySelectorAll('[data-market-map-tab]')[1]?.getAttribute('aria-selected') === 'true'
  );
  return root.evaluate((node, { cases, expected, localized, poster, selectedLocale, tolerance, initializationDelta, initializationVisualShift }) => {
    const article = node.closest('.page__content');
    const canvasHost = node.querySelector('[data-market-map-canvas]');
    const canvas = canvasHost?.querySelector('.maplibregl-canvas');
    const rootBox = node.getBoundingClientRect();
    const articleBox = article?.getBoundingClientRect();
    const tabs = [...node.querySelectorAll('[data-market-map-tab]')];
    const expectedPoster = selectedLocale === 'es' ? 'estilizada-mapa-el-salvador-es.svg' : 'estilizada-mapa-el-salvador-en.svg';
    const mapRootStyle = getComputedStyle(node);
    const titleStyle = getComputedStyle(node.querySelector('.thesis-market-map__header h3'));
    const background = mapRootStyle.backgroundColor;
    const isLight = document.documentElement.dataset.theme !== 'academic-night';
    const aside = node.querySelector('[data-market-map-aside]');
    const uiStrings = [...node.querySelectorAll('.maplibregl-control-container *')]
      .flatMap((element) => [element.textContent, element.getAttribute('title'), element.getAttribute('aria-label')])
      .filter(Boolean)
      .map((value) => value.trim());
    const untranslatedMapUi = [
      'Toggle attribution', 'Map feedback', 'Map', 'Map marker', 'Zoom in', 'Zoom out',
      'Drag to rotate map, click to reset north', 'Close popup',
      'Use Ctrl + scroll to zoom the map', 'Use ⌘ + scroll to zoom the map',
      'Use two fingers to move the map'
    ];
    const asideFonts = aside
      ? [aside, ...aside.querySelectorAll('*')]
        .filter((element) => element.getBoundingClientRect().width > 0)
        .map((element) => parseFloat(getComputedStyle(element).fontSize))
        .filter(Number.isFinite)
      : [];
    return {
      state: node.dataset.mapState || '',
      canvasVisible: Boolean(canvas && canvas.getBoundingClientRect().width > 0 && canvas.getBoundingClientRect().height > 0),
      canvasAccessible: canvasHost?.getAttribute('role') === 'region'
        && canvasHost?.getAttribute('tabindex') === '0'
        && Boolean(canvasHost?.getAttribute('aria-label')?.trim()),
      tabCount: tabs.length,
      tabsNamed: tabs.every((tab) => (tab.textContent || '').trim().length >= 5),
      labelsLocalized: localized.every(Boolean)
        && (selectedLocale === 'en' || !untranslatedMapUi.some((needle) => uiStrings.includes(needle))),
      academicOutcomesAbsent: !/(?:SIMCE relativo|Relative SIMCE|Admisión · núcleo|Core admissions)/.test(aside?.textContent || ''),
      casesWorked: JSON.stringify(cases) === JSON.stringify(expected)
        && tabs[1]?.getAttribute('aria-selected') === 'true',
      posterWorked: Boolean(poster?.endsWith(expectedPoster)),
      insideArticle: Boolean(articleBox) && rootBox.left >= articleBox.left - tolerance
        && rootBox.right <= articleBox.right + tolerance,
      attributionPresent: Boolean(node.querySelector('.maplibregl-ctrl-attrib'))
        && (node.querySelector('.maplibregl-ctrl-attrib')?.textContent || '').includes('OpenStreetMap'),
      firaApplied: mapRootStyle.fontFamily.toLowerCase().includes('fira sans'),
      titleFontPx: parseFloat(titleStyle.fontSize),
      themeSurfaceValid: isLight
        ? background === 'rgb(251, 245, 232)'
        : background === 'rgb(13, 17, 38)',
      asideMinFontPx: asideFonts.length ? Math.min(...asideFonts) : 0,
      initializationScrollDeltaPx: initializationDelta,
      initializationVisualShiftPx: initializationVisualShift
    };
  }, {
    cases: selectedCases,
    expected: expectedCases,
    localized: localizedCases,
    poster: posterHref,
    selectedLocale: locale,
    tolerance: thresholds.geometryTolerancePx,
    initializationDelta: initializationScrollDeltaPx,
    initializationVisualShift: initializationVisualShiftPx
  });
}

async function auditMarketMapFallbacks(browser, base) {
  const scenarios = [
    { locale: 'es', mode: 'module-error' },
    { locale: 'en', mode: 'webgl-unavailable' }
  ];
  const audits = [];
  for (const scenario of scenarios) {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    if (scenario.mode === 'webgl-unavailable') {
      await context.addInitScript(() => {
        const original = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function getContext(type, ...args) {
          if (typeof type === 'string' && type.toLowerCase().includes('webgl')) return null;
          return original.call(this, type, ...args);
        };
      });
    }
    const page = await context.newPage();
    if (scenario.mode === 'module-error') {
      await page.route('**/assets/dist/thesis_post2_map/main-*.js', (route) => route.abort());
    }
    const response = await page.goto(base + routes[scenario.locale], { waitUntil: 'domcontentloaded' });
    const root = page.locator('[data-thesis-market-map]');
    await root.scrollIntoViewIfNeeded();
    await page.waitForFunction(
      () => document.querySelector('[data-thesis-market-map]')?.dataset.mapState === 'fallback',
      undefined,
      { timeout: 35_000 }
    );
    const measurement = await root.evaluate((node, payload) => {
      const status = node.querySelector('[data-market-map-status]')?.textContent?.trim() || '';
      const fallbackImage = node.querySelector('[data-market-map-fallback]');
      const poster = node.querySelector('[data-market-map-poster]');
      const tabs = [...node.querySelectorAll('[data-market-map-tab]')];
      const loadingPattern = payload.locale === 'es' ? /cargando/i : /loading/i;
      return {
        locale: payload.locale,
        mode: payload.mode,
        httpStatus: payload.httpStatus,
        state: node.dataset.mapState,
        tabListHidden: node.querySelector('.thesis-market-map__tabs')?.hidden === true,
        tabsDisabled: tabs.every((tab) => tab.disabled && tab.tabIndex === -1),
        canvasHidden: node.querySelector('[data-market-map-canvas]')?.hidden === true,
        asideHidden: node.querySelector('[data-market-map-aside]')?.hidden === true,
        statusResolved: status.length > 0 && !loadingPattern.test(status),
        posterAvailable: Boolean(poster?.getAttribute('href'))
          && fallbackImage?.complete === true && fallbackImage?.naturalWidth > 0
      };
    }, { ...scenario, httpStatus: response?.status() || 0 });
    measurement.failures = evaluateFallback(measurement);
    audits.push(measurement);
    await context.close();
  }
  return audits;
}

async function auditSvgAssets(browser, base) {
  mkdirSync(screenshotDir, { recursive: true });
  const context = await browser.newContext({ viewport: { width: 1200, height: 720 } });
  const page = await context.newPage();
  const audits = [];
  try {
    for (const locale of Object.keys(routes)) {
      for (const name of svgNames) {
        const asset = `/assets/images/extender-tesis-no-es-agregar-anos/estilizada-${name}-${locale}.svg`;
        const response = await page.goto(base + asset, { waitUntil: 'load' });
        const measurement = await page.evaluate(({ assetPath, minimumFont }) => {
          const svg = document.querySelector('svg');
          const viewBox = svg?.viewBox.baseVal;
          const nodes = [...document.querySelectorAll('svg text')].filter((node) => {
            const box = node.getBoundingClientRect();
            return box.width > 0 && box.height > 0;
          });
          const rows = nodes.map((node, index) => {
            const box = node.getBBox();
            return {
              index,
              text: (node.textContent || '').trim().slice(0, 80),
              x: box.x, y: box.y, width: box.width, height: box.height,
              right: box.x + box.width, bottom: box.y + box.height,
              font: parseFloat(getComputedStyle(node).fontSize)
            };
          });
          const overlaps = [];
          for (let left = 0; left < rows.length; left += 1) {
            for (let right = left + 1; right < rows.length; right += 1) {
              const a = rows[left];
              const b = rows[right];
              const overlap = a.x < b.right - 0.5 && a.right > b.x + 0.5
                && a.y < b.bottom - 0.5 && a.bottom > b.y + 0.5;
              if (overlap) overlaps.push([a.text, b.text]);
            }
          }
          return {
            asset: assetPath,
            hasAccessibleName: Boolean(svg?.querySelector('title')?.textContent?.trim())
              && Boolean(svg?.querySelector('desc')?.textContent?.trim()),
            textInsideViewBox: Boolean(viewBox) && rows.every((row) => row.x >= -2 && row.y >= -2
              && row.right <= viewBox.width + 2 && row.bottom <= viewBox.height + 2),
            textOverlaps: overlaps,
            minimumFontPx: rows.length ? Math.min(...rows.map((row) => row.font)) : minimumFont,
            textCount: rows.length
          };
        }, { assetPath: asset, minimumFont: thresholds.svgMinFontPx });
        measurement.httpStatus = response?.status() || 0;
        measurement.failures = evaluateSvgAudit(measurement);
        audits.push(measurement);
        if (name.startsWith('mapa-')) {
          await page.screenshot({ path: `${screenshotDir}/${locale}-${name}.png` });
        }
      }
    }
  } finally {
    await context.close();
  }
  return audits;
}

const browserExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);
const browser = await chromium.launch({
  headless: true,
  ...(browserExecutable ? { executablePath: browserExecutable } : {})
});
const results = [];
let svgAudits = [];
let fallbackAudits = [];

try {
  for (const [locale, route] of Object.entries(routes)) {
    for (const theme of ['light', 'academic-night']) {
      for (const viewport of viewports) {
        const context = await browser.newContext({ viewport });
        await context.addInitScript((selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme), theme);
        const page = await context.newPage();
        // Map tiles and analytics may keep network activity alive indefinitely.
        // Navigation readiness is the local DOM; component readiness is asserted
        // explicitly by exerciseMarketMap and exerciseCarousel below.
        const response = await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded' });
        const marketMap = await exerciseMarketMap(page, locale);
        const carousel = await exerciseCarousel(page, locale);
        await page.locator('details.thesis-stylized__data').evaluateAll((nodes) => {
          nodes.forEach((node) => { node.open = true; });
        });
        const authorImageLocator = page.locator('.thesis-author-case img');
        await authorImageLocator.scrollIntoViewIfNeeded();
        await page.waitForFunction(() => {
          const image = document.querySelector('.thesis-author-case img');
          return image?.complete && image.naturalWidth > 0;
        });

        const measurement = await page.evaluate((payload) => {
          const article = document.querySelector('.page__content');
          const stylized = article.querySelector('.evidence-carousel--stylized');
          const stylizedViewport = stylized.querySelector('[data-carousel-viewport]');
          const articleBox = article.getBoundingClientRect();
          const rootBox = stylized.getBoundingClientRect();
          const viewportBox = stylizedViewport.getBoundingClientRect();
          const headings = [...article.querySelectorAll('h2, h3')].map((node) => node.textContent.trim());
          const captions = [...article.querySelectorAll('figcaption')];
          const tables = [...article.querySelectorAll('table')];
          const stylizedDetails = article.querySelector('details.thesis-stylized__data');
          const authorCase = article.querySelector('.thesis-author-case');
          const authorImage = authorCase?.querySelector('img');
          const authorLink = authorImage?.closest('a');
          const authorBox = authorCase?.getBoundingClientRect();
          const authorFonts = authorCase
            ? [authorCase, ...authorCase.querySelectorAll('*')]
              .filter((element) => element.getBoundingClientRect().width > 0)
              .map((element) => parseFloat(getComputedStyle(element).fontSize))
              .filter(Number.isFinite)
            : [];
          const tabs = [...stylized.querySelectorAll('[data-carousel-dot]')];
          const tolerance = payload.geometryTolerancePx;
          const editorialClone = article.cloneNode(true);
          editorialClone.querySelectorAll('details').forEach((node) => node.remove());
          const visibleWords = (editorialClone.textContent.match(/\S+/g) || []).length;
          const proseBlockWidths = [...article.querySelectorAll(':scope > :is(p, ul, ol)')]
            .filter((node) => node.getBoundingClientRect().width > 0)
            .map((node) => node.getBoundingClientRect().width);
          return {
            locale: payload.locale,
            theme: payload.theme,
            viewport: payload.viewport,
            httpStatus: payload.httpStatus,
            titleMatches: document.title.includes(payload.expectedTitle),
            headingsPresent: payload.expectedHeadings.every((needle) => headings.some((heading) => heading.includes(needle))),
            documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + tolerance,
            article: { present: Boolean(article), width: articleBox.width },
            proseMeasure: {
              measuredBlocks: proseBlockWidths.length,
              maxBlockWidth: proseBlockWidths.length ? Math.max(...proseBlockWidths) : 0
            },
            fonts: {
              body: parseFloat(getComputedStyle(article).fontSize),
              caption: captions.length ? Math.min(...captions.map((node) => parseFloat(getComputedStyle(node).fontSize))) : 0
            },
            content: { visibleWords },
            retiredCarouselCount: article.querySelectorAll('.evidence-carousel--results').length,
            stylizedCarousel: {
              count: article.querySelectorAll('.evidence-carousel--stylized').length,
              enhanced: stylized.classList.contains('is-enhanced'),
              slideCount: stylized.querySelectorAll('[data-carousel-slide]').length,
              tabCount: tabs.length,
              tabsNamed: tabs.every((node) => (node.innerText || '').trim().length >= 4),
              mapsFirst: payload.initialKinds.slice(0, payload.expectedMapsFirst)
                .every((kind) => kind === 'map')
                && payload.initialKinds.slice(payload.expectedMapsFirst)
                  .every((kind) => kind !== 'map'),
              controlsAccessible: [...stylized.querySelectorAll('[data-carousel-previous], [data-carousel-next], [data-carousel-dot]')]
                .every((node) => Boolean(node.getAttribute('aria-label')?.trim())),
              viewportContained: viewportBox.left >= -tolerance
                && viewportBox.right <= document.documentElement.clientWidth + tolerance,
              rootInsideArticle: rootBox.left >= articleBox.left - tolerance && rootBox.right <= articleBox.right + tolerance,
              statusUpdated: (stylized.querySelector('[data-carousel-status]')?.textContent || '').trim() === payload.expectedStatus,
              keyboardAdvanced: stylized.querySelector('[data-carousel-dot="1"]')?.getAttribute('aria-current') === 'true'
            },
            authorCase: {
              present: Boolean(authorCase),
              insideArticle: Boolean(authorBox)
                && authorBox.left >= articleBox.left - tolerance
                && authorBox.right <= articleBox.right + tolerance,
              imageLoaded: Boolean(authorImage?.complete && authorImage.naturalWidth > 0),
              vectorTarget: Boolean(authorLink?.href.endsWith(`estilizada-mapa-el-salvador-${payload.locale}.svg`)),
              altPresent: Boolean(authorImage?.getAttribute('alt')?.trim()),
              minFontPx: authorFonts.length ? Math.min(...authorFonts) : 0
            },
            semanticStructure: {
              invalidCarouselArticleRoles: article.querySelectorAll('article[role="group"][aria-roledescription="slide"]').length,
              invalidDefinitionChildren: [...article.querySelectorAll('.thesis-author-case__facts > div')]
                .reduce((count, group) => count + [...group.children]
                  .filter((child) => !['DT', 'DD'].includes(child.tagName)).length, 0)
            },
            tables: {
              detailsOpen: stylizedDetails?.open === true,
              contained: tables.every((table) => {
                const wrapper = table.closest('.tabla-desliza');
                if (!wrapper) return true;
                const box = wrapper.getBoundingClientRect();
                const overflow = getComputedStyle(wrapper).overflowX;
                return box.left >= -tolerance
                  && box.right <= document.documentElement.clientWidth + tolerance
                  && (wrapper.scrollWidth <= wrapper.clientWidth + tolerance || ['auto', 'scroll'].includes(overflow))
                  && wrapper.getAttribute('role') === 'region'
                  && wrapper.getAttribute('tabindex') === '0'
                  && Boolean(wrapper.getAttribute('aria-label')?.trim());
              })
            },
            referencesPresent: headings.some((heading) => heading.includes(payload.expectedHeadings.at(-1)))
          };
        }, {
          locale, theme, viewport,
          httpStatus: response?.status() || 0,
          expectedTitle: expectedTitle[locale],
          expectedStatus: locale === 'es' ? 'Figura 2 de 5' : 'Figure 2 of 5',
          expectedHeadings: expectedHeadings[locale],
          expectedMapsFirst: thresholds.expectedMapsFirst,
          geometryTolerancePx: thresholds.geometryTolerancePx,
          initialKinds: carousel.initialKinds
        });
        measurement.stylizedFigures = carousel.figures;
        measurement.stylizedPopup = carousel.popup;
        measurement.marketMap = marketMap;
        measurement.failures = evaluateMeasurement(measurement);
        measurement.softWarnings = measurement.content.visibleWords > thresholds.targetVisibleWordsSoft
          ? ['post-above-soft-word-target']
          : [];
        results.push(measurement);
        if (theme === 'light' && [390, 1440, 1920].includes(viewport.width)) {
          mkdirSync(screenshotDir, { recursive: true });
          await page.locator('[data-thesis-market-map]').screenshot({
            path: `${screenshotDir}/${locale}-market-map-${viewport.width}.png`
          });
        }
        await context.close();
      }
    }
  }
  fallbackAudits = await auditMarketMapFallbacks(browser, baseUrl);
  svgAudits = await auditSvgAssets(browser, baseUrl);
} finally {
  await browser.close();
}

const failures = [
  ...results.flatMap((row) => row.failures.map((failure) => ({
    surface: 'page', locale: row.locale, theme: row.theme, viewport: row.viewport, failure,
    initializationScrollDeltaPx: row.marketMap.initializationScrollDeltaPx,
    initializationVisualShiftPx: row.marketMap.initializationVisualShiftPx
  }))),
  ...svgAudits.flatMap((row) => row.failures.map((failure) => ({
    surface: 'svg', asset: row.asset, failure, overlaps: row.textOverlaps
  }))),
  ...fallbackAudits.flatMap((row) => row.failures.map((failure) => ({
    surface: 'fallback', locale: row.locale, mode: row.mode, failure
  })))
];
const report = {
  status: failures.length ? 'FAIL' : 'PASS',
  baseUrl,
  thresholds,
  pageCases: results.length,
  svgCases: svgAudits.length,
  fallbackCases: fallbackAudits.length,
  requiredPageCases: 24,
  requiredFallbackCases: 2,
  screenshots: screenshotDir,
  failures,
  softWarnings: results.flatMap((row) => row.softWarnings.map((warning) => ({
    locale: row.locale, theme: row.theme, viewport: row.viewport, warning,
    visibleWords: row.content.visibleWords, target: thresholds.targetVisibleWordsSoft
  }))),
  ...(summaryOnly ? {} : { results, svgAudits, fallbackAudits })
};
console.log(JSON.stringify(report, null, 2));
process.exit(failures.length ? 1 : 0);
