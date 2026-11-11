# Educación III · carrusel LinkedIn nativo

Selección delegada por el autor: HTML/CSS + Chromium. Nueve láminas, texto seleccionable, fuentes Fira Sans incrustadas y gráficos SVG. Mejor compromiso local por reutilización del flujo web y control editorial; no superioridad universal sobre Typst, Beamer o Scribus. Piloto y comparación: `difusion/pilotos/educacion-iii-motores/`.

Desde la raíz de 3cucharadas:

```bash
python3 scripts/render_linkedin_native.py --content difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/content.json --output difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/out --filename educacion-iii-linkedin.pdf
python3 scripts/render_linkedin_native.py --content difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/content.json --output difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/out --filename educacion-iii-linkedin.pdf --verify-only
python3 scripts/probe_linkedin_native.py --content difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/content.json --pdf difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/out/educacion-iii-linkedin.pdf --output difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/out/probes
```

Salida: `out/educacion-iii-linkedin.pdf`. `out/build.json` conserva hashes de inputs y PDF; `out/qa.json` contenido, fuentes y enlaces; `out/layout.json` desbordes; `out/probes/summary.json` falsación; `out/visual-review.json` revisión visual del hash entregado. Generador conserva el PDF anterior si falla: comprobar código y recibo.

Editar contenido en `content.json`, diseño en `scripts/linkedin_native/template.py`. La fuente científica está congelada en `source-lock.json`: revisar cambios y significado antes de renovar hashes. Una coincidencia literal no valida causalidad ni población. El enlace usa campaña `tesis_post3`.

Conserva eras documentales separadas, límites de identificación, diferencia entre registro y escolarización real, intervalos y poblaciones distintas. El indicador previo no ajusta el contraste principal; las cotas no son intervalos de confianza. No se presenta asociación como efecto causal.

Revisión final 2026-11-10: páginas 1–9 individualmente y vistas a 390 px; sin cortes ni solapamientos observados. Los pies son secundarios y pequeños a tamaño móvil; no se ocultan en ellos las conclusiones principales. El PDF etiquetado no equivale a certificación PDF/UA. QA geométrico no garantiza ausencia de todo solapamiento: inspeccionar siempre.

Pruebas negativas reales: cifra alterada, página omitida, PDF raster y desborde → código 1; contenido modificado → rechazo por hash; PDF original → código 0. No se probó carga en LinkedIn ni publicación. Telegram se registra por separado en `out/telegram-delivery.json`; aceptación API no prueba lectura humana.

Skill invocable: `$publicacion-externa Prepara el carrusel LinkedIn del post <ref> con la plantilla HTML/CSS nativa`. Instrucciones completas en `penta-agent/skills/publicacion-externa/references/carrusel-linkedin-nativo.md`.

Rollback: conservar salidas del piloto; ninguna plantilla antigua fue eliminada. Este trabajo no incluye commits, pushes ni publicación en redes.

## Custodia del cierre

`evidence/` conserva el snapshot de recibos de la versión entregada: build, QA, geometría, revisión visual, pruebas negativas y Telegram. Son evidencia histórica del hash indicado, no prueba automática del estado futuro. `out/` contiene el PDF y los artefactos locales regenerables. Commits locales autorizados el 2026-11-10; sin push.
