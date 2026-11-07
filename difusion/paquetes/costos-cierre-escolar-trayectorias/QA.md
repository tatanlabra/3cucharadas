# QA — Paquete de difusión externa (`costos-cierre-escolar-trayectorias`)

- **Generado:** 2026-10-28; **actualizado y alineado con la estructura liderada por la ventana macro 2005–2024 y las pruebas de estrés del zoom 2016–2019:** 2026-11-07
- **Estado:** **Paquete local preparado y verificado** (`estado: preparado_local`; `r/PublicPolicy`, `X` y `Spotify` registrados como publicados).

---

## 1. Comprobado localmente

- [x] Paridad numérica verificada con `ruby scripts/verify_difusion_coherente.rb costos-cierre-escolar-trayectorias` y `--all-declared` (código de salida `0`).
- [x] `scripts/reddit_prefill_urls.py costos-cierre-escolar-trayectorias` genera las URLs prellenadas con código de salida `0`.
- [x] **Jerarquía narrativa actualizada en todas las piezas largas y de síntesis (`00-metadata.yaml`, `01-en-source.md`, `devto.md`, `medium.md`, `hn.txt`, `linkedin.md`, `reddit-dataisbeautiful.md`, `reddit-hilos.md`, `x.md`):**
  1. **Ventana macro de 20 años (`2005–2024`):** `1.648` cierres limpios `RCID v1` (`D2`), `1.141` cierres regulares con soporte, `78.972` trayectorias expuestas frente a `734.472` controles (`79.709.054` registros de matrícula y `73.873.835` de rendimiento en `2004–2025`), las `19` cohortes anuales estimables (`2006–2024`) con signo positivo (`+0,94` a `+28,22 pp`, mediana `+7,18 pp`), agregado de Callaway y Sant'Anna ponderado por expuestos de `+9,11 pp` (`[+5,34; +12,88]`, con cotas de Manski `[+0,43; +16,21] pp` estrictamente sobre cero), pesos iguales `+7,55 pp` (`[+5,52; +9,57]`) y efectos aleatorios `+6,29 pp` (`[+4,49; +8,09]`, `I² = 76,5 %`, intervalo de predicción `[+0,09; +12,49]`).
  2. **Cinco etapas institucionales:** concentración del `89,7 %` de los cierres (`1.023` de `1.141`) y del `86,7 %` de los expuestos (`68.496` de `78.972`) en `2005–2010` (`521` cierres, `36.984` expuestos, `+12,15 pp` `[+3,78; +20,52]`, cotas de Manski `[+3,49; +18,83]`) y `2011–2015` (`502` cierres, `31.512` expuestos, `+7,82 pp` `[+6,20; +9,41]`, pico de `+1,85 pp` en no matrícula por dos años), y atenuación posterior en `2016–2019` (`+5,29 pp`, cotas `[−1,15; +10,98] pp`), `2020–2022` (`+2,70 pp`) y `2023–2024` (`+2,59 pp`).
  3. **Zoom pre-registrado `2016–2019` (`5,5 %` de los cierres, `7,8 %` de los expuestos, `21,9` episodios efectivos en progresión) y sus tres pruebas de estrés:** (a) subconjunto con `≥ 90 %` de registros válidos en `G−1` (`1.822` expuestos, `38 %` del soporte: `+4,26 pp` y cotas de Manski `[+0,09; +7,84] pp` estrictamente sobre cero, `λ* = 1,0114`); (b) sensibilidad a pretendencias de Rambachan y Roth 2023 (placebos `+0,16`, `+0,30`, `+0,40 pp`, cota superior `0,81 pp`, margen de ruptura `2,07 pp` = `2,54` veces) y separación entre estudiantes continuos (`3.556` *stayers*: `+3,87 pp` `[+1,04; +6,69]`) y entrantes recientes (`1.033`: `+9,58 pp` `[+5,06; +14,10]`); y (c) calidad histórica previa de la escuela receptora (`ΔQ_i` en `G−1` entre `4.362` reubicados: `+2,03 pp` en `2.099` que pasan a receptores con mayor tasa de promoción vs `+5,38 pp` en `2.263` que pasan a receptores con tasa igual o menor; diferencia `−3,35 pp`).
- [x] **Regla de no duplicación cumplida:** `01-en-source.md`, `medium.md` y `devto.md` tienen estructuras y cuerpos diferenciados.
- [x] **Invariante epistémico de cotas preservado en todas las piezas con cifras:** toda mención de `+5,29` / `+5.29` aparece acompañada de sus cotas de datos faltantes de Manski (`−1,15 a 10,98 pp` / `−1.15 to 10.98 pp`) y de la calificación de resultado inconcluso en la ventana 2016–2019 global.
- [x] **Privacidad y redlines:** ninguna pieza contiene identificadores individuales (`MRUN`), códigos `RBD` específicos ni rutas locales privadas (`/home/`, `/mnt/`, `/tmp/`).
- [x] Subdirectorio `podcast/` y `social.json` preservados sin modificaciones.
- [x] Edición adversarial del 2026-11-07 (Claude Fable): la brecha de cobertura de actas estaba rotulada «−19,24 pp in the full series» en `01-en-source.md`, `devto.md` y `reddit-dataisbeautiful.md`; según la tabla 7 del post, −19,4 pp es la proporción sin ponderar y −19,24 pp la cifra con controles reponderados al pareo (la de la figura 2), no un dato de la serie larga. El contraste de calidad de la receptora (−3,35 pp) ya no se presenta como «much smaller» en `hn.txt` ni sin su salvedad en `medium.md`/`devto.md` (descriptivo, sin intervalo propio, destino elegido por las familias). El subtítulo de `medium.md` ya no dice que «cada cohorte quedó atrás» sino que la estimación puntual fue mayor en cada cohorte medible. El snippet Ruby de `devto.md` ahora reproduce la función real de `scripts/verify_thesis_post3.rb` (incluye el chequeo `represented == total`). Voz autoral en singular en `devto.md` y `medium.md`.
- [ ] Reejecutar `ruby scripts/verify_difusion_coherente.rb --all-declared` y `python3 scripts/reddit_prefill_urls.py costos-cierre-escolar-trayectorias` tras la edición del 2026-11-07: el agente no pudo lanzarlos (permiso denegado en sesión no interactiva); las marcas de paridad de arriba describen la corrida previa.

---

## 2. Pasos manuales pendientes (requieren sesión humana autorizada)

- [ ] **Aprobación editorial humana** antes de enviar las piezas externas aún no publicadas (`linkedin.md`, `medium.md`, `devto.md`, `hn.txt`, `reddit-dataisbeautiful.md`, `r/demography`, `r/econometrics`, `social.json`).
- [ ] **Importación en Medium (`medium.md`):** verificar en la interfaz de Medium que el *Canonical Link* apunte a `https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/`.
- [ ] **Reglas en vivo de `r/dataisbeautiful`, `r/demography` y `r/econometrics`:** revisar desde sesión de navegador humana antes de publicar.
