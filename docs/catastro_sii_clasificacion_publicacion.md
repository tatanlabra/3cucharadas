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

## Evidencia de redistribución a resolver antes del vector predial

- **HECHO.** La [Resolución Exenta N° 8656 del
  SII](https://www.sii.cl/documentos/resoluciones/1999/r865699.htm) describe la
  venta de la Base de Datos Catastro y señala que toda venta se acompaña de una
  carta compromiso que prohíbe traspasar o vender esa información a terceros.
  También indica que la base no contiene nombre ni RUT de propietarios.
- **INFERENCIA OPERATIVA.** Si las fuentes de este piloto se obtuvieron bajo
  esa modalidad o una condición equivalente, publicar PMTiles que preservan
  geometrías prediales individualizadas requeriría una autorización expresa de
  redistribución; la reducción de atributos no sustituye ese permiso.
- **NO VERIFICADO.** Aún no se ha incorporado el documento de adquisición de
  estas fuentes ni una autorización posterior del SII que permita el vector
  derivado. Tampoco se declara aquí que la resolución de 1999 sea la única
  norma aplicable o que continúe sin modificaciones.

Por tanto, se mantiene `PENDING` para el vector predial público. Para levantar
el gate se requiere conservar, junto al run de publicación, la evidencia de la
modalidad de adquisición y una autorización escrita aplicable a esta
redistribución. La capa comunal agregada y el basemap OSM se evalúan por sus
propios términos, separados de este gate.
