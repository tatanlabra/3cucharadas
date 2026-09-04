---
layout: single
title: "Multiagentes en 3 cucharadas III: una memoria que deja huellas"
subtitle: "Del RAG auditable a una memoria gobernada: por qué todavía no es un clon digital"
date: 2026-09-03 00:00:00 -0400
last_modified_at: 2026-09-03 00:00:00 -0400
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, rag, memoria-agentes, procedencia, privacidad, gobernanza, knowledge-graph, evaluacion-rag, threejs]
description: "Tercera bitácora de penta-agent: procedencia, vigencia, evaluación y una proyección 3D saneada de su memoria de trabajo."
excerpt: "El sistema ya recupera y visualiza trazas. El problema ahora es gobernar qué persiste, qué caduca y qué nunca debe salir de su ámbito."
author: clabra
lang: es
ref: multiagente-penta-agent-memoria-gobernada-poc
permalink: /ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/
distribution:
  social: true
  republish: []
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, servicios locales (Qdrant y Sentence Transformers por loopback, timers systemd --user), Qdrant con vector nombrado `dense`"
en_abstract: >
  Third log of a local multi-agent setup. The previous entry made its shared
  memory measurable; this one asks a harder question: what should persist,
  what should expire, and what must never leave its scope. Four sources are
  kept apart by contract rather than merged — curated operational memory,
  a private and reversible personal-mail pilot, authorized process metadata
  from a thesis project, and the sanitized public projection built from them.
  A frozen 319-context staging collection, embedded with Qwen3-Embedding-0.6B
  on CPU, was used to test five retrieval changes against 40 queries with 8
  negatives; only one was promoted (dropping the BM25 boost from 0.10 to 0.00,
  38 complete / 2 partial / 0 failed, recall@5 0.9635, MRR 0.8396). A reranker
  scored better on MRR (0.9010) and was still rejected: median latency went
  from 2.37 s to 15.83 s, with a 91.10 s worst case. The 3D viewer is a static,
  regenerable export with a text fallback — a map of recorded strategies, not
  a mind. What this does not show is equally explicit: retrieval quality is not
  answer fidelity, two multi-source cases remain partial, and none of this
  amounts to a digital clone.
math: false
published: true
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria-gobernada.webp
  og_image: /assets/images/multiagente-penta-agent-memoria-gobernada/og-memoria-gobernada-1200x630.webp
  og_image_alt: "Cuatro fuentes gobernadas sobre plataformas separadas —memoria de trabajo, correo personal sellado bajo cristal, índice de tesis y proyección pública— con una membrana que solo deja pasar tres salidas permitidas."
---

> **Estado de la demostración.** El visor se regeneró el 29 de agosto de 2026 desde una proyección pública saneada. El artefacto no contiene cuerpos de correo, adjuntos, direcciones, rutas absolutas, tokens, credenciales ni microdatos. El índice canónico y las fuentes privadas permanecen fuera del sitio.
{: .notice--warning}

> **Convención de lectura.** **HECHO LOCAL** designa una medición fechada y reproducible en los artefactos del proyecto; **INFERENCIA DE DISEÑO**, una conclusión extraída de esas mediciones; y **NO VERIFICADO**, una capacidad que el sistema no se atribuye. Un conteo, una arista o una prueba de infraestructura no demuestran comprensión, identidad ni fidelidad general de respuesta.
{: .notice--info}

## Preámbulo: recordar no basta

En la [segunda parte](/ia/productividad/desarrollo/multiagente-penta-agent-memoria/) intenté resolver un problema acotado: que la memoria de `penta-agent` recuperara evidencia y reconociera cuándo no la encontraba. Esa pieza existe. La pregunta de esta tercera parte es más incómoda: **¿qué ocurre cuando esa memoria comienza a crecer?**

Un índice puede acumular fragmentos sin dificultad. Una memoria útil, en cambio, debe conservar procedencia, vigencia, permisos, contradicciones y criterios de eliminación. También debe distinguir entre encontrar una fuente y responder correctamente a partir de ella. La literatura reciente insiste en separar RAG, gestión de contexto y memoria de agentes, porque cumplen funciones diferentes y exigen evaluaciones distintas (Hu et al. 2025).

Este post corrige, además, dos atajos del borrador inicial. El primero reducía el sistema a unos pocos nodos decorativos: era seguro, pero no informativo. El segundo confundía fidelidad con saturación: un grafo puede derivarse de datos reales y seguir siendo un ovillo ilegible. La solución no es inventar una alegoría ni publicar todas las trazas, sino construir una proyección limitada, reproducible y reconociblemente vinculada a la evidencia.

La historia que sigue tiene tres movimientos: qué cambió desde la parte II; qué experimentos resistieron una evaluación que podía fallar; y cómo mostrar la memoria sin hacerla pasar por una mente.

---

## Primera cucharada: de recuperar fragmentos a gobernar evidencia

En esta arquitectura, RAG se ocupa de recuperar información; la capa de memoria añade reglas para conservarla, actualizarla, descartarla y volver a utilizarla. Ninguna de esas funciones equivale, por sí sola, a identidad. Cada fuente debe viajar con su origen, transformación, ámbito de acceso, vigencia y salida permitida. PROV-O aporta un vocabulario interoperable para la parte de procedencia —entidades, actividades y agentes—; los permisos y la vigencia exigen reglas adicionales (Lebo, Sahoo y McGuinness 2013).

### Lo que cambió desde la parte II

| Compromiso pendiente | Evidencia incorporada en esta versión | Límite que permanece abierto |
|---|---|---|
| Comparar recuperación densa, léxica y reordenamiento sin alterar producción. | Colección `penta_context_qwen3_staging`, corte congelado de 319 contextos y 40 consultas evaluadas con `k=5`. | El mejor pase sigue en 38 casos completos y 2 parciales; la compuerta estricta continúa cerrada. |
| Evaluar si una respuesta usa las fuentes recuperadas y sabe abstenerse. | Contrato `context-answer-v1`, con 12 casos positivos y 6 negativos saneados. | La prueba integral de un modelo local y la revisión humana de los casos reservados aún no se completan. |
| Incorporar vigencia sin borrar la historia. | Entorno de pruebas que admite `supersedes` solo desde una fecha posterior y rechaza sucesores competidores. | Todavía no existe un razonador temporal conectado a la memoria viva. |
| Hacer visible el crecimiento sin confundir topología con verdad. | Visor 3D estático, regenerable desde JSON saneado y con alternativa textual cuando no hay WebGL. | El visor no consulta Qdrant, no valida aristas y no representa una mente. |

### Qué memoria existe realmente

| Capa | Corte local al 29 de agosto de 2026 | Qué permite sostener | Qué no permite sostener |
|---|---|---|---|
| Experiencia de `penta-agent` | 16.955 puntos indexados, 1.432 estrategias, 3.949 relaciones, 12 comunidades y 8 tipos de tarea. | Existen trazas operativas, vecindades semánticas, correcciones y fallos explorables. | Cada arista no es una relación causal ni una afirmación verdadera. |
| Contexto curado | 319 contextos canónicos en `penta_context_v2`; la comprobación local respondió `green`. | Un *handoff* o una decisión curada puede recuperarse con procedencia. | El índice no sustituye al registro canónico ni cubre todo el historial. |
| Proceso de investigación | Instantánea pública con 796 artefactos derivados, 533 vínculos y 7 asuntos pendientes; búsqueda FTS5 y TF-IDF. | La cadena de trabajo de la tesis puede inspeccionarse sin publicar documentos ni microdatos. | No demuestra ejecución histórica, réplica ni resultados sustantivos. |
| Correo personal | Inventario privado de 12.072 mensajes únicos, 8.559 duplicados y cobertura 2011–2026. | La lectura de solo inventario funciona dentro de un ámbito autorizado. | El correo no es un corpus público ni un modelo de personalidad. |
| Memoria personal local | Prototipo separado con `mbox`, SQLite/FTS, ámbitos explícitos, purga y evaluación sintética. | Existe una ruta técnica reversible para recuperar material privado. | No está autorizado un flujo generativo sobre correo sensible. |

La procedencia también debe registrar las fallas de la propia tubería. El exportador histórico esperaba un vector simple, mientras el índice actual utiliza el vector nombrado `dense`. La primera regeneración produjo un grafo degradado, sin aristas semánticas. Una prueba contra el índice real descubrió la incompatibilidad; después de adaptar el exportador, reaparecieron 3.658 aristas semánticas. El episodio deja una regla práctica: **una visualización auditable debe mostrar cuándo su cadena de datos se degradó, por qué ocurrió y cómo se recompuso**.

### Del comando a la tarea

La unidad mínima del índice sigue siendo una estrategia observada. Muchas estrategias tienen forma de comando porque así quedaron registradas las acciones. Para hacerlas legibles sin inventar intenciones, añadí una clasificación determinista basada en estrategia, herramienta, transporte y proyecto.

| Tipo de trabajo derivado | Estrategias | Pregunta que ayuda a formular |
|---|---:|---|
| Coordinar agentes y decisiones | 399 | ¿Qué se aprendió al delegar una tarea o dejar un *handoff*? |
| Investigar y analizar datos | 396 | ¿Qué tácticas se repiten al examinar datos, tesis y fuentes? |
| Leer y rastrear evidencia | 385 | ¿Qué antecedentes se inspeccionaron antes de decidir? |
| Ejecutar y automatizar | 118 | ¿Qué pasos implementaron un cambio ya revisado? |
| Versionar y comparar cambios | 76 | ¿Qué controles se aplicaron antes de conservar una modificación? |
| Probar y verificar | 28 | ¿Qué se comprobó en vez de declararse terminado? |
| Operar herramientas y servicios | 18 | ¿Qué infraestructura permitió o bloqueó el flujo? |
| Editar y comunicar | 12 | ¿Qué convirtió evidencia técnica en documentación o publicación? |

Esta capa es una lente pedagógica, no una ontología del autor. Una estrategia puede pertenecer a más de una tarea, pero hoy queda asignada a la primera regla coincidente. Por eso sirve para orientarse, no para medir productividad ni atribuir capacidades humanas al sistema.

---

## Segunda cucharada: experimentar sin mezclar ni promover

La arquitectura tiene capas con funciones distintas: el *ledger* y los archivos fuente son canónicos; Qdrant es un índice regenerable; el visor es una proyección pública; y los adaptadores privados permanecen fuera de Git. Esta separación evita que una coincidencia vectorial se convierta, sin revisión, en un hecho durable.

### La prueba de concepto no es una licuadora de fuentes

Correo, tesis y memoria de trabajo no son nodos intercambiables. En esta etapa, solo el contexto curado alimenta la recuperación entre agentes y la proyección pública. El correo conserva una ruta privada, reversible y vetable; la tesis aporta metadatos de proceso autorizados. Las flechas del diagrama describen salidas permitidas, no transferencias automáticas ni inferencias sobre personas. La diferencia entre acceso técnico y flujo legítimo de información es precisamente el problema que la integridad contextual busca capturar (Nissenbaum 2004).

<figure class="align-center">
  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" alt="Tres fuentes gobernadas: la memoria de trabajo permite recuperación con procedencia; el correo personal permite solo revisión privada y reversible; tesis y documentos permiten citas y estados de verificación. Una frontera impide publicar cuerpos de correo, adjuntos, direcciones, rutas absolutas, microdatos e inferencias de identidad." loading="lazy" decoding="async">
  </a>
  <figcaption>Figura 1. La integración actual es una arquitectura de permisos: la fuente determina su salida permitida.</figcaption>
</figure>

La tesis entra de esta forma: como una [instantánea pública del índice de investigación]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}), no como corpus abierto. La tarjeta expone 796 artefactos textuales derivados —316 auditorías, 244 reportes, 133 contratos, 71 pseudocódigos y 32 piezas de inventario, replicación o documentación—, 533 vínculos y 7 asuntos pendientes. Excluye fuentes históricas, DTA, Parquet, PDF, imágenes, rutas, textos y microdatos. Su búsqueda es léxica; no pretende comprensión neuronal.

Conviene decir en qué estado está esa instantánea, porque es el caso de prueba del propio argumento. Sus cifras corresponden al índice construido el 29 de agosto y son fieles a ese corte: la huella del manifiesto coincide byte a byte con la publicada. Pero el corpus siguió creciendo —hoy tiene 817 documentos, veintiuno más, todos de fases posteriores—, y el índice no se regeneró. El resultado es que la compuerta de vigencia está en rojo: `check-research-index` sale 2, con `document_count` y `source_fingerprint` en `false`, y el contrato que la agrupa sale 2 también.

Eso no invalida la instantánea; la fecha. Y es exactamente lo que una memoria gobernada debe hacer: no impedir que el mundo cambie, sino negarse a afirmar que sigue igual. Una compuerta que se hubiera quedado verde mientras el corpus crecía un 2,6% habría sido peor que no tenerla, porque habría dado por vigente un artefacto que ya no lo era. El estado publicable de esta pieza no es «verificado», es «fechado y con su compuerta abierta».
{: .notice--warning}

### Qué conviene reutilizar —y bajo qué contrato

| Necesidad | Activo local | Proyecto que merece contraste | Regla de adopción |
|---|---|---|---|
| Recuperar decisiones entre sesiones de programación | *Handoffs*, eventos y contexto curado. | [`deja-vu`](https://github.com/vshulcz/deja-vu), que indexa sesiones locales de agentes y ofrece recuperación mediante CLI y MCP. | Debe mejorar búsquedas históricas reales sin sustituir notas curadas por transcripciones crudas. |
| Mantener estado explícito de un agente | RAG evaluado y contexto curado; no un entorno general de ejecución. | [Letta Code](https://github.com/letta-ai/letta-code), *harness* actual del proyecto surgido de MemGPT (Packer et al. 2023). | Comparar sus bloques de memoria y mecanismos de reescritura con los contratos existentes antes de añadir otro entorno. |
| Extraer recuerdos desde conversaciones | Ingesta y curación humana; correo privado con veto. | [Mem0](https://github.com/mem0ai/mem0) y [Hindsight](https://github.com/vectorize-io/hindsight). | Medir precisión, falsos positivos, revocación y purga sobre datos sintéticos antes de tocar correo real. |
| Representar vigencia y contradicción | Entorno de pruebas con `supersedes`. | [Graphiti](https://github.com/getzep/graphiti), núcleo abierto de la arquitectura temporal descrita por Rasmussen et al. (2025). | Llevar decisiones fechadas a un piloto sin perder fuente, vigencia ni revisión humana. |
| Conectar conceptos, documentos y citas | Índice de proceso FTS5/TF-IDF con lista blanca. | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) para un corpus científico acotado (Edge et al. 2024). | Comparar costo, trazabilidad y recuperación contra la línea base léxica; empezar pequeño, porque el proyecto está en mantenimiento y su documentación advierte sobre el costo de indexación. |
| Visualizar una proyección reproducible | Generador local y artefacto JSON saneado. | [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph), ya incorporado. | Conservar alternativa textual y no interpretar distancia visual como afinidad humana. |

La prioridad no es instalar todo. Es ensayar, bajo el mismo contrato, aquello que pueda reducir fricción sin degradar procedencia, privacidad ni reversibilidad. Las descripciones de producto sirven para saber qué promete cada proyecto; no bastan para establecer que sea superior en este corpus. Tampoco basta con que el núcleo sea abierto: deben documentarse los modelos, servicios externos y flujos de datos necesarios para operarlo.

### Un experimento de recuperación que podía fallar

El ensayo con `Qwen3-Embedding-0.6B` se ejecutó mediante Sentence Transformers en una colección aislada, con 319 contextos congelados, vectores de 1.024 dimensiones, CPU y persistencia 319/319. No modificó `penta_context_v2`. El conjunto de prueba mantuvo 40 consultas, 8 negativos y `k=5`; la notación **38/2/0** significa 38 pases completos, 2 parciales y ningún fallo total.

La tarjeta del modelo recomienda instrucciones adaptadas a la tarea, pero una recomendación del proveedor no reemplaza la evaluación local. El resultado fue el siguiente (Zhang et al. 2025):

| Hipótesis | Cambio aislado | Resultado local | Decisión |
|---|---|---|---|
| El componente léxico desplaza evidencia densa correcta. | Bonificación BM25 de `0,10` a `0,00`, solo en `staging`. | De 36/3/1 a **38/2/0**; 8/8 negativos conservaron la abstención; *recall*@5 de 0,9635 y MRR de 0,8396. | Se conserva como punto de partida experimental; no demuestra mejora frente a producción. |
| Una instrucción genérica mejora la citabilidad. | Instrucción explícita para privilegiar fuentes completas y citables. | **33/3/4**; abstenciones negativas 6/8. | Rechazada: empeoró cobertura y abstención. |
| Un reordenador recupera fuentes complementarias. | `Qwen3-Reranker-0.6B` sobre candidatos ya admitidos. | **38/2/0**; *recall*@5 de 0,9688 y MRR de 0,9010; mediana de 15,83 s y máximo de 91,10 s, frente a 2,37 s del orden base. | Solo análisis sin conexión; el costo no justifica su promoción. |
| El repositorio aproxima la familia documental. | Diversificación por `repo_scope` dentro de una ventana de 20. | **38/2/0**; *recall*@5 de 0,9740; un parcial se resolvió y otro apareció en una tarea distinta. | Rechazada: procedencia no equivale a intención documental. |
| El consenso de dos órdenes evita trasladar el error. | Fusión RRF del orden base y el reordenado (Cormack, Clarke y Büttcher 2009). | **38/2/0**; *recall*@5 de 0,9635; mediana de 20,06 s. | Rechazada: no cerró la compuerta ni compensó el costo. |

Los dos parciales son siempre casos de múltiples fuentes: la selección no logra cubrir familias documentales distintas dentro de cinco posiciones. Aquí debo declarar un límite en vez de una medición. El diagnóstico que habría localizado en qué rango quedaban los documentos faltantes nunca llegó a correr: exigía un fichero de taxonomía de evidencia que no existe en el repositorio, y el único intento quedó registrado como `failed`. Sé que los parciales existen y qué casos son, porque eso sí está en cada corrida; no sé a qué distancia quedaron, y no voy a escribir un número que no puedo reproducir. Aumentar `k` hasta obtener un pase habría cambiado la pregunta de evaluación, así que tampoco es la salida.

La siguiente hipótesis es más exigente y menos vistosa: metadatos humanos de linaje o intención documental, ligados a la huella del corte y de la consulta, sin acceso al conjunto dorado durante su creación. Mientras esas etiquetas no existan y la prueba estricta siga en rojo, la colección permanece en `staging`.

---

## Tercera cucharada: un mapa que no se hace pasar por una mente

La visualización se genera desde un corte saneado de la memoria de experiencia. No consulta Qdrant ni servicios externos al abrirse: recibe un artefacto estático, regenerable y auditable. La [exportación pública en JSON]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) permite inspeccionar esta corrida, y el HTML debe poder reproducirse desde ese archivo sin releer fuentes privadas.

> **Lectura guiada.** Primero abre **Tareas** y selecciona una familia, por ejemplo «Investigar y analizar datos». Luego usa **Proy** para distinguir dónde ocurrió el trabajo. Solo al final abre **Errores** o el modo diagnóstico para inspeccionar una fricción concreta. El visor debe comenzar por una pregunta, no por una nube de puntos.
{: .notice--primary}

<section class="rag-knowledge-graph" aria-labelledby="rag-knowledge-graph-title">
  <div class="rag-knowledge-graph__header">
    <div>
      <p class="rag-knowledge-graph__eyebrow">Proyección pública · 2026-08-29</p>
      <h3 id="rag-knowledge-graph-title">Mapa de estrategias registradas por penta-agent</h3>
      <p>Corte del 29 de agosto: 1.432 estrategias · 3.949 relaciones · 8 tipos de tarea · 16.955 puntos indexados</p>
    </div>
    <a class="rag-knowledge-graph__open" href="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" target="_blank" rel="noopener">Abrir visor completo<span class="screen-reader-text"> en una pestaña nueva</span></a>
  </div>
  <iframe class="rag-knowledge-graph__frame" title="Mapa 3D navegable de tipos de trabajo y estrategias de penta-agent" src="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" loading="lazy" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>
</section>

Los números pertenecen a ese corte, no a un contador vivo. Actualizar el visor exige regenerar la proyección, sanearla de nuevo y revisar las diferencias antes de reemplazar el artefacto público.
{: .notice--info}

| Componente visible | Derivación | Lectura correcta |
|---|---|---|
| Tipos de tarea | Reglas deterministas sobre estrategia, herramienta, transporte y proyecto. | Orientan la exploración; no clasifican la psicología del autor. |
| Nodos de estrategia | Lecciones de experiencia con evidencia observada. | Representan una estrategia registrada, no una creencia. |
| Aristas semánticas | Vecindad entre representaciones vectoriales del índice derivado. | Indican similitud operacional, no causalidad. |
| Aristas estructurales y de corrección | Herramientas, repositorios, transportes o secuencias compartidas. | Son pistas que requieren abrir su procedencia. |
| Comunidades y paneles | Agregaciones deterministas de la exportación. | Ayudan a decidir qué preguntar y dónde verificar. |
| Correo y tesis | No aparecen como nodos de contenido. | Solo se publican capacidades, ámbitos y metadatos autorizados. |

La composición no intenta mostrar las 3.949 relaciones con igual énfasis. Empieza por tipos de tarea, permite aislar proyectos y errores, y reserva el detalle para la interacción. Ese es el compromiso entre una base real —demasiado grande para una ilustración— y una lectura pública —demasiado importante para un ovillo opaco—.

### De una fuente recuperada a una respuesta atribuida

Encontrar el documento correcto no garantiza una respuesta correcta. Un modelo puede omitir la condición decisiva, citar otra fuente o contestar cuando debería abstenerse. LongMemEval separa extracción, razonamiento entre sesiones, temporalidad, actualización y abstención; LongMemEval-V2 —todavía presentado como trabajo en curso— desplaza el foco hacia trayectorias de agentes, conocimiento de flujos, cambios de estado, fallos recurrentes y premisas inválidas (Wu et al. 2024; Wu et al. 2026). Mi conjunto local es mucho más pequeño y no es comparable con esos resultados: su función es verificar el contrato del proyecto.

`context-answer-v1` contiene 18 casos saneados: 12 positivos, con afirmaciones y fuentes obligatorias, y 6 negativos. Una *fixture* determinista pasó 18/18. Eso demuestra que el evaluador distingue una salida válida de una inválida; no demuestra que un modelo generativo responda bien.

| Brazo evaluado | Resultado | Interpretación correcta |
|---|---|---|
| *Fixture* determinista | 18/18 | La compuerta funciona sobre casos construidos; no mide un modelo. |
| Qwen generativo mediante puente externo | Primer lote rechazado por contener infraestructura interna; segundo lote sin salida estructurada evaluable. | Resultado **no concluyente**; no corresponde llamarlo abstención ni fracaso de respuesta. |
| Gemini mediante Antigravity | La lectura inicial dio 11/18 porque mezclaba casos exportables y `local_only`. El corte legítimo —5 positivos y 6 negativos— pasó 11/11 al reevaluar el mismo artefacto. | Valida solo el subconjunto permitido; no resuelve los 7 positivos locales ni compara proveedores. |
| Paquete local de procedencia | 7/7 fuentes quedaron alineadas después de probar fallos de ámbito, fragmento, manifiesto y vigencia. | Están listas para revisión humana; aún no existe una respuesta local evaluada. |

La corrección de 11/18 a 11/11 no mejora artificialmente un puntaje: repara el universo de evaluación. Una fuente marcada `local_only` no se vuelve exportable porque un escáner de secretos no encuentre coincidencias. La gobernanza comienza precisamente cuando el denominador también respeta los permisos.

El siguiente peldaño es concreto: ejecutar una respuesta local autorizada, conservar los negativos y revisar cada salida por una persona. Hasta entonces, la evidencia permite hablar de una compuerta de atribución; no de una memoria generativa fiable.

---

## Cierre: una memoria útil antes que un clon digital

En este proyecto, «clon digital» es un horizonte retórico, no una categoría técnica validada. No usaré ese nombre para un RAG con más documentos ni para un avatar que responde con seguridad. Lo reservaría, como mínimo, para un sistema con memoria temporal capaz de rectificarse; preferencias y límites revocables; evidencia de autoría; comportamiento evaluado en situaciones nuevas; y control humano sobre qué se conserva, comparte o elimina. MemGPT y los agentes generativos de Park et al. ofrecen arquitecturas influyentes para manejar contexto, recuerdos, reflexión y planificación, pero no convierten esas funciones en identidad (Packer et al. 2023; Park et al. 2023).

La ruta defendible queda organizada en cinco compuertas:

1. **Procedencia y admisión.** Toda fuente entra con rol, ámbito, sensibilidad, consentimiento y salida permitida. Leer no equivale a promover.
2. **Tiempo y contradicción.** Una actualización debe conservar lo anterior, declarar desde cuándo rige y cerrar ante sucesores incompatibles.
3. **Recuperación y respuesta.** El sistema debe encontrar evidencia suficiente, citar la que realmente recibió y abstenerse cuando falta.
4. **Autoría y agencia.** Ningún correo entrante autoriza inferencias sobre estilo, valores o identidad; esas afirmaciones requieren material propio, adhesión expresa y revisión.
5. **Control y reversibilidad.** Toda memoria sensible necesita veto, purga por ámbito, trazabilidad y posibilidad efectiva de revocación.

La evidencia de esta tercera parte permite describir `penta-agent` como un prototipo local de memoria gobernada: conserva experiencia, registra correcciones, expone una proyección pública limitada y permite que sus pruebas fallen sin alterar producción. Eso es más preciso —y más defendible— que llamarlo clon digital.

El próximo avance no consiste en añadir más nodos. Consiste en cerrar la evaluación local de respuestas y comparar alternativas —Graphiti, GraphRAG o `deja-vu`— bajo el mismo corte, los mismos permisos y criterios de salida observables. Una memoria digna de confianza no es la que presume recordarlo todo, sino la que puede explicar **de dónde obtuvo cada afirmación, desde cuándo vale, quién puede verla y cuándo debe responder «no lo sé»**.

---

## Referencias

### Bibliografía

Cormack, Gordon V., Charles L. A. Clarke y Stefan Büttcher. 2009. «Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods». En *Proceedings of the 32nd Annual International ACM SIGIR Conference on Research and Development in Information Retrieval*, 758–59. Nueva York: Association for Computing Machinery. <https://doi.org/10.1145/1571941.1572114>.

Edge, Darren, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness y Jonathan Larson. 2024. «From Local to Global: A GraphRAG Approach to Query-Focused Summarization». arXiv, 24 de abril de 2024; revisión del 19 de febrero de 2025. <https://arxiv.org/abs/2404.16130>.

Hu, Yuyang, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu, Fangyi Zhu, Jiahang Lin et al. 2025. «Memory in the Age of AI Agents». arXiv, 15 de diciembre de 2025. <https://arxiv.org/abs/2512.13564>.

Lebo, Timothy, Satya Sahoo y Deborah McGuinness, eds. 2013. *PROV-O: The PROV Ontology*. Recomendación del W3C, 30 de abril de 2013. <https://www.w3.org/TR/prov-o/>.

Nissenbaum, Helen. 2004. «Privacy as Contextual Integrity». *Washington Law Review* 79, n.º 1: 119–58. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/>.

Packer, Charles, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica y Joseph E. Gonzalez. 2023. «MemGPT: Towards LLMs as Operating Systems». arXiv, 12 de octubre de 2023; revisión del 12 de febrero de 2024. <https://doi.org/10.48550/arXiv.2310.08560>.

Park, Joon Sung, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang y Michael S. Bernstein. 2023. «Generative Agents: Interactive Simulacra of Human Behavior». En *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, artículo 2, 1–22. Nueva York: Association for Computing Machinery. <https://doi.org/10.1145/3586183.3606763>.

Rasmussen, Preston, Pavlo Paliychuk, Travis Beauvais, Jack Ryan y Daniel Chalef. 2025. «Zep: A Temporal Knowledge Graph Architecture for Agent Memory». arXiv, 20 de enero de 2025. <https://arxiv.org/abs/2501.13956>.

Wu, Di, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang y Dong Yu. 2024. «LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory». arXiv, 14 de octubre de 2024; revisión del 4 de marzo de 2025. Trabajo aceptado en ICLR 2025. <https://arxiv.org/abs/2410.10813>.

Wu, Di, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng y Kai-Wei Chang. 2026. «LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues». Trabajo en curso, arXiv, 12 de mayo de 2026. <https://arxiv.org/abs/2605.12493>.

Zhang, Yanzhao, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie et al. 2025. «Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models». arXiv, 5 de junio de 2025. <https://arxiv.org/abs/2506.05176>.

### Software y documentación técnica

GetZep. s. f. *Graphiti: A Framework for Building Temporal Knowledge Graphs*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/getzep/graphiti>.

Hugging Face. s. f. *Sentence Transformers*. Documentación técnica. Consultada el 31 de agosto de 2026. <https://www.sbert.net/>.

Letta AI. s. f. *Letta Code*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/letta-ai/letta-code>.

Mem0 AI. s. f. *Mem0: Universal Memory Layer for AI Agents*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/mem0ai/mem0>.

Microsoft. s. f. *GraphRAG*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/microsoft/graphrag>.

Qwen. s. f. *Qwen3-Embedding-0.6B*. Tarjeta de modelo, Hugging Face. Consultada el 31 de agosto de 2026. <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>.

Qwen. s. f. *Qwen3-Reranker-0.6B*. Tarjeta de modelo, Hugging Face. Consultada el 31 de agosto de 2026. <https://huggingface.co/Qwen/Qwen3-Reranker-0.6B>.

Shulcz, Vladislav. s. f. *deja-vu*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/vshulcz/deja-vu>.

Vasturiano. s. f. *3d-force-graph*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/vasturiano/3d-force-graph>.

Vectorize. s. f. *Hindsight: Agent Memory That Learns*. Repositorio de GitHub. Consultado el 31 de agosto de 2026. <https://github.com/vectorize-io/hindsight>.

> **Conflictos de interés de las fuentes.** Las tarjetas de modelo, los repositorios y varios artículos de sistemas están escritos por sus propios desarrolladores o por organizaciones que ofrecen servicios asociados; LongMemEval-V2, además, sigue declarado como trabajo en curso. Se usan aquí para documentar arquitectura, funciones declaradas y estado de mantenimiento, no para aceptar afirmaciones de superioridad. Las métricas de `penta-agent` también son evidencia producida por el propio proyecto y requieren artefactos reproducibles y revisión independiente antes de sostener comparaciones generales.
{: .notice--info}
