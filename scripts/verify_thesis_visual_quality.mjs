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

async function main() {
  const args = process.argv.slice(2);
  const baseUrl = (readOption(args, '--base-url') || 'http://127.0.0.1:4004').replace(/\/$/, '');
  const reportPath = readOption(args, '--report');
  const screenshotDir = readOption(args, '--screenshot-dir');
  const fixture = readOption(args, '--fixture');
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
