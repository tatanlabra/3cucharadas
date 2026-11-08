# Cápsula de audio — Extender mi tesis en 3 cucharadas (parte III)

Paquete local para el episodio conversacional de dos voces en **NotebookLM (Audio Overview)** sobre la parte III de la serie de la tesis (`costos-cierre-escolar-trayectorias`). Este directorio se versiona en el repositorio y está excluido del build público (`_config.yml`).

| Pieza | Archivo | Estado |
|---|---|---|
| Fuente editorial autónoma sincronizada con la narrativa 2005–2024 (etapas institucionales primero, zoom 2016–2019 y verificaciones M1–M3 después) | `01-fuente.md` | completo; cifras contrastadas con el post (7 de noviembre de 2026) |
| Texto literal para el campo de personalización de Audio Overview | `personalizacion.txt` | completo; bajo el tope de cuatrocientos noventa caracteres |
| Guion conversacional de referencia (hablantes A `es-ES` y B `es-CL`) | `guion.md` | publicado; congelado (no se edita: es el insumo del audio ya emitido) |
| Guion breve centrado en el efecto global 2005–2024, insumo real del episodio publicado | `guion-breve.md` + `guion-breve-QA.md` | publicado; guion congelado, QA con divergencias respecto del post actualizado |
| Procedencia, parámetros, rutas de custodia y enlaces publicados | `origen.yaml` | publicado en Spotify y Apple Podcasts; congelado |
| Registro de evidencia y lista de verificación | `QA.md` | QA documental cerrada; divergencias audio/post registradas |

## Procedimiento manual para generar y publicar el audio

El episodio ya está publicado (1 de noviembre de 2026). Los pasos siguientes aplican solo si se decide regenerar la cápsula con la fuente actualizada.

1. Abrir <https://notebook.google.com/> y crear un cuaderno nuevo y aislado para este episodio.
2. Cargar **únicamente** el archivo `01-fuente.md` como fuente del cuaderno.
3. En **Audio Overview**, elegir el formato **Deep Dive («Análisis en profundidad»)**, longitud **media** (*Default*, ni *Shorter* ni *Longer*), idioma **español**, y pegar íntegramente el contenido de `personalizacion.txt` en el cuadro de personalización.
4. Generar el audio, descargarlo en `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/costos-cierre-escolar-trayectorias/capsula-es-master-estereo.m4a` y verificar duración (`ffprobe`), sonoridad y fidelidad mediante escucha humana siguiendo `QA.md`.
5. Una vez aprobado por escucha humana, ensamblar con las cortinas del podcast (`source-masters/podcast-cortinas/ensamblar.py`) y registrar los hashes y enlaces en `origen.yaml` y `QA.md`.
