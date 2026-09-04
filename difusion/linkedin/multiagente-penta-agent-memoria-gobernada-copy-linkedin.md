**Multiagentes III: una memoria que deja huellas**

Tercera parte: la memoria ya recupera bien. El problema ahora es gobernarla.

Qué persiste, qué caduca y qué nunca debe salir de su ámbito.

En esta tercera bitácora de mi sistema multiagente el avance no es recuperar mejor, sino separar por contrato cuatro fuentes que la tentación pide fusionar: la memoria de trabajo curada, un piloto de correo personal que es privado y reversible, metadatos de proceso autorizados de un proyecto de tesis, y la proyección pública derivada de todo ello. La diferencia entre acceso técnico y flujo legítimo de información es justo lo que un buscador vectorial no distingue solo.

Probé cinco cambios de recuperación sobre una colección aislada de 319 contextos, con @Qdrant y Qwen3-Embedding-0.6B en CPU. Promoví uno: quitar la bonificación BM25 (38 completos, 2 parciales, 0 fallos; recall@5 0,9635; 8/8 negativos rechazados). Rechacé cuatro, y el más interesante es el reordenador: puntuaba mejor —MRR 0,9010— y la mediana de latencia subía de 2,37 a 15,83 segundos, con un peor caso de 91,10. Mejor no siempre es promovible.

Publico esto con una compuerta en rojo, a propósito. El índice de proceso que cito se construyó el 29 de agosto; desde entonces el corpus creció de 796 a 817 documentos y no se regeneró, así que `check-research-index` sale 2. La instantánea sigue siendo fiel a su fecha —su huella coincide byte a byte—, pero su vigencia caducó. Una compuerta que se hubiera quedado verde mientras el corpus crecía habría sido peor que no tenerla.

El post trae un visor 3D navegable de las estrategias registradas: 1.432 nodos, 3.949 relaciones, ocho tipos de trabajo. Es un mapa de trabajo registrado, no un modelo de una mente, y el texto insiste en la diferencia. Todavía no es un clon digital, y digo por qué con más detalle del que suele darse.

Me interesa leer otros criterios de gobernanza de memoria: qué dejan caducar, qué se niegan a publicar aunque técnicamente puedan, y cómo distinguen una memoria útil de una promesa de continuidad.

#RAG #AIAgents #KnowledgeGraph #ContextEngineering #MLOps


## Primer comentario

La bitácora completa, con el visor y las mediciones:

https://3cucharadas.cl/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/?utm_source=linkedin&utm_medium=social&utm_campaign=multiagente_memoria_gobernada

## Carrusel

6 láminas en `multiagente-penta-agent-memoria-gobernada-carrusel.pdf`. Subirlo como documento nativo de LinkedIn, no como imágenes sueltas: el formato documento se muestra como carrusel deslizable y mide vistas por lámina.

## Nota de publicación

Convertir manualmente `@Qdrant` en mención real con el typeahead de LinkedIn. Si no resuelve como entidad, dejar `Qdrant` en texto plano.

No mencionar a Alibaba/Qwen como entidad: el modelo se cita por nombre técnico, no como marca asociada al post.
