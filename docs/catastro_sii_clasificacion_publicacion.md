# Clasificación de publicación — Catastro SII

Última revisión: 2026-07-18 UTC.

## Decisión operativa vigente

El usuario declara que este proyecto y los datos Catastro SII usados aquí no
contienen datos privados que requieran resguardo. Por ello `stata01` se utiliza
para procesar y obtener artefactos, y los PMTiles necesarios se migran a la
laptop para revisión cartográfica local antes de un despliegue en 3 Cucharadas.

Esta decisión no convierte los artefactos locales en publicados: una revisión de
licencia o permiso de redistribución es distinta de la privacidad. Tampoco cambia
los invariantes técnicos: no se copia GeoParquet completo al sitio, no se publica
GeoJSON predial completo y la geometría fuente no se repara ni se modifica.

## Esquema fuente auditado (nombres, sin valores)

Las dos fuentes piloto contienen identificadores prediales (`rol`, `comuna`,
`manzana`, `predio`, `predioPublicado_*`, `dc_bc*`, `dc_padre*`), direcciones o
ubicación (`direccion_sii`, `dc_direccion`, `ubicacion`), valores tributarios o
comerciales (`valor*`, `dc_avaluo_*`, `dc_contribucion_semestral`) y características
constructivas. No se observó una columna de nombre o RUT de personas. Esta es una
auditoría de nombres de columnas; no sustituye una revisión jurídica o de licencia.

## Contrato de la derivación web

La capa predial de Atacama conserva únicamente:

```text
cod_region, cod_comuna, destino_clase, calidad_geometrica, version_datos, geometry
```

Los identificadores, direcciones, avalúos, contribuciones y demás columnas de la
fuente no se copian. La geometría se lee como fuente inmutable: las geometrías
`null` o vacías se cuentan y se excluyen sólo de la derivación; una geometría no
vacía inválida detiene el build y nunca se aplica `MakeValid`.

La capa comunal usa DPA 2023 y métricas agregadas. Los PMTiles de preview local
están ignorados por Git y se sirven sólo desde `localhost`; el manifest versionado
de producción continúa sin exponer la capa predial hasta que la entrega se
promueva explícitamente.
