# CASEN 2024: hogares con sitio propio compartido

## Estimando y límites

`p_h = Σ expr × I(v9 ∈ {3,4}) / Σ expr × I(v9 ∈ {1,…,11})`, con una observación por hogar: su jefatura (`pco1=1`). El denominador incluye arrendatarios, cesionarios y las demás tenencias válidas; no se restringe a propietarios. Cada región usa la misma definición con dominio regional. El cálculo comunal usa `expc` y se publica únicamente como descripción exploratoria, sin inferencia representativa ni intervalos.

El indicador cuenta **hogares** que declaran sitio propio compartido con otras viviendas. No identifica todos los sitios compartidos: otros regímenes de tenencia pueden coexistir en un sitio. Tampoco identifica viviendas únicas, sitios únicos, roles fiscales, exenciones ni una fracción causal de la brecha entre roles y viviendas.

La [nota oficial de uso, enero de 2026](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf), páginas 1–5, define cobertura, unidades, factores y cruce por persona. Su distinción territorial sustenta `expr` para nacional/regiones y la advertencia comunal. El [portal oficial CASEN 2024](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024) proporciona la base y los libros de códigos; se congelan sus archivos locales por SHA-256 en `provenance.json`. La encuesta tiene dominios de diseño; ello no garantiza automáticamente precisión suficiente de este indicador particular.

## Fuentes, extracción y validación

- R carga el RData original en un entorno aislado y comprueba almacenamiento y clases de las once columnas antes de convertirlas. Acepta vectores integer/double con clases numéricas o labelled admitidas; rechaza factores, texto, integer64 y clases desconocidas. Después retira atributos y convierte a numeric, evitando despacho S3 de coerción. Los datos seleccionados pasan por memoria a Python; ningún archivo derivado contiene personas, hogares ni identificadores.
- La base complementaria se une por `(folio, id_persona)` con cardinalidad uno a uno y cobertura idéntica en ambos sentidos; no hay unión por posición ni multiplicación de filas.
- Todos los hogares deben tener una sola jefatura; cada campo de vivienda, diseño, geografía, `v9` y `v28` debe ser consistente dentro del hogar. Un incumplimiento aborta la exportación.
- Se exigen pesos de jefatura `expr` y `expc` positivos y finitos, territorios/diseño no faltantes y conservación de todos los pares `(varstrat,varunit)` al pasar de personas a jefaturas.
- El libro de códigos, hoja `V`, contiene `v9=1,…,11`; positivos 3 y 4. `NA` se trata como falta de respuesta; cualquier código no documentado, incluidos sentinelas trasladados desde otra pregunta, aborta. Los códigos no se recodifican a cero.
- `v28=1/2` es una pregunta condicionada. No se usa como filtro general. En el diagnóstico de vivienda se toma el hogar único; en viviendas multihogar se exige un principal único. La selección es un diagnóstico muestral no ponderado, nunca un peso oficial de vivienda.
- `n_flagged=0` es un centinela tautológico de exportación exitosa: las inconsistencias excluyentes abortan antes de exportar. Ese cero no constituye una medición independiente ni evidencia positiva de calidad. La evidencia de los controles reside en las comprobaciones ejecutadas y sus casos de rechazo; `n_missing` se refiere exclusivamente a `v9` ausente.

## Incertidumbre de diseño

Para dominio `d`, total ponderado válido `T_d` y razón `p`, la contribución de cada hogar es `e_j = w_j I(j ∈ d) (y_j-p)/T_d`. Se agregan estas contribuciones por PSU anidada en estrato. La varianza es `Σ_h [m_h/(m_h−1)] Σ_i (e_hi−media_h)^2`.

Se conservan **todas las PSU del diseño**, incluyendo las exteriores al dominio y las que solo contienen respuestas no válidas, con contribución cero. `n_psu`, `n_strata` y `design_df` describen ese diseño completo, no el número de PSU efectivamente observado en una comuna. Para comunas sin muestra los tres se declaran cero y `ci_status=no_sample`.

La aproximación usa reposición a nivel de conglomerado y no aplica corrección de población finita, por faltar los tamaños por etapa. `IC95 = clip(p ± 1.959963985 SE, 0, 1)` es un intervalo normal aproximado, no un intervalo exacto. Cualquier estrato con una sola PSU invalida SE e IC (`not_estimable_singleton`), incluso fuera del dominio: no se inventa una política oficial para singleton. Razones en 0/1 o varianza degenerada producen `not_conclusive_boundary_or_degenerate` con SE/IC nulos, nunca una falsa certeza exacta. Dominio vacío produce estimación nula. Todas las comunas muestreadas tienen `descriptive_nonrepresentative_no_ci`.

La referencia Julia `_taylor_prop_se` se lee sin modificarla. La paridad se limita a fixtures con al menos dos PSU por estrato porque esa función omite singleton, mientras este pipeline los declara no estimables. Coincidencia entre implementaciones es una comprobación de consistencia; la prueba independiente es el oráculo algebraico manual: pesos `(1,2,1,2)`, dos estratos con dos PSU, `p=1/3`, `V=8/81`; otro dominio con dos de tres PSU exige `V=3/16`, que cambia incorrectamente a `1/4` si se elimina la PSU externa.

## Robustez, cobertura y selección

`audit.json:sensitivity` entrega por territorio composición urbano/rural, tasas dentro de cada área, ponderación utilizada y cotas al reponer toda falta de respuesta como negativa o positiva. Son descripciones de composición, no un efecto causal urbano/rural. Si `Y` es el total positivo, `M` el peso faltante y `T` el total de hogares, las cotas son `Y/T` y `(Y+M)/T`. Si no hay faltantes ambas coinciden con la estimación de casos completos; esto no prueba ausencia de sesgos de medición o no respuesta de encuesta.

El universo comunal procede de `V1_Viviendas-y-hogares-censados.xlsx`, Censo 2024, hoja 2. El cruce observado tiene 346 comunas: 335 muestreadas y 11 sin muestra; se incluyen todas por CUT, sin ranking. Las comunas fuera de la muestra CASEN tienen `estimate=null`, `ci_status=no_sample` y conteos muestrales cero; no se imputan tasas cero. `audit.json:commune_coverage` contiene el cruce y los nombres/CUT ausentes. Valparaíso y Viña del Mar fueron seleccionadas después de exploración previa; sus resultados no son contrastes confirmatorios.

## Resultado observado de esta ejecución

| Comprobación | Observación |
|---|---|
| Personas / hogares / viviendas muestrales | 218.367 / 78.654 / 77.618 |
| Positivos `v9=3/4` entre jefaturas | 787 hogares, sin faltantes `v9` |
| Total nacional expandido de hogares válidos | 7.143.171 con `expr` |
| `p_h` nacional | 1,0878222 %; SE 0,0600480 puntos porcentuales |
| IC normal aproximado nacional | 0,9701303–1,2055141 % |
| Diseño completo | 12.512 PSU, 756 estratos, 11.756 grados de libertad |
| Diagnóstico de vivienda | 76.712 viviendas unihogar y 906 multihogar; las 906 tienen principal único |
| Filtro general `v28` | Rechazado: 76.252 jefaturas tienen `v28` faltante |

Como contraste descriptivo, la composición nacional expandida es 88,4510 % urbana y 11,5490 % rural; las respectivas tasas son 1,0668 % y 1,2491 %. Valparaíso tiene 98,5093 % de peso urbano y Viña del Mar 100 %; sus tasas comunales descriptivas son 9,2681 % y 8,5995 %. No hay observaciones rurales en Viña del Mar: la tasa rural es nula en el sentido de dato ausente (`null`), no una tasa cero.

Estas cifras pertenecen a la ejecución y fuentes cuyos hashes figuran en los recibos; no son un oráculo fijado para futuras versiones.

## Anexo algebraico sin aplicación fiscal

Definir `R1 = roles/viviendas` y `p_v` como una proporción **hipotética de viviendas** que están en sitios con exactamente dos viviendas, suponiendo que todos los otros sitios contienen una vivienda. Entonces `sitios = viviendas × (1 − p_v/2)` y `R2(p_v) = roles/sitios = R1/(1 − p_v/2)`. La fórmula cambia si cambia la definición del parámetro o la multiplicidad. **No sustituir `p_v` por `p_h`**, ni usar esta identidad para ajustar la brecha fiscal: no se dispone del enlace representativo vivienda–sitio–rol que permitiría hacerlo.

## Reproducción y aceptación

Desde la raíz del repositorio analítico, definir argumentos con rutas locales autorizadas; las rutas privadas no forman parte de los artefactos públicos:

```sh
python3 v5_brecha/scripts/casen_shared_site.py \
  --rdata "$CASEN_RDATA" --communes "$CASEN_COMMUNES" \
  --codebook "$CASEN_CODEBOOK" --communal-codebook "$CASEN_COMMUNAL_CODEBOOK" \
  --use-note "$CASEN_USE_NOTE" --commune-universe "$CENSUS_COMMUNES"
python3 -m unittest discover \
  -s v5_brecha/tests -p test_casen_shared_site.py -v
python3 v5_brecha/artifacts/casen_shared_site/evidence/reproduce_checks.py \
  --julia-reference "$JULIA_TAYLOR_SOURCE" --julia-project "$JULIA_REFERENCE_PROJECT"
```

No se ejecuta `prepare_sources`, no se instala software y no se escribe en las fuentes externas. `evidence/verification.json` registra suites, hashes y paridad Julia. Seis mutaciones aisladas deben salir no cero: desactivar la guarda numérica de R, quitar PSU exteriores, limitar indebidamente la tenencia del denominador, fabricar IC exacto de borde, contar personas como hogares y omitir singleton. La recuperación usa el código original cuyo hash se conserva. Los fixtures negativos de unión, pesos y claves deben rechazar la entrada. Los artefactos CSV/Parquet/JSON se comparan entre sí y con la partición regional ponderada.

`provenance.json` liga fuentes, código y salidas; el pipeline verifica que los hashes de código capturados al inicio siguen iguales antes de exportar; `evidence/pipeline-receipt.json` liga ejecución y aceptación. Un hash distinto, una falla científica, falta de muestra convertida a cero, o datos privados en la exportación bloquea D1 y exige regenerar/revisar. Un test verde no demuestra causalidad, representatividad comunal ni optimalidad global.

Rollback: retirar únicamente los archivos propios de este módulo y sus agregados tras revisar el diff; conservar evidencia y trabajo ajeno. No modificar las fuentes, el pipeline fiscal anterior ni las proyecciones del blog. No se realiza commit ni publicación desde D1.


## Disposición de revisión D2

- **F1, P1:** observado con un RData sintético real: el reader anterior salía 0 y convertía el factor `v9="2"` a código 4. El defecto se reprodujo antes de corregir; `evidence/D2-F1-red-factor.json` conserva el contraejemplo y el reader anterior permanece en el histórico.
- **F1, estado de la fuente original:** inspección exclusiva de clases y dimensiones observó 11 columnas de almacenamiento double: cinco `haven_labelled/vctrs_vctr/double` y seis `numeric`. No había factor ni integer64. Esto descarta remapeo por factor en ese archivo concreto; no garantiza otras versiones de fuente.
- **F1, corrección:** `src/casen_shared_site/rdata.py` centraliza el reader usado por main y pruebas. Siete pruebas mediante Rscript y RData sintéticos cubren numeric, integer, labelled numérico, factor, carácter, integer64 y salida exclusiva de metadata. Una mutación que desactiva la guarda debe producir fallo observado antes de recuperar verde.
- **F1, fallo adicional de prueba:** la primera ejecución detectó que pandas omitía una fila completamente vacía en el fixture de una sola columna numeric con NA. Se corrigió con `skip_blank_lines=False`; el fallo se conserva en `evidence/D2-F1-r-tests-initial-failure.log` y la recuperación de las siete pruebas en `evidence/D2-F1-r-tests-green.log`.
- **F1, privacidad de metadata:** el guard anterior confundió los nombres `folio`/`id_persona` del esquema con valores de personas. Se conserva ese falso positivo en `evidence/D2-F1-privacy-false-positive.log`; ahora sólo se admite la estructura exacta de clases/almacenamiento y dos fixtures rechazan identificadores fuera de ella o valores ocultos dentro de metadata.
- **F2:** la política de cualquier singleton ⇒ SE/IC no estimable se conserva deliberadamente como restricción conservadora; no se adopta una corrección oficial inexistente.
- **F3:** se explicita que `n_flagged=0` no es prueba positiva independiente de calidad. Los recibos y pruebas de rechazo son la evidencia pertinente.
- **Trazabilidad:** el freeze anterior `e40cae6a5f77becf9634b51c1e4b75be3ea21bc1f2cfd56d5dd487c61d5b791f`, sus archivos, recibos y logs fueron preservados bajo `evidence/history/pre-d2-f1-e40cae6a5f77/`. `evidence/D2-F1-disposition.json` registra el vínculo del candidato y la comparación de agregados; el digest vigente está en [`evidence/freeze.json:source_digest`](../artifacts/casen_shared_site/evidence/freeze.json) y comprende este método, sin incrustarlo autorreferencialmente; la revisión enfocada D2 sigue siendo necesaria.
