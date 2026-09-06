# Cadencia de cierre de difusión · septiembre de 2026

Esta cola no agenda ni publica automáticamente. Cada fila se ejecuta a mano en
su fecha, se verifica en la plataforma y recién entonces se registra en
`_data/distribucion.yml`. D0 queda reservado al release técnico de esta
remediación.

| Día | Fecha | Única plataforma | Pieza | Artefacto o fuente | Gate de cierre |
|---:|---|---|---|---|---|
| D0 | 2026-09-06 | Infraestructura | Release técnico | Commits de remediación | Mismo SHA en GitLab/GitHub, CI y Pages verdes; no enviar Telegram de mantenimiento |
| D1 | 2026-09-07 | DEV.to | Nushell | `difusion/paquetes/nushell-coprocesador-estructurado/devto.md` | Publicar el borrador 4584688, verificar canónico y registrar `estado: publicado` |
| D2 | 2026-09-08 | Mastodon | Nushell ES + respuesta EN | `difusion/paquetes/nushell-coprocesador-estructurado/social-corto.md` | Verificar raíz y respuesta; registrar ambas URLs |
| D3 | 2026-09-09 | DEV.to | Multiagente III | Export de `scripts/syndicate_devto.rb --export-dir DIR` | Revisar y publicar borrador 4582774; verificar canónico |
| D4 | 2026-09-10 | Bluesky | Nushell ES + respuesta EN | `difusion/paquetes/nushell-coprocesador-estructurado/social-corto.md` | Verificar raíz y respuesta; registrar ambas URLs |
| D5 | 2026-09-11 | Medium | Nushell | `difusion/paquetes/nushell-coprocesador-estructurado/medium.md` | Verificar publicación y canónico hacia 3cucharadas.cl |
| D6 | 2026-09-12 | Medium | Multiagente III | Importación manual desde el canónico EN | Revisar adaptación, publicar y registrar URL |
| D7 | 2026-09-13 | DEV.to | CASEN 2024 | Export reproducible del borrador 4584590 | Revisar seis imágenes de galerías, publicar y verificar canónico |
| D8 | 2026-09-14 | Medium | CASEN 2024 | Importación manual desde el canónico EN | Revisar glosas del contexto chileno, publicar y registrar URL |
| D9 | 2026-09-15 | DEV.to | Multiagente I | Export reproducible del borrador 4584570 | Publicar y verificar canónico |
| D10 | 2026-09-16 | DEV.to | AI Quota HUD | Export reproducible del borrador 4235233 | Publicar y verificar canónico |
| D11 | 2026-09-17 | Medium | AI Quota HUD | Importación manual desde el canónico EN | Publicar y verificar canónico |
| D12 | 2026-09-18 | DEV.to | Multiagente II | Export reproducible del borrador 4584571 | Confirmar que enlace al post I e imagen son absolutos; publicar y verificar canónico |
| D13 | 2026-09-19 | DEV.to | Avalúo y vulnerabilidad | Export reproducible del borrador 4584596 | Publicar y verificar canónico |
| D14 | 2026-09-20 | Medium | Avalúo y vulnerabilidad | Importación manual desde el canónico EN | Publicar y verificar canónico |

## Dependencias duras

| Dependencia | Regla |
|---|---|
| Sitio canónico | La URL EN responde 200 y su `canonical` apunta a sí misma antes de abrir el destino externo |
| DEV.to | El Markdown exportado pasa la validación Liquid; `canonical_url` queda limpio y el borrador remoto conserva su id |
| Medium | La historia se importa o configura con canónico hacia `https://3cucharadas.cl`; la previsualización se revisa antes de publicar |
| Social bilingüe | ES es la raíz y EN una respuesta del mismo hilo; Mastodon y Bluesky se cierran por separado |
| Registro | Una fila solo cambia a cumplida después de verificar la URL pública y actualizar `_data/distribucion.yml` |
| Ritmo | Una plataforma por fecha; ES + EN cuentan como una sola superficie cuando pertenecen al mismo hilo |

## Reanudación diaria

1. Ejecutar `ruby scripts/verify_distribution_done.rb --ventana 30`.
2. Exportar DEV.to con `ruby scripts/syndicate_devto.rb --export-dir /tmp/devto-drafts` cuando corresponda.
3. Comparar el artefacto con el borrador remoto y revisar la previsualización.
4. Publicar manualmente solo la fila del día.
5. Verificar URL, canónico y contenido visible; registrar evidencia y volver a ejecutar el gate.
