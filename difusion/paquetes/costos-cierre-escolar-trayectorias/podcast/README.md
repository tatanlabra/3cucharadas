# Cápsula de audio — Extender mi tesis en 3 cucharadas (parte III)

Paquete local preparado para generar el episodio conversacional de dos voces en **NotebookLM (Audio Overview)** sobre la parte III de la serie de la tesis (`costos-cierre-escolar-trayectorias`). Este directorio se versiona en el repositorio y está excluido del build público (`_config.yml`).

| Pieza | Archivo | Estado |
|---|---|---|
| Fuente editorial autónoma para cargar en NotebookLM | `01-fuente.md` | completo y verificado |
| Texto literal para el campo de personalización de Audio Overview | `personalizacion.txt` | completo (1.248 caracteres) |
| Guion conversacional de referencia (hablantes A `es-ES` y B `es-CL`) | `guion.md` | completo (~2.950 palabras pronunciables) |
| Procedencia, parámetros y rutas de custodia | `origen.yaml` | preparado (`etapa: preparado`, pendiente máster) |
| Registro de evidencia (`EV-01` a `EV-12`) y checklist de escucha humana | `QA.md` | QA documental en verde; escucha pendiente de audio |

## Procedimiento manual para generar y publicar el audio

1. Abrir <https://notebook.google.com/> y crear un cuaderno nuevo y aislado para este episodio.
2. Cargar **únicamente** el archivo `01-fuente.md` como fuente del cuaderno.
3. En **Audio Overview**, elegir el formato **Deep Dive («Análisis en profundidad»)**, longitud **media** (*Default*, ni *Shorter* ni *Longer*), idioma **español**, y pegar íntegramente el contenido de `personalizacion.txt` en el cuadro de personalización.
4. Generar el audio, descargarlo en `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/costos-cierre-escolar-trayectorias/capsula-es-master-estereo.m4a` y verificar duración (`ffprobe`), sonoridad y fidelidad mediante escucha humana siguiendo `QA.md`.
5. Una vez aprobado por escucha humana, ensamblar con las cortinas del podcast (`source-masters/podcast-cortinas/ensamblar.py`) y completar los hashes y enlaces en `origen.yaml` y `QA.md`.
