# Avalúos II — revisión del escenario monetario, 11 de septiembre de 2026

## Alcance y decisión editorial

Se conserva la base revisada aportada por el usuario y las veinte filas de sus tablas. Se añade a la segunda cucharada un escenario de impuesto general teórico, calculado por predio y agregado por comuna. La tercera cucharada distingue ese resultado de giros efectivos, deuda constatada y recaudación. El manuscrito archivado en `docs/editorial-sources/avaluos-ii-revisado-20260911.md` no fue modificado.

La publicación fue autorizada por el usuario al terminar todos los pasos y revisiones. Esta revisión delegada mantiene ambos documentos en `_drafts` y con `published: false`; el coordinador conserva la responsabilidad de validación integral, promoción y despliegue.

| Decisión | Aplicación | Motivo verificable |
|---|---|---|
| Unidad del modelo | Impuesto general teórico anual equivalente bajo parámetros 2026S1 | No se dispone de giro neto habitacional conciliado; el escenario normativo no se presenta como ese dato observado |
| Orden de operaciones | Calcular cada impuesto; luego media y mediana; finalmente multiplicar por residuo y q | Una función con exención y tramos no conmuta en general con el promedio |
| Denominador | Todos los predios habitacionales con avalúo válido, incluidos resultados cero | Excluir ceros inflaría el traslado del perfil observado a un predio comparable elegido de ese universo |
| Media y mediana | Dos referencias, sin orden garantizado ni intervalo estadístico | Resúmenes de distribución no identifican límites de incertidumbre ni la distribución de inmuebles ausentes |
| q | Fracción hipotética del residuo que daría lugar a nuevos predios comparables | No vuelve a aplicar la proporción afecta ni modela una tasa de cobro; escenarios 1, 0,5 y 0,25 |
| Selección | Residuo positivo y avalúo mediano superior a $60.030.710 | Mantiene las quince comunas del filtro editorial; el gráfico monetario cambia su orden por escenario con la media |
| Componentes omitidos | Aseo, sobretasas y beneficios particulares | La exclusión define el modelo; no prueba que el resultado sea un límite inferior o superior del giro efectivo |
| Materialidad | Se conserva como escenario físico independiente | No hay distribución conjunta identificada que justifique usarla como otro descuento tributario |

## Revisión adversarial de afirmaciones

| Tipo | Afirmación y evidencia | Límite o condición de descarte |
|---|---|---|
| Hecho verificado | El ejemplo oficial SII consultado describe los parámetros de 2026S1: exento $60.030.710, cambio en $214.395.361, tasas anuales 0,893 % y 1,042 % | No se extrapola la vigencia a 2026S2 ni a una liquidación individual |
| Hecho verificado | El diccionario de detalle catastral define el campo semestral como contribución con aseo, y el destino habitacional en su tabla | El campo observado no se llama neto; tampoco se emplea como recaudación pagada |
| Deducción | La exención general introduce ceros en el impuesto teórico; los ceros deben permanecer en ambos estadísticos del universo definido | Una mediana cero no significa ausencia de predios afectos; la revisión conserva ese contraejemplo |
| Deducción | Reducir q a la mitad o a un cuarto escala linealmente los montos | No valida cuál q representa la realidad ni garantiza el orden de comunas si q varía entre ellas |
| Patrón descriptivo | Una brecha física más pequeña puede acompañarse de mayor escala monetaria al cambiar el perfil de avalúos | La comparación es condicional al universo y al modelo, no una probabilidad observada de omisión |
| Abducción provisional | Una discrepancia persistente junto a avalúos altos vuelve atendible la hipótesis de una omisión con interés tributario | Evidencia discriminante: inmuebles localizados, expediente, destino y fechas; descartar si roles matrices, otros destinos o períodos concilian la diferencia |
| Supuesto no identificado | El perfil tributario de los predios eventualmente incorporados sería comparable al registrado | Se debilita si la revisión revela predios de menor avalúo, múltiples viviendas por rol o beneficios sistemáticamente diferentes |
| No establecido | Negligencia institucional, deuda exigible, omisiones individualizadas, ingreso municipal retenido | El post no atribuye estos resultados; requieren evidencia adicional separada del ranking |

El contraargumento más fuerte es que las unidades residuales podrían no representar nuevos predios y que, aun cuando los representen, sus avalúos y beneficios podrían diferir del catastro observado. Los escenarios q miden sensibilidad a la cantidad asumida, pero no resuelven por sí solos ese sesgo de composición. La media tampoco constituye un total esperado sin supuestos adicionales sobre esa composición; la mediana es una referencia central, no un estimador del total omitido.

## Fuentes consultadas en esta revisión

- [SII, ejemplo de cálculo para 2026S1](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf): parámetros, periodicidad y separación de aseo y sobretasas.
- [SII, estructura del detalle catastral](https://www.sii.cl/bbrr/descargas/estructura_detalle_catastral.pdf): serie no agrícola, campos 5–8 y tabla de destinos, p. 1.

Consulta web directa del 11 de septiembre de 2026. Se mantuvieron las otras referencias de la versión previa; este trabajo no afirma haber revalidado nuevamente sus doce destinos externos.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| Comparación de tablas de cada borrador contra HEAD | Veinte filas numéricas intactas en español y veinte en inglés |
| Referencias y traducción | Trece referencias resueltas por versión, mismos destinos ES/EN, incluido el nuevo diccionario catastral |
| Terminología y estado | Una definición del código habitacional por idioma; `published: false` en ambos |
| Render matemático con Kramdown y KaTeX del bundle | Ocho expresiones y ocho MathML por versión; una fórmula en bloque; sin error KaTeX ni delimitadores sin procesar |
| Ranking y productos monetarios | Quince comunas seleccionadas con el filtro declarado; orden idéntico a `metadata.model_ranking`; media y mediana por residuo coinciden en las quince, tolerancia relativa 1e-12 |
| Sensibilidad q | Los quince resultados con q=0,5 y q=0,25 equivalen a mitad y cuarto del escenario con la media, tolerancia relativa 1e-12 |
| Contraste del relato | Iquique: $36 millones con mediana y $4.309 millones con media; Lo Barnechea: $4.983 y $6.669 millones; todos coinciden con el redondeo del artefacto |
| Tablas monetarias generadas | Quince filas y noventa celdas numéricas por idioma coinciden con el artefacto y el orden declarado; 180 celdas verificadas entre ES/EN |
| Imágenes monetarias | Los cuatro SVG referidos existen, con viewBox 792 × 612; los atributos width/height reservan esa proporción antes de la carga diferida |
| Whitespace | `git diff --check` correcto tras las ediciones |

Artefacto verificado: `../catastros_sii/v5_brecha/artifacts/fiscal_gap/communes.json`, SHA-256 `552da0e5e1a088f76f953f44081a357d9ed8f5de30a31c337ddee891e2037a58`. La tabla siguiente registra los valores previos al redondeo narrativo, en CLP de impuesto teórico anual equivalente y q=1.

| Comuna | Residuo | Mediana por predio | Media por predio | Escenario con mediana | Escenario con media |
|---|---:|---:|---:|---:|---:|
| Iquique | 18.949 | 1.912,35057 | 227.387,45920421815 | 36.237.130,95093 | 4.308.764.964,46073 |
| Lo Barnechea | 2.300 | 2.166.548,87347 | 2.899.661,91583923 | 4.983.062.408,981 | 6.669.222.406,430229 |

Lo Barnechea ocupa el primer lugar con el orden definido. El contraejemplo de Iquique se explica expresamente: el centro de su avalúo queda cerca del umbral y los dos escenarios resultan muy separados. No se afirma que el par media–mediana sea estrecho, un rango probabilístico ni una banda que contenga una cantidad omitida real.

## Pendientes de integración

- El build Jekyll completo, la revisión visual de la sección, el contraste contra el visor y la publicación corresponden al cierre integrado.

Riesgo residual de interpretación: medio, por la transferencia hipotética entre unidades distintas y por la composición desconocida de los inmuebles ausentes. La documentación reduce la posibilidad de confundir escenario con evidencia de deuda, pero no identifica las omisiones ni la obligación tributaria efectiva.

## Actualización del coordinador

Tras aprobar el build de borradores y sus enlaces, ambos artículos pasaron a `_posts/2026-09-11-avaluos-ii-brecha-residencial{,-en}.md`, con publicación habilitada. El artefacto final es `c21b29389e3a3f0c3d90d7383ac5d19c41851a67d308261a6db841d70e6badfc`: incorpora q=0 y aclaración de sensibilidad; conserva todos los montos narrados y el ranking. El recálculo sólo presenta diferencias flotantes inferiores a 0,000001 CLP en cuatro campos de Galvarino, fuera del ranking. El informe anterior conserva el hash efectivamente revisado en ese momento.
