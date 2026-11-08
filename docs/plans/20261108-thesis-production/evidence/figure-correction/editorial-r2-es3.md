# Corrección editorial r2 — Anexo III ES

Estado: corrección de fuente completada; QA de navegador pendiente del próximo build congelado.

## Hallazgo y cambio

- Claude B8: el anexo ES saltaba de «Serie, sensibilidad y receptoras» a la tabla A4; faltaban método escalonado, universo de 20 cohortes, estimabilidad 19/17 y cuatro lecturas con cautelas presentes en EN.
- `_pages/tesis-post3-anexo-metodologico.md:94–96`: agregado cálculo de contrastes por cohorte y posterior agregación, 20/19/17 cohortes, soporte D2 y referencias Callaway–Sant’Anna, Sun–Abraham y Roth como marco metodológico. Las tres notas bibliográficas se definen en la misma página (`:253`, `:273`, `:277`), con las mismas claves y entradas que el artículo III.
- La primera redacción atribuía controles «que todavía no cerraban». Se retiró después de inspeccionar `incubadora/tesis_mae_mejorada/research/post3/agy_full_series_v1/compute_full_series_2004_2025.py:432–433`, donde se excluyen estudiantes expuestos alguna vez y escuelas del conjunto de cierres. El anexo ya no atribuye al productor una familia de controles ni un estimador específico sin prueba de implementación.
- `_pages/tesis-post3-anexo-metodologico.md:110`: la fila de +9,11 pp ahora dice «ponderado por expuestos»; conserva cifras y deja Callaway–Sant’Anna como referencia metodológica, sin afirmar que el cálculo reproduzca su estimador exacto.
- `_pages/tesis-post3-anexo-metodologico.md:116–122`: agregadas cuatro lecturas: agregados y heterogeneidad, concentración 2005–2015, atenuación desde 2016 y límite frente a atribución legal. Los números se tomaron de la tabla A4 sin cambiar sus celdas.
- `_pages/tesis-post3-anexo-metodologico.md:120`: **+1,85 pp** se declara máximo entre los cinco subagregados institucionales; el rango anual de la tabla A4 llega a **+4,56 pp**. Queda pendiente corregir la expresión inglesa «series-wide peak» en el anexo EN, de propiedad del editor EN.
- `_pages/tesis-post3-anexo-metodologico.md:66,124,126,134,219,221`: sustituida la etiqueta de prerregistro por «especificado tras el piloto». `research/post3/confirmatory_design_v3.yaml:1–29` documenta `independent_preregistration: false`, piloto solapado observado y especificación anterior a la ejecución completa v3.

## Verificación

| Comando | Exit | Resultado |
|---|---:|---|
| `ruby scripts/verify_thesis_post3.rb --lang es` | 0 | `POST3_VALID lang=es` |
| `ruby scripts/verify_thesis_post3.rb` | 0 | `POST3_VALID lang=both` |
| `git diff --check` | 0 | Sin errores de formato |

El gate avisa `upstream_custody=UNCOMMITTED_FILE_HASHES`: confirma coherencia entre post y proyección actual, pero no custodia científica en un commit upstream. La fuente cambiada invalida el recibo de navegador anterior; ejecutar QA III local y público solo tras congelar fuentes, build y manifiestos finales.

## Figura III: etiqueta metodológica y derivados

- Evidencia: `incubadora/tesis_mae_mejorada/research/post3/agy_full_series_v1/compute_full_series_2004_2025.py:432–433` excluye del control estudiantes expuestos alguna vez y escuelas del conjunto de cierres; una etiqueta pública «Callaway y Sant’Anna» como estimador exacto excedía esa implementación. El artefacto de resultados conserva las magnitudes; el cambio es de atribución editorial.
- `incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py:199–204,299–304,364–405,534–631`: panel B, rótulo del agregado, `desc` SVG y metadatos ES/EN ahora dicen «ponderado por expuestos» / «exposed-weighted»; **+9,11 pp** y cotas Manski **[+0,43; +16,21]** intactas. La forma de tres paneles se conserva porque aporta cohorte, régimen y selección basal; rediseñarla no resolvería el error de atribución y ampliaría superficie de cambio.
- El productor ahora acepta `--only-figure cohort-series-infographic` para regenerar esa familia y calcular el manifiesto completo usando bytes existentes de las otras figuras. Fue necesario porque el build completo reescribió fuentes embebidas de 24 SVG ajenos a la familia; se restauraron exactamente sus bytes previos, comprobados contra HEAD, y el build selectivo preservó esos activos.
- `outputs/post3_visuals/manifest.json` SHA-256 `3c207de3c56f23c5d83874edd78a6fdc3b353ce81333baec8b389ca6ce42b4bd`; productor SHA-256 `ad3e36895604a0ead525a9c7aa698d72ce78b3bc8f1ac6a7bada9bd58f8e0245`. Espejo blog byte idéntico por validación. CSV de la serie SHA-256 `cb82f6185462c69beb7b148d7fbcfa6955f48da3801486183b99c69d43f0325a`, sin cambio frente al snapshot previo.

| Comando | Exit | Resultado |
|---|---:|---|
| `/opt/entornos/mamba312/bin/python scripts/336_post3_visuals.py build --only-figure cohort-series-infographic` | 0 | `PASS: 77 artefactos registrados` |
| `/opt/entornos/mamba312/bin/python scripts/336_post3_visuals.py validate` | 0 | `PASS: visuales Post III vigentes, accesibles y espejados` |
| `ruby scripts/verify_visual_assets.rb --strict` | 0 | 18 manifests, 238 activos, 0 avisos |
| `python scripts/validate_skill.py` | 0 | `PASS skill contract` |
| `rg -n 'Callaway|Sant|C&S aggregate|Agregado C&S' assets/images/tesis-post3/cohort-series-infographic-*.svg assets/images/tesis-post3/cohort-series-infographic-*.visual-manifest.json assets/images/tesis-post3/manifest.json` | 1 | Ninguna etiqueta exacta residual en derivados públicos |

Comparación SHA-256 antes/después en `outputs/post3_visuals` y espejo: 16 variantes SVG/PNG de la familia, ocho manifiestos por visual —dos de esta familia y seis ligados al SHA del productor— y el manifiesto global cambiaron; cero CSV y cero activos SVG/PNG ajenos a la familia cambiaron. Inspección raster de móviles ES claro y EN oscuro: la nueva etiqueta cabe en el panel A.

## QA funcional local del build r2

Artefacto `/tmp/codex-thesis-production-site`, servidor `http://127.0.0.1:4005`, ambos posts y anexos ES/EN, claro/oscuro y 320/390/768/1440 px:

| Comando | Exit | Resultado |
|---|---:|---|
| `node scripts/verify_thesis_post3_browser.mjs --base-url http://127.0.0.1:4005 --artifact-root /tmp/codex-thesis-production-site --summary --receipt docs/plans/20261108-thesis-production/evidence/figure-correction/r2-post3-browser-local.json` | 0 | 32/32 filas, noJS e impresión PASS; manifiesto 77/77, SHA `3c207de3c56f23c5d83874edd78a6fdc3b353ce81333baec8b389ca6ce42b4bd` |
| `node scripts/verify_thesis_post4_browser.mjs --base-url http://127.0.0.1:4005 --artifact-root /tmp/codex-thesis-production-site --summary --receipt docs/plans/20261108-thesis-production/evidence/figure-correction/r2-post4-browser-local.json` | 0 | 32/32 filas, noJS e impresión PASS; manifiesto 51/51, SHA `e89bdf4f3f025bd73edbaf49f3d5cc09326c6f40bc48765cf898042d811ba308` |

Un primer intento III dentro del sandbox salió 2 antes de abrir una página: Brave falló al iniciar crashpad (`setsockopt: Operation not permitted`). Los dos recibos válidos se obtuvieron ejecutando Playwright en el host. Esta QA es local y anterior a la eventual publicación; la QA pública necesita un nuevo SHA desplegado y artefacto CI concordante.
