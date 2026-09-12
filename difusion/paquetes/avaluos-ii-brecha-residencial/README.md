# Avalúos II — paquete y estado de difusión

Estado al cierre del 12 de septiembre de 2026: Mastodon y Bluesky publicados y verificados en ES/EN; X publicado según confirmación del autor, pendiente de URL; LinkedIn con edición del autor e imagen adjunta, publicación sin verificar. El bloqueo por inicio de sesión quedó superado. No hay programación acreditada. Evidencia: `docs/releases/20260912-social-closeout/publication.json` y `00-metadata.json`.

`linkedin.txt` conserva una propuesta anterior a la edición final del autor en la plataforma. `x-single.txt` conserva la versión local propuesta; no acredita el texto exacto publicado. Se versionan como material de trabajo, sin sustituir las versiones del autor ni autorizar su reenvío. `social.json` sí contiene el texto utilizado en Mastodon/Bluesky.

| Pieza | Archivo para copiar | Imagen sugerida |
|---|---|---|
| LinkedIn ES | [linkedin.txt](linkedin.txt) | [Escenarios monetarios](media/monetary-top15-es-dark.png) |
| X, publicación única alternativa | [x-single.txt](x-single.txt) | [Diferencia residencial](media/gap-top15-es-dark.png) |
| X, hilo de cinco mensajes | `x-01.txt` a `x-05.txt`, en ese orden | Diferencia residencial en el primero; escenarios monetarios en el tercero |

El mensaje único y el hilo de X son alternativas históricas: el autor ya confirmó una publicación, por lo que no corresponde enviar ahora la otra. Los archivos `.txt` conservan solo texto; las instrucciones y textos alternativos están separados. Las imágenes son copias exactas de las figuras revisadas, sin recortes ni cambios de cifras.

## Criterio editorial

- Tipo: análisis de datos y política pública; audiencia profesional chilena.
- Idea central: una discrepancia persistente junto a avalúos altos orienta una revisión predial, pero no prueba omisión ni deuda tributaria.
- Evidencia seleccionada: Lo Barnechea, residuo de 2.300 unidades y escenarios de $4.983/$6.669 millones; Iquique, 18.949 unidades y $36/$4.309 millones. Valores redondeados del artículo local revisado.
- Condición del cálculo: un nuevo predio comparable por unidad residual; impuesto general teórico anual equivalente, con ceros incluidos y parámetros del primer semestre de 2026. No son giros efectivos, recaudación constatada ni ingresos municipales íntegros.
- CASEN identifica una tenencia declarada por hogares; no estima viviendas por sitio. No se descuenta de las barras ni de los escenarios fiscales.
- Materialidad y campamentos son escenarios con supuestos; no identifican por sí solos predios omitidos. No atribuir ilegalidad, exención ni negligencia de forma automática.
- Gráficos: Python/Matplotlib y agregados verificables. Portada: ilustración conceptual con IA; no presentarla como cartografía o evidencia territorial.

## Pendientes documentales y lecciones

1. Capturar las URLs públicas de LinkedIn/X y el texto final del autor; no inferir ausencia de publicación de la falta de registro.
2. Conservar la deuda de rendimiento AC-Q6: la autorización de publicación no convirtió el resultado RED en PASS.
3. Adjuntar medios antes de la edición final; si el autor ya editó, respaldar texto y menciones y verificar su conservación después de adjuntar.
4. Verificar visualmente recorte, ejes y cifras de cualquier video. Un MP4 técnicamente válido no basta: los ensayos en `/tmp` no quedaron aprobados para difusión.

La propuesta original «LinkedIn y X al día siguiente» quedó superada por la publicación que confirmó el autor. No constituye una reserva ni debe convertirse en un envío duplicado. Los textos alternativos preparados están en [alt-text.md](alt-text.md); su existencia no acredita que la plataforma los haya guardado.

Las comprobaciones y sus límites están en [QA.md](QA.md); las fuentes, versiones y hashes, en `00-metadata.json`.
