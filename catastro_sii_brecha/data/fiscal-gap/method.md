# Avalúos II: método, fuentes y errata

## Qué mide la comparación

Una diferencia entre viviendas particulares del Censo 2024 y roles habitacionales del SII (código de destino H) 2026S1. Una vivienda es una unidad censal; un rol identifica un bien raíz. No existe aquí un enlace individual que permita identificar viviendas sin rol. Viviendas vacantes también cuentan; viviendas rurales pueden estar en predios de destino agrícola. Copropiedad, roles matrices, subdivisiones y destino preferente pueden romper la correspondencia uno a uno.

La tabla conserva todas las comunas, diferencias negativas y fuentes ausentes. El gráfico físico muestra las 15 mayores brechas positivas restantes tras el supuesto de campamentos, entre comunas cubiertas. El modelo monetario adicional ordena otro conjunto: comunas con residuo positivo y mediana de avalúo observado sobre el umbral general, por escenario de impuesto medio calculado por predio. Ninguno es un ranking de evasión, deuda, recursos perdidos ni negligencia.

## Fuentes y fechas

| Fuente | Uso | Alcance |
|---|---|---|
| [INE Censo 2024](https://censo2024.ine.gob.cl/resultados/) | Viviendas particulares por comuna; `tipo_operativo = 2` | 7.638.396; excluye colectivas y situación de calle; hogares concilian con agregado INE |
| [Espejo catastral](https://catastral.cl/) | Extractos 2026S1 descargados 24-07-2026 | 6.054.808 roles habitacionales únicos; también incluye registros sin coordenadas |
| [SII por destino](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html) | Control independiente 2026S1 | 6.056.150 roles habitacionales; diferencia de 1.342 frente al extracto, causa pendiente |
| [SII Producto 3, Resolución 5/2010](https://www.sii.cl/documentos/resoluciones/2010/2010-5.pdf) | Definición del campo catastral semestral | Puede incluir aseo y sobretasas; documentación histórica, requiere confirmar contrato de la extracción actual |
| [SII descarga rol de contribuciones](https://www.sii.cl/entidades_externas/descargarolcontribuciones.htm) | Contraste de definición RC | La cuota trimestral también incluye aseo; no sustituye al neto |
| [Cuenta pública SII 2025](https://www.sii.cl/cuenta_publica/2025/cuenta_publica_2025.pdf) | Control del contraste 2024S2 | 5.856.068 roles habitacionales, coincidencia nacional del archivo histórico |
| [MINVU parque habitacional](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/) | Dos planillas oficiales 2026S1, destino y tramos de avalúo, revisadas 10-09-2026 | 6.057.949 roles habitacionales; las 346 filas comunales concilian entre ambas planillas y con sus totales |
| [SII estadísticas comunales vigentes](https://www.sii.cl/sobre_el_sii/estadisticas/estadisticas_bienes_raices_por_comuna.html) | 16 CSV de carga dinámica, 2026S1, M$ al 01-01-2026 | Componentes para todos los destinos no agrícolas, no para los predios habitacionales separadamente |
| [MINVU, Caracterización de campamentos en Censo 2024](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/) | Autoridad metodológica del cruce georreferenciado MINVU–INE | En la foto 2024: 1.373 campamentos con viviendas ocupadas, 81.993 viviendas, 77.399 hogares y 238.491 personas |
| `CNC_2026.zip`, entregado por la persona usuaria | Polígonos vigentes al 25-05-2026; se publican agregados comunales e imágenes cartográficas sin identificadores | 1.345 polígonos; `HOGARESCAT` suma 82.576; `HOGARESCEN` numérico suma 71.760 y falta en 222 polígonos |
| `BBDD_CNC_innominada-.zip`, entregado por la persona usuaria | Auditoría de compatibilidad; no alimenta el ajuste | Registro histórico 2011–2021 a nivel persona/hogar; no representa el stock comunal vigente de 2026 |

Antártica (CUT 12202) y Trehuaco (16207) no tienen extracto en este conjunto. Su ausencia no acredita cero roles en el SII. Los 1.342 roles habitacionales faltantes del total nacional no se imputan a una comuna sin evidencia. Trehuaco sí tiene 1.276 roles habitacionales en el archivo histórico 2024S2, bajo CONARA 08108; se conserva ese dato separado, sin imputar 2026. El contraste histórico usa 2024S2 y la misma homologación; no identifica fechas de alta ni sigue automáticamente un panel de inmuebles idénticos.

## Campamentos: ajuste de sensibilidad, no nueva verdad

El informe MINVU confirma que el cruce correcto es espacial: superpone polígonos de campamentos y microdatos censales georreferenciados. El CSV público de viviendas que usamos no contiene coordenadas, manzana ni una bandera de campamento. Por eso no intentamos reconstruir ese enlace con el identificador anonimizado de vivienda.

La capa CNC 2026 sí contiene por polígono `HOGARESCEN`, un conteo que interpretamos como hogares del Censo por su nombre y por coherencia con el método publicado. El archivo no trae diccionario de campos. Esta semántica, por tanto, es una inferencia documentada y falsable: se descartará si MINVU publica un diccionario que atribuya al campo otra unidad o fecha.

Para cada comuna calculamos:

$$
D_c = V_{c,2024}-H_{c,2026S1}
$$

$$
D^{sens}_{c}=D_c-C^{obs}_{c}
$$

donde $C^{obs}_{c}$ es la suma numérica de `HOGARESCEN` en los polígonos del CNC 2026. La operación supone, sólo para explorar sensibilidad, que cada hogar censado en campamento explica una vivienda censal que no debiera exigir un rol habitacional separado. No observa ese enlace, no sabe si el terreno tiene rol matriz, no sabe si la vivienda está incorporada como construcción y no sabe si supera el avalúo exento.

La resta reduce la suma de brechas positivas de 1.588.449 a 1.516.689 unidades: 71.760, o 4,52%. Alto Hospicio baja de 15.368 a 6.232; Viña del Mar, de 24.030 a 16.016; Antofagasta, de 21.755 a 14.218. En cambio, Valparaíso conserva 29.961 de 32.533 y Puerto Montt 28.404 de 29.036. Esas diferencias muestran que campamentos son una explicación cuantitativamente importante en algunas comunas, pero no absorben el patrón nacional ni la mayor parte de las brechas grandes.

La capa tiene 222 polígonos con `HOGARESCEN` igual a `S/I` o vacío, repartidos en 95 comunas cubiertas por el espejo. El residuo de esas comunas descuenta sólo lo observado y puede estar sobreestimado respecto del mismo contrafactual. La tabla marca `partial_census_count`; no reemplaza el faltante por cero ni usa `HOGARESCAT` como imputación. Las 153 comunas sin polígono vigente se distinguen de las 96 con conteo completo y de las dos sin fuente de roles.

`HOGARESCAT` no se usa para restar: corresponde a otra medición, suma 82.576 y combina momentos de ingreso 2011, 2019, 2022 y 2024. La divergencia entre el informe 2024, `HOGARESCEN` y `HOGARESCAT` es evidencia de movilidad, actualización y diferencias operativas, no un error corregible eligiendo el número mayor.

## Materialidad censal: descriptor amplio y no identificador de campamento

Reproducimos los indicadores viv04–viv06 del [manual de microdatos INE, pp. 103–106](https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf) en viviendas particulares ocupadas con moradores presentes. Una vivienda es irrecuperable por su tipo —mediagua, mejora, emergencia, rancho, choza, móvil u otro— o por paredes/techo precarios, falta de cubierta sólida o piso de tierra, **siempre después de excluir respuestas desconocidas en el tipo o los materiales**. El total corregido es 72.642 y coincide con la [publicación INE del 30-05-2025](https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/05/30/censo-2024-el-61-1-de-los-hogares-residen-en-una-vivienda-propia-y-el-26-2-en-una-vivienda-arrendada).

No restamos esas 72.642. La materialidad no informa tenencia del suelo, formalidad urbanística, rol matriz ni localización dentro de un campamento. Además, se superpone con los hogares ya contados en `HOGARESCEN`; sumarla produciría doble descuento. Una vivienda en campamento puede tener materialidad aceptable y una vivienda irrecuperable puede estar fuera de un campamento o dentro de un predio formal.

**Errata de materialidad:** la primera versión contaba 73.338 porque aplicaba la condición «algún material precario o tipo irrecuperable» antes de resolver faltantes en otro componente. El código oficial da precedencia a esos faltantes; 696 casos vuelven a desconocidos. No cambia ninguna vivienda censal total, rol habitacional, hogar de campamento ni brecha residual. El indicador de tipo por sí solo conserva 46.517; el de materialidad con respuesta completa da 31.953. Sus universos clasificables son distintos y no se suman para reconstruir viv06.

### Composición hipotética del residuo

La categoría del gráfico es **tipo y tres materiales aceptables, bajo un supuesto de composición**. Exige casa, departamento, vivienda tradicional indígena o pieza —códigos públicos de tipo 1, 3, 5, 6—, paredes 1–3, techo 1–4 y piso 1. En los microdatos públicos las casas 1/2 y departamentos 3/4 del cuestionario se agrupan en 1 y 3 por anonimización; no se excluyen departamentos. «Aceptable» no significa lujo, alto precio, cumplimiento urbanístico ni ausencia de defectos: el Censo no mide aquí superficie construida, conservación, terminaciones, valor del suelo o avalúo fiscal.

Hay una discrepancia interna en la definición viv04 del manual: la prosa de p. 103 acepta ciertas paredes recuperables, pero su código R de p. 104 exige los tres componentes aceptables. También la prosa exige todos los componentes irrecuperables mientras el código usa cualquiera. Seguimos la regla computable R y explicitamos sus códigos; una aclaración posterior del INE obligaría a revisar esta decisión. Se conservan por separado 5.799.969 viviendas con tres materiales aceptables y 5.774.146 con **tipo y materiales** aceptables: las 25.823 restantes son de tipo irrecuperable.

| Referencia observada | Total nacional |
|---|---:|
| Ocupadas con moradores presentes | 6.408.172 |
| Tres materiales con respuesta válida | 6.403.784 |
| Algún material sin respuesta válida | 4.388 |
| Tipo y tres materiales aceptables | 5.774.146 |
| No irrecuperables con tipo y materiales completos | 6.331.142 |

Para cada comuna, $p_c=A_c/O_c$, donde $A_c$ es la cantidad observada de tipo y materiales aceptables, y $O_c$ todas las ocupadas con moradores. Luego se divide el residuo positivo $R_c=\max(D_c-C^{obs}_c,0)$ en $R_c p_c$ y $R_c(1-p_c)$. La segunda parte se llama **resto del residuo**: incluye materiales recuperables, tipos irrecuperables y no respuesta, sin afirmar que sean viviendas precarias. Ambas partes suman exactamente $R_c$; junto con la parte absorbida por campamentos reconstruyen la brecha positiva original. Los valores fraccionarios son equivalentes de vivienda del escenario; se redondean sólo al mostrarlos.

La hipótesis de transferencia supone que la composición del conjunto que eventualmente explique el residuo se parece a la observada en toda la comuna. No hay una muestra enlazada de viviendas sin rol que la valide. Además, el residuo inicial incluye viviendas vacantes, mientras la materialidad sólo se observa en ocupadas; y el grupo de referencia puede incluir campamentos. Esa selección impide tratar $p_c$ como probabilidad individual, prevalencia conocida entre viviendas sin rol o proporción que paga contribuciones.

La robustez compara tres tratamientos: mantener faltantes fuera del numerador principal; excluirlos del denominador (`materiality_acceptable_complete_case_scenario`); y asignarlos todos a aceptable (`materiality_acceptable_missing_upper_scenario`). Este último es un extremo de **no respuesta dentro de la misma hipótesis**, no cota de viviendas omitidas. También se muestra un escenario más amplio basado en no-irrecuperables completos (`non_irrecoverable_scenario`). Sin la hipótesis de transferencia, la fracción aceptable del residuo sólo queda entre 0 y 1. No corresponde un error estándar o intervalo de muestreo: la incertidumbre principal es de identificación y comparabilidad, no de tamaño muestral.

La suma del escenario principal es 1.318.682 equivalentes, de un residuo positivo total de 1.516.689; el resto es 198.007. El escenario de casos completos da 1.319.408 y asignar todos los faltantes a aceptable da 1.319.518. El criterio más amplio de no-irrecuperables completos da 1.492.300. Los tres primeros resultados son próximos porque la no respuesta material es baja; esa estabilidad **no prueba** que la composición sea transferible a viviendas no enlazadas o vacantes.

### Avalúos habitacionales observados para orientar una revisión

El stock residencial `dc_cod_destino='H'` sí tiene `dc_avaluo_fiscal`: 6.054.808 observaciones válidas, ninguna faltante o negativa y 17 valores cero, incluidos en media y mediana. Se usa ese campo administrativo del mismo corte 2026S1, sin filtrar geocodificación ni sustituirlo por campos de la API de otro contrato. La mediana se calcula sobre todos los roles de cada CUT: en Santiago se unen sus tres shards antes de calcularla.

Se informan media, mediana y proporción de roles habitacionales observados con avalúo estrictamente mayor a **$60.030.710**, el monto exento general habitacional que el [ejemplo oficial SII](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf) identifica para 2026S1. La referencia nacional del espejo es media $54.778.847, mediana $35.337.200 y 1.558.841 roles habitacionales sobre ese umbral. No se usan los $61.711.570 de 2026S2 con avalúos del primer semestre. Estar sobre el umbral general tampoco descarta exenciones especiales o rebajas.

El control independiente de avalúo nacional habitacional informa $331.697.870.962.000, frente a $331.675.400.421.251 en el espejo: quedan $22.470.540.749 sin conciliar junto con los 1.342 roles ausentes. Esa diferencia no se distribuye entre comunas ni se transforma en un factor de ajuste. Las estadísticas comunales describen exclusivamente los roles efectivamente disponibles. El selector residuo positivo y mediana sobre umbral entrega 15 comunas, ordenadas por residuo, no por recaudación potencial; Iquique y Puerto Varas apenas superan el umbral en su mediana, por lo que no deben describirse como un salto grande sin informar su magnitud.

Un criterio de revisión transparente es observar dónde coexisten un residuo positivo, una categoría aceptable apreciable bajo el supuesto y una mediana habitacional superior al umbral. Esto selecciona lugares para contrastar predios, sin estimar la probabilidad de que lo ausente tribute. Una media alta por sí sola puede depender de pocos predios extremos; por ello se acompaña de mediana y proporción. Tampoco se multiplican automáticamente las dos proporciones: no observamos la distribución conjunta de materialidad y avalúo del residuo. La revisión debe comprobar primero si existe omisión, cuál es el inmueble imponible, qué valor corresponde y qué exenciones aplican.

| Hipótesis provisional | Evidencia que la discrimina | Condición de descarte |
|---|---|---|
| La composición aceptable del residuo se parece a la comuna | Enlace validado de viviendas/edificaciones a predios y comparación de materialidad entre enlazadas y no enlazadas, incluyendo vacantes y campamentos | Diferencias sustantivas de composición o demostración de que el residuo se explica por unidades ya contenidas en roles existentes |
| En lugares con avalúos habitacionales altos existen omisiones materialmente relevantes | Edificaciones concretas ausentes o ampliaciones no incorporadas, avalúo individual sobre exención y obligación temporal acreditada | Rol existente y construcción incorporada; o avalúo/exenciones que descarten impuesto exigible |
| La media alta señala un contexto extendido de alto avalúo | Mediana y proporción sobre umbral también altas | Media impulsada por pocos casos mientras la mediana y la mayoría quedan bajo el umbral |

## Lectura epistémica y pruebas de descarte

| Clase | Conclusión | Evidencia discriminante o condición de descarte |
|---|---|---|
| Hecho observado | El CNC 2026 contiene 1.345 polígonos, 71.760 hogares Censo numéricos y 222 polígonos sin ese conteo | Cambiar bytes, miembros, filas o totales rompe el build por hash y conciliación |
| Deducción | Restar hogares de campamento sólo puede ser un contrafactual porque las unidades no se enlazan uno a uno | Se volvería ajuste observado únicamente con una llave o enlace espacial validado vivienda–predio–rol |
| Inducción | El supuesto por campamentos reduce una fracción desigual: grande en Alto Hospicio, Viña del Mar y Antofagasta; pequeña en varias líderes | Se refuta si una versión completa y comparable de los polígonos cambia sustantivamente esas participaciones |
| Abducción A | Parte de la brecha proviene de viviendas en asentamientos irregulares | Gana apoyo con enlaces espaciales vivienda–campamento sin rol habitacional; se descarta donde esas viviendas estén dentro de roles matrices o habitacionales existentes |
| Abducción B | Parte proviene de viviendas rurales, copropiedad o roles matrices | Gana apoyo con destino agrícola, copropiedad y relaciones prediales; se descarta con correspondencia uno a uno que siga faltando |
| Abducción C | Parte corresponde a rezago catastral exigible | Requiere fecha de construcción, aviso, obligación, avalúo sobre exención y alta posterior; se descarta si el rol existía o no había obligación |
| Abducción D | Parte es incompatibilidad temporal o error de clasificación/homologación | Gana apoyo al reconstruir cortes equivalentes; se descarta si el patrón persiste con igual fecha, fuente íntegra y claves validadas |

La ilegalidad tampoco implica ausencia permanente de rol. La [Ley 17.235](https://www.bcn.cl/leychile/navegar?i=128563) aplica el impuesto territorial a bienes raíces y el rol identifica el predio, no cada vivienda. Además, el [artículo 16 de la Ley 20.234](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0) dispone que, después de la recepción definitiva y el otorgamiento de escrituras en ciertos loteos irregulares regularizados, el SII asigne rol y avalúo separado. La afirmación «el SII jamás los tendrá» no es compatible con ese procedimiento legal.

## Por qué el impuesto neto observado sigue sin identificarse

El campo DC no separa contribución neta, aseo y sobretasas. Su suma habitacional es 508.919.215.492 CLP; el control SII por destino informa 455.500.163.000 CLP de giro semestral, incluyendo sobretasas. La diferencia de 53.419.052.492 CLP es una discrepancia de conciliación, **no** un cálculo de impuestos omitidos ni un monto de aseo identificado. Estos totales de auditoría no se multiplican por la brecha residencial.

Los PDFs comunales inicialmente consultados de [Los Ríos](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrc_los_rios.pdf) y [RM](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrc_santiago.pdf) corresponden a 2025S2. La revisión del 10-09-2026 encontró los CSV dinámicos vigentes de las 16 regiones: sí corresponden a 2026S1. Sus controles nacionales coinciden: 8.512.452 predios no agrícolas y 1.293.666.863.000 CLP netos semestrales, más sobretasas, con 59.910.165.000 CLP de aseo informados separadamente. Este universo incluye comercio, oficinas, estacionamientos y otros destinos; dividir su neto por los roles habitacionales fabricaría una media residencial. La disponibilidad del período se resuelve, la del universo fiscal habitacional no.

### Qué agrega el control MINVU

Las dos planillas MINVU atribuyen 1.342 roles habitacionales a Trehuaco (escrito «Treguaco») y cero a Antártica. Es evidencia agregada oficial adicional, no una recuperación de los shards faltantes del espejo. El gráfico conserva su extracción única; los valores nuevos se consultan en la [conciliación oficial separada](source-audit.json).

La suma MINVU supera al cuadro nacional SII en 1.799 roles habitacionales. Entre las 344 comunas cubiertas por el espejo hay 208 diferencias positivas y ninguna negativa; suman precisamente 1.799. Calama aporta 420, Lo Barnechea 114 y Concepción 109. Trehuaco aporta otros 1.342 al comparar MINVU con el espejo. Así, la diferencia de totales ya tiene una descomposición comprobable, aunque su causa administrativa sigue pendiente.

Un corte o una revisión posterior del catastro es una hipótesis compatible con el patrón unilateral. Se distinguiría de una diferencia de cobertura o clasificación mediante fechas efectivas, reglas de inclusión y claves de altas/bajas. Se descartaría como explicación temporal si se acredita que ambos extractos comparten fecha y versión, o si las diferencias responden a duplicados o reclasificación. La igualdad de semestre no acredita igualdad de versión. Esta hipótesis no demuestra rezago tributario.

Una vez obtenido el neto: B(q) = max(viviendas − roles habitacionales, 0) × q × media anual equivalente de los roles habitacionales. El equivalente anual duplica el semestre bajo sus mismas condiciones: no es impuesto anual efectivamente girado o cobrado. La media incluye ceros. Media y promedio son el mismo estadístico; la mediana puede ser cero y se mostrará junto a proporción positiva, media y mediana entre positivos.

q = 0, 0,25, 0,5 y 1 son escenarios transparentes. q = 1 no es una omisión observada ni una cota superior real. No se estiman errores estándar de muestreo. La conversión **basada en neto observado** permanecerá nula hasta disponer de una fuente compatible. El modelo general explicado más abajo produce valores adicionales con otro estimando y otros supuestos; no llena esos campos con valores de demostración.

## Errata de identidad territorial del visor anterior

| Comuna INE | CUT | CONARA SII correcto | Recuento habitacional anterior erróneo | Recuento habitacional corregido, mismo extracto anterior |
|---|---|---|---:|---:|
| Coyhaique | 11101 | 11401 | 7.984 | 19.563 |
| Aysén | 11201 | 11101 | 1.801 | 7.984 |
| Chile Chico | 11401 | 11201 | 19.563 | 1.801 |

La tabla oficial CONARA identifica la comuna; los nombres del espejo y el sufijo CUT de algunos archivos estaban intercambiados. Se corrigieron indicadores dependientes y celdas de densidad de esas tres comunas, manteniendo la extracción anterior del visor y su total nacional. El nuevo diagnóstico tiene extracción 24-07-2026 y valores propios; las capas UV y el período del post I no se rehacen.

El metadato principal se actualizó a roles habitacionales / todas las viviendas particulares, que ya era la lectura del visor. El campo histórico `viviendas_ocupadas_censo_2024` sólo contiene viviendas con moradores presentes, no todas las ocupadas; el diccionario ahora lo explicita.

## Mapas de Valparaíso y Puerto Montt

El anexo muestra las dos comunas con mayor brecha restante mediante imágenes de
predios habitacionales del mismo extracto, unidades vecinales de marzo de 2026 y
campamentos CNC de mayo de 2026. El detalle es un recorte urbano; el recuadro
pequeño sitúa ese recorte entre las unidades vecinales comunales. La cifra de brecha
pertenece a toda la comuna y no se atribuye al sector ampliado.

La geometría procede del espejo y puede asociarse por ubicación o proximidad;
no certifica límites legales. Un polígono puede representar varios roles y se
dibuja una vez. Los registros sin geometría no se sustituyen por parcelas inventadas.
El fondo usa calles y aguas OSM locales cuya fecha efectiva de extracción no está
acreditada. La escala y el norte se calculan en WGS 84 / UTM 19S.

El [manifiesto de las imágenes](maps-audit.json) conserva hashes de fuentes y PNG,
conteos comunales y del recorte, métodos de asociación y límites. Sólo se distribuyen
imágenes y evidencia agregada: no vectores prediales, nombres de campamentos,
folios, direcciones ni registros de personas. La superposición no enlaza viviendas
del Censo con roles ni demuestra ausencia de cobro.

## Escenarios monetarios adicionales: regla general por predio

Este modelo **no reconstruye el giro efectivo ni levanta el bloqueo del neto observado**. Añade una pregunta distinta: cuánto representa el residuo si las propiedades que hipotéticamente lo explicaran tuviesen la distribución de avalúos del stock habitacional observado y se aplicara sólo la regla tributaria general.

El [ejemplo oficial SII, válido para 2026S1](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf) fija el monto exento E = $60.030.710, el cambio de tramo T = $214.395.361 y tasas anuales de 0,893% y 1,042%. Para cada avalúo total A se calcula `g(A) = 0,00893 × max(min(A,T) − E, 0) + 0,01042 × max(A − T, 0)`. El ejemplo A = $237.530.004 da $1.619.539,31349 anuales y una cuota redondeada de $404.885. Se excluyen aseo, sobretasas y beneficios o exenciones particulares; por eso no se interpreta como contribución efectiva de ese rol. La regla se congela en el primer semestre: es un equivalente anual y no una liquidación real de todo 2026.

El cálculo se aplica **antes** de promediar o tomar medianas, sin redondear cada predio. Los ceros bajo el umbral forman parte de ambas estadísticas. Las partes administrativas de una comuna se reúnen antes de la agregación; no se promedian medianas de shards. La mediana interpolada también puede cambiar si se transforma después: con avalúos E−10 y E+10, la mediana del avalúo es E y su impuesto es cero, mientras la mediana de los dos impuestos calculados es $0,04465. Un avalúo ausente, negativo o no finito deja sin modelo a toda la comuna; no se usa el promedio de los casos completos como si fuera el del conjunto.

Para el residuo positivo R tras sensibilidad de campamentos se ofrecen **dos escenarios**: `R × mediana(g(A))` y `R × promedio(g(A))`. No se multiplica otra vez por la proporción que supera el umbral, porque los ceros ya participan; tampoco por materialidad aceptable, que no mide tributación. La sensibilidad `q = 0; 0,25; 0,5; 1` se puede aplicar a **ambos** escenarios para variar la fracción hipotética del residuo. El archivo persiste columnas adicionales de q = 0,25 y 0,5 para el promedio; el visor calcula cualquiera de los dos escenarios multiplicando su valor de q = 1. q = 0 significa transferencia nula cuando existe un modelo válido, sin convertir en cero una comuna sin información. q no se estima con los datos; una q común positiva sólo cambia la escala y q = 0 iguala los montos en cero, conservando el orden de referencia.

La transferencia de la distribución observada es un **supuesto**, no una muestra de viviendas sin rol. Viviendas rurales en predios agrícolas, segundas viviendas, subdivisiones, roles matrices, diferencias de fecha y errores censales pueden alterar su pertinencia. La materialidad no corrige esas diferencias ni mide superficie, suelo o exenciones. El rango entre media y mediana no es intervalo de confianza ni límites garantizados: en general la mediana puede superar al promedio. El modelo tampoco localiza qué viviendas generan el residuo.

El ranking `model_ranking` exige fuente completa, residuo positivo y mediana de avalúo observado estrictamente sobre E. Ordena por `modeled_gap_mean_clp`, con empate por CUT normalizado, y muestra hasta 15 comunas. La restricción de mediana alta es un criterio explícito de revisión territorial, no una probabilidad demostrada de que el residuo tribute. El ranking físico conserva sus propias 15 comunas y sus dos anexos: no se sustituyen por los del modelo.

En esta extracción hay 344 comunas con avalúos completos y dos sin fuente. Las 15 priorizadas suman aproximadamente $36.389 millones anuales en el escenario promedio y $13.464 millones en el mediano. El desglose y la evidencia están en `avaluos-ii-modeled-fiscal-evidence-20260911.md`. Son órdenes de magnitud bajo los supuestos anteriores, no recursos municipales retenidos ni deuda cobrable identificada.

La explicación de rezago del catastro se contrastaría con una muestra enlazada que documente viviendas comparables, existencia previa, obligación exigible y falta de incorporación. Se descartaría para los casos explicados por roles existentes, otro destino, exención o diferencia censal. Una distribución de avalúos de las viviendas enlazadas distinta de la observada refutaría la transferencia monetaria usada aquí. La recuperación de los catastros en NFS confirma disponibilidad de avalúos; no identifica por sí sola esas obligaciones.

## Responsabilidad y evidencia necesaria

SII determina avalúos y giros; TGR recauda. Girado y pagado son cantidades distintas. El impuesto territorial participa del Fondo Común Municipal: un peso adicional de impuesto asociado a una comuna no equivale automáticamente a un peso adicional retenido por su municipio. No se estima aquí esa distribución.

Una sospecha de rezago requiere documentar existencia y características del inmueble, correspondencia con el rol, fecha de aviso o información disponible, exigibilidad, exenciones y fecha efectiva de incorporación o actualización. Una brecha agregada sólo prioriza una investigación. Una omisión podría afectar una ampliación de un rol existente sin crear un rol nuevo.

[Datos JSON](communes.json), [CSV](communes.csv), [Parquet](communes.parquet), [diccionario](dictionary.json), [huellas SHA-256](inputs.json) y [auditoría agregada](audit.json) acompañan el diagnóstico. Las huellas describen las fuentes empleadas; no convierten el espejo en una publicación oficial del SII.
