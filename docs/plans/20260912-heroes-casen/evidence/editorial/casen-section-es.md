### Varias viviendas en un sitio: una explicación adicional que sí merece contrastarse

Dos viviendas pueden compartir un terreno y estar consideradas en un mismo rol. En ese caso, el Censo cuenta dos viviendas sin que necesariamente falte un predio en el registro tributario. Este mecanismo puede contribuir a la diferencia; demostrar cuánto aporta exige vincular **vivienda, sitio y rol**. El diccionario público examinado y el [manual de microdatos del Censo, pp. 17–20][ine-manual], permiten enlazar vivienda, hogar y persona, pero no proporcionan un identificador común de sitio o rol para esta conciliación. Varios hogares dentro de una vivienda tampoco equivalen a varias viviendas dentro de un sitio.

CASEN 2024 permite observar una señal más acotada. En su pregunta de tenencia, las categorías 3 y 4 identifican hogares que declaran **sitio propio compartido con otras viviendas**, pagado o pagándose. No preguntan cuántas viviendas hay en el sitio. Calculo su proporción entre **todos los hogares con respuesta válida**, incluidos arrendatarios y otras tenencias, usando una jefatura por hogar. La pregunta sobre hogar principal es condicional; filtrarla en toda la base eliminaría indebidamente hogares de viviendas unihogar. Véase el [cuestionario oficial, pp. 79 y 83][casen-cuestionario].

El resultado nacional es **1,09 % de los hogares**, con un intervalo aproximado del 95 % de **0,97 % a 1,21 %**. Procede de 78.654 hogares muestrales, sin respuestas faltantes en esa pregunta. La estimación nacional y las regionales usan `expr` y linealización de Taylor con estratos y conglomerados; el intervalo expresa incertidumbre muestral, no todos los posibles errores de medición. La [nota oficial de uso de CASEN][casen-nota] distingue estos dominios del uso descriptivo comunal.

<!-- CASEN_FIGURE_AND_TABLE -->

Valparaíso y Viña del Mar muestran **9,27 % y 8,60 %**, respectivamente, en el cálculo comunal ponderado con `expc`. Son señales exploratorias: las elegí después de observar su discrepancia y estos resultados **no son estimaciones representativas de cada comuna**. La presencia de un factor comunal no les confiere esa propiedad. La tabla conserva tamaños muestrales y faltantes; las once comunas sin muestra se registran como dato ausente, nunca como cero.

La deducción es limitada pero útil: contar viviendas y contar roles puede producir diferencias aun con un registro correcto. El patrón observado en estas dos comunas vuelve pertinente examinar los sitios compartidos. La hipótesis es que expliquen una parte de su discrepancia, junto con campamentos, destinos agrícolas, fechas y eventuales omisiones. La evidencia que permitiría distinguir estas explicaciones es una muestra representativa que enlace viviendas con sitios y roles; la hipótesis perdería fuerza como explicación material si ese cruce mostrara que su aporte es pequeño bajo un criterio fijado antes de medirlo.

**No descuento este porcentaje de las barras ni de los escenarios en pesos.** Describe una tenencia de hogares, no la proporción de viviendas que sobran en el recuento. Además, no cubre todas las formas de compartir sitio y podría superponerse con campamentos. Restarlo ahora produciría una precisión aparente y podría contar dos veces la misma explicación.
{: .notice--info}

<details markdown="1">
<summary>Por qué no convertir directamente el porcentaje CASEN en viviendas por sitio</summary>

En un ejemplo puramente hipotético, si una proporción $$p_v$$ de las **viviendas** perteneciera a sitios con exactamente dos viviendas y las restantes ocuparan sitios individuales, habría $$V(1-p_v/2)$$ sitios. La razón roles/sitios sería $$R_2=R_1/(1-p_v/2)$$, con $$R_1=\text{roles}/V$$. Por ejemplo, un $$p_v=0{,}20$$ supuesto equivaldría a 90 sitios por cada 100 viviendas. La proporción CASEN de **hogares** no es ese parámetro: la fórmula ilustra el mecanismo, pero no estima un ajuste fiscal.

</details>
