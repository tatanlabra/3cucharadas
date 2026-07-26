# Convención de distribución y medición externa

Fase 5.2 de `archivo/handoffs/difusion/HANDOFF-2026-07-25-distribucion-3cucharadas.md`.
Fuente original de esta convención: `publicacion-externa/references/checklists.md`
(skill instalada en `penta-agent/skills/`) — este documento la fija como
referencia única para el sitio, sin variaciones improvisadas por post o por
plataforma.

## Convención UTM

Patrón único:

```
?utm_source=<plataforma>&utm_medium=<tipo>&utm_campaign=<slug-del-post>
```

| Plataforma | `utm_source` | `utm_medium` |
|---|---|---|
| Hacker News | `hackernews` | `referral` |
| Medium | `medium` | `syndication` |
| dev.to | `devto` | `syndication` |
| Reddit | `reddit` | `community` |
| LinkedIn | `linkedin` | `social` |
| Bluesky | `bluesky` | `social` |
| Mastodon | `mastodon` | `social` |
| Boletín | `newsletter` | `email` |

`utm_campaign` es siempre el slug del post (mismo valor que `ref` en el front
matter, o el último segmento del `permalink`).

**Advertencia:** los parámetros UTM crean variantes de URL. El canónico
autorreferente de cada post las consolida, pero conviene revisar en Search
Console que no aparezcan como páginas separadas (ver
`followup-seo-gsc-estabilidad-2026-07-09.md` en esta misma carpeta para el
último control hecho).

## Quién aplica la convención

- La skill `publicacion-externa` la aplica al generar `00-metadata.yaml` y
  cada pieza del paquete (`distribucion/<slug>/`) para HN/Medium/dev.to/
  Reddit/LinkedIn/social corto.
- `scripts/syndicate_devto.rb` la aplica al `canonical_url` que manda a la
  API de dev.to (Fase 4.3).
- Cualquier envío manual (LinkedIn nativo, Bluesky/Mastodon vía
  `cucharadas-difusion`) debe seguir la misma tabla al construir el enlace.

## Registro: `_data/distribucion.yml`

Fuente de verdad de qué se publicó, dónde, cuándo y con qué resultado.
Esquema:

```yaml
- slug: <permalink-basename>
  ref_interno: <front matter `ref`>
  url_canonica: <URL absoluta del post en 3cucharadas.cl>
  titulo_usado: <título tal como aparece en el blog>
  publicaciones:
    - plataforma: <mastodon|bluesky|devto|hackernews|medium|reddit|linkedin|...>
      fecha: <YYYY-MM-DD>
      url_publicada: <URL real de la pieza en esa plataforma>
      resultado_30d: <null hasta cumplir 30 días desde el último envío>
```

Este registro es explícitamente el punto de reconciliación entre tres
mecanismos que si no se cruzan, fragmentan la información:

1. El front matter `distribution: {social, republish}` por post.
2. El ledger externo de `cucharadas_difusion`
   (`~/.local/state/3cucharadas-difusion/ledger.jsonl`, fuera de este repo).
3. Este mismo archivo.

Antes de dar por buena una medición, revisar los tres — no asumir que uno
solo tiene la foto completa.

## Qué medir (y qué no)

No usar visitas como métrica de decisión: un pico de tráfico de Hacker News
no es audiencia.

| Métrica | Qué revela | Umbral sugerido |
|---|---|---|
| Lectores recurrentes por canal a 30 días | Si el canal deja audiencia o solo tráfico | Descartar el canal si aporta menos del 5 % tras seis publicaciones |
| Suscriptores/seguidores nuevos por hora invertida | Rendimiento real del esfuerzo | Comparar entre canales, no contra un absoluto |
| Comentarios sustantivos recibidos | Señal de que alguien leyó y le importó | Preferir sobre conteo de comentarios total |

Fase 5.1 (analítica sin cookies) y Fase 5.4 (tablero mensual) quedan
pendientes de una decisión de infraestructura del autor — ver la auditoría
para el detalle.
