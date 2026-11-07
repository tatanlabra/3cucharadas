# Extender mi tesis en 3 cucharadas (parte III) — Paquete de difusión y podcast (`costos-cierre-escolar-trayectorias`)

Estado: **actualizado y verificado localmente el 2026-11-07**, liderando con la ventana macro de 20 años (`2005–2024`: `1.141` cierres regulares con soporte, `78.972` trayectorias expuestas vs. `734.472` controles, `19` cohortes anuales positivas, Callaway y Sant'Anna `+9,11 pp` con cotas de Manski `[+0,43; +16,21] pp`, efectos aleatorios `+6,29 pp`), las 5 etapas institucionales (`2005–2010`, `2011–2015`, `2016–2019`, `2020–2022`, `2023–2024`) y el zoom pre-registrado `2016–2019` (`5,5 %` de los cierres) con sus tres pruebas de estrés (cobertura `G−1 ≥ 90 %` con cotas `[+0,09; +7,84] pp`, pretendencias Rambachan–Roth y continuos vs. entrantes recientes, y calidad previa de la escuela receptora `ΔQ_i`).

| Canal / Pieza | Archivo | Estado | Observaciones |
|---|---|---|---|
| Metadatos y resumen de evidencia | `00-metadata.yaml` | preparado | Canónicos ES/EN, serie completa `2005–2024`, 5 regímenes y zoom `2016–2019` |
| Fuente transcreada maestra (EN) | `01-en-source.md` | preparado | Liderada por la ventana `2005–2024`, las 5 etapas y las 3 pruebas de estrés del zoom `2016–2019` |
| Medium (EN narrativo) | `medium.md` | preparado | Cuerpo narrativo autónomo e instrucciones para fijar el enlace canónico |
| dev.to (EN técnico/reproducible) | `devto.md` | preparado | `published: false`, `canonical_url` hacia EN, foco en DuckDB + gate Ruby + DiD escalonado 20 años |
| Hacker News (envío normal) | `hn.txt` | preparado | Título neutro, comentario inicial del autor y notas para las 3 objeciones técnicas principales |
| Reddit (`r/dataisbeautiful`) | `reddit-dataisbeautiful.md` | preparado | Título `[OC]` para la Figura 2 EN + primer comentario obligatorio con fuente y herramientas |
| Reddit (hilos temáticos EN) | `reddit-hilos.md` | parcial (`r/PublicPolicy` publicado) | `r/PublicPolicy` publicado el 2026-11-01 (`1xle8rs`); borradores listos para `r/dataisbeautiful`, `r/demography` y `r/econometrics` |
| LinkedIn (ES nativo + variante EN) | `linkedin.md` | preparado | Enlace con UTM en el cuerpo y síntesis de la serie `2005–2024`, las 5 etapas y el zoom `2016–2019` |
| X (Twitter) | `x.md` | publicado | Publicado el 2026-11-01 (`status/2116991976646082665`) + hilo actualizado |
| Mastodon y Bluesky | `social-corto.md` / `social.json` | preparado | Raíz ES y respuesta EN sin cifras aisladas ni promoción causal |
| Cápsula de audio NotebookLM / Spotify | `podcast/` | publicado | Publicado en Spotify (`episode/4VIIXt7nDk8RwrtkqEVVZ7`) |
| Control de calidad del paquete | `QA.md` | verificado local | Checklist de paridad numérica (`verify_difusion_coherente.rb`), cotas de Manski y URLs de Reddit |

## Edición adversarial del 2026-11-07

- Mejoras econométricas destacadas en todas las piezas largas: M1 (sensibilidad a pretendencias de Rambachan–Roth simplificada y anclaje en G−2: continuos frente a entrantes tardíos), M2 (cotas de Manski estratificadas por cobertura de actas bajo el DS 315) y M3 (calidad previa de la escuela receptora, ΔQ), siempre subordinadas a la ventana macro 2005–2024 y sus cinco regímenes.
- Correcciones: rótulo de la brecha de cobertura −19,24 pp (reponderada al pareo, no «serie completa»), salvedades del contraste −3,35 pp, subtítulo de Medium sin sobreafirmación, snippet Ruby fiel al gate real, voz autoral en singular.
- Pendiente humano: reejecutar los dos gates listados en `QA.md` antes de cualquier envío.
