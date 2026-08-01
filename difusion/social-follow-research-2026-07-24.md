# Investigacion de cuentas para seguir: Mastodon y Bluesky

Fecha: 2026-07-24
Estado: investigacion local, sin acciones automaticas de seguimiento ni publicacion.

## Criterio

La busqueda se filtro por el perfil de 3 Cucharadas: IA aplicada, RAG/agentes, MLOps, software reproducible, datos/estadistica, economia aplicada, politicas publicas, datos abiertos y comunidad hispanohablante/LatAm.

Regla practica:

- Seguir: cuenta activa, tecnica o curatorial, con probabilidad de conversacion o descubrimiento util.
- Mencionar: cuenta relevante para una tecnologia usada, aunque publique poco.
- Vigilar: posible valor, pero baja actividad, cuenta personal muy amplia o señal aun debil.
- Descartar: homonimos, bots, bridges, RSS sin curacion, cuentas mudas o cuentas no verificadas.

## Evidencia revisada

- Busqueda web en Reddit/Hacker News y foros: la señal util fue metodologica, no una lista estable de handles. El consenso practico es usar Starter Packs/listas por interes, seguir por lotes pequenos y revisar actividad real.
- Bluesky: Starter Packs oficiales, Bluesky Directory, API publica `public.api.bsky.app`.
- Mastodon/Fediverse: Fedi.Directory, Fedi.Tips, busqueda publica desde `mastodon.social`, lookup directo en instancias federadas.
- Ledger local: ya quedaron seguidas `qdrant.bsky.social`, `mcp-community.bsky.social` y `huggingface@mas.to`.

Fuentes utiles:

- Bluesky Starter Packs: https://bsky.social/about/blog/06-26-2024-starter-packs
- Bluesky Directory: https://blueskydirectory.com/starter-packs
- Open Source + DevOps + AI pack: https://blueskydirectory.com/starter-packs/a/350428-open-source-devops-ai
- Fedi.Tips, discovery en Mastodon/Fediverse: https://fedi.tips/how-do-i-find-people-to-follow-on-mastodon-and-the-fediverse/
- Fedi.Directory: https://fedi.directory/
- Ask HN, cuentas en Bluesky para perfil Hacker News: https://news.ycombinator.com/item?id=42189890
- Reddit r/BlueskySocial, busquedas sobre starter packs y follows: https://www.reddit.com/r/BlueskySocial/search/?q=starter%20pack%20follow
- Reddit r/Mastodon, busquedas sobre discovery y hashtags: https://www.reddit.com/r/Mastodon/search/?q=follow%20hashtags

## Bluesky: seguir ahora

### IA aplicada, RAG, agentes, evaluacion y stack

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `simonwillison.net` | 48.412 seguidores, 4.742 posts | IA aplicada, LLMs, herramientas abiertas, datos y criterio tecnico sobrio. |
| `hamel.bsky.social` | 6.626 seguidores, 126 posts | Evals y validacion practica de sistemas LLM. Muy alineado con memoria/evaluador. |
| `langchain.bsky.social` | 2.170 seguidores, 212 posts | RAG, agentes y aplicaciones context-aware. Buena cuenta para seguir y eventualmente mencionar solo si aplica. |
| `llamaindex.bsky.social` | 1.173 seguidores, 1.061 posts | Agentes sobre documentos, RAG y document intelligence. Alta pertinencia. |
| `hf.co` | 16.593 seguidores, 3 posts | Hugging Face oficial, relevante para modelos/embeddings; baja actividad, pero buen follow institucional. |
| `qdrant.bsky.social` | 246 seguidores, 98 posts | Vector database usado en el stack. Ya seguido. |
| `mcp-community.bsky.social` | 112 seguidores, 430 posts | MCP y protocolo. Ya seguido. |
| `atproto.com` | 119.745 seguidores, 232 posts | Plataforma/protocolo de Bluesky; util para entender facets, embeds y difusion. |
| `github.com` | 70.116 seguidores, 470 posts | Dev platform y ecosistema open source. |
| `docker.com` | 1.285 seguidores, 877 posts | Infra reproducible, contenedores, MLOps local. |
| `vscode.dev` | 18.280 seguidores, 811 posts | Editor/dev tooling con foco en IA. |
| `ai2.bsky.social` | 4.753 seguidores, 1.009 posts | Open models, investigacion aplicada y evaluaciones. |
| `msftresearch.bsky.social` | 4.971 seguidores, 365 posts | Investigacion ML/IA con volumen moderado. |
| `technologyreview.com` | 27.851 seguidores, 1.197 posts | Cobertura tecnica de IA con audiencia amplia. |

### Personas IA/ML con buena senal

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `chiphuyen.bsky.social` | 6.006 seguidores, 14 posts | AI engineering y ML systems; baja frecuencia, alta pertinencia. |
| `eugeneyan.com` | 10.797 seguidores, 455 posts | ML aplicado, recomendaciones, engineering writing. |
| `vickiboykis.com` | 70.894 seguidores, 2.675 posts | Embeddings, sistemas, datos, escritura tecnica. Muy buena para cruces RAG-datos. |
| `rasbt.bsky.social` | 10.313 seguidores, 317 posts | LLMs, ML y material tecnico reproducible. |
| `thomwolf.bsky.social` | 12.597 seguidores, 122 posts | Hugging Face y open ML. |
| `natolambert.bsky.social` | 14.260 seguidores, 2.061 posts | LLMs, RLHF, open models, evaluacion social de IA. |
| `sashamtl.bsky.social` | 12.017 seguidores, 233 posts | IA responsable, clima e impacto social. |
| `merve.bsky.social` | 8.542 seguidores, 242 posts | Hugging Face, multimodalidad y VLMs. |
| `philschmid.bsky.social` | 2.876 seguidores, 75 posts | LLMs en Hugging Face y despliegue practico. |
| `randomwalker.bsky.social` | 23.627 seguidores, 159 posts | Critica informada de IA y riesgo de sobrepromesas. |
| `sayash.bsky.social` | 8.575 seguidores, 40 posts | Impacto social de IA y evaluacion critica. |
| `mmitchell.bsky.social` | 23.503 seguidores, 1.930 posts | Etica, gobernanza e impactos de IA. |
| `emollick.bsky.social` | 35.893 seguidores, 2.856 posts | IA en trabajo, educacion y adopcion. Alto impacto, mas generalista. |

### Datos, R/Python, reproducibilidad y visualizacion

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `posit.co` | 8.172 seguidores, 614 posts | RStudio/Posit, R, Python y ciencia de datos. |
| `python.org` | 11.415 seguidores, 355 posts | Python Software Foundation. |
| `realpython.com` | 2.192 seguidores, 3.966 posts | Python practico; buena frecuencia. |
| `pyopensci.org` | 2.251 seguidores, 176 posts | Python, open science y software cientifico. |
| `ropensci.org` | 246 seguidores, 8 posts | Reproducibilidad y datos abiertos; baja actividad, pero alta afinidad. |
| `observablehq.com` | 2.252 seguidores, 243 posts | Visualizacion y notebooks interactivos. |
| `datawrapper.de` | 3.867 seguidores, 443 posts | Graficos, mapas y tablas para comunicacion publica. |
| `plotly.com` | 1.694 seguidores, 435 posts | Visualizacion y apps de datos. |
| `datavizsociety.bsky.social` | 9.915 seguidores, 610 posts | Comunidad de visualizacion. |
| `ourworldindata.org` | 47.613 seguidores, 3.356 posts | Datos abiertos, evidencia y comunicacion publica. |

### Economia, causalidad, estadistica y politicas publicas

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `gmcd.bsky.social` | 5.188 seguidores, 744 posts | Economia y data science. Muy alineado con el perfil. |
| `nickchk.com` | 8.603 seguidores, 1.387 posts | Econometria causal, docencia y codigo. |
| `pedrosantanna.bsky.social` | 8.672 seguidores, 139 posts | Difference-in-differences y econometria. |
| `p-hunermund.com` | 23.886 seguidores, 7.157 posts | Economia empirica, data science y causalidad. |
| `paulgp.com` | 19.038 seguidores, 4.211 posts | Econometria aplicada. |
| `andrew.heiss.phd` | 19.124 seguidores, 5.459 posts | Public policy, causal inference, dataviz y R. |
| `vincentab.bsky.social` | 6.386 seguidores, 1.181 posts | R, ciencia politica y modelos aplicados. |
| `jmwooldridge.bsky.social` | 11.248 seguidores, 309 posts | Econometria. |
| `miguelhernan.org` | 8.432 seguidores, 36 posts | Inferencia causal; baja frecuencia, alto valor. |
| `lucystats.bsky.social` | 5.512 seguidores, 295 posts | Bioestadistica y metodos. |
| `maxkasy.bsky.social` | 5.855 seguidores, 189 posts | ML, politica, econometria e inequidad. |
| `claudia-sahm.bsky.social` | 54.435 seguidores, 747 posts | Macroeconomia aplicada, fiscal y Fed. |
| `jasonfurman.bsky.social` | 25.086 seguidores, 1.300 posts | Politica economica y macro. |
| `ernietedeschi.bsky.social` | 18.276 seguidores, 418 posts | Economia aplicada, medicion y politica publica. |
| `josephpolitano.bsky.social` | 111.946 seguidores, 10.413 posts | Newsletter de economia basada en datos. |
| `jburnmurdoch.ft.com` | 118.153 seguidores, 1.192 posts | Data journalism y visualizacion economica. |
| `andrewvandam.bsky.social` | 14.247 seguidores, 213 posts | Columnas de datos. |
| `brookings.edu` | 15.756 seguidores, 483 posts | Think tank de politicas publicas. |
| `nber.org` | 12.666 seguidores, 2.894 posts | Investigacion economica. |
| `appam.bsky.social` | 4.418 seguidores, 635 posts | Politica publica y administracion. |
| `urbaninstitute.bsky.social` | 11.967 seguidores, 643 posts | Datos y politicas publicas. |
| `voxeu.org` | 6.305 seguidores, 979 posts | Analisis economico CEPR. |
| `cepr.org` | 10.278 seguidores, 933 posts | Investigacion economica europea. |
| `epi.org` | 21.836 seguidores, 1.072 posts | Trabajo, economia laboral y politicas distributivas. |
| `rand.org` | 6.198 seguidores, 1.068 posts | Investigacion aplicada a politicas. |
| `centeronbudget.bsky.social` | 11.828 seguidores, 1.210 posts | Presupuesto, politica social y desigualdad. |

### Espanol, LatAm y Chile

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `monsoriu.bsky.social` | 201 seguidores, 142 posts | Pack "Uso practico de IA Generativa"; util para comunidad hispana IA. |
| `tallereconomico.bsky.social` | 54 seguidores, 35 posts | Economia y educacion economica en espanol; pequena pero pertinente. |
| `carranzajuanp.bsky.social` | 185 seguidores, 53 posts | Economia, estadistica y ciencia de datos aplicada. |
| `economiausp.bsky.social` | 1.250 seguidores, 90 posts | Economia academica LatAm/Brasil. |
| `elpais.com` | 165.500 seguidores, 38.193 posts | Alto alcance en espanol; seguir solo si quieres senal periodistica amplia. |

## Bluesky: mencionar o vigilar, no seguir como prioridad

| Cuenta | Estado | Motivo |
|---|---|---|
| `anthropic.com` | Dominio verificado, 15.726 seguidores, 0 posts | Relevante para Claude/MCP. Sirve para mencion puntual si corresponde, no aporta feed. |
| `continue.dev` | 195 seguidores, 0 posts | Proyecto relevante, pero sin actividad en la API publica. |
| `weaviate.bsky.social` | 117 seguidores, 54 posts | Relevante como vector DB, pero baja senal frente a Qdrant/LlamaIndex/LangChain. |
| `csail.mit.edu` | 5.365 seguidores, 15 posts | Institucional y prestigiosa, baja frecuencia. |
| `susanathey.bsky.social` | 11.667 seguidores, 10 posts | Alta autoridad academica, baja frecuencia. |
| `cdechaisemartin.bsky.social` | 6.186 seguidores, 119 posts | Muy pertinente para econometria; seguir si quieres reforzar causalidad. |
| `jondr44.bsky.social` | 3.047 seguidores, 28 posts | Econometria causal; baja frecuencia. |

## Bluesky: descartes observados

- `openai.com`, `openai.bsky.social`: no resolvieron como perfiles validos via API publica.
- `ollama.com`, `ollama.bsky.social`: no resolvieron como perfiles validos via API publica.
- `pinecone.bsky.social`: homonimo sin senal tecnica.
- `chroma.bsky.social`: homonimo no relacionado con vector DB.
- `lancedb.com`, `langfuse.com`, `arize.com`, `trychroma.com`, `worldbank.org`, `oecd.org`, `ciperchile.cl`, `ciperchile.bsky.social`: no resolvieron como perfiles validos via API publica en este barrido.

## Mastodon/Fediverse: seguir ahora

### Discovery y plataforma

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `@FediFollows@social.growyourown.services` | 76.607 seguidores, 4.824 posts, activo 2026-07-24 | Curacion manual de cuentas por categorias. Es el mejor follow para seguir descubriendo sin depender de buscadores. |
| `@FediTips@social.growyourown.services` | 235.595 seguidores, 8.485 posts, activo 2026-07-23 | Buenas practicas, busqueda, hashtags y funcionamiento del fediverso. |
| `@Mastodon@mastodon.social` | 875.709 seguidores, 551 posts, activo 2026-07-23 | Cuenta oficial de plataforma; seguir si quieres estar al dia de cambios. |

### IA, RAG, MLOps y software reproducible

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `@llamaindex@fosstodon.org` | 157 seguidores, 1.642 posts | Agentes/RAG sobre documentos; una de las pocas cuentas tecnicas activas en Fediverse para este nicho. |
| `@juliasilge@fosstodon.org` | 4.649 seguidores, 1.033 posts, activo 2026-07-13 | Data science, MLOps, R y texto. Alta afinidad. |
| `@ogrisel@sigmoid.social` | 2.282 seguidores, 445 posts | scikit-learn y ML engineering. |
| `@abi@masto.ai` | 1.982 seguidores, 253 posts | ML engineering y LLMOps; vigilar tono antes de interactuar. |
| `@reproducible_builds@fosstodon.org` | 1.288 seguidores, 315 posts, activo 2026-07-17 | Reproducibilidad de builds y supply chain. |
| `@realpython@fosstodon.org` | 2.100 seguidores, 1.384 posts, activo 2026-07-24 | Python practico, tutoriales y comunidad. |
| `@pythonbytes@fosstodon.org` | 3.408 seguidores, 253 posts, activo 2026-06-01 | Noticias de Python para devs. |
| `@pyOpenSci@fosstodon.org` | 1.275 seguidores, 681 posts, activo 2026-06-24 | Python open science. |
| `@scientific_python@fosstodon.org` | 439 seguidores, 13 posts, activo 2026-01-08 | Institucional del ecosistema Scientific Python; menos activo, pero canonico. |

### Datos, estadistica, R y open science

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `@R_Foundation@fosstodon.org` | 5.556 seguidores, 94 posts, activo 2026-06-26 | Cuenta oficial del proyecto R. |
| `@RConsortium@fosstodon.org` | 968 seguidores, 674 posts, activo 2026-07-21 | Ecosistema R, empresas y comunidad. |
| `@rOpenSci@hachyderm.io` | 2.990 seguidores, 1.348 posts, activo 2026-07-21 | Reproducibilidad, open data, software cientifico. |
| `@OpenRefine@fosstodon.org` | 650 seguidores, 125 posts, activo 2026-07-23 | Limpieza de datos reales. Muy alineado con trabajos tipo catastro/datos publicos. |
| `@Python4DataScience@mastodon.social` | 420 seguidores, 117 posts, activo 2026-07-24 | Material Python/data science. |
| `@freakonometrics@mastodon.social` | 7.698 seguidores, 8.726 posts, activo 2026-07-24 | Estadistica, economia y datos. |
| `@JASPStats@fosstodon.org` | 841 seguidores, 66 posts, activo 2026-06-17 | Estadistica aplicada y software abierto. |
| `@useR_conf@mastodon.social` | 802 seguidores, 102 posts, activo 2026-06-08 | Conferencia R; util por comunidad. |
| `@wikiresearch@mastodon.social` | 1.574 seguidores, 2.459 posts, activo 2026-07-17 | Investigacion Wikimedia/Wikidata; datos abiertos. |
| `@openstreetmap@en.osm.town` | 20.054 seguidores, 582 posts, activo 2026-07-14 | Datos geograficos abiertos, mapas y comunidad OSM. |

### Politicas publicas, gobierno digital y economia

| Cuenta | Evidencia API | Motivo |
|---|---:|---|
| `@CivicCoding@social.bund.de` | 671 seguidores, 1.212 posts, activo 2026-07-24 | IA para bien comun/gobierno; buen puente entre IA y sector publico. |
| `@civictech@mastodon.social` | 149 seguidores, 1.145 posts | Civic Tech Field Guide; bajo follower count, pero buena curacion tematica. |
| `@InseeFr@social.numerique.gouv.fr` | 1.444 seguidores, 1.457 posts, activo 2026-07-24 | Estadisticas oficiales, economia y sociedad. |
| `@JuanDGut@dair-community.social` | 938 seguidores, 96 posts | Politica publica, regulacion e IA; revisar timeline antes de seguir. |
| `@donmoyn@sciences.social` | 4.300 seguidores, 236 posts, ultimo post 2024-08-23 | Public policy; baja actividad reciente, mejor Bluesky si existe/si esta activo. |

## Mastodon/Fediverse: ya seguido o baja prioridad

| Cuenta | Estado | Motivo |
|---|---|---|
| `@huggingface@mas.to` | Ya seguida; 812 seguidores, 0 posts | Oficial/relevante, pero no aporta feed por ahora. Mantener para posible mencion. |
| `@SebRaschka@mastodon.social` | 2.354 seguidores, 224 posts, ultimo post 2025-03-03 | Alto valor tecnico, baja actividad reciente en Mastodon. Mejor seguir en Bluesky si se prioriza feed activo. |
| `@ChristophMolnar@sigmoid.social` | 790 seguidores, 34 posts, ultimo post 2023-09-08 | Interpretabilidad ML; valioso pero inactivo. |
| `@publicsectorai@sfba.social` | 59 seguidores, 4 posts | Tema muy alineado, cuenta muy chica/inactiva. Vigilar. |
| `@ciperchile@lile.cl` | 3.319 seguidores, 646 posts, ultimo post 2023-10-25 | Relevante para Chile/datos/periodismo, pero no activo. |

## Mastodon/Fediverse: descartes observados

- Qdrant, LangChain, OpenAI, Anthropic, Ollama, Pinecone, Chroma, LanceDB y RAG como terminos devolvieron principalmente homonimos, bots, comunidades Lemmy genericas o RSS bridges desde `mastodon.social`.
- `blog.langchain.dev@rss-parrot.net` existe como bridge RSS, pero no lo recomiendo para interaccion.
- Cuentas Flipboard/Threads con muchos seguidores fueron tratadas como ruido salvo que tengan curacion directamente relevante.

## Lotes recomendados

### Lote 1: impacto tecnico inmediato

Bluesky:

`simonwillison.net`, `hamel.bsky.social`, `langchain.bsky.social`, `llamaindex.bsky.social`, `hf.co`, `vickiboykis.com`, `eugeneyan.com`, `rasbt.bsky.social`, `ai2.bsky.social`, `posit.co`

Mastodon:

`@FediFollows@social.growyourown.services`, `@FediTips@social.growyourown.services`, `@llamaindex@fosstodon.org`, `@juliasilge@fosstodon.org`, `@R_Foundation@fosstodon.org`, `@RConsortium@fosstodon.org`, `@rOpenSci@hachyderm.io`, `@OpenRefine@fosstodon.org`, `@realpython@fosstodon.org`, `@reproducible_builds@fosstodon.org`

### Lote 2: economia, causalidad y politica publica

Bluesky:

`gmcd.bsky.social`, `nickchk.com`, `pedrosantanna.bsky.social`, `p-hunermund.com`, `paulgp.com`, `andrew.heiss.phd`, `vincentab.bsky.social`, `jmwooldridge.bsky.social`, `claudia-sahm.bsky.social`, `jasonfurman.bsky.social`, `josephpolitano.bsky.social`, `jburnmurdoch.ft.com`, `nber.org`, `brookings.edu`, `appam.bsky.social`, `urbaninstitute.bsky.social`, `voxeu.org`, `cepr.org`

Mastodon:

`@freakonometrics@mastodon.social`, `@InseeFr@social.numerique.gouv.fr`, `@CivicCoding@social.bund.de`, `@civictech@mastodon.social`, `@JuanDGut@dair-community.social`

### Lote 3: comunidad hispana/LatAm y visualizacion

Bluesky:

`monsoriu.bsky.social`, `tallereconomico.bsky.social`, `carranzajuanp.bsky.social`, `economiausp.bsky.social`, `datawrapper.de`, `observablehq.com`, `datavizsociety.bsky.social`, `ourworldindata.org`

Mastodon:

`@pyOpenSci@fosstodon.org`, `@Python4DataScience@mastodon.social`, `@wikiresearch@mastodon.social`, `@openstreetmap@en.osm.town`, `@useR_conf@mastodon.social`

## Hashtags recomendados por plataforma

### Bluesky

Usar 3 a 5, no todos:

`#RAG`, `#AIAgents`, `#MLOps`, `#LLMOps`, `#DataScience`, `#CausalInference`, `#Econometrics`, `#RStats`, `#OpenSource`, `#OpenData`, `#GovTech`, `#PublicPolicy`, `#Dataviz`

### Mastodon

Usar CamelCase y mantener 4 a 6 maximo:

`#RStats`, `#Python`, `#DataScience`, `#MachineLearning`, `#MLOps`, `#LLMOps`, `#CausalInference`, `#EconTwitter`, `#PublicPolicy`, `#OpenData`, `#OpenScience`, `#CivicTech`, `#IA`, `#InteligenciaArtificial`

## Reglas de mencion para difusion

- Maximo una mencion fuerte por post en Bluesky, salvo que dos tecnologias hayan sido usadas directamente.
- Mastodon: preferir hashtags; mencionar cuentas solo si son activas y directamente involucradas.
- No mencionar OpenAI/Ollama/Pinecone/Chroma en esta campana si no hay handle oficial verificado y activo.
- Para posts tecnicos de RAG/memoria: `@qdrant.bsky.social`, `@mcp-community.bsky.social`, `@langchain.bsky.social`, `@llamaindex.bsky.social` son los candidatos naturales, pero solo si el texto realmente habla de ellos.
- Para posts de evaluacion y calidad: `hamel.bsky.social`, `simonwillison.net`, `rasbt.bsky.social`, `randomwalker.bsky.social` son mejores como comunidad a seguir que como menciones directas.
- Para posts de datos/politica publica: priorizar `andrew.heiss.phd`, `gmcd.bsky.social`, `ourworldindata.org`, `appam.bsky.social`, `urbaninstitute.bsky.social`, `@CivicCoding@social.bund.de`.

## Rutina de crecimiento sugerida

1. Seguir 10 a 15 cuentas por lote, no todo de una vez.
2. Antes de publicar, revisar si alguna de esas cuentas posteo algo relacionado en las ultimas 2 semanas.
3. Responder 2 o 3 hilos tecnicos con comentarios concretos antes de publicar el post propio.
4. En Bluesky, revisar Starter Packs por `RAG`, `AI Engineering`, `Causal Inference`, `Data Science` y `Public Policy` cada mes.
5. En Mastodon, seguir hashtags de nicho y cuentas curatoriales primero; la busqueda textual es menos confiable por federacion.
