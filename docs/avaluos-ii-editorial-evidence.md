# Avalúos II: evidencia y decisiones editoriales

Fecha de revisión: 2026-09-10. Alcance: borradores ES/EN, interpretación de la brecha, campamentos, materialidad y avalúos H. No es un dictamen sobre inmuebles ni una autorización de publicación.

## Pregunta y estrategia de fuentes

Pregunta: ¿qué evidencia permite priorizar una revisión catastral con interés tributario sin convertir una diferencia comunal de unidades en propiedades omitidas o contribuciones impagas?

Criterio de inclusión: fuentes primarias oficiales chilenas para unidades, procedimiento y período; manual INE para clasificación; publicaciones originales para el mecanismo de capacidad fiscal y sus contraejemplos. Se excluyen blogs inmobiliarios, comentarios de redes, resultados sin procedencia y coeficientes internacionales para extrapolar montos a Chile.

Consultas MCP `paper-search.search_papers` sobre `property tax cadastre information constraints tax capacity randomized property registration` y `property tax cadastre`, fuente OpenAlex: ambas devolvieron cero resultados sin error del proveedor. Se continuó con búsqueda web de fuentes primarias. `bibliography-apa.format_apa` resolvió los DOI 10.3386/w29923 y 10.1086/730551; no se escribió en bibliografías ajenas al proyecto. El documento del FMI se identificó y leyó directamente en el sitio del editor.

## Fuentes verificadas y alcance de cada afirmación

| Fuente | Evidencia localizada | Uso y límite editorial |
|---|---|---|
| [SII, ejemplo de casa 2026S1](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf), p. 1 | Monto exento habitacional $60.030.710, período explícito primer semestre 2026 | Comparación de cada avalúo H con el umbral del mismo período; no sustituye exenciones ni cálculo individual del impuesto |
| [SII, avalúo fiscal y valor comercial](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm), FAQ actualizada 08-04-2026 | Son conceptos distintos | No llamar precio de venta al avalúo ni importar tasaciones comerciales |
| [SII, qué es el avalúo fiscal](https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html) | Terreno más construcción; ubicación, superficie, materialidad y otros factores | Materialidad aceptable no basta para determinar avalúo ni obligación |
| [SII, documentación para solicitudes](https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html), Modificación de Avalúo de Construcción | Admite planos o croquis y otros antecedentes para construcciones no regularizadas | Refuta equiparar informalidad urbanística con imposibilidad de registro fiscal |
| [SII, inclusión de un bien raíz](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm), FAQ actualizada 07-04-2026 | Procedimiento de registro de terreno/construcción y avalúo | Enrolar y actualizar un rol existente son actuaciones diferentes; no identificar su necesidad mediante una resta |
| [Ley 20.234, artículo 16](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0) | Roles y avalúos separados después de determinados hitos de regularización | La informalidad actual no equivale a ausencia fiscal permanente; no extenderlo a todos los asentamientos |
| [TGR, impuestos y tipos de impuestos](https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos) y [SII, contribuciones y distribución](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html) | Recaudación por Tesorería y distribución municipal mediante FCM | No confundir giro con pago ni pesos asociados a una comuna con ingresos retenidos íntegramente |
| [INE, manual de microdatos Censo 2024](https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf), pp. 103–106 | Código viv04, viv05 y viv06 | Tipo y materiales aceptables constituyen un escenario estricto; no calidad integral, lujo o condición tributaria |
| [MINVU, repositorio vivienda y déficit](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/), Caracterización de campamentos en Censo 2024 | Cruce geográfico 2024 con 1.373 campamentos, 81.993 viviendas ocupadas y 77.399 hogares | No confundir la fotografía oficial 2024 con los 1.345 polígonos vigentes de CNC 2026 |
| [Grote y Wen (2024)](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf), pp. 16–18, cuadro 2 y sección Coverage | Distingue cobertura, valoración y recaudación; propone enlazar imágenes, terreno y registros | Marco administrativo para una revisión predial; no ofrece una tasa chilena de omisión |
| [Dzansi et al. (2022, revisión febrero 2025)](https://www.nber.org/system/files/working_papers/w29923/w29923.pdf), resumen original indexado | Experimento con tecnología geoespacial para localizar contribuyentes y entregar giros en Ghana | Evidencia de un mecanismo administrativo, sin transferir tamaño de efecto ni probabilidad a Chile; lectura limitada a resumen original indexado y metadatos DOI porque la apertura directa respondió 403 |
| [D'Arcy, Nistotskaya y Olsson (2024)](https://www.journals.uchicago.edu/doi/full/10.1086/730551), introducción y sección IV | Panel histórico, causalidad limitada; no encuentra efecto sobre impuesto a la propiedad en mecanismos | Contraejemplo a «mejor catastro implica automáticamente más recaudación predial»; tampoco demuestra ausencia de beneficio en Chile |

La página dinámica de [SII sobre reajustes y exenciones](https://www.sii.cl/ayudas/ayudas_por_servicios/2242-reajustes_exenciones-2468.html) ya muestra 2026S2 ($61.711.570), por lo que no se usa para reemplazar el umbral del extracto 2026S1. ChileAtiende también tenía indexado el umbral H1 correcto, pero el PDF SII con período explícito es el respaldo principal.

El manual INE se leyó desde `/home/ende/Descargas/investigacion/censo2024/manual_uso_microdatos_censo2024.pdf`, pp. 103–108, con `pdftotext`; su URL oficial no pudo abrirse mediante el fetch web de esta revisión. El texto local confirma dos discrepancias entre prosa y código: la prosa permite paredes recuperables en materialidad aceptable y exige todos los materiales irrecuperables; el código exige tres aceptables y basta un componente irrecuperable, después de no respuesta. El análisis sigue el código y declara esa decisión.

## Inferencia y pruebas que podrían refutarla

| Nivel | Afirmación válida | Prueba discriminante o descarte |
|---|---|---|
| Hecho agregado | Existen totales censales, conteos H, hogares CNC con dato y atributos observados de viviendas/roles | Reconciliación de cortes, universos, claves y hashes; una falla exige corregir la cifra |
| Deducción | Vivienda, hogar, construcción y predio no son unidades equivalentes; restarlas no identifica omisiones | Sólo un enlace individual puede demostrar correspondencia predial |
| Inducción descriptiva | El descuento uno a uno de campamentos cambia desigualmente las brechas comunales | Repetición bajo fuente/corte comparable y revisión de polígonos sin conteo |
| Escenario | Trasladar al residuo la proporción de tipo/materiales aceptables del parque ocupado | Si el parque residual difiere del observado o del universo ocupado, revisar o descartar el traslado; alternativas por no respuesta y categoría amplia |
| Abducción tributaria | Residuo persistente más avalúos H altos justifica investigar posibles predios omitidos o avalúos desactualizados | Construcción geolocalizada, rol/destino, superficie, avalúo, exenciones y fechas; se descarta para un caso si ya está bien registrado o no hay obligación exigible |
| Incertidumbre | Media/mediana/proporción H observada no identifica distribución ni probabilidad de los posibles ausentes | Muestra vinculada con diseño de selección, comparación de atributos y validación predial independiente |

No se multiplica el escenario de materialidad por la proporción H sobre umbral: no hay enlace entre las dos poblaciones ni distribución conjunta. No se presentan intervalos de confianza de estos escenarios como si provinieran de una muestra probabilística. Las variantes son sensibilidad de supuestos, no bandas estadísticas de probabilidad.

## Corrección explícita y responsabilidades

El borrador anterior decía 73.338 viviendas irrecuperables. Aplicar la prioridad de no respuesta del código viv06 reduce el conteo a 72.642: 696 menos. No cambia viviendas totales, roles H ni descuento campamentos. El indicador central adicional usa tipo aceptable y los tres componentes materiales aceptables: 5.774.146, sobre 6.408.172 viviendas ocupadas con moradores presentes. Contar sólo los materiales daría 5.799.969, incluyendo 25.823 viviendas de tipo irrecuperable, razón para exigir ambas condiciones.

Las cifras comunales nuevas se incorporan a los borradores a partir del artefacto reconstruido `catastros_sii/v5_brecha/artifacts/fiscal_gap/communes.json`, versión 3. La construcción y prueba de esos artefactos pertenecen a `catastros_sii/v5_brecha`; este documento audita su interpretación editorial.

La selección editorial no usa una puntuación fiscal: `camp_sensitivity_positive_gap > 0` y `assessment_median_clp > 60030710`. Hay 15 comunas elegibles y se publican todas, ordenadas por residuo descendente, sin seleccionar sólo ejemplos favorables. Se incluyen residuo, `materiality_acceptable_scenario` redondeado, mediana H en millones y `assessment_above_exemption_share`. La media Iquique $73.844.661,60018735 contrasta con su mediana $60.244.859 para mostrar que no son intercambiables. Lo Barnechea (residuo 2.300, mediana $290.026.123, proporción sobre umbral 85,6288835881%) y Zapallar (1.948, $182.981.548,5, 74,9674690956%) permiten explicar el contraste entre tamaño físico y perfil de avalúos, condicionando cualquier traslado a comparabilidad verificada. La selección por mediana no mide certeza ni importancia fiscal de una eventual omisión.

Los borradores conservan `published: false` y la conciliación fiscal pendiente. El texto no acusa negligencia ni identifica una deuda. Señala una prioridad verificable de revisión y exige enlazar inmuebles, obligaciones y fechas antes de valorar giros faltantes. Asemejar propiedades a partir de una media comunal es una hipótesis de selección, no un hallazgo de ausencia de cobro.

## Validación editorial local

- Front matter ES/EN parseado con PyYAML; idioma y `published: false` correctos; bloques `details` equilibrados.
- 48 comprobaciones numéricas contra `communes.json`: las 15 filas seleccionadas, cinco filas de campamentos y cuatro cifras nacionales, en ambos idiomas; todas aprobadas.
- El primer intento del comprobador ad hoc usó una clave inexistente (`gap_2026s1`) y falló con `KeyError`; corregido a la clave real `signed_gap`, la conciliación pasó. No fue una discrepancia del artefacto ni del texto.
- `git diff --check` sin errores. El build Jekyll y la verificación visual integrada quedan a cargo del agente principal, que trabaja simultáneamente en el visor.

## Bibliografía normalizada

- Grote, M., & Wen, J.-F. (2024). *How to Design and Implement Property Tax Reforms* (How to Note 2024/006). International Monetary Fund. https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf
- Dzansi, J., Jensen, A., Lagakos, D., & Telli, H. (2022). *Technology and Tax Capacity: Evidence from Local Governments in Ghana* (Working Paper 29923; revisión de febrero de 2025 consultada). National Bureau of Economic Research. https://doi.org/10.3386/w29923
- D'Arcy, M., Nistotskaya, M., & Olsson, O. (2024). Cadasters and economic growth: A long-run cross-country panel. *Journal of Political Economy, 132*(11), 3785–3826. https://doi.org/10.1086/730551
