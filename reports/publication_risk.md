# Gate de publicación cartográfica

## Estado inicial

`LEGAL_PUBLICATION_STATUS=PENDING`.

Un PMTiles es descargable: ocultar atributos en un popup no los protege. Mientras
el gate no sea exactamente `AUTHORIZED_VECTOR`, el pipeline no construye una entrega
publicable ni puede ejecutar una subida a R2 de predios.

## Controles obligatorios

1. Lista permitida de atributos aplicada antes de teselar y verificada desde los
   metadatos PMTiles.
2. Sin RUN, roles, propietarios, direcciones, folios, clientes, IDs fuente, valores
   exactos, superficies exactas ni vínculos con otros registros.
3. Fuente inmutable: cualquier reparación se rechaza en vez de escribirse sobre el
   GeoParquet maestro. Las validaciones se ejecutan sobre una copia de trabajo.
4. Polígonos presentados como cartografía referencial; nunca como deslindes o dominio.
5. R2 exige CORS para `Range`, expone `Content-Range` y se verifica con una petición
   `206` desde el origen del sitio.
6. Los artefactos se versionan. Un manifest anterior permanece como rollback.

## Riesgos abiertos

- Habilitación de redistribución vectorial SII: pendiente de decisión jurídica.
- `stata01`: sin proyecto, datos ni toolchain de teselación durante este diagnóstico.
- Cloudflare R2: sin bucket, endpoint, dominio ni política CORS verificables desde el
  repositorio; no se usan credenciales ni se realiza upload.
