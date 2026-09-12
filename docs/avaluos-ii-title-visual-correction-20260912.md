# Avalúos II — corrección de título y sistema visual

Fecha: 12-09-2026. El usuario rechazó el título y la dirección artística publicados porque no seguían las convenciones existentes de 3 Cucharadas. Esta corrección reemplaza la referencia visual; no modifica datos, cálculos ni conclusiones tributarias.

## Contexto recuperado y decisión

| Tipo | Evidencia | Decisión |
|---|---|---|
| Hecho | Ocho títulos ES del sitio usan la fórmula «tema en 3 cucharadas: tesis»; las series Multiagentes II y III colocan el numeral después de «3 cucharadas». | Usar «Avalúos en 3 cucharadas II: dónde revisar la brecha residencial» y su equivalente EN. |
| Hecho | Avalúos I usa una ilustración Tokyo Night con fondo azul profundo, cian, azul eléctrico, violeta, magenta y acentos lima; el handoff editorial reserva esa identidad para piezas generadas por IA. | El par nuevo toma Avalúos I como referencia de estilo y conserva texto/título en HTML. |
| Hecho | El par publicado el 11-09 usaba una maqueta arquitectónica gris, paleta teal/ámbar y tamaños 1942x809/1672x941. | Queda sustituido como hero/teaser vigente; se conserva como antecedente histórico sin referencias desde los posts. |
| Deducción | El patrón de archivo responsivo del sitio requiere teaser 1280x720 y sibling 640x360 bajo `assets/images/teasers/`; el sistema editorial fija hero 1600x900 y OG 1200x630. | Entregar los cuatro tamaños exactos y declararlos en el manifiesto. |
| Inducción acotada | Los títulos publicados y el primer Avalúo repiten la firma «en 3 cucharadas»; su omisión en el segundo post rompe una pauta visible del corpus actual. | La firma se incorpora en ES y «in 3 spoonfuls» en EN. |
| Abducción provisional | La primera generación se desvió porque el prompt prohibió el brillo Tokyo Night y pidió una revista financiera sobria, aunque el precedente de la serie mostraba lo contrario. | La evidencia discriminante es el prompt conservado y la comparación visual. Se descartaría esta explicación si una pieza generada con la referencia y paleta correctas volviera a la misma estética gris. |

Recall utilizado: `ctx-handoff-2758c5ba272319e7bf9c2feb` para la separación `web`/`social`/`ai-generada`, más inspección vigente de los posts, activos y handoffs. El resultado semántico era pertinente pero no contenía la regla completa del título; se completó con evidencia directa del repositorio.

## Activos vigentes

| Pieza | Archivo | Dimensiones | Bytes |
|---|---|---:|---:|
| Hero | `assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp` | 1600x900 | 156.080 |
| Teaser | `assets/images/teasers/teaser-avaluos-ii-brecha-residencial-1280x720.webp` | 1280x720 | 166.536 |
| Teaser móvil | `assets/images/teasers/teaser-avaluos-ii-brecha-residencial-640x360.webp` | 640x360 | 55.682 |
| OG | `assets/images/avaluos-ii/og-avaluos-ii-brecha-residencial-1200x630.webp` | 1200x630 | 144.804 |

Frente al par WebP anterior, el hero baja de 1.449.082 a 156.080 bytes y el teaser principal de 1.495.992 a 166.536 bytes. La comparación combina cambio de contenido, resolución y compresión; describe la transferencia final y no aísla causalmente cada factor.

## Prompts ejecutados

Modo: `image_gen` integrado. El hero usa como referencia estilística el hero de Avalúos I; el teaser usa el hero nuevo como referencia de escena y estilo. Los PNG originales permanecen en el almacenamiento de generación integrado; sólo las entregas WebP optimizadas son consumidas por el proyecto.

### Hero

```text
Use case: stylized-concept. Asset type: bilingual editorial website hero for the second post in the 3 Cucharadas property-assessment series. Image 1 is the approved visual style reference for this series. Match its Tokyo Night editorial identity, color energy, urban geometry, luminous linework, and sober technical mood; do not copy its person, wording, charts, numbers or exact composition. Create a 16:9 conceptual illustration about the gap between Chile's physical residential city and its cadastral records. Use a deep navy hillside city with luminous parcel polygons that align in many places but leave a few discontinuities. Keep the left 42 percent dark and calm for the HTML title and the main city on the right. Palette: #090B18, #111527, #F4F5F8, #00CFFF, #2F7DF6, #7A5CFA, #E83ECA, with sparse #B9E437 and #FF9E45. No text, numbers, currency, logos, flags, seals, identifiable people or properties, fake statistics, real maps, photorealism, beige corporate rendering, dashboards or stigmatizing imagery.
```

### Teaser

```text
Use case: style-transfer. Asset type: 16:9 teaser and social-card illustration. Image 1 is the newly generated hero and defines the exact scene, Tokyo Night palette, line language, lighting and subject. Recompose the same hillside residential city and luminous cadastral layer into a compact centered frame; remove the hero's empty title area, preserve safe margins and make the motif legible at 320 pixels. Keep large shapes and the same navy, cyan, blue, violet, magenta and warm-window palette. No text, numbers, charts, logos, flags, seals, currency, people, watermark, fake statistics, real maps, photorealism or gray corporate rendering.
```

## Verificación

El manifiesto corregido se ejecutó primero contra las referencias antiguas y falló con cuatro errores V10, dos por idioma. Tras actualizar los front matter, `ruby scripts/verify_visual_assets.rb --strict` aprobó nueve manifiestos, 108 activos referenciados y cero avisos. El resto de build, QA visual y producción queda ligado al contrato de corrección.

El build productivo final aprobó y generó 1.312 entradas por 78.898.222 bytes. `verify_site_artifact.rb`, `verify_distribution_readiness.rb` y `verify_repo_governance.rb --strict` quedaron verdes; el gate de distribución comprobó 20 posts y OG de al menos 1.200 px. Las cinco pruebas de salud sumaron 23 aserciones sin fallos. Persisten sólo las deprecaciones Sass `@import` ya conocidas del tema.

Se inspeccionaron el hero ES a 1440x1000, ES a 390x844 y EN a 390x844, además del teaser móvil y el OG finales. La primera captura EN reveló que el caption largo se truncaba; se abreviaron ambos idiomas y la segunda captura confirmó el texto completo. Título, tiempo de lectura y ciudad permanecen separados y legibles en las tres muestras; esto no certifica todos los navegadores ni un iPhone físico.

Axe 4.12.1 acotado a WCAG 2 A/AA produjo cero violaciones, 30 comprobaciones aprobadas y una inconclusa: no puede resolver automáticamente contraste sobre gradientes. La corrida sin filtro también muestra tres hallazgos de buenas prácticas del template compartido —orden de encabezados y regiones/landmarks—; esta corrección no tocó ese template y no los presenta como resueltos.

Estado local: C1–C3 completos. C4 permanece pendiente hasta observar CI y comparar en producción el título y los cuatro recursos contra los hashes locales.
