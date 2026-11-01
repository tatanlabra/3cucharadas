#!/usr/bin/env node
// Mide la caja de cada <a href> de las láminas de un carrusel ya cortadas por
// render-linkedin-carousel.sh (slide-NN.html) e imprime un JSON para anotar el PDF.
// El PDF del carrusel se arma con capturas PNG, así que los enlaces del HTML se pierden
// si nadie los vuelve a poner como anotaciones /Link (carousel_pdf_links.py).
// Uso: carousel-link-rects.mjs DIR_LAMINAS [ANCHO_PX] [ALTO_PX]
import { createRequire } from 'node:module';
import { existsSync, readdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const [dir, width = '1080', height = '1350'] = process.argv.slice(2);
if (!dir) {
  console.error('Uso: carousel-link-rects.mjs DIR_LAMINAS [ANCHO_PX] [ALTO_PX]');
  process.exit(2);
}
const scriptDir = dirname(fileURLToPath(import.meta.url));
const playwrightPath = process.env.PLAYWRIGHT_MODULE_PATH
  || resolve(scriptDir, '../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright');
if (!existsSync(playwrightPath)) {
  console.error(`Playwright no está en ${playwrightPath}`);
  process.exit(2);
}
const { chromium } = createRequire(import.meta.url)(playwrightPath);
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  || ['/usr/bin/chromium', '/usr/bin/brave', '/usr/bin/google-chrome-stable'].find(existsSync);

const files = readdirSync(dir).filter((name) => /^slide-\d+\.html$/.test(name)).sort();
const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
const out = [];
try {
  const page = await browser.newPage({ viewport: { width: Number(width), height: Number(height) } });
  for (const [index, name] of files.entries()) {
    await page.goto(pathToFileURL(resolve(dir, name)).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map((anchor) => {
      const box = anchor.getBoundingClientRect();
      return { href: anchor.href, x: box.x, y: box.y, w: box.width, h: box.height };
    }));
    for (const link of links) out.push({ page: index, ...link });
  }
} finally {
  await browser.close();
}
process.stdout.write(`${JSON.stringify(out)}\n`);
