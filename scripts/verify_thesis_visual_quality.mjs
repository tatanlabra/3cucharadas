#!/usr/bin/env node

// Rendered visual QA for the bilingual III–IV articles and methods annexes.
// This observes browser output; the scientific and artifact contracts live in
// verify_thesis_post{3,4}.rb and verify_thesis_series_browser.mjs.
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(scriptDir, '..');
const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
const prefix = '/datos/educacion/politica-publica/';
const routes = [
  { id: 'iii-article', slug: 'costos-cierre-escolar-trayectorias', kind: 'article', figures: 2 },
  { id: 'iii-annex', slug: 'costos-cierre-escolar-trayectorias', kind: 'annex', figures: 2 },
  { id: 'iv-article', slug: 'cierre-escolar-educacion-superior-causal-ml', kind: 'article', figures: 1 },
  { id: 'iv-annex', slug: 'cierre-escolar-educacion-superior-causal-ml', kind: 'annex', figures: 2 }
];
const locales = ['es', 'en'];
const themes = ['light', 'academic-night'];
const widths = [320, 390, 768, 1440];
const readOption = (args, flag) => {
  const index = args.indexOf(flag);
  return index < 0 ? null : args[index + 1];
};
const routePath = (entry, locale) => `${locale === 'en' ? '/en' : ''}${prefix}${entry.slug}/`
  + (entry.kind === 'annex' ? 'anexo-metodologico/' : '');
const round = (number) => Math.round(number * 100) / 100;

function evaluate(row) {
  const failures = [];
  if (row.httpStatus !== 200) failures.push('route-status');
  if (row.themeValue !== row.expectedTheme) failures.push('theme-state');
  if (row.documentOverflow || row.clipped.length) failures.push('content-clipping');
  if (!row.fonts.bodyFira || !row.fonts.faceLoaded || row.fonts.bodyPx < 16)
    failures.push('font-loading-or-size');
  if (row.textContrast.unmeasured || row.textContrast.failures.length)
    failures.push('text-contrast');
  if (row.figureCount !== row.expectedFigures || row.imagesFailed.length
    || row.figureSourcesFailed.length) failures.push('image-or-variant');
  if (row.svgContrast.unmeasured || row.svgContrast.failures.length)
    failures.push('svg-contrast');
  if (row.svgContrast.minRenderedTextPx < 9) failures.push('svg-text-size');
  if (row.criticalErrors.length) failures.push('console-or-network');
  if (row.screenshotError) failures.push('screenshot');
  return failures;
}

async function inspect(browser, baseUrl, entry, locale, theme, width, screenshotDir, fixture = null) {
  const path = routePath(entry, locale);
  const viewport = { width, height: width < 768 ? 844 : 1000 };
  const context = await browser.newContext({ viewport, reducedMotion: 'reduce', colorScheme: 'light' });
  await context.addInitScript((mode) => localStorage.setItem('3cucharadas-theme', mode), theme);
  const page = await context.newPage();
  const criticalErrors = [];
  const externalErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error' && !message.text().includes('favicon'))
      criticalErrors.push(`console:${message.text()}`);
  });
  page.on('pageerror', (error) => criticalErrors.push(`pageerror:${error.message}`));
  page.on('requestfailed', (request) => {
    const target = request.url();
    const record = `request:${target}:${request.failure()?.errorText || 'failed'}`;
    (target.startsWith(baseUrl) ? criticalErrors : externalErrors).push(record);
  });
  page.on('response', (response) => {
    if (response.status() >= 400 && !response.url().includes('favicon')) {
      const record = `http-${response.status()}:${response.url()}`;
      (response.url().startsWith(baseUrl) ? criticalErrors : externalErrors).push(record);
    }
  });
  try {
    const response = await page.goto(baseUrl + path, { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await page.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;transition-duration:0s!important;scroll-behavior:auto!important;caret-color:transparent!important}' });
    await page.evaluate(async () => {
      await document.fonts.ready;
      const images = [...document.images].filter((image) =>
        image.hasAttribute('src') || image.hasAttribute('srcset') || image.currentSrc);
      images.forEach((image) => { image.loading = 'eager'; });
      await Promise.all(images.map((image) => image.complete ? null : new Promise((done) => {
        const timer = setTimeout(done, 12_000);
        image.addEventListener('load', () => { clearTimeout(timer); done(); }, { once: true });
        image.addEventListener('error', () => { clearTimeout(timer); done(); }, { once: true });
      })));
    });
    if (fixture === 'low-contrast') await page.evaluate(() => {
      const paragraph = document.querySelector('.page__content > p');
      if (!paragraph) throw new Error('fixture target paragraph missing');
      paragraph.style.setProperty('color', '#ffffff', 'important');
      paragraph.style.setProperty('background-color', '#ffffff', 'important');
    });
    await page.waitForTimeout(150);
    const measurements = await page.evaluate(async (expected) => {
      const parseColor = (value) => {
        const match = value?.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)$/i);
        if (!match) return null;
        return [Number(match[1]), Number(match[2]), Number(match[3]), match[4] === undefined ? 1 : Number(match[4])];
      };
      const parseHex = (value) => {
        const match = value?.trim().match(/^#([0-9a-f]{6})$/i);
        return match ? [1, 3, 5].map((start) => parseInt(match[1].slice(start - 1, start + 1), 16)) : null;
      };
      const composite = (front, back) => front.slice(0, 3).map((part, index) =>
        front[3] * part + (1 - front[3]) * back[index]);
      const background = (element) => {
        const chain = [];
        for (let current = element; current; current = current.parentElement) chain.unshift(current);
        let color = [255, 255, 255];
        let uncertain = false;
        for (const node of chain) {
          const style = getComputedStyle(node);
          const next = parseColor(style.backgroundColor);
          if (next) color = composite(next, color);
          else uncertain = true;
          if (style.backgroundImage !== 'none') uncertain = true;
        }
        return { color, uncertain };
      };
      const luminance = (rgb) => {
        const transformed = rgb.map((part) => {
          const normalized = part / 255;
          return normalized <= 0.04045 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
        });
        return transformed[0] * 0.2126 + transformed[1] * 0.7152 + transformed[2] * 0.0722;
      };
      const contrast = (front, back) => {
        const first = luminance(front), second = luminance(back);
        return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
      };
      const content = document.querySelector('.page__content');
      const candidates = [document.querySelector('.page__title'),
        ...(content?.querySelectorAll('p,h2,h3,h4,li,th,td,figcaption,a,code') || [])].filter(Boolean);
      const contrastRows = candidates.filter((element) => {
        const style = getComputedStyle(element), rect = element.getBoundingClientRect();
        const directText = [...element.childNodes].filter((node) => node.nodeType === Node.TEXT_NODE)
          .map((node) => node.textContent).join('').trim();
        return directText.length >= 2 && rect.width > 0 && rect.height > 0
          && style.display !== 'none' && style.visibility === 'visible'
          && !element.closest('[aria-hidden="true"]');
      }).map((element) => {
        const style = getComputedStyle(element);
        const foreground = parseColor(style.color);
        const surface = background(element);
        const renderedColor = foreground ? composite(foreground, surface.color) : null;
        const ratio = renderedColor ? contrast(renderedColor, surface.color) : null;
        const size = parseFloat(style.fontSize), weight = parseInt(style.fontWeight, 10) || 400;
        const required = size >= 24 || (size >= 18.66 && weight >= 700) ? 3 : 4.5;
        return { tag: element.tagName.toLowerCase(), id: element.id || '',
          excerpt: element.textContent.trim().slice(0, 60), ratio: ratio === null ? null : Math.round(ratio * 100) / 100,
          required, fontPx: size, foreground: style.color,
          background: surface.color.map((part) => Math.round(part)), uncertain: surface.uncertain };
      });
      const contrastFailures = contrastRows.filter((row) => row.ratio === null || row.ratio + 0.01 < row.required);
      const figures = [...(content?.querySelectorAll('figure.post3-figure') || [])];
      const imageRows = [...document.images].filter((image) =>
        image.hasAttribute('src') || image.hasAttribute('srcset') || image.currentSrc).map((image) => ({
        alt: image.alt.slice(0, 60), src: image.currentSrc || image.src,
        markup: image.outerHTML.slice(0, 180),
        complete: image.complete && image.naturalWidth > 0 && image.naturalHeight > 0
      }));
      const expectedVariant = `${expected.theme === 'academic-night' ? '-dark' : '-light'}${expected.width < 768 ? '-mobile' : ''}.svg`;
      const figureSourcesFailed = figures.map((figure) => figure.querySelector('img.post3-theme-image'))
        .filter((image) => !image || !(image.currentSrc || '').endsWith(expectedVariant))
        .map((image) => image?.currentSrc || 'missing image');
      const svgRows = await Promise.all(figures.map(async (figure) => {
        const image = figure.querySelector('img.post3-theme-image');
        if (!image?.currentSrc) return { id: figure.id, unmeasured: true, reason: 'image missing' };
        try {
          const response = await fetch(image.currentSrc);
          if (!response.ok) return { id: figure.id, unmeasured: true, reason: `svg http ${response.status}` };
          const xml = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
          if (xml.querySelector('parsererror')) return { id: figure.id, unmeasured: true, reason: 'svg parse' };
          const canvas = xml.querySelector('g#patch_1 path')?.getAttribute('style')?.match(/(?:^|;)\s*fill:\s*(#[0-9a-f]{6})/i)?.[1];
          const bg = parseHex(canvas);
          const viewWidth = Number(xml.documentElement.getAttribute('viewBox')?.split(/\s+/)?.[2]);
          const renderedWidth = image.getBoundingClientRect().width;
          if (!bg || !viewWidth || !renderedWidth) return { id: figure.id, unmeasured: true, reason: 'svg geometry' };
          const labels = [...xml.querySelectorAll('text')].map((text) => {
            const style = text.getAttribute('style') || '';
            const fill = style.match(/(?:^|;)\s*fill:\s*(#[0-9a-f]{6})/i)?.[1];
            const font = Number(style.match(/(?:^|;)\s*font-size:\s*([\d.]+)px/i)?.[1]);
            const fg = parseHex(fill);
            return { text: text.textContent.trim().slice(0, 50),
              ratio: fg ? Math.round(contrast(fg, bg) * 100) / 100 : null,
              renderedPx: font ? Math.round(font * renderedWidth / viewWidth * 100) / 100 : null };
          });
          return { id: figure.id, unmeasured: labels.length === 0 || labels.some((label) => label.ratio === null
            || label.renderedPx === null), canvas, labels: labels.length,
          minContrast: Math.min(...labels.map((label) => label.ratio ?? 0)),
          minRenderedTextPx: Math.min(...labels.map((label) => label.renderedPx ?? 0)),
          failures: labels.filter((label) => label.ratio !== null && label.ratio < 4.5).slice(0, 10) };
        } catch (error) { return { id: figure.id, unmeasured: true, reason: error.message }; }
      }));
      const clipped = [...(content?.querySelectorAll('figure.post3-figure,.tabla-desliza,.notice--primary,nav.thesis-series-nav') || [])]
        .filter((element) => {
          const box = element.getBoundingClientRect();
          return box.width && (box.left < -2 || box.right > innerWidth + 2);
        }).map((element) => `${element.tagName.toLowerCase()}#${element.id || ''}`);
      const contentStyle = content ? getComputedStyle(content) : null;
      const loadedFira = [...document.fonts].some((face) => face.family.replace(/["']/g, '') === 'Fira Sans'
        && face.status === 'loaded');
      return { themeValue: document.documentElement.getAttribute('data-theme') || 'light',
        documentOverflow: document.documentElement.scrollWidth > innerWidth + 2,
        clipped,
        fonts: { bodyFira: Boolean(contentStyle?.fontFamily.includes('Fira Sans')),
          bodyPx: contentStyle ? parseFloat(contentStyle.fontSize) : 0,
          faceLoaded: loadedFira,
          loadedFaces: [...document.fonts].filter((face) => face.status === 'loaded').map((face) => face.family) },
        textContrast: { count: contrastRows.length, unmeasured: contrastRows.length === 0
          || contrastRows.some((row) => row.ratio === null),
        minimum: Math.min(...contrastRows.map((row) => row.ratio ?? 0)),
        uncertainBackgrounds: contrastRows.filter((row) => row.uncertain).length,
        failures: contrastFailures.slice(0, 20) },
        figureCount: figures.length,
        imagesFailed: imageRows.filter((image) => !image.complete),
        figureSourcesFailed,
        svgContrast: { count: svgRows.length, unmeasured: svgRows.some((row) => row.unmeasured),
          minimum: Math.min(...svgRows.map((row) => row.minContrast ?? 0)),
          minRenderedTextPx: Math.min(...svgRows.map((row) => row.minRenderedTextPx ?? 0)),
          failures: svgRows.flatMap((row) => row.failures || []).slice(0, 20), figures: svgRows } };
    }, { theme, width });
    const row = { route: path, id: entry.id, locale, theme, expectedTheme: theme, width,
      httpStatus: response?.status() || 0, expectedFigures: entry.figures,
      criticalErrors, externalErrors, ...measurements, screenshots: [], screenshotError: null };
    if (screenshotDir) {
      try {
        const name = `${entry.id}-${locale}-${theme}-${width}`;
        await page.evaluate(() => window.scrollTo(0, 0));
        const top = resolve(screenshotDir, `${name}-top.png`);
        await page.screenshot({ path: top, animations: 'disabled' });
        row.screenshots.push(top);
        if (width === 320 || width === 1440) {
          const figure = page.locator('.page__content figure.post3-figure').first();
          if (await figure.count()) {
            const figurePath = resolve(screenshotDir, `${name}-figure.png`);
            await figure.screenshot({ path: figurePath, animations: 'disabled' });
            row.screenshots.push(figurePath);
          }
        }
      } catch (error) { row.screenshotError = error.message; }
    }
    row.failures = evaluate(row);
    return row;
  } finally { await context.close(); }
}

async function main() {
  const args = process.argv.slice(2);
  const baseUrl = (readOption(args, '--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
  const reportPath = readOption(args, '--report');
  const screenshotDir = readOption(args, '--screenshot-dir');
  const fixture = readOption(args, '--fixture');
  if (!/^https?:\/\//.test(baseUrl) || !existsSync(playwrightPath)
    || (fixture && fixture !== 'low-contrast')) {
    console.error(JSON.stringify({ status: 'ERROR', error: 'invalid base URL, Playwright path or fixture' }));
    process.exitCode = 2;
    return;
  }
  if (screenshotDir) mkdirSync(screenshotDir, { recursive: true });
  const playwright = createRequire(import.meta.url)(playwrightPath);
  const executable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
    || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);
  const browser = await playwright.chromium.launch({ headless: true,
    ...(executable ? { executablePath: executable } : {}), args: ['--no-sandbox'] });
  let report;
  try {
    if (fixture) {
      const entry = routes[0];
      const baseline = await inspect(browser, baseUrl, entry, 'es', 'light', 390, null);
      const mutant = await inspect(browser, baseUrl, entry, 'es', 'light', 390, null, fixture);
      const discriminates = baseline.failures.length === 0 && mutant.failures.includes('text-contrast')
        && mutant.textContrast.failures.some((failure) => failure.ratio === 1);
      report = { status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture,
        baseline: { failures: baseline.failures, minimum: baseline.textContrast.minimum,
          sampled: baseline.textContrast.count,
          contrastFailures: baseline.textContrast.failures.slice(0, 5),
          imagesFailed: baseline.imagesFailed, figureSourcesFailed: baseline.figureSourcesFailed },
        mutant: { failures: mutant.failures, minimum: mutant.textContrast.minimum,
          samples: mutant.textContrast.failures.slice(0, 3) } };
      process.exitCode = discriminates ? 1 : 2;
    } else {
      const rows = [];
      for (const entry of routes) for (const locale of locales) for (const theme of themes)
        for (const width of widths) rows.push(await inspect(browser, baseUrl, entry, locale, theme,
          width, screenshotDir));
      report = { status: rows.every((row) => row.failures.length === 0) ? 'PASS' : 'FAIL',
        testedAt: new Date().toISOString(), baseUrl, matrix: '8 routes x 2 themes x 4 widths',
        rows, summary: { rows: rows.length, failed: rows.filter((row) => row.failures.length).length,
          screenshots: rows.reduce((total, row) => total + row.screenshots.length, 0),
          minTextContrast: round(Math.min(...rows.map((row) => row.textContrast.minimum))),
          minSvgContrast: round(Math.min(...rows.map((row) => row.svgContrast.minimum))),
          minSvgTextPx: round(Math.min(...rows.map((row) => row.svgContrast.minRenderedTextPx))) } };
      process.exitCode = report.status === 'PASS' ? 0 : 1;
    }
  } finally { await browser.close(); }
  if (reportPath) {
    mkdirSync(dirname(resolve(reportPath)), { recursive: true });
    writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  }
  console.log(JSON.stringify(report.status === 'PASS' || report.status === 'FAIL'
    ? { status: report.status, ...report.summary,
      failedRows: report.rows.filter((row) => row.failures.length).map((row) => ({
        route: row.route, theme: row.theme, width: row.width, failures: row.failures,
        textContrast: row.textContrast.failures.slice(0, 2), svgContrast: row.svgContrast.failures.slice(0, 2),
        criticalErrors: row.criticalErrors.slice(0, 2) })) }
    : report));
}

main().catch((error) => {
  console.error(JSON.stringify({ status: 'ERROR', error: error.stack || error.message }));
  process.exitCode = 2;
});
