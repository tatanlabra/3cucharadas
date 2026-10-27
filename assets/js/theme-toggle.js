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
      var stored = window.localStorage.getItem(STORAGE_KEY);
      // Sin elección guardada manda lo que resolvió head.html (incluido el tema del sistema).
      return stored === null ? normalizeTheme(root.getAttribute("data-theme")) : normalizeTheme(stored);
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
      themeColor.setAttribute("content", theme === DARK_THEME ? "#161616" : "#faf7f0");
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

  function updatePost3Visuals(theme) {
    var isDark = theme === DARK_THEME;
    var variant = isDark ? "dark" : "light";
    var images = document.querySelectorAll(".post3-theme-image");
    var sources = document.querySelectorAll(".post3-theme-source");
    var links = document.querySelectorAll(".post3-theme-link");

    Array.prototype.forEach.call(sources, function (source) {
      var sourceSet = source.dataset[variant + "Srcset"];
      if (sourceSet) {
        source.setAttribute("srcset", sourceSet);
      }
    });

    Array.prototype.forEach.call(images, function (image) {
      var source = image.dataset[variant + "Src"];
      var sourceSet = image.dataset[variant + "Srcset"];
      if (source) {
        image.setAttribute("src", source);
      }
      if (sourceSet) {
        image.setAttribute("srcset", sourceSet);
      }
    });

    Array.prototype.forEach.call(links, function (link) {
      var target = link.dataset[variant + "Href"];
      if (target) {
        link.setAttribute("href", target);
      }
    });
  }

  function applyTheme(value) {
    var theme = normalizeTheme(value);
    root.setAttribute("data-theme", theme);
    root.style.colorScheme = theme === DARK_THEME ? "dark" : "light";
    updateThemeColor(theme);
    updateButtons(theme);
    updatePost3Visuals(theme);
    return theme;
  }

  function toggleTheme() {
    var currentTheme = normalizeTheme(root.getAttribute("data-theme"));
    var nextTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    applyTheme(nextTheme);
    storeTheme(nextTheme);
  }

  function initializeThemeToggle() {
    applyTheme(readStoredTheme());

    // Solo se migra el valor heredado; el tema del sistema no se persiste como elección.
    try {
      if (window.localStorage.getItem(STORAGE_KEY) === LEGACY_DARK_THEME) {
        storeTheme(DARK_THEME);
      }
    } catch (error) {
      // Sin almacenamiento no hay nada que migrar.
    }

    var buttons = document.querySelectorAll("[data-theme-toggle]");
    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener("click", toggleTheme);
    });

    // Las láminas oscuras pierden contraste sobre el papel blanco. La vista
    // impresa usa temporalmente el arte claro y luego restaura el tema elegido.
    window.addEventListener("beforeprint", function () {
      updatePost3Visuals(LIGHT_THEME);
    });
    window.addEventListener("afterprint", function () {
      updatePost3Visuals(normalizeTheme(root.getAttribute("data-theme")));
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
