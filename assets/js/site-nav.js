/**
 * Barra de navegación y tabla de contenidos en móvil.
 *
 * Sustituye al greedy-nav del tema, que decidía qué enlaces caben midiendo
 * anchos en cada `resize`. Ese cálculo ignoraba dos controles que el sitio
 * inyectaba dentro del <nav>, medía la lupa antes de que llegara Font Awesome y
 * medía el título después de que el navegador ya lo hubiera encogido. Con dos
 * ítems de menú no hay reparto que optimizar, así que aquí no se mide nada: el
 * CSS decide con un breakpoint y este archivo sólo gestiona estado y foco.
 *
 * `aria-expanded` es la única fuente de verdad. El CSS abre el panel con
 * `[aria-expanded="true"] ~ .masthead__nav-list`, de modo que el estado accesible y
 * el visual no pueden divergir.
 */
(function () {
  "use strict";

  var DESKTOP = "(min-width: 48em)";

  var nav = document.getElementById("site-nav");
  var toggle = nav && nav.querySelector(".masthead__nav-toggle");
  var menu = document.getElementById("site-nav-menu");
  var desktop = window.matchMedia(DESKTOP);

  function isOpen() {
    return toggle.getAttribute("aria-expanded") === "true";
  }

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function close(restoreFocus) {
    if (!isOpen()) return;
    setOpen(false);
    // Sólo se devuelve el foco cuando el cierre fue intencional (Escape). Tras un
    // clic fuera, robarlo sacaría al usuario de donde acaba de pulsar.
    if (restoreFocus) toggle.focus();
  }

  if (toggle && menu) {
    // El botón sólo existe para quien tiene JavaScript. Sin él, `.no-js` deja la
    // lista visible y oculta el botón, así que la navegación nunca queda
    // inalcanzable.
    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) close(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close(true);
    });

    // `pointerdown` y no `click`: cierra antes de que el navegador procese la
    // pulsación, de modo que el destino no se desplaza bajo el dedo.
    document.addEventListener("pointerdown", function (event) {
      if (!nav.contains(event.target)) close(false);
    });

    // Al cruzar a escritorio la lista vuelve a ser inline. Si el panel siguiera
    // marcado como abierto, `aria-expanded="true"` describiría un panel que ya
    // no existe.
    addMediaListener(desktop, function (matches) {
      if (matches) close(false);
    });
  }

  /**
   * La tabla de contenidos se colapsa en <details> por debajo de $large: en un
   * post largo, el índice completo empujaba el cuerpo del artículo fuera de la
   * primera pantalla. Desde $large recupera su forma de columna fija.
   *
   * `open` es una propiedad del DOM y no puede gobernarse desde una media query,
   * así que la sincroniza este listener.
   */
  function syncTableOfContents(matches) {
    var panels = document.querySelectorAll(".toc__details");
    for (var i = 0; i < panels.length; i += 1) {
      panels[i].open = matches;
    }
  }

  function addMediaListener(query, handler) {
    handler(query.matches);
    if (typeof query.addEventListener === "function") {
      query.addEventListener("change", function (event) {
        handler(event.matches);
      });
    } else if (typeof query.addListener === "function") {
      // Safari < 14 y navegadores antiguos: `MediaQueryList` no era EventTarget.
      query.addListener(function (event) {
        handler(event.matches);
      });
    }
  }

  addMediaListener(desktop, syncTableOfContents);
})();
