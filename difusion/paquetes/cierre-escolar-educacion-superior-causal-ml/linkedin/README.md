# Carrusel LinkedIn IV — paquete listo, no publicado

- PDF: `out/educacion-iv-linkedin.pdf`, 12 páginas nativas, formato 4:5, texto seleccionable, Fira Sans incrustada y enlace al artículo.
- Fuente: post IV vigente; `source-lock.json` fija texto y assets. Post canónico intacto.
- Alcance de canal: LinkedIn ES, tema oscuro fijo; no se alteran variantes ES/EN o claro/oscuro del sitio.
- Punto e intervalo elegido para mostrar magnitud e incertidumbre. Se descartaron barras sin intervalo y flujos individuales que los agregados no identifican. Escala común entre los cuatro destinos.
- Cobertura: acceso, cuatro destinos, persistencia, titulación, sensibilidad y límites; ventanas y denominadores visibles. Fuente completa para resultados secundarios.
- `texto-accesible.md`: transcripción, tabla de valores y límites. No equivale a certificación PDF/UA.
- Revisión independiente: REQUEST_CHANGES → corrección del sesgo de controles → APPROVE del contenido. Inspección visual individual por integrador: 12 páginas, incluida escala móvil de 390 px.
- Pruebas negativas: cifra adulterada, página omitida, raster, desborde y contenido cambiado rechazados; original aceptado. Recibos en `evidence/`.
- LinkedIn 2026-11-11: acceso redirige a login y desafío humano Cloudflare; sin subida ni envío. Requiere sesión utilizable.

## Reproducir

```bash
python3 scripts/render_linkedin_native.py --content difusion/paquetes/cierre-escolar-educacion-superior-causal-ml/linkedin/content.json --output difusion/paquetes/cierre-escolar-educacion-superior-causal-ml/linkedin/out --filename educacion-iv-linkedin.pdf
```

`out/` contiene derivados locales ignorados. Inventario de campaña registra solo archivos versionables; la custodia integral se comprueba en checkout aislado sin derivados locales. El PDF puede cambiar hash por metadatos internos al reconstruirse; el recibo acredita la ejecución concreta.
