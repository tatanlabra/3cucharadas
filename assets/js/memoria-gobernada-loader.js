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
