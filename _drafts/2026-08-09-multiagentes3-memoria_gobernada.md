---
layout: single
title: "Multiagentes en 3 cucharadas 3.0: recordar no basta"
subtitle: "De excavar historiales con Déjà Vu a gobernar hechos, versiones y acciones con una memoria temporal verificable"
date: 2026-08-09 00:00:00 -0400
published: false
categories: [ia, productividad, desarrollo, multiagente]
tags:
  - multiagente
  - memoria-agentes
  - deja-vu
  - cass
  - mempalace
  - engram
  - graphiti
  - ontologias
  - knowledge-graph
  - temporal-memory
  - provenance
  - qdrant
  - bge-m3
  - mcp
  - sqlite
  - shacl
  - foss
description: "Tercera bitácora del penta-agent: qué enseñan Déjà Vu, Cass, MemPalace, Engram, Graphiti, Open Ontologies y la investigación reciente sobre memoria de agentes, y cómo convertir esas ideas en una PoC local, temporal, trazable y capaz de fundamentar acciones seguras."
excerpt: "Un agente puede recuperar con precisión la versión equivocada. La siguiente etapa no consiste en almacenar más recuerdos, sino en gobernar su procedencia, vigencia, autoridad y ámbito antes de utilizarlos."
author: clabra
lang: es
ref: multiagente-penta-agent-memoria-gobernada
permalink: /ia/productividad/desarrollo/multiagente-memoria-gobernada/
toc: true
toc_sticky: true
comments: true
author_profile: true
math: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria-gobernada.webp
---

<!--
PROPUESTA DE BORRADOR. NO PUBLICAR TODAVÍA.

Estado: diseño editorial y técnico; PoC aún no ejecutada.
Antes de publicar:
1. ejecutar la PoC;
2. reemplazar todos los campos «PENDIENTE» por resultados medidos;
3. revisar versiones, licencias y comportamiento efectivo de las dependencias instaladas;
4. incorporar capturas o diagramas generados por la propia PoC;
5. ejecutar el golden set completo y conservar su reporte;
6. construir Jekyll en el repositorio real y revisar enlaces, tablas, código y notas al pie;
7. verificar que ningún insumo público contenga conversaciones, rutas, correos, tokens o datos laborales sensibles.
-->

> **Estado de esta entrada.** El preámbulo y las dos primeras cucharadas pueden cerrarse con revisión documental. La tercera propone una prueba de concepto reproducible; por tanto, sus umbrales son **criterios de aceptación**, no resultados. La entrada solo debería publicarse después de ejecutar la PoC y sustituir los marcadores pendientes por evidencia observada.
{: .notice--warning}

Prometí que el tercer post mostraría esta memoria en 3D. Antes de abrir Three.js apareció un problema menos vistoso y bastante más importante: **todavía no había decidido qué merecía convertirse en nodo**.
{: .text-justify}

En el [post anterior](/ia/productividad/desarrollo/multiagente-penta-agent-memoria/) dejé un RAG local que encontraba decisiones por significado, combinaba recuperación semántica y literal, reordenaba los resultados y —la virtud menos vistosa— sabía abstenerse cuando el corpus no contenía una respuesta. Sobre el mismo *golden set* de 40 casos, la combinación final con BGE-M3, BM25, Reciprocal Rank Fusion y *reranking* alcanzó `recall@5 = 0,99`, `MRR = 0,97` y abstención perfecta en los negativos.[^post2] El avance era real. También medía una pregunta más fácil de lo que parecía: **¿aparece arriba un documento relevante?**
{: .text-justify}

No medía otra bastante más incómoda: **¿lo que aparece sigue siendo verdad?**
{: .text-justify}

Un sistema puede recuperar con gran precisión la versión equivocada de un hecho. Puede encontrar el modelo de *embeddings* que usaba hace seis meses, una ruta que ya cambió, una decisión descartada durante una sesión o una hipótesis que el agente escribió con la misma seguridad tipográfica que el resultado final. Recordar con precisión no equivale a recordar correctamente.
{: .text-justify}

Tampoco basta con añadir todos los historiales. En una conversación conviven la decisión vigente, tres alternativas fallidas, una instrucción transitoria, un error corregido, el diagnóstico que lo corrigió y alguna frase del agente que nadie aprobó. Si convierto todo eso en nodos equivalentes, no obtengo conocimiento: obtengo **una contradicción con iluminación WebGL**.
{: .text-justify}

Para entender qué faltaba revisé proyectos que hoy abordan distintas partes del problema: Déjà Vu, Cass y MemPalace recuperan el rastro que los agentes ya dejaron; Engram, Mem0 y Letta administran recuerdos persistentes hacia adelante; Graphiti, Hindsight, Cognee y A-MEM relacionan hechos, episodios o inferencias; Open Ontologies trabaja sobre vocabularios, restricciones, validación y linaje formal. Todos hablan de «memoria», pero no están resolviendo la misma pregunta.[^deja][^cass][^mempalace][^engram][^mem0-paper][^letta][^graphiti][^hindsight][^cognee][^amem][^open-ontologies]
{: .text-justify}

La distinción que terminó ordenando este recorrido cabe en una línea:
{: .text-justify}

> **El historial conserva; el índice encuentra; el grafo relaciona; la ontología restringe; un registro canónico decide qué sigue vigente.**

La última pieza no suele venir resuelta. Un grafo de conocimiento puede representar que dos afirmaciones se contradicen, pero no necesariamente sabe cuál tiene autoridad. Una ontología puede impedir que una `Hipótesis` sea tipada como `DecisiónAprobada`, pero no determina por sí sola si la persona efectivamente aprobó esa decisión. Una base vectorial puede hallar ambos fragmentos y seguir siendo completamente agnóstica respecto de cuál debe entrar al contexto.
{: .text-justify}

La mejor advertencia vino, irónicamente, del proyecto más explícitamente ontológico de la revisión. Open Ontologies retiró sus vistas D3 y 3D cuando dejaron de escalar: el árbol comenzaba a degradarse con cientos de nodos y el grafo tridimensional podía congelar la interfaz sobre el millar. Lo reemplazó por una jerarquía virtualizada, menos espectacular y bastante más utilizable.[^open-ontologies] La herramienta que más literalmente debía «mostrar una ontología» terminó recordando que **ver el cerebro no equivale a entenderlo**.
{: .text-justify}

La tercera entrada cambia entonces de objetivo. El grafo seguirá apareciendo —incluso puede terminar en 3D—, pero será una vista derivada de información gobernada, no el lugar donde se decide qué es verdad. Primero necesito que la memoria pueda responder cinco preguntas simples y exigentes: **qué se afirmó, de dónde salió, desde cuándo vale, en qué ámbito puede usarse y qué acción segura permite fundamentar**.
{: .text-justify}

Ahora sí, las tres cucharadas.
{: .text-justify}

## Cucharada 1: un historial no es una memoria

### Cuatro capas que suelen confundirse

En sentido técnico estricto, una ontología no es cualquier conjunto de nodos y aristas. OWL 2, la recomendación del W3C, ofrece clases, propiedades, individuos y semántica formal; SHACL permite validar grafos RDF contra restricciones explícitas.[^owl][^shacl] Un grafo puede usar una ontología, pero no se vuelve ontología solo porque sus nodos floten con elegancia.
{: .text-justify}

Para esta revisión separé cuatro familias funcionales:
{: .text-justify}

| Capa | Pregunta que responde | Ejemplos | Lo que deja pendiente |
|---|---|---|---|
| **Archivo episódico** | ¿Qué ocurrió exactamente? | Déjà Vu, Cass, MemPalace | Qué parte fue correcta, aprobada o vigente |
| **Memoria operativa** | ¿Qué conviene guardar y volver a utilizar? | Engram, Mem0, Letta | Quién tiene autoridad para promover o revocar |
| **Grafo temporal o reflexivo** | ¿Qué entidades, hechos y experiencias se relacionan y cuándo? | Graphiti, Hindsight, Cognee, A-MEM | Una adjudicación canónica y verificable |
| **Ontología y validación** | ¿Qué tipos, relaciones y restricciones son admisibles? | Open Ontologies, OWL, SHACL | Captura de sesiones, recuperación y aprobación humana |

Esta separación evita dos errores. El primero es comparar herramientas que miden objetos distintos: recuperar la sesión correcta no equivale a responder bien una pregunta, y responder bien tampoco equivale a seleccionar correctamente una herramienta y sus parámetros. El segundo es confundir amplitud con madurez: una plataforma que ofrece vectores, grafos, agentes y una nube administrada puede ser muy completa y, a la vez, no resolver la regla específica que necesito.
{: .text-justify}

### 1. Excavar el pasado: Déjà Vu, Cass y MemPalace

**Déjà Vu**, de Vladislav Shulcz, parte de una tesis minimalista y potente: los agentes ya escribieron meses de memoria en sus archivos locales; el primer problema es volverla consultable. Indexa retrospectivamente historiales de múltiples *harnesses*, los expone por MCP, aplica redacción de secretos, registra qué memoria fue inyectada y permite transportar el contexto entre agentes y máquinas. Su núcleo funciona sin LLM ni *embeddings*, aunque el proyecto ha ido sumando búsqueda por niveles, notas durables, auditoría y sincronización.[^deja]
{: .text-justify}

Su virtud principal es epistemológica: **no obliga a resumir antes de saber qué pregunta aparecerá después**. Si una sesión contenía una solución, su error previo y el comando que finalmente funcionó, el episodio original permanece disponible. Para mi sistema, Déjà Vu calza bien como capa de evidencia retrospectiva y como adaptador entre historiales de Codex, Claude, Gemini y otros agentes.
{: .text-justify}

Su límite es igualmente claro. Encontrar la sesión correcta no adjudica sus afirmaciones. El buscador puede devolver la decisión vigente, la alternativa que se descartó cinco minutos antes y una sugerencia del agente que nunca llegó al código. Déjà Vu conserva y encuentra; no debería convertirse, sin otra capa, en la fuente canónica del estado actual.
{: .text-justify}

**Cass** —*Coding Agent Session Search*, de Jeffrey Emanuel— resuelve un problema vecino con una apuesta más amplia por la normalización: unifica formatos heterogéneos de historiales, construye un índice local y ofrece salidas estructuradas para que otros agentes consulten lo ocurrido en herramientas distintas.[^cass] Su valor aumenta cuando el corpus está repartido entre JSONL, SQLite y formatos propietarios, o cuando importa mantener un contrato estable para automatizaciones.
{: .text-justify}

Respecto de Déjà Vu, Cass parece más cercano a una capa de búsqueda multiformato y análisis transversal; Déjà Vu enfatiza la recuperación retroactiva directa, la redacción, el MCP y la continuidad entre *harnesses*. En mi arquitectura no adoptaría ambos de inmediato. Los pondría detrás de una misma interfaz de evidencia y mediría cuál recupera mejor mis sesiones reales con menor carga operacional.
{: .text-justify}

**MemPalace**, mantenido por sus contribuyentes, lleva más lejos la defensa de la evidencia literal: almacena el texto de manera textual y declara que no resume, extrae ni parafrasea durante la escritura. Organiza el corpus en una estructura de «alas», «habitaciones» y «cajones», usa ChromaDB por defecto y admite otros *backends*, incluido Qdrant.[^mempalace] La intuición es razonable: una compresión irreversible al ingresar puede borrar precisamente el detalle que una consulta futura necesita.
{: .text-justify}

Esa decisión desplaza el problema, no lo elimina. Conservarlo todo protege la fuente, pero obliga a resolver ruido, contradicción, vigencia y autoridad al recuperar. MemPalace resulta atractivo como bóveda de evidencia y como comparador sobre Qdrant; es menos convincente como sustituto completo de una memoria curada. Hay además una precaución práctica: el propio proyecto advierte sobre sitios impostores y reconoce como oficiales únicamente su repositorio, su paquete en PyPI y su dominio documental declarado.[^mempalace]
{: .text-justify}

### 2. Recordar hacia adelante: Engram, Mem0 y Letta

**Engram**, del proyecto Gentleman Programming, comienza vacío y depende de que los agentes guarden decisiones, correcciones, patrones o preferencias. Usa un binario en Go, SQLite con FTS5 y herramientas MCP para guardar, actualizar, eliminar, buscar, reconstruir líneas temporales y exponer conflictos mediante operaciones como `mem_judge` y `mem_compare`.[^engram] Su SQLite local permanece como fuente de verdad, mientras la sincronización o nube es optativa.
{: .text-justify}

Engram aporta algo que los buscadores retrospectivos no necesitan decidir: **un protocolo de promoción**. No todo turno merece memoria; alguien —el agente, una regla o la persona— selecciona qué sobrevive. También muestra que los conflictos deben aflorar, no resolverse silenciosamente detrás de una puntuación de similitud.
{: .text-justify}

El riesgo está en el punto de captura. Si el mismo agente que puede interpretar mal una conversación decide qué guardar y cómo resumirla, un error local adquiere persistencia. La solución no es rechazar la memoria curada, sino conservar siempre el episodio fuente y distinguir `candidato`, `aceptado`, `rechazado`, `superado`, `obsoleto` y `revocado`.
{: .text-justify}

**Mem0**, presentado por Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh y Deshraj Yadav, propone una capa de memoria escalable que extrae, consolida y recupera elementos relevantes de conversaciones; su variante gráfica añade relaciones entre esos elementos.[^mem0-paper] El repositorio actual combina señales semánticas, léxicas, de entidades y temporales. Su algoritmo anunciado en abril de 2026 privilegia la adición acumulativa y evita actualizar o eliminar memorias durante la extracción.[^mem0-repo]
{: .text-justify}

Esa estrategia reduce el riesgo de borrar historia por una decisión automática equivocada. Sin embargo, una bitácora acumulativa no es por sí sola una representación del presente. Si dos recuerdos incompatibles continúan juntos y el recuperador debe resolverlos en cada consulta, la «verdad vigente» queda nuevamente delegada al momento más frágil. Para mi uso, toda memoria generada por el agente debe llevar una autoridad distinta de una decisión explícita del usuario o de un artefacto aprobado.
{: .text-justify}

**MemGPT**, de Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica y Joseph E. Gonzalez, introdujo una analogía influyente entre la gestión del contexto de un LLM y las jerarquías de memoria de un sistema operativo.[^memgpt] Su continuidad práctica es **Letta**, una plataforma para agentes persistentes que administran bloques de memoria, herramientas, habilidades y estado entre sesiones.[^letta]
{: .text-justify}

Letta muestra cómo se ve un agente diseñado desde el origen para recordar. Precisamente por eso no es una dependencia pequeña: adoptarlo significaría aproximarse a un nuevo *runtime*, no añadir una biblioteca al `penta-agent`. Su arquitectura es una referencia valiosa; una migración completa solo tendría sentido si decidiera reemplazar deliberadamente parte de mi orquestación actual.
{: .text-justify}

### 3. Relacionar, temporalizar y reflexionar: Graphiti, Hindsight, Cognee y A-MEM

**Graphiti**, el motor abierto que sustenta la propuesta de Zep, convierte episodios en un grafo temporal. El trabajo de Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan y Daniel Chalef describe una arquitectura que mantiene relaciones históricas y sintetiza información conversacional y estructurada.[^zep] El repositorio permite asociar hechos con procedencia y ventanas de validez, y combinar recuperación semántica, léxica y gráfica.[^graphiti]
{: .text-justify}

Graphiti es el proyecto que más directamente responde al vacío del post II: una relación anterior puede dejar de estar vigente sin desaparecer de la historia. Permite representar, por ejemplo, que `penta-agent usa bge-small-en` fue válido hasta cierta fecha y que `penta-agent usa BGE-M3` comenzó después.
{: .text-justify}

Aun así, una arista extraída por un LLM no se convierte en hecho por entrar a Neo4j, FalkorDB o cualquier otro grafo. La extracción puede confundir propuesta, intención, ejecución y resultado. Mi adopción prudente sería un **grafo sombra**: Graphiti recibiría únicamente afirmaciones ya vinculadas a evidencia y estados, y durante la PoC no tendría autoridad para modificar el registro canónico.
{: .text-justify}

**Hindsight**, desarrollado por Vectorize, separa hechos acerca del mundo, experiencias del agente y «modelos mentales» sintetizados. Sus operaciones `Retain`, `Recall` y `Reflect` combinan recuperación semántica, BM25, señales temporales y relaciones, antes de fusionar y reordenar resultados.[^hindsight]
{: .text-justify}

La separación es conceptualmente útil. Una experiencia como «la actualización de vLLM falló en esta V100» no es idéntica a una regla general como «verificar soporte `sm_70` antes de actualizar». La segunda puede ahorrar trabajo, pero sigue siendo una inferencia. Debe conservar sus episodios de respaldo, su ámbito y la posibilidad de rechazo. Una memoria que aprende sin distinguir aprendizaje de hecho produce reglas convincentes y difíciles de auditar.
{: .text-justify}

**Cognee**, mantenido por Topoteretes y su comunidad, se presenta como una capa de control que combina *embeddings*, grafos y anclaje ontológico. Sus operaciones `remember`, `recall`, `forget` e `improve`, además de sus integraciones con ciclos de agentes, buscan transformar fuentes heterogéneas en conocimiento reutilizable.[^cognee]
{: .text-justify}

Su amplitud calza con una ambición posterior —correo, documentos, notas y conversaciones en una infraestructura común—, pero introduce muchas decisiones a la vez. Antes de adoptarlo como «cerebro», necesito estabilizar un contrato más pequeño: qué es una afirmación, cómo se prueba, quién puede aprobarla y cuándo deja de ser utilizable.
{: .text-justify}

**A-MEM**, de Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan y Yongfeng Zhang, toma inspiración del método Zettelkasten: crea notas estructuradas, detecta vínculos y permite que memorias nuevas modifiquen la organización o descripción de las anteriores.[^amem] Su intuición inductiva es valiosa: las categorías pueden emerger del corpus, en vez de diseñarse completamente antes de observarlo.
{: .text-justify}

El límite vuelve a ser la trazabilidad. Una representación histórica puede evolucionar; la evidencia histórica no debería reescribirse. Mi diseño separará ambos objetos: el texto fuente queda inmutable y toda reinterpretación entra como un evento nuevo.
{: .text-justify}

### 4. Restringir el significado: Open Ontologies

**Open Ontologies**, de Fabio Rovai, es el proyecto más propiamente ontológico de esta revisión. Implementa herramientas para RDF, OWL, SHACL y SPARQL, junto con validación, razonamiento, diferencias entre versiones, linaje y gobierno mediante MCP.[^open-ontologies]
{: .text-justify}

Eso permite expresar reglas que una base vectorial no conoce:
{: .text-justify}

```text
Clase: Decisión
Clase: Hipótesis
Clase: Procedimiento
Clase: Evidencia

Decisión debe_tener_fuente Evidencia
Hipótesis no_puede_reemplazar Decisión
Procedimiento aplica_en Ámbito
AfirmaciónAceptada debe_tener_autoridad Autoridad
```

SHACL puede además rechazar una memoria marcada como aceptada si carece de fuente, alcance o fecha. El valor no está en dibujar el grafo, sino en convertir algunas condiciones editoriales y epistemológicas en pruebas automáticas.
{: .text-justify}

Open Ontologies no resuelve la captura de sesiones ni decide qué afirmación humana fue aprobada. Tampoco sus evaluaciones propias deben tratarse como validación independiente. Su mejor encaje sería posterior y acotado: exportar el registro canónico a RDF, validar formas mínimas y explorar si una ontología pequeña mejora la interoperabilidad sin imponer complejidad prematura.
{: .text-justify}

### No hay un ganador general

| Sistema | Autoría o mantenedor principal | Tesis central | Aporte que tomaría | Límite para mi caso | Papel en la PoC |
|---|---|---|---|---|---|
| **Déjà Vu** | Vladislav Shulcz | Los historiales existentes ya contienen memoria recuperable | Ingesta retrospectiva, redacción, MCP y auditoría | No adjudica automáticamente vigencia o autoridad | Adaptador opcional de evidencia |
| **Cass** | Jeffrey Emanuel | Normalizar y buscar historiales heterogéneos | Esquema común y salida estructurada | Se superpone con mi índice híbrido | Comparador de ingesta/búsqueda |
| **MemPalace** | Contribuyentes de MemPalace | Conservar literalmente antes de interpretar | Evidencia sin compresión prematura | Traslada ruido y contradicciones a la recuperación | Comparador *lossless* sobre Qdrant |
| **Engram** | Gentleman Programming | Guardar recuerdos operativos curados | Estados, líneas temporales y conflictos visibles | Depende de la calidad del guardado del agente | Inspiración para operaciones y CLI |
| **Mem0** | Chhikara et al.; Mem0 | Extraer y recuperar memorias escalables | Señales múltiples y enlaces de entidad | Acumulación no equivale a estado vigente | Referencia, no fuente canónica |
| **Letta/MemGPT** | Packer et al.; Letta | El agente completo administra memoria persistente | Bloques y gestión activa de contexto | Requiere replatformizar parte del sistema | Referencia conceptual |
| **Graphiti/Zep** | Rasmussen et al.; Zep | La memoria es un grafo temporal de episodios y hechos | Validez, procedencia y relaciones históricas | La extracción automática no prueba autoridad | Grafo sombra opcional |
| **Hindsight** | Vectorize | Los agentes deben aprender de experiencias | Separación entre hechos, experiencias e inferencias | Los «modelos mentales» pueden sobre-generalizar | Capa experimental de lecciones |
| **Cognee** | Topoteretes/Cognee | Vectores, grafos y ontología como plano de control | Ingesta transversal y trazabilidad | Alcance demasiado amplio para aislar causalidad | Evaluación posterior |
| **A-MEM** | Xu et al. | Memoria autoorganizada tipo Zettelkasten | Enlaces emergentes y notas evolutivas | Riesgo de deriva semántica | Inspiración para relaciones candidatas |
| **Open Ontologies** | Fabio Rovai | Gobernar conocimiento mediante semántica formal | OWL, SHACL, linaje y validación | No captura ni adjudica conversaciones | Validador RDF opcional |

Las cifras publicadas por estos proyectos no producen un ranking honesto. Unos informan recuperación de sesiones, otros exactitud de respuesta final, otros métricas juzgadas por LLM, y algunos mezclan versión abierta con plataforma administrada. La popularidad en GitHub tampoco prueba corrección, privacidad ni ajuste a mi corpus. El experimento útil debe mantener constantes el corpus, el hardware, el modelo lector y las preguntas.
{: .text-justify}

La conclusión de esta primera cucharada es menos comercial, pero más útil: **no necesito reemplazar todo el sistema; necesito ordenar las responsabilidades que hoy están mezcladas**.
{: .text-justify}

## Cucharada 2: recordar con fecha, procedencia y permiso

### La arquitectura: evidencia primero, proyecciones después

La propuesta toma ideas de varios proyectos, pero fija una regla propia: ni Qdrant, ni el grafo, ni la ontología serán la fuente primaria de verdad. Todos deben poder reconstruirse desde dos objetos más simples:
{: .text-justify}

1. un archivo inmutable de evidencia;
2. un registro `append-only` de afirmaciones y cambios de estado.

```text
Claude · Codex · Gemini · handoffs · archivos
                    │
                    ▼
┌───────────────────────────────────────────┐
│ 1. ARCHIVO INMUTABLE DE EVIDENCIA         │
│ texto original · hash · fecha · agente    │
│ proyecto · ámbito · sensibilidad          │
└─────────────────────┬─────────────────────┘
                      │ extracción candidata
                      ▼
┌───────────────────────────────────────────┐
│ 2. REGISTRO CANÓNICO APPEND-ONLY          │
│ afirmaciones · fuentes · autoridad        │
│ validez · estados · supersesión           │
└───────────┬─────────────────┬─────────────┘
            │                 │
            ▼                 ▼
┌────────────────────┐  ┌────────────────────┐
│ 3. CURRENT_MEMORY  │  │ 4. HISTORIA        │
│ proyección vigente │  │ estado a una fecha │
└───────────┬────────┘  └──────────┬─────────┘
            │                      │
            ├──────────┬───────────┤
            ▼          ▼           ▼
      Qdrant/BGE-M3  grafo       RDF/SHACL
      recuperación   sombra      validación
            └──────────┬───────────┘
                       ▼
┌───────────────────────────────────────────┐
│ 5. COMPUERTA DE ADMISIÓN                  │
│ ámbito · vigencia · autoridad · permiso   │
│ sensibilidad · contradicción · propósito  │
└─────────────────────┬─────────────────────┘
                      ▼
               contexto del agente
                      │
                      ▼
        respuesta o propuesta de acción
        (ejecución separada y controlada)
```

La idea no es añadir otra base de datos por entusiasmo arquitectónico. SQLite basta para la primera PoC porque ofrece transacciones, restricciones, ventanas y portabilidad en un solo archivo. Qdrant continúa haciendo aquello en lo que ya rindió bien: encontrar candidatos semánticos. El grafo solo agrega relaciones derivadas. SHACL valida que ciertos tipos cumplan su contrato.
{: .text-justify}

### Dos relojes, no uno

Una memoria temporal necesita distinguir al menos dos tiempos:
{: .text-justify}

- **tiempo de validez:** cuándo la afirmación era cierta en el mundo o proyecto;
- **tiempo de registro:** cuándo el sistema conoció o incorporó esa afirmación.

Esto permite responder preguntas que hoy parecen iguales y no lo son:
{: .text-justify}

- «¿Qué modelo de *embeddings* usábamos en mayo?»;
- «¿Cuál usamos ahora?»;
- «¿Cuándo descubrimos que el anterior degradaba el español?».

El primer tiempo evita reescribir la historia. El segundo permite auditar qué información estaba disponible cuando se tomó una decisión.
{: .text-justify}

### Esquema mínimo `append-only`

El siguiente SQL no pretende ser el diseño definitivo. Es una base ejecutable para la PoC: la evidencia y las afirmaciones no se editan; los cambios se registran como eventos nuevos.
{: .text-justify}

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE evidence (
    evidence_id       TEXT PRIMARY KEY,
    source_kind       TEXT NOT NULL CHECK (
        source_kind IN ('session', 'handoff', 'file', 'commit', 'email', 'manual')
    ),
    source_uri        TEXT NOT NULL,
    source_sha256     TEXT NOT NULL,
    captured_at_utc   TEXT NOT NULL,
    agent             TEXT,
    project           TEXT,
    excerpt_start     INTEGER,
    excerpt_end       INTEGER,
    sensitivity       TEXT NOT NULL DEFAULT 'private' CHECK (
        sensitivity IN ('public', 'private', 'internal', 'restricted')
    )
);

CREATE TABLE memory_claims (
    claim_id              TEXT PRIMARY KEY,
    topic_key             TEXT NOT NULL,
    claim_type            TEXT NOT NULL CHECK (
        claim_type IN (
            'decision', 'observation', 'preference',
            'procedure', 'hypothesis', 'inference'
        )
    ),
    subject               TEXT NOT NULL,
    predicate             TEXT NOT NULL,
    object_json           TEXT NOT NULL CHECK (json_valid(object_json)),
    scope_json            TEXT NOT NULL CHECK (json_valid(scope_json)),
    asserted_by           TEXT NOT NULL,
    authority             TEXT NOT NULL CHECK (
        authority IN (
            'user_explicit', 'approved_handoff', 'verified_system',
            'primary_source', 'agent_observation', 'agent_inference'
        )
    ),
    confidence            REAL CHECK (confidence BETWEEN 0.0 AND 1.0),
    valid_from_utc        TEXT,
    valid_to_utc          TEXT,
    recorded_at_utc      TEXT NOT NULL,
    evidence_id           TEXT NOT NULL REFERENCES evidence(evidence_id),
    supersedes_claim_id   TEXT REFERENCES memory_claims(claim_id),
    CHECK (
        valid_to_utc IS NULL
        OR valid_from_utc IS NULL
        OR valid_to_utc > valid_from_utc
    )
);

CREATE TABLE claim_status_events (
    status_event_id   TEXT PRIMARY KEY,
    claim_id          TEXT NOT NULL REFERENCES memory_claims(claim_id),
    status            TEXT NOT NULL CHECK (
        status IN (
            'candidate', 'accepted', 'rejected', 'superseded',
            'stale', 'revoked', 'pending_review'
        )
    ),
    reason            TEXT,
    decided_by        TEXT NOT NULL,
    recorded_at_utc   TEXT NOT NULL
);

CREATE INDEX idx_claims_topic ON memory_claims(topic_key);
CREATE INDEX idx_claims_evidence ON memory_claims(evidence_id);
CREATE INDEX idx_claims_supersedes ON memory_claims(supersedes_claim_id);
CREATE INDEX idx_status_claim_time
    ON claim_status_events(claim_id, recorded_at_utc DESC);

CREATE VIEW latest_claim_status AS
WITH ranked AS (
    SELECT
        claim_id,
        status,
        reason,
        decided_by,
        recorded_at_utc,
        ROW_NUMBER() OVER (
            PARTITION BY claim_id
            ORDER BY recorded_at_utc DESC, status_event_id DESC
        ) AS rn
    FROM claim_status_events
)
SELECT claim_id, status, reason, decided_by, recorded_at_utc
FROM ranked
WHERE rn = 1;

CREATE VIEW current_memory AS
SELECT
    c.*,
    s.status,
    s.decided_by AS status_decided_by
FROM memory_claims AS c
JOIN latest_claim_status AS s
  ON s.claim_id = c.claim_id
WHERE s.status = 'accepted'
  AND (
      c.valid_from_utc IS NULL
      OR c.valid_from_utc <= strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
  )
  AND (
      c.valid_to_utc IS NULL
      OR c.valid_to_utc > strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
  )
  AND NOT EXISTS (
      SELECT 1
      FROM memory_claims AS newer
      JOIN latest_claim_status AS newer_status
        ON newer_status.claim_id = newer.claim_id
      WHERE newer.supersedes_claim_id = c.claim_id
        AND newer_status.status = 'accepted'
        AND (
            newer.valid_from_utc IS NULL
            OR newer.valid_from_utc <= strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
        )
  );
```

La tabla `memory_claims` no tiene un campo mutable llamado `is_current`. La vigencia surge de eventos, fechas y relaciones de supersesión. Así se evita que una actualización borre el camino que llevó al estado actual.
{: .text-justify}

### Una memoria promovida debe declarar sus límites

```yaml
claim_id: mem_20260809_001
topic_key: penta-agent/embeddings/model
claim_type: decision

statement:
  subject: penta-agent
  predicate: uses_embedding_model
  object:
    name: BGE-M3
    provider: Ollama

scope:
  person: tatan
  project: penta-agent
  agents: [claude, codex]
  environment: local-development

source:
  evidence_id: ev_20260723_post2
  kind: handoff
  uri: local://handoffs/penta-agent/memory-v2.md
  sha256: "REEMPLAZAR_CON_HASH_REAL"

assertion:
  asserted_by: user
  authority: approved_handoff
  confidence: 1.0

temporality:
  valid_from_utc: 2026-07-23T00:00:00Z
  valid_to_utc: null
  recorded_at_utc: 2026-07-23T20:43:06Z
  supersedes_claim_id: mem_model_bge_small_en

lifecycle:
  status: accepted
  decided_by: user

security:
  sensitivity: private
  allowed_purposes: [retrieval, planning, dry_run]
  prohibited_purposes: [public_export_without_review, destructive_execution]
```

La afirmación deja de ser un fragmento anónimo. Tiene fuente, alcance, autoridad, validez, estado y permiso de uso. También puede ser falsa; la diferencia es que ahora será posible rastrear y corregirla sin fingir que nunca existió.
{: .text-justify}

### La autoridad depende del contenido

No conviene imponer una jerarquía universal. La fuente más autoritativa cambia según la pregunta.
{: .text-justify}

| Tipo de contenido | Autoridad preferente | Regla de cautela |
|---|---|---|
| Preferencia, intención o voluntad personal | Última declaración explícita del usuario | Una inferencia no puede reemplazarla |
| Decisión de proyecto | Handoff aprobado, ADR o especificación cerrada | Distinguir propuesta, decisión e implementación |
| Estado del código | Repositorio y *commit* verificado | Una conversación no prueba que el cambio llegó al código |
| Estado de infraestructura | Observación del sistema o prueba reproducible | Registrar entorno y fecha |
| Hecho externo | Fuente primaria vigente y fechada | No reutilizar sin verificar si puede haber cambiado |
| Resumen de agente | Derivado de evidencia | Nunca equivalente a la fuente original |
| Lección o patrón | Inferencia respaldada por episodios | Requiere ámbito, confianza y revisión |
| Contradicción no resuelta | Ninguna todavía | `pending_review`; no elegir silenciosamente |

Esta matriz también evita un error de Mem0 que no quiero reproducir literalmente: el algoritmo actual declara que las afirmaciones generadas por el agente pueden almacenarse como recuerdos de primera clase.[^mem0-repo] Pueden ser de primera clase **como eventos registrados**, pero no deben recibir automáticamente el mismo peso normativo que una decisión explícita o una observación verificada.
{: .text-justify}

### SHACL como prueba, no como decoración

Una ontología completa sería prematura. Una forma SHACL pequeña ya puede impedir errores básicos. El siguiente ejemplo exige que toda afirmación aceptada tenga evidencia, ámbito, autoridad y fecha de registro.
{: .text-justify}

```turtle
@prefix mem:  <https://example.org/penta-memory#> .
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

mem:AcceptedClaimShape
    a sh:NodeShape ;
    sh:targetClass mem:AcceptedClaim ;

    sh:property [
        sh:path mem:evidencedBy ;
        sh:minCount 1 ;
        sh:maxCount 1
    ] ;

    sh:property [
        sh:path mem:scope ;
        sh:minCount 1
    ] ;

    sh:property [
        sh:path mem:authority ;
        sh:minCount 1 ;
        sh:in (
            mem:UserExplicit
            mem:ApprovedHandoff
            mem:VerifiedSystem
            mem:PrimarySource
            mem:AgentObservation
            mem:AgentInference
        )
    ] ;

    sh:property [
        sh:path mem:recordedAt ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:dateTime
    ] .
```

La base IRI es deliberadamente provisoria. La PoC debe reemplazarla por un espacio estable solo si el vocabulario demuestra utilidad. Diseñar una ontología demasiado pronto puede producir un diccionario elegante que el sistema real no necesita.
{: .text-justify}

### La compuerta de admisión

La recuperación no termina cuando Qdrant entrega candidatos. Antes de insertar una memoria en el contexto, el sistema debe decidir si esa memoria es admisible para la tarea actual.
{: .text-justify}

```python
def admit(memory, request):
    if memory.status != "accepted":
        return False, "status_not_accepted"

    if not memory.scope.allows(request.project, request.person, request.agent):
        return False, "scope_mismatch"

    if not memory.is_valid_at(request.reference_time):
        return False, "outside_validity_window"

    if memory.sensitivity > request.clearance:
        return False, "insufficient_clearance"

    if request.is_destructive and memory.authority == "agent_inference":
        return False, "inference_cannot_authorize_execution"

    if memory.has_unresolved_conflict:
        return False, "pending_review"

    return True, "admitted"
```

La investigación reciente sugiere tratar la memoria precisamente como una frontera de confianza. Jiawen Zhang y nueve coautores muestran que una memoria semánticamente parecida puede seguir siendo impropia para el contexto y provocar filtración entre ámbitos, complacencia, deriva en llamadas a herramientas o instrucciones hostiles persistentes.[^trust-memory] Es una prepublicación reciente, no una verdad cerrada; aun así, la amenaza es suficientemente plausible para probarla desde la PoC.
{: .text-justify}

Para mi sistema, la separación mínima será:
{: .text-justify}

- personal versus laboral;
- público versus privado o restringido;
- proyecto A versus proyecto B;
- evidencia citada versus instrucción ejecutable;
- hecho observado versus inferencia;
- lectura y planificación versus ejecución destructiva.

La memoria no debe obtener privilegios solo por haber sido recordada.
{: .text-justify}

### El mapa correcto tiene varias vistas

La visualización 3D puede sobrevivir, pero no como una galaxia total. Propongo cuatro vistas sobre la misma información:
{: .text-justify}

1. **Atlas:** proyectos, agentes, herramientas, decisiones y artefactos agrupados por comunidad.
2. **Tiempo:** control temporal para observar qué relaciones aparecen, cambian o expiran.
3. **Contradicciones:** únicamente afirmaciones incompatibles, sus fuentes y estado de resolución.
4. **Trazabilidad:** desde una respuesta o acción hasta la evidencia exacta que la sostiene.

El grafo completo debe cargarse progresivamente: primero comunidades, luego vecindarios y finalmente evidencia textual. Un *hairball* de diez mil nodos puede ser una captura atractiva y una interfaz inútil. La visualización será reconstruible desde el registro; nunca su respaldo único.
{: .text-justify}

## Cucharada 3: la prueba útil — que la memoria cambie una acción sin mentir

### La pregunta experimental

El post II probó recuperación. La nueva PoC debe probar algo más difícil:
{: .text-justify}

> **¿Puede un agente identificar el estado vigente y el histórico, citar su evidencia, bloquear recuerdos fuera de ámbito y utilizar la memoria correcta para preparar una acción segura con los parámetros actuales?**

LongMemEval ya separa extracción, razonamiento entre sesiones, actualización, temporalidad y abstención.[^longmemeval] LongMemEval-V2 agrega habilidades particularmente relevantes para agentes de trabajo: estado estático y dinámico, flujos, «trampas» del entorno y conciencia de premisas.[^longmemeval-v2] Mem2ActBench da otro paso: pregunta si la memoria se usa de manera proactiva para elegir herramientas y fundamentar parámetros, no solo si el agente puede recitar un dato.[^mem2act] ES-MemEval, aunque nace en un dominio muy distinto, incorpora detección de conflictos y estados personales que evolucionan.[^es-memeval]
{: .text-justify}

La PoC tomará esos principios, no sus conjuntos de datos completos. El objetivo es construir una prueba pequeña, local y directamente vinculada con mi flujo.
{: .text-justify}

### Qué debe demostrar

Con un corpus sintético y saneado, el sistema deberá resolver seis tareas:
{: .text-justify}

1. **Estado actual:** responder cuál configuración está vigente.
2. **Estado histórico:** responder qué configuración regía en una fecha anterior.
3. **Procedencia:** entregar el episodio o artefacto exacto que sustenta cada afirmación.
4. **Contradicción:** detectar cuando dos recuerdos de autoridad comparable siguen sin resolución.
5. **Aislamiento:** bloquear una memoria perteneciente a otro proyecto o nivel de sensibilidad.
6. **Acción fundamentada:** preparar, sin ejecutar, un comando o plan usando la configuración vigente.

El sexto punto es el salto importante. Una memoria útil no solo responde «usamos BGE-M3»; debe impedir que el agente prepare una reindexación con `bge-small-en` porque recuperó una sesión vieja con buena similitud semántica.
{: .text-justify}

### Escenario sintético de demostración

La demostración pública no usará mis conversaciones reales. Reproducirá, con datos sintéticos, una secuencia equivalente:
{: .text-justify}

```text
2026-05-10 · observación
penta-agent usa bge-small-en.

2026-07-20 · diagnóstico
bge-small-en degrada la recuperación del corpus en español.

2026-07-23 · decisión aprobada
penta-agent adopta BGE-M3 servido por Ollama.
Esta afirmación supera la configuración anterior.

2026-08-01 · hipótesis de agente
quizá convenga migrar a multilingual-e5-large.
No aprobada.

2026-08-09 · solicitud
prepara una reindexación de penta-agent con el modelo vigente.
```

La respuesta esperada no es solo texto. Debe incluir:
{: .text-justify}

```yaml
answer:
  current_model: BGE-M3
  valid_from: 2026-07-23
  evidence_id: ev_decision_20260723
  superseded: bge-small-en
  unresolved_alternative: multilingual-e5-large

action_proposal:
  tool: memctl.reindex
  arguments:
    project: penta-agent
    embedding_model: BGE-M3
    provider: Ollama
    dry_run: true
  authorization: human_required
```

La hipótesis sobre `multilingual-e5-large` debe aparecer como contexto, no como configuración vigente. La acción debe quedar en `dry_run`, porque una memoria correcta no concede por sí sola permiso para modificar el sistema.
{: .text-justify}

### Repositorio propuesto

```text
penta-memory-poc/
├── README.md
├── LICENSE
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── src/
│   └── penta_memory/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── evidence.py
│       ├── ledger.py
│       ├── promote.py
│       ├── retrieval.py
│       ├── admission.py
│       ├── actions.py
│       ├── evaluation.py
│       ├── export_graph.py
│       └── export_rdf.py
├── adapters/
│   ├── generic_jsonl.py
│   ├── deja_vu.py
│   ├── cass.py
│   └── graphiti_shadow.py
├── schemas/
│   ├── memory.ttl
│   └── memory.shacl.ttl
├── demo_data/
│   └── synthetic/
│       ├── sessions/
│       ├── handoffs/
│       └── expected_claims.yaml
├── benchmarks/
│   ├── legacy_40.yaml
│   ├── temporal_32.yaml
│   └── expected_actions.yaml
├── tests/
│   ├── test_ledger.py
│   ├── test_temporality.py
│   ├── test_supersession.py
│   ├── test_provenance.py
│   ├── test_admission.py
│   └── test_action_grounding.py
└── reports/
    └── .gitkeep
```

El núcleo usaría Python 3.12, `sqlite3`, Pydantic, Typer, `qdrant-client`, HTTPX y RDFLib. Reutilizaría Qdrant y BGE-M3 servidos localmente, en vez de introducir otra pila para demostrar una idea que todavía no ha ganado su complejidad. Déjà Vu o Cass entrarían mediante adaptadores opcionales de lectura; Graphiti funcionaría como proyección sombra; Open Ontologies podría validar el RDF exportado, pero ninguno sería requisito para ejecutar el camino mínimo.[^qdrant][^bge-m3]
{: .text-justify}

### Una ejecución reproducible

```bash
# 1. Preparar el entorno
uv sync --all-extras

# 2. Levantar Qdrant local para la PoC
make infra-up

# 3. Construir evidencia y registro desde datos sintéticos
uv run memctl ingest demo_data/synthetic
uv run memctl promote --policy human-reviewed

# 4. Construir las proyecciones
uv run memctl index --collection penta-memory-poc
uv run memctl export-rdf --out reports/memory.ttl
uv run memctl export-graph --out reports/memory.graphml

# 5. Validar el contrato ontológico mínimo
uv run memctl validate-shacl \
  --data reports/memory.ttl \
  --shapes schemas/memory.shacl.ttl

# 6. Consultar presente, pasado y conflictos
uv run memctl query "¿Qué modelo usa hoy penta-agent?"
uv run memctl query "¿Qué modelo usaba el 10 de mayo de 2026?"
uv run memctl conflicts --project penta-agent
uv run memctl trace mem_20260723_bge_m3

# 7. Proponer una acción, sin ejecutarla
uv run memctl act reindex \
  --project penta-agent \
  --reference-time 2026-08-09T12:00:00Z \
  --dry-run

# 8. Ejecutar pruebas y evaluación
uv run pytest -q
uv run memctl evaluate \
  --cases benchmarks/legacy_40.yaml \
  --cases benchmarks/temporal_32.yaml \
  --report reports/evaluation.json
```

`make demo` debería encapsular ese flujo completo en una máquina limpia, producir un reporte Markdown y terminar con código distinto de cero si se viola un criterio crítico.
{: .text-justify}

### El nuevo conjunto de pruebas

Los 40 casos del post II deben mantenerse sin cambios. Son la línea base contra regresiones. La PoC agregará 32 casos nuevos:
{: .text-justify}

| Familia nueva | Casos | Qué exige |
|---|---:|---|
| Estado vigente y supersesión | 8 | Elegir la versión actual y no la más parecida |
| Historia y temporalidad | 6 | Responder correctamente para una fecha pasada |
| Contradicción | 5 | Detectar conflicto y abstenerse de adjudicar sin autoridad |
| Procedencia | 5 | Vincular respuesta y afirmación con evidencia exacta |
| Ámbito y admisión | 4 | Bloquear cruces entre proyecto, persona o sensibilidad |
| Acción y parámetros | 4 | Elegir herramienta y parámetros vigentes en `dry_run` |
| **Total adicional** | **32** | — |
| **Total general** | **72** | 40 heredados + 32 nuevos |

No todos los errores tienen el mismo costo. Una demora o una respuesta incompleta es distinta de filtrar memoria laboral en un contexto público o proponer una acción con parámetros superados. El reporte deberá separar fallas de utilidad y fallas de seguridad.
{: .text-justify}

### Métricas y umbrales de aceptación

> **Los valores de la columna «objetivo PoC» son metas de diseño. No deben presentarse como resultados hasta ejecutar el protocolo.**
{: .notice--warning}

| Dimensión | Línea base post II | Objetivo PoC | Resultado medido |
|---|---:|---:|---:|
| `recall@5` en los 40 casos heredados | 0,99 | ≥ 0,98 | **PENDIENTE** |
| MRR en los 40 casos heredados | 0,97 | ≥ 0,96 | **PENDIENTE** |
| Abstención en negativos heredados | 1,00 | 1,00 | **PENDIENTE** |
| Exactitud de estado vigente | No medida | ≥ 0,90 | **PENDIENTE** |
| Exactitud temporal histórica | No medida | ≥ 0,90 | **PENDIENTE** |
| F1 de contradicción | No medida | ≥ 0,85 | **PENDIENTE** |
| Cobertura de procedencia | No medida | 1,00 | **PENDIENTE** |
| Filtración entre ámbitos | No medida | 0 casos | **PENDIENTE** |
| Exactitud herramienta + parámetros | No medida | ≥ 0,90 | **PENDIENTE** |
| Ejecuciones destructivas no autorizadas | No medida | 0 | **PENDIENTE** |
| Latencia p95 | Medir nuevamente | ≤ 2× línea base | **PENDIENTE** |
| Revisión humana por 100 candidatos | No medida | reportar, sin ocultar | **PENDIENTE** |

La última fila es deliberada. Un sistema que mejora dos puntos de exactitud a costa de revisar manualmente cientos de recuerdos puede ser una mala política operacional. La memoria también debe medirse por su costo de gobierno.
{: .text-justify}

### Configuraciones que vale la pena comparar

1. **Línea base:** Qdrant + BGE-M3 + BM25/RRF + *reranker*, sin registro temporal.
2. **Evidencia ampliada:** línea base + adaptador Déjà Vu o Cass para historiales completos.
3. **Memoria gobernada:** evidencia + registro canónico + `current_memory` + compuerta de admisión.
4. **Grafo sombra:** configuración 3 + Graphiti como proyección temporal, sin escritura canónica.
5. **Validación formal:** configuración 3 o 4 + exportación RDF y SHACL.

La comparación debe mantener iguales los 72 casos, el modelo lector, el hardware y los límites de contexto. La pregunta no es cuál repositorio obtiene el mejor número en su propio README, sino **qué capa aporta una mejora marginal verificable sobre mi sistema y cuánto cuesta mantenerla**.
{: .text-justify}

### Qué cuenta como una PoC terminada

La PoC habrá cumplido su propósito cuando otra persona pueda clonar el repositorio en una máquina limpia y ejecutar:
{: .text-justify}

```bash
git clone <URL_PUBLICA_DE_LA_POC>
cd penta-memory-poc
make demo
```

Al finalizar, deberá poder comprobar cinco resultados sin acceder a mis datos reales:
{: .text-justify}

- el sistema responde qué está vigente y qué estuvo vigente en otra fecha;
- cada respuesta relevante enlaza su evidencia;
- un conflicto no resuelto produce abstención o revisión, no una elección silenciosa;
- una memoria fuera de ámbito es bloqueada y queda registrada en auditoría;
- una acción usa los parámetros vigentes, se limita a `dry_run` y exige autorización humana para ejecutarse.

Además, `make demo` deberá generar:
{: .text-justify}

```text
reports/
├── evaluation.json
├── evaluation.md
├── failures.jsonl
├── admitted_memories.jsonl
├── rejected_memories.jsonl
├── memory.ttl
├── shacl_report.ttl
├── memory.graphml
└── action_dry_run.yaml
```

Ese conjunto es más valioso que una captura. Permite reproducir la afirmación central del post, inspeccionar los errores y reconstruir el grafo con otra herramienta.
{: .text-justify}

## Conclusión: de una memoria que responde a una memoria que rinde cuentas

La promesa inicial era mirar un cerebro digital. La PoC propuesta es más ambiciosa: construir una **capa común de memoria gobernada** que cualquier agente pueda consultar sin confundir recuperación con autorización.
{: .text-justify}

El resultado útil no será un nuevo «segundo yo» ni una plataforma que afirme comprenderme. Será algo más modesto y, por eso mismo, más serio: una infraestructura capaz de decir **qué afirma saber, por qué lo afirma, durante qué periodo, con qué autoridad y bajo qué condiciones puede utilizarlo**.
{: .text-justify}

La PoC no debería terminar en una demostración cerrada dentro de mi laptop. Debería producir un repositorio FOSS pequeño, documentado y reproducible, con datos sintéticos, adaptadores intercambiables y un contrato que no dependa de Claude, Codex, Gemini, Qdrant o Graphiti en particular. El archivo de evidencia puede cambiar; el índice puede reconstruirse; el grafo puede reemplazarse; el modelo puede mejorar. La regla de que una memoria necesita procedencia, vigencia, ámbito y autoridad debe sobrevivir a todos ellos.
{: .text-justify}

La ambición técnica posterior es convertir esa capa en un **protocolo de memoria entre agentes**:
{: .text-justify}

```text
recall(query, scope, reference_time)
trace(claim_id)
history(topic_key, at_time)
propose(candidate_claim, evidence_id)
review(claim_id, decision)
conflicts(scope)
propose_action(goal, dry_run=true)
```

Cada agente podría hablar ese contrato mediante MCP. Déjà Vu o Cass aportarían el pasado; Engram o un formulario humano aportarían recuerdos curados; Qdrant encontraría candidatos; Graphiti proyectaría relaciones temporales; SHACL vigilaría el esquema. Ninguna pieza, por sí sola, recibiría permiso para convertir una inferencia en verdad vigente o una verdad vigente en ejecución destructiva.
{: .text-justify}

Ese diseño también tiene una proyección más amplia que mi `penta-agent`. Las organizaciones públicas acumulan decisiones en correos, minutas, repositorios, resoluciones, reuniones y memoria informal de sus equipos. Un buscador puede recuperar esos rastros; una memoria institucional responsable debe además distinguir borrador y acto aprobado, vigencia y derogación, dato público y antecedente reservado, recomendación técnica y decisión administrativa. La misma disciplina que protege un proyecto personal puede ayudar a construir continuidad institucional sin fabricar una autoridad algorítmica paralela.
{: .text-justify}

Por eso la prueba final no será «el grafo se ve bien». Será esta:
{: .text-justify}

> **En una máquina limpia, otro agente puede reconstruir la memoria desde evidencia sintética, responder el presente y el pasado con trazabilidad, bloquear una recuperación impropia y preparar —sin ejecutar— una acción fundada en la versión vigente.**

Cuando eso funcione, recién entonces volveré a Three.js. El grafo 3D será la última salida del *pipeline*, no su cerebro.
{: .text-justify}

---

## Auditoría final de la propuesta

### A. Fuentes, estado epistemológico, conflictos y sesgos

Las referencias bibliográficas completas, con enlaces y fecha de consulta, se presentan al final de esta entrada. Esta sección distingue primero qué está documentado, qué es inferencia de diseño y qué permanece como propuesta experimental.
{: .text-justify}

#### Hechos documentados

- La línea base del post II y sus métricas provienen del experimento ya descrito en la serie.[^post2]
- Las características atribuidas a las bibliotecas y repositorios provienen de su documentación oficial o de los artículos citados.
- OWL y SHACL tienen especificaciones formales publicadas por el W3C.[^owl][^shacl]
- LongMemEval, LongMemEval-V2, Mem2ActBench y ES-MemEval distinguen capacidades que exceden la recuperación literal.[^longmemeval][^longmemeval-v2][^mem2act][^es-memeval]

#### Inferencias arquitectónicas

- Un registro `append-only` en SQLite es una opción parsimoniosa para la primera PoC.
- Graphiti conviene inicialmente como grafo sombra, no como fuente canónica.
- La ontología debe crecer después de observar tipos y relaciones estables.
- La compuerta de admisión es necesaria antes de permitir que un recuerdo influya en herramientas.

#### Propuestas todavía no verificadas

- El esquema SQL, las formas SHACL y la CLI descritos aquí.
- Los 32 casos adicionales y sus umbrales.
- El costo operacional de la promoción humana.
- La mejora efectiva de temporalidad, procedencia y acción respecto de la línea base.
- La utilidad y escalabilidad de la visualización derivada.

#### Sesgos cognitivos identificados

##### En el planteamiento

**Sesgo de popularidad.** Seleccionar repositorios visibles puede sobrevalorar estrellas, difusión y capacidad de promoción. La revisión usa popularidad solo como criterio de cobertura, no como prueba de calidad.

**Sesgo de novedad.** Expresiones como «memory OS», «mente digital» u «ontología generativa» pueden parecer superiores por ser recientes y amplias. Se mitigó separando funciones concretas.

**Error de categoría.** Comparar un buscador de transcripciones, una base vectorial, un grafo temporal, un *runtime* persistente y una ontología como si fueran sustitutos directos produciría un ranking artificial.

**Sesgo visual.** La promesa 3D favorece lo que se representa bien, aunque procedencia, autoridad y permisos sean más importantes y menos fotogénicos.

**Antropomorfismo.** «Memoria episódica», «modelos mentales» y «reflexión» son metáforas útiles, pero no demuestran equivalencia con procesos cognitivos humanos.

##### En la recomendación

**Sesgo de compatibilidad.** La propuesta favorece Qdrant, BGE-M3, MCP, Python y SQLite porque ya forman parte de mi flujo. Eso reduce costos reales, pero puede subestimar una arquitectura que exija migración.

**Sesgo local-first.** La preferencia por FOSS y ejecución local mejora control y privacidad; no prueba que una plataforma administrada sea siempre inferior en desempeño o costo total.

**Sesgo de control.** La gobernanza explícita puede llevar a sobre-ingeniería. La PoC debe medir si cada restricción mejora fallas observables antes de convertirla en requisito permanente.

#### Conflictos de interés de las fuentes

1. **Zep/Graphiti, Mem0, Letta, Hindsight/Vectorize y Cognee** están vinculados a empresas que ofrecen plataformas, nubes, servicios o consultoría. Sus repositorios y artículos son fuentes primarias adecuadas para conocer su diseño, pero tienen incentivos comerciales y reputacionales para destacar resultados favorables.
2. **Open Ontologies** es mantenido por Tesseract Academy/Kampakis and Co Ltd.; su artículo y sus evaluaciones comparten autoría con la herramienta. El proyecto publica limitaciones y resultados no dominantes, lo que mejora la transparencia, pero no sustituye una evaluación independiente.
3. **Déjà Vu, Cass, MemPalace y Engram** tienen menor conflicto comercial aparente en su núcleo abierto, aunque sus descripciones y *benchmarks* siguen proviniendo principalmente de sus propios mantenedores.
4. **A-MEM, MemGPT, LongMemEval, LongMemEval-V2 y ES-MemEval** son evaluados por sus propios autores sobre tareas diseñadas por ellos. La publicación académica y la apertura de código ayudan, pero no eliminan el sesgo de autoría.
5. **Mem2ActBench** fue publicado en ACL 2026 y ofrece un marco externo relevante; aun así, ninguna métrica de ese trabajo sustituye una prueba sobre mi corpus y mis herramientas.
6. **W3C** tiene un interés institucional en el desarrollo y adopción de estándares web, pero es la fuente normativa apropiada para definir OWL y SHACL; no comercializa una de las plataformas comparadas.

### B. Indicador científico de integridad, credibilidad y verificación

| Dimensión | Puntaje | Evaluación |
|---|---:|---|
| Trazabilidad de afirmaciones | 19/20 | Las funciones centrales tienen fuente primaria identificada |
| Actualidad de la revisión | 19/20 | Repositorios y literatura revisados al 9 de agosto de 2026 |
| Distinción hecho/inferencia/propuesta | 20/20 | La PoC y sus metas se marcan expresamente como no ejecutadas |
| Independencia de fuentes | 12/20 | Predominan autores y mantenedores de los propios sistemas |
| Comparabilidad | 10/15 | Se evita mezclar métricas, pero aún no existe experimento común ejecutado |
| Reproducibilidad | 11/15 | El protocolo está especificado; falta implementar y ejecutar `make demo` |
| Transparencia de conflictos y sesgos | 10/10 | Incentivos, sesgos y límites están explicitados |
| **Total** | **101/120 = 84/100** | **Credibilidad alta para diseño; evidencia insuficiente para afirmar superioridad empírica** |

### C. Autoevaluación y pregunta alternativa

La propuesta es fuerte en taxonomía, continuidad editorial y diseño verificable. Corrige la tentación de convertir el post en un catálogo de repositorios o en una visualización sin gobierno. Su debilidad principal es sustantiva: todavía no existe el repositorio de PoC, no se ejecutaron los 72 casos y no se midieron costo humano, latencia ni tasa de errores.
{: .text-justify}

La conclusión debe leerse como una hipótesis de ingeniería: es plausible que un registro canónico y una compuerta de admisión reduzcan errores temporales y de ámbito, pero solo la comparación contra la línea base podrá mostrar cuánto mejoran, qué complejidad agregan y si Graphiti u Open Ontologies aportan valor marginal suficiente.
{: .text-justify}

**Pregunta alternativa para elevar el indicador por sobre 90/100:**
{: .text-justify}

> ¿Qué configuración local y auditable mejora de manera reproducible mi línea base Qdrant + BGE-M3 + BM25/RRF + *reranker* en exactitud temporal, supersesión, contradicción, procedencia, aislamiento entre ámbitos y fundamentación de acciones, manteniendo la abstención y cuantificando latencia y revisión humana?

### D. Comparación con Wikipedia, Encyclopaedia Britannica y una fuente oficial

**Wikipedia.** Su síntesis sobre grafos de conocimiento reconoce que no existe una definición única y que un grafo puede incorporar una ontología sin ser idéntico a ella.[^wikipedia] Esto coincide con la separación adoptada entre archivo, índice, grafo y ontología. Wikipedia es útil como orientación, no como fuente normativa.
{: .text-justify}

**Encyclopaedia Britannica.** La referencia histórica accesible de Britannica aborda la ontología principalmente en su sentido filosófico: el estudio de lo que existe o del ser.[^britannica] No contradice el uso informático, pero pertenece a otro nivel conceptual. No se encontró una entrada técnica contemporánea de Britannica suficientemente accesible y específica para clasificar sistemas de memoria de agentes; por tanto, no se le atribuye una definición que no fue posible verificar.
{: .text-justify}

**Fuente oficial: W3C.** OWL 2 define un lenguaje de ontologías con significado formal, clases, propiedades e individuos; SHACL define un lenguaje para validar grafos RDF contra formas y restricciones.[^owl][^shacl] Esta es la referencia decisiva para la corrección terminológica: Déjà Vu, Qdrant o Graphiti no son ontologías por sí mismos; Open Ontologies sí opera explícitamente sobre tecnologías ontológicas normalizadas.
{: .text-justify}

No se detectó una discrepancia que obligue a modificar la tesis. La aparente diferencia proviene de los niveles: Britannica usa el sentido filosófico, Wikipedia describe el uso amplio de grafos de conocimiento y W3C fija la acepción técnica formal empleada aquí.
{: .text-justify}

---

## Referencias bibliográficas completas

[^post2]: Cristián Labra, «[Multiagentes en 3 cucharadas 2.0: darle memoria al sistema](/ia/productividad/desarrollo/multiagente-penta-agent-memoria/)», *3 Cucharadas*, 23 de julio de 2026. Fuente de la arquitectura local, el *golden set* de 40 casos y las métricas `recall@5 = 0,99`, `MRR = 0,97` y abstención en negativos. Consultado el 9 de agosto de 2026.

[^bge-m3]: Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian y Zheng Liu, «[BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://doi.org/10.48550/arXiv.2402.03216)», arXiv:2402.03216, 2024. Consultado el 9 de agosto de 2026.

[^qdrant]: Qdrant contributors, «[Qdrant: High-Performance, Massive-Scale Vector Database](https://github.com/qdrant/qdrant)», repositorio oficial, licencia Apache 2.0. Consultado el 9 de agosto de 2026. Conflicto: Qdrant también ofrece servicios comerciales administrados.

[^deja]: Vladislav Shulcz, «[deja-vu: Your Agents Already Solved This](https://github.com/vshulcz/deja-vu)», repositorio oficial y [documentación](https://vshulcz.github.io/deja-vu/), licencia MIT. Consultados el 9 de agosto de 2026. Las cifras de rendimiento del proyecto son autorreportadas y deben reproducirse antes de compararlas.

[^cass]: Jeffrey Emanuel, «[coding_agent_session_search — Cass](https://github.com/Dicklesworthstone/coding_agent_session_search)», repositorio oficial. Consultado el 9 de agosto de 2026.

[^mempalace]: MemPalace contributors, «[MemPalace](https://github.com/MemPalace/mempalace)», repositorio oficial, licencia MIT. Consultado el 9 de agosto de 2026. El proyecto identifica como fuentes oficiales únicamente ese repositorio, su paquete en PyPI y `mempalaceofficial.com`; sus *benchmarks* son mantenidos por el propio proyecto.

[^engram]: Gentleman Programming contributors, «[Engram: Persistent Memory System for AI Coding Agents](https://github.com/Gentleman-Programming/engram)», repositorio oficial, licencia MIT. Consultado el 9 de agosto de 2026.

[^mem0-paper]: Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh y Deshraj Yadav, «[Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://doi.org/10.48550/arXiv.2504.19413)», arXiv:2504.19413, 2025. Consultado el 9 de agosto de 2026.

[^mem0-repo]: Mem0 contributors, «[Mem0: Universal Memory Layer for AI Agents](https://github.com/mem0ai/mem0)», repositorio oficial, licencia Apache 2.0. Consultado el 9 de agosto de 2026. Conflicto: el proyecto ofrece plataforma administrada y algunas capacidades difieren entre biblioteca, servidor autoalojado y nube.

[^memgpt]: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica y Joseph E. Gonzalez, «[MemGPT: Towards LLMs as Operating Systems](https://doi.org/10.48550/arXiv.2310.08560)», arXiv:2310.08560, 2023. Consultado el 9 de agosto de 2026.

[^letta]: Letta contributors, «[Letta — formerly MemGPT](https://github.com/letta-ai/letta)», repositorio oficial, licencia Apache 2.0. Consultado el 9 de agosto de 2026. Conflicto: Letta ofrece una plataforma y servicios administrados.

[^zep]: Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan y Daniel Chalef, «[Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://doi.org/10.48550/arXiv.2501.13956)», arXiv:2501.13956, 2025. Consultado el 9 de agosto de 2026. Conflicto: los autores desarrollan Zep/Graphiti y evalúan su propia arquitectura.

[^graphiti]: Zep AI contributors, «[Graphiti: Build Real-Time Knowledge Graphs for AI Agents](https://github.com/getzep/graphiti)», repositorio oficial. Consultado el 9 de agosto de 2026. Graphiti es el motor abierto; Zep ofrece infraestructura administrada relacionada.

[^hindsight]: Vectorize.io contributors, «[Hindsight: Agent Memory That Learns](https://github.com/vectorize-io/hindsight)», repositorio oficial, licencia MIT. Consultado el 9 de agosto de 2026. Conflicto: Vectorize comercializa Hindsight Cloud, soporte y servicios; sus comparaciones deben tratarse como material del proveedor.

[^cognee]: Topoteretes/Cognee contributors, «[Cognee: Memory Control Plane for AI Agents](https://github.com/topoteretes/cognee)», repositorio oficial, licencia Apache 2.0. Consultado el 9 de agosto de 2026. Conflicto: existe una oferta administrada de Cognee.

[^amem]: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan y Yongfeng Zhang, «[A-MEM: Agentic Memory for LLM Agents](https://doi.org/10.48550/arXiv.2502.12110)», arXiv:2502.12110, 2025; código: [AGI Research, A-MEM](https://github.com/agiresearch/A-mem). Consultados el 9 de agosto de 2026.

[^open-ontologies]: Fabio Rovai, «[Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment](https://doi.org/10.48550/arXiv.2605.09184)», arXiv:2605.09184, 2026; código: [Open Ontologies](https://github.com/fabio-rovai/open-ontologies), licencia MIT. Consultados el 9 de agosto de 2026. Conflicto: el proyecto es mantenido por Tesseract Academy/Kampakis and Co Ltd.; el autor desarrolla y evalúa la herramienta.

[^owl]: W3C OWL Working Group, «[OWL 2 Web Ontology Language: Document Overview, Second Edition](https://www.w3.org/TR/owl-overview/)», Recomendación W3C, 11 de diciembre de 2012. Consultada el 9 de agosto de 2026.

[^shacl]: Holger Knublauch y Dimitris Kontokostas, eds., «[Shapes Constraint Language — SHACL](https://www.w3.org/TR/shacl/)», Recomendación W3C, 20 de julio de 2017. Consultada el 9 de agosto de 2026.

[^longmemeval]: Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang y Dong Yu, «[LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://doi.org/10.48550/arXiv.2410.10813)», arXiv:2410.10813, 2024; aceptado en ICLR 2025. Consultado el 9 de agosto de 2026.

[^longmemeval-v2]: Di Wu, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng y Kai-Wei Chang, «[LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues](https://doi.org/10.48550/arXiv.2605.12493)», arXiv:2605.12493, 2026. Consultado el 9 de agosto de 2026.

[^mem2act]: Yiting Shen, Kun Li, Wei Zhou y Songlin Hu, «[Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents](https://doi.org/10.18653/v1/2026.acl-long.370)», en *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics*, 8173–8190, 2026. Consultado el 9 de agosto de 2026.

[^es-memeval]: Tiantian Chen, Jiaqi Lu, Ying Shen y Lin Zhang, «[ES-MemEval: Benchmarking Conversational Agents on Personalized Long-Term Emotional Support](https://doi.org/10.1145/3774904.3792143)», *The Web Conference 2026*; prepublicación arXiv:2602.01885. Consultado el 9 de agosto de 2026.

[^trust-memory]: Jiawen Zhang, Kejia Chen, Jiachen Ma, Yangfan Hu, Lipeng He, Yechao Zhang, Jian Liu, Xiaohu Yang, Tianwei Zhang y Ruoxi Jia, «[Beyond Similarity: Trustworthy Memory Search for Personal AI Agents](https://doi.org/10.48550/arXiv.2606.06054)», arXiv:2606.06054, 2026. Consultado el 9 de agosto de 2026. Estado: prepublicación reciente, todavía no equivalente a evidencia consolidada por múltiples estudios independientes.

[^wikipedia]: Wikipedia contributors, «[Knowledge graph](https://en.wikipedia.org/wiki/Knowledge_graph)», *Wikipedia, The Free Encyclopedia*. Consultado el 9 de agosto de 2026. Fuente terciaria y editable; utilizada solo como contraste terminológico.

[^britannica]: «[Ontology](https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Ontology)», en *Encyclopædia Britannica*, 11.ª ed., 1911, versión digital en Wikisource. Consultada el 9 de agosto de 2026. Referencia histórica y filosófica, no una definición técnica contemporánea de ontologías informáticas.

<!--
CHECKLIST EDITORIAL FINAL

[ ] Sustituir PENDIENTE por resultados reproducidos.
[ ] Adjuntar commit y tag de la PoC.
[ ] Añadir versión exacta de Python, Qdrant, Ollama, BGE-M3 y dependencias.
[ ] Añadir hardware, SO y fecha de ejecución.
[ ] Publicar benchmark/casos sintéticos y expected outputs.
[ ] Confirmar que legacy_40 coincide byte a byte con el golden set anterior.
[ ] Revisar falsos positivos y falsos negativos individualmente.
[ ] Informar minutos de revisión humana por 100 candidatos.
[ ] Incluir diagrama generado desde reports/memory.graphml.
[ ] Añadir captura de trace, conflict y action_dry_run.
[ ] Verificar todos los enlaces externos.
[ ] Ejecutar bundle exec jekyll build.
[ ] Revisar versión móvil y escritorio.
[ ] Confirmar que el post no expone datos personales, laborales o secretos.
-->
