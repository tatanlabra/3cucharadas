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
| Resumen y avance de la sesión | [avaluos-ii-todo.md](avaluos-ii-todo.md), derivado de los contratos principal y F8–F11 |
| Ajustes del visor y evidencia vigente | [Contrato F9](avaluos-ii-polish-contract.yaml), [evidencia](avaluos-ii-polish-evidence.md) |
| Base revisada, ES/EN y fecha | [Contrato F10](avaluos-ii-editorial-consolidation-contract.yaml), [evidencia editorial](avaluos-ii-editorial-consolidation-evidence.md) |
| Hero, teaser y diagnóstico imagegen | [Contrato F11](avaluos-ii-visual-editorial-contract.yaml), [diagnóstico](avaluos-ii-imagegen-diagnosis-20260911.md) |
| Cierre integral y rendimiento | [Pruebas finales](avaluos-ii-final-closeout-20260911.md), [ensayo emparejado](catastro-paired-loading-20260911-focus.md) |
| Auditoría deductiva, inductiva y abductiva | [avaluos-ii-audit.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-audit.md) |
| Evidencia y limitaciones de QA | [avaluos-ii-validation.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-validation.md) |
| Solicitud de datos preparada, no enviada | [avaluos-ii-solicitud-datos.md](../../catastros_sii/v5_brecha/docs/avaluos-ii-solicitud-datos.md) |
| Diseño de post III CCU, sin ejecución | [avaluos-iii-ccu-protocol.md](../../catastros_sii/v5_brecha/docs/avaluos-iii-ccu-protocol.md) |

La tabla registra 346 comunas, 344 con fuente 2026S1 y 6.054.808 roles habitacionales únicos. La verificación final combina 132 pruebas TS Catastro y tres de Memoria Gobernada, 53 analíticas y 52 Python del visor, sin omisiones. Vitest se corrigió a 4.1.11 y npm audit terminó sin vulnerabilidades reportadas. El mapa útil frío mejoró 20,43% en el ensayo local emparejado; no se extrapola a percentiles de producción. No se reconstruyeron PMTiles nacionales. Ambos borradores quedan fuera de la producción normal. El detalle de entornos, comandos y límites está en el cierre final; los resultados anteriores se conservan como historia.

El preview solicitado permanece en <http://127.0.0.1:4004/catastro_sii_brecha/>. Se comprobó HTTP 200 desde el host; un fallo de acceso desde el sandbox no prueba que el servidor haya caído. No iniciar otro servidor si 4004 ya responde. Para reconstruir los borradores con Node 26.8.1 y el bundle Ruby del proyecto:

```sh
npm run build:catastro
JEKYLL_ENV=production bundle exec jekyll build --drafts --unpublished -d /tmp/avaluos-ii-preview
```

Las sesiones temporales de QA se cierran al terminar; el servidor Jekyll 4004 se conserva por petición del usuario. No hay una aprobación pendiente para el trabajo local autorizado. Obtener la fuente tributaria compatible impide cerrar el ranking monetario; la solicitud preparada no ha sido enviada.

Antecedente del 10-09-2026: dos planillas MINVU concilian en 346 comunas y resuelven el control agregado de Trehuaco (1.342 roles habitacionales) y Antártica (0). El total MINVU supera en 1.799 al cuadro SII; hay 208 diferencias positivas entre comunas cubiertas por el espejo. Los 16 CSV comunales SII vigentes sí son 2026S1, pero su neto es no agrícola, no exclusivamente habitacional. Ese corte pasó 32 pruebas v5; el corte posterior pasó 53. No se declara terminado el ranking monetario.
