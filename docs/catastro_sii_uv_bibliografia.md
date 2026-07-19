# Sustento académico — Avalúo fiscal SII × IGVUST por Unidad Vecinal

Bibliografía de respaldo para el post que agrega el avalúo fiscal de 10.343.893 predios del SII
a Unidades Vecinales mediante prorrateo geométrico y lo cruza con el Índice Global de
Vulnerabilidad Socioterritorial (IGVUST) del Ministerio de Desarrollo Social y Familia.

---

## Nota de método y convenciones de verificación

Estrategia de búsqueda: consulta bibliográfica estructurada contra la **API pública de CrossRef**
(`api.crossref.org/works`, campo `query.bibliographic`) para metadatos de revistas; recuperación
directa de PDF primarios (IGVUST, CATMOG 38, BCN) con extracción de texto local; y búsqueda web
para fuentes institucionales y pre-DOI. Normalización APA para revistas, Chicago para documentos
institucionales.

| Marca | Significado |
|---|---|
| ✅ | **Verificado contra CrossRef.** DOI, título, revista, volumen, número, páginas y año confirmados por consulta a la API en esta sesión. |
| 📄 | **Verificado por recuperación del documento.** Descargué el PDF y extraje el dato citado. Se incluyen citas textuales. |
| 🌐 | **Verificado por búsqueda web.** El ítem existe y los datos coinciden en varias fuentes independientes, pero no hay registro CrossRef de primera mano. |
| ⚠️ | **Sin verificar.** De memoria. Requiere comprobación antes de publicar. |

**Convención de páginas:** un `†` tras el rango indica que CrossRef expone **sólo la página
inicial** (típico de registros depositados vía JSTOR); la página final proviene de memoria y no
está verificada. Sin `†`, el rango completo está verificado.

**No se incluye ningún DOI que no haya resuelto en esta sesión.** Donde no hay DOI, se dice.

---

## 1. Precios hedónicos

**✅ Rosen, S. (1974). Hedonic Prices and Implicit Markets: Product Differentiation in Pure
Competition.** *Journal of Political Economy*, 82(1), 34–55.
DOI: [10.1086/260169](https://doi.org/10.1086/260169)

> Es la fundación teórica de toda la tesis del post. Rosen demuestra que el precio de un bien
> diferenciado es un **equilibrio de mercado que revela precios implícitos** de sus atributos, no
> una suma contable de costos. Eso es lo que autoriza a leer el avalúo como un agregador de
> seguridad, conectividad y materialidad. Es también donde está la letra chica: los precios
> implícitos son la **envolvente** de ofertas y demandas, así que identificar disposición marginal
> a pagar a partir de una sola sección cruzada está mal identificado (el "problema de segunda
> etapa" de Rosen). El post debe afirmar *asociación*, no *valoración causal de atributos*.

**✅ Lancaster, K. J. (1966). A New Approach to Consumer Theory.** *Journal of Political Economy*,
74(2), 132–157.
DOI: [10.1086/259131](https://doi.org/10.1086/259131)

> El antecedente que hace inteligible a Rosen: la utilidad no viene del bien sino de sus
> características. Sirve para justificar en una línea, ante un lector no económico, por qué un
> predio es un *vector de atributos territoriales* y no un objeto indivisible. Útil para la
> exposición divulgativa más que para la defensa metodológica.

**✅ Sheppard, S. (1999). Hedonic analysis of housing markets.** En P. Cheshire & E. S. Mills
(Eds.), *Handbook of Regional and Urban Economics*, Vol. 3 (cap. 41, pp. 1595–1635). Elsevier.
DOI: [10.1016/S1574-0080(99)80010-8](https://doi.org/10.1016/S1574-0080(99)80010-8)

> Revisión canónica. Su valor concreto aquí es que documenta **qué atributos aparecen
> sistemáticamente significativos** en mercados de vivienda (accesibilidad, calidad ambiental,
> vecindario, características estructurales), que es exactamente la lista que el post atribuye al
> avalúo. Permite decir "la literatura encuentra recurrentemente X" en vez de afirmarlo sin apoyo.

**✅ Kuminoff, N. V., Parmeter, C. F., & Pope, J. C. (2010). Which hedonic models can we trust to
recover the marginal willingness to pay for environmental amenities?** *Journal of Environmental
Economics and Management*, 60(3), 145–160.
DOI: [10.1016/j.jeem.2010.06.001](https://doi.org/10.1016/j.jeem.2010.06.001)

> El contrapeso honesto. Vía Monte Carlo muestran que la especificación funcional y las variables
> omitidas producen **sesgos grandes** en los precios implícitos estimados. Es la referencia que
> obliga al post a no decir "el avalúo mide el valor de la seguridad": sostiene que el avalúo
> *incorpora* atributos, no que los *cuantifique bien* uno por uno.

**✅ Bishop, K. C., Kuminoff, N. V., Banzhaf, H. S., Boyle, K. J., von Gravenitz, K., Pope, J. C.,
Smith, V. K., & Timmins, C. D. (2020). Best Practices for Using Hedonic Property Value Models to
Measure Willingness to Pay for Environmental Quality.** *Review of Environmental Economics and
Policy*, 14(2), 260–281.
DOI: [10.1093/reep/reaa001](https://doi.org/10.1093/reep/reaa001)

> Consenso metodológico reciente y firmado por buena parte de los autores del área. Sirve para
> acotar el alcance en una frase citable: los modelos hedónicos son creíbles para *capitalización
> de amenidades en precios*, y frágiles para *valoración de bienestar*. Exactamente la distinción
> que el post necesita para no sobrevender su tesis.

---

## 2. Avalúo fiscal vs. valor de mercado: *assessment ratio* y regresividad

Esta es la sección crítica: es la objeción más probable y mejor documentada al post.

**✅🌐 Berry, C. R. (2021). Reassessing the Property Tax.** Working paper, University of Chicago
Harris School of Public Policy. SSRN.
DOI: [10.2139/ssrn.3800536](https://doi.org/10.2139/ssrn.3800536) ·
[SSRN 3800536](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3800536)

> ✅ registro CrossRef confirmado; 🌐 fecha de circulación (9 de marzo de 2021) verificada por
> búsqueda web, **no** por metadatos CrossRef (el registro SSRN no expone fecha). **No encontré
> versión publicada en revista** — citar como working paper.
>
> Es la referencia más contundente del bloque. Con datos de casi todo EE.UU. documenta que la
> regresividad de la tasación es **sistemática y generalizada**, no un defecto local: el decil más
> barato enfrenta un nivel de tasación cerca del **doble** que el decil más caro. Crucialmente,
> atribuye el fenómeno a **limitaciones de datos y método de tasación**, no a error de medición ni
> a decisión política deliberada — que es precisamente el mecanismo que aplicaría al SII, un
> tasador masivo que reavalúa con modelos y no con transacciones individuales. Si el post ignora
> este trabajo, la crítica llegará por aquí.

**✅ Hodge, T. R., McMillen, D. P., Sands, G., & Skidmore, M. (2017). Assessment Inequity in a
Declining Housing Market: The Case of Detroit.** *Real Estate Economics*, 45(2), 237–258.
DOI: [10.1111/1540-6229.12126](https://doi.org/10.1111/1540-6229.12126)
*(publicación impresa abril 2017; versión online 21-01-2016 — verificados ambos campos)*

> El caso extremo y mejor estudiado. Muestra que en mercados **a la baja** la regresividad se
> dispara, porque el avalúo se rezaga respecto del precio y ese rezago pega desproporcionadamente
> abajo. Es directamente transferible al post: en comunas chilenas con mercados deprimidos o poco
> transados, el avalúo se despega del valor precisamente donde el IGVUST marca más vulnerabilidad
> — lo que puede **atenuar artificialmente** la correlación que el post reporta.

**✅ McMillen, D., & Singh, R. (2020). Assessment Regressivity and Property Taxation.** *The
Journal of Real Estate Finance and Economics*, 60(1–2), 155–169.
DOI: [10.1007/s11146-019-09715-x](https://doi.org/10.1007/s11146-019-09715-x)
*(impresa feb. 2020; online 20-07-2019 — verificados ambos campos)*

> Aporte **econométrico**, no sustantivo: advierte que buena parte de la regresividad medida es
> artefacto del estimador. Regresar ratio sobre precio de venta induce sesgo porque el precio
> aparece a ambos lados; proponen enfoques cuantílicos. Es la referencia que el post debe citar
> **si mide regresividad**, y la que lo protege de que le objeten el método. También justifica no
> intentar medir regresividad sin datos de transacciones.

**📄 International Association of Assessing Officers (IAAO). *Standard on Ratio Studies*.**
[PDF oficial](https://www.iaao.org/wp-content/uploads/Standard_on_Ratio_Studies.pdf)
*(URL verificada: HTTP 200, application/pdf, ~2,2 MB)*

> ⚠️ **Año de edición sin verificar.** Confirmé que el PDF existe y descarga, pero no abrí la
> portada para fijar la edición; circulan versiones 2010, 2013 y posteriores y las fuentes
> secundarias las citan indistintamente. **Verificar la edición antes de citar.**
>
> Es el estándar operativo que define los tres estadísticos que el post debería nombrar si toca el
> tema: **COD** (dispersión — uniformidad horizontal), **PRD** (diferencial relacionado con el
> precio) y **PRB** (sesgo relacionado con el precio). Umbrales según fuentes secundarias
> concordantes: PRD aceptable **0,98–1,03**, donde >1,03 indica **regresividad**; PRB aceptable
> **−0,05 a +0,05**, inaceptable fuera de −0,10/+0,10; el PRB se interpreta como el cambio
> porcentual del nivel de tasación cuando el valor se duplica. Valor para el post: existe un
> **estándar profesional internacional** con umbrales numéricos, así que "¿es regresivo el avalúo
> del SII?" es una pregunta con respuesta medible, no una opinión. Y el post puede declarar
> honestamente que **no la respondió**, por carecer de precios de transacción.

**✅ Hodge, T. R., Komarek, T. M., & McAllister, A. (2024). A Double Negative: Capitalizing on
Assessment Regressivity.** *Public Finance Review*, 53(6), 752–785.
DOI: [10.1177/10911421241280456](https://doi.org/10.1177/10911421241280456)

> Cierra el círculo con la sección 1: la regresividad de la tasación **se capitaliza** en los
> precios, o sea el error de tasación entra al mercado y se vuelve parte del valor observado. Si
> el post quiere ser fino, esto implica que avalúo y valor no son dos magnitudes independientes
> donde una aproxima a la otra, sino que **se contaminan mutuamente**. Es un matiz sofisticado y
> defendible.

**✅ Carbonnier, C. (2023). Property Tax Regressivity, the Case of Québec.** *Public Finance
Review*, 52(2), 155–181.
DOI: [10.1177/10911421231212354](https://doi.org/10.1177/10911421231212354)

> Sirve a un solo propósito, pero importante: demuestra que la regresividad **no es una rareza
> estadounidense**. Bloquea la réplica fácil de "esa literatura es de EE.UU., acá el SII funciona
> distinto". No sustituye evidencia chilena, que sigue faltando (ver §8).

---

## 3. Índices compuestos de vulnerabilidad

**📄 Ministerio de Desarrollo Social y Familia. *Informe de resultados IGVUST*.** Sistema de
Indicadores de Vulnerabilidad Socioterritorial (SIVUST). Banco Integrado de Datos (BIDAT).
[PDF](https://bid-ckan-dataset.ministeriodesarrollosocial.gob.cl/dataset/ce0a80ce-e7e8-4014-a00b-23f00d93d8f1/resource/6c71d287-d441-4641-8a5a-3c48b0fd2d31/download/informe-de-resultados-igvust.pdf)

> **Fuente primaria del propio índice.** Descargué y extraje el texto. Verbatim verificado:
>
> > "Para poder construir el índice global, los **18 indicadores** contenidos en las **7
> > dimensiones** que lo componen deben multiplicarse, cada uno, por su respectivo ponderador.
> > Estos coeficientes son **producto de un análisis factorial** que toma en cuenta la naturaleza
> > de los datos tratados."
>
> Esto confirma de primera mano dos cosas que el post necesita: (a) el IGVUST es una **agregación
> lineal ponderada** de 18 indicadores en 7 dimensiones, y (b) **los pesos salen de análisis
> factorial**, no de juicio experto ni de pesos iguales. Es exactamente la construcción que la
> literatura de §3 somete a crítica, y permite escribir la advertencia con conocimiento del
> objeto en vez de en abstracto.
>
> ⚠️ **Fecha del informe sin verificar** — no aparece en las páginas que extraje; el documento
> cita fuentes de 2024 y 2025. Verificar antes de citar con año.

**✅ OECD & Joint Research Centre. (2008). *Handbook on Constructing Composite Indicators:
Methodology and User Guide*.** OECD Publishing.
DOI: [10.1787/9789264043466-en](https://doi.org/10.1787/9789264043466-en)
*Versión working paper: Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A., &
Giovannini, E. (2005). OECD Statistics Working Papers.* ✅
DOI: [10.1787/533411815016](https://doi.org/10.1787/533411815016)

> El manual que el post cita para justificar sus reservas. Lo relevante no es que exista, sino sus
> advertencias concretas: la **normalización y la ponderación son decisiones no neutrales**, la
> **agregación lineal impone sustituibilidad perfecta** entre dimensiones (una buena escuela
> "compensa" una mala vivienda, cosa que nadie defendería explícitamente), y todo índice compuesto
> debe acompañarse de **análisis de sensibilidad**. Aplicado al IGVUST: sus 18 indicadores se
> suman ponderadamente, luego la compensación entre dimensiones **está asumida por construcción**.

**✅ Saisana, M., Saltelli, A., & Tarantola, S. (2005). Uncertainty and Sensitivity Analysis
Techniques as Tools for the Quality Assessment of Composite Indicators.** *Journal of the Royal
Statistical Society Series A: Statistics in Society*, 168(2), 307–323.
DOI: [10.1111/j.1467-985X.2005.00350.x](https://doi.org/10.1111/j.1467-985X.2005.00350.x)

> La versión formal y citable del argumento anterior. Muestra empíricamente que **los rankings de
> índices compuestos se mueven mucho** al variar supuestos de normalización, ponderación y
> agregación. Es la referencia exacta para advertir que el **cuartil IGVUST de una UV concreta no
> es un dato duro**, sino condicionado a decisiones metodológicas — advertencia obligatoria si el
> post muestra UV individuales en un mapa.

**✅ Cutter, S. L., Boruff, B. J., & Shirley, W. L. (2003). Social Vulnerability to Environmental
Hazards.** *Social Science Quarterly*, 84(2), 242–261.
DOI: [10.1111/1540-6237.8402002](https://doi.org/10.1111/1540-6237.8402002)

> El SoVI, referente internacional de índices de vulnerabilidad territorial construidos por
> **análisis factorial** — el mismo método que el IGVUST. Aporta genealogía (el IGVUST no es una
> invención local sino una familia metodológica con 20 años de recorrido) y también la crítica
> heredada: los factores son **estadísticos, no teóricos**, y su interpretación sustantiva es
> siempre discutible.

---

## 4. Medidas de desigualdad y descomposición

**⚠️ Theil, H. (1967). *Economics and Information Theory*.** North-Holland, Amsterdam.

> **Sin verificar por CrossRef**: la API sólo indexa *reseñas* del libro (p. ej. en *OR* 1967 y
> *Econometrica* 1969), no el libro. Editorial y año son de memoria. **Verificar contra catálogo
> antes de citar.**
>
> Origen del índice. Su aporte conceptual al post es que el índice de Theil es una medida de
> **entropía**: cuantifica cuánta información se pierde al asumir que el avalúo se reparte
> uniformemente. Esa lectura es mucho más comunicable en divulgación que "medida de desigualdad".

**✅ Bourguignon, F. (1979). Decomposable Income Inequality Measures.** *Econometrica*, 47(4),
901–920†.
DOI: [10.2307/1914138](https://doi.org/10.2307/1914138)

**✅ Shorrocks, A. F. (1980). The Class of Additively Decomposable Inequality Measures.**
*Econometrica*, 48(3), 613–625†.
DOI: [10.2307/1913126](https://doi.org/10.2307/1913126)

> Este par es el que **autoriza** la descomposición del post. Resultado clave: dentro de las
> medidas que cumplen los axiomas razonables, la **única familia aditivamente descomponible** en
> intra + inter grupo sin término residual es la de **entropía generalizada** (a la que pertenece
> Theil). Corolario directo y defensivo para el post: **el Gini no admite esa descomposición
> limpia** — al descomponerlo por subgrupos con solapamiento aparece un término de traslape
> irreducible. Es decir, reportar Gini = 0,7265 *y* descomponer con Theil no es incoherencia: es
> exactamente lo que la teoría exige. Conviene decirlo en el post, porque parece un desliz y no lo
> es.

**✅ Shorrocks, A. F. (1984). Inequality Decomposition by Population Subgroups.** *Econometrica*,
52(6), 1369–1385†.
DOI: [10.2307/1913511](https://doi.org/10.2307/1913511)

> **La referencia más importante de todo el documento para el hallazgo central del post.** Trata
> formalmente qué pasa al **cambiar la partición**. Y de aquí sale una corrección que el post
> necesita antes de publicar: si las comunas están **anidadas** dentro de las regiones, entonces
> refinar la partición (16 regiones → ~345 comunas) hace que el componente *entre grupos*
> **aumente necesariamente**, porque la desigualdad entre comunas de una misma región pasa de
> contarse como "intra" a contarse como "inter". Que el inter-grupo suba de **19,0% (regiones) a
> 56,9% (comunas)** es entonces, en buena parte, **una identidad algebraica, no un descubrimiento
> empírico**. El post **no debería** presentarlo como "se invierte", que sugiere un hallazgo
> sustantivo. La formulación defendible es: *la desigualdad es sobre todo intra-regional pero
> inter-comunal, y esa diferencia es en gran medida un efecto mecánico de la escala de agregación*
> — lo cual, bien contado, **refuerza** el argumento MAUP en vez de debilitarlo. Ver §9.

**✅ Cowell, F. A. (2011). *Measuring Inequality* (3.ª ed.).** Oxford University Press. (LSE
Perspectives in Economic Analysis).
DOI: [10.1093/acprof:osobl/9780199594030.001.0001](https://doi.org/10.1093/acprof:osobl/9780199594030.001.0001)

> Manual de referencia y la cita más práctica de las cinco: cubre Gini, Theil, entropía
> generalizada y descomposición en un solo lugar y con notación consistente. Es la que conviene
> citar en un post de divulgación cuando se quiere una sola fuente que el lector pueda consultar
> sin acceso a *Econometrica*.

---

## 5. Problema de la unidad areal modificable (MAUP)

**✅ Gehlke, C. E., & Biehl, K. (1934). Certain Effects of Grouping upon the Size of the
Correlation Coefficient in Census Tract Material.** *Journal of the American Statistical
Association*, 29(185A), 169–170.
DOI: [10.1080/01621459.1934.10506247](https://doi.org/10.1080/01621459.1934.10506247)
*(existe además el registro JSTOR paralelo [10.2307/2277827](https://doi.org/10.2307/2277827),
29(185), p. 169)*

> El hallazgo original, 45 años antes de que el problema tuviera nombre: al agregar tractos
> censales en unidades mayores, **la correlación crece**. Aporte concreto al post: cualquier
> correlación avalúo–IGVUST que se reporte **depende del nivel de agregación**, y este trabajo lo
> muestra desde 1934. Excelente para abrir la sección MAUP con una anécdota histórica.

**🌐 Openshaw, S., & Taylor, P. J. (1979). A million or so correlation coefficients: three
experiments on the modifiable areal unit problem.** En N. Wrigley (Ed.), *Statistical Applications
in the Spatial Sciences* (pp. 127–144). Pion, London.

> **Sin DOI** (capítulo pre-DOI; no está en CrossRef). Datos verificados por concordancia entre
> Semantic Scholar, SciSpace y CiNii. El artículo que **acuña el término MAUP**. Construyen
> agregaciones alternativas de las mismas unidades base y obtienen correlaciones que barren
> prácticamente **todo el rango de −1 a +1** con los mismos datos subyacentes. Es la cita
> demoledora para el post: la elección de zonificación puede fabricar casi cualquier resultado, y
> las UV son una zonificación que el analista **no eligió pero tampoco controla**.

**📄 Openshaw, S. *The Modifiable Areal Unit Problem*.** Concepts and Techniques in Modern
Geography (CATMOG) No. 38. Geo Books, Norwich. ISSN 0306-6142 · ISBN 0 86094 134 5.
[PDF](https://www.uio.no/studier/emner/sv/iss/SGO9010/openshaw1983.pdf)

> Descargué el PDF y extraje la portada. Verificados textualmente: título, autor, serie **No. 38**,
> ISSN, ISBN y pie de imprenta ("Published by Geo Books. Norwich—Printed by Headley Brothers Ltd.
> Kent").
>
> ⚠️ **El año NO aparece en la portada.** Se cita habitualmente como **1984**, la copia que
> circula está nombrada `openshaw1983`, y el texto interno referencia hechos de **marzo de 1983**
> (por lo que no puede ser anterior a 1983). **Citar como 1983 o 1984 requiere comprobación en
> catálogo; no afirmar un año sin verificarlo.**
>
> Es el tratamiento monográfico y el más citable en divulgación, porque separa con claridad los
> **dos efectos**: el de **escala** (cambia el tamaño de las unidades) y el de **zonificación**
> (mismo número de unidades, distinto trazado). El post sufre los dos a la vez.

**✅ Fotheringham, A. S., & Wong, D. W. S. (1991). The Modifiable Areal Unit Problem in
Multivariate Statistical Analysis.** *Environment and Planning A*, 23(7), 1025–1044.
DOI: [10.1068/a231025](https://doi.org/10.1068/a231025)

> Extiende el MAUP más allá de correlaciones bivariadas: muestra que en análisis multivariado los
> parámetros son **impredecibles** ante cambios de zonificación — ni siquiera se puede anticipar
> la dirección del sesgo. Es la referencia que impide al post decir "el MAUP probablemente
> subestima/sobreestima": lo honesto es decir que **no se sabe**.

**✅ Robinson, W. S. (1950). Ecological Correlations and the Behavior of Individuals.** *American
Sociological Review*, 15(3), 351–357†.
DOI: [10.2307/2087176](https://doi.org/10.2307/2087176)

> La **falacia ecológica**, primo hermano del MAUP y riesgo directo aquí: el post relaciona
> avalúo *de UV* con vulnerabilidad *de UV*, y de ahí **no se sigue** nada sobre predios ni
> personas. Una UV de alto avalúo promedio puede contener hogares muy vulnerables. Debe declararse
> explícitamente.

---

## 6. Agregación areal: el prorrateo geométrico

*Tema no pedido en el índice original, pero es la operación central del post — 10,3 millones de
predios repartidos a UV por intersección de polígonos — y tiene literatura propia. Sin esto, la
crítica metodológica más directa queda sin respuesta.*

**✅ Goodchild, M. F., Anselin, L., & Deichmann, U. (1993). A Framework for the Areal
Interpolation of Socioeconomic Data.** *Environment and Planning A*, 25(3), 383–397.
DOI: [10.1068/a250383](https://doi.org/10.1068/a250383)

> El marco formal de lo que hace el post. Distingue el **areal weighting** simple (repartir
> proporcional al área intersectada, que es el prorrateo geométrico usado) de métodos que emplean
> información auxiliar. Aporte crítico: el areal weighting asume **homogeneidad interna** de la
> unidad de origen; cuando el atributo se distribuye de forma desigual dentro del polígono, el
> reparto introduce error. Para avalúo predial esto importa menos que para población (el predio es
> pequeño y su avalúo es un atributo puntual), y **el post puede argumentar eso a su favor** — pero
> debe argumentarlo, no darlo por obvio.

**✅ Tobler, W. R. (1979). Smooth Pycnophylactic Interpolation for Geographical Regions.**
*Journal of the American Statistical Association*, 74(367), 519–530.
DOI: [10.1080/01621459.1979.10481647](https://doi.org/10.1080/01621459.1979.10481647)

> Introduce la condición **picnofiláctica**: la interpolación debe **preservar la masa total** de
> cada unidad de origen. Es el criterio de validación que el post debería reportar explícitamente:
> ¿la suma de avalúo prorrateado a las UV reproduce el avalúo total del SII? Dado que un **2,88%**
> de los predios no cae en ninguna UV, la respuesta es **no**, y el post ya lo sabe — Tobler da el
> vocabulario técnico para declararlo con precisión en vez de como anomalía.

**✅ Flowerdew, R., & Green, M. (1992). Developments in areal interpolation methods and GIS.**
*The Annals of Regional Science*, 26(1), 67–78.
DOI: [10.1007/BF01581481](https://doi.org/10.1007/BF01581481)

> Panorama de alternativas al reparto proporcional al área. Su utilidad para el post es acotada
> pero real: permite decir "se usó el método más simple, existiendo otros" — lo que **es** una
> limitación declarable, y declararla desarma la objeción antes de que llegue.

---

## 7. Coropletas bivariadas

**✅ Meyer, M. A., Broome, F. R., & Schweitzer, R. H. (1975). Color Statistical Mapping by the
U.S. Bureau of the Census.** *The American Cartographer*, 2(2), 101–117.
DOI: [10.1559/152304075784313250](https://doi.org/10.1559/152304075784313250)

> **El origen documentado de la coropleta bivariada**, y confirma la intuición del brief: nace en
> el **US Census Bureau**, en los mapas bivariados del atlas censal de los años 70. Es la cita
> correcta para la frase "esta técnica viene de…", en vez de atribuirla a fuentes secundarias
> recientes de divulgación.

**✅ Olson, J. M. (1981). Spectrally Encoded Two-Variable Maps.** *Annals of the Association of
American Geographers*, 71(2), 259–276.
DOI: [10.1111/j.1467-8306.1981.tb01352.x](https://doi.org/10.1111/j.1467-8306.1981.tb01352.x)

> ⚠️ **Corrección al brief.** El encargo pedía "Stevens y Olson". La referencia **académica** de
> Olson es ésta (1981); existe además un trabajo previo suyo de 1975 sobre organización del color
> en mapas de dos variables (actas de Auto-Carto), que **no verifiqué y no está en CrossRef**. Y
> "Stevens" corresponde con alta probabilidad a **Joshua Stevens**, autor del artículo web de 2015
> que popularizó la técnica: es una fuente **divulgativa/práctica, no académica** — perfectamente
> citable como tal, pero **no como respaldo académico**. No la incluyo como referencia verificada.
>
> El aporte de Olson: evalúa **empíricamente** si los lectores logran descodificar mapas de dos
> variables, y encuentra que depende críticamente del diseño del esquema de color y de la leyenda.

**✅ Wainer, H., & Francolini, C. M. (1980). An Empirical Inquiry concerning Human Understanding
of Two-Variable Color Maps.** *The American Statistician*, 34(2), 81–93.
DOI: [10.1080/00031305.1980.10483006](https://doi.org/10.1080/00031305.1980.10483006)

> **La crítica más dura y la más necesaria para el post.** Testean los mapas bivariados del propio
> Census Bureau y concluyen que los lectores **fracasan** en recuperar la información bivariada:
> las leyendas de dos dimensiones resultan esencialmente indescifrables para el lector medio. Es
> la referencia obligatoria si el post usa una malla **4×4 = 16 colores**, que está en o por
> encima del límite razonable. Justifica acompañar el mapa con mapas univariados o con lectura
> guiada, y decirlo abiertamente.

**✅ Brewer, C. A., & Pickle, L. (2002). Evaluation of Methods for Classifying Epidemiological
Data on Choropleth Maps in Series.** *Annals of the Association of American Geographers*, 92(4),
662–681.
DOI: [10.1111/1467-8306.00310](https://doi.org/10.1111/1467-8306.00310)

> Evidencia experimental sobre **métodos de corte en clases** (cuantiles, natural breaks, etc.) y
> su efecto en la lectura. Pertinente porque el post usa **cuartiles** en ambos ejes: es una
> decisión de clasificación con consecuencias, no una operación neutra, y su interacción con
> distribuciones muy asimétricas —como el avalúo, Gini 0,7265— merece mención.

**✅ Eyton, J. R. (1984). Complementary-Color, Two-Variable Maps.** *Annals of the Association of
American Geographers*, 74(3), 477–490.
DOI: [10.1111/j.1467-8306.1984.tb01469.x](https://doi.org/10.1111/j.1467-8306.1984.tb01469.x)

> Complementario y opcional. Propone construir el esquema bivariado con colores complementarios
> para maximizar discriminabilidad. Útil sólo si el post quiere justificar **por qué** eligió su
> paleta; prescindible si no.

---

## 8. Chile: impuesto territorial, unidades vecinales y estudios territoriales

**📄 Cavada Herrera, J. P. (2025, abril). *Impuesto Territorial: Historia, aspectos generales,
forma de cálculo y exenciones*.** Biblioteca del Congreso Nacional de Chile, Asesoría Técnica
Parlamentaria. 29 pp.
[PDF](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio%2F10221%2F37065%2F2%2FImpuesto_Territorial_2025_aspectos_generales_EDIT_PA.pdf)

> Descargado y extraído; autor, fecha y contenido verificados en el propio documento. Es la mejor
> fuente institucional única para la sección chilena del post. Datos verificados directamente:
>
> - La norma vigente es la **Ley N° 17.235, de 1969**, sobre Impuesto Territorial, contenida en el
>   **DFL N° 1, de 1998, del Ministerio de Hacienda** (texto refundido, coordinado y sistematizado).
> - Los **reavalúos son cada 4 años** desde enero de 2014.
> - Tasas: **1% anual** bienes raíces agrícolas, **1,4%** no agrícolas (con sobretasas en varios
>   casos).
> - Recaudación: **40%** ingreso propio municipal / **60%** al Fondo Común Municipal (35/65 para
>   Santiago, Providencia, Las Condes y Vitacura).
> - **Dato de alto valor para el post:** el documento lista **nueve leyes que han pospuesto
>   reavalúos** que correspondía aplicar — Leyes 19.000 (1990), 19.182 (1992), 19.259 (1993),
>   19.380 (1995), 19.468 (1996), 20.002 (2005), 20.455 (2010), 20.650 (2012) y 20.731 (2014).
>   Esto es evidencia **chilena y oficial** de que el avalúo se desactualiza por decisión
>   legislativa recurrente, lo que ataca directamente la tesis "avalúo ≈ valor territorial". Debe
>   entrar en los límites (§9).

**🌐 Ley N° 17.235, sobre Impuesto Territorial** (texto refundido: DFL N° 1 de 1998, Ministerio de
Hacienda). Biblioteca del Congreso Nacional.
URL probable: `https://www.bcn.cl/leychile/navegar?idNorma=28849`

**🌐 Ley N° 19.418, sobre Juntas de Vecinos y demás Organizaciones Comunitarias** (texto refundido:
DTO 58 de 1997, Ministerio del Interior — `idNorma=70040`). Biblioteca del Congreso Nacional.
URL probable: `https://www.bcn.cl/leychile/navegar?idNorma=30785`

> ⚠️ **Las dos URL están sin verificar de primera mano.** BCN LeyChile es una aplicación JS que
> devuelve **HTTP 401** a acceso programático y no renderiza en el recuperador. Los `idNorma`
> provienen de títulos indexados por buscador ("Ley Chile - Ley 17235…", "Ley Chile - Ley 19418…"),
> que es evidencia razonable pero **no confirmación**. **Abrir ambas en navegador antes de
> publicar.** El *contenido* sustantivo de la Ley 17.235, en cambio, sí está verificado vía el
> documento BCN anterior.
>
> Lo que aporta la **Ley 19.418** es el núcleo del hallazgo del post sobre el 2,88%: define la
> Unidad Vecinal como **"el territorio jurisdiccional de una Junta de Vecinos"**, que debe
> corresponder al *"pueblo, barrio, población, sector o aldea en que conviven los vecinos"* — es
> decir, se define por **agrupación vecinal efectiva**, y su delimitación queda entregada al
> municipio considerando continuidad física y juntas preexistentes. **Por construcción legal, las
> UV no teselan el territorio nacional**: donde no hay vecinos organizados, no hay UV. Que en
> comunas mineras y patagónicas el 100% de los predios quede fuera no es un error del cruce: es la
> ley funcionando como está escrita. Esta es la mejor cita del post y conviene citarla textual.

**✅ Agostini, C. A., & Palmucci, G. A. (2008). The Anticipated Capitalisation Effect of a New
Metro Line on Housing Prices.** *Fiscal Studies*, 29(2), 233–256.
DOI: [10.1111/j.1475-5890.2008.00074.x](https://doi.org/10.1111/j.1475-5890.2008.00074.x)

> **Precios hedónicos aplicados a Chile**, y el puente empírico que le faltaba a la tesis del
> post: muestra que en Santiago la accesibilidad (una nueva línea de Metro) **se capitaliza en el
> precio de la vivienda**, y que lo hace incluso de forma anticipada. Es la evidencia local de que
> el mecanismo hedónico opera en el mercado chileno, no sólo en la teoría ni sólo en el Norte
> global.

**✅ Agostini, C. A., Hojman, D., Román, A., & Valenzuela, L. (2016). Segregación residencial de
ingresos en el Gran Santiago, 1992-2002: una estimación robusta.** *EURE (Santiago)*, 42(127),
159–184.
DOI: [10.4067/S0250-71612016000300007](https://doi.org/10.4067/S0250-71612016000300007)

> El antecedente metodológico más cercano al post en la literatura chilena: medición de
> segregación por ingresos con atención explícita a la **robustez frente a la escala de las
> unidades territoriales**. Es la referencia que permite situar el trabajo del post en una
> tradición existente en vez de presentarlo como ejercicio aislado, y donde comparar órdenes de
> magnitud.

**✅ Sabatini, F., Cáceres, G., & Cerda, J. (2001). Segregación residencial en las principales
ciudades chilenas: Tendencias de las tres últimas décadas y posibles cursos de acción.** *EURE
(Santiago)*, 27(82).
DOI: [10.4067/S0250-71612001008200002](https://doi.org/10.4067/S0250-71612001008200002)
*(CrossRef no expone rango de páginas para este registro)*

> El trabajo fundacional sobre segregación residencial chilena y el más citado del área. Aporta el
> marco interpretativo: la segregación en Chile combina **alta concentración a gran escala** con
> creciente heterogeneidad a escala fina — patrón que es exactamente lo que el post observa al ver
> desigualdad predominantemente intra-regional pero inter-comunal.

> **Vacío detectado:** no encontré estudios que usen **avalúo fiscal del SII** como fuente para
> análisis territorial o de segregación en Chile. Si se confirma tras búsqueda en SciELO y
> repositorios institucionales, **es un argumento de originalidad para el post** — pero conviene
> enunciarlo con prudencia ("no encontramos"), no como certeza.

---

## 9. Límites que la literatura obliga a declarar

Cada punto es una advertencia que el post debe incluir explícitamente, con su respaldo.

**1. El avalúo fiscal es regresivo respecto del valor de mercado, y eso sesga el cruce.**
*(Berry 2021; Hodge et al. 2017; McMillen & Singh 2020; IAAO)*
Las propiedades baratas tienden a estar **sobre-tasadas** respecto de las caras. Si eso ocurre en
Chile, el avalúo **comprime** la desigualdad real: el Gini de 0,7265 sería un **piso**, no una
estimación centrada. El post no puede verificarlo porque **no dispone de precios de transacción**,
y debe decirlo. Además, Hodge et al. (2017) implica que el sesgo es **peor donde el mercado está
deprimido** — o sea, correlacionado con el propio IGVUST, que es el peor escenario posible para un
cruce: no es ruido, es sesgo alineado con la variable de interés.

**2. El avalúo se desactualiza por ley, no sólo por rezago técnico.**
*(BCN / Cavada 2025 — verificado en documento oficial)*
Nueve leyes han pospuesto reavalúos desde 1990. Un avalúo "vigente" puede reflejar un mercado de
varios años atrás, y el rezago no se distribuye de forma neutra en el territorio. Es evidencia
chilena, oficial y difícil de refutar; **omitirla sería la falla más evitable del post.**

**3. MAUP: el resultado depende de unidades que nadie diseñó para esto.**
*(Openshaw & Taylor 1979; Openshaw CATMOG 38; Fotheringham & Wong 1991; Gehlke & Biehl 1934)*
Las UV varían enormemente en superficie y población, y su trazado responde a organización vecinal
histórica, no a criterio estadístico. Openshaw y Taylor mostraron que zonificaciones alternativas
de los mismos datos generan correlaciones que cubren casi todo el rango posible. Fotheringham y
Wong agregan que en análisis multivariado **ni siquiera se puede predecir la dirección del sesgo**.
El post debe declarar que sus cifras son **condicionales a la malla UV** y no propiedades del
territorio chileno.

**4. La inversión del Theil entre región y comuna es, en buena medida, mecánica.**
*(Shorrocks 1984; Bourguignon 1979)*
**Corrección de fondo, no matiz de redacción.** Si las comunas están anidadas en las regiones,
pasar a una partición más fina **necesariamente** aumenta el componente inter-grupo, porque la
desigualdad entre comunas de una misma región se reclasifica de "intra" a "inter". El salto de
19,0% a 56,9% es en gran parte **una identidad**, no un hallazgo. Recomendación concreta: no
escribir "se invierte" como si fuera un descubrimiento; escribir que la desigualdad es
**intra-regional pero inter-comunal**, y usarlo como **ilustración didáctica del MAUP** — que es
un uso legítimo, honesto y de hecho más interesante. Complemento útil: aclarar que el **Gini no es
aditivamente descomponible** (Bourguignon; Shorrocks 1980), lo que explica por qué se usó Theil
para descomponer y Gini sólo como nivel.

**5. Los cuartiles del IGVUST no son comparables entre grupos — y lo dice la propia fuente.**
*(Informe IGVUST, MDSF — verbatim verificado)*
El informe oficial señala textualmente:

> "**Nota 2:** Los cuartiles asignados son válidos exclusivamente para la región analizada, por lo
> que **no es posible establecer comparaciones directas con comunas o UV de otras regiones**."

El productor del índice **ya declaró** el límite. A esto se suma lo que observó el post: los
cuartiles son **equipoblados en UV, no en personas** — el cuartil más vulnerable concentra 25% de
las UV pero sólo 12,5% de la población. Se sigue que **"cuartil 4" no significa lo mismo en dos
regiones distintas**, y que cualquier lectura per cápita a partir de cuartiles de UV está mal
planteada. Citar la Nota 2 textual es la jugada más fuerte disponible: es el límite reconocido por
la fuente, no una objeción externa.

**6. Falacia ecológica: nada de esto habla de personas ni de predios.**
*(Robinson 1950)*
Todas las relaciones son entre **agregados de UV**. Una UV con avalúo promedio alto puede contener
hogares muy vulnerables, y viceversa. El post no puede concluir nada sobre hogares individuales.

**7. El IGVUST es un constructo, no una medición.**
*(OECD/JRC 2008; Saisana et al. 2005; Cutter et al. 2003; Informe IGVUST)*
Verificado en la fuente: 18 indicadores, 7 dimensiones, **ponderadores por análisis factorial**,
**agregación lineal**. Eso impone **sustituibilidad perfecta entre dimensiones** por construcción
(mejor acceso "compensa" peor vivienda), y los rankings de índices compuestos son **sensibles a
esas decisiones**. El cuartil de una UV concreta no es un dato duro.

**8. El 2,88% fuera de UV no es error: es el diseño legal — pero sesga la muestra.**
*(Ley 19.418; Tobler 1979; Goodchild et al. 1993)*
Las UV son territorios jurisdiccionales de juntas de vecinos, no una teselación. Ahora bien, para
el análisis esto **sí** tiene consecuencia: la pérdida **no es aleatoria** — se concentra en
comunas mineras y patagónicas, donde llega al 100%. El universo efectivamente analizado está
**sesgado hacia lo urbano organizado**, y la condición picnofiláctica de Tobler no se cumple.
Declarar el porcentaje **y su distribución territorial**, no sólo el promedio nacional.

**9. Los mapas bivariados 4×4 están en el límite de lo legible.**
*(Wainer & Francolini 1980; Olson 1981; Brewer & Pickle 2002)*
Wainer y Francolini encontraron que los lectores **fracasan** en descodificar mapas bivariados del
Census Bureau. Con 16 colores el post está en la frontera superior. Mitigación recomendable:
acompañar con mapas univariados, leyenda explicada en prosa, y no apoyar ninguna afirmación
central **exclusivamente** en la lectura del mapa bivariado.

---

## Anexo — Hallazgos que afectan al texto del post

Detectados al verificar; conviene resolverlos antes de publicar.

1. **Discrepancia en el número de UV.** El brief indica **6.891** UV. El informe oficial del
   IGVUST señala textualmente: *"A nivel nacional, existen **6.887** Unidades Vecinales"*
   (atribuido a Ministerio de Desarrollo Social y Familia, 2025). Diferencia de 4 unidades.
   Probablemente vintages distintos de la capa, pero **el post debe declarar la fuente y fecha de
   corte de su capa UV**, porque la cifra oficial es citable y no coincide.

2. **"Se invierte" (Theil) es una sobreafirmación.** Ver §9.4. Es la corrección de mayor impacto
   de este documento.

3. **"Stevens y Olson"** mezcla una fuente divulgativa (Joshua Stevens, 2015, web) con una
   académica (Olson, 1981). El origen académico real de la técnica es Meyer, Broome & Schweitzer
   (1975), US Census Bureau — que **sí** coincide con la intuición del brief.

4. **Verificar antes de publicar:** edición del *Standard on Ratio Studies* de IAAO; año del
   CATMOG 38 de Openshaw (1983 vs. 1984); año del informe IGVUST; datos editoriales de Theil
   (1967); y las dos URL de BCN LeyChile.

5. **Se añadió §6 (agregación areal)**, no contemplada en el encargo. El prorrateo geométrico es
   la operación central del post y tiene literatura propia; sin ella, la objeción "¿cómo repartiste
   10,3 millones de predios?" queda sin respuesta bibliográfica.

---

*Referencias: 31 ítems. Verificadas contra CrossRef: 25. Verificadas por recuperación del documento
primario: 4. Verificadas sólo por búsqueda web: 2 (Openshaw & Taylor 1979; URLs BCN). Sin verificar,
marcadas como tales: Theil (1967) datos editoriales, edición IAAO, año CATMOG 38, fecha informe
IGVUST, Olson (1975).*
