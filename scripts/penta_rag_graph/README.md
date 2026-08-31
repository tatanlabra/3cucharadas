# Fuente reproducible del visor de memoria gobernada

Este directorio contiene la fuente versionada del artefacto público ubicado en
`assets/visualizations/penta-rag-knowledge-graph/` y su JSON compañero. No es
una segunda memoria: la fuente canónica sigue siendo `penta-agent` y Qdrant es
un índice derivado local.

## Material versionado

- `build_graph.py`: derivación, saneamiento y renderizado.
- `rag-graph.template.html`: interfaz, fallback sin WebGL y explicaciones.
- `vendor/3d-force-graph.min.js`: `3d-force-graph` 1.80.0, vendorizado para no
  requerir CDN ni llamadas del navegador.
- `LICENSE-3d-force-graph.txt`: licencia MIT del componente vendorizado.

## Operación segura por defecto

Desde la raíz de `3cucharadas`, comprobar que el HTML publicado puede obtenerse
exactamente del JSON ya saneado, la plantilla y el vendor versionados:

```sh
PY=/opt/entornos/mamba312/bin/python
$PY scripts/penta_rag_graph/build_graph.py --check-public
```

Para reescribir sólo el HTML desde el mismo JSON público:

```sh
$PY scripts/penta_rag_graph/build_graph.py --render-public
```

Estos dos modos no leen Qdrant, correo, tesis ni la memoria canónica.

## Regeneración deliberada

Sólo para producir un nuevo corte público y con autorización para leer las
fuentes locales, ejecutar:

```sh
$PY scripts/penta_rag_graph/build_graph.py --sanitize
```

Ese modo lee `penta-agent/memory/experience-lessons.yaml`, el ledger de eventos
y el índice Qdrant local. Escribe únicamente `public-graph.json` e `index.html`
del sitio; no produce exportaciones privadas ni llama proveedores externos.
Antes de aceptar el nuevo corte, ejecutar el escáner sobre los dos artefactos,
`--check-public`, el gate del Post III y el build Jekyll. No editar HTML o JSON
a mano: se corrige esta fuente y se vuelve a generar.

## Límites de publicación

- El visor es una proyección de estrategias y evidencia operativa, no un mapa
  de personas, identidad, preferencias o relaciones causales.
- Correo y tesis no se exportan como contenido del grafo.
- La matriz Safari 16.x y Firefox 104.x sigue siendo humana; ver
  `scripts/postiii_browser_gate.md`.
