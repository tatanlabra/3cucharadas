# PLAN_STATE v2 — cierre y difusión III–IV

Estado documental: implementación local verificada; commit/push autorizados; despliegue pendiente.
HANDOFF-TRACE: Codex integrador → Codex revisor gpt-6-sol high | collaboration | revisión de delta recibida, APPROVE, original bajo evidence/.

## Alcance decidido por el autor

- Único episodio para III y IV; reemplazo del audio existente en Spotify, sin episodio nuevo.
- Corregir Mastodon/Bluesky y completar canales faltantes. Autor no publicó otros canales del IV.
- LinkedIn con carrusel nuevo, pero esperar elección de diseño/tecnología de otra sesión Codex. No tocar difusion/pilotos/.
- Campaña: LinkedIn, X, Medium EN y un subreddit pertinente tras leer reglas. DEV.to/HN excluidos por decisión explícita.
- Paquetes editoriales III después de cerrar difusión, solo preparación local: Zenodo, MPRA, EPAA, Calidad; fichas condicionales SciELO Preprints, Estudios Públicos y Economics of Education Review. Handoff adjunto usa cifras antiguas que deberán auditarse contra versión vigente.
- Usuario autoriza avanzar sin consultas, commit selectivo, push y aviso Telegram cuando las comprobaciones estén completas. No presentar campaña completa mientras falten canales.
- Objetivo de convenio/Fiscalía descartado por el autor: ajeno a esta tarea; no continuar.

## Estado vivo

| Estado | Ítem | Evidencia / condición |
|---|---|---|
| [x] | Mastodon IV ES/EN | Editados y verificados por API pública |
| [x] | Bluesky IV ES/EN | Aclaraciones publicadas y verificadas; originales conservados |
| [x] | Spotify III–IV | Enclosure público SHA b17fa59baaabf1642f800d329836a1e253d0aa336f2f86f7bfb564ea611f8499 idéntico a archivo final; 12:48 |
| [x] | Audio local III/IV ES | Misma URL; declaración IA; HTML con exactamente una cápsula cada uno; EN sin cápsula |
| [x] | Revisión del delta | 401/403 bindings idénticos; los otros dos se restauran por inversa exacta; cuerpos científicos idénticos |
| [x] | Controles locales | Build, artefacto, promoción ES, source-health, 32 tests coherencia y 15 custodia en verde |
| [~] | Commit/push/deploy | Autorizados; verificar SHA en ambos remotos, CI y páginas públicas antes del aviso |
| [*] | LinkedIn/X/Medium | Copy nuevo comprobado; sin envíos |
| [#] | Carrusel LinkedIn | Esperar decisión de tecnología de sesión paralela; estado documental visto no acredita proceso vivo |
| [!] | Reddit | Reglas vigentes pendientes; sin formulario ni envío |
| [.] | Editorial III | Después de difusión; no comenzar depósitos ni comunicaciones |

## Límites y evidencia

Audio no escuchado ni transcrito integralmente por los agentes; coincidencia binaria prueba reemplazo, no exactitud científica hablada. Apple: se enlaza programa existente; no se verificó propagación del audio reemplazado en Apple.

La revisión científica original queda preservada en evidence/semantic-review-before-audio.json. El recibo vigente añade revisión independiente del delta; no afirma nueva lectura científica integral. source-health-final.json registra los checks locales; no acredita CI ni publicación.

El chequeo numérico antes incluía carruseles archivados; dos casos fallaron antes del cambio. Excluye ahora solo difusion/historico/; el mismo contenido obsoleto en carpeta activa sigue siendo rechazado. La custodia histórica admite campañas nuevas solo con fuentes e inventario ligados a hashes, sin restaurar piezas históricas exactas. Conserva 42 archivos, ocho fuentes y ocho carruseles históricos.

El navegador automatizable no encontró Chrome disponible. LinkedIn/X/Medium siguen requiriendo sesión apropiada o interacción del autor. Ningún paquete local equivale a publicación. difusion/pilotos/ era ajeno y no se incluye en commit.
