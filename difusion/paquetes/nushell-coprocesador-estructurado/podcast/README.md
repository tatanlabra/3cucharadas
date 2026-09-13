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
| Audio publicado (mono 64 kbps) | `../../../../assets/audio/nushell-coprocesador-estructurado/capsula-es-989s.mp4` | en el repo, declarado en `docs/contracts/repo-governance.yaml` |
| Transcripción | — | **no existe**; el bloque del post lo declara |

## Lo que este episodio no tiene, y por qué

Se generó con `~/Descargas/prompt_capsula_3cucharadas.md` antes de que existiera el flujo. Los tres
artefactos editoriales que la plantilla sucesora sí exige —fuente, personalización y guion— no se
conservaron. Para el próximo episodio se usa
`penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md`, que los pide.

## Si se regenera el audio

El nombre del archivo publicado lleva la duración (`-989s`). Un episodio nuevo con otra duración
estrena ruta y no necesita purga de la caché de Cloudflare. Un reemplazo que conserve exactamente
la misma duración **sí** la necesita: `scripts/purge_cloudflare_cache.sh --changed`, y solo después
de que el pipeline esté en `success`.
