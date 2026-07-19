# HANDOFF BRIEFING — Fase 2: Avalúo territorial × IGVUST a escala Unidad Vecinal

## Metadata

- Task ID: `3cucharadas-uv-avaluo-igvust`
- From -> To: Claude (Opus 4.8) -> Codex / próxima sesión
- Via: VS Code + CLI
- From model: claude-opus-4-8
- To model: unknown
- From model source: self_report
- To model source: unknown
- Skill: `handoff-protocol`
- Timestamp: 2026-07-19 12:15 -04
- Repos: `/home/ende/Descargas/programaciones/activos/3cucharadas` (sitio) y `.../activos/catastros_sii` (datos)
- Rama: `feature/catastro-sii-mapas`
- HEAD: `c1efcae1 perf(sitio): sirve el logo a la resolución en que se muestra`

## Trazabilidad

HANDOFF-TRACE: Claude le solicita continuidad a Codex (model: unknown) via VS Code

MODEL-REPORT: {"agent":"Claude","provider":"Anthropic","model":"claude-opus-4-8","source":"self_report"}

DECISION: human_validation

---

## Objetivo vigente

Cruzar el **avalúo fiscal del SII** (todos los predios, no solo habitacionales) con el **IGVUST del MDSF** a escala de **Unidad Vecinal**, para preguntar dónde el valor territorial y la vulnerabilidad oficial se contradicen. Producto: segundo selector de mapa (bivariado 4×4) en el visor + post en 3cucharadas.

Tesis: el avalúo es la base del impuesto territorial y por precios hedónicos incorpora seguridad, infraestructura, conectividad y materialidad. No es precio de mercado, pero la relación no es arbitraria.

---

## Estado: FASE 1 CERRADA

6 commits en `feature/catastro-sii-mapas`, compuerta en exit 0 (36 tests Python, 19 vitest).

| Commit | Contenido |
|---|---|
| `ab61d11f` | feat: visor predial Atacama, capa comunal acotada por zoom |
| `66e18c64` | fix: `promote_manifest.py` preserva `commune_default_views` |
| `d9ef1f6c` | fix: paleta clara versionada en la plantilla del basemap |
| `65807a74` | chore: `_headers` con CSP Report-Only + guard de PMTiles en CI |
| `e2468557` | chore: `fetch_check` en upload_r2 + `verify_r2_cors.sh` |
| `c1efcae1` | perf: logo 154 KB → 3,5 KB |

**Estilo claro ya está en R2**: `basemap_chile_20260719T124804Z.style.json`, HTTP 200 + CORS, idéntico al aprobado. Ambos manifests apuntan a él. El estilo neón viejo sigue disponible para rollback.

### Pendiente de Fase 1
- [ ] **Merge a `main` + push** — decisión humana. El visor NUNCA se ha publicado (`3cucharadas.cl/catastro_sii_brecha/` da 404). Es lanzamiento inicial, no actualización.
- [ ] `verify_public_tiles.sh` solo corre DESPUÉS del despliegue. Que falle ahora es correcto.

---

## Estado: FASE 2 EN CURSO

### Completo y validado

- [x] Paquete nuevo `catastros_sii/uv_avaluo/` (espeja la convención de `v5_brecha/`).
- [x] **Etapa 0**: `data/derived/uv_geom.parquet` — 6.891 UV, 6.888 usables, 3 en cuarentena.
- [x] **Golden Caldera PASS**: 10.295 predios, fuga **0,165%** (límite 0,25%), asignación 99,91%.
  La fuga era 0,141% antes de introducir `geom_join`; ver gotcha 11.
- [x] **Oráculo CONARA PASS**: shard 3202 cae en CUT 3102 con 10.287 predios.
- [x] Tabla CONARA del SII versionada en `uv_avaluo/config/conara_sii_comunas.csv` (347 filas).

### Etapa 1 COMPLETA

- [x] **346/346 shards** procesados, todas las compuertas de `qa_report.py` pasan.
  9.401.277 predios deduplicados, 271.150 sin UV (2,884%), fuga mediana 0,641%.
  - Verificado que las tres comunas críticas pasan: Caldera (golden, 0,165%), Cisnes
    (la que reventaba la memoria, 16,2 s) y Las Condes (389.921 predios, 10,9 s).

### Visor: capa UV avanzada y verde

- [x] **Paleta bivariada 4×4 generada y validada**, no elegida a ojo: interpolación
  bilineal entre cuatro esquinas con significado, en ambos temas, contra sus
  superficies reales (`#fcfcfb` / `#1a1a19`). Vive en `layers.ts` como
  `BIVARIATE_PALETTE`. La celda `14` (alta vulnerabilidad **con** alto avalúo) es la
  contradicción que el mapa persigue y recibe el color más saliente: `#5b2a6e`,
  contraste 10,22 en claro.
  - Separación mínima entre celdas adyacentes: 11,6 en claro, **5,9 en oscuro**. Por
    eso la leyenda y el popup no son opcionales en modo oscuro.
- [x] `bivariateFillExpression(theme)` — función **pura**, testeable sin MapLibre.
- [x] `addUvLayers` / `removeUvLayers` en `layers.ts`.
- [x] `AppState` extendido con `mapScale` y `uvLayerVisible`; `UvFeatureProperties` en `types.ts`.
- [x] `tests/catastro_sii/uv-layers.test.ts` — 6 tests. Uno fija que la celda `14` sea
  la más oscura de su fila: si alguien reordena la paleta, la prueba lo detiene.
- [x] **typecheck exit 0 · 25 tests vitest verdes** (19 previos + 6 nuevos).

### Etapas 2-3 EJECUTADAS

- [x] `aggregate.py` + `build_aggregates.py` corrieron. Salidas en
  `data/derived/uv_avaluo.parquet`, `desigualdad_comunal.parquet` y
  `qa/aggregates_summary.json`. Ver la sección de resultados más abajo.
  - Bug corregido en la primera ejecución: `theil_decomposition` anidaba una window
    function dentro de un agregado, lo que DuckDB rechaza. Se reescribió calculando la
    media por grupo en un CTE aparte y reincorporándola por join.
- [~] `src/uv_avaluo/bundle.py` — Etapa 4, aún sin ejecutar (le falta el CLI). Incluye el crosswalk CONARA→CUT derivado
  del propio join espacial (CUT dominante por shard); ese join estaba mal escrito
  como `LEFT JOIN d ON false` y ya quedó corregido.

### Cableado del visor: hecho salvo el último tramo

- [x] `uvLayerAvailable(index, communeCode)` en `availability.ts`. **Gate paralelo**, no
      acoplado al predial: usa su propio índice `data/uv/index.json` para no contaminar
      `parcel_regions`, que lleva el gate legal.
- [x] **Test de no-regresión** en `availability.test.ts`: verifica en ambos sentidos que
      tener capa UV no otorga fuente predial y viceversa. Si alguien acopla los gates,
      falla.
- [x] `MapController.setUvLayer(url, theme)` y `setUvVisible()` en `map.ts`. Al cambiar
      de comuna usa `getSource().setData()`, no remove/add. Si el fetch falla, degrada a
      mapa sin capa, nunca a mapa roto.
- [x] `index.html`: checkbox `#map-layer-uv` en el fieldset existente + leyenda `#uv-legend`
      con los 16 `<span>` y su `aria-label` descriptivo.
- [x] `style.css`: las 16 celdas × 2 temas, validadas con `check:catastro:static-css`.
      **Ojo**: el visor arranca en tema OSCURO, así que `:root` lleva los tonos oscuros y
      `[data-theme="light"]` los sobreescribe — al revés de lo que uno asume.
- [x] **typecheck exit 0 · 28 tests vitest verdes.**

- [ ] **FALTA**: cablear en `app.ts` el handler del checkbox `#map-layer-uv` y del cambio
      de comuna → cargar `data/uv/<cut>.json` vía `setUvLayer`, mostrar/ocultar
      `#uv-legend`, y refrescar la paleta al cambiar de tema. Es el único tramo pendiente
      del visor.

### Subagentes: uno entregó, el otro murió

- [x] **Explorador de burbujas ENTREGADO y validado**:
      `catastro_sii_brecha/assets/explorer.js` (18.991 B, presupuesto 22.528) y
      `explorer.css` (8.335 B). Verificado: sintaxis OK, cero `eval`/`new Function`, cero
      dependencias externas, y el único match de `innerHTML` es un comentario que afirma
      que no se usa. **Falta**: montarlo en `index.html` y generar su JSON de datos.
- [ ] **Bibliografía NO se escribió**: el subagente murió por límite de sesión antes de
      crear `docs/catastro_sii_uv_bibliografia.md`. Hay que relanzarlo. El briefing que
      usé está en el historial; los temas son precios hedónicos (Rosen 1974), assessment
      ratio y regresividad de la tasación, índices compuestos de vulnerabilidad, Theil y
      su descomposición, coropletas bivariadas y MAUP, más marco legal chileno
      (Ley 19.418, impuesto territorial).

### No empezado

- [ ] `scripts/build_web_bundle.py` (falta el CLI de `bundle.py`)
- [ ] Figuras estáticas matplotlib → WebP
- [ ] Post ES/EN

---

## Gotchas técnicos verificados — LEER ANTES DE TOCAR CÓDIGO

### 1. `ST_Transform` necesita `always_xy := true`
Sin él devuelve `(lat, lon)` y **el join espacial da 0 intersecciones**. Me pasó y costó un ciclo de diagnóstico.

### 2. Y además `ST_SetCRS` para alinear la etiqueta
`always_xy` deja el resultado marcado `OGC:CRS84`, mientras los predios dicen `EPSG:4326`. Mismo datum, pero `ST_Intersects` se niega a operar con etiquetas distintas. Ya resuelto en `geom.py`.

### 3. CONARA ≠ CUT
El GeoParquet usa código CONARA del SII (división pre-2007). Casos: Caldera CONARA `03202` / CUT `03102`; Diego de Almagro CONARA `03102` / CUT `03202` — **invertidos entre sí**. Alhué CONARA `14605` / CUT `13502`.

**El join espacial ES el crosswalk**: entrega CUT directo desde la geometría UV. La tabla CONARA es *oráculo de validación*, no dependencia. Para unir desigualdad (indexada por CONARA) con agregados UV (por CUT), el puente se deriva del propio join: CUT dominante por shard.

### 4. `predio` NO es clave única
La clave catastral es `(comuna, manzana, predio)`. En Caldera: 11.285 filas → 10.292 predios únicos. **Sin deduplicar, el avalúo se cuenta múltiple.**

### 5. Usar `pol_area_m2`, no `dc_sup_terreno`
Cobertura 97,4% vs 87,2%. El prorrateo es geométrico (`ST_Intersection / ST_Area`), no necesita superficie declarada.

### 6. NO renormalizar `frac`
El residual `1 − Σfrac` **es la métrica de fuga**. Renormalizar a 1 la haría invisible.

### 7. Cortes IGVUST: geometría 202603 + atributos 202606
Empatan 6.891↔6.891, cero UV sin geometría. La geometría UV es estable (1-2 cambios/año), por eso la combinación es segura. **NUNCA mezclar atributos de ambos cortes**: solo 0,4% de las UV conservan `rank_nac` entre marzo y junio.

### 8. C1 = MAYOR vulnerabilidad
Convención MDSF invertida desde enero 2026. Cualquier salida anterior tiene el sentido opuesto.

### 9. El IGVUST publicado NO trae valor continuo
Solo `rank_nac` (ordinal 1..6891) y cuartiles. `c_ig_reg` y `c_ig_com` **no son comparables entre grupos** (advertencia oficial del MDSF). Solo `c_ig_nac` sirve para comparación transversal.

### 10. La fuga NO es un bug: es el hallazgo

Caldera daba 0,141% y **no era representativo**. La fuga mediana ronda **1,9%** y hay
casos extremos. Diagnóstico en Antofagasta (CONARA 2201): solo 1,3% de predios sin
UV, pero **32,6% de fuga de avalúo** — 2.325 predios concentran 7.260 MMM CLP en
1.030 km².

Causa: las Unidades Vecinales son unidades de **organización vecinal** (Ley 19.418),
definidas por decreto municipal donde vive gente. **No son una teselación completa
del país.** Un yacimiento minero o un área industrial remota no pertenece a ninguna
UV. El catastro registra ahí valor que el IGVUST no puede ver.

Eso es material de post, no un defecto. La compuerta de QA se recalibró: ya no exige
fuga < 1%, solo descarta valores absurdos (>99% o negativos), y **reporta** la
distribución. Peores casos observados: 1106 Camarones 84,9% · 1208 Colchane 65,0% ·
2201 Antofagasta 32,6%.

### 11. Memoria: el problema NO era el tamaño de la comuna

Tres intentos fallidos con OOM antes de dar con la causa. La secuencia del diagnóstico
vale más que la conclusión:

1. Sospeché acumulación entre shards → reciclé la conexión cada 15. **Siguió fallando.**
2. Reciclé en **cada** shard. **Siguió fallando** → no era acumulación.
3. Identifiqué la comuna concreta: **Cisnes (11102), en Aysén**. Pocos predios (5.192),
   así que tampoco era volumen de predios.
4. Causa real: **las UV patagónicas son gigantescas**. Natales tiene **2,3 millones de
   vértices en una sola UV**; Punta Arenas 1,0 M; Cabo de Hornos 843 K. El prefiltro por
   bbox de una comuna austral arrastra varias de esas y el `ST_Intersects` las
   materializa en memoria.

**Fix: `geom_join`, geometría de trabajo con tolerancia proporcional al tamaño.**
UV > ~500 km² → 55 m; > ~50 km² → 11 m; el resto intacta. Resultado: **7,98 M → 1,73 M
vértices (21,7%) con cambio máximo de área de 0,65%**. Una tolerancia uniforme de 5 m
movía áreas hasta 6,2% — por eso es proporcional y no plana.

`geom` conserva la geometría fiel y es la que va al GeoJSON publicado; `geom_join` solo
se usa para el join.

Efecto medido: el golden Caldera pasó de 0,141% a **0,165%** de fuga. Es el costo
aceptado y está documentado en `config/sources.json` (`nota_golden_fuga`), con el umbral
subido a 0,25%.

Además, en `config.connect()`: `preserve_insertion_order=false`, `temp_directory` con
spill a disco, `max_temp_directory_size=40GB`, `memory_limit=4GB`, `threads=3`.

### 11b. `ST_Simplify` descarta la etiqueta de CRS

Y `ALTER TABLE … ADD COLUMN geom_join GEOMETRY` crea la columna **sin CRS**, así que un
`ST_SetCRS` dentro del `UPDATE` no se propaga al tipo. La solución que funciona es
aplicarlo **al leer**, en `shard.py`:
`SELECT ST_SetCRS(geom_join, 'EPSG:4326') AS geom FROM read_parquet(...)`.

### 12. Herramientas
- `pyogrio`, `fiona`, `rtree`: **ROTOS** (libjxl.so.0.11). `geopandas` 1.1.4 sí carga.
- `tippecanoe`, `pmtiles`: **no instalados** localmente (viven en stata01).
- **duckdb 1.5.4 + spatial es el motor**: lee shapefile vía `/vsizip/`, GeoParquet, y hace todo el trabajo espacial.

---

## Decisiones inmutables

1. **No tocar `authorizedParcelSource` ni `manifest.parcel_regions`** — gate legal del piloto Atacama, con test propio. La capa UV es un gate **paralelo**.
2. **No generar PMTiles de UV** — sin tippecanoe; GeoJSON simplificado por comuna (~20 m, `simplify_deg` declarado en el JSON).
3. **No exportar avalúo por predio** en artefactos web — solo agregados UV.
4. **Nunca `MakeValid`** — las 3 UV inválidas (Ovalle 43018092, Coelemu 162037323, Frutillar 101054603; 3.098 personas, 0,019%) van a cuarentena con reporte nominal.
5. **Gini nacional NO se promedia** desde los comunales. Theil debe cumplir `|T − (within+between)| < 1e-10`.
6. Todos los predios, sin distinguir destino. Todas las UV, urbanas y rurales, **declarando el sesgo**.

---

## Sesgo estructural que ordena el relato

Los cuartiles IGVUST son **equipoblados en UV, no en personas**:

| Cuartil | UV | Población RSH |
|---|---:|---:|
| C1 (mayor vulnerabilidad) | 1.722 | 2.004.716 |
| C2 | 1.723 | 4.060.631 |
| C3 | 1.723 | 4.881.781 |
| C4 | 1.723 | 4.990.776 |

**C1 tiene el 25% de las UV pero el 12,5% de la población.** El 80% de C1 es rural o mixto; el 47% de C4 es urbano. Los predios SII se densifican en lo urbano. Un coroplético de UV sobre-representa territorio disperso **por construcción** — esto va declarado en la leyenda y en el post.

Además: 35,5% de las UV son 100% rurales. El IGVUST **no** es un índice urbano.

---

## Cómo retomar

```bash
cd /home/ende/Descargas/programaciones/activos/catastros_sii/uv_avaluo

# 1. ¿Dónde quedó la Etapa 1? El checkpoint está en qa/shard_manifest.json
python3 -c "import json;m=json.load(open('qa/shard_manifest.json'));print(len(m),'shards')"

# 2. Reanudar (salta lo ya hecho, ~8s por comuna pendiente)
python3 scripts/build_pairs.py

# 3. Compuertas
python3 scripts/qa_report.py

# 4. Agregados (SIN PROBAR — esperar que termine la Etapa 1)
python3 scripts/build_aggregates.py
```

### Orden sugerido al retomar

1. **Terminar Etapa 1** (`build_pairs.py`) y pasar `qa_report.py`. Iba en **335/346**.
2. **Ejecutar por primera vez** `build_aggregates.py`. Nunca corrió: espera fallos de
   SQL en `aggregate.py`, sobre todo en `theil_decomposition`, cuya identidad
   `within + between = total` aborta si no cierra a 1e-10.
3. **Escribir `scripts/build_web_bundle.py`**, el CLI que falta para `bundle.py`. Debe
   emitir además `data/uv/index.json` con la lista de comunas, que es lo que consume
   `uvLayerAvailable`.
4. **Cerrar el visor**: el handler en `app.ts` (único tramo pendiente, ver arriba).
5. Revisar qué dejaron los dos subagentes.
6. Figuras y post.

### Verificación del frontend en cualquier momento
```bash
cd /home/ende/Descargas/programaciones/activos/3cucharadas
npm run check:catastro && npm run test:catastro && npm run check:catastro:static-css
bash scripts/catastro_sii/validate_build.sh   # compuerta completa
```
Estado al cerrar la sesión: **typecheck 0 · 28 tests vitest · CSS válido**.

Reprocesar una comuna: `python3 scripts/build_pairs.py --communes 3202 --force`

### Verificación numérica esperada
- Golden Caldera: 10.295 predios, fuga **0,165%**, CUT dominante 3102 con 10.287 predios
- 346 shards. **NO esperes fuga < 1%**: la mediana ronda 1,9% y las comunas mineras y
  patagónicas llegan a 85%. Eso es correcto y es el hallazgo (gotcha 10). La compuerta
  solo rechaza valores absurdos: > 99% o negativos.
- 10.343.893 predios totales en la fuente
- Trehuaco (CONARA 08108 / CUT 16207) **no tiene archivo de predios** — coincide con `quality.json` de Fase 1 (`comunas_sin_fuente_sii: ["12202","16207"]`)

---

## RESULTADOS DEL PIPELINE — ya reproducibles

Etapas 1-3 completas. **346/346 shards, todas las compuertas pasan.**

```
predios deduplicados : 9.401.277   (+942.616 duplicados removidos = 10.343.893)
sin UV               :   271.150   (2,884%)
fuga mediana         :     0,641%
UV con predios       : 6.857 de 6.891
```

Salidas de `build_aggregates.py` (`qa/aggregates_summary.json`):

| Medida | Valor |
|---|---|
| **Gini nacional, avalúo por UV** | **0,7265** |
| **Theil por región** | total 1,2042 · **81,0% intra** · 19,0% entre |
| **Theil por comuna** | total 1,2042 · 43,1% intra · **56,9% entre** |

Dos lecturas para el post:
1. Entre **regiones** la desigualdad es abrumadoramente **interna** (81%), igual que
   sugería el cálculo ad-hoc sobre comunas (77,7%). El resultado se sostiene al cambiar
   de unidad de observación.
2. Entre **comunas** la descomposición **se invierte**: 56,9% de la desigualdad es
   *entre* comunas. Las comunas son internamente más homogéneas que las regiones — el
   territorio segrega a escala comunal, no regional.

El Gini de 0,7265 sobre UV es mucho mayor que el 0,3785 calculado sobre avalúo por
predio comunal: la UV captura concentración territorial que el promedio comunal disuelve.

**5 comunas con fuga 100%** (Tortel, Timaukel, San Gregorio, Laguna Blanca, Río Verde):
sus UV existen pero cubren solo el poblado (168–525 personas) y todos sus predios son
estancias fuera de ellas. Es real, no un bug; la compuerta se recalibró para aceptar el
100% exacto y rechazar solo lo imposible (>100% o negativo).

---

## Cifras que NO se pueden publicar sin recomputar

Calculé estas ad-hoc, **no salen del pipeline** (las de Theil/Gini ya fueron sustituidas
por las de arriba):
- Gini de avalúo por predio comunal: 0,3785 — unidad de observación distinta
- Skew de `cobertura_censo_pct`: 10,85; kurtosis 163,1
- Spearman CASEN n-muestral vs discrepancia: ρ = −0,258, p = 1,8e−06
- ρ(cobertura_censo, cobertura_coordenadas) = 0,409, p = 2,5e−15

`build_aggregates.py` debe reproducirlas. **Si difieren, manda el pipeline.**

---

## Riesgos y flags

- [!] `bundle.py` y `aggregate.py` están **escritos pero sin ejecutar**. Esperar a que termine la Etapa 1.
- [!] 16 colores del bivariado 4×4 está en el límite perceptible, más con el theme toggle claro/oscuro. La matriz debe construirse parametrizada `n×n` para poder degradar a 3×3 cambiando una constante.
- [!] 8,8% de predios sin avalúo se propaga a Gini, Lorenz y Theil. `cobertura_avaluo_pct` va declarada en cada figura.
- [!] El avalúo fiscal **no es precio de mercado**: hay exenciones, reavalúos periódicos por destino, y lo agrícola usa metodología de áreas homogéneas. Nota metodológica obligatoria en el post, aunque se analicen todos los destinos juntos.
- [!] Los claims hedónicos son **inferencias, no hechos observados**. Cerrar con skill `auditoria-critica`.
- [!] Usar skill `investigacion-bibliografia` para el sustento académico (Rosen 1974 y posteriores, avalúo vs mercado, índices compuestos de vulnerabilidad, Theil, coropletas bivariadas).

---

## Plan completo

`/home/ende/.claude/plans/toma-el-handoff-abierto-giggly-waffle.md` — contiene esquemas de tablas intermedias, integración con el visor archivo por archivo, y la lista de "qué NO se hace".

## Criterio de hecho

Cerrado cuando: las 346 comunas pasen `qa_report.py`; Gini y Theil se reproduzcan desde el pipeline; el visor muestre el bivariado UV sin romper el piloto Atacama (`validate_build.sh` verde); el explorador funcione dentro del presupuesto de bytes; y el post ES/EN esté publicado con sustento bibliográfico y nota metodológica.

---

## PUBLICADO — 2026-07-19

`main` = `48e86f48`, empujado a GitLab y GitHub. GitLab Pages desplegó en ~135 s.

| Verificación | Resultado |
|---|---|
| `https://3cucharadas.cl/catastro_sii_brecha/` | **HTTP 200** (antes 404: nunca se había publicado) |
| `verify_public_tiles.sh` | **PASS completo** — basemap, estilo nuevo, fuente Noto, comunas y Atacama, todos con Range/CORS; manifest con 345 comunas |
| Compuerta `validate_build.sh` sobre `main` | exit 0 |

Commits de Fase 2 incluidos: `08453a78` (capa UV con gate propio, UI oculta) y
`9975c28d` (explorador de burbujas).

### ⚠️ HALLAZGO POST-DESPLIEGUE: el `_headers` NO se está aplicando

Verificado contra producción: de las cabeceras que añadí en Fase 1 **no llega ninguna**.
La única presente es `permissions-policy: interest-cohort=()`, que es un default del
hosting y no la mía (la mía declara además `geolocation`, `microphone`, `camera`).

Faltan en producción: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` y
`Content-Security-Policy-Report-Only`.

Dato clave del diagnóstico: `https://3cucharadas.cl/_headers` responde **200**, es decir
el archivo **sí llegó al artefacto** pero se está sirviendo como contenido estático en
vez de interpretarse como configuración. El `include: _headers` de `_config.yml`
funcionó; lo que no funciona es que el hosting lo consuma.

Hipótesis a verificar (no alcancé a cerrarlo):
1. GitLab Pages soporta `_headers` desde 16.7 pero puede requerir plan o configuración
   específica del proyecto.
2. El dominio podría estar servido por otro frontend (no devuelve cabecera `server`,
   lo que sugiere un proxy delante) y ese frontend ignora el archivo.
3. Si el hosting efectivo resultara ser GitHub Pages, `_headers` no aplica en absoluto
   — GitHub Pages no permite cabeceras personalizadas y habría que ponerlas en el
   proxy (Cloudflare Transform Rules, por ejemplo).

**Mientras esto no se resuelva, el sitio está publicado sin política de seguridad.**
No es un regreso respecto al estado anterior (antes tampoco tenía), pero el trabajo de
Fase 1 en ese frente todavía no rinde. Prioridad alta para la próxima sesión.

---

## 🚨 BUG EN PRODUCCIÓN: la portada muestra 1 post de 6

Detectado por la auditoría de gemas y **verificado contra el sitio en vivo**:

```
posts visibles en https://3cucharadas.cl/ : 1
post mostrado : "CASEN 2024 en 3 cucharadas…" (2026-03-15, el MÁS ANTIGUO)
pager         : Anterior · 1 · 2 · Siguiente
posts ES      : 6
```

**Los 5 posts más recientes no aparecen en la portada**, incluido el del catastro SII.

Causa: `index.html:5` fija `permalink: /`. Con `paginate: 5` y 6 posts, `jekyll-paginate`
genera dos páginas y **ambas escriben en `/`**, así que la página 2 pisa a la 1. No
existe ningún directorio `_site/page*`. Mismo síntoma en `/en/`.

Es anterior a todo este trabajo y es independiente del visor, pero pesa mucho más que
cualquier optimización de gemas: es la primera pantalla del sitio.

## Auditoría de gemas — resumen

**Hallazgo que corrige el encargo**: `jekyll-gist` NO está en el `Gemfile`; entra como
dependencia del tema (`minimal-mistakes-jekyll-4.28.0.gemspec:23-27`, junto con
`jekyll-paginate`, `jekyll-sitemap`, `jekyll-feed`, `jekyll-include-cache`). Mientras el
tema sea gema, **`octokit` 4.x no se puede sacar del bundle**; solo se puede dejar de
cargar quitándolo de `plugins:`.

Sin uso, verificado positivamente (no "no encontré", sino ausencia comprobada contra los
1913 alias de gemoji y contra los marcadores que las gemas emiten en el HTML):

| Quitar | Ahorro | Nota |
|---|---|---|
| `jemoji` | **≈21,1 MB** | arrastra `nokogiri`, `activesupport`, `prism`, `html-pipeline`… |
| `jekyll-seo-tag` | 184 KB | los meta tags los emite `_includes/seo.html`, no la gema |
| `faraday-retry` | 60 KB | solo silencia un warning de octokit |
| `jekyll-gist` de `plugins:` | 0 en disco | pero deja de hacer `require "octokit"` en cada build |

Total ≈13% del bundle. Desbloquea `html-pipeline` 2.14 → 3.2.

**No tocar**: `kramdown-math-katex` (el CI aborta sin `class="katex"`), y las cinco que
el tema reinstala igual. Quitar `jekyll-sitemap` del Gemfile es cosmético y **perdería el
comentario de `_config.yml:259-260`** que evita que alguien la reactive por error.

Comandos exactos para aplicarlo: en el informe del subagente. La verificación clave es un
`diff` de los meta tags entre el build actual y el nuevo — debe salir vacío.
