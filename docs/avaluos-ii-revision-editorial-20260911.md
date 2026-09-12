# Revisión de la nueva base editorial — 11-09-2026

Base aportada por el usuario: [`avaluos-ii-revisado-20260911.md`](editorial-sources/avaluos-ii-revisado-20260911.md), revisión realizada con ChatGPT web según su indicación. SHA-256 leído: `e1c1a376390a44d5f08ae521668ea05fbc7a2f09af58f782c04682cbb6edce2c`. Se conserva sin modificaciones. Este documento entrega la revisión solicitada; no traduce, promueve ni publica el artículo.

La nueva versión distingue expresamente los dos grupos de quince comunas, explica la composición hipotética de materialidad y separa vivienda de rol. Se contrastaron las veinte filas comunales de sus dos tablas con `communes.json`: coincidencia en conteos, porcentajes y medianas, al redondeo mostrado. La elección editorial recomendada es trabajar desde esta versión.

## Ajustes antes de traducir

| Prioridad | Lugar en el borrador | Ajuste propuesto | Motivo |
|---|---|---|---|
| Alta | Tercera cucharada y líneas 134–138 | Separar escenario comunal en pesos de obligaciones efectivamente omitidas | El primero requiere neto compatible y supuestos explícitos; el segundo exige además identificación predial, fechas y situación tributaria. El texto actual mezcla estos requisitos |
| Alta | Introducción, título y cierre, línea 146 | Recuperar explícitamente el interés tributario de investigar una discrepancia persistente junto a avalúos altos; retirar «una deuda inventada» | Mantiene el propósito del usuario con tono afirmativo, sin transformar el perfil observado en probabilidad de omisión |
| Alta | Campamentos, línea 57 | Añadir una frase que distinga descuento analítico de exención: el SII contempla tasar construcciones no regularizadas | La versión anterior lo aclaraba; su eliminación deja abierta la interpretación de que campamento significa ausencia de obligación o imposibilidad de rol |
| Media | Línea 119 | Cambiar «introduciría un sesgo de selección» por «podría introducir un sesgo si los inmuebles ausentes tienen un perfil distinto» | Se conoce el riesgo; no se ha observado la composición de los ausentes ni probado que difiera |
| Menor | Línea 142 y bibliografía | Enlazar Grote y Wen en el cuerpo y escribir «pp. 16–18»; mantener fuentes primarias con fecha/corte explícitos | El contenido citado está respaldado; no es obligatorio reintroducir todos los estudios internacionales de la versión anterior |
| Técnica | Front matter de ambos borradores ES | Consolidar una sola fuente española con el `ref` y permalink canónicos; conservar el original recibido como antecedente fuera de las entradas compiladas | El nuevo archivo y `avaluos-ii-brecha-residencial.md` tienen iguales `lang: es`, `ref` y permalink. No deben competir por el mismo destino en builds con borradores |
| Técnica | Fecha y futura versión inglesa | Fechar ambas versiones el 11-09-2026 con zona America/Santiago, UTC−03:00, y traducir desde el español consolidado | El nuevo manuscrito conserva 09-09 y −04:00; el inglés existente corresponde a la versión anterior |

Redacción sugerida para resolver el principal problema metodológico:

> Para construir un escenario comunal en pesos falta una contribución neta habitacional compatible y conciliada, junto con supuestos explícitos de traslado. Para cuantificar obligaciones efectivamente omitidas, además hay que identificar los predios y verificar fechas, beneficios y exenciones.

Título posible para la tercera cucharada: «Del escenario comunal a la comprobación predial». Título general posible: «Avalúos II: dónde la brecha residencial merece una revisión tributaria».

La distinción de campamentos está respaldada por los [documentos requeridos por el SII para tasación](https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html). El monto exento del primer semestre se comprobó en el [ejemplo oficial SII](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf). Las páginas impresas 16–18 de [Grote y Wen](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf) respaldan la secuencia de cobertura, valoración y cobro; no prueban el ranking chileno.

## Orden de continuación

1. Aplicar los ajustes a la base española y resolver la duplicación, preservando el texto recibido.
2. Traducir el español ya consolidado: distinguir `dwelling`, `household`, `property/cadastral record`, `assessed value` y `tax liability`; mantener los números y las condiciones de inferencia.
3. Fijar la fecha editorial de hoy en ambas versiones, conservando 2026S1 como período de datos; construir ES/EN y revisar enlaces, gráficos, metadatos y destino único.
4. Mantener la preparación local separada del push. La intención de publicar próximamente no se interpreta como instrucción de envío inmediato.

Estos ajustes preparan un post diagnóstico. El objetivo original de cuantificar escenarios monetarios continúa parcial por la fuente neta faltante; la revisión editorial no cierra ese requisito ni lo sustituye por otro estimando.

## Aplicación posterior — 11-09-2026

Los ajustes del listado ya están incorporados en el español canónico, traducidos al inglés y fechados hoy. El manuscrito recibido sigue intacto en el archivo de procedencia. Las dos versiones incluyen hero y teaser conceptuales generados mediante imagegen, con revisión delegada y pruebas de integración. [Contrato F10](avaluos-ii-editorial-consolidation-contract.yaml), [F11](avaluos-ii-visual-editorial-contract.yaml) y [evidencia de cierre local](avaluos-ii-editorial-consolidation-evidence.md).
