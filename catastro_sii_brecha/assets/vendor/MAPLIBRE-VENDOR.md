# MapLibre GL JS local

El visor sólo activa MapLibre cuando el artefacto de despliegue contiene una copia
local fijada de `maplibre-gl.js` y, si corresponde, su CSS. La descarga queda fuera de
este repositorio hasta verificar versión y SHA-256; después CI puede inyectar la ruta
local mediante `scripts/inject_maptiler_key.py` sin versionar `MAPTILER_PUBLIC_KEY`.
