(function () {
  "use strict";

  var host = document.getElementById("memory-observatory");
  if (!host) return;
  var isEnglish = document.documentElement.lang.toLowerCase().indexOf("en") === 0;
  var fallbackStart = isEnglish
    ? "The narrative and table remain available; the 3D view could not start."
    : "El relato y la tabla siguen disponibles; no fue posible iniciar la vista 3D.";
  var fallbackLoad = isEnglish
    ? "The narrative and table remain available; the 3D view could not load."
    : "El relato y la tabla siguen disponibles; no fue posible cargar la vista 3D.";

  function fallback(message) {
    host.dataset.state = "fallback";
    var status = document.getElementById("memory-observatory-status");
    if (status) status.textContent = message;
  }

  fetch("/assets/dist/memoria_gobernada/manifest.json", { credentials: "same-origin" })
    .then(function (response) {
      if (!response.ok) throw new Error("manifest unavailable");
      return response.json();
    })
    .then(function (manifest) {
      var keys = Object.keys(manifest);
      var entry = keys.map(function (key) { return manifest[key]; }).find(function (item) { return item && item.isEntry; });
      if (!entry || !entry.file) throw new Error("entry unavailable");
      // La hoja de estilos va en un campo aparte del manifiesto de Vite
      // (`entry.css`), no en `entry.file`. Inyectarla explicitamente: sin esto
      // el modulo arranca y dibuja, pero la pagina se queda sin las reglas de
      // .memory-observatory y .rag-knowledge-graph, y el iframe colapsa a su
      // alto por defecto. Medido el 2026-08-31: 154 px en vez de 704 px.
      (entry.css || []).forEach(function (href) {
        if (document.querySelector('link[data-memoria-gobernada="' + href + '"]')) return;
        var link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "/assets/dist/memoria_gobernada/" + href;
        link.setAttribute("data-memoria-gobernada", href);
        document.head.appendChild(link);
      });
      var script = document.createElement("script");
      script.type = "module";
      script.src = "/assets/dist/memoria_gobernada/" + entry.file;
      script.onerror = function () { fallback(fallbackStart); };
      document.head.appendChild(script);
    })
    .catch(function () {
      fallback(fallbackLoad);
    });
}());
