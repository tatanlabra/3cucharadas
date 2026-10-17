# Redline humano de los posts I y II

Estado: `APROBADO_Y_COMPROMETIDO_LOCALMENTE`

Fecha del candidato: 2026-10-17

Aprobación: 2026-10-17T19:02:03-03:00; autoriza dos commits locales coordinados,
su auditoría final y la limpieza de ambos repositorios. No autoriza push,
despliegue ni difusión.

## Custodia

| Superficie | Base | Estado del candidato |
|---|---|---|
| Blog | `043058e11010fd3b91da5650b083a689049d0456` | Línea UX de Claude integrada hasta `e22f4505150831adf25be60f6a7ae71a9c991d1b`; cambios editoriales y de cierre incluidos en el commit local que contiene este recibo |
| Investigación | `8b928c012e3e1ba9bebefaa96362d90f4ed346d7` | Freeze revisión 10 comprometido localmente en `88d97bfb99e54b5fae25f5becfd205c9535afc81` |
| Autoridad externa | — | Sin push, despliegue ni difusión |

## Post I

| Decisión | Resultado visible |
|---|---|
| Título | `Replicar mi tesis en 3 cucharadas (parte I): qué sobrevivió y qué corrigió la evidencia` |
| Relato | Tres cucharadas; distingue réplica, auditoría y extensión sin narrar la bitácora de construcción del post |
| Tabla inicial | Fusiona las antiguas tablas de auditoría y diferencias en una sola tabla de balance |
| Exclusiones | Retira la broma de notas de versión de IA, la tabla de nueve casos dudosos, nombres internos `do_058`–`do_060` y enlaces a fuentes D2 |
| Figuras | Conserva movilidad, concentración y sombra de muerte porque sostienen el argumento |
| Cierre | `Cierre: de replicar a extender`; enlaza el Post II en presente |
| Extensión | 3.427 palabras ES y 3.321 EN de texto renderizable más alternativas textuales; no cuenta etiquetas, atributos ni sintaxis Liquid |

## Post II

| Decisión | Resultado visible |
|---|---|
| Título | `Extender mi tesis en 3 cucharadas (parte II): lo que el recambio escolar todavía no permite concluir` |
| Pregunta | Abre con la continuidad educativa y separa trayectoria descriptiva de efecto causal |
| Resultados | Una tabla central de matrícula, SIMCE, IVE y comparabilidad; una segunda tabla de SLEP y SAE |
| Lenguaje | Reemplaza jerga operativa por `no estimable`; explica regresión a la media y límites de cobertura en lenguaje llano |
| Política pública | Integra Leyes 20.529 y 21.040, capacidad docente, oportunidades, fricciones y tensión laboral; reconoce la vía del artículo 31 y declara que su vigencia operativa, cronología y certificados no fueron verificados |
| Causalidad | Declara qué tendría que observarse para sostener efectos SLEP/SAE y por qué los diseños actuales no alcanzan |
| Exclusiones | Retira tabla de promesas, tabla de uso público, parámetros internos, 999 réplicas, 112 celdas y tolerancias de ejecución |
| Cierre | `Cierre: evaluar la transición, no celebrar el movimiento`; no anuncia una parte III |
| Extensión | 3.737 palabras ES y 3.670 EN de texto renderizable; no cuenta etiquetas, atributos ni sintaxis Liquid |

## Territorio y mapa

| Decisión | Resultado visible |
|---|---|
| Caso principal | Solo El Salvador; Lo Barnechea y Lo Prado salen del visor editorial |
| Escuela N.º 14 | Se distingue el punto oficial MINEDUC del candidato histórico OSM en avenida Diego Portales 500 |
| Estado epistémico | El candidato OSM es retrospectivo y no sustituye la coordenada oficial; el caso no reconstruye destinos individuales |
| Distancia | 1,272025 km para la línea del visor; la discrepancia entre el punto oficial y la sede histórica queda solo en el anexo de auditoría |
| Fusión | La línea representa la fusión documentada entre establecimientos, no el trayecto de estudiantes |
| Lámina estática | Sin enlace, imagen ni mención de fallback gráfico poco informativo |
| Atribución | Una sola atribución `© OpenStreetMap contributors`, compacta y dentro del mapa; no puede retirarse legalmente |
| Auditoría pública | GeoJSON y manifiesto acotados a RBD 391 y 390; la auditoría nacional agregada se conserva aparte |
| Contexto retirado | Se elimina del visor el desplegable demográfico/de resultados, sus figuras y tablas, porque no ayudaba a interpretar el caso único |

## Estilo, tablas y referencias

| Decisión | Resultado visible |
|---|---|
| Chicago | Reglas de Chicago-Deusto y Chicago 18 aplicadas a títulos, cuerpo, números, puntuación y transiciones; el inglés conserva deliberadamente ortografía británica en un registro institucional híbrido y la migración bibliográfica profunda sigue diferida |
| Tablas | HTML semántico nativo de Jekyll, encabezados con `scope`, letra mínima de 13 px y desplazamiento horizontal contenido en móvil |
| Referencias | Escala homogénea: 0,95 em en móvil, 0,90 em en escritorio y 1,6 de interlineado; enlaces visibles en temas claro y nocturno |
| Partes | Títulos normalizados como `(parte I)` y `(parte II)`; EN usa `(part I)` y `(part II)` |
| Voz | Se eliminan formulaciones de bitácora; se priorizan hallazgos, límites y utilidad pública |

## Integración UX de Claude

Se integró por fast-forward la línea UX de Claude hasta `e22f4505`, que incluye navegación, escala tipográfica, anatomía del post, portada, botones, fechas, tablas, alineación título–prosa, una sola región accesible por tabla, retiro de jQuery y `main.min.js`, versionado del buscador, tokens para ambos temas, contención falsable de la importación Sass y superficies temáticas para citas y avisos. La revisión humana ve ese estado combinado sin un commit nuevo de Codex.

La revisión par R13 de Claude emitió `REQUEST_CHANGES`. Se corrigieron sus dos bloqueantes —anexo EN y alcance de la Ley 20.529— y las derivas de commits, ubicación de distancias, anchos de prueba, URL del anexo, `<noscript>`, paridad de Tabla 1, leyenda EN y cautelas SLEP/SAE. R14 no encontró bloqueantes editoriales, jurídicos ni territoriales; detectó recibos obsoletos, conteo de marcado, 826 m todavía visibles y commits UX posteriores. El conteo y la ficha se corrigieron, la línea UX se integró y los recibos se regeneraron antes de abrir este redline. La precisión de seis decimales del visor se conserva porque fue una decisión explícita; el nombre público `-v1` del GeoJSON se mantiene por compatibilidad, aunque su `audit_id` sea v2.

## Contratos observados

| Gate | Rojo observado | Verde observado |
|---|---:|---:|
| Freeze científico | 2 sondas, exit 1 esperado | 29 pruebas, 13 sondas negativas y contrato, exit 0 |
| Cierre editorial | Caso territorial retirado reinyectado, exit 1 esperado | Cuatro posts y rangos, exit 0 |
| Separación territorial | Casos sistemáticos reinyectados, exit 1 esperado | Un caso, auditoría y atribución, exit 0 |
| UX visual | Overflow inyectado, exit 1 esperado | Post II 24/24; Post I 24/24; fallback 4/4; sin JS 2/2; enlaces profundos 2/2 |
| UX transversal | — | 32 pruebas, incluidas alineación título–párrafo, región única por tabla, retiro de jQuery, recursos versionados y tokens de tema, exit 0 |
| `agent-browser` | — | 320 y 1.440 px sin overflow; mapa `ready`, una atribución OSM, cero láminas estáticas, cero «826 m» y alineación título–párrafo de 0 px |
| Coordenadas | — | 8 pruebas, exit 0 |
| Mapa unitario | — | 4 pruebas, exit 0 |
| Build y artefacto | — | Jekyll y artefacto de 72.139.190 bytes con 1.552 entradas, exit 0 |
| Cierre local | Árbol del blog sucio, exit 1 esperado | Dos commits coordinados y ambos worktrees limpios, exit 0 |

## Riesgos y límites que permanecen

- La identidad byte a byte de visuales solo se garantiza entre corridas del mismo entorno fijado, no entre hosts distintos.
- El build emite advertencias de deprecación de `@import` de Sass; no afecta este candidato y su migración sería otro alcance.
- El health transversal conserva un fallo preexistente en `test_polyglot_doctor`: el fixture exige anclas GFM con tildes y el runtime local las translitera. No proviene del diff de los posts, pero debe reconciliarse antes de un push.
- El gate científico imprime ruido no fatal por `config/paths.local.toml`; las pruebas y el contrato terminan en exit 0.
- La URL productiva no se valida hasta que exista autorización separada para push y despliegue.
- `assets/dist/thesis_post2_map` está ignorado deliberadamente; CI ejecuta `npm run build:thesis-post2-map`, por lo que no se versiona un bundle derivado.
- El nombre `viewer-coordinate-audit-v1` se conserva para no romper enlaces públicos; el manifiesto declara `audit_id` v2 y su contenido actualizado.
- Los SVG territoriales retirados permanecen como assets sin enlace para evitar una eliminación no aprobada; ni los posts ni el visor los referencian.

## Preview local

- Post I ES: <http://127.0.0.1:4004/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/>
- Post I EN: <http://127.0.0.1:4004/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/>
- Post II ES: <http://127.0.0.1:4004/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/>
- Post II EN: <http://127.0.0.1:4004/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/>
- Auditoría: <http://127.0.0.1:4004/datos/educacion/auditoria-coordenadas-rbd/>

## Decisión requerida

La aprobación de este redline autoriza únicamente los dos commits locales coordinados y su auditoría final. No autoriza push, despliegue ni difusión.
