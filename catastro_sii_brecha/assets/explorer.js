/*!
 * explorer.js · Explorador de burbujas comunal — Catastro SII / brecha UV-avalúo.
 *
 * Scatter tipo Rosling, sin animación, con cuatro selectores (eje X, eje Y,
 * tamaño y color) sobre las 346 comunas. Sin dependencias: el SVG se arma con
 * createElementNS y no se usa innerHTML en ningún punto (hay CSP en _headers).
 *
 * Montaje — la página sólo aporta un contenedor vacío:
 *
 *   <link rel="stylesheet" href="assets/explorer.css">
 *   <div id="explorador-burbujas" data-src="data/explorador_comunal.json"></div>
 *   <script src="assets/explorer.js" defer></script>
 *
 * Toda la interfaz se construye desde aquí a propósito: index.html y style.css
 * se editan en paralelo y este módulo no debe depender de su marcado.
 */
(() => {
  "use strict";

  const host = document.querySelector("[data-explorador], #explorador-burbujas");
  if (!host) return; // La página no incluye el explorador: nada que hacer.

  const NS = "http://www.w3.org/2000/svg";
  const FUENTE = host.dataset.src || "data/explorador_comunal.json";

  /* Metadatos por variable: [etiqueta, sufijo, roles].
     roles: "x" habilita el uso en ejes, "s" en tamaño, "c" en color continuo.
     Los decimales NO se declaran aquí: se deducen del rango observado (ver
     decimales()), así el explorador no tiene que asumir si una participación
     llega en 0–1 o en 0–100 ni queda desincronizado si el pipeline cambia. */
  const VARS = {
    avaluo_total_mmm: ["Avalúo total", " MMM$", "xsc"],
    predios: ["Predios", "", "xs"],
    poblacion_censo: ["Población (Censo)", "", "xs"],
    poblacion_rsh: ["Población (RSH)", "", "s"],
    hogares: ["Hogares (RSH)", "", "s"],
    n_uv: ["Unidades vecinales", "", "s"],
    superficie_km2: ["Superficie", " km²", "x"],
    gini_avaluo: ["Gini del avalúo", "", "xc"],
    share_top10: ["Participación del decil superior", "", "xc"],
    p90_p50: ["Razón P90/P50", "", "xc"],
    pct_urbano: ["Predios urbanos", "%", "xc"],
    cobertura_coords_pct: ["Cobertura de coordenadas", "%", "xc"],
    vulnerabilidad_media: ["Vulnerabilidad media (RSH)", "", "xc"]
  };

  /* Por defecto: avalúo total en log contra vulnerabilidad. Es la lectura más
     directa de la brecha y estrena la escala log, que esta serie necesita. */
  const estado = { x: "avaluo_total_mmm", y: "vulnerabilidad_media", s: "poblacion_censo", c: "region", xlog: true, ylog: false };

  const MARGEN = { arriba: 14, derecha: 16, abajo: 48, izquierda: 62 };
  const CLASES = 5; // Cortes del color continuo.

  let datos = null;
  let anchoPrevio = 0;
  let temporizador = 0;
  const decimalesPorVar = new Map();

  /* ---------- utilidades de DOM ---------- */

  function nodoSvg(etiqueta, atributos) {
    const nodo = document.createElementNS(NS, etiqueta);
    for (const clave in atributos) nodo.setAttribute(clave, atributos[clave]);
    return nodo;
  }

  function nodo(etiqueta, clase, texto) {
    const elemento = document.createElement(etiqueta);
    if (clase) elemento.className = clase;
    if (texto != null) elemento.textContent = texto;
    return elemento;
  }

  /* ---------- formato numérico ---------- */

  /* Los decimales salen del orden de magnitud de la serie: conteos grandes sin
     decimales, índices acotados con tres. Evita rotular "45,300" un porcentaje. */
  function decimales(clave) {
    if (decimalesPorVar.has(clave)) return decimalesPorVar.get(clave);
    let max = 0;
    for (const valor of datos.series[clave] || []) {
      const absoluto = Math.abs(valor);
      if (valor != null && absoluto > max) max = absoluto;
    }
    const cifras = max >= 1000 ? 0 : max >= 100 ? 1 : max >= 10 ? 2 : 3;
    decimalesPorVar.set(clave, cifras);
    return cifras;
  }

  function fmt(clave, valor) {
    if (valor == null) return "sin dato";
    const cifras = decimales(clave);
    return valor.toLocaleString("es-CL", { minimumFractionDigits: cifras, maximumFractionDigits: cifras }) + VARS[clave][1];
  }

  /* Los ejes usan notación compacta sobre 10.000 ("1,2 M"): un rótulo de eje con
     nueve dígitos se pisa con el vecino. El tooltip siempre da la cifra completa. */
  function fmtEje(valor, compacto) {
    const opciones = compacto
      ? { notation: "compact", maximumFractionDigits: 1 }
      : { maximumFractionDigits: Math.abs(valor) >= 100 ? 0 : Math.abs(valor) >= 1 ? 2 : 3 };
    return valor.toLocaleString("es-CL", opciones);
  }

  /* ---------- escalas ---------- */

  function dominio(valores) {
    let bajo = Infinity;
    let alto = -Infinity;
    for (const valor of valores) {
      if (valor < bajo) bajo = valor;
      if (valor > alto) alto = valor;
    }
    if (!(bajo < alto)) { bajo -= 0.5; alto += 0.5; } // Serie constante o de un punto.
    const holgura = (alto - bajo) * 0.06; // Deja aire para que las burbujas del borde no se corten.
    return [bajo - holgura, alto + holgura];
  }

  function pasoLegible(bruto) {
    const magnitud = Math.pow(10, Math.floor(Math.log10(bruto)));
    const normal = bruto / magnitud;
    return (normal <= 1 ? 1 : normal <= 2 ? 2 : normal <= 5 ? 5 : 10) * magnitud;
  }

  /* Devuelve [{t, v}] con t en el espacio transformado (log10 si aplica) y v en
     unidades originales para el rótulo. */
  function marcas([bajo, alto], log) {
    const salida = [];
    if (log) {
      const desde = Math.floor(bajo);
      const hasta = Math.ceil(alto);
      // Con pocas décadas visibles se intercalan 2 y 5; si no, el eje se satura.
      const mantisas = hasta - desde <= 3 ? [1, 2, 5] : [1];
      for (let decada = desde; decada <= hasta; decada++) {
        for (const mantisa of mantisas) {
          const t = decada + Math.log10(mantisa);
          if (t >= bajo && t <= alto) salida.push({ t, v: mantisa * Math.pow(10, decada) });
        }
      }
      return salida;
    }
    const paso = pasoLegible((alto - bajo) / 5);
    for (let valor = Math.ceil(bajo / paso) * paso; valor <= alto + paso * 1e-9; valor += paso) {
      salida.push({ t: valor, v: valor });
    }
    return salida;
  }

  /* Cortes por cuantiles, no por intervalos iguales: el avalúo tiene cola derecha
     extrema y un corte uniforme dejaría cuatro clases vacías. */
  function cortes(valores) {
    const ordenados = valores.filter((valor) => valor != null).sort((a, b) => a - b);
    const salida = [];
    if (!ordenados.length) return salida;
    for (let i = 1; i < CLASES; i++) salida.push(ordenados[Math.floor((ordenados.length * i) / CLASES)]);
    return salida;
  }

  function claseDe(valor, limites) {
    let indice = 0;
    while (indice < limites.length && valor >= limites[indice]) indice++;
    return indice;
  }

  /* ---------- interfaz ---------- */

  const controles = nodo("div", "exp-controles");
  const svg = nodoSvg("svg", { class: "exp-svg", preserveAspectRatio: "xMidYMid meet", role: "img" });
  const leyenda = nodo("div", "exp-leyenda");
  const estatus = nodo("p", "exp-estatus", "Cargando datos comunales…");
  estatus.setAttribute("role", "status");

  function selector(id, etiqueta, rol, valorInicial, extra) {
    const campo = nodo("label", "exp-campo");
    campo.setAttribute("for", id);
    campo.append(nodo("span", "exp-campo-titulo", etiqueta));
    const caja = nodo("span", "exp-select-wrap");
    const select = nodo("select");
    select.id = id;
    for (const opcion of extra || []) {
      const item = nodo("option", null, opcion[1]);
      item.value = opcion[0];
      select.append(item);
    }
    for (const clave in VARS) {
      if (!VARS[clave][2].includes(rol)) continue;
      const item = nodo("option", null, VARS[clave][0]);
      item.value = clave;
      select.append(item);
    }
    select.value = valorInicial;
    caja.append(select);
    campo.append(caja);
    controles.append(campo);
    return select;
  }

  function casilla(id, etiqueta, marcada) {
    const envoltura = nodo("label", "exp-casilla");
    envoltura.setAttribute("for", id);
    const entrada = nodo("input");
    entrada.type = "checkbox";
    entrada.id = id;
    entrada.checked = marcada;
    envoltura.append(entrada, nodo("span", null, etiqueta));
    return { envoltura, entrada };
  }

  function montarControles() {
    const selX = selector("exp-x", "01 · Eje horizontal", "x", estado.x);
    const logX = casilla("exp-x-log", "Escala logarítmica", estado.xlog);
    controles.append(logX.envoltura);
    const selY = selector("exp-y", "02 · Eje vertical", "x", estado.y);
    const logY = casilla("exp-y-log", "Escala logarítmica", estado.ylog);
    controles.append(logY.envoltura);
    const selS = selector("exp-size", "03 · Tamaño de burbuja", "s", estado.s);
    const selC = selector("exp-color", "04 · Color", "c", estado.c, [["region", "Región"], ["", "Sin color"]]);

    const enlazar = (elemento, campo, propiedad) => elemento.addEventListener("change", () => {
      estado[campo] = elemento[propiedad];
      dibujar();
    });
    enlazar(selX, "x", "value");
    enlazar(selY, "y", "value");
    enlazar(selS, "s", "value");
    enlazar(selC, "c", "value");
    enlazar(logX.entrada, "xlog", "checked");
    enlazar(logY.entrada, "ylog", "checked");

    host.append(controles, svg, leyenda, estatus);
  }

  /* ---------- dibujo ---------- */

  /* El viewBox se calcula desde el ancho medido en vez de fijarse: un viewBox de
     800 escalado a un móvil de 360 px dejaría los rótulos en ~5 px reales. Con
     escala ~1:1 la tipografía del eje mide lo que dice medir. preserveAspectRatio
     mantiene la proporción entre resize y resize. */
  function anchoUtil() {
    return Math.max(320, Math.min(920, Math.round(host.clientWidth || 720)));
  }

  function ordenRegiones() {
    /* Las regiones se ordenan por el menor código comunal, que reproduce el orden
       administrativo (I a XVI). Así la paleta —un espectro continuo— se lee como
       gradiente territorial y no como 16 colores sueltos, que serían
       indistinguibles de todos modos. */
    const minimos = new Map();
    for (let i = 0; i < datos.n; i++) {
      const region = datos.region[i];
      const codigo = Number(datos.codigo[i]) || 0;
      if (!minimos.has(region) || codigo < minimos.get(region)) minimos.set(region, codigo);
    }
    const nombres = [...minimos.keys()].sort((a, b) => minimos.get(a) - minimos.get(b));
    const indices = new Map();
    nombres.forEach((nombre, indice) => indices.set(nombre, indice));
    return { nombres, indices };
  }

  function textoBurbuja(indice, claves) {
    const lineas = [datos.comuna[indice] + " · " + datos.region[indice]];
    for (const clave of claves) lineas.push(VARS[clave][0] + ": " + fmt(clave, datos.series[clave][indice]));
    return lineas.join("\n");
  }

  function ejes(grupo, ancho, alto, dx, dy, aX, aY) {
    const { izquierda: L, arriba: T } = MARGEN;
    const pAncho = ancho - L - MARGEN.derecha;
    const pAlto = alto - T - MARGEN.abajo;

    for (const marca of marcas(dx, estado.xlog)) {
      const px = L + ((marca.t - dx[0]) / (dx[1] - dx[0])) * pAncho;
      grupo.append(nodoSvg("line", { class: "exp-rejilla", x1: px, y1: T, x2: px, y2: T + pAlto }));
      const rotulo = nodoSvg("text", { class: "exp-marca", x: px, y: T + pAlto + 18, "text-anchor": "middle" });
      rotulo.textContent = fmtEje(marca.v, aX);
      grupo.append(rotulo);
    }
    for (const marca of marcas(dy, estado.ylog)) {
      const py = T + pAlto - ((marca.t - dy[0]) / (dy[1] - dy[0])) * pAlto;
      grupo.append(nodoSvg("line", { class: "exp-rejilla", x1: L, y1: py, x2: L + pAncho, y2: py }));
      const rotulo = nodoSvg("text", { class: "exp-marca", x: L - 9, y: py + 4, "text-anchor": "end" });
      rotulo.textContent = fmtEje(marca.v, aY);
      grupo.append(rotulo);
    }

    const tituloX = nodoSvg("text", { class: "exp-eje-titulo", x: L + pAncho / 2, y: alto - 10, "text-anchor": "middle" });
    tituloX.textContent = VARS[estado.x][0] + (estado.xlog ? " (log)" : "");
    const tituloY = nodoSvg("text", {
      class: "exp-eje-titulo",
      x: 0, y: 0, "text-anchor": "middle",
      transform: "translate(14 " + (T + pAlto / 2) + ") rotate(-90)"
    });
    tituloY.textContent = VARS[estado.y][0] + (estado.ylog ? " (log)" : "");
    grupo.append(tituloX, tituloY);
  }

  function pintarLeyenda(modo, limites, regiones, claveColor) {
    leyenda.replaceChildren();
    if (modo === "ninguno") return;
    const titulo = nodo("p", "exp-leyenda-titulo", modo === "region" ? "Región" : VARS[claveColor][0]);
    leyenda.append(titulo);
    const lista = nodo("ul", "exp-leyenda-lista");
    if (modo === "region") {
      regiones.nombres.forEach((nombre, indice) => {
        const item = nodo("li");
        item.append(nodo("span", "exp-muestra exp-k" + (indice % 16)), nodo("span", null, nombre));
        lista.append(item);
      });
    } else {
      for (let clase = 0; clase < CLASES; clase++) {
        const desde = limites[clase - 1];
        const hasta = limites[clase];
        const texto = clase === 0
          ? "menos de " + fmt(claveColor, hasta)
          : clase === CLASES - 1 ? fmt(claveColor, desde) + " o más" : fmt(claveColor, desde) + " – " + fmt(claveColor, hasta);
        const item = nodo("li");
        item.append(nodo("span", "exp-muestra exp-c" + clase), nodo("span", null, texto));
        lista.append(item);
      }
      const item = nodo("li");
      item.append(nodo("span", "exp-muestra exp-cn"), nodo("span", null, "sin dato"));
      lista.append(item);
    }
    leyenda.append(lista);
  }

  function dibujar() {
    if (!datos) return;
    const ancho = anchoUtil();
    anchoPrevio = ancho;
    const alto = Math.max(300, Math.min(540, Math.round(ancho * 0.66)));
    const { izquierda: L, arriba: T } = MARGEN;
    const pAncho = ancho - L - MARGEN.derecha;
    const pAlto = alto - T - MARGEN.abajo;
    svg.setAttribute("viewBox", "0 0 " + ancho + " " + alto);

    const serieX = datos.series[estado.x];
    const serieY = datos.series[estado.y];
    const serieS = datos.series[estado.s];
    const claveColor = estado.c && estado.c !== "region" ? estado.c : null;
    const serieC = claveColor ? datos.series[claveColor] : null;

    // Un punto sólo entra si tiene las tres coordenadas; en log, además, positivas.
    const puntos = [];
    let descartados = 0;
    for (let i = 0; i < datos.n; i++) {
      const x = serieX[i];
      const y = serieY[i];
      const s = serieS[i];
      if (x == null || y == null || s == null || (estado.xlog && x <= 0) || (estado.ylog && y <= 0)) { descartados++; continue; }
      puntos.push(i);
    }

    const grupo = nodoSvg("g");
    if (!puntos.length) {
      svg.replaceChildren(grupo);
      leyenda.replaceChildren();
      estatus.textContent = "Ninguna comuna tiene datos para esta combinación. Prueba con otras variables o desactiva la escala logarítmica.";
      return;
    }

    const tx = estado.xlog ? Math.log10 : (valor) => valor;
    const ty = estado.ylog ? Math.log10 : (valor) => valor;
    const dx = dominio(puntos.map((i) => tx(serieX[i])));
    const dy = dominio(puntos.map((i) => ty(serieY[i])));
    const maxX = Math.max(...puntos.map((i) => Math.abs(serieX[i])));
    const maxY = Math.max(...puntos.map((i) => Math.abs(serieY[i])));

    ejes(grupo, ancho, alto, dx, dy, maxX >= 10000, maxY >= 10000);

    const px = (valor) => L + ((tx(valor) - dx[0]) / (dx[1] - dx[0])) * pAncho;
    const py = (valor) => T + pAlto - ((ty(valor) - dy[0]) / (dy[1] - dy[0])) * pAlto;

    /* Radio proporcional a la raíz del valor sobre el máximo: es el área —no el
       radio— la que codifica la magnitud. El piso de 3 px evita que las comunas
       chicas desaparezcan cuando el máximo es un orden mayor. */
    const maxS = Math.max(...puntos.map((i) => serieS[i]));
    const radioMax = Math.max(11, Math.min(22, pAncho / 32));
    const radio = (valor) => Math.max(3, radioMax * Math.sqrt(Math.max(0, valor) / (maxS || 1)));

    let modo = "ninguno";
    let limites = [];
    let regiones = null;
    let colorDe = () => "exp-c2";
    if (estado.c === "region") {
      modo = "region";
      regiones = ordenRegiones();
      colorDe = (i) => "exp-k" + (regiones.indices.get(datos.region[i]) % 16);
    } else if (serieC) {
      modo = "continuo";
      limites = cortes(puntos.map((i) => serieC[i]));
      colorDe = (i) => serieC[i] == null ? "exp-cn" : "exp-c" + claseDe(serieC[i], limites);
    }

    // De mayor a menor: si no, las burbujas grandes tapan por completo a las chicas.
    const orden = puntos.slice().sort((a, b) => serieS[b] - serieS[a]);
    const claves = [...new Set([estado.x, estado.y, estado.s, claveColor].filter(Boolean))];
    const capa = nodoSvg("g", { class: "exp-burbujas" });
    for (const i of orden) {
      const circulo = nodoSvg("circle", {
        class: "exp-burbuja " + colorDe(i),
        cx: px(serieX[i]).toFixed(1),
        cy: py(serieY[i]).toFixed(1),
        r: radio(serieS[i]).toFixed(1)
      });
      const titulo = nodoSvg("title");
      titulo.textContent = textoBurbuja(i, claves);
      circulo.append(titulo);
      capa.append(circulo);
    }
    grupo.append(capa);
    svg.replaceChildren(grupo);

    pintarLeyenda(modo, limites, regiones, claveColor);

    const etiquetaColor = modo === "region" ? "región" : modo === "continuo" ? VARS[claveColor][0].toLowerCase() : "sin codificar";
    svg.setAttribute("aria-label",
      "Gráfico de burbujas de " + puntos.length + " comunas: " + VARS[estado.y][0].toLowerCase() +
      " según " + VARS[estado.x][0].toLowerCase() + ". El tamaño representa " + VARS[estado.s][0].toLowerCase() +
      " y el color, " + etiquetaColor + ". Cada burbuja muestra sus valores al posarse sobre ella.");
    estatus.textContent = puntos.length + " comunas en pantalla" +
      (descartados ? " · " + descartados + " sin dato en esta combinación" : "") + ".";
  }

  /* ---------- carga ---------- */

  function fallar() {
    controles.replaceChildren();
    svg.remove();
    leyenda.replaceChildren();
    estatus.textContent = "No fue posible cargar los datos del explorador. El resto de la ficha comunal sigue disponible.";
  }

  montarControles();

  fetch(FUENTE, { cache: "force-cache" })
    .then((respuesta) => {
      if (!respuesta.ok) throw new Error("respuesta " + respuesta.status);
      return respuesta.json();
    })
    .then((json) => {
      if (!json || !json.series || !json.n) throw new Error("estructura inesperada");
      datos = json;
      dibujar();
    })
    .catch(fallar); // Degradación silenciosa: mensaje en pantalla, no excepción en consola.

  /* El viewBox se recalcula sólo si el ancho cambió de verdad: el resize dispara
     decenas de eventos y cada redibujo son ~350 nodos. */
  window.addEventListener("resize", () => {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => {
      if (datos && Math.abs(anchoUtil() - anchoPrevio) > 8) dibujar();
    }, 160);
  });
})();
