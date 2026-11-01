# QA — Paquete de difusión externa (`costos-cierre-escolar-trayectorias`)

- **Generado:** 2026-10-28; **revisado tras la auditoría:** 2026-10-31 (ver la sección de correcciones al final de la sección 1)
- **Estado:** **Paquete local preparado y verificado** (`estado: preparado_local`). Ningún envío externo ha sido ejecutado; `distribution.social` permanece en `false` en el front matter del post canónico hasta revisión editorial humana.

---

## 1. Comprobado localmente

- [x] Los posts canónicos ES (`_posts/2026-10-23-costos-cierre-escolar-trayectorias.md`) y EN (`_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md`) pasan `ruby scripts/verify_thesis_post3.rb` (`POST3_VALID`) y las 306 aserciones de `tests/test_verify_thesis_post3.rb` (corrida del 2026-10-31, tras agregar las fixtures de efectos aleatorios y apéndice; la del 28 de octubre registraba 278).
- [x] El sitio compilado pasa `node scripts/verify_thesis_post3_browser.mjs` en Chromium a través de los 4 viewports (`320`, `390`, `768` y `1440 px`) y los dos temas (`light` y `academic-night`), con `live: 0`, `no_js: 0`, `print: 0`, `text_resize_200: 0`, `preferences: 0`, `asset_hash_mismatches: 0` y `artifact_not_bound: false`.
- [x] **Regla de no duplicación cumplida:** `01-en-source.md` (transcreación maestra completa), `medium.md` (ensayo narrativo autónomo para público general) y `devto.md` (artículo técnico centrado en SQL/DuckDB, Ruby gate y econometría de diferencias en diferencias escalonadas) tienen estructuras y cuerpos diferenciados.
- [x] **Invariante epistémico de cotas preservado en todas las piezas con cifras:** toda mención de `+5,29` / `+5.29` aparece acompañada de sus cotas de datos faltantes de Manski (`−1,15 a 10,98 pp` / `−1.15 to 10.98 pp`) y de la calificación de resultado inconcluso en la ventana principal 2016–2019.
- [x] **Paridad exacta con el artefacto gobernado de serie completa (`post3_full_series_did_2004_2025_v1.json`):** todas las piezas reportan los 5 regímenes institucionales (`+12,15`, `+7,82`, `+5,29`, `+2,70` y `+2,59 pp`), los 1.141 episodios con soporte (`78.972` expuestos y `734.472` controles) y los 3 agregados (`+9,11 pp` Callaway y Sant'Anna con cotas `[+0,43; +16,21] pp`, `+7,55 pp` pesos iguales y `+6,29 pp` con efectos aleatorios, `I² = 76,5 %` e intervalo de predicción `[+0,09; +12,49]`, leídos de `post3_audit_light_v1.json`).
- [x] **Corrección del 2026-10-31:** el agregado de varianza inversa (`+5,14 pp`) se retiró por falsa precisión; la regla `RCID v1` usa ≥ 10 estudiantes, ≥ 70 % a un destino y HHI ≥ 0,50; la pretendencia `−1,49` se retiró por no tener fuente. Coherencia numérica revalidada con `verify_difusion_coherente.rb`.
- [x] **Privacidad y redlines:** ninguna pieza contiene identificadores individuales (`MRUN`), códigos `RBD` específicos ni rutas locales privadas (`/home/`, `/mnt/`, `/tmp/`).
- [x] `social.json` cumple los límites de longitud de Bluesky (≤ 300 caracteres: 282 ES / 273 EN) y Mastodon (≤ 500 caracteres contando URL), sin cifras sueltas sin denominador y sin frases causales prohibidas.
- [x] `devto.md` declara `published: false` y `canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/`.

---

## 2. No comprobado aún (requiere acción humana o etapa de publicación externa autorizada)

- [ ] **Aprobación editorial humana** del paquete de difusión y del audio generado en NotebookLM.
- [ ] **Importación en Medium (`medium.md`):** verificar en la interfaz de Medium que el *Canonical Link* apunte a `https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/`.
- [ ] **Borrador en dev.to (`devto.md`):** crear o actualizar cuando el autor habilite la distribución externa.
- [ ] **Reglas en vivo de `r/dataisbeautiful` (`reddit-dataisbeautiful.md`):** revisar desde sesión de navegador humana antes de publicar el gráfico `[OC]`.
- [ ] **Envío a Mastodon y Bluesky (`social.json`):** requiere aprobación humana en el flujo de `3cucharadas-site`.

## Reddit (2026-11-01)

Investigación de solo lectura, sin publicar. La API pública de Reddit respondió 403 en los 17 subs
probados y la lectura automática está bloqueada: **ninguna regla oficial quedó verificada**. Los
tamaños son de GummySearch (2026-11-01). Copys en `reddit-hilos.md`.

| Orden | Sub | Tamaño | Tipo de envío | Riesgo principal |
|---|---|---|---|---|
| ES 1 | r/chile | ~921 mil | enlace, con flair "Análisis de Actualidad" o "Cultura / Sociedad" | autopromoción (no verificado) |
| ES 2 | r/RepublicadeChile | ~128 mil | enlace o texto, con flair "Debate & Opinión" | autopromoción (no verificado) |
| EN 1 | r/dataisbeautiful | ~21,8 millones | imagen [OC] (`assets/images/tesis-post3/cohort-series-infographic-en-light.png`) y comentario de fuente | quitan el post si falta el comentario de fuente o si el título exagera |
| EN 2 | r/econometrics | ~46 mil | texto que pide crítica del diseño | autopromoción (no verificado) |
| EN 3 | r/education | ~247 mil | enlace | audiencia mayoritariamente de EE. UU. |

Descartados: r/AskEconomics (solo preguntas), r/statistics (tema periférico), r/CausalInference
(~2 mil) y r/Universidad (no encontrado). En reserva: r/Santiago, r/latinoamerica y r/publicpolicy.

### Reorientación (2026-11-01, decisión del autor)

Solo subs en inglés de datos, política pública y cambio demográfico; r/chile y r/RepublicadeChile
quedan fuera porque su temática no es pertinente.

| Orden | Sub | Evidencia de existencia y tamaño | Riesgo principal |
|---|---|---|---|
| 1 | r/dataisbeautiful | ~21,8 millones (GummySearch) | quitan el post si falta el comentario de fuente o si el título exagera |
| 2 | r/demography | espejos públicos: "a community for all those who want to discuss and share topics associated with demography and demographic change"; activo, con gráficos de fecundidad de 2025–2026; tamaño no verificado | reglas sobre enlaces propios no verificadas |
| 3 | r/PublicPolicy | ~23 mil (GummySearch, caché de 2026-06-20; el servicio cerró y la cifra puede estar desactualizada) | autopromoción no verificada |
| reserva | r/econometrics | ~46 mil (GummySearch) | autopromoción no verificada |

Segundo intento (mismo día): con un navegador headless (agent-browser, Chrome), old.reddit.com y www.reddit.com responden "You've been blocked by network security". No se intentó evadir el bloqueo: las reglas solo pueden leerse desde una sesión humana.
