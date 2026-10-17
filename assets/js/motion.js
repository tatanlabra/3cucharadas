/* Movimiento editorial de 3cucharadas (auditoría UX 2026-10-17; aprobado M1-M4).
 *
 * Reglas: nada se oculta antes de que este script corra (el estado pendiente lo pone
 * JS solo a lo que está bajo el pliegue), cada aparición ocurre una vez y se deja de
 * observar, y con prefers-reduced-motion no hay apariciones. El indicador de las tres
 * cucharadas es navegación, no decoración: funciona igual con movimiento reducido.
 * Mientras el lector baja se esconde, y reaparece al detenerse o al subir: así no tapa
 * el texto que se está leyendo al avanzar. Con el foco dentro no se esconde.
 * Contrato: docs/contracts/ux-transversal.yml (movimiento-accesible, firma-tres-cucharadas).
 */
(function () {
  "use strict";

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function reveal() {
    if (reduce || !("IntersectionObserver" in window)) return;
    var targets = document.querySelectorAll(
      ".archive__item, .page__content > figure, .page__content .evidence-carousel, .page__content .territorial-evidence"
    );
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.remove("motion-pending");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    var fold = window.innerHeight;
    var column = 0;
    Array.prototype.forEach.call(targets, function (element) {
      if (element.getBoundingClientRect().top < fold) return; // lo visible al cargar no se toca
      element.classList.add("motion-pending");
      element.style.setProperty("--motion-delay", (column++ % 3) * 80 + "ms");
      observer.observe(element);
    });
  }

  var SPOON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<ellipse cx="12" cy="7.5" rx="5.2" ry="6.3"/><rect x="10.9" y="13" width="2.2" height="9.5" rx="1.1"/></svg>';

  function spoonfuls() {
    var all = Array.prototype.slice.call(document.querySelectorAll(".page__content > h2[id]"));
    var heads = all.filter(function (h) { return /^(Cucharada|Spoonful) [1-3]\b/.test(h.textContent.trim()); });
    if (heads.length !== 3) return;
    var english = (document.documentElement.lang || "").indexOf("en") === 0;
    var nav = document.createElement("nav");
    nav.className = "cucharadas";
    nav.setAttribute("aria-label", english ? "Reading progress by spoonful" : "Avance de lectura por cucharada");
    heads.forEach(function (heading, index) {
      var link = document.createElement("a");
      link.className = "cucharadas__step";
      link.href = "#" + heading.id;
      link.setAttribute("aria-label", heading.textContent.trim());
      link.innerHTML = '<span class="cucharadas__spoon">' + SPOON + '</span>' +
        '<span class="cucharadas__spoon cucharadas__spoon--fill">' + SPOON + '</span>' +
        '<span class="cucharadas__n" aria-hidden="true">' + (index + 1) + '</span>';
      nav.appendChild(link);
    });
    document.body.appendChild(nav);

    var content = document.querySelector(".page__content");
    var steps = nav.children;
    var queued = false;
    function edges(index) {
      var next = all[all.indexOf(heads[index]) + 1];
      var top = heads[index].getBoundingClientRect().top + window.scrollY;
      var end = next ? next.getBoundingClientRect().top + window.scrollY
        : content.getBoundingClientRect().bottom + window.scrollY;
      return [top, end];
    }
    function update() {
      queued = false;
      var reading = window.scrollY + window.innerHeight * 0.35;
      var last = edges(2)[1];
      heads.forEach(function (_, index) {
        var span = edges(index);
        var fill = Math.min(1, Math.max(0, (reading - span[0]) / (span[1] - span[0])));
        steps[index].style.setProperty("--fill", fill.toFixed(3));
        steps[index].toggleAttribute("data-done", fill >= 1);
        if (fill > 0 && fill < 1) steps[index].setAttribute("aria-current", "step");
        else steps[index].removeAttribute("aria-current");
      });
      var inside = reading > edges(0)[0] - window.innerHeight * 0.4 && reading < last + window.innerHeight * 0.6;
      nav.classList.toggle("is-visible", inside);
    }
    function request() {
      if (!queued) { queued = true; window.requestAnimationFrame(update); }
    }
    var lastY = window.scrollY;
    var idle = null;
    function tuck() {
      var y = window.scrollY;
      if (y > lastY + 4 && !nav.contains(document.activeElement)) nav.classList.add("is-tucked");
      else if (y < lastY - 4) nav.classList.remove("is-tucked");
      lastY = y;
      window.clearTimeout(idle);
      idle = window.setTimeout(function () { nav.classList.remove("is-tucked"); }, 900);
      request();
    }
    window.addEventListener("scroll", tuck, { passive: true });
    window.addEventListener("resize", request, { passive: true });
    update();
  }

  function start() { reveal(); spoonfuls(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
}());
