# Checklist de cierre — Mapas Catastro SII

Última actualización: 2026-07-18 UTC
Alcance bloqueado: capa comunal nacional + piloto predial Atacama (Caldera y Diego de Almagro). No se generalizan regiones ni se publican vectores SII antes de completar todos los gates aplicables.

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

- [x] `LEGAL_PUBLICATION_STATUS=PENDING` mantiene capas y predios en `available: false`.
- [x] Pipeline limita los atributos prediales públicos y rechaza geometrías inválidas sin alterar la fuente maestra.
- [x] Subida R2 aborta salvo `AUTHORIZED_VECTOR`.
- [ ] Autorización jurídica explícita para redistribución vectorial SII.
- [ ] Bucket R2, dominio, CORS y prueba HTTP `Range` con respuesta `206`.

## 3. Datos y entorno remoto

- [x] Caldera, Diego de Almagro y DPA 2023 coinciden por SHA-256 entre local y `stata01`.
- [x] Workspace remoto aislado creado con sólo código versionado; no contiene GeoParquet ni credenciales.
- [x] Se identificaron como faltantes en `python_base`: Tippecanoe, PMTiles y rclone; GeoPandas, PyArrow y GDAL ya están disponibles.
- [x] Retiro de los clones temporales creados en `/mnt/d_58` y `/tmp`; permanecen `site`, logs, tiles y las fuentes.
- [x] Instalación directa de Tippecanoe, PMTiles (`pmtiles-show`) y rclone en `/opt/conda/envs/python_base` mediante conda-forge.
- [x] GeoPandas, PyArrow, GDAL, Tippecanoe, PMTiles (`pmtiles-show`) y rclone validados en `python_base`; Fedora ya tenía `proj-data`, por lo que no se instala DNF adicional.
- [x] Se confirmó que Tippecanoe no puede crear su base SQLite sobre CIFS; el runner construye en disco local y copia los artefactos privados al almacenamiento persistente tras validar.
- [~] Workspace privado se migra de `d_58` a `/mnt/nas05/proyecto_catastral_sii/outputs/maps/catastro_sii_brechas_maps`; la capacidad se registra y se usa un límite privado de 95% autorizado para este piloto.
- [ ] Extraer DPA 2023 y validar el cruce 345 geometrías + exclusión explícita `12202` contra 346 métricas.

## 4. Piloto privado Atacama

- [ ] Construir PMTiles comunal y Atacama con `PENDING`, sólo en almacenamiento privado.
- [~] El primer build en `nas05` identificó 5 geometrías residenciales vacías en Caldera; se excluyen sólo de la derivación con conteo auditado, sin reparar ni alterar el GeoParquet fuente.
- [~] El reintento expuso y corrige un constructor de GeoDataFrame con índice no contiguo; no escribió artefactos prediales persistentes.
- [ ] Validar `pmtiles-show`, capa, bounds, zoom, conteos, atributos y cero geometrías inválidas.
- [~] Medir y hacer cumplir tamaños de tesela: p50 <150 KB, p95 <500 KB, máximo <1 MB. El piloto actual mide 4,7 KB/94 KB (comunal) y 277 B/85 KB (predial) en p95/máximo; el reporte se integrará al run.
- [ ] Pruebas de integración: nacional → Atacama → Caldera/Diego → cambio de región y liberación de source previo.
- [ ] Pruebas visuales y móviles, accesibilidad básica, atribución visible y métricas sincronizadas.

## 5. Staging, producción y rollback

- [ ] Basemap Protomaps/OSM autoalojado como PMTiles y estilo validado.
- [ ] Staging privado o autorizado, sin exponer vectores SII con el gate actual.
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
