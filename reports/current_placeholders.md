# Contrato de placeholders preservados

Este inventario se tomó de `catastro_sii_brecha/index.html` antes de integrar Vite.
Los selectores, las métricas y los textos existentes son parte de la interfaz pública
y no se reemplazan.

| Elemento actual | IDs o clases | Estado tras la integración |
| --- | --- | --- |
| Selector territorial | `#region`, `#comuna`, `#status`, `#selection-context` | Mantener marcado y etiquetas; sincronizar con URL, capa comunal y encuadre. |
| Interruptor predial | `#parcel-layer`, `#parcel-layer-note` | Mantenerlo; se habilita únicamente con región piloto seleccionada, zoom suficiente, manifest válido y gate legal autorizado. |
| Mapa | `#map`, `#density`, `#map-note`, `#map-status` | El canvas se conserva como fallback agregado; MapLibre se monta en `#map` sin eliminarlo. |
| Métricas | `#coverage`, `#population`, `#records`, `#coordinates`, `#surface`, `#assessment`, `#historical`, `#casen` | Conservan fuente `comunas.json`/Parquet y formato actual. No se duplican cifras en TypeScript. |
| Resumen nacional | `#national-records`, `#national-communes`, `#national-coordinate-coverage` | Se mantiene y actualiza desde el mismo catálogo comunal. |
| Hallazgo y cautelas | `#finding`, bloques metodológicos y de fuentes | Se preservan textualmente; se agregan avisos cartográficos sin reescribir la metodología existente. |
| Tema y accesibilidad | `#theme-toggle`, `.skip-link`, `role=status`, `aria-live` | Se preservan; MapLibre incorpora controles con nombre accesible y no es la única vía de lectura. |

## Contenido que no se toca

- Hero, marca, CTA, disclaimer, cards, tipografías, paleta neón y modo claro/oscuro.
- Descarga pública de métricas agregadas y `metodologia.html`.
- La representación nacional de celdas agregadas como fallback.
- La regla explícita: cobertura residencial equivalente no es población residente ni
  una explicación causal.
