(function () {
  "use strict";

  var STORAGE_KEY = "3cucharadas-theme";
  var LIGHT_THEME = "light";
  var DARK_THEME = "academic-night";
  var LEGACY_DARK_THEME = "tokyo-night";
  var root = document.documentElement;

  function normalizeTheme(value) {
    return value === DARK_THEME || value === LEGACY_DARK_THEME ? DARK_THEME : LIGHT_THEME;
  }

  function readStoredTheme() {
    try {
      return normalizeTheme(window.localStorage.getItem(STORAGE_KEY));
    } catch (error) {
      return normalizeTheme(root.getAttribute("data-theme"));
    }
  }

  function storeTheme(theme) {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (error) {
      // El cambio funciona durante la sesión aunque no pueda persistirse.
    }
  }

  function updateThemeColor(theme) {
    var themeColor = document.querySelector("meta[data-theme-color]");
    if (themeColor) {
      themeColor.setAttribute("content", theme === DARK_THEME ? "#161616" : "#ffffff");
    }
  }

  function updateButtons(theme) {
    var isDark = theme === DARK_THEME;
    var buttons = document.querySelectorAll("[data-theme-toggle]");

    Array.prototype.forEach.call(buttons, function (button) {
      var label = isDark ? button.dataset.themeLightLabel : button.dataset.themeDarkLabel;
      button.setAttribute("aria-pressed", String(isDark));
      if (label) {
        button.setAttribute("aria-label", label);
        button.setAttribute("title", label);
      }
    });
  }

  function applyTheme(value) {
    var theme = normalizeTheme(value);
    root.setAttribute("data-theme", theme);
    root.style.colorScheme = theme === DARK_THEME ? "dark" : "light";
    updateThemeColor(theme);
    updateButtons(theme);
    return theme;
  }

  function toggleTheme() {
    var currentTheme = normalizeTheme(root.getAttribute("data-theme"));
    var nextTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    applyTheme(nextTheme);
    storeTheme(nextTheme);
  }

  function initializeThemeToggle() {
    var theme = applyTheme(readStoredTheme());

    if (theme === DARK_THEME) {
      storeTheme(theme);
    }

    var buttons = document.querySelectorAll("[data-theme-toggle]");
    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener("click", toggleTheme);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeThemeToggle);
  } else {
    initializeThemeToggle();
  }

  window.addEventListener("storage", function (event) {
    if (event.key === STORAGE_KEY) {
      applyTheme(event.newValue);
    }
  });
}());
