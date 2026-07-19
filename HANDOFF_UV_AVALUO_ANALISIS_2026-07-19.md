# HANDOFF — Análisis avalúo × vulnerabilidad (UV/IGVUST) y su publicación

## Metadata

- Task ID: `3cucharadas-uv-avaluo-analisis`
- From → To: Claude (Opus 4.8) → Codex
- Via: VS Code + CLI
- From model: claude-opus-4-8 · From model source: self_report
- Skill: `handoff-protocol`
- Timestamp: 2026-07-19 ~20:00 -04
- Repos: `activos/3cucharadas` (sitio) · `activos/catastros_sii` (datos)
- Rama: `main` · HEAD: `3adca3c4`

HANDOFF-TRACE: Claude le solicita continuidad a Codex (model: unknown) via VS Code

MODEL-REPORT: {"agent":"Claude","provider":"Anthropic","model":"claude-opus-4-8","source":"self_report"}

DECISION: human_validation

---

## ⚠️ LEE ESTO PRIMERO: hay dos cosas sin commitear a propósito

```
 M _config.yml                              ← NO COMMITEAR TAL CUAL
 M docs/cabeceras_seguridad_cloudflare.md   ← sí commitear (aviso de doc obsoleto)
```

**`_config.yml` tiene levantada la exclusión del visor** para una revisión local en curso
(`jekyll serve` en el puerto 4001). El estado que debe volver a producción es **con** el
bloque de exclusión:

```yaml
exclude:
  # Visor Catastro SII retirado de publicación mientras se pule. Para volver a
  # publicarlo basta con quitar estas dos líneas y el published:false de los posts.
  - catastro_sii_brecha
  - assets/dist/catastro_sii
```

Antes de cualquier commit de `_config.yml`, **restaura ese bloque**. Si un subagente que
quedó corriendo tocó `paginate: 5 → 8`, ese cambio sí va, pero sin arrastrar la exclusión.

**Puerto 4000 = LiteLLM.** Usar 4001+ para previews.

---

## Estado de publicación

| | Estado |
|---|---|
| `https://3cucharadas.cl/` | **200** — 5 posts en portada |
| `/catastro_sii_brecha/` | **404** — retirado a propósito |
| `/datos/python/openstreetmap/catastro-sii-brecha/` | **404** — post viejo retirado |

La retirada es reversible: los posts llevan `published: false` (conservan archivo e
historial) y el visor sale por exclusión en `_config.yml`. `verify_site_artifact.rb` tiene
sus checks del visor dentro de un `if Dir.exist?`, así que la compuerta sigue en exit 0.

**Para republicar:** quitar las dos líneas del `exclude` y el `published: false` de los dos
posts (`_posts/2026-07-17-catastro-sii-brecha-python-osm{,-en}.md`).

---

## LO QUE BLOQUEA: una decisión de fondo sobre el eje del mapa

El post y el mapa bivariado usan **avalúo por hogar** en el eje X. **Los datos dicen que
fue mala elección.** Esto hay que resolverlo antes de publicar nada.

### Evidencia

Matriz bivariada 4×4 (qv=1 más vulnerable, qa=4 más avalúo/hogar), en número de UV:

```
        qa1    qa2    qa3    qa4
 qv1    399    344    446    530     ← la celda "contradictoria" es la MAYOR
 qv2    564    451    385    321
 qv3    467    509    429    316
 qv4    293    419    463    546
```

No es diagonal. La celda "muy vulnerable + mucho avalúo" (530 UV) supera a la "coherente"
(399). Parecía hallazgo; **es artefacto del denominador**. Dentro de `qv1`:

| Celda | UV | Hogares (mediana) | Superficie (mediana) | Avalúo/hogar |
|---|---:|---:|---:|---:|
| qv1·qa1 | 399 | 265 | 3,4 km² | 10,2 MM |
| qv1·qa2 | 344 | 368 | 15,2 km² | 26,2 MM |
| qv1·qa3 | 446 | 274 | 45,6 km² | 57,6 MM |
| qv1·qa4 | **530** | **120** | **78,2 km²** | 185,6 MM |

Al subir el indicador, los hogares caen (265→120) y la superficie se multiplica por 23. Son
UV rurales extensas con poca gente: el ratio sube porque el denominador es chico.

Correlaciones (n≈6.850):

```
corr(ln av/hogar, ln hogares)     = -0,265
corr(ln av/hogar, ln superficie)  = +0,487
corr(ln av/hogar, vulnerabilidad) = -0,061   ← prácticamente CERO
```

### El dato que cambia el diseño

| Normalización | corr con vulnerabilidad | n |
|---|---:|---:|
| avalúo / hogar | −0,061 | 6.849 |
| avalúo / persona | −0,079 | 6.849 |
| **avalúo / m²** | **−0,582** | 6.851 |
| avalúo total | −0,371 | 6.857 |

**Avalúo por m² sí correlaciona fuerte** (−0,58): donde el suelo vale más por metro, menos
vulnerabilidad. Es la hipótesis hedónica del post.

**Pero restringido a UV urbanas (`p_urbano > 50`) se desploma a +0,079** (n=3.221). El
−0,58 nacional captura sobre todo el gradiente urbano-rural, no diferencias de barrio.

### Tres opciones, la decisión es del humano

- **A** — cambiar el eje a avalúo/m² y reescribir la cucharada 2 con cuatro hechos
  estilizados. Requiere regenerar el bundle del visor con el cuartil nuevo.
- **B** — mantener avalúo/hogar y publicar el resultado nulo como hallazgo metodológico.
  Honesto, menos vistoso, no toca el visor.
- **C** *(mi recomendación)* — presentar **ambas** normalizaciones como el hecho estilizado
  central: la conclusión depende de cómo normalices, que es MAUP en forma pura y conecta
  con la advertencia del Theil que el post ya trae. Requiere regenerar el bundle.

Si se elige A o C: en `bundle.py`, `add_national_quartiles()` calcula
`q_avaluo_hogar_nac` sobre `avaluo_por_hogar`. Hay que añadir (o sustituir por)
`q_avaluo_m2_nac` sobre `avaluo_por_m2`, propagarlo al GeoJSON en `build_uv_geojson()`
(propiedad `qa`) y regenerar con `scripts/build_web_bundle.py`.

---

## Estado del pipeline (terminado y verificado)

`activos/catastros_sii/uv_avaluo/` — commit `68c0d79`.

```
346/346 shards · todas las compuertas de qa_report.py pasan
predios deduplicados : 9.401.277  (+942.616 duplicados = 10.343.893)
sin UV               :   271.150  (2,884%)
fuga mediana         :     0,641%
UV con predios       : 6.857 de 6.891
```

Resultados en `qa/aggregates_summary.json`:

| Medida | Valor |
|---|---|
| Gini nacional (avalúo por UV) | **0,7265** |
| Theil por región | total 1,2042 · **81,0% intra** · 19,0% entre |
| Theil por comuna | 43,1% intra · 56,9% entre |

⚠️ **La "inversión" del Theil es en buena parte algebraica**, no evidencia: con particiones
anidadas, refinar la partición sube el componente entre-grupos (Shorrocks 1984). El post ya
lo declara así y lo usa como ilustración del MAUP. **No revertir esa redacción.**

### Artefactos web ya generados y commiteados
- `catastro_sii_brecha/data/uv/*.json` — 346 comunas + `index.json`, 9,4 MB total
- `catastro_sii_brecha/data/explorador_comunal.json` — 346 comunas, 39 KB

---

## Trabajo pendiente, en orden

1. **Resolver la decisión A/B/C** del eje. Bloquea todo lo demás.
2. **Reescribir la cucharada 2** del borrador con tablas y 3-4 hechos estilizados. El
   usuario pidió esto explícitamente y aceptó que alargue el post.
   Borrador: `_drafts/2026-07-20-avaluo-vulnerabilidad-unidad-vecinal.md` (1.306 palabras,
   4 bloques KaTeX, 6 DOI). Estilo aprobado por el usuario: no cambiarlo, solo añadir.
3. **Par en inglés** `-en.md` con el mismo `ref: avaluo-vulnerabilidad-uv`.
4. **Montar el explorador**: `catastro_sii_brecha/assets/explorer.{js,css}` existen,
   validados (19 KB, sin `innerHTML`, sin dependencias) pero **no están referenciados en
   ninguna página**. Falta el `<script>`/`<link>` y un contenedor.
5. **Republicar** visor y post cuando estén pulidos.
6. **Cloudflare**: proxy activo (A, AAAA y www en naranja, verificado). **Faltan las tres
   Transform Rules** — 0 de 5 cabeceras propias llegan hoy. Runbook completo con valores
   literales en `docs/runbook_cloudflare_headers.md`. Dos trampas: usar `Set` y no `Add`,
   y filtro `http.host` en las tres reglas o se rompe el CORS de `tiles`.
   **No instalar Origin Certificate**: el origen ya tiene GTS válido hasta el 3-oct y es la
   única acción irreversible del procedimiento.

### Subagente en vuelo al momento de escribir esto
Uno quedó corriendo con dos tareas: subir `paginate` de 5 a 8 (para que el pager quede
inactivo) e investigar por qué cambió el teaser del post de CASEN. **Revisar qué dejó en el
working tree antes de commitear.**

---

## Gotchas del pipeline (los caros de redescubrir)

1. **`ST_Transform` necesita `always_xy := true`** o los ejes salen invertidos y el join da
   0 intersecciones.
2. **`ST_Simplify` descarta la etiqueta CRS**, y `ALTER TABLE … ADD COLUMN GEOMETRY` crea la
   columna sin CRS. Solución: `ST_SetCRS(geom_join, 'EPSG:4326')` **al leer**, en `shard.py`.
3. **CONARA ≠ CUT.** El GeoParquet usa código CONARA del SII (división pre-2007). Caldera es
   CONARA 03202 / CUT 03102 — invertido con Diego de Almagro. El join espacial **es** el
   crosswalk; la tabla del SII (`config/conara_sii_comunas.csv`) es oráculo de validación.
4. **`predio` no es clave única**: la clave catastral es `(comuna, manzana, predio)`.
5. **La fuga NO se renormaliza.** El residuo `1 − Σfrac` es la única señal de que un predio
   quedó fuera de toda UV. En comunas mineras y patagónicas llega al 100% y es correcto:
   las UV son unidades de organización vecinal (Ley 19.418), no teselan el territorio.
6. **Memoria de DuckDB**: las UV patagónicas llegan a 2,3 M de vértices (Natales) y
   reventaban el join. Fix: `geom_join` con tolerancia proporcional al tamaño (7,98 M → 1,73 M
   vértices, cambio de área máximo 0,65%). Lo mismo aplicó al GeoJSON publicado: con
   tolerancia plana Natales pesaba 8 MB, con proporcional 507 KB.
7. **Un CUT puede recibir predios de más de un shard CONARA** cuando el límite comunal cruza.
   El join con desigualdad duplicaba filas (348 comunas para 346 reales); se colapsa por CUT
   ponderando por número de predios.

---

## Cómo retomar

```bash
cd /home/ende/Descargas/programaciones/activos/catastros_sii/uv_avaluo
python3 scripts/qa_report.py            # compuertas del pipeline
python3 scripts/build_aggregates.py     # recomputa Gini/Theil en segundos
python3 scripts/build_web_bundle.py     # regenera GeoJSON + explorador

cd ../../3cucharadas
bash scripts/catastro_sii/validate_build.sh   # compuerta completa, debe dar 0
```

Preview local (recordar: 4000 es LiteLLM):
```bash
JEKYLL_ENV=development bundle exec jekyll serve --drafts --future --host 127.0.0.1 --port 4001 --no-watch
```

---

## Documentación de apoyo

- `docs/catastro_sii_uv_bibliografia.md` — 31 referencias, 25 validadas contra CrossRef.
  Contiene las tres advertencias que el post debe declarar y la corrección sobre el Theil.
- `docs/runbook_cloudflare_headers.md` — procedimiento vigente.
- `docs/cabeceras_seguridad_cloudflare.md` — **obsoleto**, marcado como tal; se conserva por
  el diagnóstico de la causa raíz.
- `HANDOFF_3CUCHARADAS_UV_AVALUO_IGVUST_2026-07-19.md` — handoff anterior, con el detalle
  completo del pipeline.

## Criterio de hecho

Cerrado cuando: se resuelva la decisión del eje; la cucharada 2 tenga sus tablas y hechos
estilizados; exista el par ES/EN; el explorador esté montado; visor y post estén
republicados con `validate_build.sh` en 0; y las Transform Rules de Cloudflare entreguen las
cinco cabeceras sin romper el CORS de `tiles`.
