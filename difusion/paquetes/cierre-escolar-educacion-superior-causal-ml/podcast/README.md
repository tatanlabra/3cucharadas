# Cápsula de audio — Extender mi tesis en 3 cucharadas (parte IV)

Paquete local preparado para generar el episodio conversacional de dos voces en **NotebookLM (Audio Overview)** sobre la parte IV y cierre de la serie de la tesis (`cierre-escolar-educacion-superior-causal-ml`). Este directorio se versiona en el repositorio y está excluido del build público (`_config.yml`).

| Pieza | Archivo | Estado |
|---|---|---|
| Fuente editorial autónoma en prosa para cargar en NotebookLM | `01-fuente.md` | completo; cifras contrastadas con el post (7 de noviembre de 2026) |
| Texto literal para el campo de personalización de Audio Overview (ambas voces en español de Chile) | `personalizacion.txt` | completo; bajo el tope de cuatrocientos noventa caracteres |
| Guion conversacional de referencia (dos voces `A` y `B`, unos veinte minutos) | `guion.md` | completo; revisión editorial del 7 de noviembre de 2026 |
| Guion breve de cinco minutos con verificación de cifras | `guion-breve.md` + `guion-breve-QA.md` | completo; entre seiscientas cincuenta y ochocientas cincuenta palabras |
| Procedencia, parámetros y rutas de custodia | `origen.yaml` | preparado (`etapa: preparado`, pendiente máster) |
| Registro de evidencia (`EV-01` a `EV-13`) y lista de verificación de escucha humana | `QA.md` | QA documental cerrada; escucha pendiente de audio |

## Procedimiento manual para generar y publicar el audio

1. Abrir <https://notebook.google.com/> y crear un cuaderno nuevo y aislado para este episodio.
2. Cargar **únicamente** el archivo `01-fuente.md` (o `guion-breve.md` si se busca una cápsula compacta) como fuente del cuaderno.
3. En **Audio Overview**, elegir el formato **Deep Dive («Análisis en profundidad»)**, longitud **media** (*Default*, ni *Shorter* ni *Longer*), idioma **español**, y pegar íntegramente el contenido de `personalizacion.txt` en el cuadro de personalización.
4. Generar el audio, descargarlo en `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/cierre-escolar-educacion-superior-causal-ml/capsula-es-master-estereo.m4a` y verificar duración (`ffprobe`), sonoridad y fidelidad mediante escucha humana siguiendo `QA.md`.
5. Una vez aprobado por escucha humana, ensamblar con las cortinas del podcast (`source-masters/podcast-cortinas/ensamblar.py`) o nivelar en Audacity a menos dieciséis LUFS, subir a Spotify for Creators (que distribuye por RSS a Apple Podcasts) y completar los hashes y enlaces en `origen.yaml` y `QA.md`.
