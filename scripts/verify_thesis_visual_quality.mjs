#!/usr/bin/env node

// Rendered visual QA for the bilingual III–IV articles and methods annexes.
// This observes browser output; the scientific and artifact contracts live in
// verify_thesis_post{3,4}.rb and verify_thesis_series_browser.mjs.
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
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
const widths = [320, 390, 768, 1024, 1440];
const readOption = (args, flag) => {
  const index = args.indexOf(flag);
  return index < 0 ? null : args[index + 1];
};
const readOptions = (args, flag) => args.flatMap((arg, index) =>
  arg === flag && args[index + 1] ? [args[index + 1]] : []);
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
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
  if (row.id.startsWith('iv-') && (row.svgGeometry.unmeasured || row.svgGeometry.failures.length))
    failures.push('svg-label-geometry');
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
  if (fixture === 'broken-active-svg') {
    await page.route('**/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg',
      (request) => request.abort('failed'));
  }
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
      const round = (number) => Math.round(number * 100) / 100;
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
      const figureSources = figures.map((figure) => figure.querySelector('img.post3-theme-image')?.currentSrc || '');
      const ladderImage = figures.find((figure) => figure.id === 'fig-post4-1')
        ?.querySelector('img.post3-theme-image');
      const svgLayout = ladderImage && content ? {
        imageWidth: round(ladderImage.getBoundingClientRect().width),
        contentWidth: round(content.getBoundingClientRect().width),
        fillRatio: content.getBoundingClientRect().width
          ? round(ladderImage.getBoundingClientRect().width / content.getBoundingClientRect().width)
          : 0 } : { fillRatio: expected.entryId === 'iv-article' ? 0 : 1 };
      const measureFigureGeometry = async (xml, renderedWidth, figureId) => {
        const contracts = {
          'fig-post4-1': { family: 'selection', roles: {
            value: [/^selection-value-[ab]-[1-5]$/, 10],
            rung: [/^selection-rung-[ab]-[1-5]$/, 10],
            ci: [/^selection-ci-[ab]-[1-5]$/, 10],
            point: [/^selection-point-[ab]-[1-5]$/, 10],
            spine: [/^selection-spine-[ab]-(?:top|right|bottom|left)$/, 8] },
          textRoles: ['value', 'rung'], markRoles: ['ci', 'point', 'spine'] },
          'fig-post4-2': { family: 'longitudinal', roles: {
            value: [/^longitudinal-value-[01]-[1-3]$/, 6],
            category: [/^longitudinal-category-[01]-[1-3]$/, 6],
            bar: [/^longitudinal-bar-[01]-[1-3]$/, 6],
            spine: [/^longitudinal-spine-[01]-(?:top|right|bottom|left)$/, 8] },
          textRoles: ['value', 'category'], markRoles: ['bar', 'spine'] },
          'fig-post4-3': { family: 'causal', roles: {
            gateValue: [/^causal-gate-value-[a-z0-9_]+-[04]$/, 6],
            gateLine: [/^causal-gate-line-[a-z0-9_]+-[0-3]$/, 12],
            paesValue: [/^causal-paes-value-[0-2]-[1-4]$/, 12],
            category: [/^causal-category-[01]-[1-5]$/, 9],
            paesBar: [/^causal-paes-bar-[0-2]-[1-4]$/, 12],
            spine: [/^causal-spine-[01]-(?:top|right|bottom|left)$/, 8] },
          textRoles: ['gateValue', 'paesValue', 'category'], markRoles: ['gateLine', 'paesBar', 'spine'] }
        };
        const contract = contracts[figureId];
        if (!contract) return { unmeasured: true, reason: `unknown figure ${figureId}`, failures: [] };
        const svg = document.importNode(xml.documentElement, true);
        const holder = document.createElement('div');
        holder.style.cssText = `position:fixed;left:-10000px;top:0;width:${renderedWidth}px;visibility:hidden;pointer-events:none`;
        svg.style.width = `${renderedWidth}px`;
        svg.style.height = 'auto';
        holder.append(svg);
        document.body.append(holder);
        try {
          await document.fonts.ready;
          const idNodes = [...svg.querySelectorAll('[id]')];
          const ids = Object.entries(contract.roles).map(([kind, [pattern]]) =>
            [kind, idNodes.filter((node) => pattern.test(node.id))]);
          const byKind = Object.fromEntries(ids);
          const counts = Object.fromEntries(ids.map(([kind, nodes]) => [kind, nodes.length]));
          if (Object.entries(contract.roles).some(([kind, [, count]]) => counts[kind] !== count))
            return { unmeasured: true, reason: `${contract.family} QA IDs missing`, counts, failures: [] };
          const mutation = {
            'svg-value-overlap': ['fig-post4-1', 'selection-value-a-1', 'selection-ci-a-1'],
            'svg-longitudinal-overlap': ['fig-post4-2', 'longitudinal-value-0-1', 'longitudinal-bar-1-1'],
            'svg-causal-overlap': ['fig-post4-3', 'causal-paes-value-1-1', 'causal-paes-bar-0-1'],
            'svg-own-bar-overlap': ['fig-post4-2', 'longitudinal-value-1-2', 'longitudinal-bar-1-2'],
            'svg-gate-line-overlap': ['fig-post4-3', 'causal-gate-value-persist_2yr-0',
              'causal-gate-line-any_he_two_year-0'],
            'svg-frame-overlap': ['fig-post4-1', 'selection-value-a-1', 'selection-spine-a-top']
          }[expected.fixture];
          if (mutation?.[0] === figureId) {
            const value = svg.querySelector(`#${mutation[1]}`);
            const ci = svg.querySelector(`#${mutation[2]}`);
            const a = value.getBoundingClientRect(), b = ci.getBoundingClientRect();
            const linePath = /(?:-gate-line-|-spine-)/.test(ci.id)
              ? (ci.matches('path') ? ci : ci.querySelector('path')) : null;
            const midpoint = linePath?.getPointAtLength(linePath.getTotalLength()
              * (expected.fixture === 'svg-frame-overlap' ? 0.64 : 0.5));
            const centre = midpoint ? new DOMPoint(midpoint.x, midpoint.y)
              .matrixTransform(linePath.getScreenCTM()) : null;
            const targetX = expected.fixture === 'svg-own-bar-overlap'
              ? b.left + 4 + a.width / 2 : centre?.x ?? b.left + b.width / 2;
            const targetY = centre?.y ?? b.top + b.height / 2;
            value.style.transform = `translate(${targetX - a.left - a.width / 2}px, ${targetY - a.top - a.height / 2}px)`;
          }
          const box = (node, pad = 0) => {
            const r = node.getBoundingClientRect();
            return { left: r.left - pad, right: r.right + pad, top: r.top - pad,
              bottom: r.bottom + pad, width: r.width, height: r.height };
          };
          const overlap = (a, b) => ({ x: Math.min(a.right, b.right) - Math.max(a.left, b.left),
            y: Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) });
          const labels = contract.textRoles.flatMap((kind) => byKind[kind].map((node) => ({
            id: node.id, text: node.textContent.trim().slice(0, 65), box: box(node) })));
          const scale = renderedWidth / Number(svg.getAttribute('viewBox').split(/\s+/)[2]);
          const marks = contract.markRoles.flatMap((kind) => byKind[kind].map((node) => {
            const path = node.matches('path') ? node : node.querySelector('path');
            let curve = null;
            if ((kind === 'gateLine' || kind === 'spine') && path?.getScreenCTM()) {
              const length = path.getTotalLength();
              const steps = Math.max(2, Math.ceil(length * scale / 2));
              curve = Array.from({ length: steps + 1 }, (_, index) => {
                const point = path.getPointAtLength(length * index / steps);
                const screen = new DOMPoint(point.x, point.y).matrixTransform(path.getScreenCTM());
                return { x: screen.x, y: screen.y };
              });
            }
            return { id: node.id, kind, curve,
              box: box(node, kind === 'ci' ? Math.max(1.5,
                parseFloat(path?.style.strokeWidth || '2') * scale / 2)
                : kind === 'point' ? 1 : 0) };
          }));
          if (marks.some((mark) => (mark.kind === 'gateLine' || mark.kind === 'spine') && !mark.curve))
            return { unmeasured: true, reason: 'line path geometry unavailable', counts, failures: [] };
          const otherText = [...svg.querySelectorAll('text')].filter((node) =>
            !contract.textRoles.some((kind) => byKind[kind].some((group) => group.contains(node)))
              && node.textContent.trim())
            .map((node) => ({ id: node.closest('[id]')?.id || 'text',
              text: node.textContent.trim().slice(0, 65), box: box(node) }));
          const failures = [];
          for (const label of labels) {
            if (label.box.width < 1 || label.box.height < 1) {
              failures.push({ type: 'unrendered-label', label: label.id });
              continue;
            }
            for (const mark of marks) {
              if (mark.curve) {
                const crossing = mark.curve.find((point) => point.x > label.box.left - 1.5
                  && point.x < label.box.right + 1.5 && point.y > label.box.top - 1.5
                  && point.y < label.box.bottom + 1.5);
                if (crossing) failures.push({ type: 'label-mark', label: label.id,
                  mark: mark.id, crossingPx: [round(crossing.x), round(crossing.y)] });
                continue;
              }
              const hit = overlap(label.box, mark.box);
              if (hit.x > 2 && hit.y > 1.5) failures.push({ type: 'label-mark',
                label: label.id, mark: mark.id, overlapPx: [round(hit.x), round(hit.y)] });
            }
            for (const text of [...labels, ...otherText]) {
              if (text.id === label.id) continue;
              const hit = overlap(label.box, text.box);
              if (hit.x > 2 && hit.y > 2) failures.push({ type: 'label-text',
                label: label.id, other: text.id, otherText: text.text,
                overlapPx: [round(hit.x), round(hit.y)] });
            }
          }
          return { unmeasured: false, family: contract.family, counts, renderedWidth: round(renderedWidth),
            failures: failures.slice(0, 30), collisionCount: failures.length };
        } finally { holder.remove(); }
      };
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
          const geometry = /^fig-post4-[123]$/.test(figure.id)
            ? await measureFigureGeometry(xml, renderedWidth, figure.id) : null;
          const labels = [...xml.querySelectorAll('text')].map((text) => {
            const style = text.getAttribute('style') || '';
            const fill = style.match(/(?:^|;)\s*fill:\s*(#[0-9a-f]{6})/i)?.[1];
            const font = Number(style.match(/(?:^|;)\s*font-size:\s*([\d.]+)px/i)?.[1]);
            const fg = parseHex(fill);
            return { text: text.textContent.trim().slice(0, 50),
              ratio: fg ? Math.round(contrast(fg, bg) * 100) / 100 : null,
              renderedPx: font ? Math.round(font * renderedWidth / viewWidth * 100) / 100 : null };
          });
          return { id: figure.id, geometry, unmeasured: labels.length === 0 || labels.some((label) => label.ratio === null
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
        figureSources,
        svgContrast: { count: svgRows.length, unmeasured: svgRows.some((row) => row.unmeasured),
          minimum: Math.min(...svgRows.map((row) => row.minContrast ?? 0)),
          minRenderedTextPx: Math.min(...svgRows.map((row) => row.minRenderedTextPx ?? 0)),
          failures: svgRows.flatMap((row) => row.failures || []).slice(0, 20), figures: svgRows },
        svgLayout,
        svgGeometry: { unmeasured: expected.entryId.startsWith('iv-')
          && svgRows.some((row) => !row.geometry || row.geometry.unmeasured),
        failures: svgRows.flatMap((row) => row.geometry?.failures || []),
        figures: svgRows.filter((row) => row.geometry).map((row) => ({
          id: row.id, ...row.geometry })) } };
    }, { theme, width, fixture, entryId: entry.id });
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
        if (entry.id.startsWith('iv-') || width === 320 || width === 1440) {
          const figuresToCapture = entry.id === 'iv-article'
            ? ['#fig-post4-1'] : entry.id === 'iv-annex'
              ? ['#fig-post4-2', '#fig-post4-3'] : ['.page__content figure.post3-figure'];
          for (const selector of figuresToCapture) {
            const figure = page.locator(selector).first();
            if (await figure.count()) {
              const figurePath = resolve(screenshotDir, `${name}-${selector.startsWith('#')
                ? selector.slice(1) : 'figure'}.png`);
              await figure.screenshot({ path: figurePath, animations: 'disabled' });
              row.screenshots.push(figurePath);
            }
          }
        }
      } catch (error) { row.screenshotError = error.message; }
    }
    row.transientAborts = criticalErrors.filter((error) => {
      if (!error.startsWith('request:') || !error.endsWith(':net::ERR_ABORTED')
        || row.imagesFailed.length || row.figureSourcesFailed.length) return false;
      const url = error.slice('request:'.length, -':net::ERR_ABORTED'.length);
      return /\/assets\/images\/tesis-post[34]\/[a-z0-9-]+\.svg$/.test(url)
        && !row.figureSources.includes(url);
    });
    row.criticalErrors = criticalErrors.filter((error) => !row.transientAborts.includes(error));
    row.failures = evaluate(row);
    return row;
  } finally { await context.close(); }
}

// Scientific-reset SVGs use renderer-owned role IDs. This independent preflight
// also works before the F3 pages exist; it never promotes a draft to PASS.
async function inspectResetSvg(page, markup, renderedWidth, expectedRoles, mutation = null,
  expectedIds = null, expectedRates = null, expectedRows = null, expectedSensitivity = null,
  expectedIvSensitivity = null) {
  await page.setContent(`<main style="margin:0;width:${renderedWidth}px">${markup}</main>`);
  await page.evaluate(() => document.fonts.ready);
  return page.evaluate(({ renderedWidth, expectedRoles, mutation, expectedIds,
    expectedRates, expectedRows, expectedSensitivity, expectedIvSensitivity }) => {
    const svg = document.querySelector('svg');
    if (!svg) return { failures: ['svg-missing'], minTextPx: 0, labels: 0, marks: 0 };
    svg.style.width = `${renderedWidth}px`;
    svg.style.height = 'auto';
    const labels = [...svg.querySelectorAll('text')].filter((node) => node.textContent.trim());
    const markSelector = '[id^="interval-"],[id^="estimate-"],[id^="fill-"],[id^="point-"]'
      + (expectedSensitivity ? ',[id^="bound-"],[id^="lower_pp-"],[id^="upper_pp-"],'
        + '[id^="zero-reference-"]' : expectedIvSensitivity ? ',[id^="zero-"]' : '');
    const marks = [...svg.querySelectorAll(markSelector)];
    if (mutation === 'missing-mark') marks.find((node) => node.id.startsWith('estimate-'))?.remove();
    if (mutation === 'anticipation-missing-mark')
      marks.find((node) => node.id.startsWith('fill-anticipation-'))?.remove();
    if (mutation === 'anticipation-wrong-rate-mark') {
      const fill = svg.querySelector('[id^="fill-anticipation-"] path');
      fill?.setAttribute('d', 'M 60 50 L 90 50');
    }
    if (mutation === 'anticipation-description-leak') {
      const description = svg.querySelector(':scope > desc');
      if (description) description.textContent = description.textContent.replace('suppressed', '77.7%');
    }
    if (mutation === 'anticipation-private-mark') {
      const privateRow = svg.querySelector('[id^="status-"]');
      const match = privateRow?.id.match(/^status-(treated|control)-(\d{4})$/);
      if (match) {
        const namespace = 'http://www.w3.org/2000/svg';
        const group = document.createElementNS(namespace, 'g');
        group.id = `point-anticipation-${match[1]}-${match[2]}`;
        const path = document.createElementNS(namespace, 'path');
        path.setAttribute('d', 'M 70 60 L 74 60');
        path.setAttribute('stroke', '#111111');
        path.setAttribute('stroke-width', '3');
        group.append(path);
        svg.append(group);
      }
    }
    if (mutation === 'sensitivity-wrong-ci-geometry') {
      const path = svg.querySelector('#interval-school-0 path');
      path?.setAttribute('d', 'M 30 142.74 L 60 142.74');
    }
    if (mutation === 'sensitivity-missing-zero-reference')
      svg.querySelector('#zero-reference-0')?.remove();
    if (mutation === 'sensitivity-bounds-false-point') {
      const node = svg.querySelector('#bound-0');
      const point = node?.cloneNode(true);
      if (point) { point.id = 'estimate-0'; node.after(point); }
    }
    if (mutation === 'sensitivity-bounds-wrong-label') {
      const node = [...svg.querySelectorAll('text')].find((text) =>
        /No escolarización real|Actual non-enrollment/.test(text.textContent));
      if (node) node.textContent = 'Sin registro escolar en dos años';
    }
    if (mutation === 'sensitivity-d1-wrong-period') {
      const node = [...svg.querySelectorAll('text')].find((text) => text.textContent.includes('2016–2024'));
      if (node) node.textContent = node.textContent.replace('2016–2024', '2016–2019');
    }
    if (mutation === 'iv-sensitivity-wrong-ci')
      svg.querySelector('[id^="interval-"] path')?.setAttribute('d','M 10 150 L 20 150');
    if (mutation === 'iv-sensitivity-missing-zero')
      svg.querySelector('[id^="zero-"]')?.remove();
    if (mutation === 'iv-sensitivity-private-label') {
      const node = svg.querySelector('text');
      if (node) node.textContent = `${node.textContent} · N=7`;
    }
    if (mutation === 'small-text') labels[0]?.style.setProperty('font-size', '8px', 'important');
    if (mutation === 'low-contrast') labels[0]?.style.setProperty('fill',
      getComputedStyle(svg.querySelector('#patch_1 path,#patch_1 rect')).fill, 'important');
    if (mutation === 'text-overlap' && labels.length > 1) {
      const first = labels[0].getBoundingClientRect();
      const second = labels[1].getBoundingClientRect();
      labels[1].style.transform = `translate(${first.left - second.left}px,${first.top - second.top}px)`;
    }
    if (mutation === 'text-mark' && labels.length && marks.length) {
      const label = labels[0].getBoundingClientRect();
      const mark = marks.find((node) => node.id.startsWith('estimate-')) || marks[0];
      const box = mark.getBoundingClientRect();
      labels[0].style.transform = `translate(${box.left + box.width / 2 - label.left - label.width / 2}px,`
        + `${box.top + box.height / 2 - label.top - label.height / 2}px)`;
    }
    const rect = (node) => node.getBoundingClientRect();
    const overlap = (a, b) => ({ x: Math.min(a.right, b.right) - Math.max(a.left, b.left),
      y: Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) });
    const failures = [];
    const box = rect(svg);
    const viewBox = svg.viewBox.baseVal;
    const scale = box.width / viewBox.width;
    const textRows = labels.map((node) => ({ node, id: node.closest('[id]')?.id || 'text',
      box: rect(node), px: parseFloat(getComputedStyle(node).fontSize) * scale }));
    const rgb = (value) => {
      const hex = value?.match(/^#([0-9a-f]{6})$/i);
      if (hex) return [0, 2, 4].map((index) => parseInt(hex[1].slice(index, index + 2), 16));
      const match = value?.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)/i);
      return match ? [Number(match[1]), Number(match[2]), Number(match[3])] : null;
    };
    const luminance = (color) => color.map((component) => {
      const normalized = component / 255;
      return normalized <= 0.04045 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
    }).reduce((sum, component, index) => sum + component * [0.2126, 0.7152, 0.0722][index], 0);
    const canvas = rgb(getComputedStyle(svg.querySelector('#patch_1 path,#patch_1 rect')).fill);
    const contrastRatios = textRows.map((row) => {
      const ink = rgb(getComputedStyle(row.node).fill);
      if (!ink || !canvas) return null;
      const a = luminance(ink), b = luminance(canvas);
      return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    });
    const minContrast = Math.min(...contrastRatios.filter((ratio) => ratio !== null));
    if (contrastRatios.some((ratio) => ratio === null)) failures.push('svg-contrast-unmeasured');
    else if (minContrast < 4.5) failures.push('svg-text-contrast');
    const minTextPx = Math.min(...textRows.map((row) => row.px));
    if (!Number.isFinite(minTextPx) || minTextPx < 14 - 0.01) failures.push('svg-text-under-14px');
    if (!viewBox.width || !viewBox.height || labels.length === 0) failures.push('svg-unmeasured');
    const actualMarks = [...svg.querySelectorAll(markSelector)];
    const roleCounts = Object.fromEntries(['interval', 'estimate', 'fill', 'point']
      .map((role) => [role, actualMarks.filter((node) => node.id.startsWith(`${role}-`)).length]));
    const trackIds = [...svg.querySelectorAll('[id^="track-anticipation-"]')]
      .map((node) => node.id);
    const present = actualMarks.filter((node) => {
      const path = node.matches('path') ? node : node.querySelector('path');
      const r = rect(node);
      return path && Math.max(r.width, r.height) > 0.5;
    });
    if (!expectedSensitivity && !expectedIvSensitivity && (Object.entries(expectedRoles).some(([role, count]) =>
      present.filter((node) => node.id.startsWith(`${role}-`)).length !== count)
      || present.length !== Object.values(expectedRoles).reduce((sum, count) => sum + count, 0)))
      failures.push('svg-mark-missing');
    if (expectedIds) {
      const actualIds = actualMarks.map((node) => node.id);
      if (actualIds.length !== expectedIds.marks.length
        || expectedIds.marks.some((id) => !actualIds.includes(id))
        || new Set(actualIds).size !== actualIds.length)
        failures.push('svg-mark-identity');
      if (trackIds.length !== expectedIds.tracks.length
        || expectedIds.tracks.some((id) => !trackIds.includes(id))
        || new Set(trackIds).size !== trackIds.length)
        failures.push('svg-track-identity');
      const statusIds = [...svg.querySelectorAll('[id^="status-"]')].map((node) => node.id);
      if (statusIds.length !== expectedIds.statuses.length
        || expectedIds.statuses.some((id) => !statusIds.includes(id)
          || !svg.querySelector(`[id="${id}"]`)?.textContent.trim())
        || new Set(statusIds).size !== statusIds.length)
        failures.push('svg-status-label');
      if (expectedIds.statuses.some((id) => {
        const value = svg.querySelector(`[id="${id}"]`)?.textContent || '';
        return /\d+(?:[.,]\d+)?\s*%|\b(?:n|schools|escuelas)\s*[=:]\s*\d+/i.test(value);
      })) failures.push('svg-status-private-value');
    }
    if (expectedSensitivity) {
      const { kind, rows, axisBound, locale } = expectedSensitivity;
      const plotted = kind === 'd1_d2' ? rows.filter((row) => row.era === 'modern') : rows;
      const roles = kind === 'did'
        ? ['zero-reference','interval-school','estimate-school','interval-two-way','estimate-two-way']
        : kind === 'bounds' ? ['zero-reference','bound','lower_pp','upper_pp']
          : ['zero-reference','interval','estimate'];
      const expected = plotted.flatMap((_, index) => roles.map((role) => `${role}-${index}`));
      const observed = actualMarks.map((node) => node.id);
      if (observed.length !== expected.length || new Set(observed).size !== observed.length
        || expected.some((id) => !observed.includes(id)))
        failures.push('svg-sensitivity-mark-identity');
      const xFor = (value) => viewBox.width * (0.08 + (value + axisBound) / (2 * axisBound) * 0.66);
      const path = (id) => svg.querySelector(`[id="${id}"] path`);
      const start = (id) => path(id)?.getPointAtLength(0);
      const end = (id) => {
        const item = path(id);
        return item?.getPointAtLength(item.getTotalLength());
      };
      const near = (actual, expected) => Number.isFinite(actual)
        && Math.abs(actual - expected) <= 0.75;
      const check = (id, x, label) => {
        if (!near(start(id)?.x, x)) failures.push(`svg-sensitivity-${label}:${id}`);
      };
      const checkInterval = (id, low, high) => {
        if (!near(start(id)?.x, xFor(low)) || !near(end(id)?.x, xFor(high)))
          failures.push(`svg-sensitivity-interval-geometry:${id}`);
      };
      const number = (value) => `${value < 0 ? '−' : '+'}${Math.abs(value).toFixed(1)
        .replace('.', locale === 'es' ? ',' : '.')}`;
      const text = [...svg.querySelectorAll('text')].map((node) => node.textContent.trim());
      for (let index = 0; index < plotted.length; index += 1) {
        const row = plotted[index];
        check(`zero-reference-${index}`, xFor(0), 'zero-reference');
        const zeroPath = path(`zero-reference-${index}`);
        const zeroLow = Math.min(start(`zero-reference-${index}`)?.y ?? NaN,
          end(`zero-reference-${index}`)?.y ?? NaN);
        const zeroHigh = Math.max(start(`zero-reference-${index}`)?.y ?? NaN,
          end(`zero-reference-${index}`)?.y ?? NaN);
        const lineIds = kind === 'did' ? [`interval-school-${index}`,`interval-two-way-${index}`]
          : kind === 'bounds' ? [`bound-${index}`] : [`interval-${index}`];
        if (!zeroPath || lineIds.some((id) => {
          const y = start(id)?.y;
          return !Number.isFinite(y) || y < zeroLow - 1 || y > zeroHigh + 1;
        })) failures.push(`svg-sensitivity-row-zero:${index}`);
        let expectedText;
        if (kind === 'did') {
          checkInterval(`interval-school-${index}`,row.school_ci_low_pp,row.school_ci_high_pp);
          checkInterval(`interval-two-way-${index}`,row.two_way_ci_low_pp,row.two_way_ci_high_pp);
          check(`estimate-school-${index}`,xFor(row.estimate_pp),'estimate-geometry');
          check(`estimate-two-way-${index}`,xFor(row.estimate_pp),'estimate-geometry');
          expectedText = number(row.estimate_pp);
        } else if (kind === 'bounds') {
          checkInterval(`bound-${index}`,row.lower_pp,row.upper_pp);
          check(`lower_pp-${index}`,xFor(row.lower_pp),'bound-endpoint');
          check(`upper_pp-${index}`,xFor(row.upper_pp),'bound-endpoint');
          expectedText = `${number(row.lower_pp)} ${locale === 'es' ? 'a' : 'to'} ${number(row.upper_pp)}`;
        } else {
          checkInterval(`interval-${index}`,row.ci_low_pp,row.ci_high_pp);
          check(`estimate-${index}`,xFor(row.estimate_pp),'estimate-geometry');
          expectedText = number(row.estimate_pp);
        }
        const valueNode = svg.querySelector(`[id="value-${index}"]`);
        const renderedValues = [...(valueNode?.querySelectorAll('text') || [])]
          .map((node) => node.textContent.trim());
        const expectedValues = kind === 'bounds' && renderedValues.length === 2
          ? [number(row.lower_pp), number(row.upper_pp)] : [expectedText];
        if (renderedValues.length !== expectedValues.length
          || expectedValues.some((value, position) => renderedValues[position] !== value))
          failures.push(`svg-sensitivity-value-label:${index}`);
        const period = `${row.cohort_start}–${row.cohort_end}`;
        const era = locale === 'es' ? row.era === 'historical' ? 'histórica' : 'moderna' : row.era;
        const rowLabels = [...svg.querySelectorAll('text')]
          .filter((node) => Boolean(valueNode && (node.compareDocumentPosition(valueNode) & Node.DOCUMENT_POSITION_FOLLOWING)))
          .slice(-2).map((node) => node.textContent.trim()).join(' ').toLowerCase();
        const contrast = kind === 'd1_d2' ? (row.contrast?.startsWith('main') ? 'D2' : 'D1')
          + (row.contrast?.endsWith('common') ? locale === 'es' ? ' común' : ' common'
            : locale === 'es' ? ' completa' : ' full') : null;
        if (!rowLabels.includes(period) || !(kind === 'd1_d2'
          ? rowLabels.includes(contrast.toLowerCase()) : rowLabels.includes(era)))
          failures.push(`svg-sensitivity-period-label:${index}`);
      }
      if (kind === 'bounds') {
        const label = locale === 'es' ? 'No escolarización real' : 'Actual non-enrollment';
        if (text.filter((value) => value.includes(label)).length !== 2)
          failures.push('svg-sensitivity-true-schooling-label');
      }
      if (kind === 'd1_d2' && !text.some((value) =>
        value.includes('2005–2015') && value.includes('D1 = D2')))
        failures.push('svg-sensitivity-historical-status');
    }
    if (expectedIvSensitivity) {
      const { rows, axisBound, locale } = expectedIvSensitivity;
      const roleIds = rows.flatMap((row) => [`zero-${row.variant}`,
        `interval-${row.variant}`,`estimate-${row.variant}`]);
      const observed = actualMarks.map((node) => node.id);
      if (observed.length !== roleIds.length || new Set(observed).size !== observed.length
        || roleIds.some((id) => !observed.includes(id)))
        failures.push('svg-iv-sensitivity-mark-identity');
      const xFor = (value) => viewBox.width * (0.08 + (value + axisBound)/(2*axisBound)*0.64);
      const at = (id) => svg.querySelector(`[id="${id}"] path`);
      const pt = (path, final = false) => path?.getPointAtLength(final ? path.getTotalLength() : 0);
      const near = (a,b) => Number.isFinite(a) && Math.abs(a-b) <= 0.75;
      for (const row of rows) {
        const zero = at(`zero-${row.variant}`), interval = at(`interval-${row.variant}`);
        const estimateGroup = svg.querySelector(`[id="estimate-${row.variant}"]`);
        const estimateUse = estimateGroup?.querySelector('use');
        const estimatePath = estimateGroup?.querySelector('path');
        const estimateX = estimateUse ? Number(estimateUse.getAttribute('x'))
          : pt(estimatePath)?.x;
        if (!near(pt(zero)?.x,xFor(0)) || !near(pt(zero,true)?.x,xFor(0)))
          failures.push(`svg-iv-sensitivity-zero:${row.variant}`);
        if (!near(pt(interval)?.x,xFor(row.ci_low_pp))
          || !near(pt(interval,true)?.x,xFor(row.ci_high_pp)))
          failures.push(`svg-iv-sensitivity-ci:${row.variant}`);
        if (!near(estimateX,xFor(row.estimate_pp)))
          failures.push(`svg-iv-sensitivity-point:${row.variant}`);
        if (!Number.isFinite(pt(zero)?.y) || !Number.isFinite(pt(interval)?.y)
          || pt(interval)?.y < Math.min(pt(zero)?.y,pt(zero,true)?.y)-1
          || pt(interval)?.y > Math.max(pt(zero)?.y,pt(zero,true)?.y)+1)
          failures.push(`svg-iv-sensitivity-row-zero:${row.variant}`);
        const value = `${row.estimate_pp < 0 ? '−' : '+'}${Math.abs(row.estimate_pp)
          .toFixed(1).replace('.',locale === 'es' ? ',' : '.')}`;
        if (svg.querySelector(`[id="value-${row.variant}"]`)?.textContent.trim() !== value)
          failures.push(`svg-iv-sensitivity-value:${row.variant}`);
      }
      if (svg.querySelector('#axis-guide') == null)
        failures.push('svg-iv-sensitivity-axis-guide');
      const visible = [...svg.querySelectorAll('text,title,desc')]
        .map((node) => node.textContent).join(' ');
      if (/\b(?:n_treated|n_control|treated_post|control_post|treated_pre|control_pre)\b|\bN\s*[=:]\s*\d/i.test(visible))
        failures.push('svg-iv-sensitivity-private-value');
    }
    if (expectedRates) for (const row of expectedRates) {
      const id = `anticipation-${row.arm}-${row.year}`;
      const track = svg.querySelector(`[id="track-${id}"] path`);
      const fill = svg.querySelector(`[id="fill-${id}"] path`);
      const point = svg.querySelector(`[id="point-${id}"] use`);
      if (!track || !fill || !point) {
        failures.push(`svg-rate-unmeasured:${id}`); continue;
      }
      const trackLength = track.getTotalLength();
      const fillLength = fill.getTotalLength();
      const observedRate = trackLength > 0 ? 100 * fillLength / trackLength : NaN;
      if (!Number.isFinite(observedRate) || Math.abs(observedRate - row.rate) > 0.15)
        failures.push(`svg-rate-mismatch:${id}`);
      const end = fill.getPointAtLength(fillLength);
      const pointX = Number(point.getAttribute('x'));
      const pointY = Number(point.getAttribute('y'));
      if (!Number.isFinite(pointX) || !Number.isFinite(pointY)
        || Math.hypot(end.x - pointX, end.y - pointY) * scale > 1.5)
        failures.push(`svg-rate-point:${id}`);
    }
    if (expectedRows) {
      const description = svg.querySelector(':scope > desc')?.textContent || '';
      const described = [...description.matchAll(/\b(\d{4})\s+([^:;]+):\s*([^;]+)/g)];
      if (described.length !== expectedRows.length) failures.push('svg-description-row-count');
      for (let index = 0; index < Math.min(described.length, expectedRows.length); index += 1) {
        const row = expectedRows[index];
        const phrase = described[index][3].split(/\. (?=[A-ZÁÉÍÓÚ])/)[0];
        const percent = phrase.match(/(\d{1,3}(?:[.,]\d+)?)\s*%/);
        if (Number(described[index][1]) !== Number(row.cohort_year))
          failures.push(`svg-description-cohort:${index}`);
        if (row.display_status === 'OBSERVED') {
          if (!percent || Math.abs(Number(percent[1].replace(',', '.')) - row.rate_pp) > 0.01)
            failures.push(`svg-description-rate:${index}`);
        } else if (percent || /\b(?:n|schools|escuelas)\s*[=:]\s*\d+/i.test(phrase))
          failures.push(`svg-description-private-rate:${index}`);
      }
    }
    for (const row of textRows) {
      if (row.box.width < 1 || row.box.height < 1 || row.box.left < box.left - 1
        || row.box.right > box.right + 1 || row.box.top < box.top - 1
        || row.box.bottom > box.bottom + 1) failures.push(`svg-text-clipped:${row.id}`);
    }
    for (let i = 0; i < textRows.length; i += 1) for (let j = i + 1; j < textRows.length; j += 1) {
      const hit = overlap(textRows[i].box, textRows[j].box);
      if (hit.x > 2 && hit.y > 2) failures.push(`svg-text-overlap:${textRows[i].id}:${textRows[j].id}`);
    }
    for (const row of textRows) for (const mark of present) {
      const path = mark.matches('path') ? mark : mark.querySelector('path');
      if (!path) continue;
      if (mark.id.startsWith('fill-')) {
        const hit = overlap(row.box, rect(mark));
        if (hit.x > 2 && hit.y > 1.5) failures.push(`svg-text-mark:${row.id}:${mark.id}`);
      } else if (typeof path.getTotalLength === 'function' && path.getScreenCTM()) {
        const length = path.getTotalLength();
        const steps = Math.max(2, Math.ceil(length * scale / 2));
        for (let i = 0; i <= steps; i += 1) {
          const point = path.getPointAtLength(length * i / steps);
          const screen = new DOMPoint(point.x, point.y).matrixTransform(path.getScreenCTM());
          if (screen.x > row.box.left - 1.5 && screen.x < row.box.right + 1.5
            && screen.y > row.box.top - 1.5 && screen.y < row.box.bottom + 1.5) {
            failures.push(`svg-text-mark:${row.id}:${mark.id}`);
            break;
          }
        }
      }
    }
    return { failures: [...new Set(failures)].slice(0, 50), minTextPx: Math.round(minTextPx * 100) / 100,
      minContrast: Math.round(minContrast * 100) / 100,
      labels: labels.length, marks: present.length, roleCounts,
      trackCount: trackIds.length, renderedWidth };
  }, { renderedWidth, expectedRoles, mutation, expectedIds, expectedRates, expectedRows,
    expectedSensitivity, expectedIvSensitivity });
}

function sensitivitySvgFixture(fixture) {
  const kind = fixture.includes('bounds') ? 'bounds' : fixture.includes('d1-') ? 'd1_d2' : 'did';
  const axisBound = 10;
  const x = (value) => 400 * (0.08 + (value + axisBound) / (2 * axisBound) * 0.66);
  const line = (id, x0, y0, x1, y1) => `<g id="${id}"><path d="M ${x0} ${y0} L ${x1} ${y1}" stroke="#111111" stroke-width="2"/></g>`;
  const text = (value, y, id = '') => `${id ? `<g id="${id}">` : ''}<text x="20" y="${y}" style="font-size:16px;fill:#111111">${value}</text>${id ? '</g>' : ''}`;
  let rows;
  let height;
  let content = '';
  if (kind === 'did') {
    rows = [{ era: 'historical', cohort_start: 2008, cohort_end: 2015,
      estimate_pp: 2, school_ci_low_pp: 1, school_ci_high_pp: 3,
      two_way_ci_low_pp: 0, two_way_ci_high_pp: 4 }];
    height = 250;
    content += text('Historical · 2008–2015', 75) + text('+2.0', 105, 'value-0');
    content += line('zero-reference-0',x(0),140,x(0),170);
    content += line('interval-school-0',x(1),150,x(3),150);
    content += line('estimate-school-0',x(2),150,x(2)+2,150);
    content += line('interval-two-way-0',x(0),160,x(4),160);
    content += line('estimate-two-way-0',x(2),160,x(2)+2,160);
  } else if (kind === 'bounds') {
    rows = Array.from({ length: 4 }, (_, index) => ({
      era: index % 2 ? 'modern' : 'historical',
      cohort_start: index % 2 ? 2016 : 2005,
      cohort_end: index === 3 ? 2023 : index === 1 ? 2024 : 2015,
      lower_pp: index - 2, upper_pp: index + 2
    }));
    height = 680;
    for (let index = 0; index < rows.length; index += 1) {
      const row = rows[index];
      const y = 135 + 130 * index;
      const label = index < 2 ? 'Progression' : 'No escolarización real';
      const era = row.era === 'modern' ? 'moderna' : 'histórica';
      const sign = (value) => `${value < 0 ? '−' : '+'}${Math.abs(value).toFixed(1).replace('.',',')}`;
      content += text(`${label} · ${era} · ${row.cohort_start}–${row.cohort_end}`, y - 55);
      content += text(`${sign(row.lower_pp)} a ${sign(row.upper_pp)}`, y - 30, `value-${index}`);
      content += line(`zero-reference-${index}`,x(0),y-10,x(0),y+10);
      content += line(`bound-${index}`,x(row.lower_pp),y,x(row.upper_pp),y);
      content += line(`lower_pp-${index}`,x(row.lower_pp),y,x(row.lower_pp)+2,y);
      content += line(`upper_pp-${index}`,x(row.upper_pp),y,x(row.upper_pp)+2,y);
    }
  } else {
    rows = [{ era: 'historical', cohort_start: 2005, cohort_end: 2015,
      status: 'NON_DISCRIMINATING_IDENTICAL_EXPOSURE_FLAGS' },
    { era: 'modern', contrast: 'main_full', cohort_start: 2016, cohort_end: 2024,
      estimate_pp: 2, ci_low_pp: 1, ci_high_pp: 3 }];
    height = 300;
    content += text('D2 full · 2016–2024', 75) + text('+2.0', 105, 'value-0');
    content += line('zero-reference-0',x(0),140,x(0),160);
    content += line('interval-0',x(1),150,x(3),150);
    content += line('estimate-0',x(2),150,x(2)+2,150);
    content += text('Historical 2005–2015: D1 = D2', 235);
  }
  const markup = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 ${height}">`
    + `<g id="patch_1"><rect width="400" height="${height}" fill="#ffffff"/></g>`
    + text('Sensitivity fixture',30) + content + '</svg>';
  return { markup, expected: { kind, rows, axisBound, locale: kind === 'bounds' ? 'es' : 'en' } };
}

function ivSensitivitySvgFixture() {
  const axisBound = 10;
  const x = (value) => 400 * (0.08 + (value + axisBound)/(2*axisBound)*0.64);
  const row = { variant: 'primary', estimate_pp: 2, ci_low_pp: 1, ci_high_pp: 3 };
  const line = (id,x0,y0,x1,y1) => `<g id="${id}"><path d="M ${x0} ${y0} L ${x1} ${y1}" stroke="#111111" stroke-width="2"/></g>`;
  const markup = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260">'
    + '<g id="patch_1"><rect width="400" height="260" fill="#ffffff"/></g>'
    + '<text x="20" y="30" style="font-size:16px;fill:#111111">IV sensitivity</text>'
    + '<text x="20" y="75" style="font-size:16px;fill:#111111">Primary reference</text>'
    + '<g id="value-primary"><text x="20" y="105" style="font-size:16px;fill:#111111">+2.0</text></g>'
    + line('zero-primary',x(0),140,x(0),160)
    + line('interval-primary',x(1),150,x(3),150)
    + line('estimate-primary',x(2),150,x(2)+2,150)
    + line('axis-guide',x(-10),220,x(10),220) + '</svg>';
  return { markup, expected: { kind: 'comparison', rows: [row], axisBound, locale: 'en' } };
}

async function runScientificReset(args) {
  const fixture = readOption(args, '--reset-fixture');
  const manifestPaths = readOptions(args, '--reset-manifest');
  const reportPath = readOption(args, '--report');
  const playwright = createRequire(import.meta.url)(playwrightPath);
  const executable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
    || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);
  const browser = await playwright.chromium.launch({ headless: true,
    ...(executable ? { executablePath: executable } : {}), args: ['--no-sandbox'] });
  let report;
  try {
    const page = await browser.newPage();
    if (fixture) {
      const anticipationFixture = fixture.startsWith('anticipation-');
      const ivSensitivityFixture = fixture.startsWith('iv-sensitivity-')
        ? ivSensitivitySvgFixture() : null;
      const sensitivityFixture = fixture.startsWith('sensitivity-')
        ? sensitivitySvgFixture(fixture) : null;
      const synthetic = ivSensitivityFixture ? ivSensitivityFixture.markup
        : sensitivityFixture ? sensitivityFixture.markup : anticipationFixture
        ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 100">'
          + '<desc>Prior enrollment; 2006 treated: 50.0%; 2005 treated: suppressed.</desc>'
          + '<g id="patch_1"><rect width="140" height="100" fill="#ffffff"/></g>'
          + '<text id="title" x="5" y="18" style="font-size:16px">Prior enrollment</text>'
          + '<g id="track-anticipation-treated-2006"><path d="M 60 50 L 100 50" stroke="#cccccc"/></g>'
          + '<g id="fill-anticipation-treated-2006"><path d="M 60 50 L 80 50" stroke="#224466" stroke-width="3"/></g>'
          + '<g id="point-anticipation-treated-2006"><defs><path id="dot" d="M -2 0 L 2 0" stroke="#224466" stroke-width="3"/></defs><use href="#dot" x="80" y="50"/></g>'
          + '<text id="status-treated-2005" x="5" y="78" style="font-size:16px">Suppressed</text>'
          + '</svg>'
        : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80">'
        + '<g id="patch_1"><rect width="100" height="80" fill="#ffffff"/></g>'
        + '<text id="title" x="5" y="18" style="font-size:16px">Title</text>'
        + '<text id="value-0" x="5" y="42" style="font-size:16px">Value</text>'
        + '<g id="estimate-0"><path d="M 60 60 L 64 60" stroke="black" stroke-width="3"/></g>'
        + '</svg>';
      const expectedIds = anticipationFixture ? {
        marks: ['fill-anticipation-treated-2006', 'point-anticipation-treated-2006'],
        tracks: ['track-anticipation-treated-2006'], statuses: ['status-treated-2005']
      } : null;
      const expectedRates = anticipationFixture ? [{ arm: 'treated', year: 2006, rate: 50 }] : null;
      const expectedRows = anticipationFixture ? [
        { cohort_year: 2006, display_status: 'OBSERVED', rate_pp: 50 },
        { cohort_year: 2005, display_status: 'NOT_ESTIMABLE_PANEL_BOUNDARY', rate_pp: null }
      ] : null;
      const size = sensitivityFixture || ivSensitivityFixture ? 400 : anticipationFixture ? 140 : 100;
      const roles = sensitivityFixture || ivSensitivityFixture
        ? {} : anticipationFixture ? { fill: 1, point: 1 } : { estimate: 1 };
      const baseline = await inspectResetSvg(page, synthetic, size, roles, null,
        expectedIds, expectedRates, expectedRows, sensitivityFixture?.expected,
        ivSensitivityFixture?.expected);
      const mutated = await inspectResetSvg(page, synthetic, size, roles, fixture,
        expectedIds, expectedRates, expectedRows, sensitivityFixture?.expected,
        ivSensitivityFixture?.expected);
      const expected = { 'missing-mark': 'svg-mark-missing', 'small-text': 'svg-text-under-14px',
        'low-contrast': 'svg-text-contrast',
        'text-overlap': 'svg-text-overlap', 'text-mark': 'svg-text-mark',
        'anticipation-missing-mark': 'svg-mark-missing',
        'anticipation-private-mark': 'svg-mark-identity',
        'anticipation-wrong-rate-mark': 'svg-rate-mismatch',
        'anticipation-description-leak': 'svg-description-private-rate',
        'sensitivity-wrong-ci-geometry': 'svg-sensitivity-interval-geometry',
        'sensitivity-missing-zero-reference': 'svg-sensitivity-mark-identity',
        'sensitivity-bounds-false-point': 'svg-sensitivity-mark-identity',
        'sensitivity-bounds-wrong-label': 'svg-sensitivity-true-schooling-label',
        'sensitivity-d1-wrong-period': 'svg-sensitivity-period-label',
        'iv-sensitivity-wrong-ci': 'svg-iv-sensitivity-ci',
        'iv-sensitivity-missing-zero': 'svg-iv-sensitivity-mark-identity',
        'iv-sensitivity-private-label': 'svg-iv-sensitivity-private-value'
      }[fixture];
      const discriminates = Boolean(expected) && baseline.failures.length === 0
        && mutated.failures.some((failure) => failure.startsWith(expected));
      report = { status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture,
        baseline, mutated, expected };
      process.exitCode = discriminates ? 1 : 2;
    } else {
      if (!manifestPaths.length || manifestPaths.some((path) => !existsSync(path)))
        throw new Error('--reset-manifest missing for one or more families');
      const manifests = manifestPaths.map((path) => ({ path,
        manifest: JSON.parse(readFileSync(path, 'utf8')) }));
      if (manifests.some(({ manifest }) => !Array.isArray(manifest.figures)
        || !manifest.figures.length || !Array.isArray(manifest.files)))
        throw new Error('reset manifest lacks figures/files');
      const rows = [];
      const familyCounts = Object.fromEntries(['primary', 'anticipation', 'sensitivity'].map((family) =>
        [family, manifests.filter(({ manifest }) =>
          (manifest.family === 'post4_primary_projected' ? 'primary'
            : manifest.family || 'primary') === family).length]));
      const isIII = manifests.some(({ manifest }) => manifest.family === 'anticipation'
        || (manifest.family === 'sensitivity' && manifest.series !== 'IV')
        || manifest.series === 'III'
        || manifest.figures.some((figure) => !figure.kind && Boolean(figure.outcome)));
      const inventoryFailures = [];
      if (familyCounts.primary !== 1 || (isIII && (familyCounts.anticipation !== 1
        || familyCounts.sensitivity !== 1))
        || (!isIII && (familyCounts.anticipation !== 0 || familyCounts.sensitivity !== 1)))
        inventoryFailures.push('manifest-family-inventory');
      for (const { path: manifestPath, manifest } of manifests) {
        const family = manifest.family || 'primary';
        const folder = dirname(resolve(manifestPath));
        for (const figure of manifest.figures) {
          const ivSensitivity = family === 'sensitivity' && manifest.series === 'IV';
          const stem = ivSensitivity ? `post4-sensitivity-${figure.kind}-${figure.era}`
            : family === 'sensitivity' ? figure.stem : family === 'anticipation'
            ? `post3-anticipation-${figure.outcome}-${figure.era}`
            : figure.kind ? `post4-${figure.kind}-${figure.era}`
              : `post3-${figure.outcome}-${figure.era}`;
          const observed = family === 'anticipation' ? figure.source_rows.filter((row) =>
            row.display_status === 'OBSERVED') : [];
          const suppressed = family === 'anticipation' ? figure.source_rows.filter((row) =>
            row.display_status !== 'OBSERVED') : [];
          const expectedRoles = family === 'sensitivity'
            ? {} : family === 'anticipation'
            ? { fill: observed.length, point: observed.length }
            : figure.kind === 'access' ? { fill: 4, point: 4 }
              : { interval: figure.source_rows.length, estimate: figure.source_rows.length };
          const expectedIds = family === 'anticipation' ? {
            marks: observed.flatMap((row) => ['fill', 'point'].map((role) =>
              `${role}-anticipation-${row.arm}-${row.cohort_year}`)),
            tracks: observed.map((row) => `track-anticipation-${row.arm}-${row.cohort_year}`),
            statuses: suppressed.map((row) => `status-${row.arm}-${row.cohort_year}`)
          } : null;
          const expectedRates = family === 'anticipation' ? observed.map((row) => ({
            arm: row.arm, year: row.cohort_year, rate: row.rate_pp })) : null;
          const expectedRows = family === 'anticipation' ? figure.source_rows : null;
          const expectedSensitivity = family === 'sensitivity' && !ivSensitivity ? {
            kind: figure.kind, rows: figure.source_rows, axisBound: figure.axis_bound_pp
          } : null;
          const expectedIvSensitivity = ivSensitivity ? {
            kind: figure.kind, rows: figure.source_rows, axisBound: figure.axis_bound_pp
          } : null;
        for (const locale of locales) for (const theme of ['light', 'dark'])
          for (const width of widths) {
            const layout = width < 768 ? 'mobile' : 'desktop';
            const name = `${stem}-${locale}-${theme}-${layout}.svg`;
            const item = manifest.files.find((entry) => entry.name === name);
            if (!item || !existsSync(resolve(folder, name))) {
              rows.push({ name, width, failures: ['svg-file-missing'] });
              continue;
            }
            const bytes = readFileSync(resolve(folder, name));
            if (sha256(bytes) !== item.sha256) {
              rows.push({ name, width, failures: ['svg-source-hash'] });
              continue;
            }
            const renderedWidth = width < 768 ? (width === 320 ? 294 : 358) : 672;
            const measured = await inspectResetSvg(page, bytes.toString('utf8'),
              renderedWidth, expectedRoles, null, expectedIds, expectedRates, expectedRows,
              expectedSensitivity ? { ...expectedSensitivity, locale } : null,
              expectedIvSensitivity ? { ...expectedIvSensitivity, locale } : null);
            rows.push({ family, name, width, ...measured });
          }
        }
      }
      const readiness = manifests.every(({ manifest }) => manifest.f2_complete === true
        && manifest.publication_authorized === true);
      const geometryPass = rows.every((row) => row.failures.length === 0)
        && inventoryFailures.length === 0;
      report = { status: geometryPass ? 'PREFLIGHT_ONLY' : 'FAIL', geometryPass,
        manifest: manifestPaths.map((path) => resolve(path)),
        familyCounts, inventoryFailures, scientificReady: readiness, draft: !readiness,
        rows: rows.length, failedRows: rows.filter((row) => row.failures.length),
        minTextPx: Math.min(...rows.map((row) => row.minTextPx ?? 0)),
        minContrast: Math.min(...rows.map((row) => row.minContrast ?? 0)) };
      process.exitCode = 1;
    }
  } finally { await browser.close(); }
  if (reportPath) { mkdirSync(dirname(resolve(reportPath)), { recursive: true });
    writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`); }
  console.log(JSON.stringify(report));
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--reset-manifest') || args.includes('--reset-fixture')) {
    await runScientificReset(args);
    return;
  }
  const baseUrl = (readOption(args, '--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
  const reportPath = readOption(args, '--report');
  const screenshotDir = readOption(args, '--screenshot-dir');
  const fixture = readOption(args, '--fixture');
  if (!fixture) {
    console.error(JSON.stringify({ status: 'ERROR', error:
      '--reset-manifest is required; legacy III/IV geometry IDs and 9 px threshold are obsolete' }));
    process.exitCode = 2;
    return;
  }
  const ivFigureOnly = args.includes('--iv-figure-only');
  const ivOnly = args.includes('--iv-only');
  if (!/^https?:\/\//.test(baseUrl) || !existsSync(playwrightPath)
    || (fixture && !['low-contrast', 'broken-active-svg', 'svg-value-overlap',
      'svg-longitudinal-overlap', 'svg-causal-overlap', 'svg-own-bar-overlap',
      'svg-gate-line-overlap', 'svg-frame-overlap'].includes(fixture))) {
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
      const geometryFixture = fixture?.startsWith('svg-') && fixture !== 'broken-active-svg';
      const entry = geometryFixture ? (['svg-value-overlap', 'svg-frame-overlap'].includes(fixture)
        ? routes[2] : routes[3]) : routes[0];
      const baseline = await inspect(browser, baseUrl, entry, 'es', 'light', 390, null);
      const mutant = await inspect(browser, baseUrl, entry, 'es', 'light', 390, null, fixture);
      const expectedCollision = {
        'svg-value-overlap': ['selection-value-a-1', 'selection-ci-a-1'],
        'svg-longitudinal-overlap': ['longitudinal-value-0-1', 'longitudinal-bar-1-1'],
        'svg-causal-overlap': ['causal-paes-value-1-1', 'causal-paes-bar-0-1'],
        'svg-own-bar-overlap': ['longitudinal-value-1-2', 'longitudinal-bar-1-2'],
        'svg-gate-line-overlap': ['causal-gate-value-persist_2yr-0',
          'causal-gate-line-any_he_two_year-0'],
        'svg-frame-overlap': ['selection-value-a-1', 'selection-spine-a-top']
      }[fixture];
      const targetMarkHits = geometryFixture ? mutant.svgGeometry.failures.filter((failure) =>
        failure.type === 'label-mark' && failure.label === expectedCollision[0]) : [];
      const isolatedCollision = geometryFixture && ['svg-own-bar-overlap', 'svg-frame-overlap'].includes(fixture)
        ? mutant.svgGeometry.failures.length === 1 && targetMarkHits.length === 1
          && targetMarkHits[0].mark === expectedCollision[1]
          && mutant.failures.length === 1 && mutant.failures[0] === 'svg-label-geometry'
        : null;
      const discriminates = baseline.failures.length === 0 && (fixture === 'low-contrast'
        ? mutant.failures.includes('text-contrast')
          && mutant.textContrast.failures.some((failure) => failure.ratio === 1)
        : geometryFixture
          ? mutant.failures.includes('svg-label-geometry')
            && targetMarkHits.some((failure) => failure.mark === expectedCollision[1])
            && (isolatedCollision === null || isolatedCollision)
          : mutant.failures.includes('image-or-variant')
            && mutant.imagesFailed.some((image) => image.src.includes('cohort-series-infographic-es-light-mobile.svg'))
            && mutant.criticalErrors.some((error) => error.includes('cohort-series-infographic-es-light-mobile.svg')));
      report = { status: discriminates ? 'EXPECTED_FAIL' : 'WRONG_FAILURE', fixture,
        ...(isolatedCollision !== null ? { isolatedCollision,
          wouldPassWithoutTargetMark: isolatedCollision } : {}),
        baseline: { failures: baseline.failures, minimum: baseline.textContrast.minimum,
          sampled: baseline.textContrast.count,
          contrastFailures: baseline.textContrast.failures.slice(0, 5),
          imagesFailed: baseline.imagesFailed, figureSourcesFailed: baseline.figureSourcesFailed,
          svgGeometry: baseline.svgGeometry },
        mutant: { failures: mutant.failures, minimum: mutant.textContrast.minimum,
          samples: mutant.textContrast.failures.slice(0, 3), imagesFailed: mutant.imagesFailed,
          criticalErrors: mutant.criticalErrors, transientAborts: mutant.transientAborts,
          svgGeometry: mutant.svgGeometry } };
      process.exitCode = discriminates ? 1 : 2;
    } else {
      const rows = [];
      for (const entry of (ivFigureOnly ? [routes[2]] : ivOnly ? routes.slice(2) : routes))
        for (const locale of locales)
        for (const theme of themes)
        for (const width of widths) rows.push(await inspect(browser, baseUrl, entry, locale, theme,
          width, screenshotDir));
      report = { status: rows.every((row) => row.failures.length === 0) ? 'PASS' : 'FAIL',
        testedAt: new Date().toISOString(), baseUrl,
        matrix: `${ivFigureOnly ? '2' : ivOnly ? '4' : '8'} routes x 2 themes x 4 widths`,
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
        svgLayout: row.svgLayout, svgGeometry: row.svgGeometry,
        criticalErrors: row.criticalErrors.slice(0, 2) })) }
    : report));
}

main().catch((error) => {
  console.error(JSON.stringify({ status: 'ERROR', error: error.stack || error.message }));
  process.exitCode = 2;
});
