# MapLibre GL JS local

MapLibre GL JS y PMTiles se empaquetan con Vite desde versiones exactas de
`package-lock.json`. El cargador estable `assets/map-app-loader.js` resuelve el
manifest Vite y carga los activos hasheados sólo al acercarse al visor. No se inyectan
claves ni se depende de MapTiler u otro proveedor de teselas externo.
