# HANDOFF BRIEFING — Catastro SII Mapas

## Metadata

- Task ID: `3cucharadas-catastro-sii-mapas-atacama`
- From -> To: Codex -> próxima sesión Codex / humano revisor
- Via: VS Code + CLI
- From model: GPT-5 (Codex)
- To model: unknown
- From model source: self_report
- To model source: unknown
- Skill: `handoff-protocol`
- Timestamp: 2026-07-19 06:35 -04
- Repositorio: `/home/ende/Descargas/programaciones/activos/3cucharadas`
- Rama: `feature/catastro-sii-mapas`
- HEAD base: `f60c74b4 feat(catastro): habilita piloto Atacama en R2`

## Trazabilidad

HANDOFF-TRACE: Codex le solicita continuidad a próxima sesión Codex (model: unknown) via VS Code

HANDOFF-TRACE: próxima sesión Codex responde la continuidad a Codex (model: unknown) via VS Code

MODEL-REPORT: {"agent":"Codex","provider":"OpenAI","model":"GPT-5","source":"self_report"}

MODEL-REPORT: {"agent":"próxima sesión Codex","provider":"unknown","model":"unknown","source":"unknown"}

DECISION: human_validation

## Objetivo vigente

Cerrar el piloto cartográfico de Atacama en el visor Jekyll de 3 Cucharadas: capa comunal nacional liviana y PMTiles prediales bajo demanda para Caldera (`03102`) y Diego de Almagro (`03202`), usando MapLibre GL JS, PMTiles, TypeScript/Vite, base Protomaps/OSM autoalojada y R2. Primero aprobación visual local; después integración y publicación.

## Decisiones inmutables

- Mantener Jekyll como sitio principal; el visor vive en `catastro_sii_brecha/` y se previsualiza en el puerto `4001`.
- Usar MapLibre GL JS + PMTiles + TypeScript/Vite. No reintroducir GeoJSON predial completo ni publicar GeoParquet predial.
- No alterar geometrías fuente. Las coordenadas de cámara son sólo metadatos de vista, no una edición geométrica.
- La carga predial es estrictamente bajo demanda y sólo para comunas autorizadas por el manifest. En este piloto: Caldera y Diego de Almagro.
- Los datos del proyecto fueron declarados no privados por el usuario. Aun así, conservar el límite técnico de distribución: sólo PMTiles curados y atributos mínimos (`predio`, avalúo fiscal, clase/destino y calidad geométrica); no exportar formatos prediales completos.
- Los procesos de datos canónicos se hicieron en `stata01`; los artefactos persistentes están en `/mnt/nas05` y la copia de revisión está en la laptop. No usar `d_58`.
- R2 ya existe: bucket `3cucharadas-tiles`, dominio `tiles.3cucharadas.cl`. No registrar ni exponer credenciales, Access Keys ni Account ID en este archivo.
- No hacer push, merge a `main`, despliegue GitLab Pages ni modificación de R2 sin un PASS visual humano explícito.

## Estado de implementación

### Completo y validado

- [x] Capa comunal nacional: 345 comunas; exclusión documentada `12202`.
- [x] PMTiles predial Atacama generado y validado: corrida `20260718T212932Z`.
- [x] Piloto habilitado sólo para Caldera (`03102`) y Diego de Almagro (`03202`).
- [x] Asteriscos en selector: `Atacama *`, `Caldera *`, `Diego de Almagro *` se derivan del manifest autorizado, no están codificados a mano.
- [x] La tarjeta de mapa permanece oculta para una comuna sin mapa; sus métricas agregadas siguen visibles.
- [x] Cargador Vite/MapLibre diferido: no arranca hasta que se elige una comuna habilitada.
- [x] Gating adicional en `authorizedParcelSource`: incluso dentro de una región con PMTiles no carga predios fuera de `source.communes`.
- [x] Se corrigió el mapa vacío local. Causa observada: WEBrick/Jekyll devolvía `304` sin cuerpo para rangos PMTiles cacheados. `NoStoreFetchSource` se usa sólo en `localhost`/`127.0.0.1`; R2 conserva su caché normal.
- [x] Validación de navegador real automatizada con Brave/CDP: tarjeta visible, base + comunas + PMTiles predial solicitados y polígonos efectivamente dibujados.
- [x] Cámara inicial por capital comunal, con zoom predial: Caldera `[-70.8267, -27.0674]`, zoom `15.4`; Diego de Almagro `[-70.0494, -26.3670]`, zoom `15.3`.
- [x] Controles de visor: navegación de MapLibre, escala métrica, checkboxes OSM/comunas/predios y botón `Recentrar`.
- [x] Se verificó por navegador que la escala marca `100 m`, que predios se oculta/restaura y que `Recentrar` devuelve a la vista inicial.
- [x] Paleta cartográfica local sobria: base OSM clara, agua azul suave, calles blancas y predios azul-gris por avalúo fiscal. Se eliminó el neón retro del mapa.
- [x] Favicon: sin bloque verde; ahora usa superficie oscura discreta e icono claro.
- [x] Versionado: cabecera muestra `Versión: DD/MM/AAAA`; el pie conserva fecha y hora en zona `America/Santiago`.
- [x] Validación final más reciente:

  ```text
  npm run check:catastro                 PASS
  npm run test:catastro                  7 archivos / 17 pruebas PASS
  npm run check:catastro:static-css      PASS
  python3 tests                          29 pruebas PASS (7 skips esperados)
  npm run build:catastro                 PASS
  Jekyll + verify_site_artifact          PASS
  ```

### Implementación parcial / drifts que el receptor debe conservar

- [~] Cambios de código sin commit. `git status --short` debe mostrar 16 archivos modificados; no limpiar ni usar `git checkout`/`reset`.
- [~] El estilo cartográfico corregido sólo está en una ruta ignorada por Git:

  ```text
  assets/data/catastro_sii/local/20260718T212932Z/basemap_chile_20260718T212932Z.style.json
  ```

  Esa es la fuente que hace que el preview local actual se vea bien. El objeto de igual nombre ya existe en R2 y `upload_r2.sh` usa `--immutable`, por lo que no se puede sobrescribir de forma segura. Para producción se debe crear **un nuevo nombre versionado de estilo**, actualizar ambos manifests para apuntar a él, y subir ese objeto nuevo.

- [~] El manifest de revisión local también está ignorado:

  ```text
  assets/data/catastro_sii/local/manifest.json
  ```

  Contiene `commune_default_views`; el manifest público rastreado también fue actualizado, pero cualquier nueva generación/promoción debe retener esas cámaras.

- [~] `scripts/catastro_sii/promote_manifest.py` hoy sólo preserva `commune_focus_bounds`; si se vuelve a ejecutar, elimina `commune_default_views` del manifest público. Corregirlo antes de usarlo de nuevo o aplicar una configuración posterior explícita.

- [~] `scripts/catastro_sii/r2-cors.json` incluye localmente `http://127.0.0.1:4001`, pero la política real de Cloudflare todavía debe revisarse/actualizarse en el dashboard si se probarán assets R2 directamente desde esa URL. El preview actual no depende de eso porque usa PMTiles same-origin locales.

- [~] La pantalla de mapa no libera la instancia MapLibre si el usuario cambia desde un piloto a una comuna sin mapa: la tarjeta se oculta y no carga ninguna nueva capa predial, que cumple el contrato funcional. El teardown total es una optimización posterior, no un bloqueo de release.

### Pendiente de decisión humana

- [ ] Abrir el preview en navegador normal y aprobar: icono de cabecera, composición de colores, escala de predios, centros de Caldera y Diego de Almagro, y controles.
- [ ] Acordar si la paleta clara azul-gris pasa a producción tal cual. La implementación local ya está hecha; sólo falta aceptación visual.

## Artefactos y cambios de trabajo

### Rastreables en Git, aún sin commit

- `assets/data/catastro_sii/manifest.json` — agrega vistas iniciales por capital para las dos comunas piloto.
- `assets/src/catastro_sii/types.ts` — contrato `CommuneDefaultView` y `commune_default_views`.
- `assets/src/catastro_sii/availability.ts` — gate por comuna autorizada, no sólo por región.
- `assets/src/catastro_sii/map.ts` — transporte PMTiles local sin cache 304, registro de fuentes, escala métrica, visibilidad de capas y cámara/recenter.
- `assets/src/catastro_sii/layers.ts` — colores comunales/prediales sobrios y mejor contraste.
- `assets/src/catastro_sii/app.ts` — controles de capas/recenter y selección de cámara por capital.
- `assets/src/catastro_sii/styles.scss` — controles y popup claros sobre la base OSM.
- `catastro_sii_brecha/index.html` — favicon, sello de versión superior, controles y leyenda.
- `catastro_sii_brecha/app.js` — disponibilidad por manifest, asteriscos, ocultación, sello de versión y carga diferida.
- `catastro_sii_brecha/assets/map-config.js` — manifest publicado configurado.
- `catastro_sii_brecha/assets/map-app-loader.js` — carga sólo tras evento de elegibilidad.
- `catastro_sii_brecha/style.css` — favicon sin verde, toolbar, soporte responsive y superficie de mapa.
- `scripts/catastro_sii/r2-cors.json` — origen `127.0.0.1:4001` candidato.
- `tests/catastro_sii/accessibility.test.ts` — controla navegación + escala.
- `tests/catastro_sii/availability.test.ts` — asegura que el piloto no fuga a otra comuna de Atacama.
- `tests/catastro_sii/map-parcel-lifecycle.test.ts` — dobles MapLibre compatibles con los nuevos métodos.

### Locales ignorados, necesarios para reproducir el preview actual

- `assets/data/catastro_sii/local/manifest.json` — manifest de revisión local con cámaras.
- `assets/data/catastro_sii/local/20260718T212932Z/basemap_chile_20260718T212932Z.style.json` — estilo claro actualizado.
- `assets/data/catastro_sii/local/20260718T212932Z/*.pmtiles` — base, comunas y predios. No agregar a Git.
- `assets/dist/catastro_sii/` — build Vite ignorada; regenerar, no versionar.

## Diagnóstico reproducible del mapa vacío

1. El PMTiles predial contiene datos válidos. A zoom 15, sobre Caldera, se verificaron 727 features MVT en una tesela y atributos permitidos como `predio`, `avaluo_fiscal_clp`, `cod_comuna` y `destino_clase`.
2. Brave mostró solicitudes PMTiles `206` iniciales seguidas por múltiples `304` para ranges cached cuando se usaba el `FetchSource` estándar contra Jekyll/WEBrick.
3. El canvas quedaba en fondo claro sin teselas, aunque `map-status` afirmara que la capa se añadió.
4. `NoStoreFetchSource` pide los rangos locales con `cache: "no-store"`; la captura posterior mostró calles, agua y predios. Se limita a hosts de preview para no degradar la caché de R2.

## Cómo retomar localmente

```bash
cd /home/ende/Descargas/programaciones/activos/3cucharadas

# Verificar cambios existentes; no descartar modificaciones.
git status --short

# Compuerta completa.
bash scripts/catastro_sii/validate_build.sh

# Preview local.
JEKYLL_ENV=development bundle exec jekyll serve --host 127.0.0.1 --port 4001 --no-watch
```

URLs de revisión:

```text
http://localhost:4001/catastro_sii_brecha/?region=03&comuna=03102#explorar
http://localhost:4001/catastro_sii_brecha/?region=03&comuna=03202#explorar
```

Pruebas manuales mínimas:

1. Caldera y Diego de Almagro llevan `*`; Copiapó no.
2. Caldera y Diego muestran mapa; Copiapó no muestra tarjeta de mapa.
3. En ambas piloto aparecen caminos, etiquetas cuando corresponda y polígonos prediales; click abre `Predio` y `Avalúo fiscal`.
4. `OSM`, `Comunas` y `Predios` cambian sólo su capa; `Recentrar` retorna al núcleo urbano.
5. La cabecera muestra el favicon sin recuadro verde y `Versión: 19/07/2026`; el pie muestra la versión con hora.

## To-do detallado y orden de cierre

### A. Cerrar configuración y drifts antes de publicar

- [ ] Crear un nuevo estilo versionado, por ejemplo `basemap_chile_20260719T0635Z.style.json`, a partir del estilo local claro validado. No sobrescribir `basemap_chile_20260718T212932Z.style.json` en R2.
- [ ] Cambiar `basemap.style_url` en:

  ```text
  assets/data/catastro_sii/manifest.json
  assets/data/catastro_sii/local/manifest.json
  ```

- [ ] Corregir `scripts/catastro_sii/promote_manifest.py` para preservar `commune_default_views`, idealmente desde una configuración versionada de cámaras por comuna; añadir prueba que falle si una promoción borra esos campos.
- [ ] Resolver si se versiona el estilo base en una ruta rastreable/plantilla. No añadir los PMTiles ni `assets/data/catastro_sii/local/` al repositorio.
- [ ] Si se probará R2 desde `127.0.0.1`, aplicar manualmente la política de CORS de `scripts/catastro_sii/r2-cors.json` en Cloudflare. Mantener `Range`, `Accept-Ranges`, `Content-Range` y `ETag` expuestos.

### B. Revalidar localmente

- [ ] Ejecutar `bash scripts/catastro_sii/validate_build.sh` después de cualquier cambio de estilo/manifest.
- [ ] Hacer revisión visual de ambas comunas piloto, desktop y móvil.
- [ ] Confirmar accesibilidad manual: foco en canvas/controles, labels de checkboxes, popup sin robo de foco y contraste de predios/base.
- [ ] Hacer prueba de rendimiento con caché fría: primera carga de Caldera, luego Diego de Almagro; registrar Network Range y ausencia de errores de consola.

### C. Preparar commit local, todavía sin publicar

- [ ] Revisar `git diff --check` y `git status --short`.
- [ ] Staging selectivo de los archivos rastreables de esta lista; no incluir `assets/dist/`, PMTiles locales, perfiles de navegador ni archivos temporales.
- [ ] Crear commit con autor explícito:

  ```bash
  git commit --author='tatan <tatanlabra@gmail.com>' -m 'feat(catastro): mejora visor predial Atacama'
  ```

- [ ] Volver a correr la compuerta desde el commit.

### D. Subir el estilo nuevo a R2 y promover sitio

- [ ] Ejecutar el preflight sin revelar credenciales. Usar el remoto rclone ya configurado, bucket `3cucharadas-tiles`, prefijo `catastro-sii` y base pública `https://tiles.3cucharadas.cl/catastro-sii`.
- [ ] Subir **sólo** el nuevo JSON de estilo versionado con `scripts/catastro_sii/upload_r2.sh`. El script usa `--immutable`; esa es la protección esperada.
- [ ] Verificar HTTP `200` + CORS del estilo y `206` + Range/CORS de los tres PMTiles desde el origen de producción.
- [ ] Sólo tras PASS de almacenamiento, publicar el commit por el flujo GitLab Pages establecido para `main`.
- [ ] Ejecutar:

  ```bash
  bash scripts/catastro_sii/verify_public_tiles.sh
  ```

- [ ] Abrir `https://3cucharadas.cl/catastro_sii_brecha/`, verificar ambos pilotos y comprobar que el manifest público coincide con el local.

### E. Rollback

- [ ] Si falla el estilo nuevo: restaurar `basemap.style_url` al último estilo versionado conocido, desplegar sólo el manifest/código anterior y repetir `verify_public_tiles.sh`.
- [ ] No borrar PMTiles ni objetos R2 para rollback; los nombres versionados permiten volver a apuntar al activo previo.

## Riesgos y flags

- [!] No publicar aún: cambios sin commit y revisión humana visual pendiente.
- [!] No sobrescribir el estilo R2 existente: el script lo impide por diseño y los cachés públicos podrían mezclar estilos.
- [!] No regenerar `promote_manifest.py` sin preservar cámaras; hoy borra el nuevo campo de vista.
- [!] Evitar afirmar rendimiento productivo hasta medir R2/Pages reales; la evidencia actual es local.
- [!] Advertencias conocidas no bloqueantes: Sass `@import` deprecado, conflictos Jekyll de `index.html`, chunk MapLibre cercano a 1 MB. No hubo errores de build.
- [!] `NoStoreFetchSource` se limita a preview local; no expandirlo a R2 sin medir impacto en operaciones/cache.

## Criterio de hecho para el receptor

El trabajo estará realmente cerrado cuando: el usuario apruebe visualmente ambos pilotos; el estilo claro esté versionado e inmutable en R2; el manifest publicado apunte a ese estilo y conserve las cámaras; GitLab Pages sirva el commit; `verify_public_tiles.sh` pase; y se valide manualmente que una comuna no piloto no carga ni muestra mapa predial.
