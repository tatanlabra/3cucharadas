# Checklist de cierre — Mapas Catastro SII

Última actualización: 2026-07-18 UTC
Alcance bloqueado: capa comunal nacional + piloto predial Atacama (Caldera y Diego de Almagro). No se generalizan regiones antes de completar todos los gates aplicables. `stata01` procesa; los PMTiles auditados pasan a la laptop para revisión local antes de cualquier despliegue.

Leyenda: `[x]` comprobado, `[~]` en curso o parcialmente resuelto, `[ ]` pendiente, `[!]` bloqueado con causa conocida.

## 1. Código y sitio

- [x] Diagnóstico, placeholders, textos y fallback de la página existente preservados.
- [x] MapLibre GL JS, PMTiles, TypeScript y Vite integrados con carga diferida.
- [x] URL compartible región/comuna y alias plural → ruta canónica.
- [~] Gate reproducible: el gate integral se ejecuta con Node 24.18.0/npm 11.16.0 temporal en `/tmp`; el PATH persistente aún sólo ofrece Node 26.4.0/npm 12.0.1 y falla en `npm ci`. Falta instalar/registrar el runtime aislado de Node 24 para que el PASS sea reproducible tras reinicio.
- [x] Dependencias de desarrollo actualizadas y auditoría npm sin vulnerabilidades.
- [x] Commit fuente remoto registrado: `2fc2424c`.
- [x] Promoción de manifest atómica, con prueba de éxito y de rollback ante índice territorial ausente.
- [x] DPA 2023 tratada explícitamente: campo `CUT_COM` y exclusión declarada de Antártica Chilena `12202`.

## 2. Seguridad y publicación

- [x] El usuario declara que este proyecto no contiene datos privados a resguardar; se documenta la diferencia entre privacidad y licencia en `docs/catastro_sii_clasificacion_publicacion.md`.
- [x] Contrato predial de ocho campos regenerado: `predio` y `avaluo_fiscal_clp`, sin rol/dirección/propietario; el run `20260718T212932Z` conserva 10.892 polígonos H y rechaza geometrías inválidas sin alterar la fuente.
- [x] Upload R2 admite sólo nombres versionados de base/comunas con `PENDING`; un PMTiles `predios_region_*` exige `AUTHORIZED_VECTOR`, y nunca sube GeoParquet, FGB, reportes ni manifests de build.
- [x] Alcance de publicación aclarado: el usuario declara públicas las fuentes y autoriza su uso; la Resolución 8656 regula la venta SII de 1999, no se usa como bloqueo genérico. Se conserva atribución, derivación mínima y aviso referencial; `PENDING` sólo señala que R2/manifest aún no se despliegan.
- [!] Bucket R2, dominio, CORS y prueba HTTP `Range` pública: no existe aún un remoto `rclone` ni variables de despliegue configuradas en `stata01`; faltan esos insumos externos.

## 3. Datos y entorno remoto

- [x] Caldera, Diego de Almagro y DPA 2023 coinciden por SHA-256 entre local y `stata01`.
- [x] Workspace remoto aislado creado con sólo código versionado; no contiene GeoParquet ni credenciales.
- [x] Se identificaron como faltantes en `python_base`: Tippecanoe, PMTiles y rclone; GeoPandas, PyArrow y GDAL ya están disponibles.
- [x] Retiro de los clones temporales creados en `/mnt/d_58` y `/tmp`; permanecen `site`, logs, tiles y las fuentes.
- [x] Instalación directa de Tippecanoe, PMTiles (`pmtiles-show`) y rclone en `/opt/conda/envs/python_base` mediante conda-forge.
- [x] GeoPandas, PyArrow, GDAL, Tippecanoe, PMTiles (`pmtiles-show`) y rclone validados en `python_base`; Fedora ya tenía `proj-data`, por lo que no se instala DNF adicional.
- [x] Se confirmó que Tippecanoe no puede crear su base SQLite sobre CIFS; el runner construye en disco local y copia los artefactos no publicados al almacenamiento persistente tras validar.
- [x] Workspace de procesamiento migrado desde `d_58` a `/mnt/nas05/proyecto_catastral_sii/outputs/maps/catastro_sii_brechas_maps`; el scratch SQLite permanece en `/tmp` y el piloto usó el override no versionado de 95% registrado.
- [x] DPA 2023 validada: 345 geometrías y exclusión explícita `12202` frente a 346 métricas.
- [x] PMTiles, estilo, fuente PBF e índices del run `20260718T212932Z` migrados a la laptop; los SHA-256 coinciden con `stata01`, están ignorados por Git y el preview responde `200` + `206 Range` local.
- [x] El preview local elimina el selector H y abre por defecto Caldera con el piloto Atacama; selector, métricas y cámara quedan sincronizados y la capa heredada de celdas queda oculta al iniciar MapLibre.
- [x] Prueba de navegador Firefox sobre la URL normal: basemap, fuente PBF, PMTiles comunal/predial y canvas MapLibre de 1082×598 px cargan; Caldera y Diego de Almagro se alternan sin errores JavaScript. Un clic real muestra `Predio` y `Avalúo fiscal` legibles.
- [x] Regeneración de Atacama con `predio` y `avaluo_fiscal_clp`: `python_base` aprueba 14 pruebas geoespaciales; PMTiles, esquema, bounds y presupuesto auditados en `stata01`, luego sincronizados localmente.

## 4. Piloto de validación Atacama

- [x] PMTiles comunal y Atacama construidos con `PENDING` en almacenamiento de procesamiento; run `20260718T212932Z` persiste sólo sus derivados validados.
- [x] El piloto audita y excluye de la derivación 2 geometrías `null` y 5 vacías en Caldera, y 456 `null` en Diego de Almagro; no modifica el GeoParquet fuente.
- [x] El reintento corrigió el constructor con índice no contiguo antes del run persistido.
- [x] `pmtiles-show`, capas, bounds, zoom, conteos, esquema exacto de atributos y cero geometrías derivadas inválidas validados en `stata01`.
- [x] Presupuesto de tesela se mide y exige antes de persistir: predial p50=540 B, p95=558 B, máx=132.485 B (límites 150 KB/500 KB/1 MB).
- [x] Pruebas de integración: nacional → Atacama → Caldera/Diego y salida a Antofagasta pasó en Firefox. Fuera de Atacama el estado confirma mapa comunal sin capa predial autorizada; el unit test cubre la liberación ordenada de capas y source.
- [x] Gate funcional unitario: una fuente predial sólo puede resolverse para una región seleccionada con `AUTHORIZED_VECTOR`; `PENDING` retorna nulo y no inicia carga.
- [~] Pruebas visuales desktop y viewport móvil (390 px), atribución visible y métricas sincronizadas: PASS en Firefox; falta recorrido de accesibilidad con teclado/lector de pantalla.

## 5. Staging, producción y rollback

- [x] Basemap Protomaps/OSM: extractor oficial remoto con región multipolígono, PMTiles autoalojado (600.873.308 B), fuente PBF, etiquetas de ciudades y calles blanco-neón; revisado y sincronizado al preview.
- [ ] Staging local o autorizado, sin exponer vectores SII mientras el gate de entrega siga pendiente.
- [ ] Tras autorización: upload R2 versionado, CORS/Range comprobados y manifest promovido.
- [ ] Rollback ensayado: manifest anterior, PMTiles versionados y reversión Git documentada.
- [ ] Producción.
- [ ] Generalización a otras regiones sólo después de aprobar íntegramente el piloto.

## Registro breve

| UTC | Cambio | Evidencia / siguiente gate |
| --- | --- | --- |
| 2026-07-18 | Integración y hardening local | `2fc2424c`; validación completa local aprobada. |
| 2026-07-18 | Corrección de entorno por instrucción del usuario | Se abandona el clon temporal: el script queda restringido a `python_base`; se eliminan los directorios creados y se instalarán sólo los tres binarios faltantes en `/opt/conda`. |
| 2026-07-18 | Entorno `python_base` cerrado | Tippecanoe 2.79.0, PMTiles 3.7.0 (`pmtiles-show`) y rclone 1.74.3 instalados desde conda-forge. DNF ya tenía `proj-data`; no se modifica Fedora. |
| 2026-07-18 | Primer intento de piloto detenido sin artefactos | La DPA usa `CUT_COM`; el runner no lo propagaba. Se corrige el contrato antes de reintentar. |
| 2026-07-18 | Segundo intento detenido sin artefactos válidos | Tippecanoe no obtiene lock SQLite sobre CIFS. Se aísla el build en `/tmp`; el directorio fallido se retira antes de reintentar. |
| 2026-07-18 | Corrección operativa | El workspace completo deja `d_58` y pasa a `nas05`; el scratch SQLite sigue en `/tmp`. |
| 2026-07-18 | Clasificación de datos y entrega local | El usuario declara que no hay datos privados a resguardar. Se auditaron sólo nombres de columnas, se mantiene una derivación mínima y se agrega flujo `stata01` → laptop para preview localhost ignorado por Git. |
| 2026-07-18 | Hardening de publicación | Se reemplaza el CLI PMTiles inexistente por el adaptador Conda/Python y R2 pasa a allowlist de activos + PASS real de GET Range/CORS. |
| 2026-07-18 | Preflight de dependencias externas | No se encontró archivo Protomaps/OSM en `nas05` ni remoto/variables R2 configuradas en `stata01`; ambos quedan identificados, sin intentar descarga ni publicación. |
| 2026-07-18 | Preview predeterminado corregido | El loopback normal consume el manifest local actual, inicia MapLibre sin esperar intersección y carga el piloto Atacama por defecto. Vite/Jekyll y 8 tests pasan; HTTP local entrega manifest `200` y PMTiles con `206 Range`. |
| 2026-07-18 | Diagnóstico de runtime del visor | Firefox detectó que Vite precargaba el chunk MapLibre desde `/chunks/` y recibía HTML. Se fija `base=/assets/dist/catastro_sii/`, se agrega test de configuración, atribución por defecto para la capa comunal y ocultamiento prioritario del canvas heredado. La URL normal queda comprobada con canvas MapLibre, PMTiles comunal/predial y cero errores JavaScript. |
| 2026-07-18 | Corrección de layout CSS del visor | Una función `linear-gradient` sin cerrar hacía que el navegador descartara las reglas posteriores y dejara el contenedor en altura cero. Se corrige y se incorpora `check:catastro:static-css` al gate. Firefox confirma ahora canvas 1082×598 px, PMTiles comunal/predial, `density` oculto y cero errores. |
| 2026-07-18 | Flujo Caldera/Diego comprobado | Firefox selecciona Caldera (`03102`) y Diego de Almagro (`03202`), actualiza URL y estado de la capa predial referencial, conserva MapLibre y no registra errores. |
| 2026-07-18 | Evidencia de redistribución SII | Se incorpora una fuente oficial sobre la Base de Datos Catastro y la carta compromiso de no traspaso. Se clasifica como hecho/inferencia/no verificado: no hay contrato de adquisición de estas fuentes ni autorización para publicar vector predial, por lo que el gate sigue `PENDING`. |
| 2026-07-18 | Brecha de runtime local detectada | La máquina ahora expone sólo Node 26.4.0/npm 12.0.1, mientras el repositorio fija Node 24.18.0. Los checks directos pasan, pero `npm ci` falla con Node 26 antes del gate integral; no se cambia el contrato ni se instala un runtime sin decisión explícita. |
| 2026-07-18 | Diagnóstico deductivo e inductivo del visor | El manifest local desactiva el basemap y el predial inicia en z13 mientras Diego se enfoca a una comuna extensa; los Parquet H verifican `predio` y `dc_avaluo_fiscal` sin nulos. Se implementan fondo Protomaps oscuro, fuentes PBF, calles blanco-neón, etiquetas y foco de mayor densidad predial. |
| 2026-07-18 | Gate remoto de atributos | Tras sincronizar scripts y tests, `python_base` aprueba 13 pruebas geoespaciales. El primer intento reveló tests remotos desactualizados y una aserción frágil de tamaño de archivo; ambos se corrigen antes de iniciar la nueva corrida Atacama. |
| 2026-07-18 | Run cartográfico cerrado | `20260718T212932Z`: Atacama con 10.892 polígonos H, `predio` y `avaluo_fiscal_clp`; PMTiles predial 22.050.380 B (p50/p95/máx: 540/558/132.485 B). Basemap autoalojado 600.873.308 B, PBF y estilo oscuro/neón copiados a la laptop. |
| 2026-07-18 | Validación visual e interacción | Firefox comprueba calles blanco-neón, etiqueta Caldera, polígonos prediales visibles y popup real (`Predio: 93`, `Avalúo fiscal: $52.008.082`). Selector inicial, mapa y métricas coinciden en Caldera; Diego de Almagro cambia correctamente. |
| 2026-07-18 | Integración de salida y móvil | Firefox en 390 px mantiene canvas 288×302, Caldera/Diego y atribución. Al cambiar a Antofagasta, el estado confirma que sólo queda la capa comunal y no hay predial autorizado. |
| 2026-07-18 | Gate integral | `validate_build.sh` PASS con Node 24.18.0/npm 11.16.0: `npm ci`, TypeScript, CSS, 12 tests Vitest, 14 Python (7 geoespaciales omitidos localmente), Vite, Jekyll y verificador de artefacto. |
| 2026-07-18 | Cierre de scratch remoto | Tras verificar hashes y copia local, se retiraron 409 MB de builds y storage Podman efímeros en `/tmp`; los artefactos versionados de `20260718T212932Z` permanecen intactos en `/mnt/nas05`. |
