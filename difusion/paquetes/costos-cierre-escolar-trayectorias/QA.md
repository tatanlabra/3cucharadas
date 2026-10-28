# QA — Paquete de difusión externa (`costos-cierre-escolar-trayectorias`)

- **Generado:** 2026-10-28
- **Estado:** **Paquete local preparado y verificado** (`estado: preparado_local`). Ningún envío externo ha sido ejecutado; `distribution.social` permanece en `false` en el front matter del post canónico hasta revisión editorial humana.

---

## 1. Comprobado localmente

- [x] Los posts canónicos ES (`_posts/2026-10-23-costos-cierre-escolar-trayectorias.md`) y EN (`_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md`) pasan `ruby scripts/verify_thesis_post3.rb` (`POST3_VALID`) y las 278 aserciones de `tests/test_verify_thesis_post3.rb`.
- [x] El sitio compilado pasa `node scripts/verify_thesis_post3_browser.mjs` en Chromium a través de los 4 viewports (`320`, `390`, `768` y `1440 px`) y los dos temas (`light` y `academic-night`), con `live: 0`, `no_js: 0`, `print: 0`, `text_resize_200: 0`, `preferences: 0`, `asset_hash_mismatches: 0` y `artifact_not_bound: false`.
- [x] **Regla de no duplicación cumplida:** `01-en-source.md` (transcreación maestra completa), `medium.md` (ensayo narrativo autónomo para público general) y `devto.md` (artículo técnico centrado en SQL/DuckDB, Ruby gate y econometría de diferencias en diferencias escalonadas) tienen estructuras y cuerpos diferenciados.
- [x] **Invariante epistémico de cotas preservado en todas las piezas con cifras:** toda mención de `+5,29` / `+5.29` aparece acompañada de sus cotas de datos faltantes de Manski (`−1,15 a 10,98 pp` / `−1.15 to 10.98 pp`) y de la calificación de resultado inconcluso en la ventana principal 2016–2019.
- [x] **Paridad exacta con el artefacto gobernado de serie completa (`post3_full_series_did_2004_2025_v1.json`):** todas las piezas reportan los 5 regímenes institucionales (`+12,15`, `+7,82`, `+5,29`, `+2,70` y `+2,59 pp`), los 1.141 episodios con soporte (`78.972` expuestos y `734.472` controles) y los 3 agregados (`+9,11 pp` Callaway y Sant'Anna con cotas `[+0,43; +16,21] pp`, `+7,55 pp` pesos iguales y `+5,14 pp` varianza inversa con `I² = 76,48 %`).
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
