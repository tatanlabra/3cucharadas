# Plan de mejora, auditoría geográfica y prepublicación del Post II

## Handoff a Claude Code

| Campo | Valor |
|---|---|
| Origen | Codex, integrador de planificación |
| Destino | Claude Code, integrador de ejecución |
| Vía | Archivo Markdown local + `PLAN_STATE v2` |
| Timestamp | `2026-10-11T16:47:22-03:00` |
| Plan vivo | `PLAN_STATE.yml` en este mismo directorio |
| Estado documental | Plan aceptado para ejecución; implementación aún no iniciada |
| Acciones externas | Sin commit, push, despliegue, difusión ni publicación |

`HANDOFF-TRACE: usuario → Codex integrador, planificación → Claude Code integrador, ejecución mediante plan-board → Claude par, revisión R3 sobre hashes finales → humano H1`

### Decisiones inmutables

- Reemplazar íntegramente el Post II actual por la nueva narración.
- Mantener R-007 como bloqueo del artículo, no del blog.
- Usar el título ES “Extender mi tesis en 3 cucharadas II: ¿mejora la educación cuando abren y cierran escuelas?”.
- Auditar nacionalmente los establecimientos activos del Directorio oficial más reciente, todas las dependencias.
- Presentar la auditoría MINEDUC–OSM como recuadro breve más anexo técnico bilingüe.
- Tratar OSM, Wikidata y Wikipedia como fuentes secundarias, nunca como ground truth automático.
- Registrar toda investigación pendiente de los `PLACEHOLDER` como tarea emergente del ToDo dinámico.
- Preservar ES/EN, procedencia, fuentes canónicas y cambios concurrentes del worktree.
- Mantener bloqueadas todas las acciones externas hasta una autorización separada.

### Tarea para Claude Code

- Importar este documento al `plan-board` y congelar su línea base antes de editar.
- Ejecutar fase por fase, conservando causas, dependencias, verificaciones y bloqueos en `PLAN_STATE v2`.
- Usar `penta-agent` como fuente de verdad para routing, handoffs, gates y ejecución remota.
- No marcar un gate como aprobado hasta observar su canary rojo pertinente y el posterior verde.
- Mantener bajo custodia briefings y respuestas originales del par.

## 1. Estado, decisiones y límites

| Campo `PLAN_STATE v2` | Estado |
|---|---|
| Plan | `thesis-post2-closeout-20261011`, revisión objetivo 8 |
| Objetivo | Reemplazar el Post II y agregar una auditoría nacional MINEDUC–OSM como producto secundario |
| Cobertura elegida | Todos los establecimientos activos del Directorio oficial más reciente, todas las dependencias |
| Producto elegido | Recuadro breve en Post II más anexo técnico bilingüe y reproducible |
| Narrativa | Reemplazo completo por el nuevo borrador, subordinado a la evidencia congelada |
| Novedad | Excluida del blog; R-007 seguirá abierto únicamente para el artículo |
| Título ES | “Extender mi tesis en 3 cucharadas II: ¿mejora la educación cuando abren y cierran escuelas?” |
| Autoría de archivos | Un escritor por archivo y fase; Claude Code integra la ejecución |
| Revisión par | Claude en revisión adversarial R3 después de fijar hashes |
| Acciones externas | Sin commit, push, despliegue, difusión ni publicación |
| Bloqueo operativo | `/mnt/nas05` en `stata08` fue observado al 99 %, con 64 GB libres |
| Estado general | Ejecución editorial posible; auditoría remota bloqueada hasta aprobar el preflight |

- El portal MINEDUC actualmente ofrece directorios desde 1992 y muestra 2025 como el más reciente; se revalidará fecha, esquema y hash al ejecutar: <https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/>.
- La auditoría nacional no reemplazará la auditoría SLEP 2025 existente: la extenderá sin modificar retrospectivamente su contrato.
- La disponibilidad actual de 29 faltantes entre 5.131 escuelas públicas SLEP no permite inferir la brecha nacional.
- La ejecución OSM no comenzará mientras el NFS siga sobre 90 %.
- La alternativa predeterminada será esperar capacidad; un scratch distinto del NFS requerirá espacio verificado y autorización explícita.
- No se escaneará `/`, no se ejecutarán búsquedas amplias y no se consultará masivamente la instancia pública de Nominatim.

## 2. Arquitectura editorial y epistémica

### Relato principal

- La primera pantalla dirá que los datos no identifican el efecto causal de abrir o cerrar escuelas.
- La tabla inicial responderá desempeño, regla conjunta, rol institucional y alcance territorial.
- La expresión pública será “330 casos retenidos bajo la definición estricta” en la primera mención.
- “La respuesta corta es no” se sustituirá por “la regla schumpeteriana conjunta no encuentra respaldo”.
- El texto conservará los tres movimientos: cambios observados, desempeño y límites, territorio y agenda del Post III.
- El recuadro geográfico aparecerá dentro del movimiento territorial y no modificará la tesis central.
- El recuadro tendrá como máximo 300 palabras, una tabla compacta y un enlace al anexo.
- Título del recuadro ES: **“Auditar el punto antes de medir la distancia”**.
- Título del recuadro EN: **“Audit the point before measuring distance”**.
- No se añadirá un mapa nacional interactivo al Post II.

### Jerarquía de evidencia geográfica

| Categoría | Significado permitido | Lenguaje prohibido |
|---|---|---|
| `HECHO_OBSERVADO` | Valor presente en un snapshot identificado de MINEDUC u OSM | “Ubicación verdadera” |
| `COORDENADA_OFICIAL_INVALIDA` | Vacía, cero, no numérica o fuera de límites plausibles de Chile | “OSM corrigió MINEDUC” |
| `CANDIDATO_DE_DISCREPANCIA` | Una regla reproducible detecta diferencia que requiere revisión | “Error confirmado” |
| `DISCREPANCIA_CORROBORADA` | Coinciden RBD explícito, evidencia espacial y una segunda fuente fechada | “Fraude” o intención institucional |
| `ERROR_OFICIAL_CONFIRMADO` | MINEDUC corrige el registro o una fuente institucional autoritativa acredita el punto correcto | Confirmación basada solo en OSM |
| `NO_RESUELTO` | Las fuentes discrepan o no permiten identificar el establecimiento | Imputación automática |

- OSM, Wikidata y Wikipedia serán evidencia secundaria, no ground truth.
- La ausencia de una escuela en OSM no demostrará que la coordenada MINEDUC sea correcta.
- Un punto OSM podrá representar acceso, edificio, campus o centroide de un polígono.
- Dos RBD en el mismo punto podrán representar un campus compartido y no se marcarán automáticamente como error.
- Las etiquetas `source=*` se usarán para identificar posible dependencia entre OSM y MINEDUC.
- Una coordenada histórica distinta podrá reflejar traslado, fusión o cambio de sede, no necesariamente un error.

## 3. Auditoría nacional MINEDUC–OSM

### Universo y alcance temporal

- El universo principal será cada RBD activo del directorio oficial más reciente disponible y validado al ejecutar.
- Se incluirán todas las dependencias y regiones.
- Los códigos de estado activo se confirmarán contra el diccionario de la versión seleccionada.
- El análisis histórico 2014–último año se limitará a RBD actuales marcados y a los casos usados en Post II.
- No se auditarán exhaustivamente todos los RBD cerrados históricos dentro de este producto.
- La unidad primaria será `RBD × año del directorio`.
- El resultado público distinguirá establecimientos, filas anuales, candidatos OSM y casos adjudicados.

### Preflight remoto obligatorio

1. Ejecutar únicamente mediante `penta-agent/scripts/remote_exec.sh`.
2. Comprobar conectividad, `/proc/pressure/io`, espacio del filesystem objetivo y salud de Nominatim.
3. Bloquear si el filesystem de salida supera 90 % o si la presión de E/S indica carga sostenida riesgosa.
4. Registrar fecha de indexación y versión de la base OSM.
5. Inventariar mediante conteos acotados las tablas, geometrías y etiquetas educacionales disponibles.
6. Preferir una vista o exportación OSM de solo lectura ya existente.
7. Usar SQL acotado sobre la base local únicamente si existe acceso de solo lectura documentado.
8. Si solo existe la API HTTP de Nominatim, usarla únicamente sobre casos oficiales ya marcados.
9. Si no existe superficie apta para extracción nacional, declarar E-22 bloqueada y no simular cobertura OSM completa.
10. Conservar logs, comandos, códigos de salida, timestamps y hashes sin mostrar IP, credenciales ni configuración sensible.

### Extracción OSM

- Retener nodos, vías o relaciones con señal educacional en `amenity`, `building` o etiquetas equivalentes.
- Incluir `school`, `kindergarten` y `college`, preservando el tipo original para evitar equivalencias falsas.
- Retener `osm_type`, `osm_id`, geometría, `name`, `official_name`, `alt_name`, `operator`, dirección, referencias, `wikidata`, `wikipedia`, `source` y fecha disponible.
- Calcular `ST_PointOnSurface` para polígonos y conservar el tipo geométrico original.
- No copiar el dump OSM completo al repositorio.
- Guardar el snapshot privado fuera de Git con fecha, conteos y SHA-256.
- Sincronizar únicamente el extracto mínimo mediante el patrón canónico de `rsync` y verificar su manifiesto.

### Matching reproducible

| Nivel | Regla | Uso |
|---|---|---|
| A | Referencia OSM que identifica explícitamente el mismo RBD | Candidato de mayor confianza |
| B | Nombre normalizado exacto, misma comuna y candidato único | Candidato fuerte, no confirmación |
| C | Similitud de nombre ≥0,90, misma comuna y coincidencia de tipo o dirección | Revisión manual obligatoria |
| D | Solo cercanía espacial | Nunca produce match por sí sola |

- Se reutilizará la normalización de nombres del registro de identidad escolar.
- Se examinará empíricamente qué etiquetas OSM contienen RBD antes de fijar sus alias.
- Wikidata o Wikipedia sin coincidencia nominal y territorial no elevarán la confianza.
- Los empates conservarán todos los candidatos y el estado `AMBIGUOUS_MATCH`.
- Ningún match modificará las coordenadas oficiales ni las geometrías principales.
- El matching no usará matrícula, SIMCE, admisión ni otro resultado educativo.

### Señales de calidad geográfica

| Señal | Regla de auditoría | Interpretación |
|---|---|---|
| Faltante | Coordenada vacía, cero, no numérica o fuera de Chile | Brecha oficial verificable |
| Comuna | Punto fuera del polígono comunal; sensibilidad con buffer de 250 m | Posible comuna o coordenada errada |
| Duplicado | RBD distintos separados ≤10 m | Revisión de campus compartido o copia |
| Salto temporal | Mismo RBD cambia ≥1 km entre directorios consecutivos | Posible traslado, corrección o error |
| Divergencia OSM | Match A/B con distancia MINEDUC–OSM | Diferencia entre fuentes, no error confirmado |
| Ausencia OSM | No existe candidato A–C | Falta de contraste, no validación oficial |

- Las divergencias se reportarán acumulativamente a 100 m, 250 m, 500 m, 1 km, 2 km y 5 km.
- El corte primario de priorización será 1 km, pero se publicará la sensibilidad completa.
- Toda coordenada oficial faltante con match A será candidata prioritaria.
- Todo match A sobre 1 km será revisado manualmente.
- Todo caso usado en Post II será revisado sin importar la distancia.
- La revisión conservará una categoría explícita para campus grandes y accesos versus centroides.
- La precisión del matching se evaluará en una muestra estratificada con semilla `20261011`.
- La muestra incluirá matches A compatibles, matches A divergentes, matches B/C y duplicados.
- La revisión manual no convertirá automáticamente una fuente web corriente en evidencia histórica.

### Outputs

| Superficie | Contenido | Custodia |
|---|---|---|
| Parquet privado | Cruce completo MINEDUC–OSM, candidatos y distancias | Fuera de Git |
| JSON de auditoría | Conteos, reglas, hashes, estados y limitaciones | Repositorio de investigación |
| Informe Markdown | Método, resultados, falsación y adjudicación | Repositorio de investigación |
| Resumen público JSON | Conteos agregados por región, señal y confianza | Blog |
| Anexo ES/EN | Metodología, resultados y casos corroborados | Jekyll |
| CSV candidato | Solo si supera privacidad y licencia | Blog o exclusión documentada |

- El anexo tendrá los permalinks `/datos/educacion/auditoria-coordenadas-rbd/` y `/en/data/education/rbd-coordinate-audit/`.
- El anexo presentará conteos agregados, distribución de distancias y una tabla acotada de casos adjudicados.
- El listado completo combinado MINEDUC–OSM no se publicará hasta resolver compatibilidad de licencias.
- El raw oficial seguirá limitado a la lista blanca institucional: RBD, nombre, comuna, año, estado, coordenadas y dirección solo cuando sea necesaria.
- Se excluirán MRUN, RUT de sostenedor, identificadores personales y campos ajenos a la finalidad.

### Licencia y atribución

- Toda superficie pública que use OSM mostrará “© OpenStreetMap contributors” y un enlace visible a la ODbL.
- Los metadatos de cualquier base o archivo derivado incluirán origen y licencia OSM.
- Referencia oficial: <https://osmfoundation.org/wiki/Attribution_Guidelines>.
- Referencia ODbL: <https://www.openstreetmap.org/copyright/en>.
- El portal MINEDUC observado no declara una licencia de redistribución junto a los archivos; esta ausencia seguirá tratándose como riesgo, no como permiso.
- Si el gate jurídico no acredita compatibilidad, se publicarán solo agregados, figuras y una tabla pequeña de casos adjudicados con enlaces a las fuentes.
- No se enviarán correcciones a OSM, Wikidata ni MINEDUC como parte del plan.

## 4. Registro exhaustivo de `PLACEHOLDER` y ToDo dinámico

### Contrato nuevo de trazabilidad

`PLAN_STATE.yml` incorporará `placeholder_registry` con estos campos:

- `id`
- `target_status`
- `requires_additional_research`
- `emergent_task_id`
- `publication_blocking`
- `evidence_paths`
- `claim_action`
- `unblock_condition`

El verificador fallará si:

- falta alguno de PH-01 a PH-18;
- un PH requiere investigación y no tiene tarea emergente;
- una tarea figura `done` sin evidencia;
- un PH bloqueante permanece abierto al llegar a H1;
- un PH no bloqueante conserva en el post el claim que motivó su investigación;
- aparece `PLACEHOLDER`, `PH-*` o una nota editorial en el artefacto público.

### Estado objetivo de los 18 marcadores

| PH | Estado objetivo | Tratamiento |
|---|---|---|
| PH-01 | `CORREGIDO` | Conciliar transiciones 2015–2025 y El Salvador 2013/2014 |
| PH-02 | `LIMITACION_DOCUMENTADA` | Mantener candidatos de identidad sin confirmación automática |
| PH-03 | `LIMITACION_DOCUMENTADA` | No atribuir causalmente aperturas o cierres a SLEP |
| PH-04 | `VERIFICADO` | Mantener 665, 76, 188 y 47 con denominadores separados |
| PH-05 | `LIMITACION_DOCUMENTADA` | Mostrar embudos sin afirmar representatividad |
| PH-06 | `LIMITACION_DOCUMENTADA` | Tratar 10 como umbral retrospectivo y mostrar sensibilidad |
| PH-07 | `VERIFICADO` | MR2 no estimable; retirar puntos subsoportados |
| PH-08 | `CORREGIDO` | Corregir signos e intervalos MR3 en freeze revisión 5 |
| PH-09 | `LIMITACION_DOCUMENTADA` | Literatura contextual sin claim de novedad |
| PH-10 | `LIMITACION_DOCUMENTADA` | Fechar marco institucional y evitar atribución retroactiva |
| PH-11 | `CORREGIDO` | Completar auditoría nacional MINEDUC–OSM antes de H1 |
| PH-12 | `LIMITACION_DOCUMENTADA` | Hacer visible censura derecha y selección de ejemplos |
| PH-13 | `VERIFICADO` | Mantener nombres, RBD, años, distancias y roles comprobados |
| PH-14 | `LIMITACION_DOCUMENTADA` | No afirmar motivo administrativo ni destinos individuales |
| PH-15 | `VERIFICADO` | Mantener 55,7 % como proyección poblacional de 6–17 años |
| PH-16 | `DEFERIDO_POST_III` | Registrar escenarios demográficos y capacidad como agenda |
| PH-17 | `VERIFICADO` | Mantener ejecución, 999 réplicas, 112 celdas y residual |
| PH-18 | `CORREGIDO` | Obtener declaraciones autorales antes de H1 |

### Nuevas tareas emergentes

| ID | Fuente | Tarea | ¿Bloquea Post II? |
|---|---|---|---|
| E-21 | Usuario + infraestructura | Resolver capacidad de `stata08`, inventariar snapshot OSM y acreditar lectura segura | Sí, bloquea E-22 |
| E-22 | PH-11 | Construir auditoría nacional vigente e historia acotada de los RBD marcados | Sí |
| E-23 | PH-11 + licencia | Resolver la superficie pública compatible con ODbL y situación MINEDUC | Sí para CSV completo; no para agregados |
| E-24 | PH-02 | Evaluar 16 exclusiones y cuatro posibles reemplazos administrativos | No si el claim sigue acotado |
| E-25 | PH-03 | Evaluar diseños y datos adicionales para rol SLEP | No; queda en carril académico |
| E-26 | PH-05 | Medir composición y selección entre universo amplio y depurado | No si no se afirma representatividad |
| E-27 | PH-06 | Completar sensibilidad de soporte y reglas 5/10/20 | No si el texto conserva el límite |
| E-28 | PH-09 | Completar R-007, textos íntegros y revisión independiente de novedad | No para blog; sí para artículo |
| E-29 | PH-10 | Completar crosswalk normativo por año y traspaso | No si la redacción usa solo hechos fechados |
| E-30 | PH-12 | Profundizar ventanas, censura y estabilidad de la selección de casos | No si se divulga la cobertura vigente |
| E-31 | PH-14 | Buscar acto administrativo, motivo y destinos individuales de El Salvador | No si esos claims permanecen retirados |
| E-32 | PH-16 | Diseñar Post III sobre demografía, capacidad y accesibilidad | No; diferida |
| E-33 | PH-17 | Completar sensibilidades reproducibles pendientes | No para el alcance descriptivo actual |
| E-34 | PH-18 | Recabar financiamiento, vínculos, uso de IA y aprobación autoral | Sí, bloquea H1 |

- Una tarea no bloqueante podrá seguir abierta únicamente si el claim correspondiente fue retirado o degradado.
- Una tarea diferida necesitará condición de desbloqueo y destino explícito.
- Ningún ToDo podrá desaparecer porque el texto público omita su `PLACEHOLDER`.
- Las tareas nuevas surgidas durante investigación deberán registrar `cause`, fuente, impacto, aceptación y autoridad.
- El estado global no podrá declararse completo mientras existan tareas emergentes bloqueantes.

## 5. Cambios editoriales, estadísticos y de gobernanza

### Evidencia estadística pública

- MR1 SIMCE: `+0,029`, IC `[-0,095; +0,158]`, `n=21`, sin lectura causal.
- El punto MR1 de admisión se retirará porque el resultado es `NOT_ESTIMABLE`.
- Ningún punto MR2 subsoportado aparecerá en el post.
- MR3 admisión: `+0,00011268`, IC `[+0,00002717; +0,00021294]`.
- MR3 SIMCE: `−0,00010523`, IC `[−0,00034624; +0,00010268]`.
- RBD 390 seguirá descrito como receptor de fusión, no como apertura.
- Rancagua seguirá identificado como caso sin puntajes observados.
- El Salvador seguirá fuera de la muestra sistemática.
- La proyección de 55,7 % no se traducirá en cierres, matrícula ni recomendación de política.

### Custodia editorial

- Preservar bytes, hashes y patch selectivo de los posts ES/EN actuales antes de reemplazarlos.
- Archivar el nuevo borrador como candidato de fuente con su hash original.
- Observar primero el gate rojo por identidad duplicada entre `_drafts` y `_posts`.
- Retirar la copia conflictiva de `_drafts` solo después de registrar ese rojo.
- Mantener una fuente canónica ES y una EN con el mismo `ref`, permalink, fecha y visuales.
- Omitir `published: false` para QA equivalente a producción.
- Mantener `distribution.social: false`.
- No usar `git reset`, `git restore` ni limpiar cambios ajenos.

### Programa de liberación

- Elevar el contrato del Post II a revisión 10.
- Mantener F8 como revisión pública/adversarial sin bloqueo R-007.
- Trasladar `BLK-R007` a `TASK-F10-ARTICLE-FINAL`.
- Mantener F9 como freeze público dependiente de F8.
- Hacer depender F12 de `[F9, F11]`, no de F10.
- Marcar `TASK-F12-POST1` como `superseded` bajo `DEC-REL-002`.
- Registrar `DEC-REL-005` con reemplazo completo, desacople R-007 y título amplio.
- Registrar `DEC-REL-006` con cobertura nacional y producto recuadro más anexo.
- Resolver `BLK-POST2-CONTRACT` solo con contrato, freeze, auditoría geográfica y hashes vigentes.
- Resolver D-14 únicamente después de `make release-validate` y `make release-status`.
- Mantener `DRIFT-002` abierto como deuda global diferente.
- Incorporar al freeze revisión 5 el hash y los conteos aceptados de la auditoría geográfica.

## 6. Pruebas y falsación

| Gate | Rojo obligatorio | Verde exigido |
|---|---|---|
| Capacidad remota | Filesystem de salida >90 % | Uso ≤90 % y presión de E/S aceptable |
| Snapshot OSM | Falta fecha, versión, hash o licencia | Manifest completo y reproducible |
| Privacidad | Exportación contiene RUT, MRUN o campos fuera de lista blanca | Solo campos institucionales autorizados |
| Matching A | Referencia RBD equivocada enlaza dos entidades | Correspondencia exacta y única |
| Matching B/C | Nombre aproximado se confirma automáticamente | Estado de revisión sin imputación |
| Empate | Dos candidatos se reducen arbitrariamente a uno | `AMBIGUOUS_MATCH` conserva alternativas |
| Fuente dependiente | OSM con fuente MINEDUC se trata como corroboración independiente | Riesgo de fuente compartida visible |
| Comuna | Punto cercano al borde falla por tolerancia | Sensibilidad con buffer de 250 m |
| Duplicados | Campus compartido se etiqueta como error | Estado candidato hasta adjudicación |
| Temporalidad | Salto de coordenada se interpreta como error | Se consideran traslado, fusión y corrección |
| Distancia | Solo se publica el corte de 1 km | Conteos a 100/250/500 m y 1/2/5 km |
| OSM ausente | Ausencia se interpreta como validación MINEDUC | Estado `NO_OSM_CANDIDATE` |
| Licencia | CSV combinado se publica sin aviso ODbL | Atribución y gate de compatibilidad |
| Registro PH | Un PH investigable carece de tarea emergente | PH-01–PH-18 trazados y adjudicados |
| Higiene | Sobrevive `PLACEHOLDER`, `PH-*` o nota interna | Ningún marcador en artefactos públicos |
| Duplicidad Jekyll | Coexisten fuentes con `(lang, ref, permalink)` iguales | Exactamente una fuente canónica por idioma |
| Límite causal | Título amplio sin advertencia inicial | Frontera causal visible en primera pantalla |
| Novedad | “Primer estudio” o equivalente | Cero claims públicos de novedad |
| Estimabilidad | Se publica un punto no estimable | Solo resultados admisibles |
| Freeze | SRF-006 usa signos o intervalos incorrectos | Freeze revisión 5 consistente |
| Routing R-007 | R-007 vuelve a bloquear F8/F12 | R-007 bloquea solo artículo |
| Paridad | Cambia cifra, signo o límite entre idiomas | Equivalencia numérica y epistémica |
| Build | Jekyll o Vite falla en destino limpio | Códigos independientes 0 |
| Artefacto | Falta post, anexo, visual o `/en/` | Ambos idiomas y recursos completos |
| Visual | Overflow, salto o fallback roto | 360–1.920 px, claro/oscuro, sin regresiones |
| Accesibilidad | Axe encuentra violación o inconcluso no adjudicado | Cero violaciones e inconclusos |
| Revisión R3 | El par recibe un briefing sin hashes finales | Hallazgos adjudicados y gates repetidos |
| H1 | Falta financiamiento, vínculos, IA o aprobación bilingüe | Aprobación humana sobre preview coincidente |
| EXT | Intento de commit, push, deploy o difusión | Permanece bloqueado sin autoridad nueva |

### Pruebas unitarias mínimas de la auditoría

- Coordenada vacía y cero se clasifican como faltantes.
- Latitud y longitud invertidas no pasan como coordenada válida.
- Un punto fuera de Chile falla cerrado.
- Un punto dentro del buffer comunal no produce falso positivo duro.
- Dos RBD co-localizados no se confirman como error.
- Un match RBD explícito prevalece sobre similitud nominal.
- Un match difuso nunca imputa coordenada.
- Un empate preserva todos los candidatos.
- Un salto histórico conserva las hipótesis de traslado y corrección.
- Un objeto OSM de polígono usa `PointOnSurface`.
- Las distancias se calculan geodésicamente.
- El extracto público omite campos personales.
- El resumen público reconcilia exactamente con el audit JSON.
- El código falla si falta atribución OSM.
- El código falla si se intenta sobrescribir coordenadas MINEDUC.

## 7. Secuencia de ejecución

- [ ] F0 — Crear recibo de custodia del working tree y materializar el estado actualizado del plan.
- [ ] F1 — Añadir `placeholder_registry`, E-21–E-34 y `DEC-REL-005/006`.
- [ ] F2 — Implementar pruebas unitarias y canaries de la auditoría antes del extractor real.
- [ ] F3 — Repetir el preflight de `stata08`; mantener E-21 bloqueada si el NFS continúa sobre 90 %.
- [ ] F4 — Inventariar la superficie OSM y congelar su contrato de extracción.
- [ ] F5 — Construir el extracto privado, el matching y la adjudicación.
- [ ] F6 — Emitir informe, audit JSON y resumen público; aplicar el gate de licencia al CSV.
- [ ] F7 — Corregir PH-11 e incorporar el recuadro y el anexo bilingüe.
- [ ] F8 — Reescribir y fijar primero el Post II ES.
- [ ] F9 — Crear el hermano EN desde el ES aprobado semánticamente.
- [ ] F10 — Actualizar freeze revisión 5, contrato revisión 10 y programa de liberación.
- [ ] F11 — Observar todos los nuevos gates rojo→verde con códigos de salida sin tuberías.
- [ ] F12 — Ejecutar suites, Jekyll, Vite, artefacto, matriz visual y Axe.
- [ ] F13 — Entregar hashes finales y evidencia al par para R3.
- [ ] F14 — Repetir gates proporcionales tras cualquier reparación.
- [ ] F15 — Solicitar H1 para contenido, declaraciones, anexo y preview bilingüe.
- [#] EXT — Commit, push, despliegue y difusión; desbloqueo: autorización humana posterior y específica.

## 8. Criterio de hecho y rollback

- El post responde su pregunta sin prometer causalidad.
- Los 18 `PLACEHOLDER` quedan cerrados, limitados o trazados en el ToDo dinámico.
- La auditoría cubre el universo nacional vigente declarado.
- Cada cifra geográfica distingue fuente, año, unidad y denominador.
- Ninguna discrepancia OSM se llama error oficial sin corroboración institucional.
- La auditoría histórica se limita a RBD actuales marcados y casos del Post II.
- El recuadro aporta valor sin dominar la narración.
- El anexo ES/EN conserva método, sensibilidad, atribución y límites.
- Los gates nuevos se observan en rojo y luego en verde.
- R-007 continúa bloqueando el artículo y no el blog.
- Si falla un gate duro, se restauran solo los archivos propiedad de la fase mediante el patch de custodia.
- Si aparece una cifra material contradictoria, se corrigen primero freeze, contrato, ES y EN.
- El cierre local no se presenta como publicación.

## Flags y riesgos vivos

- La observación del NFS al 99 % es vigente solo para el preflight realizado; debe revalidarse.
- La superficie interna exacta de OSM/Nominatim en `stata08` todavía no fue inventariada por el bloqueo de capacidad.
- OSM puede reproducir datos MINEDUC y no constituir corroboración independiente.
- La redistribución de una base combinada MINEDUC–OSM sigue condicionada al gate de licencia.
- El working tree contiene cambios concurrentes y no debe limpiarse ni atribuirse íntegramente a esta tarea.
- La revisión anterior del par no cubre la ampliación OSM; R3 debe juzgar el snapshot final.
