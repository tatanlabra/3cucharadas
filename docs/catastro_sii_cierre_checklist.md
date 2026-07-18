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
- [x] Tippecanoe, rclone y PMTiles se resolvieron desde conda-forge al clonar el entorno geoespacial.
- [!] El primer clon Conda quedó en un CIFS sin ejecución de binarios: el Python del entorno devuelve `Permission denied`.
- [~] Separar entorno y datos: el entorno requiere filesystem ejecutable <90%; los tiles privados pueden persistir en otro volumen <90%.
- [ ] Confirmar GeoPandas, PyArrow, GDAL, Tippecanoe, PMTiles y rclone ejecutables en el entorno final.
- [ ] Extraer DPA 2023 y validar el cruce 345 geometrías + exclusión explícita `12202` contra 346 métricas.

## 4. Piloto privado Atacama

- [ ] Construir PMTiles comunal y Atacama con `PENDING`, sólo en almacenamiento privado.
- [ ] Validar `pmtiles verify/show`, capa, bounds, zoom, conteos, atributos y cero geometrías inválidas.
- [ ] Medir tamaños de tesela: p50 <150 KB, p95 <500 KB, máximo <1 MB o excepción documentada.
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
| 2026-07-18 | Workspace remoto y aprovisionamiento Conda | Paquetes instalados en clon aislado; falla de ejecución por montaje CIFS. Siguiente: clonar el entorno en filesystem ejecutable y reutilizar la caché ya descargada. |
