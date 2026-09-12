# Revisión adversarial del plan: héroes, CASEN y figuras

Fecha: 2026-09-12. Solicitud: revisión con GPT-6-Astra, esfuerzo high.

## Procedencia y alcance

- Revisor: subagente `/root/astra_high_review`, invocado con `model=gpt-6-astra`, `reasoning_effort=high`, `fork_turns=3`.
- Se canceló inmediatamente una primera invocación con herencia completa para hacer explícita la selección de modelo en una invocación de contexto acotado; su resultado no se utilizó.
- La selección está documentada por la llamada; no se dispone de un recibo independiente del backend del proveedor.
- Revisión separada del coordinador, pero ambos son OpenAI: no es revisión entre proveedores.
- Inspeccionó plan resumido y cláusulas exactas, fuentes/código local y cuestionario oficial; no recalculó microdatos, ejecutó builds ni probó UI.
- Dictamen: sin P0 observado; correcciones P1 necesarias antes de implementación. El default corregido de hogares es defendible, condicionado a verificación.
- Estado: **hallazgos incorporados al plan**, no corregidos todavía en el producto.

## Hallazgos y resolución del coordinador

| ID | Prioridad | Hallazgo | Resolución ejecutable |
|---|---|---|---|
| A01 | P1 | La redacción sobre jefatura/principal permite un filtro global incorrecto v28=1; v28 solo se habilita en viviendas multihogar. | D1 usa hogares como estimando principal. Diagnóstico vivienda distingue hogar único, principal válido y ambiguos. Fixture conserva viviendas de hogar único. No se afirma que ese filtro erróneo ya estuviera implementado. |
| A02 | P1 | v9=3/4 no identifica toda co-localización ni viviendas/sitio: indica sitio propio compartido declarado por hogares. | D1/E1 rotulan literalmente el indicador; denominador todos hogares con respuesta válida, no solo propietarios. |
| A03 | P1 | No hay factor oficial vivienda acreditado; seleccionar una jefatura o promediar pesos no lo crea. | Medida principal hogar con expr; no estimación vivienda oficial. r₂ queda como álgebra con p hipotético, sin insertar la proporción de hogares. |
| A04 | P1 | Julia conserva UPM fuera del dominio pero omite estratos de una UPM. | Port Python con fixture manual, contraste Julia solo cuando aplicable; singleton no documentado => IC null y motivo, nunca contribución cero implícita. |
| A05 | P1 | Correlación comunal casi cero no refuta el mecanismo de compartir sitios. | Quitar cláusula de descarte causal; inferencia ecológica limitada. Un estudio futuro requerirá enlace representativo y umbral material fijado previamente. |
| A06 | P1 | Porcentajes previos pueden usar otra unidad/ponderación. | Recalcular nacional y 16 regiones. Cifras previas no son golden tests. Valparaíso/Viña son selecciones exploratorias posteriores a observar los datos. |
| A07 | P1 | Invariancia estricta podría preservar un error fiscal descubierto. | CASEN no entra al cálculo fiscal; si otro error aparece, incidente separado y cierre afectado bloqueado, sin forzar igualdad. |
| A08 | P2 | Generación del héroe no prueba asistencia histórica en texto. | some_ai histórico se apoya en declaración explícita del usuario; conservar unknown en componentes sin evidencia, sin fabricar historia. |
| A09 | P2 | Falta de metadatos no justifica regenerar automáticamente. | Buscar recibos/declaración; reusar con procedencia desconocida cuando corresponda. Regenerar por calidad/familia con original conservado. |
| A10 | P2 | Fondo CSS no consume alt ni selecciona variantes responsive por existir. | U1 cablea picture/srcset/sizes y preload coincidentes, semántica decorativa/informativa explícita, verificación de recurso realmente transferido. |
| A11 | P2 | SVG con texto en archivo no significa texto seleccionable dentro de img. | Descargar SVG y CSV, tabla HTML accesible y validación del embed real. No prometer selección inline. |

## Evidencia focal

| Evidencia | Localización |
|---|---|
| v9 y categorías de tenencia | [Cuestionario CASEN 2024, p. 79](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf#page=79) |
| Habilitación de v28 | [Cuestionario CASEN 2024, p. 83](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf#page=83); libro de códigos CASEN, hoja V filas 153–154 |
| Comunal no representativo | Proyecto CASEN `julia_viz/docs/notes/casen2024_notas.md:151`; [nota oficial](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf) |
| Peso vivienda construido | Repo catastros_sii, `v5_brecha/scripts/prepare_sources.py:212` |
| Dominio y singleton Taylor | Proyecto CASEN `julia_viz/src/07b_complex_survey_ci.jl:56` y `:79` |
| Enum de Forem | [Article oficial](https://raw.githubusercontent.com/forem/forem/main/app/models/article.rb), líneas 134–139 al consultar |
| Overlay accesible/responsive | Blog `_includes/page__hero.html:24` y `:59` |
| SVG vs embed | Blog `scripts/catastro_sii/project_fiscal_gap.py:109`; post Avalúos II ES, imagen en línea 84 |

## Separación epistémica

- **Hecho:** v9 es categoría de tenencia y v28 tiene habilitación; el código observado omite singletons.
- **Deducción:** el conteo de viviendas por sitio no se identifica con esas variables; multiplicar p_h por brecha no lo corrige.
- **Inducción pendiente:** patrones nacionales/regionales/comunales deben recalcularse para el nuevo estimando.
- **Abducción:** co-localización es una explicación compatible, junto con copropiedad, roles matriz/agrícolas, fechas y cobertura; no está identificada causalmente.
- **Discriminación futura:** estimar directamente contribución de co-localización con enlace vivienda–sitio–rol y cobertura representativa; descartar aporte material solo si límite superior queda bajo umbral prerregistrado.
- **Límite:** consenso del coordinador y Astra no acredita corrección empírica ni optimalidad de proveedores.

## Segunda pasada de Astra sobre los documentos

- Confirmó coherentes unidad hogar, r₂ hipotético, singletons sin IC, aislamiento fiscal y límites de proveedor.
- Detectó una dependencia de build faltante: E1 ahora construye y liga fuentes/artefacto antes de verificar _site y entregarlo a R1; Q1 renueva si hay cambios.
- Detectó carrera de verificador: H1 puede producir imágenes en paralelo, pero su aceptación final espera el checker estabilizado de U1.
- Detectó comandos de revisión que eran prosa: D2/R1/G1 ahora declaran manual_review, informe estructurado y comparación de digest.
- La entrada de V1 quedó explícitamente condicionada a D2 y V0. Estas son correcciones documentales, no validación ejecutada del producto.

## Snapshot operativo

- Blog limpio antes de crear este paquete: `fix/pipelines-verdes`, HEAD `bf1ff5ac`.
- Repo analítico limpio: `main`, HEAD `93e3dba979839b3e9711a939a98e57a33e7ede96`.
- Caché de cuotas de 3 minutos al consultar: Claude sesión 76% libre/semanal 97%; Codex semanal 97%; Gemini Google semanal 96%.
- Copilot reporta renovación vencida: no se usa como base confiable de asignación.
- La lectura de cuota no demuestra disponibilidad de ejecución de Claude/Gemini; se hará preflight al despachar.
- experience-memory devolvió abstención; la revisión se fundamentó en fuentes actuales, no en una recuperación semántica.
- Selector MCP produjo recomendaciones, pero informó `MCP observation unavailable; calls continue unmeasured`; no se afirma registro persistente de esa observación.
