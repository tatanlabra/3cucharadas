# Coherencia y activos: cierre local de controles

El control de coherencia exige ahora una `ref` exacta o `--all-declared`. Antes,
site-health invocaba implícitamente otro artículo y no inspeccionaba los TXT/JSON
de Avalúos II. Los recibos históricos se conservan: un PASS anterior sobre el
post predeterminado no acredita Avalúos II.

| Control | Ejecución local | Alcance |
|---|---|---|
| Coherencia por artículo | `ruby scripts/verify_difusion_coherente.rb avaluos-ii-brecha-residencial` | Ref exacta, posts ES/EN y piezas identificadas |
| Paquetes declarados | `ruby scripts/verify_difusion_coherente.rb --all-declared` | Directorios con metadata JSON/YAML; no significa todos los posts del blog |
| Formato histórico | `ruby scripts/verify_difusion_coherente.rb multiagente-penta-agent-memoria-gobernada-poc` | Ref exacta del post y alias explícito de nombres de piezas |
| Regresión de coherencia | `ruby tests/test_verify_difusion_coherente.rb` | Cobertura, formatos, cambios de cifras, extracción y precisión de redondeo |
| Regresión móvil | `ruby tests/test_verify_visual_assets_mobile.rb` | Existencia y pertenencia publicable de `teaser_mobile` |
| Integración | `ruby scripts/verify_site_health.rb --profile source` | Incluye ambos tests y los controles de fuente existentes |

Se comparan valores normalizados con idioma y decimales TeX; no se borran los
separadores indiscriminadamente. Las conversiones ms→s solo se aceptan con unidades
explícitas y la precisión escrita: 6239 ms admite 6,2 s o 6,24 s, pero no 6,20 s.
Las notas operativas del formato Reddit se separan mediante secciones explícitas;
el contenido publicable vacío y los JSON de copy desconocidos fallan.

El control numérico compara conjuntos, no asigna cada cifra a una afirmación.
Conserva exclusiones históricas de años, enteros de un dígito, dimensiones comunes
y encabezados/código de Markdown. No demuestra corrección científica, cobertura
de todo el texto renderizado, publicación efectiva ni igualdad semántica.
Las piezas fuera de los formatos y paquetes declarados requieren alcance explícito.

La revisión adversarial reprodujo y corrigió pérdida de precisión por ceros finales,
extracciones vacías y ausencia del test móvil en la suite integral. La evidencia
append-only de baseline, revisiones y recuperación está en el repositorio canónico
`penta-agent/experiments/skills-closeout-six/`, junto con seis pares de evaluación
de skills. Los ensayos fueron simulaciones locales; no hubo publicaciones, cargas
de medios, programación, borradores remotos ni push. Este cierre no acredita un
despliegue ni reemplaza los pendientes históricos de rendimiento.
