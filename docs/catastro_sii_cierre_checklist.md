# Checklist de cierre — Mapas Catastro SII

Última actualización: 2026-07-18 UTC
Alcance bloqueado: capa comunal nacional + piloto predial Atacama (Caldera y Diego de Almagro). No se generalizan regiones antes de completar todos los gates aplicables. `stata01` procesa; los PMTiles auditados pasan a la laptop para revisión local antes de cualquier despliegue.

Leyenda: `[x]` comprobado, `[~]` en curso o parcialmente resuelto, `[ ]` pendiente, `[!]` bloqueado con causa conocida.

## 1. Código y sitio

- [x] Diagnóstico, placeholders, textos y fallback de la página existente preservados.
- [x] MapLibre GL JS, PMTiles, TypeScript y Vite integrados con carga diferida.
- [x] URL compartible región/comuna y alias plural → ruta canónica.
- [x] Build reproducible con Node 24, TypeScript, Vitest, tests Python, Vite, Jekyll y verificador de artefacto.
- [x] Dependencias de desarrollo actualizadas y auditoría npm sin vulnerabilidades.
- [x] Commit fuente remoto registrado: `2fc2424c`.
- [x] Promoción de manifest atómica, con prueba de éxito y de rollback ante índice territorial ausente.
- [x] DPA 2023 tratada explícitamente: campo `CUT_COM` y exclusión declarada de Antártica Chilena `12202`.

## 2. Seguridad y publicación

- [x] El usuario declara que este proyecto no contiene datos privados a resguardar; se documenta la diferencia entre privacidad y licencia en `docs/catastro_sii_clasificacion_publicacion.md`.
- [x] Pipeline limita la derivación predial a seis campos, rechaza geometrías inválidas y no altera la fuente maestra.
- [x] Upload R2 admite sólo nombres versionados de base/comunas con `PENDING`; un PMTiles `predios_region_*` exige `AUTHORIZED_VECTOR`, y nunca sube GeoParquet, FGB, reportes ni manifests de build.
- [~] Revisión de licencia/permiso de redistribución vectorial SII, separada de privacidad; no hay evidencia documental incorporada todavía.
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
- [x] PMTiles e índices del run `20260718T194751Z` migrados a la laptop; cuatro SHA-256 coinciden con `stata01`, están ignorados por Git y el preview responde `200` + `206 Range` local.

## 4. Piloto de validación Atacama

- [x] PMTiles comunal y Atacama construidos con `PENDING` en almacenamiento de procesamiento; run `20260718T194751Z` persiste sólo sus derivados validados.
- [x] El piloto audita y excluye de la derivación 2 geometrías `null` y 5 vacías en Caldera, y 456 `null` en Diego de Almagro; no modifica el GeoParquet fuente.
- [x] El reintento corrigió el constructor con índice no contiguo antes del run persistido.
- [x] `pmtiles-show`, capas, bounds, zoom, conteos, esquema exacto de atributos y cero geometrías derivadas inválidas validados en `stata01`.
- [x] Presupuesto de tesela se mide y exige antes de persistir: comunal p50=632 B, p95=4.668 B, máx=96.708 B; predial p50=259 B, p95=277 B, máx=86.630 B (límites 150 KB/500 KB/1 MB).
- [ ] Pruebas de integración: nacional → Atacama → Caldera/Diego → cambio de región y liberación de source previo.
- [x] Gate funcional unitario: una fuente predial sólo puede resolverse para una región seleccionada con `AUTHORIZED_VECTOR`; `PENDING` retorna nulo y no inicia carga.
- [ ] Pruebas visuales y móviles, accesibilidad básica, atribución visible y métricas sincronizadas.

## 5. Staging, producción y rollback

- [!] Basemap Protomaps/OSM: extractor por bbox probado en código con `python_base`, estilo listo; no hay aún un archivo Protomaps/OSM versionado bajo `nas05` para generar y revisar el PMTiles Chile.
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
