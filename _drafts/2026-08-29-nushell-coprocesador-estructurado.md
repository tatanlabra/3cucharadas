---
layout: single
title: "Nushell en 3 cucharadas: un coprocesador estructurado, no una shell nueva"
subtitle: "De por qué las tuberías de texto son frágiles a si una skill concreta arregla algo: 120 corridas para averiguarlo"
date: 2026-08-29 00:00:00 +0000
categories: [ia, productividad, desarrollo, multiagente]
tags: [nushell, shell, agentes, claude-code, codex, routing, context-engineering, docker, arch-linux, benchmark]
description: "Integré Nushell como vía de enrutamiento selectiva y medí si sirve: microbenchmark, A/B a nivel de agente y análisis estadístico en R con bootstrap y Clopper-Pearson. Cada nivel de evidencia desmintió al anterior."
excerpt: "300 corridas, tres niveles de evidencia y un visor en R. Cada nivel desmintió al anterior: la skill no se activaba, y dos de los tres efectos que daba por buenos no eran afirmables con la muestra que tenía."
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
entorno: "EndeavourOS (Arch), zsh, nushell 0.115.1, Claude Code + Codex sobre el mismo workspace"
header:
  teaser: /assets/images/teasers/teaser-structured-shell.webp
  og_image: /assets/images/structured-shell/og-1200.webp
  og_image_alt: "Resultados del A/B: la activación de la skill pasó de 0/15 a 14/15 tras dos rondas de afinado, sin sobreactivación"
en_abstract: >
  Agents live on text, and text pipelines are subtle in ways that bite quietly.
  That general claim is not mine: formal work on the POSIX shell describes its
  power and subtlety as "a dangerous combination", and a HotOS paper notes that
  while many replacement shells have been proposed, the Unix shell persists.
  So I did not replace mine. I added Nushell to a local multi-agent setup as a
  selective routing lane and then measured, twice, whether it changes anything.
  First level: pipeline against pipeline. Nushell loses on wall time in every
  timed task, and only wins on bytes when there is something to reduce. Second
  level, and the one that matters: agent against agent, the same five Spanish
  requests to headless Claude Code with and without the skill. The first version
  activated zero times out of fifteen. Two rounds of description tuning later,
  guided by the product docs rather than intuition, activation reached 14/15 on
  positive tasks with zero over-activation, accuracy went 21/25 to 25/25, and the
  cost on tasks it should ignore stayed at noise level. The experiment also found
  three defects no pipeline benchmark could: Claude Code shadows find and grep
  with bfs and ugrep, "fd -I" lifts .gitignore but still skips hidden files, and
  piping into "nu -c" is silently ignored and returns null with exit 0 — which
  had been costing 77 seconds and 3,714 tokens per query until I documented it.
---

Un agente de código vive del texto. Le pides los procesos que más memoria consumen, recibe
cuatrocientas líneas de columnas alineadas por espacios, y tiene que decidir con `awk` dónde empieza
la columna que le importa. Cada uno de esos pasos es un sitio donde el resultado puede salir mal
**sin error**: un `2>/dev/null` de más, un formato de fecha que la implementación local no acepta,
una bandera que excluye la mitad del árbol.

Este post va de si vale la pena meter una shell tipada en ese hueco. Empieza por el problema
general, sigue por lo que construí, y termina en 120 corridas midiendo si sirve. Adelanto la parte
incómoda: la primera versión de lo que construí **no se activaba nunca**, y me habría enterado
tarde si me hubiera quedado en el benchmark que suele hacerse.

## El problema no es la shell: es el texto

La fragilidad de las tuberías de texto está documentada mucho antes de que hubiera agentes. Greenberg
y Blatt construyeron una semántica formal ejecutable de la shell POSIX y describen el objeto de
estudio sin rodeos: *«Its power and its subtlety are a dangerous combination»*. Su experimento es el
dato duro: compararon su semántica contra **siete shells que aspiran a cumplir POSIX** —bash, dash,
zsh, OSH, mksh, ksh93 y yash— usando tres baterías de pruebas. La conclusión operativa es que la
conformidad con el estándar es una cuestión que hay que medir, no suponer[^smoosh].

No es que la tubería carezca de estructura: la tiene, sólo que implícita. Handa y colegas
formalizaron un modelo de flujo de datos *consciente del orden* para tuberías Unix, demostraron
correctas las transformaciones que explotan su paralelismo y las evaluaron sobre 47
tuberías[^dataflow]. Es decir: el modelo de datos existe, pero vive en la cabeza de quien escribe el
comando, no en la herramienta.

Para un humano en una terminal, eso es asumible. Para un agente que encadena comandos sin ver la
salida intermedia, cada supuesto implícito es un fallo silencioso esperando su turno.

## Por qué no reemplacé la shell

La tentación obvia es cambiar de shell. La literatura sugiere que es mala idea. Greenberg, Kallas y
Vasilakis, revisando cincuenta años de shell, lo dicen en una frase: *«While many replacement shells
have been proposed, the Unix shell persists»*[^next50]. Persiste porque es infraestructura crítica y
porque casi todo lo que existe asume su semántica.

Nushell promete justamente lo contrario del texto. Su propia página lo formula así: *«Nu pipelines
use structured data so you can safely select, filter, and sort the same way every time. Stop parsing
strings and start solving problems»*[^nushell]. Es una promesa, no un resultado — y el resto del post
es el intento de comprobarla.

Así que la decisión fue tratarlo como un **problema de enrutamiento**, no de lenguaje. `zsh` sigue
siendo la shell. Hay cuatro vías, y siempre gana la más baja que resuelva con robustez:

```text
1. comando nativo          git · systemctl · pacman · ssh · rsync
2. herramienta especializada  rg · jq · yq · awk
3. Nushell                 datos tipados, varias transformaciones
4. motor analítico         DuckDB · Python · Polars · R
```

El criterio de éxito, que es contraintuitivo y conviene fijar antes de medir nada:

> El éxito no es que el agente use Nushell mucho. Es que lo use **pocas veces**, y precisamente
> cuando las estructuras tipadas reducen el parseo, los errores o el contexto. Una activación
> frecuente es un defecto de enrutamiento, no un logro.

La pregunta de cierre, antes de escribir `nu`: *¿estoy explotando datos tipados, o solo ejecutando un
comando a través de otra shell?* Si es lo segundo, no se usa.

## Qué construí

Poco, y a propósito. Nushell ya estaba instalado por `pacman`, así que no hubo que tocar el sistema.

- **Una skill** con la política de enrutamiento, proyectada por symlink a Claude Code y a Codex, y
  por transformación a Copilot.
- **Una regla de router** con términos deliberadamente estrechos. `json` a secas **no** está.
- **Un wrapper de sesenta líneas**, `nu-query`: `nu -n -c` sin configuración personal, timeout,
  contrato JSON forzado, tope de filas que **dice cuántas omitió** en vez de truncar en silencio, y
  una línea de registro con la forma y el coste —nunca el texto de la consulta—.

```json
{"rows_total": 462, "rows_shown": 2, "truncated": true, "data": [ … ]}
```

- **Dos gates**: casos de enrutamiento positivos y negativos, y un smoke que ejecuta los ejemplos
  reales de la skill contra el Nushell instalado.

Una decisión que quiero dejar por escrito: **el wrapper no está en la lista de permisos
autoaprobados, y es deliberado.** `nu -c` puede mutar el sistema; autorizarlo por patrón sería una
vía de escape al gestor de permisos. Evalué una lista negra de comandos peligrosos y la descarté:
una garantía basada en coincidencia de cadenas no es una garantía. Es fricción que decidí pagar.

### El gate se puso rojo el primer día, y estuvo bien

Escribí once casos negativos, uno por cada categoría que la política prohíbe enrutar a Nushell.
Diez pasaron. El undécimo no:

```text
"Instala nushell siguiendo la documentación oficial del proyecto."
  → regla structured_shell → skill activada
```

El término de enrutamiento era `nushell` a secas, así que cualquier frase que nombrara la herramienta
la activaba, incluida una instalación —que la propia política prohíbe—. El arreglo fue cambiarlo por
frases de uso: `en nushell`, `con nushell`, `usa nushell`, `nushell para`.

Después rompí el gate a propósito en las dos direcciones, porque **un gate que nunca se ha visto rojo
no es un gate**: quité un término positivo y el caso positivo reprobó; añadí `json` a los términos y
reprobó el negativo del `jq`. Restaurado, verde.

## Cinco trampas que aparecieron antes de escribir la primera tubería

Diagnostiqué el entorno antes de tocarlo. Esa fase produjo más valor que la integración misma.

### 1. `ls **/*` omite los ocultos, y no avisa

El glob de Nushell no desciende a `.git`, `.venv-*` ni a nada que empiece por punto. No hay error:
devuelve menos filas.

```bash
nu -n -c 'ls   **/* | where type == file | length'   # ≈ 46.400
nu -n -c 'ls -a **/* | where type == file | length'  # ≈ 127.900
```

**El 64 % del árbol es invisible por defecto.** Es el espejo de una trampa que ya tenía documentada
con `fd` y `rg`, que respetan `.gitignore` incluso cuando crees que no. Distinto criterio, mismo
síntoma: un conteo mucho menor de lo que sabes que hay.

### 2. Claude Code sombrea `find` y `grep` dentro de su propia herramienta Bash

Esta no la vi venir. El snapshot de shell que Claude Code inyecta en cada sesión contiene, literal:

```bash
# Shadow find/grep with embedded bfs/ugrep
unalias find 2>/dev/null || true
function find { … ARGV0=bfs "$_cc_bin" -S dfs -regextype findutils-default … }
```

Dentro de la herramienta Bash del agente, `find` **es `bfs`**, no GNU findutils. Y `bfs` rechaza la
sintaxis relativa que GNU sí acepta:

```bash
find . -type f -newermt '-30 days' -size +1M -printf '%s\t%p\n'
# bfs: error: Invalid timestamp.
```

El fallo real no fue el error, fue lo que vino después: con `2>/dev/null` dentro de una tubería, eso
devolvió **0 bytes con código de salida 0, en 14 ms**. Un falso negativo silencioso que se lee como
«no hay archivos grandes». Es exactamente la clase de divergencia entre implementaciones que Greenberg
y Blatt midieron entre siete shells[^smoosh], ocurriendo dos capas más arriba.

### 3. La salida por defecto está localizada, y eso la vuelve imposible de parsear

```text
╭───┬───────────────┬──────┬─────────┬──────────────╮
│ # │     name      │ type │  size   │   modified   │
├───┼───────────────┼──────┼─────────┼──────────────┤
│ 0 │ AGENTS.md     │ file │ 15,5 kB │ an hour ago  │
```

Caracteres de caja, líneas partidas, fechas relativas y **coma decimal de `es_CL`**: `15,5 kB`. El
contrato hacia un agente es siempre `| to json`. La tabla bonita es para el humano.

### 4. `from ndjson` no existe en 0.115.1

Docker y varios CLIs más emiten **NDJSON**: un objeto por línea, no un array. `from json` falla, y
`from nuon` da `error when loading nuon text`, que despista bastante. El patrón correcto:

```nu
docker ps -a --format json | lines | each {|l| $l | from json} | group-by Image
```

### 5. `ps | get cpu` no es el `%CPU` de `ps aux`

Nushell muestrea la CPU al instante; `ps` promedia sobre la vida del proceso. Medidos con segundos de
diferencia sobre los mismos PID:

| PID | proceso | `nu ps` cpu | `ps -eo pcpu` |
|---|---|---|---|
| 1146712 | llama-server | 0.00 | 18.2 |
| 1124940 | chrome | 281.25 | 500 |

La memoria sí es comparable. La CPU responde a preguntas distintas.

## Primer nivel de evidencia: tubería contra tubería

Lo que suele publicarse. Tres tareas donde la skill dice que Nushell aporta, más una cuarta que mide
la afirmación central sobre reducir contexto. Mediana de tres corridas; sin `hyperfine` en esta
máquina, así que diferencias bajo ~50 ms no las interpreto.

| Tarea | Variante | Pasos | Tiempo | Bytes |
|---|---|---|---|---|
| archivos >1 MB, últimos 30 días | `find+sort+head` | 3 | **317 ms** | 588 |
| archivos >1 MB, últimos 30 días | nushell | 1 | 1.137 ms | 971 |
| top 5 procesos por memoria | `ps+awk` | 3 | **17 ms** | 103 |
| top 5 procesos por memoria | nushell | 1 | 225 ms | 356 |
| contenedores por imagen | `docker+sort+uniq` | 3 | **16 ms** | 339 |
| contenedores por imagen | nushell | 1 | 33 ms | 603 |
| cuánto contexto entra | volcado crudo `docker ps -a` | 1 | 16 ms | **3.353** |
| cuánto contexto entra | nushell reducido | 1 | 32 ms | **566** |

<figure>
  <img src="/assets/images/structured-shell/fig-microbenchmark.svg"
       alt="Cuatro paneles con la distribución de tiempos por tarea; cada punto es una de las 25 corridas, con mediana e intervalo de confianza" loading="lazy">
</figure>

<figure>
  <iframe src="/assets/visores/structured-shell/index.html" title="Visor interactivo del benchmark"
          loading="lazy" style="width:100%;height:660px;border:1px solid #2a3041;border-radius:6px"></iframe>
  <figcaption style="font-size:.85em;opacity:.75;margin-top:.4em">
    Visor interactivo: cambia la tarea y la métrica, y salta al A/B de agente y al veredicto.
    Los datos vienen precomputados en R; la página sólo dibuja. Pesa 28 KB.
  </figcaption>
</figure>

La tabla de arriba resume; la figura muestra lo que la tabla esconde. Cada punto es una corrida
real. Con 25 por variante los intervalos son estrechos y el veredicto no admite discusión: el
cociente de medianas es **3,49×** en la tarea de archivos (IC 95 % [3,41; 3,57]) y **11,80×** en la
de procesos (IC 95 % [11,00; 12,15]). Nushell no pierde por poco.

**Nushell pierde en tiempo, siempre.** Hasta 3,6× más lento en el barrido del árbol: arranca un
intérprete y recorre sin las optimizaciones de `find`. Quien lo elija por velocidad se equivocó de
motivo.

**En resultados pequeños también pierde en bytes.** Cinco filas de JSON indentado pesan más que cinco
líneas de texto plano. La promesa de «menos salida» sólo se cumple cuando hay algo que reducir: en la
última fila, la pregunta se responde con 566 bytes en vez de un volcado de 3.353 —y el resumen trae
*más* información, porque incluye cuántos contenedores de cada imagen están corriendo—.

Donde gana es en pasos y en semántica: `size > 1mb` y `modified > ((date now) - 30day)` son
comparaciones tipadas; la versión Bash necesita `-printf`, una fecha absoluta calculada aparte y un
`sort -rn` sobre la columna correcta. Tres sitios donde equivocarse en silencio, contra cero.

Y hubo un rendimiento concreto. Esta consulta, mientras probaba la tercera tarea:

```nu
docker ps -a --format json | lines | each {|l| $l | from json}
  | where Image =~ "paper-search" | select ID State Status
```

devolvió **entre 7 y 10 contenedores del mismo servidor MCP corriendo a la vez**, el más antiguo con
`Up 16 hours`. Contenedores stdio huérfanos: cada sesión de editor levanta el suyo y nadie los
recicla. La información estaba en `docker ps -a` desde siempre, en un formato que nadie mira.

**Pero nada de esto responde la pregunta que importa.** Compara tuberías que escribí yo, así que mide
mi habilidad escribiendo tuberías. La pregunta real es si *el agente* resuelve mejor una solicitud en
lenguaje natural teniendo la skill. Eso exige otro experimento.

## Segundo nivel: agente contra agente

Cinco tareas en español —tres donde la política dice que Nushell aporta, dos donde lo prohíbe—,
pedidas a Claude Code headless (`claude -p --output-format json`, Sonnet). Lo único que cambia entre
brazos es si la skill está disponible. La verdad de cada tarea la calcula un comando independiente
**justo antes** de cada corrida, para que la volatilidad del entorno no se confunda con acierto. Los
comandos que realmente ejecutó el agente salen del transcript de la sesión, no de lo que dice haber
hecho.

### La primera versión no se activaba nunca

**Cero de quince.** Con la skill disponible, el agente no la invocó ni una vez, y el brazo con skill
era estadísticamente indistinguible del brazo sin ella: mismo acierto, mismos comandos, misma forma.
La skill era **inerte**.

El arreglo no fue intuición. La documentación de Claude Code dice tres cosas concretas que yo no
estaba cumpliendo: que la `description` debe **poner el caso de uso primero**, que existe un campo
`when_to_use` pensado justamente para *«trigger phrases or example requests»*, y que el texto
combinado **se trunca a 1.536 caracteres** —por el final, que es donde viven los ejemplos negativos—.
Mi descripción abría con filosofía de enrutamiento y no tenía `when_to_use`.

**Ronda 1.** Reescribí la descripción para que abriera con lo que responde, y añadí 18 frases
literales de petición y de rechazo. Activación: **0/9 → 5/9** en tareas positivas.

Mejor, pero a medias. Al mirar dónde fallaba apareció el dato útil: las fallas estaban repartidas
entre las tres tareas **con el mismo prompt exacto**. No era un hueco de vocabulario, era varianza.
Aun así había un desalineamiento concreto en la peor tarea: yo escribía «consumen más memoria» y el
prompt dice «los 3 procesos que más **memoria residente** están usando».

**Ronda 2.** Añadí 7 frases más apuntando a la redacción real, y una cláusula que neutraliza una señal
contraria que sospechaba: los tres prompts terminan en *«Responde SOLO… Sin explicaciones»*, así que
escribí que pedir la respuesta corta **restringe cómo presentar el dato, no cómo obtenerlo**.

Activación: **5/9 → 28/30** (93 %). Quedan 32 caracteres de margen bajo el tope; añadir más
frases ya exige quitar otras.

### Qué gana y qué cuesta

Estado final: **100 corridas** en dos tandas medidas por separado, 30 por brazo en las tareas
positivas y 20 en las negativas.

| Subconjunto | Brazo | Acierto | Activó la skill | Tiempo mediano | Tokens de salida |
|---|---|---|---|---|---|
| positivas | `sin_skill` | 23/30 | 0/30 | **6.239 ms** | **152** |
| positivas | `con_skill` | **30/30** | **28/30** | 9.537 ms | 368 |
| negativas | `sin_skill` | 20/20 | 0/20 | 5.220 ms | 91 |
| negativas | `con_skill` | 20/20 | **0/20** | 5.107 ms | 99 |

<figure>
  <img src="/assets/images/structured-shell/fig-ab-tiempo.svg"
       alt="Distribución de tiempos por brazo en tareas positivas, con una corrida atípica de 87 segundos" loading="lazy">
</figure>

Ese punto solitario arriba del todo es una corrida de **86.852 ms**, la primera en frío. Es el
motivo por el que en todo el post leo medianas y no medias: la media del brazo con skill es
14.428 ms contra una mediana de 9.537, inflada 1,5× por ese único valor. Con medias diría «2,3×
más lento»; el cociente de medianas es **1,53×**, con intervalo [1,26; 2,22].

<figure>
  <img src="/assets/images/structured-shell/fig-ab-tokens.svg"
       alt="Distribución de tokens de salida por brazo en tareas positivas" loading="lazy">
</figure>

En tokens el cociente es **2,43×** [1,22; 3,82]. Ese intervalo importa: con la mitad de la muestra
era [0,92; 4,18], **incluía el 1**, y por tanto no permitía afirmar que hubiera diferencia. Duplicar
las corridas fue lo que convirtió una impresión en un resultado.

<figure>
  <img src="/assets/images/structured-shell/fig-ab-proporciones.svg"
       alt="Acierto y activación por brazo con intervalos exactos de Clopper-Pearson" loading="lazy">
</figure>

Y el desglose que más me gustó: **en las tareas donde la skill no debe dispararse, no cuesta nada.**
5.220 ms contra 5.107, 91 tokens contra 99. Diferencias por debajo del ruido, y **0 activaciones de
20**. Subir la activación al 93 % no arrastró ni una sola activación indebida.

### La eficiencia, que es donde la skill no sale bien parada

Medianas separadas de acierto y de coste esconden la pregunta que de verdad importa: *¿cuánto
cuesta una respuesta que sirve?* Esa métrica combina ambos ejes y penaliza al brazo barato que se
equivoca.

<figure>
  <img src="/assets/images/structured-shell/fig-eficiencia.svg"
       alt="Coste por respuesta correcta en tokens y segundos, con intervalos que se solapan" loading="lazy">
</figure>

**No compensa.** 458 tokens por acierto con la skill contra 300 sin ella; 14,4 segundos contra 9,3.
El acierto extra no paga su propio coste. Los intervalos se solapan, así que no hay evidencia de
diferencia — y el solape es una prueba conservadora, no una absolución.

Si tu criterio es «minimizar tokens por respuesta útil», este resultado dice que no actives la
skill. Si es «no equivocarte en consultas de metadatos», dice lo contrario. La medición no elige
por ti; sólo impide que elijas creyendo algo falso.

### La tarea que decide, y por qué falla sin la skill

La tarea discriminante es *«los 3 archivos más grandes de más de 1 MB modificados en los últimos 30
días»*. Sin la skill: **3 de 10**. Con ella: **10 de 10**.

El motivo no tiene nada que ver con Nushell. **Cuatro de las cinco corridas sin skill resolvieron con
`fd -I … --changed-within 30d`**, y perdieron un archivo de 434 MB que vive dentro de
`.venv-qwen-staging`. `fd -I` levanta el `.gitignore`, **pero sigue omitiendo los ocultos**: para eso
hace falta `-H`, que es otra bandera. Las que acertaron usaron `find`.

Con la skill activa, las diez corridas usaron `ls -a **/*` y las diez acertaron. El mecanismo es
verificable en los transcripts, no inferido: la skill documenta esa trampa en su primera página de
gotchas, el agente la lee, y aplica el `-a`.

Y `fd` por encima de `find` es una preferencia que impone mi propio archivo de instrucciones globales,
junto con el aviso de usar `-I`. El aviso está incompleto, y esa instrucción está produciendo
respuestas incorrectas en toda una clase de tareas. Lo encontré midiendo otra cosa.

### La sexta trampa, que sólo el experimento podía encontrar

Mirando los outliers apareció el mejor hallazgo del trabajo. Una corrida gastó **77 segundos, 15
turnos y 3.714 tokens de salida**, contra una mediana de 15 segundos para esa tarea. Fui a leer qué
había hecho:

```text
docker ps -a --format json | nu -n -c 'lines | each {|l| $l | from json} | group-by image …'
docker ps -a --format json | head -c 300      # ¿qué está llegando?
echo hello | nu -n -c '$in'; echo "exit:$?"   # ¿entra algo por stdin?
nu --help 2>&1 | rg -i "stdin|--commands"
cat penta-agent/scripts/agent/nu-query | head -60   # se puso a leer mi wrapper
```

Estaba peleando con esto, y la culpa era mía:

```bash
printf 'a\nb\n' | nu -n -c 'lines | to json --raw'
# null
# exit=0
```

**`nu -n -c` no lee stdin.** Un pipe de Bash hacia él se ignora, la tubería recibe `nothing`, y
devuelve `null` **con código de salida 0**. No falla: miente. Para un agente eso es mucho peor que un
error, porque parece una respuesta.

Y el origen estaba en mis ejemplos. La skill escribía `docker ps -a --format json | lines | each
{...}`, que es una tubería **interna de Nushell** pero se lee exactamente igual que una de Bash. El
agente hizo lo razonable y se estrelló contra un fallo silencioso.

```bash
# el comando externo va DENTRO, entre paréntesis  ← el preferido
nu -n -c '(docker ps -a --format json) | lines | each {|l| $l | from json} | group-by Image'

# o, si el dato ya viene por una tubería de Bash, hace falta --stdin
docker ps -a --format json | nu -n --stdin -c 'lines | each {|l| $l | from json}'
```

Además `nu-query` ahora detecta stdin y añade `--stdin` sólo cuando hace falta, y el smoke vigila las
tres cosas. El efecto, midiendo sólo esa tarea antes y después:

| | Tiempo | Tokens salida | Turnos | Tool calls |
|---|---|---|---|---|
| antes | 70.901 ms | 3.287 | 14 | 12 |
| después | **7.852 ms** | **303** | 4 | 2 |

**9× más rápido y 10,8× menos tokens, sin tocar una línea de Nushell.** Sólo aclarando la
documentación de la skill y dándole stdin al wrapper.

### Lo que este experimento no prueba

Cinco tareas, cinco repeticiones, un solo modelo, una sola máquina. Con n bajo, una diferencia de 1/3
contra 0/3 es ruido: la primera repetición de una ronda sugirió que la skill ganaba 3/3 en la tarea
difícil, y las siguientes lo deshicieron. Descarté además las columnas de coste y de tokens *nuevos*:
dependen de si la corrida pegó en la caché de prompt de la API, y la misma tarea en el mismo brazo
daba 26.293 tokens en una corrida y 188 en otra.

Y una advertencia sobre el afinado: **medí, cambié la descripción y volví a medir sobre las mismas
cinco tareas.** Eso corre el riesgo de ajustar a la prueba en vez de al problema. Las frases que
añadí son genéricas y no copian los prompts, pero la única forma de descartarlo del todo es un
conjunto de tareas nuevo que la descripción no haya visto. No lo hice.

## Cómo se leyeron los números, y por qué hizo falta un visor

Toda la primera versión de este post reportaba medianas en tablas. Una mediana sin su distribución
invita a leer como señal lo que puede ser ruido de muestreo, y aquí eso no era teórico: el
microbenchmark **sólo guardaba la mediana y tiraba cada corrida**. No se podía ver dispersión, ni
detectar un atípico, ni poner un intervalo. Lo primero fue cambiarlo para que emitiera una línea por
corrida; de ahí salen las 200 del primer nivel y las 100 del segundo.

El análisis va en R sobre un entorno conda aislado (`/opt/entornos/r-geo`, R 4.5.3), y el visor es
una app Shiny de cuatro pestañas que se levanta en local:

```bash
/opt/entornos/r-geo/bin/Rscript -e 'shiny::runApp("app.R", port = 4005)'
```

Cinco decisiones estadísticas, y la razón de cada una:

**Mediana, nunca media.** Ya se vio: un valor de 87 segundos infla la media 1,5×. El atípico no se
descarta —descartar datos incómodos es cómo se fabrica un resultado— sino que se muestra y se usa un
estimador que no se deja arrastrar.

**Bootstrap de percentiles, no prueba t.** Con 5 corridas por celda y distribuciones asimétricas con
cola derecha, el supuesto de normalidad no se sostiene. Diez mil remuestreos dan el intervalo de la
mediana sin suponer nada sobre la forma.

**Clopper-Pearson exacto para las proporciones.** Con 30 aciertos de 30, el método normal da un
intervalo de ancho cero, [1; 1], que afirma certeza absoluta a partir de 30 observaciones. El exacto
da [0,88; 1], que es lo que la evidencia permite decir.

**Cociente de medianas como medida de efecto.** «Cuántas veces más» se puede comparar entre tareas;
una diferencia en milisegundos, no. Y tiene una propiedad útil: **si el intervalo cruza el 1, no hay
resultado.** Es un criterio de parada, no una decoración.

**Fisher exacto para la tabla 2×2** del acierto, que es lo que corresponde con conteos bajos.

Nada de esto necesitó instalar paquetes: `boot` y `binom` no están en ese entorno, y tanto el
bootstrap como Clopper-Pearson salen de R base en veinte líneas.

### Lo que el rigor cambió, y no fue cosmético

Con la primera mitad de la muestra, esto era lo que había:

| Efecto | n = 15 por brazo | n = 30 por brazo |
|---|---|---|
| Tiempo | 1,70× [1,19; 3,11] · concluyente | **1,53× [1,26; 2,22]** · concluyente |
| Tokens | 2,39× **[0,92; 4,18]** · el IC cruza el 1 | **2,43× [1,22; 3,82]** · concluyente |
| Acierto | Fisher **p = 0,0996** | Fisher **p = 0,0105** |

Dos de los tres efectos que yo daba por buenos **no eran afirmables** con la muestra que tenía. No
lo supe hasta calcular los intervalos, y la respuesta correcta no fue rebajar el titular: fue correr
cincuenta corridas más. También comprobé que las dos tandas no difieren entre sí antes de juntarlas
—medianas de 5.660 y 6.381 ms sin skill, 9.650 y 9.424 con ella—, porque agrupar datos de momentos
distintos sin mirar es otra forma de fabricar un resultado.

Ese es el argumento entero a favor de las herramientas estadísticas en un post técnico: no adornan
la conclusión, la **cambian**. Y son baratas: el visor y las métricas son unas trescientas líneas de
R sobre datos que ya existían.

## Veredicto

Los gates pasan, la skill llega a los dos agentes y el enrutamiento se sostiene en las dos
direcciones. Medido a nivel de agente en 100 corridas, y con los efectos que **sí** son afirmables:

- **Logro:** gana. 30/30 contra 23/30 en tareas positivas, Fisher exacto **p = 0,0105**. En la tarea
  difícil, 10/10 contra 3/10.
- **Activación:** de 0 % a **93 %** (28 de 30), en dos rondas de afinado de la descripción.
- **Sobreactivación:** ninguna. **0 de 20**, con la redacción más agresiva.
- **Coste donde no le toca:** cero. 5.220 ms contra 5.107, por debajo del ruido.
- **Coste donde sí le toca:** **1,53×** el tiempo [1,26; 2,22] y **2,43×** los tokens [1,22; 3,82].
- **Eficiencia:** **no compensa**. 458 tokens por acierto contra 300. El acierto extra no paga su
  coste, aunque los intervalos se solapan y eso no es concluyente.

Ese perfil es defendible con una condición: que sepas qué estás optimizando. No estorba donde no
aplica, acierta donde aplica, y cuesta más por respuesta útil. Si tu cuello de botella son los
tokens, no la actives; si es equivocarte en consultas de metadatos, sí.

No implementé un MCP, y eso que la vía está servida: `nu 0.115.1` trae modo servidor MCP en el
propio binario. Precisamente por eso la respuesta es no, todavía: una operación se promueve a
herramienta dedicada sólo si aparece repetidamente, tiene interfaz estable, se puede definir con
parámetros tipados, la reutilizarían varios agentes y hay ventaja real de seguridad u
observabilidad. Tengo dos candidatas anotadas y ninguna cumple las cinco.

Lo que me llevo no es sobre Nushell. Es que hubo **tres niveles de evidencia y cada uno desmintió al
anterior**. El microbenchmark decía que Nushell era más lento y poco más. El A/B de agente descubrió
que la skill no se activaba nunca —y que arreglarlo cambiaba el resultado por completo—. Y las
métricas robustas mostraron que dos de los tres efectos que yo daba por buenos no eran afirmables
con la muestra que tenía.

Ninguno de los tres niveles salió de leer código. Salieron de medir, de mirar la distribución en vez
del resumen, y de aceptar que «no se puede concluir» es una conclusión.

## Referencias

[^smoosh]: Michael Greenberg y Austin J. Blatt, «Executable formal semantics for the POSIX shell», *Proceedings of the ACM on Programming Languages* 4, n.º POPL (2019): 1-30. <https://doi.org/10.1145/3371111>

[^next50]: Michael Greenberg, Konstantinos Kallas y Nikos Vasilakis, «Unix shell programming», *Proceedings of the Workshop on Hot Topics in Operating Systems* (HotOS '21), 104-111. <https://doi.org/10.1145/3458336.3465294>

[^dataflow]: Shivam Handa, Konstantinos Kallas, Nikos Vasilakis y Martin C. Rinard, «An order-aware dataflow model for parallel Unix pipelines», *Proceedings of the ACM on Programming Languages* 5, n.º ICFP (2021): 1-28. <https://doi.org/10.1145/3473570>

[^nushell]: Nushell, «A new type of shell», sitio oficial del proyecto, consultado el 29 de agosto de 2026. <https://www.nushell.sh/>
