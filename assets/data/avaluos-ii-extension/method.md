# Avalúos II: ampliación explicativa

## Alcance

Esta ampliación agrega cantidades CASEN y evidencia agregada de usos mixtos SII. Presenta por separado una comparación ampliada entre el Censo y grupos disjuntos de roles de la misma descarga directa. No modifica el espejo de julio, el visor, las cifras, figuras, sensibilidad 2024S2 ni los escenarios fiscales del análisis original, y no suma hogares CASEN o de campamentos a esa comparación.

## SII: fuente, unidad y clasificación

La fuente es la descarga nacional directa `BRORGA2441_NAC_2026_1.zip`, primer semestre de 2026. Una fila A/N representa un rol administrativo y las filas AL/NL describen líneas de terreno o construcción. Una línea residencial observable exige ordinal positivo, superficie positiva y destino H; varias líneas H del mismo rol cuentan una vez.

El grupo inicial contiene roles con destino principal distinto de H y al menos una línea H válida. Se excluye primero el rol con destino K o referenciado como bien común, y luego el rol matriz referenciado. Una unidad individual que referencia esos roles no se excluye automáticamente. El código K está documentado como bien común en la [guía oficial SII de 2013](https://www.sii.cl/portales/reavaluo_no_agricola/2013/guia_para_calcular_avaluo.pdf), aunque el PDF breve vigente lo omite. Los destinos vacíos o desconocidos no se imputan. Los 24.451 roles no agrícolas con destino principal H sin una línea H válida conservan su clasificación principal.

La serie N contiene 8.560.728 roles y 6.057.949 con destino principal H. Entre los roles no H, 90.680 tienen una línea H válida; tras las exclusiones quedan 76.493. Como ambos grupos son disjuntos dentro del mismo archivo, forman 6.134.442 roles no agrícolas con evidencia residencial. La serie A se informa aparte: 941 roles con H y 19.462 con P sin H. Estos resultados cuentan roles, no viviendas, hogares, personas, construcciones omitidas, deuda ni recaudación.

El total H principal de la descarga directa supera en 3.141 al espejo de julio y coincide con el control MINVU citado en el post. Es una concordancia agregada, no una conciliación individual completa; por eso no sustituye el denominador histórico.

## CASEN: cantidades y dominio

Las cantidades corresponden a una respuesta por hogar tomada desde el registro de jefatura cuando `v9=3/4`: sitio propio compartido con otras viviendas, pagado o pagándose. Los residentes son todas las personas pertenecientes a esos hogares, no personas que hayan respondido esa categoría de manera independiente. No se filtra por la condición de hogar principal (`v28`), que solo se pregunta en viviendas con más de un hogar. Chile usa `expr`; Valparaíso y Viña del Mar usan `expc` como descripciones comunales sin representatividad estadística. Los tamaños muestrales de hogares y residentes se publican en unidades separadas.

## Límite de combinación

Los roles principales H y los roles distintos no H con línea H válida sí se unen dentro de la misma descarga SII. La serie agrícola también cuenta roles, pero se informa aparte porque queda fuera del universo no agrícola elegido. Los hogares CASEN y de campamentos usan otra unidad y no tienen un identificador que permita controlar el solapamiento, por lo que no se suman ni se restan de esa unión. El aporte de esos mecanismos a la diferencia requeriría un enlace vivienda–sitio–rol con fechas compatibles.

## Archivos públicos

- `sii-communes.csv`: agregados por comuna y serie.
- `sii-destination-breakdown.csv`: desglose agregado del grupo elegible por destino principal.
- `casen-quantities.csv`: Chile, Valparaíso y Viña del Mar, con cantidades y muestras.
- `expanded-comparison.csv`: comparación comunal completa entre el filtro H directo y la unión ampliada.
- `expanded-national-summary.csv`: diferencia nacional neta y suma de diferencias positivas, antes y después de ampliar.
- `audit.json`: identidades y cobertura verificadas por el proyector.
- `provenance.json`: nombres, SHA-256 y URL disponibles; no incluye rutas internas.
