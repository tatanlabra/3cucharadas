# Multiagentes III — hilo de X

Estado: **preparado, no publicado.** No hay credenciales de X en esta máquina:
la publicación es manual. Campaña UTM: `multiagente-memoria-gobernada`.

Las cuatro láminas 1600×900 están en `difusion/x/laminas/`, una por post. Se
regeneran con:

```
CAROUSEL_SLIDES_DIR=difusion/x/laminas \
LINKEDIN_CAROUSEL_WIDTH=1600 LINKEDIN_CAROUSEL_HEIGHT=900 \
scripts/render-linkedin-carousel.sh difusion/x/multiagente-penta-agent-memoria-gobernada-carrusel.html
```

Cada encabezado trae el recuento del post que le sigue. El enlace se cuenta por
el largo fijo de un `t.co`, no por el suyo propio, más el salto de línea que lo
separa. El límite es el de una cuenta sin Premium: con Premium sobra margen.

El recuento vive en el encabezado a propósito: `verify_difusion_coherente.rb`
compara toda cifra de una pieza contra el cuerpo del post, y un recuento de
caracteres no afirma nada sobre el post. Los encabezados quedan fuera de esa
comparación; el cuerpo del mensaje, no.

## Hilo ES

### 01 — imagen `…-carrusel-01.png` · 253/280 · OK

Tercera bitácora del sistema multiagente que corre en mi máquina.

La memoria ya recuperaba bien. La pregunta pasó a ser más incómoda: qué persiste, qué caduca y qué nunca debe salir de su ámbito.

Cuatro fuentes separadas por contrato, no fusionadas. 🧵

### 02 — imagen `…-carrusel-02.png` · 266/280 · OK

Tener acceso técnico a un dato no decide si es legítimo reutilizarlo.

Memoria de trabajo, correo personal, índice de tesis y la proyección pública derivada. Ninguna se mezcla: cada una define qué salidas permite.

16.955 puntos, 1.432 estrategias, 3.949 relaciones.

### 03 — imagen `…-carrusel-03.png` · 276/280 · OK

40 consultas sobre 319 contextos aislados. Ocho escritas para comprobar que el sistema sepa *no* recuperar.

38 completas, 2 parciales, 0 fallos.

Probé un reordenador: ordenaba mejor y lo rechacé, porque el tiempo de respuesta subía demasiado. Mejor no siempre es promovible.

### 04 — imagen `…-carrusel-04.png` · 273/280 · OK

Publico el post con una compuerta en rojo, y es lo mejor que tiene.

El índice es del 29 de agosto; el corpus creció de 796 a 817 documentos y no se regeneró. Caducó la vigencia, no el dato.

Una compuerta verde ahí habría sido peor que no tenerla.

https://3cucharadas.cl/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/?utm_source=x&utm_medium=social&utm_campaign=multiagente-penta-agent-memoria-gobernada-poc&utm_content=es

## Thread EN

### 01 — imagen `…-carrusel-01.png` · 254/280 · OK

Third log of the multi-agent setup running on my own machine.

Memory already retrieved well. The harder question came next: what should persist, what should expire, and what must never leave its scope.

Four sources kept apart by contract, not merged. 🧵

### 02 — imagen `…-carrusel-02.png` · 235/280 · OK

What is inside: 16,955 indexed points, 1,432 strategies, 3,949 relations and 319 curated contexts.

Operational memory, personal mail, a thesis index and the sanitized public projection built from them. None of them blend into another.

### 03 — imagen `…-carrusel-03.png` · 254/280 · OK

The evaluation: 40 queries over 319 isolated contexts. Eight written to check the system knows when *not* to retrieve.

38 complete, 2 partial, 0 outright failures.

A reranker ordered results better and I rejected it anyway: response time grew too much.

### 04 — imagen `…-carrusel-04.png` · 273/280 · OK

I am publishing this post with a gate in red, and it is the best thing about it: the corpus grew from 796 to 817 documents and the index was not rebuilt.

What expired is currency, not the data. A gate still green there would be worse than no gate.

https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/?utm_source=x&utm_medium=social&utm_campaign=multiagente-penta-agent-memoria-gobernada-poc&utm_content=en

