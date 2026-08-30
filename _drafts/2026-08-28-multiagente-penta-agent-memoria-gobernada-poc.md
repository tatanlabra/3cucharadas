---
layout: single
title: "Multiagentes en 3 cucharadas III: una memoria que deja huellas"
subtitle: "Del RAG auditable a una base de conocimiento gobernada — y lo que todavía impide llamarla clon digital"
date: 2026-08-28 00:00:00 -0400
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, rag, memoria-agentes, procedencia, privacidad, gobernanza, knowledge-graph, threejs]
description: "Tercera bitácora de penta-agent: una proyección 3D regenerada desde la memoria real, las fronteras entre RAG, correo y tesis, y una ruta verificable —no una promesa— hacia un clon digital."
excerpt: "El RAG ya acumuló trazas de trabajo. El desafío no es dibujarlas: es decidir qué memoria merece persistir, cuándo deja de ser válida y qué evidencia faltaría para hablar responsablemente de un clon digital."
author: clabra
lang: es
ref: multiagente-penta-agent-memoria-gobernada-poc
permalink: /ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria.webp
  og_image: /assets/images/teasers/teaser-multiagentes-memoria.webp
  og_image_alt: "Grafo 3D de estrategias aprendidas por un sistema multiagente"
---

> **Estado de esta entrada.** Borrador ejecutable y local. La visualización se generó el 29 de agosto de 2026 desde una proyección pública saneada: no contiene cuerpos de correo, adjuntos, direcciones, rutas absolutas, tokens ni credenciales. No está publicada ni se ha enviado a remoto.
{: .notice--warning}

En la [segunda cucharada](/ia/productividad/desarrollo/multiagente-penta-agent-memoria/) el objetivo era más acotado: comprobar que una memoria podía recuperar evidencia y reconocer cuándo no la encontraba. Esa pieza existe. Lo que faltaba era mirar su consecuencia: una memoria que crece deja de ser sólo un índice y se vuelve una responsabilidad de procedencia, vigencia, acceso y revisión.
{: .text-justify}

Esta tercera parte corrige además dos errores míos. La primera versión de este borrador reducía el sistema a cuatro nodos decorativos. Era segura, pero no era informativa: convertía una base de conocimiento real en una alegoría. La segunda corrección es menos vistosa: un grafo de comandos puede ser fiel y, a la vez, ilegible. La seguridad no se consigue dibujando menos; se consigue aplicando límites verificables a una proyección que siga siendo reconociblemente derivada de la evidencia. Por eso el visor de abajo conserva sus estrategias, relaciones y fallos, pero comienza por una pregunta humana: **¿qué tipo de trabajo se ha aprendido a hacer?**
{: .text-justify}

> **Convención de lectura.** **HECHO** nombra una medición local fechada y reproducible; **INFERENCIA** nombra una decisión de diseño extraída de esos rastros; **NO VERIFICADO** nombra una capacidad que deliberadamente no se atribuye al sistema. Esta distinción es parte de la demostración: evita que un número, una arista o una prueba de infraestructura se presente como evidencia de comprensión, fidelidad de respuesta o identidad.
{: .notice--info}

## Cucharada 1: qué cambió desde II

RAG no es sinónimo de memoria de agentes, ni memoria equivale a identidad. La literatura reciente distingue recuperación, memoria, gestión de contexto y evaluación porque cumplen funciones distintas.[^memory-taxonomy] Esta entrada usa esa distinción para mostrar progreso sin convertirlo en una promesa de autonomía.
{: .text-justify}

El cierre de II dejó cuatro compromisos verificables, no una promesa vaga de “recordar más”. III los retoma con una regla de honestidad: una pieza sólo cuenta como resuelta cuando existe un artefacto, una prueba y un límite declarado. Esta es la cuenta corta antes de abrir el visor.
{: .text-justify}

| Pendiente al cerrar II | Qué III implementó localmente | Estado que sería engañoso ocultar |
|---|---|---|
| Comparar recuperación densa, léxica y *reranking* sin confundir una mejora local con producción. | Un *staging* Qwen aislado, con corte congelado de 319 contextos, negativos preservados y pruebas de ordenamiento, instrucción de consulta y *reranker*. El siguiente experimento sólo acepta una taxonomía de intención/familia documental ligada a hashes del corte y declarada `source_only`. | El mejor pase aún deja 2 casos parciales: el gate estricto sigue rojo, no hubo promoción y todavía falta la curación humana independiente de esa taxonomía. |
| Evaluar si una respuesta usa las fuentes recuperadas y sabe abstenerse. | `context-answer-v1`: 18 casos saneados que exigen cobertura de afirmaciones, citas recuperadas y abstención en negativos; el corte externo permitido pasó 11/11. | No es una evaluación integral de fidelidad generativa ni reemplaza la revisión humana de los 7 casos locales. |
| Añadir vigencia sin borrar la historia. | Un sandbox conserva evidencia anterior, admite `supersedes` sólo desde la fecha posterior y rechaza sucesores competidores. | No hay todavía razonamiento temporal conectado a la memoria viva ni adjudicación automática de contradicciones. |
| Hacer visible una memoria que crece sin confundir topología con verdad. | Un visor 3D estático, regenerado desde una proyección saneada, con categorías de trabajo y alternativa textual tanto en el post como dentro del visor cuando falta WebGL. | El visor no consulta Qdrant, no valida aristas y no representa una mente o identidad. |

Por eso la tercera parte no anuncia un sistema terminado. Muestra qué cambió desde una recuperación evaluable a una memoria con fronteras, qué pruebas ya pueden fallar y dónde todavía hace falta decidir, medir o pedir autorización humana.
{: .notice--primary}

| Capa | Evidencia local al 29 de agosto de 2026 | Qué permite sostener | Qué todavía **no** permite sostener |
|---|---|---|---|
| Memoria de experiencia de `penta-agent` | Corte público generado el 29 de agosto: 16.955 puntos del índice derivado; 1.432 estrategias, 3.949 relaciones, 12 comunidades y 8 tipos de tarea. | Que existen trazas operativas, vecindades semánticas y relaciones de corrección explorables. | Que cada arista sea una verdad causal, ni que el sistema responda correctamente a cualquier pregunta. |
| Contexto curado entre agentes | 319 contextos canónicos en `penta_context_v2`; en la comprobación local de esta entrada la colección respondió `green` y sigue siendo derivada de registros locales. | Que un handoff o decisión curada puede recuperarse con procedencia. | Que todo el historial de trabajo esté curado o que el índice sustituya al registro canónico. |
| Embeddings densos sin Ollama | `Qwen3-Embedding-0.6B` en staging directo: corte explícito de 319 contextos, 1024D en CPU y 319/319 persistidos en `penta_context_qwen3_staging`. Un segundo pase, con la política de ordenamiento declarada, dejó 38 pases, 2 parciales y 0 *miss*; los 8 negativos abstuvieron. | Que existe una vía reproducible, aislada y sin Ollama para poner a prueba y depurar un recuperador. | Que Qwen mejore la línea base, que el gate estricto esté aprobado o que deba promoverse. |
| Correo personal | Piloto local agregado: 12.072 mensajes únicos, 8.559 duplicados y años 2011–2026. El reporte privado no se versiona. | Que el inventario de sólo lectura funciona dentro de un alcance autorizado. | Que el correo sea un corpus público, una base semántica o una descripción de otras personas. |
| Memoria personal local | Prototipo separado con mbox acotado, SQLite/FTS, scopes explícitos, purga y evaluación sintética. | Que hay una ruta técnica para recuperar material privado sin mezclarlo con el RAG de agentes. | Que esté autorizado un flujo generativo sobre correo sensible o un modelo de personalidad. |
| Tesis y documentos de investigación | Instantánea pública de un índice derivado: 796 artefactos textuales de proceso, 533 vínculos y 7 *leads*; SQLite FTS5 y TF-IDF léxico, sin *embeddings* neuronales. Excluye fuentes históricas, DTA, Parquet, PDF e imágenes. | Que el proceso de investigación puede aportar trazabilidad verificable sin exponer fuentes, textos, rutas ni microdatos. | Que el índice pruebe ejecución histórica, replicación, resultados sustantivos o datos de investigación. |

Hay dos lecturas a la vez. La deductiva parte de una regla sencilla: si una fuente puede equivocarse, cambiar o ser privada, su origen y su ámbito deben viajar con ella. PROV-O formaliza precisamente la diferencia entre entidad, actividad y agente; no basta con recuperar un texto, importa qué lo produjo y mediante qué transformación.[^prov-o] La inductiva parte de los rastros observados: el RAG ya acumula estrategias repetidas, comunidades, correcciones y fallos. El grafo no inventa esas capas; las vuelve inspeccionables.
{: .text-justify}

También apareció una dependencia real que no se veía en el gráfico antiguo. El visor histórico asumía un vector simple; el índice actual usa el vector nombrado `dense`. La primera regeneración quedó degradada, sin aristas semánticas; una prueba posterior contra el índice real reveló la incompatibilidad de formato. Al adaptar el exportador y repetir la corrida, volvieron 3.658 aristas semánticas. No es una anécdota de implementación: una visualización de memoria sólo es honesta si puede mostrar cuándo su cadena de datos se degradó, por qué y cuándo se recompuso.
{: .text-justify}

### Del rastro técnico a una pregunta humana

La unidad mínima del índice sigue siendo una estrategia observada —muchas tienen forma de comando, porque así quedaron registradas las acciones—. Eso es bueno para auditar, pero malo para explicar. Para que el mapa pueda leerse antes de conocer Bash, Python o Qdrant, añadí una clasificación determinista y visible sobre esas trazas. No usa un modelo para adivinar intenciones: aplica reglas públicas a la estrategia, herramienta, transporte y proyecto, y mantiene el identificador técnico original al abrir una ficha.
{: .text-justify}

| Tipo de trabajo derivado | Estrategias en esta corrida | Ejemplo de lo que permite preguntar |
|---|---:|---|
| Coordinar agentes y decisiones | 399 | ¿Qué se aprendió al dejar un handoff o delegar una tarea? |
| Investigar y analizar datos | 396 | ¿Qué tácticas se repiten al revisar la tesis, datos y fuentes? |
| Leer y rastrear evidencia | 385 | ¿Qué antecedentes se inspeccionaron antes de tomar una decisión? |
| Ejecutar y automatizar | 118 | ¿Qué pasos implementaron un cambio una vez revisado? |
| Versionar y comparar cambios | 76 | ¿Qué controles se aplicaron antes de conservar una modificación? |
| Probar y verificar | 28 | ¿Qué se comprobó en vez de sólo declararse listo? |
| Operar herramientas y servicios | 18 | ¿Qué infraestructura hizo posible o bloqueó el flujo? |
| Editar y comunicar | 12 | ¿Qué transformó evidencia técnica en documentación o publicación? |

Esta capa es una lente pedagógica, no una ontología del autor ni una nueva verdad canónica. Una estrategia puede participar de más de una tarea y hoy queda en la primera familia que satisfacen sus reglas. Esa simplificación está declarada para que pueda corregirse: sirve para orientarse, no para medir productividad ni atribuir capacidades humanas al sistema.
{: .text-justify}

### Qué mide este mapa — y qué no

Una arista semántica indica vecindad entre centroides de estrategias indexadas; una arista estructural deriva de herramientas, repositorios o transportes compartidos; una arista de corrección conecta un fallo con una estrategia posterior relacionada. Son tres señales distintas. El tamaño del nodo resume evidencia observada; los colores iniciales agrupan tipos de tarea y los paneles permiten pasar a comunidades, proyectos, estado, agente y salud. Ninguna de esas señales demuestra intención, comprensión humana o una biografía coherente.
{: .text-justify}

La cautela importa porque las evaluaciones de memoria de largo plazo no se limitan a recuperar una frase. LongMemEval separa extracción, razonamiento multisesión, temporalidad, actualización de conocimiento y abstención.[^longmemeval] Este proyecto tiene evidencia de recuperación y de admisión; todavía no tiene una evaluación defendible de fidelidad de respuestas sobre correo, tesis o una representación del autor.
{: .text-justify}

## Cucharada 2: una base de conocimiento no se construye sólo con embeddings

La base existente tiene capas con permisos y funciones diferentes. El ledger y los archivos fuente son canónicos; Qdrant es un índice regenerable; el visor es una proyección pública; los adaptadores privados viven fuera de Git. Esta separación es menos vistosa que decir “tengo un cerebro digital”, pero evita que una coincidencia vectorial se transforme, sin revisión, en un hecho o una identidad.
{: .text-justify}

### La PoC no es una licuadora de fuentes

El diagrama siguiente hace explícito algo que un grafo 3D no debe sugerir: correo, tesis y RAG no son “nodos más” de una misma bolsa. En esta etapa sólo la memoria de trabajo curada alimenta recuperación entre agentes y la proyección pública. El correo mantiene una ruta privada, reversible y vetable; tesis y documentos sólo aportan trazabilidad autorizada. Las flechas describen salidas permitidas, no transferencias automáticas de contenido ni inferencias sobre personas.
{: .text-justify}

<figure class="align-center">
  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" alt="Tres fuentes gobernadas: RAG de trabajo permite recuperación con procedencia; correo personal permite sólo revisión privada y reversible; tesis y documentos permiten citas y estado de verificación. Una frontera prohíbe publicar cuerpos de correo, adjuntos, direcciones, rutas absolutas, microdatos e inferencias de identidad." loading="lazy" decoding="async">
  </a>
  <figcaption>Figura 1. La integración actual es una arquitectura de permisos: la fuente determina su salida permitida, no una promesa de memoria total.</figcaption>
</figure>

### La tesis entra como trazabilidad de proceso, no como corpus

El avance concreto de esta versión no es “meter la tesis al RAG”. Es una [instantánea pública del índice de investigación]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}) generada desde su manifiesto derivado después de verificar su contrato local. La tarjeta publica sólo una lista blanca de metadatos: **796** artefactos textuales derivados —316 auditorías, 244 reportes, 133 contratos, 71 pseudocódigos y 32 piezas de inventario, réplica o documentación—; **533** vínculos de proceso y **7** asuntos que siguen requiriendo revisión. No entrega documentos, títulos, rutas, hashes individuales, resultados de consultas, archivos fuente ni microdatos.
{: .text-justify}

La distinción importa más que el número. La capa de consulta es SQLite FTS5 más TF-IDF léxico reproducible: no es un *embedding* neuronal ni una afirmación de comprensión. Sus exclusiones son explícitas —fuente histórica, DTA, Parquet, PDF e imágenes— y la tarjeta declara que no demuestra ejecución histórica, réplica ni hallazgos sustantivos. Es una forma útil de sumar conocimiento de alto valor: permite preguntar por la cadena de investigación y por sus vacíos sin convertir datos, borradores o conclusiones pendientes en memoria pública del agente.
{: .text-justify}

| Problema que viene | Activo existente | Biblioteca o proyecto que merece una prueba seria | Criterio para adoptarlo — o descartarlo |
|---|---|---|---|
| Recuperar episodios de trabajo entre *harnesses* de programación | Handoffs, eventos y contexto curado de `penta-agent`. | [`deja-vu`](https://github.com/vshulcz/deja-vu), que recupera sesiones locales de distintos agentes por MCP. | Debe mejorar una búsqueda histórica real sin reemplazar registros curados por transcripciones crudas. |
| Mantener estado explícito de un agente | RAG evaluado y un contexto curado; no un runtime de memoria general. | [Letta](https://github.com/letta-ai/letta), continuación operativa de MemGPT.[^memgpt] | Comparar su memoria jerárquica con los contratos actuales antes de añadir otro runtime. |
| Probar embeddings densos sin Ollama | `penta_context_v2` sigue como línea base; `penta_context_qwen3_staging` es una colección derivada y aislada. | [`Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B), ejecutado mediante Sentence Transformers.[^qwen-embedding] | Una taxonomía de intención/familia, `source_only` y ligada a hashes debe resolver los dos parciales sin alterar admisión, negativos, `k` ni la colección activa; luego comparar calidad, latencia y CPU antes de considerar una migración. |
| Extraer recuerdos desde conversaciones o documentos | Ingesta y curación humana; correo privado con veto y scope. | [Mem0](https://github.com/mem0ai/mem0) y [Hindsight](https://github.com/vectorize-io/hindsight). | Medir precisión, revocación y falsos positivos en un conjunto sintético antes de cualquier extracción automática de correo. |
| Representar vigencia, sustitución y contradicción | Un sandbox prueba sucesión explícita y falla cerrado ante orden temporal inválido o sucesores competidores; no hay razonador temporal general. | [Graphiti](https://github.com/getzep/graphiti) y la arquitectura temporal de Zep.[^graphiti] | Llevar el caso desde fixture a decisiones de tesis o proyecto, conservando fuente, vigencia y revisión humana. |
| Conectar documentos de investigación, conceptos y citas | Instantánea de procedencia con lista blanca del índice derivado: 796 artefactos de proceso, 533 vínculos y búsqueda FTS5/TF-IDF, sin contenido exportado. | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) para un experimento acotado de corpus científico.[^graphrag] | Comparar costo, trazabilidad de citas y recuperación contra el baseline léxico actual; no ingerir microdatos, fuentes históricas ni archivos sin autorización. Un preflight local ya rechaza corpus, scope o presupuesto sin aprobación humana. El repositorio está en modo de mantenimiento y advierte que indexar puede ser costoso: aquí sería una prueba mínima y comparativa, no una dependencia de base. |
| Visualizar sin inventar una topología | Generador local y `3d-force-graph` vendorizado. | [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph), ya reutilizado en esta exportación. | Mantener una alternativa textual y una proyección saneada; no convertir distancia visual en afinidad humana. |

Este es el *mea culpa* metodológico del post: había tratado algunas de estas librerías como referencias bibliográficas cuando, para mis flujos de investigación, varias merecen experimentos comparativos de verdad. La prioridad no es instalar todas. Es probar primero las que pueden reducir fricción científica sin degradar trazabilidad: GraphRAG para documentos con citas verificables, Graphiti para vigencia y contradicción, y `deja-vu` para recuperar decisiones distribuidas entre sesiones de programación. Mem0 y Hindsight son más riesgosas para correo y perfil personal: antes necesitan un conjunto de evaluación, revocación visible y una pregunta de uso legítima.
{: .text-justify}

El ensayo con Qwen aclara también qué significa “probar”. No se cambió un servicio ni se reescribió la colección activa: se creó un entorno local aislado, se fijaron versiones, se descargó el modelo sólo bajo una señal explícita y se apuntó a otra colección. El corte guarda los 319 identificadores de contexto y su huella, no sus textos; por eso una reanudación no puede mezclar registros que llegaron después. El *smoke* verificó el modelo directo, 1.024 dimensiones y ejecución CPU. La reindexación terminó 319/319 y el *batching* persiste grupos acotados; una prueba fuerza 17 registros para comprobar que quedan 16+1 y que un registro congelado que desaparece detiene la corrida.

El primer resultado fue deliberadamente incómodo: sobre 40 consultas del set dorado, hubo 36 pases completos, 3 parciales y un *miss* en una pregunta coloquial con error tipográfico sobre el puente de delegación; los 8 negativos sí abstuvieron. El diagnóstico mostró que Qwen sí recuperaba el handoff correcto como segundo vecino denso, pero el bonus BM25 de `0,10` —que sólo reordena candidatos ya admitidos— lo expulsaba del top-5 por una coincidencia sparse genérica.

No cambié la política productiva por ese solo hallazgo. La variante Qwen declara un bonus BM25 de `0,00`, exclusivamente en staging; una prueba roja/verde reproduce el desplazamiento y luego restituye el vecino denso más fuerte. El segundo pase reutilizó los mismos 319 puntos, sin reindexar ni tocar `penta_context_v2`: dejó 38 pases, 2 parciales y ningún *miss*; el *recall@5* subió a 0,9635 y el MRR a 0,8396, con las 8 abstenciones negativas intactas. Pero los dos parciales multifuente de catastro bastan para que el evaluador estricto siga fallando.

También probé la recomendación de Qwen de declarar una instrucción de recuperación, pero no convertí una recomendación de biblioteca en dogma. Sobre exactamente el mismo corte, una instrucción genérica para privilegiar fuentes completas y citables cayó a 33 pases, 3 parciales y 4 fallos; las abstenciones negativas bajaron de 8/8 a 6/8. Esa corrida reutilizó los 319 vectores: aisló el cambio al vector de consulta y falsó la hipótesis sin tocar documentos ni producción. Por eso el prompt `query` nativo queda como predeterminado y la instrucción personalizada sólo existe como parámetro experimental. La colección sigue en staging: no establece una mejora frente a la línea base y no se promueve. No debe confundirse con el Qwen del puente externo de la sección siguiente: aquél era un modelo generativo fuera del ámbito local y su resultado fue no concluyente; éste es un experimento de *embeddings* con una mejora acotada y una falla aún abierta.[^qwen-embedding]
{: .notice--warning}

El siguiente candidato fue un reranker local de la misma familia, `Qwen3-Reranker-0.6B`: recibe sólo documentos que ya habían pasado la admisión y los reordena; no puede inventar una fuente ni levantar un negativo. En el corte fijo, sí recuperó el tercer documento del caso multifuente en español y llevó el *recall@5* de 0,9635 a 0,9688, con MRR 0,9010 y las 8 abstenciones preservadas. Pero dejó 38 pases, 2 parciales y 0 fallos: el parcial dejó de ser ese caso de catastro y apareció en `penta-agent`/skills. Peor aún, la latencia mediana subió de 2,37 s a 15,83 s, con un máximo de 91,10 s. Es una comparación honesta, no una adopción: por ahora sólo sirve como carril local de análisis offline cuando ese costo pueda justificarse.[^qwen-reranker]
{: .text-justify}

Una sonda posterior, de sólo lectura y sobre la misma colección aislada, precisó por qué no declaré victoria. Para las dos preguntas multifuente de catastro, los documentos esperados que faltaban del top‑5 sí aparecían entre los candidatos: en los rangos 7 y 10, respectivamente. Es decir, el modelo no había “olvidado” esas fuentes; el recuperador todavía no logra cubrir familias documentales distintas dentro de cinco lugares. Subir `k` hasta que el resultado pase cambiaría la pregunta de evaluación, no resolvería la selección.

El paso siguiente tampoco añade una heurística opaca: el contrato de staging ya rechaza una etiqueta que no esté ligada al hash del corte, al hash de la consulta y a una familia de vocabulario cerrado; también rechaza cualquier etiqueta que declare haber usado el set dorado. Aún no hay etiquetas humanas independientes, por lo que no existe una corrida nueva que mostrar ni un parcial “resuelto”. Lo valioso aquí es más modesto: la próxima hipótesis ya puede fallar sin tocar admisión, negativos, `k` ni la colección activa.
{: .notice--warning}

Probé entonces una diversificación acotada por `repo_scope`: dentro de una ventana de 20, reordena sólo candidatos que ya habían pasado la admisión para dar cabida a ámbitos de procedencia distintos. Conservó los 319 puntos, las 8/8 abstenciones y cero fallos; mejoró el *recall@5* agregado de 0,9635 a 0,9740 y resolvió el caso multifuente en inglés. Pero el resultado estricto siguió en 38 pases y 2 parciales: el caso español aún dejó fuera el handoff de mapas y, a cambio, apareció un parcial en las skills de `penta-agent`. Es un resultado útil precisamente porque no es una victoria: `repo_scope` es una aproximación demasiado gruesa a “familia documental”.

Como segundo control, fusioné el orden base y el del reranker con *reciprocal rank fusion* (RRF), un método clásico de combinación de rankings.[^rrf] Tampoco agregaba documentos ni elevaba `k`: reutilizó los mismos 319 puntos y conservó las 8/8 abstenciones. El resultado volvió al **38/2**, con *recall@5*=0,9635 y una mediana de 20,06 s; no recuperó ninguno de los dos parciales de catastro. La secuencia importa más que el nombre del algoritmo: RRF es una herramienta razonable, pero en este corpus no compensa el costo ni cierra el contrato. Ambos comparadores quedan offline, sin promoción. La siguiente hipótesis exige metadatos curados de linaje o intención documental y un corte de evaluación que compruebe que una mejora no traslada el error a otra tarea.
{: .notice--info}

### Bitácora de decisión: qué aprendió el recuperador

Todas estas corridas usan el mismo corte de 319 contextos, las mismas 40 consultas y `k=5`; no cambian documentos, producción ni la definición de éxito. Esta tabla no es un *leaderboard*: hace visible qué hipótesis sobrevivió y cuál no.

| Pregunta puesta a prueba | Cambio aislado | Resultado observado | Decisión |
|---|---|---|---|
| ¿El bonus sparse expulsa evidencia densa correcta? | BM25 de `0,10` a `0,00`, sólo en staging. | De 36/3/1 a **38/2/0**; 8/8 negativos siguen absteniendo. | Se conserva como punto de partida experimental; no prueba mejora frente a producción. |
| ¿Una instrucción genérica de consulta mejora la citabilidad? | Instrucción Qwen explícita. | **33/3/4** y 6/8 negativos. | Rechazada: empeora cobertura y abstención. |
| ¿Un reranker recupera fuentes complementarias? | `Qwen3-Reranker-0.6B` sobre candidatos admitidos. | **38/2/0**; MRR 0,9010, pero p50 15,83 s y un parcial se traslada a skills. | Sólo análisis offline; no promoción. |
| ¿El ámbito del repositorio equivale a familia documental? | Diversificación por `repo_scope`. | **38/2/0**; *recall@5* 0,9740, pero el error cambia de lugar. | Rechazada: procedencia no es intención documental. |
| ¿El consenso entre ambos órdenes evita ese traslado? | Fusión RRF base + reranker. | **38/2/0**; p50 20,06 s; catastro sigue parcial. | Rechazada: no justifica el costo ni cierra el gate. |

{: .text-justify}

El correo ilustra por qué. Poder leer un mensaje en Thunderbird no autoriza a promoverlo a memoria durable, inferir preferencias o publicarlo. La integridad contextual de Nissenbaum nombra esa diferencia entre acceso y flujo apropiado de información.[^nissenbaum] Por eso el correo aparece aquí como capacidad gobernada y agregado revisado, no como esfera brillante en un grafo público.
{: .text-justify}

## Cucharada 3: el grafo que ya existe

La visualización siguiente se generó localmente desde un corte de la memoria de experiencia y luego se saneó para publicación. El visor no llama a Qdrant ni a servicios externos: recibe un artefacto estático, regenerable y auditado. La apertura a pantalla completa conserva el visor profesional completo; esta página aporta el contexto y los límites. Si el visor se abre en un navegador sin WebGL, no deja un lienzo vacío: muestra las métricas derivadas y las ocho familias de trabajo en una alternativa textual propia.
{: .text-justify}

La [exportación pública en JSON]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) acompaña al visor para permitir una inspección reproducible de esta corrida. El generador, su plantilla y el motor vendorizado también quedan versionados con el sitio: antes de publicar, el HTML debe reproducirse exactamente desde ese JSON público, sin releer fuentes privadas. Es una derivación para lectura, no la memoria canónica.
{: .text-justify}

**Lectura guiada en tres pasos.** Primero abre la pestaña **Tareas** y elige, por ejemplo, “Investigar y analizar datos”: el mapa se concentra en las tácticas asociadas a esa labor. Después mira **Proy** para distinguir dónde ocurrieron —tesis, `penta-agent` u otros repositorios—. Sólo al final usa **Errores** o el modo diagnóstico para revisar una fricción concreta. Así el visor no pide interpretar una nube técnica antes de saber qué pregunta está respondiendo.
{: .notice--primary}

<section class="rag-knowledge-graph" aria-labelledby="rag-knowledge-graph-title">
  <div class="rag-knowledge-graph__header">
    <div>
      <p class="rag-knowledge-graph__eyebrow">Proyección pública · 2026-08-29</p>
      <h3 id="rag-knowledge-graph-title">Mapa de trabajo aprendido por penta-agent</h3>
      <p>Corte del 29 de agosto: 1.432 estrategias · 3.949 relaciones · 8 tipos de tarea · 16.955 puntos indexados</p>
    </div>
    <a class="rag-knowledge-graph__open" href="{{ '/assets/visualizations/penta-rag-knowledge-graph/' | relative_url }}" target="_blank" rel="noopener">Abrir visor completo<span class="screen-reader-text"> en una pestaña nueva</span></a>
  </div>
  <iframe class="rag-knowledge-graph__frame" title="Mapa 3D navegable de tipos de trabajo y estrategias de penta-agent" src="{{ '/assets/visualizations/penta-rag-knowledge-graph/' | relative_url }}" loading="lazy" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>
</section>

Los números del visor pertenecen a ese corte reproducible, no a un contador vivo. La memoria canónica y sus índices pueden cambiar después; una actualización exige regenerar la proyección, volver a sanearla y revisar qué cambia antes de reemplazar el artefacto publicado.
{: .notice--info}

{: .table-caption}
**Tabla 1** — Alternativa textual y límites de la proyección

| Componente visible | Derivación | Lectura correcta |
|---|---|---|
| Tipos de tarea | Reglas deterministas sobre estrategia, herramienta, transporte y proyecto. | Un punto de partida didáctico para formular una pregunta; no una clasificación psicológica ni exhaustiva. |
| Nodos de estrategia | Lecciones de experiencia con evidencia observada. | Una estrategia registrada, no una creencia ni un rasgo del autor. |
| Aristas semánticas | Vecindad de embeddings del índice derivado. | Similitud operacional, no causalidad. |
| Aristas estructurales y de corrección | Coocurrencia y secuencia temporal de eventos. | Una pista para inspeccionar una recuperación o un fallo; requiere abrir su procedencia. |
| Comunidades, proyectos y paneles | Agregaciones deterministas sobre la exportación. | Un mapa para explorar qué preguntar y dónde verificar, no un diagnóstico automático. |
| Correo y tesis | **No** están como nodos de contenido. | Sus capacidades, scopes y metadatos se describen arriba; su contenido sigue privado o bajo validación. |

La composición visual no intenta hacer legible cada una de las 3.949 relaciones a la vez. Empieza por tipos de tarea, permite aislar proyectos o errores y mantiene los nodos de detalle bajo interacción. Ése es el compromiso correcto entre una base real —demasiado grande para una ilustración— y una lectura pública —demasiado importante para un *hairball* opaco.
{: .text-justify}

## La nueva compuerta: de una fuente recuperada a una respuesta atribuida

Desde el post II el recuperador ya tenía preguntas doradas, métricas de ordenamiento y controles negativos. Eso no bastaba para una respuesta final: un modelo puede encontrar el documento correcto, citar otro, omitir la condición decisiva o contestar cuando debería abstenerse. Por eso separé ambos contratos.
{: .text-justify}

El nuevo conjunto local contiene 18 casos saneados: 12 preguntas con una o más afirmaciones obligatorias y 6 negativas. Para una positiva, cada afirmación debe apuntar a una fuente que el recuperador efectivamente entregó; para una negativa, la salida debe abstenerse sin adjuntar fuentes. La fixture determinista pasó 18/18, con cobertura de afirmaciones, validez de citas y abstención negativa de 1,0. Es evidencia de que el **gate** puede distinguir un contrato válido de uno inválido, no evidencia de que un modelo generativo ya responda bien.
{: .text-justify}

También observé el primer rojo externo. Un lote saneado enviado mediante el puente aislado de Qwen fue rechazado primero porque un fragmento recuperado incluía infraestructura interna; ese fragmento se filtró antes de cualquier exportación posterior. En el segundo intento, Qwen no devolvió un bloque estructurado evaluable. El resultado correcto no es ajustar el denominador ni llamar “abstención” a una ausencia: ese brazo queda **no concluyente**.
{: .notice--warning}

El 29 de agosto hice además una corrida separada con Gemini, mediante Antigravity y el mismo contrato aislado. Su lectura global dio 11/18: había 12 respuestas externas, pero se las estaba contrastando contra un set que también conservaba preguntas locales. Eso reveló una falla de diseño, no una medida razonable del proveedor. La verificación posterior del manifiesto canónico descubrió una séptima: el handoff de auditoría RSH está clasificado como `interno` y `local_only`. Que su escáner de secretos resulte limpio no lo vuelve exportable. Mantuve la pregunta y su afirmación, pero la saqué del corte externo; no fabriqué una síntesis pública ni forcé al recuperador a entregarla.
{: .text-justify}

El corte externo legítimo contiene entonces 5 positivos permitidos y 6 negativos. Al reevaluar exactamente el mismo artefacto, tuvo citas válidas, fuentes requeridas y abstención negativa correctas en sus 11 casos: **11/11**. Los siete positivos locales quedan fuera de ese benchmark, no resueltos ni borrados. Esto separa una fuente que no puede salir del ámbito local de una generación que cita mal; tampoco convierte ese 11/11 acotado en un resultado integral, una comparación entre modelos o una prueba de memoria fiable.
{: .text-justify}

El circuito local ya tiene un primer peldaño verificable, pero no es una respuesta fabricada por un modelo. Un paquete de procedencia revisa, sin invocar proveedor ni consultar Qdrant, que la fuente local exista, conserve el fragmento declarado, coincida con el hash de procedencia vigente y permanezca `local_only`. Se lo hizo fallar con un ámbito incorrecto, un fragmento ausente, un manifiesto ausente y una fuente modificada; luego, tras resincronizar selectivamente los registros que habían cambiado, la corrida vigente dejó los 7 de 7 casos listos para revisión humana. “Listo” significa que la evidencia local está alineada para ser revisada, no que un modelo ya respondió correctamente.
{: .notice--warning}

La consecuencia práctica sigue siendo menos vistosa que una tabla de puntajes: falta ejecutar una respuesta local autorizada que conserve los negativos y revisar cada respuesta por una persona. El paquete de procedencia no mide recuperación ni generación; por sí solo no da una tasa de acierto. Hasta entonces, ni Qwen ni Gemini autorizan la etiqueta de memoria fiable, y menos aún la de clon digital.
{: .text-justify}

## La ruta hacia un clon digital no está cerrada

Un clon digital no es “más contexto” ni un avatar que responda con seguridad. Implicaría, como mínimo, una memoria temporal capaz de rectificar, un modelo de preferencias y límites que pueda ser revocado, evidencia de autoría y una evaluación de comportamiento en situaciones nuevas. Los agentes generativos de Park et al. y la arquitectura de contexto de MemGPT ayudan a formular el problema, pero no prueban que este sistema tenga esas propiedades.[^park][^memgpt]
{: .text-justify}

La ruta que hoy puedo defender tiene cinco compuertas:
{: .text-justify}

1. **Procedencia y admisión.** Cada fuente nueva entra con rol, scope, sensibilidad, consentimiento y una salida permitida; leer no es promover.
2. **Tiempo y contradicción.** El sandbox ya conserva una decisión previa, admite una sucesión explícita sólo desde su fecha y rechaza sucesores competidores. Sigue sin ser un razonador temporal integrado: Graphiti es el comparador serio antes de llevar esa regla a la memoria viva.
3. **Evaluación de recuperación y respuestas.** Ya existe una compuerta local de citas, cobertura y abstención con 18 casos saneados. En paralelo, Qwen completó un corte aislado de 319 contextos. Una variante de ordenamiento declarada eliminó el *miss* inicial y dejó 38 pases completos y 2 parciales de 40, sin perder abstenciones negativas; el gate estricto continúa bloqueando la promoción por esos parciales multifuente. Es evidencia de una compuerta que permite aprender sin fabricar una victoria, no una mejora demostrada frente a producción. Una primera corrida generativa estructurada separó evidencia ausente de generación atribuida, pero falló el gate integral por recuperación incompleta. El paquete local de procedencia dejó las 7 de 7 fuentes listas para revisión tras probar sus fallos de alcance, manifiesto, fragmento y vigencia; sirve para detener una respuesta antes de usar evidencia vieja, no para declarar que un modelo respondió bien. Faltan recuperación autorizada y revisión humana.
4. **Autoría y agencia.** Un corpus autoescrito, una política de *claims* opt-in y revisión humana deben preceder cualquier afirmación sobre estilo, valores o preferencias. Correo entrante no sirve para ese fin.
5. **Control humano y reversibilidad.** Toda memoria sensible necesita veto, revocación, purga por scope y trazabilidad de la transformación que la llevó a una vista o respuesta.

La conclusión es menos espectacular y más útil: tengo una base de conocimiento multiagente que ya deja huellas. Puede recuperar contexto, conservar correcciones, mostrar su topología y mantener fuentes privadas fuera de la vitrina. Todavía no tengo un clon digital. Nombrar esa distancia es parte del trabajo; cerrarla exige experimentos comparativos, evidencia de comportamiento y decisiones humanas que ningún grafo puede tomar por mí.
{: .text-justify}

---

## Referencias

[^memory-taxonomy]: Yuyang Hu et al., «Memory in the Age of AI Agents» (2025). <https://arxiv.org/abs/2512.13564>

[^prov-o]: W3C, «PROV-O: The PROV Ontology», recomendación, 2013. <https://www.w3.org/TR/prov-o/>

[^longmemeval]: Di Wu et al., «LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory» (2024). <https://arxiv.org/abs/2410.10813>

[^memgpt]: Charles Packer et al., «MemGPT: Towards LLMs as Operating Systems» (2023). <https://doi.org/10.48550/arXiv.2310.08560>

[^graphiti]: Preston Rasmussen et al., «Zep: A Temporal Knowledge Graph Architecture for Agent Memory» (2025). <https://arxiv.org/abs/2501.13956>

[^graphrag]: Microsoft, «GraphRAG: modular graph-based Retrieval-Augmented Generation», repositorio, consultado el 30 de agosto de 2026. El README declara el proyecto en modo de mantenimiento, recomienda empezar pequeño y advierte sobre el costo potencial de indexación. <https://github.com/microsoft/graphrag>

[^qwen-embedding]: Yanzhao Zhang et al., «Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models» (2025), arXiv:2506.05176. La [tarjeta oficial de Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) documenta 1.024 dimensiones, soporte multilingüe y el uso de instrucciones para consultas.

[^qwen-reranker]: Qwen, [«Qwen3-Reranker-0.6B»](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B), tarjeta de modelo, consultada el 29 de agosto de 2026. Documenta la interfaz `CrossEncoder` de Sentence Transformers, soporte multilingüe e instrucciones definibles; las cifras anteriores son la corrida local de corte fijo, no un benchmark del proveedor.

[^rrf]: Gordon V. Cormack, Charles L. A. Clarke y Stefan Büttcher, «Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods», *Proceedings of the 32nd Annual ACM SIGIR Conference on Research and Development in Information Retrieval* (2009): 758–759. <https://doi.org/10.1145/1571941.1572114>

[^nissenbaum]: Helen Nissenbaum, «Privacy as Contextual Integrity», *Washington Law Review* 79, n.º 1 (2004): 119–158. <https://crypto.stanford.edu/portia/pubs/articles/N1500699020.html>

[^park]: Joon Sung Park et al., «Generative Agents: Interactive Simulacra of Human Behavior», *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology* (2023): 1–22. <https://doi.org/10.1145/3586183.3606763>
