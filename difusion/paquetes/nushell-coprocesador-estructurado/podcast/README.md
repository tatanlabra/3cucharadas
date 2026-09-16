# Cápsula de audio — Nushell como coprocesador estructurado

Episodio conversacional de dos voces generado con NotebookLM a partir del post publicado. Este
directorio se versiona y **no** se publica (`difusion/` está en `exclude:` de `_config.yml`).

| Pieza | Archivo | Estado |
|---|---|---|
| Procedencia, hashes y comando de re-encode | `origen.yaml` | completo |
| Registro de escucha y QA | `QA.md` | **pendiente de escucha humana** |
| Fuente editorial cargada en el cuaderno | — | no recuperada: el episodio se generó antes de existir este paquete |
| Texto de personalización de Audio Overview | — | ídem |
| Guion A/B | — | ídem; NotebookLM no entrega guion, y el planeado no es transcripción del audio |
| Máster estéreo descargado | fuera del repo, ver `origen.yaml` | conservado |
| Audio publicado | retirado del repositorio el 2026-09-15 | se distribuye por Spotify y Apple; ver `origen.yaml` |
| Transcripción | — | **no existe**; el bloque del post lo declara |

## Lo que este episodio no tiene, y por qué

Se generó antes de que existiera el flujo, con el prompt que ahora vive aquí como `prompt-usado.md`.
Estaba suelto en `~/Descargas` y este paquete lo citaba desde fuera del repositorio: una limpieza
rutinaria de esa carpeta habría destruido la única procedencia editorial que sobrevive del episodio.
Los tres artefactos que la plantilla sucesora sí exige —fuente, personalización y guion— no se
conservaron. Para el próximo episodio se usa
`penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md`, que los pide.

## Si se regenera el audio

Se sube el episodio nuevo a Spotify for Creators y se actualizan las dos URL en `audio.plataformas`
del post y en `_data/distribucion.yml`. No hay caché de borde que purgar: el sitio no sirve el
archivo desde el 2026-09-15, y la duración en el nombre —que existía para estrenar ruta y evitar esa
purga— dejó de tener función.
