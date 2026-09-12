# Universo predial de Avalúos II

Revisión de solo lectura del 2026-09-12, solicitada por el autor y contrastada por
un subagente con el código y los agregados actuales. No se repitió la extracción
completa ni se consultaron nuevos catastros oficiales.

- El conteo usa todos los registros del extracto cuyo `trim(dc_cod_destino)='H'`; no exige polígono ni coordenadas.
- `../catastros_sii/v5_brecha/scripts/build_fiscal_gap.py:126` aplica ese filtro; las líneas 127–137 cuentan filas y claves administrativas y contabilizan coordenadas ausentes por separado.
- `catastro_sii_brecha/data/fiscal-gap/audit.json` registra 6.054.808 filas y 6.054.808 claves únicas, sin claves incompletas.
- Valparaíso: 99.453 registros, 96.560 con geometría suministrada y 2.893 sin ella; solo 53.714 geometrías únicas. Fuente: `catastro_sii_brecha/data/fiscal-gap/maps-audit.json:19`.
- Contar polígonos únicos subestimaría los roles: varios registros pueden compartir geometría. El render filtra y deduplica geometrías después de comprobar el total administrativo.
- Coordenadas nulas y geometría ausente son métricas diferentes; no intercambiar sus conteos.

## Cortes y límites

El panel histórico conserva 5.985.969 registros del extracto `v46_20260627` y el
diagnóstico fiscal usa 6.054.808 de `v2026s1_20260724`. El manifiesto declara ambos
cortes (`catastro_sii_brecha/data/manifest.json:32` y `:37`); conservar el histórico
es explícito en `scripts/catastro_sii/project_fiscal_gap.py:4`. La diferencia de
68.839 registros no prueba un problema de polígonos ni una causa administrativa.

Se trata del espejo catastral disponible, no de todos los destinos del SII ni del
catastro oficial plenamente conciliado. Antártica y Trehuaco siguen sin extracto;
el post conserva las diferencias frente a los controles SII/MINVU. Este hallazgo
no elimina los supuestos de comparabilidad de vivienda, sitio y rol.
