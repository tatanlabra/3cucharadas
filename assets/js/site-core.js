/* Comportamiento base del sitio sin jQuery (capa 2, fase A; auditoría UX 2026-10-17).

   Reemplaza assets/js/main.min.js de Minimal Mistakes (124 KB: jQuery 3, FitVids,
   SmoothScroll, Gumshoe, Magnific Popup y su _main.js). Cada bloque reproduce lo que
   hacía el tema, con las mismas clases de estado, para que su CSS siga valiendo:

   - «Seguir» del autor: .author__urls.is--visible y button.open, ahora con
     aria-expanded;
   - buscador: .search-content.is--visible e .initial-content.is--hidden, Esc
     cierra y el foco va al campo (lunr-site.js sincroniza aria-expanded);
   - desplazamiento suave: en CSS (scroll-behavior), solo sin movimiento reducido;
   - índice activo: li.active en nav.toc, como Gumshoe con offset de 20 px, y el
     índice fijo se desplaza para mantener visible el ítem activo;
   - anclas de títulos: a.header-link en los títulos con id;
   - copiar código: botón en cada pre > code de .page__content;
   - imágenes ampliables: <dialog> nativo en vez de Magnific Popup, con galería,
     teclado y foco restaurado al cerrar.

   FitVids no se reemplaza: el sitio no tiene videos incrustados; los iframes de
   visores ya traen su tamaño. */
(function () {
  "use strict";

  var lang = (document.documentElement.getAttribute("lang") || "es").slice(0, 2);
  var t = lang === "en"
    ? { permalink: "Permalink", copy: "Copy code", copied: "Copied", close: "Close", prev: "Previous image", next: "Next image", of: "of" }
    : { permalink: "Enlace permanente", copy: "Copiar código", copied: "Copiado", close: "Cerrar", prev: "Imagen anterior", next: "Imagen siguiente", of: "de" };

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    followMenu();
    searchToggle();
    tocSpy();
    headingAnchors();
    copyButtons();
    lightbox();
  });

  function followMenu() {
    var button = document.querySelector(".author__urls-wrapper button");
    var list = document.querySelector(".author__urls");
    if (!button || !list) return;
    if (!list.id) list.id = "author-urls";
    button.setAttribute("aria-controls", list.id);
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", function () {
      var open = list.classList.toggle("is--visible");
      button.classList.toggle("open", open);
      button.setAttribute("aria-expanded", String(open));
    });
  }

  function searchToggle() {
    var toggle = document.querySelector(".search__toggle");
    var search = document.querySelector(".search-content");
    var initial = document.querySelector(".initial-content");
    if (!toggle || !search || !initial) return;

    function setOpen(open) {
      search.classList.toggle("is--visible", open);
      initial.classList.toggle("is--hidden", open);
      if (open) {
        // El panel entra con una transición del tema; enfocar antes la cortaría.
        window.setTimeout(function () {
          var input = search.querySelector("input");
          if (input) input.focus();
        }, 400);
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(!search.classList.contains("is--visible"));
    });
    document.addEventListener("keyup", function (event) {
      if (event.key === "Escape" && initial.classList.contains("is--hidden")) setOpen(false);
    });
  }

  function tocSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll("nav.toc a[href^='#']"));
    if (!links.length) return;
    var OFFSET = 20;
    var targets = links.map(function (a) {
      var id = decodeURIComponent(a.getAttribute("href").slice(1));
      return { link: a, item: a.parentElement, target: document.getElementById(id) };
    }).filter(function (x) { return x.target; });
    if (!targets.length) return;
    var current = null;
    var pending = false;

    function keepVisible(link) {
      var aside = document.querySelector("aside.sidebar__right.sticky");
      if (!aside || window.getComputedStyle(aside).position !== "sticky") return;
      for (var box = link.parentElement; box && box !== aside.parentElement; box = box.parentElement) {
        if (box.scrollHeight > box.clientHeight + 1 && /(auto|scroll)/.test(window.getComputedStyle(box).overflowY)) {
          var top = link.offsetTop - box.offsetTop;
          if (top < box.scrollTop) box.scrollTop = top;
          else if (top + link.offsetHeight > box.scrollTop + box.clientHeight) box.scrollTop = top + link.offsetHeight - box.clientHeight;
          return;
        }
      }
    }

    function update() {
      pending = false;
      var active = null;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].target.getBoundingClientRect().top - OFFSET <= 1) active = targets[i];
      }
      if (active === current) return;
      if (current) current.item.classList.remove("active");
      current = active;
      if (current) {
        current.item.classList.add("active");
        keepVisible(current.link);
      }
    }

    window.addEventListener("scroll", function () {
      if (!pending) { pending = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  function headingAnchors() {
    var content = document.querySelector(".page__content");
    if (!content) return;
    content.querySelectorAll("h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]").forEach(function (heading) {
      if (heading.querySelector(".header-link")) return;
      var anchor = document.createElement("a");
      anchor.className = "header-link";
      anchor.href = "#" + heading.id;
      anchor.title = t.permalink;
      anchor.innerHTML = '<span class="sr-only">' + t.permalink + '</span><i class="fas fa-link" aria-hidden="true"></i>';
      heading.appendChild(anchor);
    });
  }

  function copyButtons() {
    if (!window.enable_copy_code_button) return;
    document.querySelectorAll(".page__content pre > code").forEach(function (code) {
      var pre = code.parentElement;
      if (pre.querySelector(".clipboard-copy-button")) return;
      var button = document.createElement("button");
      button.type = "button";
      button.className = "clipboard-copy-button";
      button.title = t.copy;
      button.innerHTML = '<span class="sr-only">' + t.copy + '</span><i class="far fa-fw fa-copy" aria-hidden="true"></i><i class="fas fa-fw fa-check copied" aria-hidden="true"></i>';
      button.addEventListener("click", function () {
        var source = code.querySelector("td.code, td.rouge-code") || code;
        var done = function () {
          button.classList.add("copied");
          button.setAttribute("aria-label", t.copied);
          window.setTimeout(function () {
            button.classList.remove("copied");
            button.removeAttribute("aria-label");
          }, 1500);
        };
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(source.innerText).then(done, function () {});
        }
      });
      pre.insertBefore(button, pre.firstChild);
    });
  }

  function lightbox() {
    var selector = "a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif'],a[href$='.webp']";
    document.querySelectorAll(selector).forEach(function (a) {
      if (a.querySelector(":scope > img")) a.classList.add("image-popup");
    });
    var links = Array.prototype.slice.call(document.querySelectorAll("a.image-popup"));
    if (!links.length || typeof HTMLDialogElement !== "function") return;

    var dialog = document.createElement("dialog");
    dialog.className = "lightbox";
    dialog.innerHTML =
      '<figure class="lightbox__figure"><img class="lightbox__img" alt=""><figcaption class="lightbox__caption"></figcaption></figure>' +
      '<button type="button" class="lightbox__close" aria-label="' + t.close + '">×</button>' +
      '<button type="button" class="lightbox__prev" aria-label="' + t.prev + '">‹</button>' +
      '<button type="button" class="lightbox__next" aria-label="' + t.next + '">›</button>';
    document.body.appendChild(dialog);
    var img = dialog.querySelector(".lightbox__img");
    var caption = dialog.querySelector(".lightbox__caption");
    var prev = dialog.querySelector(".lightbox__prev");
    var next = dialog.querySelector(".lightbox__next");
    var index = 0;

    function show(i) {
      index = (i + links.length) % links.length;
      var link = links[index];
      var thumb = link.querySelector("img");
      img.src = link.getAttribute("href");
      img.alt = thumb ? thumb.getAttribute("alt") || "" : "";
      var label = img.alt || "";
      caption.textContent = links.length > 1 ? (index + 1) + " " + t.of + " " + links.length + (label ? " · " + label : "") : label;
      prev.hidden = next.hidden = links.length < 2;
    }

    links.forEach(function (link, i) {
      link.addEventListener("click", function (event) {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
        event.preventDefault();
        show(i);
        dialog.showModal();
      });
    });
    dialog.querySelector(".lightbox__close").addEventListener("click", function () { dialog.close(); });
    prev.addEventListener("click", function () { show(index - 1); });
    next.addEventListener("click", function () { show(index + 1); });
    // Como Magnific Popup con closeOnContentClick: clic en la imagen o el fondo cierra.
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog || event.target === img) dialog.close();
    });
    dialog.addEventListener("keydown", function (event) {
      if (links.length < 2) return;
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });
  }
})();
