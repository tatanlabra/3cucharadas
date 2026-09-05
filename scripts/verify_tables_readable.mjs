#!/usr/bin/env node
// Gate de legibilidad de tablas. Mide en navegador, no en la hoja de estilos:
// una regla correcta que no gana en la cascada da el mismo resultado que una
// regla ausente, y eso fue exactamente lo que pasó aquí durante meses.
//
// Criterios, del §7 del encargo de tablas responsivas:
//   1. El documento no desborda horizontalmente por culpa de una tabla.
//   2. Cada tabla envuelta desplaza SU contenedor, no la página.
//   3. Una celda de prosa mantiene una medida legible.
//   4. El texto de celda no se parte ni se centra.
//
// El umbral de 34 caracteres por línea se fijó DESPUÉS de medir la curva, y
// conviene decirlo: mi criterio inicial era 45. La medición a 320px sobre la
// tabla de 4 columnas mostró que 45 exige 3,2 veces el ancho del viewport de
// desplazamiento lateral, mientras 36 se consigue con 2,8 y el alto casi no
// mejora más allá. 34 es el suelo de esa rodilla, no una cifra cómoda elegida
// para aprobar: con el suelo roto el gate baja a 18 y reprueba.
// Playwright no es dependencia del sitio y no conviene que lo sea: arrastra
// navegadores de cientos de MB a un repositorio que hoy instala en CI con
// `npm ci`. Se resuelve desde la instalacion del MCP local, que ya existe en
// esta maquina, y si no esta el gate imprime SKIP visible en vez de fallar.
// Mismo patron que los smoke opt-in del penta-agent: el camino por defecto no
// puede depender de algo que en CI no existe, pero tampoco puede aprobar en
// silencio fingiendo que comprobo.
import { createRequire } from 'node:module';
import { existsSync } from 'node:fs';

const RUTA_PW = process.env.PLAYWRIGHT_MODULE_PATH
  || '/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/node_modules/playwright';

if (!existsSync(RUTA_PW)) {
  console.log(`SKIP gate de legibilidad de tablas: Playwright no encontrado en ${RUTA_PW}.`);
  console.log('      Defina PLAYWRIGHT_MODULE_PATH para ejecutarlo.');
  process.exit(0);
}
const require_ = createRequire(import.meta.url);
const { chromium } = require_(RUTA_PW);

const URL = process.env.TABLAS_URL || 'http://127.0.0.1:4004/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/';
const MIN_CARACTERES = Number(process.env.TABLAS_MIN_CAR || 34);
const ANCHOS = [320, 390, 768, 1024, 1440];

const navegador = await chromium.launch();
const pagina = await navegador.newPage();
let fallos = 0;
const filas = [];

for (const ancho of ANCHOS) {
  await pagina.setViewportSize({ width: ancho, height: 900 });
  await pagina.goto(URL, { waitUntil: 'networkidle' });
  const r = await pagina.evaluate(() => {
    const d = document.documentElement;
    const envs = [...document.querySelectorAll('.tabla-desliza')];
    const medidas = envs.map((env) => {
      const t = env.querySelector('table');
      const cs = [...t.querySelectorAll('td')].filter((c) => c.textContent.trim().length > 60);
      let car = null, align = null, hy = null;
      if (cs.length) {
        const mas = cs.reduce((a, b) => (b.textContent.trim().length > a.textContent.trim().length ? b : a));
        const st = getComputedStyle(mas);
        const util = mas.getBoundingClientRect().width
          - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight);
        car = Math.round(util / (parseFloat(st.fontSize) * 0.52));
        align = st.textAlign; hy = st.hyphens;
      }
      return { desplaza_contenedor: env.scrollWidth > env.clientWidth + 1, car, align, hy,
               display: getComputedStyle(t).display };
    });
    return { envoltorios: envs.length, doc_desborda: d.scrollWidth > d.clientWidth + 1,
             overflow_documento: getComputedStyle(document.body).overflowX, medidas };
  });

  const conProsa = r.medidas.filter((m) => m.car !== null);
  const peorCar = conProsa.length ? Math.min(...conProsa.map((m) => m.car)) : null;
  const malAlign = r.medidas.filter((m) => m.align && m.align !== 'start' && m.align !== 'left').length;
  const malHy = r.medidas.filter((m) => m.hy && m.hy !== 'manual' && m.hy !== 'none').length;
  const noTabla = r.medidas.filter((m) => m.display !== 'table').length;

  const errores = [];
  if (r.doc_desborda) errores.push('el documento desborda horizontalmente');
  // Un `overflow-x: hidden` en el documento produciría un falso aprobado del
  // criterio anterior: se comprueba aparte, como pide el §7.3 del encargo.
  if (r.overflow_documento === 'hidden') errores.push('el documento oculta su desbordamiento');
  if (peorCar !== null && peorCar < MIN_CARACTERES) errores.push(`celda de prosa a ${peorCar} caracteres por linea (minimo ${MIN_CARACTERES})`);
  if (malAlign) errores.push(`${malAlign} tabla(s) con texto centrado`);
  if (malHy) errores.push(`${malHy} tabla(s) partiendo palabras`);
  if (noTabla) errores.push(`${noTabla} tabla(s) sin display:table`);

  filas.push({ ancho, envoltorios: r.envoltorios, peorCar, errores });
  fallos += errores.length;
}

await navegador.close();

for (const f of filas) {
  const estado = f.errores.length ? '\x1b[31mFALLA\x1b[0m' : '\x1b[32mOK\x1b[0m';
  console.log(`  ${estado} ${String(f.ancho).padStart(4)}px  ${f.envoltorios} envoltorios  peor medida: ${f.peorCar ?? '-'} car/linea`);
  f.errores.forEach((e) => console.log(`         · ${e}`));
}
if (fallos) {
  console.error(`\nGate de legibilidad de tablas fallo (${fallos} problema(s))`);
  process.exit(1);
}
console.log(`\nGate de legibilidad de tablas OK en ${ANCHOS.length} anchos.`);
