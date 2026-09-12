# Cierre de comprobaciones locales — Avalúos II

Fecha: 11-09-2026. Esta continuación completa evidencia de carga e integración; el objetivo monetario permanece dependiente de una fuente externa. Sin push ni publicación.

## Evidencia cartográfica

La [serie emparejada completa](catastro-paired-loading-20260911-focus.md) cumple el protocolo fijado antes de medir: diez observaciones válidas, dos cebados y dos exclusiones por foco conservadas. Mapa útil frío 2.002,20 → 1.593,10 ms (−20,43 %); recarga 1.668,10 → 1.077,45 ms (−35,41 %). Estilo, capas y encuadre final equivalentes. El evento inicial `load`, con cámaras distintas, mejoró 6,72 % en frío y no acredita por sí mismo el umbral del 10 %.

Se precisó en el contrato la definición ya presente en el protocolo anterior: primer estado útil completo, no primer evento de una transición. Se conservan la redacción y evidencia históricas en Git y la explicación del ajuste en el informe. No se relajan umbrales según el resultado.

Se fijó el modo headless y se separaron los nombres de las sesiones frías. El segundo cambio evitó la reutilización inmediata del socket que había fallado. La pérdida de foco reapareció aun en headless, por lo que no se da por resuelta su causa. La conclusión de rendimiento se limita a las condiciones locales declaradas.

## Gate integral y seguridad de dependencias

La primera ejecución de `scripts/catastro_sii/validate_build.sh` pasó tipos, CSS, 132 pruebas Catastro, 52 Python sin omisiones y build Jekyll. Reportó además dos alertas moderadas correspondientes al mismo problema en `vitest` y `@vitest/mocker`. [Auditoría inicial](avaluos-ii-dependency-audit-20260911.json) y [log original](avaluos-ii-final-validation-20260911-before-vitest-patch.txt).

El [aviso oficial GHSA-82fw-gwwq-j7x9](https://github.com/vitest-dev/vitest/security/advisories/GHSA-82fw-gwwq-j7x9) identifica una lectura de archivos mediante redirects de mocks en determinadas configuraciones del servidor de desarrollo y señala 4.1.11 como versión corregida. La dependencia aquí es de desarrollo; no se observó explotación ni se atribuye una vulnerabilidad al sitio estático servido por Jekyll.

Se actualizó únicamente la familia Vitest de 4.1.10 a 4.1.11, conservando las dependencias de producción. `npm install` también quiso actualizar `@jridgewell/sourcemap-codec` de 1.5.5 a 1.6.0: la comprobación del alcance lo rechazó y se conservó 1.5.5 en el lockfile. El gate se repitió después de esa corrección, no se usa el resultado intermedio como validación del estado final.

| Comprobación final | Evidencia |
|---|---|
| Runtime fijado | Node 26.8.1, npm 11.19.0; archivo Node validado contra SHA oficial y usado temporalmente, sin instalación global |
| Python geoespacial | Entorno predial Python 3.12.13, `PROJ_DATA=/usr/share/proj`, PMTiles 3.7.0 cargado desde rueda temporal con SHA verificado |
| Gate de Catastro | [Log final](avaluos-ii-final-validation-20260911.txt): tipos, CSS, 132 pruebas TS, 52 Python y build |
| Dependencia compartida | Tres pruebas de Memoria Gobernada; total 135 pruebas Vitest entre ambas suites |
| Análisis | 53 pruebas de `v5_brecha` aprobadas en el entorno predial |
| Evaluador de rendimiento | 11 pruebas y rechazo real de sobrescritura de resultados existentes |
| Datos y mapas | `verify_fiscal_gap.py` aprobado: 346 filas, escenarios físicos, paridad de formatos y figuras, campos fiscales bloqueados preservados |
| Recursos editoriales | `verify_visual_assets.rb --strict`: 9 manifiestos, 99 assets y cero avisos |
| Auditoría npm posterior | [Resultado final](avaluos-ii-dependency-audit-20260911-after.json): cero vulnerabilidades reportadas; no equivale a una auditoría universal de seguridad |
| Alcance del parche | [Recibo de alcance y hashes](avaluos-ii-dependency-scope-20260911.json): ocho paquetes de la familia Vitest; los 16 archivos del bundle Catastro conservan idénticos SHA-256 |
| Preview final 4004 | [Comprobación desde el host](avaluos-ii-local-preview-20260911.json): portada, visor y ES/EN HTTP 200; cuatro assets coinciden con huella del HTML y fuente; PMTiles Range 206 |

Para repetir el gate completo:

```sh
NODE_HOME=/tmp/node-v26.8.1-linux-x64 PROJ_DATA=/usr/share/proj PYTHONPATH=/tmp/avaluos-pmtiles-qa-20260911/pmtiles-3.7.0-py3-none-any.whl PATH=/opt/entornos/catastros-sii-predial/bin:$PATH bash scripts/catastro_sii/validate_build.sh
PATH=/tmp/node-v26.8.1-linux-x64/bin:$PATH npm run test:memoria-gobernada
PATH=/tmp/node-v26.8.1-linux-x64/bin:$PATH npm audit --json
```

Los runtimes de `/tmp` son efímeros: deben recuperarse y verificar sus hashes si dejan de existir. No se autorizó el script de instalación opcional de `@parcel/watcher`; las pruebas y el build funcionaron sin él. Permanecen los avisos conocidos de Sass `@import` y tamaño de chunk MapLibre; no se ocultaron ni se cambió el límite del build para silenciarlos.

La comprobación previa al commit detectó espacios finales y líneas vacías al final de los logs del terminal. Se normalizaron sólo esos blancos en las copias versionadas; los originales se conservaron en `/tmp/*.txt.raw`. No se retiraron errores, avisos ni resultados.

## Límite del cierre

F9 se cierra para la implementación y validación local delimitadas. Los artículos ES/EN, imágenes y visor están preparados; F3/F4 monetarios siguen parciales. Falta suma neta y cantidad de roles habitacionales comunales 2026S1 compatibles, o un extracto con componentes separables y conciliación. No se cambia el estimando ni se sustituye el impuesto efectivo por una aplicación incompleta de tasas.

La solicitud está redactada, pero no enviada; no existe una respuesta institucional pendiente. El diseño de post III CCU está completo dentro del alcance aprobado y su ejecución es futura. Se conserva el servidor Jekyll 4004; se retiran solamente sesiones y ruta temporal del ensayo.
