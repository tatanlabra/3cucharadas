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
cod_region, cod_comuna, destino_clase, calidad_geometrica, version_datos,
predio, avaluo_fiscal_clp, geometry
```

`predio` es el número de predio de la fuente y `avaluo_fiscal_clp` proviene sólo
de `dc_avaluo_fiscal`, normalizado como entero CLP. Se excluyen explícitamente
`rol`, `rol_key`, manzana, dirección, propietario, superficie, contribuciones,
`valorTotal` y cualquier otro atributo fuente. La geometría se lee como fuente
inmutable: las geometrías `null` o vacías se cuentan y se excluyen sólo de la
derivación; una geometría no vacía inválida detiene el build y nunca se aplica
`MakeValid`.

La capa comunal usa DPA 2023 y métricas agregadas. Los PMTiles de preview local
están ignorados por Git y se sirven sólo desde `localhost`; el manifest versionado
de producción continúa sin exponer la capa predial hasta que la entrega se
promueva explícitamente.

## Alcance de la Resolución 8656 y estado de entrega

- **HECHO.** La [Resolución Exenta N° 8656 del
  SII](https://www.sii.cl/documentos/resoluciones/1999/r865699.htm) describe la
  tarifa de venta de información por el SII en 1999 y condiciona **esa venta**
  a una carta compromiso; no declara una prohibición general para toda
  reutilización de información catastral pública.
- **HECHO.** El SII mantiene una [Cartografía Digital](https://www.sii.cl/destacados/impuesto_territorial/)
  que exhibe espacialmente rol, destino y avalúos. El usuario declara que las
  fuentes de este proyecto son públicas, que la Resolución 8656 no rige su
  adquisición y autoriza su uso en 3 Cucharadas.
- **INFERENCIA OPERATIVA.** Con esa determinación del titular del proyecto y
  sin atributos de personas, la Resolución 8656 no es un bloqueo técnico para
  el piloto; el sitio conserva atribución SII, evita afirmar deslindes o dominio
  y mantiene la derivación mínima verificable.
- **NO VERIFICADO.** Esta nota no sustituye una opinión jurídica sobre la
  distribución masiva de cualquier archivo histórico ni afirma que la
  visualización SII equivalga a una licencia general. El `PENDING` actual es un
  estado de despliegue: faltan bucket R2, CORS/Range y promoción explícita del
  manifest, no una prohibición inferida desde la Resolución 8656.
