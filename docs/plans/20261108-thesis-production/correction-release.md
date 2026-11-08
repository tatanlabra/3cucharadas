# Corrección III–IV: registro de entrega

Estado: en validación; publicación correctiva pendiente.

- Párrafos justificados en artículos y anexos ES/EN, con separación silábica automática; listas conservan su composición.
- Figura 1 de IV ocupa el ancho de lectura disponible. Generador y Playwright comprueban etiquetas, intervalos, barras, líneas y marcos; fallos inducidos demuestran que los detectores rechazan cruces.
- IV abre con las 14 cohortes de 2009–2022. Los modelos detallados siguen delimitados a 2016–2019; no se recalculó ni extrapoló su evidencia.
- Revisión ES/EN conserva límites inferenciales, denominadores y cautelas. El diseño posterior al piloto no se presenta como prerregistro independiente. La agregación por expuestos no se atribuye a un estimador que el productor no implementa.
- PDF local regenerado desde fuente, anexo y figuras; no se envía ni se inventa un enlace público.

## Evidencia y límites

Los resultados anteriores al commit correctivo son históricos. `evidence/figure-correction/` conserva tanto fallos como pases; `claude-correction/` y `claude-editorial-complete/` conservan los primeros dictámenes REQUEST_CHANGES. Las revisiones posteriores deben aprobar los archivos con hashes vigentes antes del push.

La matriz visual cubre ocho rutas, dos temas y cuatro anchos. No prueba todas las combinaciones de navegador, plataforma o zoom; capturas y revisión humana complementan la geometría automática. El aviso científico upstream `UNCOMMITTED_FILE_HASHES` de III se conserva y no se redefine como un error de esta entrega.

## Publicación y reversibilidad

Push explícito a GitLab y GitHub, sin force ni omisión de hooks. CI y Pages deben corresponder al SHA entregado. Contrastar DOM de ocho rutas y bytes de los activos contra el artefacto de ese CI; repetir Playwright público.

Si aparece una regresión, mantener abierto el tablero y corregir mediante un nuevo commit. No sobrescribir historia remota. Difusión y sindicación permanecen pendientes; todos los commits de esta entrega llevan `3c-release: diffusion-deferred`.
