# Avalúos II: método, fuentes y errata

## Qué mide la comparación

Una diferencia entre viviendas particulares del Censo 2024 y roles habitacionales H del SII 2026S1. Una vivienda es una unidad censal; un rol identifica un bien raíz. No existe aquí un enlace individual que permita identificar viviendas sin rol. Viviendas vacantes también cuentan; viviendas rurales pueden estar en predios de destino agrícola. Copropiedad, roles matrices, subdivisiones y destino preferente pueden romper la correspondencia uno a uno.

La tabla conserva todas las comunas, diferencias negativas y fuentes ausentes. El gráfico físico muestra sólo las 15 mayores diferencias positivas entre comunas cubiertas. No es un ranking de evasión, deuda, recursos perdidos ni negligencia.

## Fuentes y fechas

| Fuente | Uso | Alcance |
|---|---|---|
| [INE Censo 2024](https://censo2024.ine.gob.cl/resultados/) | Viviendas particulares por comuna; `tipo_operativo = 2` | 7.638.396; excluye colectivas y situación de calle; hogares concilian con agregado INE |
| [Espejo catastral](https://catastral.cl/) | Extractos 2026S1 descargados 24-07-2026 | 6.054.808 roles H únicos; también incluye registros sin coordenadas |
| [SII por destino](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html) | Control independiente 2026S1 | 6.056.150 H; diferencia de 1.342 frente al extracto, causa pendiente |
| [SII Producto 3, Resolución 5/2010](https://www.sii.cl/documentos/resoluciones/2010/2010-5.pdf) | Definición del campo catastral semestral | Puede incluir aseo y sobretasas; documentación histórica, requiere confirmar contrato de la extracción actual |
| [SII descarga rol de contribuciones](https://www.sii.cl/entidades_externas/descargarolcontribuciones.htm) | Contraste de definición RC | La cuota trimestral también incluye aseo; no sustituye al neto |
| [Cuenta pública SII 2025](https://www.sii.cl/cuenta_publica/2025/cuenta_publica_2025.pdf) | Control del contraste 2024S2 | 5.856.068 H, coincidencia nacional del archivo histórico |
| [MINVU parque habitacional](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/) | Dos planillas oficiales 2026S1, destino y tramos de avalúo, revisadas 10-09-2026 | 6.057.949 H; las 346 filas comunales concilian entre ambas planillas y con sus totales |
| [SII estadísticas comunales vigentes](https://www.sii.cl/sobre_el_sii/estadisticas/estadisticas_bienes_raices_por_comuna.html) | 16 CSV de carga dinámica, 2026S1, M$ al 01-01-2026 | Componentes para todos los destinos no agrícolas, no para H separadamente |
| [MINVU, Caracterización de campamentos en Censo 2024](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/) | Autoridad metodológica del cruce georreferenciado MINVU–INE | En la foto 2024: 1.373 campamentos con viviendas ocupadas, 81.993 viviendas, 77.399 hogares y 238.491 personas |
| `CNC_2026.zip`, entregado por la persona usuaria | Polígonos vigentes al 25-05-2026; sólo se publican agregados comunales | 1.345 polígonos; `HOGARESCAT` suma 82.576; `HOGARESCEN` numérico suma 71.760 y falta en 222 polígonos |
| `BBDD_CNC_innominada-.zip`, entregado por la persona usuaria | Auditoría de compatibilidad; no alimenta el ajuste | Registro histórico 2011–2021 a nivel persona/hogar; no representa el stock comunal vigente de 2026 |

Antártica (CUT 12202) y Trehuaco (16207) no tienen extracto en este conjunto. Su ausencia no acredita cero roles en el SII. Los 1.342 H faltantes del total nacional no se imputan a una comuna sin evidencia. Trehuaco sí tiene 1.276 H en el archivo histórico 2024S2, bajo CONARA 08108; se conserva ese dato separado, sin imputar 2026. El contraste histórico usa 2024S2 y la misma homologación; no identifica fechas de alta ni sigue automáticamente un panel de inmuebles idénticos.

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

donde $C^{obs}_{c}$ es la suma numérica de `HOGARESCEN` en los polígonos del CNC 2026. La operación supone, sólo para explorar sensibilidad, que cada hogar censado en campamento explica una vivienda censal que no debiera exigir un rol H separado. No observa ese enlace, no sabe si el terreno tiene rol matriz, no sabe si la vivienda está incorporada como construcción y no sabe si supera el avalúo exento.

La resta reduce la suma de brechas positivas de 1.588.449 a 1.516.689 unidades: 71.760, o 4,52%. Alto Hospicio baja de 15.368 a 6.232; Viña del Mar, de 24.030 a 16.016; Antofagasta, de 21.755 a 14.218. En cambio, Valparaíso conserva 29.961 de 32.533 y Puerto Montt 28.404 de 29.036. Esas diferencias muestran que campamentos son una explicación cuantitativamente importante en algunas comunas, pero no absorben el patrón nacional ni la mayor parte de las brechas grandes.

La capa tiene 222 polígonos con `HOGARESCEN` igual a `S/I` o vacío, repartidos en 95 comunas cubiertas por el espejo. El residuo de esas comunas descuenta sólo lo observado y puede estar sobreestimado respecto del mismo contrafactual. La tabla marca `partial_census_count`; no reemplaza el faltante por cero ni usa `HOGARESCAT` como imputación. Las 153 comunas sin polígono vigente se distinguen de las 96 con conteo completo y de las dos sin fuente de roles.

`HOGARESCAT` no se usa para restar: corresponde a otra medición, suma 82.576 y combina momentos de ingreso 2011, 2019, 2022 y 2024. La divergencia entre el informe 2024, `HOGARESCEN` y `HOGARESCAT` es evidencia de movilidad, actualización y diferencias operativas, no un error corregible eligiendo el número mayor.

## Materialidad censal: descriptor amplio y no identificador de campamento

Reproducimos los indicadores viv04–viv06 del manual INE en su universo correcto: viviendas particulares ocupadas con moradores presentes. Una vivienda es irrecuperable si su tipo es mediagua, mejora, vivienda de emergencia, rancho, choza, móvil u otro; o si tiene paredes de material precario, techo precario o sin cubierta sólida, o piso de tierra. El resultado nacional es 73.338 viviendas: 46.517 por tipo, 32.427 por materialidad y una unión menor que su suma por superposición.

No restamos esas 73.338. La materialidad no informa tenencia del suelo, formalidad urbanística, rol matriz ni localización dentro de un campamento. Además, se superpone con los hogares ya contados en `HOGARESCEN`; sumarla produciría doble descuento. Una vivienda en campamento puede tener materialidad aceptable y una vivienda irrecuperable puede estar fuera de un campamento o dentro de un predio formal.

## Lectura epistémica y pruebas de descarte

| Clase | Conclusión | Evidencia discriminante o condición de descarte |
|---|---|---|
| Hecho observado | El CNC 2026 contiene 1.345 polígonos, 71.760 hogares Censo numéricos y 222 polígonos sin ese conteo | Cambiar bytes, miembros, filas o totales rompe el build por hash y conciliación |
| Deducción | Restar hogares de campamento sólo puede ser un contrafactual porque las unidades no se enlazan uno a uno | Se volvería ajuste observado únicamente con una llave o enlace espacial validado vivienda–predio–rol |
| Inducción | Campamentos explican una fracción desigual: grande en Alto Hospicio, Viña del Mar y Antofagasta; pequeña en varias líderes | Se refuta si una versión completa y comparable de los polígonos cambia sustantivamente esas participaciones |
| Abducción A | Parte de la brecha proviene de viviendas en asentamientos irregulares | Gana apoyo con enlaces espaciales vivienda–campamento sin rol H; se descarta donde esas viviendas estén dentro de roles matrices/H existentes |
| Abducción B | Parte proviene de viviendas rurales, copropiedad o roles matrices | Gana apoyo con destino agrícola, copropiedad y relaciones prediales; se descarta con correspondencia uno a uno que siga faltando |
| Abducción C | Parte corresponde a rezago catastral exigible | Requiere fecha de construcción, aviso, obligación, avalúo sobre exención y alta posterior; se descarta si el rol existía o no había obligación |
| Abducción D | Parte es incompatibilidad temporal o error de clasificación/homologación | Gana apoyo al reconstruir cortes equivalentes; se descarta si el patrón persiste con igual fecha, fuente íntegra y claves validadas |

La ilegalidad tampoco implica ausencia permanente de rol. La [Ley 17.235](https://www.bcn.cl/leychile/navegar?i=128563) aplica el impuesto territorial a bienes raíces y el rol identifica el predio, no cada vivienda. Además, el [artículo 16 de la Ley 20.234](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0) dispone que, después de la recepción definitiva y el otorgamiento de escrituras en ciertos loteos irregulares regularizados, el SII asigne rol y avalúo separado. La afirmación «el SII jamás los tendrá» no es compatible con ese procedimiento legal.

## Por qué todavía no hay barras en pesos

El campo DC no separa contribución neta, aseo y sobretasas. Su suma habitacional es 508.919.215.492 CLP; el control SII por destino informa 455.500.163.000 CLP de giro semestral, incluyendo sobretasas. La diferencia de 53.419.052.492 CLP es una discrepancia de conciliación, **no** un cálculo de impuestos omitidos ni un monto de aseo identificado. Estos totales de auditoría no se multiplican por la brecha residencial.

Los PDFs comunales inicialmente consultados de [Los Ríos](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrc_los_rios.pdf) y [RM](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrc_santiago.pdf) corresponden a 2025S2. La revisión del 10-09-2026 encontró los CSV dinámicos vigentes de las 16 regiones: sí corresponden a 2026S1. Sus controles nacionales coinciden: 8.512.452 predios no agrícolas y 1.293.666.863.000 CLP netos semestrales, más sobretasas, con 59.910.165.000 CLP de aseo informados separadamente. Este universo incluye comercio, oficinas, estacionamientos y otros destinos; dividir su neto por los H fabricaría una media residencial. La disponibilidad del período se resuelve, la del universo fiscal H no.

### Qué agrega el control MINVU

Las dos planillas MINVU atribuyen 1.342 H a Trehuaco (escrito «Treguaco») y cero a Antártica. Es evidencia agregada oficial adicional, no una recuperación de los shards faltantes del espejo. El gráfico conserva su extracción única; los valores nuevos se consultan en la [conciliación oficial separada](source-audit.json).

La suma MINVU supera al cuadro nacional SII en 1.799 H. Entre las 344 comunas cubiertas por el espejo hay 208 diferencias positivas y ninguna negativa; suman precisamente 1.799. Calama aporta 420, Lo Barnechea 114 y Concepción 109. Trehuaco aporta otros 1.342 al comparar MINVU con el espejo. Así, la diferencia de totales ya tiene una descomposición comprobable, aunque su causa administrativa sigue pendiente.

Un corte o una revisión posterior del catastro es una hipótesis compatible con el patrón unilateral. Se distinguiría de una diferencia de cobertura o clasificación mediante fechas efectivas, reglas de inclusión y claves de altas/bajas. Se descartaría como explicación temporal si se acredita que ambos extractos comparten fecha y versión, o si las diferencias responden a duplicados o reclasificación. La igualdad de semestre no acredita igualdad de versión. Esta hipótesis no demuestra rezago tributario.

Una vez obtenido el neto: B(q) = max(viviendas − roles H, 0) × q × media anual equivalente de los H. El equivalente anual duplica el semestre bajo sus mismas condiciones: no es impuesto anual efectivamente girado o cobrado. La media incluye ceros. Media y promedio son el mismo estadístico; la mediana puede ser cero y se mostrará junto a proporción positiva, media y mediana entre positivos.

q = 0, 0,25, 0,5 y 1 son escenarios transparentes. q = 1 no es una omisión observada ni una cota superior real. No se estiman errores estándar de muestreo. La conversión permanecerá nula hasta disponer de una fuente neta compatible; no hay valores de demostración en producción.

## Errata de identidad territorial del visor anterior

| Comuna INE | CUT | CONARA SII correcto | H anterior erróneo | H corregido, mismo extracto anterior |
|---|---|---|---:|---:|
| Coyhaique | 11101 | 11401 | 7.984 | 19.563 |
| Aysén | 11201 | 11101 | 1.801 | 7.984 |
| Chile Chico | 11401 | 11201 | 19.563 | 1.801 |

La tabla oficial CONARA identifica la comuna; los nombres del espejo y el sufijo CUT de algunos archivos estaban intercambiados. Se corrigieron indicadores dependientes y celdas de densidad de esas tres comunas, manteniendo la extracción anterior del visor y su total nacional. El nuevo diagnóstico tiene extracción 24-07-2026 y valores propios; las capas UV y el período del post I no se rehacen.

El metadato principal se actualizó a roles H / todas las viviendas particulares, que ya era la lectura del visor. El campo histórico `viviendas_ocupadas_censo_2024` sólo contiene viviendas con moradores presentes, no todas las ocupadas; el diccionario ahora lo explicita.

## Responsabilidad y evidencia necesaria

SII determina avalúos y giros; TGR recauda. Girado y pagado son cantidades distintas. El impuesto territorial participa del Fondo Común Municipal: un peso adicional de impuesto asociado a una comuna no equivale automáticamente a un peso adicional retenido por su municipio. No se estima aquí esa distribución.

Una sospecha de rezago requiere documentar existencia y características del inmueble, correspondencia con el rol, fecha de aviso o información disponible, exigibilidad, exenciones y fecha efectiva de incorporación o actualización. Una brecha agregada sólo prioriza una investigación. Una omisión podría afectar una ampliación de un rol existente sin crear un rol nuevo.

[Datos JSON](communes.json), [CSV](communes.csv), [Parquet](communes.parquet), [diccionario](dictionary.json), [huellas SHA-256](inputs.json) y [auditoría agregada](audit.json) acompañan el diagnóstico. Las huellas describen las fuentes empleadas; no convierten el espejo en una publicación oficial del SII.
