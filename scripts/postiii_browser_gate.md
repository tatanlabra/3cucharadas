# Gate de navegador humano — Post III y visor 3D

Este protocolo es una compuerta de publicación, no una lista decorativa. Sólo se
puede marcar **PASS** si cada observación requerida se hizo en el navegador y
versión indicados. Un navegador más nuevo, una simulación o una captura de Chrome
no sustituyen Safari 16 ni Firefox 104.

## Precondiciones automatizables

Desde `activos/3cucharadas`, ejecutar antes de abrir un navegador objetivo:

```sh
/opt/entornos/mamba312/bin/python scripts/penta_rag_graph/build_graph.py --check-public
node scripts/postiii_browser_gate.mjs
node scripts/postiii_browser_gate.mjs --probe
node scripts/postiii_browser_gate.mjs --probe-webgl-fallback
```

Los cuatro comandos deben devolver únicamente `PASS` o `[ok]`. El primero prueba que
el HTML y JSON publicados corresponden exactamente a la plantilla y vendor versionados,
sin leer Qdrant ni fuentes privadas. Los dos últimos limitan la prueba a
`http://127.0.0.1:4004`; si el preview no está activo, fallan. `--probe-webgl-fallback`
anula WebGL sólo en Chromium local y exige el resumen directo del visor: título, cuatro
métricas y las ocho familias. Es una regresión automatizable, no evidencia para Safari 16
ni Firefox 104. Para el control
automatizado de Chromium, esperar la carga completa antes de ejecutar Axe:

```sh
agent-browser --session postiii-gate open http://127.0.0.1:4004/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/ --headless
agent-browser --session postiii-gate wait --load networkidle
agent-browser --session postiii-gate a11y --tags wcag2a,wcag2aa
agent-browser --session postiii-gate open http://127.0.0.1:4004/assets/visualizations/penta-rag-knowledge-graph/ --headless
agent-browser --session postiii-gate wait --load networkidle
agent-browser --session postiii-gate a11y --tags wcag2a,wcag2aa
agent-browser --session postiii-gate close
```

Una auditoría antes de `networkidle` no es evidencia: puede informar contraste
contra una hoja de estilos aún no cargada. Axe incompleto no es PASS automático;
anotar selector y motivo de cada resultado `incomplete`.

## Gate humano por plataforma

Abrir las dos rutas siguientes, primero a 1280 px de ancho y luego a 390 px:

| Navegador exigido | Ruta | Observación que debe quedar registrada | Fallo que bloquea publicación |
| --- | --- | --- | --- |
| Safari **16.x** real | Post III | Título «Multiagentes en 3 cucharadas III», las tres cucharadas, el enlace «Abrir visor completo», el `iframe` titulado y la Tabla 1 textual son legibles. | Safari distinto de 16.x; iframe ausente; tabla alternativa ausente o ilegible. |
| Safari **16.x** real | Visor | Si WebGL inicia, se ve el grafo, los paneles no tapan toda la escena y las pestañas Tareas/Proy responden. Elegir «Probar y verificar» cambia el filtro de tipo de tarea y aparece «Ver todos los tipos de tarea». Si WebGL no inicia, aparece «La proyección 3D no pudo iniciarse», cuatro métricas y las ocho familias. | Lienzo vacío sin fallback; lista de tareas vacía cuando WebGL existe; filtro no cambia; fallback sin métricas o familias. |
| Firefox **104.x** real | Post III | El contenido y la tabla alternativa siguen disponibles sin interpretar el grafo; el botón de abrir visor anuncia nueva pestaña. | Firefox distinto de 104.x; información sólo visible en el canvas; enlace o iframe no identificable. |
| Firefox **104.x** real | Visor | Si WebGL inicia, Tareas muestra categorías con descripción, Proy muestra proyectos y reset devuelve el filtro a «Todas». Si no inicia, aparece el fallback directo con título, métricas y ocho familias. | Grafo/paneles vacíos; categorías sin texto; pestañas o reset sin respuesta; fallback ausente o incompleto. |
| Ambos | Post y visor | Con teclado, el foco visible llega al enlace, controles, pestañas, categoría elegida y reset. La lectura guiada y la Tabla 1 explican que similitud no es causalidad y que correo/tesis no son nodos de contenido. | Foco invisible o atrapado; controles no activables; límites/procedencia no accesibles fuera del canvas. |

## Alternativa textual y WebGL

La alternativa aprobada combina **la Tabla 1 del Post III**, la lectura guiada,
la exportación JSON y el fallback directo del visor. Al simular WebGL ausente en
Chromium, el visor debe reemplazar el lienzo por «La proyección 3D no pudo
iniciarse», cuatro métricas y ocho familias legibles. Esa simulación detecta
regresiones locales, pero no reemplaza Safari 16 ni Firefox 104.

Si un navegador objetivo no soporta o no inicia WebGL, el fallback completo es
la condición mínima para que el visor siga siendo legible. Aun así se registra
como fallback, no como prueba de compatibilidad del grafo 3D en esa plataforma.

## Registro mínimo de evidencia

Anotar en el handoff o revisión editorial: fecha/hora, sistema operativo,
navegador y versión exacta, las dos URLs, viewport, PASS/FAIL por fila, rutas de
capturas y cualquier `incomplete` de Axe. Si falta una fila, la compuerta queda
`[ghost]` por plataforma o revisión humana, no «aprobada parcialmente».
