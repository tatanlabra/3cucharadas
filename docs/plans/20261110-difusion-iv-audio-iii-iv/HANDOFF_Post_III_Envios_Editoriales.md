# Handoff para Codex · Post III sobre cierres escolares en Chile

**Autor:** Cristián Labra Olivares  
**Proyecto:** 3 Cucharadas  
**Fecha de preparación:** 10 de noviembre de 2026, Santiago de Chile  
**Estado:** el Post III está publicado en el sitio. Los paquetes editoriales están por preparar.

## Encargo

Prepara, en el entorno local del autor, un paquete de presentación del Post III para **Zenodo, MPRA/IDEAS–RePEc, Education Policy Analysis Archives (EPAA) y Calidad en la Educación**. Deja fichas de elegibilidad y, cuando corresponda, paquetes condicionales para **SciELO Preprints, Estudios Públicos y Economics of Education Review**. El producto final es una carpeta con archivos listos para revisión humana, formularios en texto y borradores de consultas. Este encargo autoriza preparación local. El autor decide y ejecuta los envíos, depósitos públicos y comunicaciones externas.

Usa un manuscrito maestro y adapta la presentación a cada destino. Conserva el análisis publicado como versión de referencia. Si el repositorio permite ejecutar sensibilidades adicionales, regístralas como trabajo posterior con fecha, código y salidas propias. Prepara las variantes en paralelo. La prioridad para arbitraje es EPAA y la segunda opción es Calidad en la Educación. Para difusión en economía, la vía directa es MPRA. Para preservar una copia del artículo web, la vía es Zenodo.

## 1. Localizar y fijar la versión

1. Desde el repositorio Jekyll, lee las instrucciones locales y revisa `git status --short`. Localiza las versiones ES y EN con `rg -n 'costos-cierre-escolar-trayectorias|RCID v1|78[.,]972' _posts assets` o adapta la búsqueda a la estructura real. Identifica las figuras, tablas, CSV, notas y referencias. Localiza el repositorio de investigación solo si ya tienes acceso autorizado en el entorno.
2. Contrasta el archivo local con la versión web. Guarda en el manifiesto las URL, fecha de consulta, fecha de actualización mostrada, ruta del fuente, SHA de Git si se conoce y huellas SHA-256 de los insumos exportados. Si la publicación y el borrador difieren, usa la versión publicada para Zenodo y registra las divergencias relevantes para el manuscrito.
3. Verifica cualquier PDF existente contra la web. Si solo encuentras el carrusel de difusión o una versión anterior, exporta un PDF del artículo completo con texto seleccionable, figuras legibles, referencias y enlace al original.

**Versiones públicas**  
- [Post III en español](https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/)
- [Post III en inglés](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/)
- [Directorio MINEDUC](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/) · [Matrícula](https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/) · [Rendimiento](https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/)

## 2. Auditar cifras y redactar el manuscrito maestro

**Título de trabajo ES:** *Cierres escolares y continuidad educativa en Chile: evidencia longitudinal de las cohortes 2005–2024*.  
**Título de trabajo EN:** *School Closures and Educational Continuity in Chile: Longitudinal Evidence from the 2005–2024 Cohorts*.

Estructura sugerida: pregunta de política educativa, aporte frente a la literatura, fuentes y población, clasificación de cierres, diseño de comparación, resultados, limitaciones, implicancias y disponibilidad de materiales. Presenta la **ventana principal 2016–2019**, fijada antes de estimar la serie larga, y luego la ampliación a 2005–2024. Explica por qué los desenlaces y denominadores varían entre análisis. Describe la falla de progresión como un indicador compuesto de rezago o salida del registro. Usa «brecha ajustada» o «asociación» para los resultados actuales. Contrasta la contribución con [Grau, Hojman y Mizala (2018)](https://doi.org/10.1016/j.econedurev.2018.05.003) y cita por separado el documento de trabajo de 2014, verificando la autoría de la versión efectivamente citada.

**Controles de referencia para contrastar con la versión vigente**

- En el soporte de la serie larga figuran **1.141 episodios**, **78.972 observaciones expuestas** y **734.472 controles**. Comprueba las unidades, los denominadores por desenlace y la diferencia entre cobertura del panel y cohortes estimadas.
- A partir del CSV de la figura 3, recalcula el conteo de signos, rango, mediana y promedio simple. En la versión cotejada anteriormente, las **19 cohortes estimables de 2006–2024** tienen brechas puntuales positivas, **ocho** intervalos incluyen cero, la mediana es **7,18 pp** y el promedio simple es **7,55 pp**.
- Para **2016–2019**, coteja **+5,29 pp** e intervalo **[2,08; 8,51]** con las cotas por faltantes **[−1,15; 10,98]**. Explica que los intervalos y las cotas representan incertidumbres distintas. Mantén separados los agregados de **9,11**, **7,55** y **6,29 pp** y sus métodos. Etiqueta cada cifra como recalculada, cotejada o solamente reportada.
- Registra los cinco CSV públicos bajo `/assets/images/tesis-post3/`: `sample-flow-data.csv`, `post-pilot-reestimation-data.csv`, `missingness-bounds-data.csv`, `cohort-series-infographic-data.csv` y `territorial-audit-data.csv`. Incluye diccionario, redondeos y tabla de correspondencia entre archivo, figura y afirmación.
- Documenta la limitación del código privado y el alcance de la verificación. Si el autor autoriza preparar código para distribución, revisa que pueda ejecutarse desde las fuentes públicas y elimina rutas privadas, credenciales, microdatos e identificadores. Deja las declaraciones de autoría, financiamiento, afiliación, conflictos, ética y uso de IA para validación del autor.

Si los insumos autorizados están disponibles, compara **D1 y D2 de la RCID v1**, manteniendo fijo el resto del diseño en lo posible. D2 utiliza destinos observados después del cierre para excluir traslados concentrados. Reporta cómo cambian muestra, composición, brecha e incertidumbre. Si se profundiza la identificación, evalúa exposición fijada dos años antes, tendencias previas de la serie larga, sensibilidad a tendencias no paralelas y dependencia por controles compartidos. Si faltan insumos, deja un protocolo ejecutable y el resultado pendiente. Continúa preparando las versiones que pueden sostenerse con la evidencia actual.

## 3. Preparar cada destino

En cada ficha incluye URL oficial, fecha consultada, sección, formato, límites, requisitos de datos y ética, cargos si corresponden, política de publicación previa y preprints, preguntas abiertas y paso manual. Para una política ambigua, guarda la consulta editorial y registra la respuesta cuando el autor la tenga.

| Destino | Entregable local | Decisión de envío |
|---|---|---|
| **Zenodo** | PDF fiel a la web, cinco CSV, README, metadatos ES/EN, licencia por confirmar y URL de origen. | Archivar la versión web como informe u otro tipo apropiado según el formulario. Si hay interés inmediato en arbitraje, resolver antes si agregar un depósito público afectaría la elegibilidad del manuscrito derivado. |
| **MPRA → IDEAS/RePEc** | PDF académico autónomo y sin protección, título, resumen y palabras clave ES/EN, códigos JEL candidatos I21 e I28 por verificar, y nota sobre el post previo. | Enviar a MPRA. Una vez aceptado e indexado, comprobar registro en IDEAS/EconPapers y asociarlo al perfil del autor. |
| **EPAA** | Borrador de consulta en español, carta de presentación, portada separada y manuscrito anonimizado según la guía. Como referencia, preparar resumen de hasta 200 palabras, 3–5 palabras clave y hasta cinco tablas o figuras en el cuerpo. | Primera consulta para arbitraje. Verificar vigencia de requisitos, pausas de recepción, política de anonimización y tratamiento de anexos. |
| **Calidad en la Educación** | Consulta editorial, carta y variante *Estudios* orientada a Chile. Como referencia, respetar las 10.000 palabras totales, incluyendo tablas, gráficos, notas y bibliografía. | Alternativa a EPAA. Preparar ambas variantes y presentar el manuscrito a una sola revista a la vez. |
| **SciELO Preprints** | Ficha de elegibilidad, PDF académico y metadatos condicionales. | Elegir esta vía antes de depositar el mismo manuscrito en otro servidor de preprints. Verificar las condiciones sobre licencia CC BY, depósito previo y autorización de la revista cuando corresponda. |
| **Estudios Públicos** | Ficha y esquema de nota de investigación centrada en RCID y continuidad escolar. | Confirmar vigencia del formato de nota y criterio sobre el blog previo. Expandir a manuscrito solo si hay encaje editorial. |
| **Economics of Education Review** | Ficha en inglés y esquema de contribución frente al artículo de 2018. | Reservar para una versión con reproducción desde fuentes y sensibilidades metodológicas resueltas. Revisar la guía oficial antes de invertir en la adaptación. |

**Consulta editorial común para adaptar:** «¿Considerarían para evaluación un manuscrito original derivado de un artículo de divulgación ya publicado en el sitio personal del autor, que presenta resultados y CSV agregados? El manuscrito reorganiza la contribución para una audiencia académica y declara la relación con esa publicación. ¿Se considera publicación previa? ¿Cambiaría la respuesta si el autor archivara la versión del blog en Zenodo o depositara el manuscrito académico como documento de trabajo?». Agrega título, enlace y las diferencias que existan efectivamente. Verifica el canal editorial oficial antes de dejar el borrador listo.

## 4. Entrega y criterios de aceptación

Entrega una carpeta de trabajo según las convenciones locales. Usa `post-iii-envios/` como nombre provisional si no hay una ruta definida. Incluye:

- `README.md` con orden de presentación, estado y paso manual por destino.
- `manuscrito-maestro.md` y exportaciones PDF/DOCX según corresponda. Revisa los archivos renderizados, paginación, tablas, figuras, hipervínculos y referencias.
- `auditoria/` con manifiesto, cotejo de cifras, materiales públicos y registro de pendientes. Conserva comandos y resultados de toda ejecución efectiva.
- `destinos/` con fichas, metadatos, consultas y variantes. Distingue «listo para revisión del autor», «pendiente de respuesta editorial» y «requiere análisis adicional». Revisa los metadatos de autor y el material suplementario de la versión anónima.
- Un resumen de diferencias entre versiones, afirmaciones con evidencia parcial y archivos que requieren decisión del autor. Comprueba que los paquetes externos contengan exclusivamente archivos destinados a distribución. Deja el sitio y sus rutas de publicación fuera de la entrega editorial.

## Normas y fuentes para actualizar antes de enviar

- [Zenodo](https://help.zenodo.org/docs/deposit/about-records/) · [MPRA](https://mpra.ub.uni-muenchen.de/information.html) · [Envío a MPRA](https://mpra.ub.uni-muenchen.de/help/submission.html) · [Participar en IDEAS/RePEc](https://ideas.repec.org/participate.html)
- [EPAA, alcance](https://epaa.asu.edu/index.php/epaa/about) · [EPAA, envíos](https://epaa.asu.edu/index.php/epaa/about/submissions) · [Calidad en la Educación, envíos](https://www.calidadenlaeducacion.cl/index.php/rce/about/submissions)
- [SciELO Preprints](https://preprints.scielo.org/index.php/scielo/about/submissions) · [Estudios Públicos](https://www.estudiospublicos.cl/index.php/cep/informacion-revista) · [Economics of Education Review](https://www.sciencedirect.com/journal/economics-of-education-review/publish/guide-for-authors)
