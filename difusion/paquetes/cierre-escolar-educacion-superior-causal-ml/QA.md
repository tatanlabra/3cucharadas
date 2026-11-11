# QA y límites

- Fuente ES leída íntegramente; copy nuevo derivado de revisión científica vigente. Coherencia numérica con corpus ES/EN + anexos: PASS. Esta comprobación no demuestra por sí sola equivalencia semántica.
- HTML público cotejado en reclamo principal, contrastes, intervalos y nota de corrección.
- Mastodon ES/EN editado y Bluesky ES/EN aclarado por decisión humana. Cuatro textos comprobados por API pública.
- Spotify: el autor reemplazó archivo conservando URL; SHA del enclosure público idéntico al archivo final de distribución. No se escuchó ni transcribió integralmente el contenido; no se afirma auditoría científica del audio.
- LinkedIn: copy preparado; carrusel en espera de decisión tecnológica de otra sesión, sin intervención en sus archivos.
- X: 3 bloques, 246/237/210 caracteres contando URL como 23. No enviados.
- Medium: adaptación EN local; requiere fijar canónico EN y comprobar tras publicación. Guía consultada: https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium.
- Reddit: reglas del destino pendientes, sin formulario abierto ni envío.
- DEV.to/HN: excluidos por decisión del autor en grill-me.
- Chequeo anterior fallaba al incluir dos carruseles históricos; corregida selección para excluir solo difusion/historico/. Dos pruebas fallaron antes del cambio; paquete activo obsoleto sigue siendo rechazado. Suite: 32 pruebas, 106 aserciones, 0 fallos.
- Evidencia y límites de release: docs/plans/20261110-difusion-iv-audio-iii-iv/ESTADO.md.
