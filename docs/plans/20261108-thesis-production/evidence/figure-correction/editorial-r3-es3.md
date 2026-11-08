# Corrección editorial r3 — Post y anexo III ES

Dictamen de entrada: `docs/plans/20261108-thesis-production/evidence/claude-editorial-r2/result.md` (`REQUEST_CHANGES`). Alcance de este recibo: solo fuentes ES de III; EN y IV tienen otros escritores. Fuente congelada para rebuild: post SHA-256 `5672354531cf876374e29f883177a539759627e5813ac88143f9d9e935f0d1fd`; anexo SHA-256 `da1c8c48eec2f5fe0b5ecd692c985632c857e1b599c981536b791d59bcb1893f`.

| Hallazgo | Corrección | Evidencia de fuente |
|---|---|---|
| Atribución al estimador Callaway y Sant’Anna | Anexo `:161` dice «+9,11 puntos ponderados por expuestos»; tabla A4 `:110` ya usa la misma etiqueta. | `compute_full_series_2004_2025.py:432–433` define exclusiones de controles; no prueba implementación exacta del estimador publicado. |
| Momento de especificación 2016–2019 | Post `:101` y anexo `:126,:221` dicen piloto solapado observado, especificación anterior a ejecución v3 completa y ausencia de prerregistro independiente. Se retiró «antes de mirar la serie completa». | `research/post3/confirmatory_design_v3.yaml:1–29`: `specified_after_pilot_before_full_v3_execution`, `independent_preregistration: false`. |
| Universo de controles | Post `:86` y anexo `:96` describen escuelas sin cierre registrado en el universo del cálculo, exclusión de estudiantes expuestos alguna vez, contraste por cohorte y agregación; Callaway/Sun/Roth quedan como literatura de diseño, no sello del estimador ejecutado. | `research/post3/agy_full_series_v1/compute_full_series_2004_2025.py:350–358,378–433`. |
| Unidad de conteo | Post `:75` y anexo `:39` aclaran que 78.972/734.472 son observaciones estudiante-cohorte, no necesariamente personas distintas. | Denominadores de tabla A1 y 20 cohortes de tabla A4; cifras intactas. |
| Nota jurídica | Post `:136` conserva la referencia Castro Paredes como contexto sobre cierre voluntario; elimina la afirmación no verificada de que la nota del anexo acredita trámite con mera información de alternativas. | El anexo `#certeza-documental-y-regla-empirica` documenta el artículo 27 sobre actas, no ese hecho. No se abrió el PDF de la BCN ni se inventó una página. |
| Límite del pareo | Anexo `:151` explicita que el equilibrio en variables registradas no prueba equilibrio en no observables ni trayectorias paralelas. | Alineado con anexo EN `:156` y diagnóstico basal tabla A3. |
| Analogías ELI5 | Anexo `:146,:151` sustituye «sala de reuniones» y «dos películas» por tamaño efectivo y método en prosa directa. | 21,1/21,9/17,7 episodios efectivos intactos. |

Verificación de fuente:

| Comando | Exit | Resultado |
|---|---:|---|
| `ruby scripts/verify_thesis_post3.rb --lang es` | 0 | `POST3_VALID lang=es`; aviso de custodia upstream `UNCOMMITTED_FILE_HASHES` |
| `git diff --check` | 0 | Sin errores de formato |
| `rg -n 'en Callaway y Sant|antes de mirar|dos películas|sala de reuniones|controles de establecimientos aún abiertos' _posts/2026-10-23-costos-cierre-escolar-trayectorias.md _pages/tesis-post3-anexo-metodologico.md` | 1 | Ninguna formulación obsoleta encontrada |

Los recibos de navegador local r2 preceden esta corrección textual y no acreditan el artefacto r3. Tras el build r3 fresco en `/tmp/codex-thesis-production-site`, servido en `http://127.0.0.1:4005`, se repitió la matriz funcional completa:

| Comando | Exit | Resultado |
|---|---:|---|
| `node scripts/verify_thesis_post3_browser.mjs --base-url http://127.0.0.1:4005 --artifact-root /tmp/codex-thesis-production-site --summary --receipt docs/plans/20261108-thesis-production/evidence/figure-correction/r3-post3-browser-local.json` | 0 | 32/32 filas; noJS/print y CSS PASS; manifiesto III 77/77, SHA `3c207de3c56f23c5d83874edd78a6fdc3b353ce81333baec8b389ca6ce42b4bd` |
| `node scripts/verify_thesis_post4_browser.mjs --base-url http://127.0.0.1:4005 --artifact-root /tmp/codex-thesis-production-site --summary --receipt docs/plans/20261108-thesis-production/evidence/figure-correction/r3-post4-browser-local.json` | 0 | 32/32 filas; noJS/print y CSS PASS; manifiesto IV 51/51, SHA `a29020d552c24eb42bff845dc090629befd86e7bd06a728d492493a543e972d8` |

La QA pública sigue pendiente del nuevo SHA desplegado y del artefacto CI concordante.
