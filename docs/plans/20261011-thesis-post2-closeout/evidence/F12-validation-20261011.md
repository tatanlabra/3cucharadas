# F12 — suites, build, artefacto, visual y accesibilidad

- Fecha: `2026-10-11`.
- Alcance: Post II ES/EN, anexo geográfico, bundle cartográfico y dependencias de build del sitio.
- Resultado: verde después de falsación y reparaciones; no concede publicación.

| Gate | Resultado final |
|---|---|
| Freeze científico | 17 pruebas, validación y Ruff `exit 0`; hash `b471c02`, 58 artefactos, 15 claims |
| Auditoría MINEDUC–OSM | 22 pruebas, cinco probes `exit 2` esperado, validación pública y Ruff `exit 0` |
| Source health | todos los checks `PASS`, `exit 0` |
| TypeScript/Vitest/Vite | Catastro 136 pruebas; memoria gobernada 3 pruebas; checks y tres builds `exit 0` |
| Jekyll | build de producción `exit 0`; avisos Sass deprecados no bloqueantes |
| Artefacto | `70.913.596` bytes, `1.521` entradas, `exit 0` |
| Matriz Playwright | 24/24 páginas, 12/12 SVG vigentes, 2/2 fallbacks; cero fallos |
| Axe 4.12.1 ES | 26 reglas aprobadas, 0 violaciones, 0 inconclusos |
| Axe 4.12.1 EN | 26 reglas aprobadas, 0 violaciones, 0 inconclusos |

## Rojos observados y reparación

- El test del freeze rechazó una observación Git obsoleta después de cambiar `HEAD`; el snapshot se regeneró contra `5caf912` sin introducir autorreferencia.
- El primer preview dentro del sandbox no pudo abrir un socket local (`Errno::EPERM`); la misma suite fuera del sandbox alcanzó el navegador.
- El visor agotó 35 segundos esperando un estilo remoto; se añadió timeout de 3 segundos y fallback cartográfico.
- Las 24 combinaciones detectaron `market-map-case-switch-broken` porque una comparación interna conservaba Rancagua y La Reina; se desplazó a Lo Barnechea y Lo Prado.
- La inspección de screenshots reveló que el inventario SVG seguía auditando los mapas históricos; se desplazó el gate a los SVG vigentes y la matriz completa volvió a verde.
- Axe encontró contraste de `1,07:1` en la tabla del recuadro y `3,06:1` en enlaces; CSS acotado al componente produjo 0 violaciones y 0 inconclusos en ES y EN.

## Evidencia contraria y límites

- El cuerpo visible supera la meta blanda: 3.237 palabras ES y 3.110 EN en el render; no es un gate duro y el canario acredita que no se ocultó.
- El bundle principal del mapa es de aproximadamente 985 kB sin comprimir; Vite emite una advertencia no bloqueante de chunk mayor a 500 kB.
- El basemap remoto puede degradar a OSM raster o lámina estática; las dos rutas de fallback fueron verificadas.
