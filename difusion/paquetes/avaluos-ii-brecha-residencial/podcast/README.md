# Cápsula de audio — Avalúos II, brecha residencial

Episodio conversacional de dos voces generado con NotebookLM a partir del post publicado, titulado
en origen «Las casas que le faltan al SII». Este directorio se versiona y **no** se publica
(`difusion/` está en `exclude:` de `_config.yml`).

| Pieza | Archivo | Estado |
|---|---|---|
| Procedencia, hashes y coherencia con la revisión del post | `origen.yaml` | completo |
| Registro de escucha y QA | `QA.md` | escuchado y aprobado por la persona usuaria |
| Fuente editorial, personalización y guion | — | no conservados: el episodio se generó antes de que la plantilla los exigiera |
| Máster estéreo | fuera del repo, ver `origen.yaml` | conservado |
| Audio publicado (mono 64 kbps) | `../../../../assets/audio/avaluos-ii-brecha-residencial/capsula-es-1616s.mp4` | en el repo, declarado en `docs/contracts/repo-governance.yaml` |
| Transcripción | — | **no existe**; el bloque del post lo declara |

## Este episodio movió la ventana de duración

Dura **1616 s (26:56)**, fuera del máximo de 1200 s que la plantilla fijó con el primer episodio.
No se recortó: la propia plantilla manda revisar la ventana con la medición nueva en vez de forzar
el audio. Con n=2 —989 s y 1616 s— la ventana pasa a **600–1800 s**, y así queda escrito en
`penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md` y en
`docs/flujo-podcast.md`. Sigue siendo una ventana con dos observaciones: el tercer episodio puede
volver a moverla.

## Si se regenera el audio

El nombre lleva la duración (`-1616s`). Un episodio nuevo con otra duración estrena ruta y no
necesita purga de Cloudflare. Un reemplazo que conserve la duración exacta **sí** la necesita:
`scripts/purge_cloudflare_cache.sh --changed`, después de que el pipeline esté en `success`.
