---
layout: single
title: "Nushell en 3 cucharadas: ¿cuándo una shell estructurada le saca jugo a un agente?"
subtitle: "R, microbenchmarks y 380 ejecuciones para distinguir mejora, empeoramiento e indiferencia"
date: 2026-08-29 00:00:00 -0400
last_modified_at: 2026-09-05 00:00:00 -0400
categories: [ia, productividad, desarrollo, multiagente]
tags: [nushell, shell, agentes, claude-code, codex, routing, context-engineering, docker, arch-linux, benchmark, r]
description: "Probé con evidencia si una ruta selectiva hacia Nushell ayuda a agentes de código: mejoró algunos aciertos, elevó tiempo y tokens, y fue indiferente en un caso real agregado."
excerpt: "Un corpus afinado, un holdout y una recreación agregada de mi tesis muestran cuándo Nushell mejora el flujo, cuándo lo empeora y cuándo no cambia el resultado."
author: clabra
lang: es
ref: nushell-coprocesador-estructurado
permalink: /ia/productividad/desarrollo/nushell-coprocesador-estructurado/
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
repo: https://github.com/tatanlabra/penta-agent
entorno: "EndeavourOS (Arch), zsh, Nushell 0.115.1 y Claude Code + Codex sobre el mismo workspace"
header:
  teaser: /assets/images/teasers/teaser-structured-shell.webp
  og_image: /assets/images/structured-shell/og-1200.webp
  og_image_alt: "Un flujo de datos entra a un núcleo de procesamiento y se divide en tres rutas estructuradas representadas en azul, magenta y gris"
en_abstract: >
  I tested whether a selective Nushell route makes sense for coding agents instead
  of assuming that a typed shell must be better. The evidence comprises 380 runs:
  a 200-run pipeline microbenchmark, a tuned 100-run agent A/B test, a 50-run
  holdout, and a 30-run aggregate case based on a governed reconstruction of my
  master's thesis. Nushell improved accuracy in some task families, increased
  latency and output tokens, and produced no accuracy advantage in the real
  aggregate case. The defensible result is therefore a bounded routing rule, not
  a claim that Nushell is generally superior.
---

## Preámbulo — ¿La estructura realmente ayuda?

A fines de agosto de 2026 escuché a Lorenzo Carbonell, de [atareao.es](https://atareao.es/), hablar de Nushell y de su ventaja al trabajar con datos estructurados. Me quedó dando vueltas la pregunta: **¿esa estructura puede ayudarme realmente en mi flujo?**

La shell Unix funciona bien, pero muchas de sus tuberías dependen de texto, posiciones de columnas y opciones que no siempre se comportan igual entre implementaciones.[^greenberg-2020] Nushell propone otra lógica: mantiene tablas y valores tipados —por ejemplo, fechas, números o tamaños— durante la tubería.[^nushell]

No quise reemplazar `zsh`. Preferí usar Nushell como una ruta selectiva y someter esa decisión a tres resultados posibles:

- **mejora**, si aumenta la corrección lo suficiente para justificar el coste;
- **empeoramiento**, si añade tiempo, tokens o complejidad sin compensarlos;
- **indiferencia**, si cambia la ruta técnica pero no el resultado relevante.

Para probarlo escribí una *skill* (una regla que orienta al agente sobre cuándo usar una herramienta) y reuní **380 ejecuciones**: 200 comparaciones de tuberías, 100 pruebas A/B sobre un corpus afinado, 50 corridas con tareas retenidas y 30 observaciones de un caso real agregado inspirado en la recreación de mi tesis.

Son muchas repeticiones, pero pocas familias de tareas. Además, parte de la integración fue afinada durante el proceso. Por eso los resultados son **evidencia exploratoria y acotada, no una prueba universal**.

La pregunta no es si Nushell es mejor que Bash:

> **¿En qué casos una ruta estructurada mejora el trabajo de un agente, en cuáles lo empeora y en cuáles resulta indiferente?**

---

## Primera cucharada — Enrutar antes de reemplazar

La política usa la herramienta menos compleja que resuelve la tarea con robustez.

| Nivel | Herramienta preferente | Uso preferente |
|---|---|---|
| 1 | `git`, `systemctl`, `pacman`, `ssh`, `rsync` | La operación ya tiene una interfaz directa. |
| 2 | `rg`, `jq`, `yq`, `awk`, `fd` | Una utilidad especializada resuelve la transformación. |
| 3 | Nushell | Varias transformaciones sobre datos tabulares o tipados. |
| 4 | DuckDB, Python, Polars o R | El volumen o la lógica requieren un motor analítico. |
{: tabindex="0" aria-label="Política de enrutamiento de herramientas"}

Antes de comparar resultados, conviene ubicar las familias. Que varias herramientas se llamen *shell* no implica que transporten la misma clase de información: `zsh` suele coordinar texto y comandos; Nushell conserva valores estructurados. El diagrama orienta, no declara una ganadora.

<figure>
  <picture>
    <source media="(max-width: 40em)" srcset="/assets/images/structured-shell/fig-d2-familias-shell-mobile.svg">
    <img src="/assets/images/structured-shell/fig-d2-familias-shell.svg"
         alt="Diagrama D2. Las shells de texto sh, Bash y zsh pasan texto entre programas; fish es una shell interactiva no POSIX; Nushell transporta registros, columnas, números y fechas; PowerShell encadena objetos .NET. El experimento compara solamente la ruta selectiva entre zsh y Nushell."
         loading="lazy">
  </picture>
  <figcaption><strong>D2 — Dónde encaja Nushell.</strong> Es un mapa conceptual para leer la regla de enrutamiento, no un ranking de shells ni una comparación con fish o PowerShell.</figcaption>
</figure>

La regla práctica es sencilla: **si Nushell solo sirve para ejecutar dentro de otra shell un comando que ya funciona bien, sobra**.

La integración quedó compuesta por una *skill*, reglas de activación estrechas y un pequeño envoltorio, `nu-query`, que devuelve JSON, aplica un tiempo máximo y declara si truncó filas. No lo agregué a permisos autoaprobados: `nu -c` puede modificar el sistema.

Antes de medir aparecieron fallos más interesantes que cualquier benchmark. En el entorno probado, `ls **/*` omitía rutas ocultas, Claude Code sustituía algunos comandos por otras implementaciones y la salida localizada complicaba el parseo. En aquel árbol, `ls **/*` encontró unos 46.400 archivos y `ls -a **/*` unos 127.900: omitir `-a` dejaba fuera cerca del 64 %. No es una propiedad general de Nushell; es una advertencia fechada sobre un error silencioso observado en ese entorno.

---

## Segunda cucharada — Medir con R, no con impresiones

### Primer nivel: tubería contra tubería

El primer experimento fue un **microbenchmark** (comparación repetida de tareas pequeñas y bien acotadas): cuatro tareas, dos variantes y 25 repeticiones por variante, para un total de **200 ejecuciones**. Analicé los resultados con R 4.5.3.

| Tarea | Variante | Tiempo mediano | Salida |
|---|---|---:|---:|
| Archivos > 1 MB, últimos 30 días | `find + sort + head` | **389 ms** | **648 B** |
| | Nushell | 1.315 ms | 1.060 B |
| Cinco procesos con mayor memoria | `ps + awk` | **22 ms** | **113 B** |
| | Nushell | 233 ms | 366 B |
| Contenedores agrupados por imagen | `docker + sort + uniq` | **19 ms** | **339 B** |
| | Nushell | 40 ms | 603 B |
| Contexto de `docker ps -a` | Sin reducir | **17 ms** | 3.353 B |
| | Agregado en Nushell | 39 ms | **566 B** |
{: tabindex="0" aria-label="Microbenchmark congelado de tuberías"}

<figure>
  <iframe src="/assets/visores/structured-shell/index.html?lang=es"
          title="Visor interactivo del corpus de benchmark de Nushell"
          loading="eager"
          style="width:100%;height:clamp(470px,78vw,660px);border:1px solid #2a3041;border-radius:6px"></iframe>
  <figcaption style="font-size:.85em;opacity:.75;margin-top:.4em">
    El análisis se ejecutó en R. El visor representa datos precomputados del corpus congelado y no consulta la máquina de quien lee.
  </figcaption>
</figure>

El resultado fue incómodo, como debe ser una medición útil: **Nushell fue más lento en todas las tareas cronometradas**. Tampoco redujo siempre el contexto. La ventaja apareció cuando hubo agregación real: el resumen de contenedores bajó de 3.353 a 566 bytes, cerca de un 83 %.

La ganancia potencial era semántica: comparar tamaños o fechas como valores tipados deja menos supuestos implícitos que fabricar columnas de texto y luego decidir cómo ordenarlas. Pero el microbenchmark medía tuberías escritas por mí. Faltaba observar al agente.

### Segundo nivel: agente contra agente

El corpus afinado usó cinco familias de tareas en español: tres donde la política favorecía Nushell y dos donde debía evitarlo. Cada familia se repitió diez veces por brazo: **100 ejecuciones**. El agente fue Claude Code sin interfaz, con un modelo de la familia Sonnet; la verdad de referencia se recalculó antes de cada corrida y el comando se extrajo del transcript, no del relato del agente.

| Subconjunto | Brazo | Acierto | Activación | Tiempo mediano | Tokens medianos |
|---|---|---:|---:|---:|---:|
| Positivas | Sin *skill* | 23/30 | 0/30 | **6.239 ms** | **152** |
| Positivas | Con *skill* | **30/30** | **28/30** | 9.537 ms | 368 |
| Negativas | Sin *skill* | 20/20 | 0/20 | 5.220 ms | 91 |
| Negativas | Con *skill* | 20/20 | **0/20** | 5.107 ms | 99 |
{: tabindex="0" aria-label="Resultados A/B del corpus afinado"}

En las tareas positivas, el acierto observado pasó de 23/30 a 30/30. Si se tratan las 60 corridas como observaciones independientes, la prueba exacta de Fisher da *p* = 0,0105.[^r-fisher] Ese supuesto no es defendible para generalizar: la unidad sustantiva es la familia de tareas y aquí solo hay tres familias positivas, reutilizadas durante el ajuste. Por eso el valor se informa como **descripción exploratoria del corpus afinado**, no como confirmación al 5 %.

El intervalo exacto de Clopper–Pearson (un rango compatible con una proporción binomial) fue [88,4 %; 100 %] para 30/30 y [57,7 %; 90,1 %] para 23/30.[^clopper-1934][^r-binom] La mediana de tiempo aumentó 1,53× y la de tokens de salida 2,43×: **más acierto en ese corpus, pero pagando por él**. Las medianas y su incertidumbre se estimaron mediante *bootstrap* (remuestreo de las observaciones para construir intervalos).[^efron-1993]

La tarea que más separó ambos brazos pedía los tres archivos de más de 1 MB modificados durante los 30 días anteriores. Sin la *skill*, el agente acertó 3/10; con ella, 10/10. El fallo recurrente usaba `fd -I`: esa opción ignora las reglas de exclusión, pero no incluye por sí sola archivos ocultos; para eso hacen falta `-H -I` o `-u`.[^fd]

El transcript descubrió además una trampa de `stdin` (entrada estándar): Bash alimentó a `nu -c`, este devolvió `null` con código 0 y el agente entró en una búsqueda de 77 segundos. La documentación exige `--stdin` para esa ruta.[^nushell-stdin] Tras corregirlo, ese caso bajó de 70.901 a 7.852 ms y de 3.287 a 303 tokens. Es un caso causal para esa tarea, no un estimador general.

---

## Tercera cucharada — Contrapruebas antes del veredicto

### El holdout que corrigió el relato

El corpus anterior afinó y evaluó sobre las mismas cinco familias. También amplié la muestra después de observar resultados preliminares. Para medir cuánto sobrevivía fuera de ese conjunto congelé la descripción de la *skill* y escribí cinco tareas retenidas (*holdout*: casos apartados del ajuste), tres positivas y dos negativas. Cinco repeticiones por brazo produjeron **50 corridas**.

| Subconjunto retenido | Brazo | Acierto | Activación | Tiempo mediano | Tokens medianos |
|---|---|---:|---:|---:|---:|
| Positivas | Sin *skill* | 10/15 | 0/15 | **6.449 ms** | **178** |
| Positivas | Con *skill* | **14/15** | **4/15** | 8.019 ms | 282 |
| Negativas | Sin *skill* | **6/10** | 0/10 | **5.227 ms** | **143** |
| Negativas | Con *skill* | 5/10 | 0/10 | 5.476 ms | 160 |
{: tabindex="0" aria-label="Resultados del holdout posterior"}

Las cuatro activaciones positivas se concentraron en una sola familia, con 4/5. Las otras dos obtuvieron 5/5 aciertos sin activar la *skill*. El holdout es pequeño y sus tareas negativas produjeron resultados débiles en ambos brazos. No prueba una ventaja general ni que la *skill* perjudique las tareas negativas. Sí refuta una extrapolación concreta: **28/30 era una propiedad del corpus afinado, no de la integración en general**.

### Un caso real agregado de mi tesis

La segunda contraprueba reutilizó la auditoría temporal gobernada de una reconstrucción de mi tesis de magíster, pero solo como *fixture* (conjunto pequeño y congelado para probar un contrato) de agregados públicos: una fuente de 306.768 filas y 263 columnas resumida en 21 filas anuales, sin microdatos ni identificadores. El hash de la fuente, sus invariantes, la exportación y los resultados están en el [paquete reproducible del caso](https://github.com/tatanlabra/3cucharadas/tree/main/research/structured-shell-thesis-case).

El control recibió la prohibición de usar Nu; la política congelada lo exigió solo para las dos tareas estructuradas. Con Codex en modo de solo lectura y razonamiento bajo, tres tareas por dos brazos y cinco repeticiones produjeron **30 observaciones**:

- R1 pidió el ranking de agregados válidos;
- R2 recibió el mismo *fixture* corrupto y debía bloquear el ranking;
- R3 preguntó si `presencia=0` demostraba cierre institucional y debía responder que estaba fuera de alcance.

| Tarea | Sin Nu | Política Nu | Lectura estricta |
|---|---:|---:|---|
| R1 · ranking válido | 5/5; Nu 0/5; 30,6 s; 445 tokens | 5/5; Nu 5/5; 42,0 s; 580 tokens | La política activó la ruta, pero no mejoró el acierto. |
| R2 · *fixture* corrupto | 5/5; Nu 0/5; 31,4 s; 358 tokens | 5/5; Nu 5/5; 32,0 s; 410 tokens | Ambos bloquearon el ranking; la activación prevista se observó 5/5. |
| R3 · límite conceptual | 5/5; Nu 0/5; 15,0 s; 88 tokens | 5/5; Nu 0/5; 11,4 s; 62 tokens | La política no filtró Nu hacia una pregunta conceptual. |
{: tabindex="0" aria-label="Caso real agregado de tesis, A/B con Codex"}

Ambos brazos acertaron 5/5 en las tres tareas. El caso demuestra conformidad de la política —Nu en 10/10 observaciones estructuradas y en 0/5 conceptuales dentro de ese brazo—, pero **indiferencia en acierto**. No calculé un *p*-valor: cinco repeticiones del mismo caso no son cinco tipos de problema independientes. Tampoco cambia el límite del dato: `presencia=0` no prueba cierre institucional.

### Un veredicto por resultado

| Resultado | Dónde aparece | Lectura defendible |
|---|---|---|
| Mejora | Corpus afinado: 30/30 frente a 23/30; holdout: 14/15 frente a 10/15 | Hay una señal de corrección en algunas familias, pero no una tasa generalizable. |
| Empeoramiento | Microbenchmark, corpus afinado y holdout | La ruta estructurada agregó latencia y, en los experimentos con agentes, más tokens. |
| Indiferencia | Caso real agregado y tareas que no activaron la *skill* | Cambiar la ruta no mejoró el acierto cuando ambos brazos ya resolvían el contrato. |
{: tabindex="0" aria-label="Veredicto de mejora, empeoramiento e indiferencia"}

Así queda mi regla después de medir:

> **Nushell merece una prueba cuando la consulta combina datos estructurados, varias transformaciones y un riesgo concreto de error silencioso.** Para una operación nativa, una transformación única o un análisis de mayor escala, normalmente hay una herramienta más simple o más apropiada.

No quiero convertirla en mi shell principal ni pedirle al agente que la use «cuando pueda». El objetivo es exactamente el contrario: **que pueda justificar cuándo entrar y cuándo no**.

Tampoco veo todavía razones para convertir esta ruta en un servidor MCP. Una consulta merecería promoverse a herramienta dedicada si aparece reiteradamente, tiene una interfaz estable, admite parámetros tipados, puede reutilizarse entre agentes y mejora de forma verificable la seguridad u observabilidad. Estos casos aún no cumplen todas esas condiciones.

## Cierre — Una shell no es una religión

El resultado no es que Nushell gane. En el corpus afinado mejoró el acierto; en el microbenchmark y los experimentos con agentes añadió tiempo y, en estos últimos, tokens; en el caso real agregado no cambió la corrección. La decisión razonable depende del tipo de tarea y del precio de equivocarse.

Lo más interesante tampoco fue Nushell. Fue descubrir que una *skill* podía no activarse, que una regla sobre archivos ocultos podía estar incompleta y que una tubería podía devolver `null` con éxito aparente. El benchmark terminó evaluando tanto a la herramienta como a mis propias suposiciones.

Seguramente hay mejores rutas. Si están usando Nushell, DuckDB, `jq`, Python, MCP, *skills* u otra estrategia que dé al agente una ventaja concreta, me interesa conocer **qué problema resuelve, frente a qué línea base y cómo comprobaron que realmente mejora el flujo**. Más que coleccionar herramientas, sería bueno empezar a coleccionar evidencia sobre cuándo vale la pena usarlas y qué mejoran concretamente en el flujo.

## Referencias y notas

> **Conflictos de interés y procedencia.** Las métricas de `penta-agent` y del caso de tesis fueron producidas por el mismo proyecto que implementó la *skill*. La documentación de Nushell también proviene de quienes desarrollan la herramienta. Se usa para documentar su contrato y comportamiento declarado, no como prueba independiente de superioridad.
{: .notice--info}

[^greenberg-2020]: Greenberg, Michael, y Austin J. Blatt. 2020. «Executable Formal Semantics for the POSIX Shell». *Proceedings of the ACM on Programming Languages* 4 (POPL), artículo 43, 1–30. <https://doi.org/10.1145/3371111>.

[^nushell]: Nushell. s. f. «Nushell: A New Type of Shell». Consultado el 5 de septiembre de 2026. <https://www.nushell.sh/>.

[^r-fisher]: R Core Team. s. f. «Fisher's Exact Test for Count Data». *R Documentation*. Consultado el 5 de septiembre de 2026. <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html>.

[^clopper-1934]: Clopper, C. J., y E. S. Pearson. 1934. «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial». *Biometrika* 26, n.º 4: 404–413. <https://doi.org/10.1093/biomet/26.4.404>.

[^r-binom]: R Core Team. s. f. «Exact Binomial Test». *R Documentation*. Consultado el 5 de septiembre de 2026. <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html>.

[^efron-1993]: Efron, Bradley, y Robert J. Tibshirani. 1993. *An Introduction to the Bootstrap*. Nueva York: Chapman & Hall. <https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317>.

[^fd]: sharkdp. s. f. «fd: A Simple, Fast and User-Friendly Alternative to `find`». Repositorio de GitHub. Consultado el 5 de septiembre de 2026. <https://github.com/sharkdp/fd>.

[^nushell-stdin]: Nushell. s. f. «Scripts». *The Nushell Book*. Consultado el 5 de septiembre de 2026. <https://www.nushell.sh/book/scripts.html>.
