(() => {
  "use strict";

  const root = document.documentElement;
  const storageKey = "catastro-brecha-theme";
  const button = document.getElementById("theme-toggle");

  function setTheme(theme, persist = true) {
    root.dataset.theme = theme;
    const dark = theme === "dark";
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (button) {
      button.setAttribute("aria-pressed", String(dark));
      button.setAttribute("aria-label", dark ? "Activar apariencia clara" : "Activar apariencia oscura");
      button.title = dark ? "Activar apariencia clara" : "Activar apariencia oscura";
    }
    if (themeColor) themeColor.content = dark ? "#07070c" : "#e9edf4";
    if (persist) {
      try { localStorage.setItem(storageKey, theme); } catch (_) { /* El visor también funciona sin almacenamiento. */ }
    }
    window.dispatchEvent(new CustomEvent("catastro:theme", { detail: { theme } }));
  }

  setTheme(root.dataset.theme === "light" ? "light" : "dark", false);
  if (button) button.addEventListener("click", () => setTheme(root.dataset.theme === "dark" ? "light" : "dark"));

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveal = [...document.querySelectorAll(".reveal")];
  if (reducedMotion || !("IntersectionObserver" in window)) {
    reveal.forEach((element) => element.classList.add("in"));
    return;
  }

  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("in");
      currentObserver.unobserve(entry.target);
    });
  }, { threshold: 0.1 });
  reveal.forEach((element) => observer.observe(element));
})();
