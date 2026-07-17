/* Inyectar MAPTILER_PUBLIC_KEY en el despliegue; nunca versionar una llave real. */
window.CATASTRO_MAP_CONFIG = {
  maptilerKey: "",
  maplibreScript: "",
  maplibreCss: "",
  styleUrl: "https://api.maptiler.com/maps/dataviz-dark/style.json?key={key}"
};
