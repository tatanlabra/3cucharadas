import { createRequire } from 'node:module';
import { waitForImageCompleteNoJs } from '/home/ende/Descargas/programaciones/activos/3cucharadas/scripts/verify_thesis_series_browser.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/node_modules/playwright');
const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/brave', args: ['--no-sandbox'] });
const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
const page = await context.newPage();
const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="40"><rect width="100" height="40"/></svg>';
await page.route('**/*', async (route) => {
  const path = new URL(route.request().url()).pathname;
  if (path === '/') return route.fulfill({ contentType: 'text/html', body: '<img id="slow" loading="lazy" src="/slow.svg"><img id="never" loading="lazy" src="/never.svg">' });
  if (path === '/slow.svg') {
    await new Promise((done) => setTimeout(done, 800));
    return route.fulfill({ contentType: 'image/svg+xml', body: svg });
  }
  if (path === '/never.svg') {
    await new Promise((done) => setTimeout(done, 2000));
    return route.fulfill({ contentType: 'image/svg+xml', body: svg });
  }
  return route.abort();
});
await page.goto('https://fixture.test/', { waitUntil: 'domcontentloaded', timeout: 5000 });
const slow = page.locator('#slow');
const never = page.locator('#never');
await slow.scrollIntoViewIfNeeded();
await never.scrollIntoViewIfNeeded();
await slow.evaluate((image) => { image.loading = 'eager'; });
await never.evaluate((image) => { image.loading = 'eager'; });
const slowInitial = await slow.evaluate((image) => image.complete);
const neverInitial = await never.evaluate((image) => image.complete);
const slowStarted = Date.now();
const slowReady = await waitForImageCompleteNoJs(slow, 3000);
const slowElapsedMs = Date.now() - slowStarted;
const neverStarted = Date.now();
const neverReadyWithin350Ms = await waitForImageCompleteNoJs(never, 350);
const neverElapsedMs = Date.now() - neverStarted;
const slowNaturalWidth = await slow.evaluate((image) => image.naturalWidth);
const result = { status: !slowInitial && !neverInitial && slowReady && slowNaturalWidth === 100
  && !neverReadyWithin350Ms && slowElapsedMs >= 500 && neverElapsedMs >= 300 ? 'PASS' : 'FAIL',
  javascriptEnabled: false, slowInitial, neverInitial, slowReady, slowNaturalWidth,
  slowElapsedMs, neverReadyWithin350Ms, neverElapsedMs };
console.log(JSON.stringify(result));
await context.close();
await browser.close();
if (result.status !== 'PASS') process.exitCode = 1;
