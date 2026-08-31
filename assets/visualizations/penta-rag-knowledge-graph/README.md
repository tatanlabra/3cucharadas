# Proyección pública del RAG de penta-agent

`index.html` y el JSON hermano se generan localmente desde la fuente versionada
en `scripts/penta_rag_graph/` del repositorio del sitio. La fuente canónica son
las lecciones y eventos locales de `penta-agent`; Qdrant aporta las vecindades
semánticas como índice derivado.

Esta exportación fue generada el 2026-08-29. El visor comienza con ocho familias
deterministas de tipo de trabajo —coordinación, investigación, verificación y
otras— derivadas de estrategia, herramienta, transporte y proyecto. Son una ayuda
de lectura pública y revisable: no sustituyen el dato canónico ni infieren rasgos
de una persona.

Es una proyección pública: elimina rutas absolutas, no contiene cuerpos de correo,
adjuntos, direcciones de correo, tokens ni credenciales. Antes de reemplazarla se
debe regenerar, ejecutar el escáner de secretos y comprobar que el HTML y JSON
provienen de la misma corrida.

No editar el HTML ni el JSON a mano: corregir o extender el generador y volver a
exportar. Una actualización de corte usa `build_graph.py --sanitize`; el visor
usa una copia local vendorizada de `3d-force-graph` 1.80.0;
no carga un CDN ni consulta Qdrant desde el navegador. Para cambios sólo de
plantilla, `build_graph.py --render-public` vuelve a generar el HTML desde el
JSON público ya saneado, sin releer el índice. `build_graph.py --check-public`
falla si el HTML ya publicado no corresponde exactamente a ese JSON, plantilla
y vendor versionados.
