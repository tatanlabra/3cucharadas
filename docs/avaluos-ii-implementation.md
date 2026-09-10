# Avalúos II — índice de entrega local

Estado: implementación diagnóstica validada; objetivo fiscal parcial por falta de contribución neta habitacional 2026S1 conciliada. No publicado.

| Entregable | Archivo |
|---|---|
| Borrador español | [_drafts/avaluos-ii-brecha-residencial.md](../_drafts/avaluos-ii-brecha-residencial.md) |
| Borrador inglés | [_drafts/avaluos-ii-brecha-residencial-en.md](../_drafts/avaluos-ii-brecha-residencial-en.md) |
| Visor único | [catastro_sii_brecha/index.html](../catastro_sii_brecha/index.html), sección `#brecha-contribuciones` |
| Figura ES compartible | [SVG](../assets/images/avaluos-ii/gap-top15-es.svg) y [PNG](../assets/images/avaluos-ii/gap-top15-es.png), diagnóstico físico con fuentes y límites |
| Datos | [Parquet](../catastro_sii_brecha/data/fiscal-gap/communes.parquet), [CSV](../catastro_sii_brecha/data/fiscal-gap/communes.csv), [JSON](../catastro_sii_brecha/data/fiscal-gap/communes.json) |
| Conciliación oficial adicional | [source-audit.json](../catastro_sii_brecha/data/fiscal-gap/source-audit.json), 18 fuentes SII/MINVU congeladas en el repositorio analítico |
| Método público y errata | [method.md](../catastro_sii_brecha/data/fiscal-gap/method.md) |
| Contrato / TODO_STATE | [avaluos-ii-contract.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-contract.md) |
| Auditoría deductiva, inductiva y abductiva | [avaluos-ii-audit.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-audit.md) |
| Evidencia y limitaciones de QA | [avaluos-ii-validation.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-validation.md) |
| Solicitud de datos preparada, no enviada | [avaluos-ii-solicitud-datos.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-solicitud-datos.md) |
| Diseño de post III CCU, sin ejecución | [avaluos-iii-ccu-protocol.md](../../catastros_sii/v5_brecha/docs/avaluos-iii-ccu-protocol.md) |

La tabla registra 346 comunas, 344 con fuente 2026S1 y 6.054.808 H únicos. En la primera validación del 09-09 los controles pasaron 184 pruebas; siete pruebas geoespaciales se omitieron por dependencia del entorno remoto, sin reconstrucción de PMTiles. Hay builds locales de preview y producción; ambos borradores quedan fuera de la producción normal.

Para reabrir el preview con Node 26.8.1 y el bundle Ruby del proyecto:

```sh
npm run build:catastro
JEKYLL_ENV=production bundle exec jekyll build --drafts --unpublished -d /tmp/avaluos-ii-preview
node scripts/catastro_sii/serve_range_static.mjs /tmp/avaluos-ii-preview 4018 127.0.0.1 .
```

El servidor y las sesiones de QA de esta ejecución se cierran al terminar. No se requiere una aprobación pendiente para el trabajo ya realizado; obtener la fuente tributaria es la dependencia que impide cerrar el ranking monetario.

Actualización 10-09-2026: dos planillas MINVU concilian en 346 comunas y resuelven el control agregado de Trehuaco (1.342 H) y Antártica (0). El total MINVU supera en 1.799 al cuadro SII; hay 208 diferencias positivas entre comunas cubiertas por el espejo. Los 16 CSV comunales SII vigentes sí son 2026S1, pero su neto es no agrícola, no exclusivamente H. Cinco pruebas nuevas validan la conciliación y sus rechazos; 32 pruebas v5 aprobadas. No se declara terminado el ranking monetario.
