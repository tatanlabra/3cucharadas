---
layout: single
title: "Multiagentes en 3 cucharadas III: una memoria que deja huellas"
subtitle: "Del RAG auditable a una memoria más gobernada: aún no es un clon digital"
date: 2026-09-03 00:00:00 -0400
last_modified_at: 2026-09-03 00:00:00 -0400
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, rag, memoria-agentes, procedencia, privacidad, gobernanza, knowledge-graph, evaluacion-rag, threejs]
description: "Tercera bitácora de penta-agent: procedencia, vigencia, evaluación y una proyección 3D saneada de la memoria de trabajo."
excerpt: "El sistema ya recupera y visualiza trazas. El problema ahora es gobernar qué persiste, qué caduca y qué nunca debe salir de su ámbito."
author: clabra
lang: es
ref: multiagente-penta-agent-memoria-gobernada-poc
permalink: /ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/
distribution:
  social: true
  republish: []
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, servicios locales (Qdrant y Sentence Transformers por loopback, timers systemd), Qdrant con vector nombrado `dense`"
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

> **Estado de la demostración.** El visor se regeneró el 29 de agosto de 2026 desde una proyección pública saneada (limpiando cosas no públicas :D ): el artefacto no contiene cuerpos de correo, adjuntos, direcciones, rutas absolutas, tokens, credenciales ni microdatos.
{: .notice--warning}

## Preámbulo: recordar no basta

En la [segunda parte](/ia/productividad/desarrollo/multiagente-penta-agent-memoria/) intenté resolver un problema acotado: que la memoria de `penta-agent` recuperara evidencia y reconociera cuándo no la encontraba. La pregunta de esta tercera parte es más práctica y surge con el funcionamiento acumulado: **¿qué ocurre con la memoria cuando crece y se vuelve difusa o incluso contradictoria?**

Un índice puede acumular fragmentos sin dificultad, y existen bastantes herramientas que ya lo satisfacen bien. Una memoria +útil, a mi jucio, debe conservar procedencia, vigencia, permisos, contradicciones y criterios de eliminación. También debe distinguir entre encontrar una fuente y usarla correctamente. La literatura reciente insiste en separar RAG, gestión de contexto y memoria de agentes, porque cumplen funciones diferentes y exigen evaluaciones distintas [^hu-2025].

La historia que sigue tiene tres movimientos: qué cambió desde la parte II; qué experimentos resistieron una evaluación +seria; y cómo mostrar la memoria sin hacerla pasar por una mente.

---
## Primera cucharada: de recuperar fragmentos a gobernar evidencia

En la parte II el problema era **recuperar bien**: encontrar el contexto pertinente y reconocer cuándo no había evidencia suficiente. Una memoria útil no solo recupera información, también necesita saber **de dónde vino, si sigue vigente, dónde puede usarse y qué está permitido hacer con ella**.

RAG resuelve principalmente la recuperación. La capa de memoria añade reglas para conservar, actualizar, relacionar o descartar evidencia. Ninguna de esas funciones equivale, por sí sola, a identidad. Para describir la procedencia utilizo conceptos compatibles con PROV-O —entidades, actividades y agentes—, mientras que vigencia, sensibilidad y permisos requieren reglas adicionales [^lebo-2013].

### Qué cambió desde la parte II

| Pendiente en II                                                | Qué existe ahora                                                                              | Qué sigue abierto                                                                            |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Comparar recuperación densa, léxica y reordenamiento.          | Un corte congelado de 319 contextos y 40 consultas evaluadas con `k=5`.                       | El mejor pase obtiene 38 casos completos y 2 parciales; la compuerta estricta sigue cerrada. |
| Comprobar que una respuesta use las fuentes y sepa abstenerse. | El contrato `context-answer-v1`, con 12 casos positivos y 6 negativos saneados.               | Falta completar la evaluación integral con modelo local y revisión humana reservada.         |
| Incorporar vigencia sin borrar la historia.                    | La PoC admite `supersedes` solo hacia versiones posteriores y rechaza sucesores competidores. | Todavía no existe un razonador temporal conectado a la memoria viva.                         |
| Mostrar el crecimiento sin convertir el grafo en verdad.       | Un visor 3D regenerable desde JSON saneado y acompañado por una alternativa textual.          | El visor no valida relaciones ni representa una mente.                                       |

La diferencia puede parecer pequeña, pero cambia la pregunta. Ya no basta con saber **qué fragmento está cerca de una consulta**; importa también saber **qué clase de evidencia es y bajo qué condiciones puede reutilizarse**.

### Qué memoria existe realmente

La PoC reúne varias capas, pero no las trata como equivalentes:

* **Experiencia de `penta-agent`:** 16.955 puntos indexados y 1.432 estrategias permiten explorar acciones, correcciones y fallos. Una cercanía semántica no demuestra causalidad ni verdad.
* **Contexto curado:** 319 registros canónicos permiten recuperar *handoffs* y decisiones con procedencia. El índice ayuda a encontrarlos, pero no reemplaza el registro original.
* **Proceso de investigación:** una proyección con 796 artefactos derivados y 533 vínculos permite inspeccionar la trayectoria de trabajo sin publicar documentos ni microdatos.
* **Correo personal:** el inventario local contiene 12.072 mensajes únicos entre 2011 y 2026. Sirve para probar lectura y deduplicación dentro de un ámbito autorizado; no constituye un corpus público ni un modelo de personalidad.
* **Memoria personal experimental:** un prototipo separado prueba recuperación mediante `mbox`, SQLite/FTS, ámbitos y purga. No existe todavía autorización para generar respuestas a partir de correo sensible.

Esta separación evita una tentación frecuente: confundir **tener acceso técnico a una fuente** con **estar autorizado a convertirla en memoria reutilizable**.

### Una falla útil

La propia tubería dio un ejemplo de por qué la procedencia importa. El exportador histórico esperaba un vector simple, mientras el índice actual almacenaba el vector nombrado `dense`. La primera regeneración produjo un grafo degradado, sin aristas semánticas. Una prueba contra el índice real detectó la incompatibilidad y, después de corregir el exportador, reaparecieron 3.658 aristas.

La lección es más importante que el número: **una visualización auditable debe poder mostrar cuándo su cadena de datos se degradó, por qué ocurrió y cómo se recompuso**. Es un caso de uso real.

### Del comando a la tarea

Las 1.432 estrategias registradas siguen siendo la unidad básica de esta memoria. Muchas nacieron como comandos, por lo que añadí una clasificación determinista para hacerlas más legibles: coordinar agentes (399), investigar y analizar (396), rastrear evidencia (385), ejecutar o automatizar (118), versionar cambios (76), verificar (28), operar infraestructura (18) y comunicar resultados (12).

Una estrategia podría pertenecer a varias categorías, pero hoy queda asignada a la primera regla coincidente. **Es una lente para recorrer la memoria, no una descripción de la persona detrás de ella.** Esto es muy mejorable con otras visualizaciones, si saben de alguna les agradezco el consejo.

---

## Segunda cucharada: gobernar fuentes antes de mezclarlas

La arquitectura parte de una separación sencilla. El **registro canónico** (*ledger*) y los archivos fuente conservan la evidencia; Qdrant mantiene índices que pueden destruirse y regenerarse; el visor publica una proyección saneada; y los adaptadores privados permanecen fuera de Git. El índice sirve para encontrar. No tiene autoridad para convertir, por sí solo, una coincidencia vectorial en un hecho durable.

### Una arquitectura de permisos, no una licuadora

Correo, tesis (del  magister) y memoria de trabajo pueden ser técnicamente legibles por el mismo sistema, pero eso no los vuelve intercambiables. En esta PoC, solo el contexto previamente curado puede alimentar la recuperación entre agentes y la proyección pública. El correo permanece en un circuito privado, reversible y vetable; la tesis aporta únicamente metadatos de proceso autorizados.

La distinción es importante: **tener acceso técnico a un dato no determina que sea legítimo reutilizarlo para cualquier propósito**. La teoría de la integridad contextual formula precisamente este problema: la privacidad depende no solo del dato, sino también del contexto, los actores y las normas que gobiernan su circulación [^nissenbaum-2004].

<figure class="align-center">

  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" target="_blank" rel="noopener">

```
<img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/fuentes-gobernadas.svg' | relative_url }}" alt="Tres fuentes gobernadas: la memoria de trabajo permite recuperación con procedencia; el correo personal permite solo revisión privada y reversible; tesis del magister y documentos permiten citas y estados de verificación. Con una barrera que impide publicar cuerpos de correo, adjuntos, direcciones, rutas absolutas, microdatos e inferencias de identidad." loading="lazy" decoding="async">
```

  </a>

  <figcaption>Figura 1. La integración actual es una arquitectura de permisos: cada fuente determina qué salidas están permitidas.</figcaption>

</figure>

La tesis ofrece un buen ejemplo. Lo que entra al sistema público es una [instantánea del índice de investigación]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}), no el corpus. El corte del 29 de agosto contiene 796 artefactos textuales derivados —316 auditorías, 244 reportes, 133 contratos, 71 pseudocódigos y 32 piezas de inventario, replicación o documentación—, además de 533 vínculos y 7 asuntos pendientes. Quedan fuera los documentos fuente, DTA, Parquet, PDF, imágenes, rutas, textos completos y microdatos. La búsqueda es deliberadamente léxica: FTS5 y TF-IDF ayudan a encontrar artefactos, pero no pretenden comprender la investigación.

Hay un detalle más interesante que las cifras. La instantánea publicada sigue siendo fiel al corte que declara: su huella coincide con el manifiesto de ese momento. Sin embargo, el corpus continuó creciendo y llegó a 817 documentos, veintiuno más. Como el índice no se regeneró, `check-research-index` devuelve `2`: `document_count` y `source_fingerprint` ya no coinciden con el estado actual.

Eso no invalida la instantánea; **la fecha**. Su estado correcto es "válida para el corte del 29 de agosto, pero no vigente respecto del corpus actual". Una compuerta que hubiese permanecido verde después de crecer el corpus habría sido peor que una compuerta fallida: habría certificado una actualidad inexistente. Esto da cuenta formal del crecimiento y divergencia potencial de la memoria.

{: .notice--warning}

### Reutilizar antes que reinventar

Nada de esto exige construir desde cero cada componente de memoria. De hecho, una buena señal de madurez sería poder **eliminar código propio** cuando una herramienta existente resuelva mejor el mismo problema sin deteriorar privacidad, procedencia o reversibilidad.

Para recuperar decisiones dispersas entre sesiones de programación, `deja-vu` ya indexa historiales locales de numerosos agentes y los expone mediante CLI y MCP. Es un candidato natural para contrastar con mis *handoffs* y eventos antes de desarrollar otra capa equivalente.

Para memoria persistente más estructurada existen aproximaciones más ambiciosas. MemGPT introdujo la idea de administrar distintos niveles de memoria como una forma de extender el contexto efectivo de un agente [^packer-2023]; la línea actual de Letta lleva ese principio a bloques de memoria editables y memoria externa. Mem0 automatiza la extracción, consolidación y recuperación de información de conversaciones [^chhikara-2025], mientras Hindsight distingue operaciones de **retener, recuperar y reflexionar**, incorporando recuperación semántica, léxica, temporal y mediante grafos [^latimer-2025].

El problema de la **vigencia** merece un experimento separado. Graphiti, componente abierto descrito en la arquitectura de Zep, modela explícitamente relaciones que cambian en el tiempo y conserva información histórica en lugar de reemplazarla silenciosamente [^rasmussen-2025]. Eso se aproxima mucho más al problema que intento resolver con `supersedes` que seguir agregando reglas temporales propias.

Para colecciones documentales, Microsoft GraphRAG ofrece otra idea útil: construir un grafo derivado del corpus y resumir comunidades para responder preguntas globales que un RAG convencional maneja peor [^edge-2024]. No lo usaría todavía como sustituto del índice de tesis. Primero tendría que demostrar, sobre un subconjunto científico acotado, que la complejidad y el costo adicional mejoran algo que la línea base léxica no puede resolver.

La visualización, finalmente, es un problema prácticamente resuelto: `3d-force-graph` ya proporciona un diseño tridimensional basado en Three.js y algoritmos de fuerzas. La parte relevante de esta PoC no es programar otro motor gráfico, sino controlar **qué grafo recibe el navegador** y recordar que una distancia visual no demuestra proximidad conceptual, causalidad ni afinidad humana.

La regla común es simple: **probar componentes, no coleccionarlos**. Que una biblioteca pueda recordar más no significa que deba recibir más datos.

Hay además un conflicto de interés que conviene explicitar. Mem0, Hindsight, Zep/Graphiti y Letta están descritos en buena medida por sus propios equipos. Sus artículos y repositorios son fuentes apropiadas para conocer las arquitecturas que proponen, pero sus resultados comparativos no constituyen validación independiente de superioridad. Aquí los uso como diseños que merecen contraste, no como ganadores de una competencia, como tampoco mi stac es superior. Es más, problablemente lo mío es más bien experimental para mis propósitos.

### Un experimento de recuperación que podía fallar

Probé `Qwen3-Embedding-0.6B` sobre una copia aislada de 319 contextos, sin tocar producción. La evaluación usó 40 consultas, ocho de ellas diseñadas para comprobar que el sistema también supiera **no recuperar evidencia cuando no correspondía**.

La mejor configuración obtuvo **38 casos completos, 2 parciales y ningún fallo total** entre las cinco primeras posiciones. A partir de ahí probé varias mejoras posibles:

* quitar el refuerzo léxico de BM25 mantuvo el mejor resultado;
* añadir una instrucción genérica al *embedding* empeoró la recuperación y la abstención;
* `Qwen3-Reranker-0.6B` ordenó algo mejor los resultados, pero aumentó demasiado el tiempo de respuesta;
* diversificar por repositorio y fusionar rankings tampoco resolvió los dos casos parciales.

El experimento dejó una conclusión más útil que encontrar un nuevo modelo: **los dos casos pendientes no parecen necesitar más potencia, sino mejores metadatos**. Ambos requieren recuperar documentos de familias diferentes dentro de solo cinco resultados.

Por eso, la siguiente prueba será incorporar información explícita sobre **linaje e intención documental**, sin utilizar las respuestas correctas para construir esas etiquetas. Aumentar arbitrariamente `k` o seguir agregando modelos solo habría desplazado el problema.

Mientras esos dos casos no se resuelvan de forma reproducible, la colección permanece en `staging`. En este sistema, **recordar que una mejora todavía no está demostrada también forma parte de la memoria**.

## Tercera cucharada: un mapa que no se hace pasar por una mente

Después de ordenar qué puede entrar a la memoria, queda otra pregunta: **¿cómo mostrarla sin confundir una representación con la realidad?**

El visor responde con una precaución, no consulta Qdrant (la base donde se indexan los vectores) ni fuentes privadas cuando alguien abre el sitio, **recibe un JSON saneado** (un archivo de datos del que se retiró información que no debe publicarse), generado desde un corte específico de la memoria.

Así, el gráfico puede reconstruirse y auditarse sin volver a tocar las fuentes originales. La [exportación pública en JSON]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) permite incluso inspeccionar directamente qué información recibe el navegador.

### Ver la red, sin atribuirle más de lo que dice

El corte del 29 de agosto contiene **1.432 estrategias, 3.949 relaciones y ocho tipos de tarea**, derivados de 16.955 puntos indexados.

La imagen siguiente **no es esa red**: es una ilustración, y el chiste es el porcentaje. La red de verdad se explora en el visor completo, que permite seleccionar tareas, proyectos y errores.

<figure class="align-center">

  <a href="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/cerebro-20-por-ciento-1600x1000.webp' | relative_url }}"
         alt="Ilustración: media silueta de un cerebro formada por puntos y aristas que se deshace hacia la derecha en puntos sueltos, con una barra de carga detenida en 20 %."
         loading="lazy"
         decoding="async">
  </a>

  <figcaption>
    Figura 2. Ilustración, no una proyección de los datos: la metáfora del clon digital cargada al 20 %. La red se insinúa donde hay densidad y se deshace donde no la hay, que es exactamente lo que sabe hacer un índice. La proyección real, con sus nodos y aristas, está en el visor.
  </figcaption>

</figure>

[**Abrir el visor interactivo en una pestaña nueva →**]({{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }})

{: .text-center}

Conviene leerlo con algunas precauciones. Un **nodo** (un punto del gráfico) representa una estrategia registrada. Una **arista** (una línea entre dos nodos) representa alguna relación derivada: por ejemplo, similitud semántica, una herramienta compartida o una corrección. Una **comunidad** (un grupo de nodos que aparece especialmente conectado) sirve para orientarse dentro de la red.

Ninguna de esas relaciones demuestra por sí sola causalidad, verdad o una característica de la persona que utilizó el sistema. El correo y los documentos privados tampoco aparecen como nodos de contenido.

Los números pertenecen, además, a un corte fechado. Actualizar la memoria no modifica silenciosamente el gráfico: hay que regenerar la proyección, sanearla y revisar sus diferencias antes de publicarla nuevamente.

**El visor no es la memoria. Es apenas un mapa construido desde una de sus proyecciones.**

### Recuperar una fuente tampoco basta

Encontrar el documento correcto es solo la mitad del problema. El sistema también debe **usar la fuente adecuada, respetar su ámbito y abstenerse cuando la evidencia no alcanza**.

Para probar esa capa construí `context-answer-v1`, un conjunto pequeño de 18 casos: 12 con evidencia suficiente y 6 en los que la respuesta correcta era no afirmar más de lo disponible. La prueba determinista pasó los 18 casos y confirmó que la compuerta funciona; todavía no demuestra que un modelo generativo responda bien por sí solo.

Las pruebas con modelos externos dejaron, además, una regla práctica. Solo deben evaluarse fuera de la máquina las fuentes autorizadas para salir de ella. El subconjunto exportable pasó 11/11 casos; otras siete fuentes permanecieron `local_only` y requieren una evaluación dentro del entorno local.

La conclusión es simple: **recuperar no basta; cada respuesta debe conservar procedencia, permisos y capacidad de abstención**. Hasta completar esa evaluación local y su revisión humana, puedo hablar de una memoria gobernada y atribuible, pero no todavía de una memoria generativa fiable.

---

## Cierre: una memoria útil antes que un clon digital

Falta aún para el "clon digital", hoy es un horizonte lejano. Al menos falta, como mínimo, una memoria temporal capaz de rectificarse, preferencias y límites revocables, evidencia de autoría, comportamiento evaluado en situaciones nuevas y control "humano" o superior sobre qué se conserva, comparte o elimina. MemGPT[^packer-2023] y los agentes generativos de Park et al.[^park-2023] ofrecen arquitecturas influyentes para manejar contexto, recuerdos, reflexión y planificación, pero no convierten esas funciones en identidad (Packer et al. 2023; Park et al. 2023).

En esta tercera parte `penta-agent` es un prototipo local de memoria gobernada: conserva experiencia, registra correcciones, expone una proyección pública limitada y permite que sus pruebas fallen sin alterar producción.

El próximo avance no consiste en añadir más nodos. Consiste en cerrar la evaluación local de respuestas y comparar alternativas —Graphiti, GraphRAG o `deja-vu`— bajo el mismo corte, los mismos permisos y criterios de salida observables. Quedo muy atento a sus comentarios y experiencias de uso, creo que me serviría algun punto de comparación práctico más que seguir probando las muchas herramientas que salen día a día.

---

## Referencias

### Lectura complementaria

Obras que orientaron el trabajo y que esta versión ya no cita en el cuerpo. Se
conservan porque perder el rastro de lo leído es peor que declararlo.

Cormack, Gordon V., Charles L. A. Clarke y Stefan Büttcher. 2009. «Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods». En *Proceedings of the 32nd Annual International ACM SIGIR Conference on Research and Development in Information Retrieval*, 758–59. Nueva York: Association for Computing Machinery. <https://doi.org/10.1145/1571941.1572114>.

Wu, Di, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang y Dong Yu. 2024. «LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory». arXiv, 14 de octubre de 2024; revisión del 4 de marzo de 2025. Trabajo aceptado en ICLR 2025. <https://arxiv.org/abs/2410.10813>.

Wu, Di, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng y Kai-Wei Chang. 2026. «LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues». Trabajo en curso, arXiv, 12 de mayo de 2026. <https://arxiv.org/abs/2605.06304>.

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

[^chhikara-2025]: Chhikara, Prateek, Dev Khant, Saket Aryan, Taranjeet Singh y Deshraj Yadav. 2025. «Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory». arXiv, 28 de abril de 2025. <https://arxiv.org/abs/2504.19413>.

[^edge-2024]: Edge, Darren, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness y Jonathan Larson. 2024. «From Local to Global: A GraphRAG Approach to Query-Focused Summarization». arXiv, 24 de abril de 2024; revisión del 19 de febrero de 2025. <https://arxiv.org/abs/2404.16130>.

[^hu-2025]: Hu, Yuyang, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu, Fangyi Zhu, Jiahang Lin et al. 2025. «Memory in the Age of AI Agents». arXiv, 15 de diciembre de 2025. <https://arxiv.org/abs/2512.13564>.

[^latimer-2025]: Latimer, Chris, Nicoló Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang y Naren Ramakrishnan. 2025. «Hindsight Is 20/20: Building Agent Memory That Retains, Recalls, and Reflects». arXiv, 16 de diciembre de 2025. <https://arxiv.org/abs/2512.12818>.

[^lebo-2013]: Lebo, Timothy, Satya Sahoo y Deborah McGuinness, eds. 2013. *PROV-O: The PROV Ontology*. Recomendación del W3C, 30 de abril de 2013. <https://www.w3.org/TR/prov-o/>.

[^nissenbaum-2004]: Nissenbaum, Helen. 2004. «Privacy as Contextual Integrity». *Washington Law Review* 79, n.º 1: 119–58. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/>.

[^packer-2023]: Packer, Charles, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica y Joseph E. Gonzalez. 2023. «MemGPT: Towards LLMs as Operating Systems». arXiv, 12 de octubre de 2023; revisión del 12 de febrero de 2024. <https://doi.org/10.48550/arXiv.2310.08560>.

[^park-2023]: Park, Joon Sung, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang y Michael S. Bernstein. 2023. «Generative Agents: Interactive Simulacra of Human Behavior». En *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, artículo 2, 1–22. Nueva York: Association for Computing Machinery. <https://doi.org/10.1145/3586183.3606763>.

[^rasmussen-2025]: Rasmussen, Preston, Pavlo Paliychuk, Travis Beauvais, Jack Ryan y Daniel Chalef. 2025. «Zep: A Temporal Knowledge Graph Architecture for Agent Memory». arXiv, 20 de enero de 2025. <https://arxiv.org/abs/2501.13956>.
