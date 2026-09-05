#!/usr/bin/env node
// Gate de legibilidad de tablas.
//
// Mide en navegador, no en la hoja de estilos. Una regla correcta que no gana en
// la cascada da el mismo resultado que una regla ausente, y eso es exactamente lo
// que pasó aquí: `.tabla-desliza td { text-align: start }` perdía contra
// `.page__content table td { text-align: center }` por especificidad, y el
// centrado sobrevivía sin que nada avisara.
//
// Barre TODAS las páginas con tablas envueltas, no solo la que motivó el arreglo:
// el cambio de CSS alcanza a los 12 posts con tabla del sitio, y verificar uno
// dejaría 55 de las 62 tablas sin comprobar.
//
// Criterios, del §7 del encargo de tablas responsivas
// (archivo/handoffs/2026-09-04_handoff_prompt_codex_tablas_responsivas_3cucharadas.md):
//   · el documento no desborda horizontalmente, y no por haberlo ocultado
//   · la prosa de celda mantiene una medida legible
//   · el texto de celda no se centra ni se parte
//   · la tabla conserva su caja tabular
//   · una tabla numérica, que no lleva suelo, no empieza a desplazarse
//
// El umbral de 34 caracteres por línea se fijó ANTES de medir la curva de suelos.
// La medición mostró después que 45 costaría 3,6 veces el ancho del viewport de
// desplazamiento lateral y que 28 se conseguiría con 2,7. Se mantuvo 34 para no
// mover el listón tras ver los datos.
//
// Uso:
//   node scripts/verify_tables_readable.mjs
//   TABLAS_BASE=http://127.0.0.1:4004 TABLAS_ANCHOS=390 node scripts/...
import { createRequire } from 'node:module';
import { existsSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';

// Playwright no es dependencia del sitio y no conviene que lo sea: arrastra
// navegadores de cientos de MB a un repositorio que instala con `npm ci`. Se
// resuelve desde la instalación del MCP local; si no está, SKIP visible en vez de
// aprobar en silencio.
const RUTA_PW = process.env.PLAYWRIGHT_MODULE_PATH
  || '/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/node_modules/playwright';
if (!existsSync(RUTA_PW)) {
  console.log(`SKIP gate de legibilidad de tablas: Playwright no encontrado en ${RUTA_PW}.`);
  console.log('      Defina PLAYWRIGHT_MODULE_PATH para ejecutarlo.');
  process.exit(0);
}
const { chromium } = createRequire(import.meta.url)(RUTA_PW);

const BASE = process.env.TABLAS_BASE || 'http://127.0.0.1:4004';
const RAIZ = process.env.TABLAS_RAIZ || 'public';
const MIN_CARACTERES = Number(process.env.TABLAS_MIN_CAR || 34);
const ANCHOS = (process.env.TABLAS_ANCHOS || '320,390,768,1024,1440').split(',').map(Number);

function paginasConTabla(dir, salida = []) {
  for (const entrada of readdirSync(dir)) {
    const ruta = join(dir, entrada);
    if (statSync(ruta).isDirectory()) {
      if (['assets', 'catastro_sii_brecha', 'vendor', 'node_modules'].includes(entrada)) continue;
      paginasConTabla(ruta, salida);
    } else if (entrada === 'index.html' && readFileSync(ruta, 'utf8').includes('class="tabla-desliza"')) {
      salida.push('/' + relative(RAIZ, ruta).replace(/index\.html$/, ''));
    }
  }
  return salida;
}

const RUTAS = paginasConTabla(RAIZ);
if (!RUTAS.length) {
  console.log('SKIP gate de legibilidad de tablas: ninguna página construida con tablas envueltas.');
  process.exit(0);
}

const navegador = await chromium.launch();
const pagina = await navegador.newPage();
const filas = [];

for (const ancho of ANCHOS) {
  await pagina.setViewportSize({ width: ancho, height: 900 });
  for (const ruta of RUTAS) {
    await pagina.goto(BASE + ruta, { waitUntil: 'networkidle' });
    const r = await pagina.evaluate(() => {
      const d = document.documentElement;
      const envs = [...document.querySelectorAll('.tabla-desliza')];
      const medidas = envs.map((env) => {
        const t = env.querySelector('table');
        const cs = [...t.querySelectorAll('td')].filter((c) => c.textContent.trim().length > 60);
        let car = null; let align = null; let hy = null;
        if (cs.length) {
          const mas = cs.reduce((a, b) => (b.textContent.trim().length > a.textContent.trim().length ? b : a));
          const st = getComputedStyle(mas);
          const util = mas.getBoundingClientRect().width
            - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight);
          car = Math.round(util / (parseFloat(st.fontSize) * 0.52));
          align = st.textAlign; hy = st.hyphens;
        }
        return {
          perfil: env.dataset.perfil,
          desplaza: env.scrollWidth > env.clientWidth + 1,
          car, align, hy,
          display: getComputedStyle(t).display,
          minWidth: getComputedStyle(t).minWidth
        };
      });
      return {
        envoltorios: envs.length,
        doc_desborda: d.scrollWidth > d.clientWidth + 1,
        overflow_body: getComputedStyle(document.body).overflowX,
        medidas
      };
    });

    const conProsa = r.medidas.filter((m) => m.car !== null);
    const peorCar = conProsa.length ? Math.min(...conProsa.map((m) => m.car)) : null;
    const errores = [];

    if (r.doc_desborda) errores.push('el documento desborda horizontalmente');
    // Un `overflow-x: hidden` produciría un falso aprobado del criterio anterior:
    // se comprueba aparte, como pide el §7.3 del encargo.
    if (r.overflow_body === 'hidden') errores.push('el documento oculta su desbordamiento');
    if (peorCar !== null && peorCar < MIN_CARACTERES) {
      errores.push(`celda de prosa a ${peorCar} caracteres por linea (minimo ${MIN_CARACTERES})`);
    }
    const malAlign = r.medidas.filter((m) => m.align && !['start', 'left'].includes(m.align)).length;
    const malHy = r.medidas.filter((m) => m.hy && !['manual', 'none'].includes(m.hy)).length;
    const noTabla = r.medidas.filter((m) => m.display !== 'table').length;
    if (malAlign) errores.push(`${malAlign} tabla(s) con texto centrado`);
    if (malHy) errores.push(`${malHy} tabla(s) partiendo palabras`);
    if (noTabla) errores.push(`${noTabla} tabla(s) sin display:table`);

    // Regresión propia de este arreglo: el suelo es para las narrativas y no debe
    // imponerse a una tabla numérica.
    //
    // La primera versión de esta comprobación era otra —«una numérica no debería
    // desplazarse»— y estaba mal. Medido el 2026-09-05: de las cuatro tablas de
    // CASEN, tres caben con holgura (−43, −154 y −159 px de margen) y solo la de
    // 7 columnas excede en 129 px de 584. Antes cabía porque `display: block` la
    // estrujaba; ahora toma su ancho natural y desplaza un poco. Eso es lo que el
    // encargo pide, no una regresión, y el criterio marcaba en rojo el
    // comportamiento correcto.
    //
    // Lo que sí hay que proteger es que el suelo no se filtre: cualquier
    // desplazamiento de una numérica debe ser intrínseco a su contenido, nunca
    // impuesto por nosotros.
    const numConSuelo = r.medidas.filter((m) => m.perfil === 'numerica' && m.minWidth !== '0px').length;
    if (numConSuelo) {
      errores.push(`${numConSuelo} tabla(s) numerica(s) con min-width impuesto`);
    }

    filas.push({ ancho, ruta, peorCar, errores });
  }
}

await navegador.close();

for (const f of filas.filter((x) => x.errores.length)) {
  console.log(`  \x1b[31mFALLA\x1b[0m ${String(f.ancho).padStart(4)}px  ${f.ruta}`);
  f.errores.forEach((e) => console.log(`         · ${e}`));
}
for (const ancho of ANCHOS) {
  const lote = filas.filter((f) => f.ancho === ancho);
  const malos = lote.filter((f) => f.errores.length).length;
  const cars = lote.map((f) => f.peorCar).filter((c) => c !== null);
  const estado = malos ? '\x1b[31mFALLA\x1b[0m' : '\x1b[32mOK\x1b[0m';
  console.log(`  ${estado} ${String(ancho).padStart(4)}px  ${lote.length} pagina(s)  peor medida: ${cars.length ? Math.min(...cars) : '-'} car/linea`);
}

const totalErrores = filas.reduce((s, f) => s + f.errores.length, 0);
if (totalErrores) {
  console.error(`\nGate de legibilidad de tablas fallo (${totalErrores} problema(s))`);
  process.exit(1);
}
console.log(`\nGate de legibilidad de tablas OK: ${RUTAS.length} pagina(s) x ${ANCHOS.length} anchos.`);
