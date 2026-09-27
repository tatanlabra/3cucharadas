(function () {
  "use strict";

  function initializeCarousel(root) {
    var viewport = root.querySelector("[data-carousel-viewport]");
    var slides = Array.prototype.slice.call(root.querySelectorAll("[data-carousel-slide]"));
    var previous = root.querySelector("[data-carousel-previous]");
    var next = root.querySelector("[data-carousel-next]");
    var dots = Array.prototype.slice.call(root.querySelectorAll("[data-carousel-dot]"));
    var status = root.querySelector("[data-carousel-status]");
    var current = 0;
    var scrollFrame = null;

    if (!viewport || slides.length === 0 || !previous || !next) return;

    root.classList.add("is-enhanced");

    function statusText(index) {
      return root
        .getAttribute("data-status-template")
        .replace("%current%", String(index + 1))
        .replace("%total%", String(slides.length));
    }

    function update(index) {
      current = Math.max(0, Math.min(index, slides.length - 1));
      previous.disabled = current === 0;
      next.disabled = current === slides.length - 1;
      if (status) status.textContent = statusText(current);
      dots.forEach(function (dot, dotIndex) {
        if (dotIndex === current) dot.setAttribute("aria-current", "true");
        else dot.removeAttribute("aria-current");
      });
    }

    function targetLeft(index) {
      return slides[index].offsetLeft - slides[0].offsetLeft;
    }

    function goTo(index) {
      var bounded = Math.max(0, Math.min(index, slides.length - 1));
      viewport.scrollTo({
        left: targetLeft(bounded),
        behavior: "auto"
      });
      update(bounded);
    }

    function closestSlide() {
      var left = viewport.scrollLeft;
      var best = 0;
      var distance = Infinity;
      slides.forEach(function (_slide, index) {
        var candidate = Math.abs(targetLeft(index) - left);
        if (candidate < distance) {
          best = index;
          distance = candidate;
        }
      });
      update(best);
    }

    previous.addEventListener("click", function () {
      goTo(current - 1);
    });
    next.addEventListener("click", function () {
      goTo(current + 1);
    });
    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        goTo(index);
      });
    });
    viewport.addEventListener("keydown", function (event) {
      var destinations = {
        ArrowLeft: current - 1,
        ArrowRight: current + 1,
        Home: 0,
        End: slides.length - 1
      };
      if (!Object.prototype.hasOwnProperty.call(destinations, event.key)) return;
      event.preventDefault();
      goTo(destinations[event.key]);
    });
    viewport.addEventListener(
      "scroll",
      function () {
        if (scrollFrame !== null) window.cancelAnimationFrame(scrollFrame);
        scrollFrame = window.requestAnimationFrame(closestSlide);
      },
      { passive: true }
    );
    if ("ResizeObserver" in window) {
      new ResizeObserver(function () {
        viewport.scrollLeft = targetLeft(current);
      }).observe(viewport);
    }
    update(0);
  }

  function initializeAll() {
    document.querySelectorAll("[data-evidence-carousel]").forEach(initializeCarousel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeAll);
  } else {
    initializeAll();
  }
})();
