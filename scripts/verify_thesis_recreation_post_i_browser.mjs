#!/usr/bin/env node
import { createRequire } from 'node:module';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = dirname(here);
const args = process.argv.slice(2);
const valueAfter = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};
const fixture = valueAfter('--fixture');
const baseUrl = (valueAfter('--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');

const thresholds = {
  geometryTolerance: 1.5,
  carouselTitleMax: 24.5,
  slideTitleMax: 20.5,
  bodyMin: 15.5,
  controlMin: 44,
  dotMin: 24,
  desktopPipelineViewportRatioMax: 1.0,
  mobilePipelineViewportRatioMax: 1.5
};

function evaluateMeasurement(row) {
  const failures = [];
  if (row.documentOverflow) failures.push('document-overflow');
  if (row.viewport.width >= 768) {
    if (row.carousel.left < row.article.left - thresholds.geometryTolerance) failures.push('carousel-left-overflow');
    if (row.carousel.right > row.article.right + thresholds.geometryTolerance) failures.push('carousel-right-overflow');
  }
  if (row.fonts.carouselTitle > thresholds.carouselTitleMax) failures.push('carousel-title-too-large');
  if (row.fonts.slideTitle > thresholds.slideTitleMax) failures.push('slide-title-too-large');
  if (row.fonts.body < thresholds.bodyMin) failures.push('carousel-body-too-small');
  for (const [name, box] of Object.entries(row.controls)) {
    const minimum = name === 'dot' ? thresholds.dotMin : thresholds.controlMin;
    if (box.width + 0.01 < minimum || box.height + 0.01 < minimum) failures.push(`${name}-target-too-small`);
  }
  const heightRatio = row.pipeline.height / row.viewport.height;
  const limit = row.viewport.width < 768
    ? thresholds.mobilePipelineViewportRatioMax
    : thresholds.desktopPipelineViewportRatioMax;
  if (heightRatio > limit) failures.push('pipeline-too-tall');
  if (!row.pipeline.loaded) failures.push('pipeline-not-loaded');
  if (!row.pipeline.beforeFirstSubheading) failures.push('pipeline-misplaced');
  if (row.pipeline.count !== 1) failures.push('pipeline-count');
  if (!row.imagesLoaded) failures.push('carousel-image-not-loaded');
  if (row.media.imageCount !== 12 || row.media.popupLinkCount !== 12) failures.push('carousel-popup-link-count');
  if (row.media.fullSizeLinkCount !== 12 || !row.media.fullSizeLinksValid) failures.push('carousel-full-size-link');
  if (!row.media.cropFree || !row.media.aspectSafe) failures.push('carousel-image-cropped');
  if (!row.interaction.end || !row.interaction.home || !row.interaction.next) failures.push('carousel-interaction');
  if (!row.interaction.popup || !row.interaction.popupImageLoaded) failures.push('carousel-popup-missing');
  return failures;
}

if (fixture) {
  if (!['baseline', 'media-negative'].includes(fixture)) throw new Error(`Unknown fixture: ${fixture}`);
  const path = join(root, 'docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f3-baseline.json');
  const source = JSON.parse(readFileSync(path, 'utf8'));
  const row = {
    locale: 'es', theme: 'light', viewport: source.viewport,
    documentOverflow: false,
    article: { left: source.article.x, right: source.article.x + source.article.width },
    carousel: { left: source.carousel.x, right: source.carousel.x + source.carousel.width },
    fonts: {
      carouselTitle: source.typography_px.carousel_title,
      slideTitle: source.typography_px.slide_title,
      body: source.typography_px.body
    },
    controls: {
      previous: { width: source.controls_px.arrow_width, height: source.controls_px.arrow_height },
      next: { width: source.controls_px.arrow_width, height: source.controls_px.arrow_height },
      dot: { width: source.controls_px.dot_width, height: source.controls_px.dot_height }
    },
    pipeline: {
      width: source.pipeline.desktop.rendered_width,
      height: source.pipeline.desktop.rendered_height,
      loaded: true,
      beforeFirstSubheading: false,
      count: 1
    },
    imagesLoaded: true,
    media: {
      imageCount: 12,
      popupLinkCount: 12,
      fullSizeLinkCount: fixture === 'media-negative' ? 0 : 12,
      fullSizeLinksValid: fixture !== 'media-negative',
      cropFree: fixture !== 'media-negative',
      aspectSafe: true
    },
    interaction: {
      end: true,
      home: true,
      next: true,
      popup: fixture !== 'media-negative',
      popupImageLoaded: fixture !== 'media-negative'
    }
  };
  const failures = evaluateMeasurement(row);
  console.log(JSON.stringify({ status: failures.length ? 'fail' : 'pass', fixture: path, failures, measurement: row }, null, 2));
  process.exit(failures.length ? 1 : 0);
}

const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || '/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/node_modules/playwright';
if (!existsSync(playwrightPath)) {
  console.error(`FAIL: Playwright not found at ${playwrightPath}`);
  process.exit(2);
}
const { chromium } = createRequire(import.meta.url)(playwrightPath);
const routes = {
  es: '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/',
  en: '/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/'
};
const viewports = [
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 1366, height: 768 },
  { width: 1440, height: 900 }
];
const browser = await chromium.launch({ headless: true });
const results = [];

try {
  for (const [locale, route] of Object.entries(routes)) {
    for (const theme of ['light', 'academic-night']) {
      for (const viewport of viewports) {
        const context = await browser.newContext({ viewport });
        await context.addInitScript((selectedTheme) => localStorage.setItem('3cucharadas-theme', selectedTheme), theme);
        const page = await context.newPage();
        await page.goto(baseUrl + route, { waitUntil: 'networkidle' });
        await page.evaluate(() => {
          const pipeline = document.querySelector('.recreation-pipeline-figure img');
          if (pipeline) pipeline.loading = 'eager';
        });
        await page.waitForFunction(() => {
          const pipeline = document.querySelector('.recreation-pipeline-figure img');
          return pipeline && pipeline.complete && pipeline.naturalWidth > 0;
        }, null, { timeout: 15_000 });
        await page.locator('[data-evidence-carousel]').scrollIntoViewIfNeeded();
        await page.evaluate(() => {
          for (const image of document.querySelectorAll('[data-evidence-carousel] img')) image.loading = 'eager';
        });
        await page.waitForFunction(() => [...document.querySelectorAll('[data-evidence-carousel] img')].every((image) => image.complete && image.naturalWidth > 0), null, { timeout: 15_000 });
        const viewportNode = page.locator('[data-carousel-viewport]');
        await viewportNode.focus();
        await page.keyboard.press('End');
        await page.waitForTimeout(250);
        const atEnd = await page.locator('[data-carousel-status]').textContent();
        const nextDisabled = await page.locator('[data-carousel-next]').isDisabled();
        await page.keyboard.press('Home');
        await page.waitForTimeout(250);
        const atHome = await page.locator('[data-carousel-status]').textContent();
        await page.locator('[data-carousel-next]').click();
        await page.waitForTimeout(250);
        const afterNext = await page.locator('[data-carousel-status]').textContent();
        await page.locator('[data-carousel-dot="4"]').click();
        await page.waitForTimeout(250);
        await page.locator('[data-carousel-slide][data-slide-id="table-08-rounding"] [data-carousel-popup]').last().click();
        const popup = page.locator('.mfp-wrap');
        await popup.waitFor({ state: 'visible', timeout: 5_000 });
        const popupOpened = await popup.isVisible();
        const popupImageLoaded = await page.locator('.mfp-img').evaluate((image) => image.complete && image.naturalWidth > 0);
        await page.keyboard.press('Escape');
        await popup.waitFor({ state: 'hidden', timeout: 5_000 });
        const measurement = await page.evaluate(({ locale, theme, viewport, interaction, geometryTolerance }) => {
          const rect = (element) => {
            const box = element.getBoundingClientRect();
            return { left: box.left, right: box.right, width: box.width, height: box.height };
          };
          const carousel = document.querySelector('[data-evidence-carousel]');
          const article = document.querySelector('.page__content');
          const pipeline = document.querySelector('.recreation-pipeline-figure img');
          const pipelineFigure = document.querySelector('.recreation-pipeline-figure');
          const spoon2 = locale === 'es' ? 'Cucharada 2' : 'Spoonful 2';
          const heading = [...document.querySelectorAll('.page__content h2')].find((node) => node.textContent.includes(spoon2));
          const nextHeading = heading ? [...document.querySelectorAll('.page__content h3')].find((node) => node.compareDocumentPosition(heading) & Node.DOCUMENT_POSITION_PRECEDING) : null;
          const styleSize = (selector) => parseFloat(getComputedStyle(document.querySelector(selector)).fontSize);
          const documentRoot = document.documentElement;
          const pipelineRect = rect(pipeline);
          const imageRows = [...carousel.querySelectorAll('.evidence-carousel__media img')].map((image) => {
            const imageBox = image.getBoundingClientRect();
            const mediaBox = image.closest('.evidence-carousel__media').getBoundingClientRect();
            const renderedRatio = imageBox.width / imageBox.height;
            const naturalRatio = image.naturalWidth / image.naturalHeight;
            return {
              insideFrame:
                imageBox.left >= mediaBox.left - geometryTolerance
                && imageBox.right <= mediaBox.right + geometryTolerance
                && imageBox.top >= mediaBox.top - geometryTolerance
                && imageBox.bottom <= mediaBox.bottom + geometryTolerance,
              aspectDrift: Math.abs(renderedRatio - naturalRatio) / naturalRatio
            };
          });
          const popupLinks = [...carousel.querySelectorAll('[data-carousel-popup]')];
          const fullSizeLinks = [...carousel.querySelectorAll('[data-carousel-hd-link]')];
          return {
            locale, theme, viewport,
            documentOverflow: documentRoot.scrollWidth > documentRoot.clientWidth + 1,
            article: rect(article),
            carousel: rect(carousel),
            fonts: {
              carouselTitle: styleSize('.evidence-carousel__header h3'),
              slideTitle: styleSize('.evidence-carousel__slide h4'),
              body: styleSize('.evidence-carousel__slide')
            },
            controls: {
              previous: rect(document.querySelector('[data-carousel-previous]')),
              next: rect(document.querySelector('[data-carousel-next]')),
              dot: rect(document.querySelector('[data-carousel-dot]'))
            },
            pipeline: {
              ...pipelineRect,
              loaded: pipeline.complete && pipeline.naturalWidth > 0,
              beforeFirstSubheading: Boolean(pipelineFigure && nextHeading && (pipelineFigure.compareDocumentPosition(nextHeading) & Node.DOCUMENT_POSITION_FOLLOWING)),
              count: document.querySelectorAll('.recreation-pipeline-figure').length
            },
            imagesLoaded: [...carousel.querySelectorAll('img')].every((image) => image.complete && image.naturalWidth > 0),
            media: {
              imageCount: imageRows.length,
              popupLinkCount: popupLinks.length,
              fullSizeLinkCount: fullSizeLinks.length,
              fullSizeLinksValid: fullSizeLinks.every((link) =>
                link.target === '_blank'
                && link.relList.contains('noopener')
                && popupLinks.some((popupLink) => popupLink.href === link.href)
              ),
              cropFree: imageRows.every((row) => row.insideFrame),
              aspectSafe: imageRows.every((row) => row.aspectDrift < 0.01)
            },
            interaction
          };
        }, {
          locale, theme, viewport,
          geometryTolerance: thresholds.geometryTolerance,
          interaction: {
            end: /6\s*(?:de|of)\s*6/i.test(atEnd || '') && nextDisabled,
            home: /1\s*(?:de|of)\s*6/i.test(atHome || ''),
            next: /2\s*(?:de|of)\s*6/i.test(afterNext || ''),
            popup: popupOpened,
            popupImageLoaded
          }
        });
        measurement.failures = evaluateMeasurement(measurement);
        results.push(measurement);
        await context.close();
      }
    }
  }
} finally {
  await browser.close();
}

const failures = results.flatMap((row) => row.failures.map((failure) => ({ locale: row.locale, theme: row.theme, viewport: row.viewport, failure })));
console.log(JSON.stringify({ status: failures.length ? 'fail' : 'pass', baseUrl, thresholds, cases: results.length, failures, results }, null, 2));
process.exit(failures.length ? 1 : 0);
