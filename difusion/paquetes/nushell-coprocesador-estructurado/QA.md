# QA — nushell-coprocesador-estructurado

Generado: 2026-09-05
Estado: aprobado para ejecutar la cadencia; el post canónico y un borrador privado de dev.to existen, pero ninguna pieza social de este paquete fue publicada.

## Comprobado

- [x] Las URLs públicas ES y EN responden 200 — evidencia: verificación posterior al pipeline GitLab #216.
- [x] Ambos canónicos son HTTPS, absolutos y autorreferentes — evidencia: HTML público descargado.
- [x] Los `hreflang` ES, EN y `x-default` son recíprocos — evidencia: HTML público, líneas de metadatos.
- [x] OG ES/EN mide 1200×630 y teaser ES/EN mide 1280×720 — evidencia: `file` y SHA-256 idéntico entre producción y repositorio.
- [x] El visor y `tesis-case.json` responden 200 — evidencia: cabeceras públicas posteriores al deploy.
- [x] Los feeds ES, EN y dev contienen el post — evidencia: `feed.xml`, `en/feed.xml` y `feed-dev-en.xml` públicos.
- [x] El post y el paquete reproducible no exponen microdatos ni identificadores — evidencia: gate `verify_structured_shell_publication.rb` y 10 pruebas del caso.
- [x] Las cifras de las piezas derivan de `01-en-source.md` y coinciden con el post — evidencia: revisión cruzada del paquete.
- [x] `devto.md` declara `published: false` y el canónico EN sin UTM — evidencia: front matter local.
- [x] El envío HN está clasificado como normal, no Show HN — evidencia: https://news.ycombinator.com/newsguidelines.html y https://news.ycombinator.com/showhn.html.
- [x] Medium conserva instrucciones para importar o fijar el canónico — evidencia: https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium.
- [x] El carrusel LinkedIn usa PDF uniforme y queda bajo 100 MB/300 páginas — evidencia: https://www.linkedin.com/help/linkedin/answer/a518909 y validación local del PDF.

## No comprobado

- Reglas actuales de r/nushell — la API pública respondió HTTP 403; requiere inspección humana de la comunidad.
- Previsualización final que dev.to genere desde `devto.md` — el borrador remoto automático aún debe reemplazarse o editarse manualmente.
- Canónico de Medium — solo puede verificarse después de importar o guardar el borrador en la cuenta humana.
- Render final del PDF dentro de LinkedIn — la plataforma solo lo muestra después de una carga manual.
- Accesibilidad interna del carrusel — el PDF es rasterizado y no etiquetado; el texto alternativo general mitiga, pero no sustituye, una versión con texto legible por tecnologías de asistencia.
- Elegibilidad y estado de las cuentas para Reddit y Hacker News — no se inspeccionaron perfiles ni credenciales.

## Decisiones de adaptación

1. Se mantuvo el resultado triple — mejora, coste e indiferencia — para no convertir evidencia acotada en una recomendación universal.
2. Medium recibe una narración autónoma; dev.to, una guía operativa; ninguno replica `01-en-source.md`.
3. HN recibe un envío normal porque el enlace es un artículo, aunque incluya un paquete reproducible.
4. Reddit queda bloqueado en vez de inferir reglas que no pudieron observarse.
5. La cadencia asigna un solo destino público por día; el borrador privado dev.to no cuenta como publicación.

## Pasos manuales pendientes

1. Verificar r/nushell y decidir si enviar o descartar.
2. Sustituir el cuerpo del borrador dev.to 4584688 por `devto.md`, revisar y publicar recién en su fecha.
3. Importar o pegar `medium.md`, fijar el canónico y revisar el borrador.
4. Subir el PDF de LinkedIn, agregar título y texto alternativo, revisar todas las láminas y publicar.
5. Registrar URL, fecha y resultado de cada envío en `_data/distribucion.yml` y en el ledger local.
