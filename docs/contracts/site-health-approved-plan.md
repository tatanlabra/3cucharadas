<!-- Transcripción del plan aprobado con «Implement the plan» en la sesión 01a078a3-c888-7730-9866-5cd3920e1305. Preservar como referencia histórica: la autorización posterior de subagente para paleta amplió F4.1 y reemplazó sólo la restricción de delegación correspondiente. -->

# Saneamiento verificable de 3cucharadas hasta producción

## Objetivo y decisiones fijadas

Dejar el checkout operativo reconciliado, las dependencias reproducibles, los diagnósticos funcionales y producción verificada, preservando todo trabajo previo.

- Ambos videos quedarán en archivo externo trazable, con hashes, manifiestos y evidencia de aprobación.
- DEV.to podrá actualizar únicamente borradores existentes; no creará artículos ni modificará publicados.
- Codex implementará y juzgará con herramientas y contraejemplos; se declarará autorrevisión, sin delegación.
- La deuda de publicaciones sociales seguirá visible y separada de la salud técnica.
- El baseline se actualizará al comenzar: la auditoría anterior encontró `f91498b7` local, `75f80d72` remoto y 23 rutas pendientes.

## Contrato y regla del juez

Crear `docs/contracts/site-health.yaml` y un ejecutor común, `scripts/verify_site_health.rb`, reutilizando los validadores existentes.

Cada fase declarará objetivo, invariantes, entrada, salida, evidencia, condición de falsación y rollback. El reporte distinguirá `PASS`, `FAIL` y `NO_CONCLUYENTE`; devolverá respectivamente códigos 0, 1 y 2. Una colección vacía, una prueba omitida o un error de herramienta nunca equivaldrán a éxito.

| Tipo de evidencia | Exigencia |
|---|---|
| Deductiva | Cada conclusión debe derivarse de un invariante y una comprobación ligada al SHA, configuración e inputs evaluados |
| Inductiva | Cada gate nuevo o modificado debe rechazar un fallo pertinente y aprobar después su recuperación |
| Contraria | Registrar regresiones, resultados negativos, candidatos descartados y límites de cobertura |
| Optimalidad | Comparar contra el baseline bajo iguales condiciones; aprobar primero restricciones duras y después mejoras medibles |

Invariantes globales: cero pérdida de trabajo, cero alteración de datos canónicos o aprobaciones históricas, cero publicaciones fuera del alcance y cero relajación silenciosa de gates.

Los desempates favorecerán menor superficie de cambio, reversibilidad, accesibilidad, trazabilidad y costo operativo. Ninguna puntuación compensará un incumplimiento duro.

## Fases de ejecución

La secuencia será F0 → F1 → F2 → F3 → F4 → F5 → F6; sólo se paralelizarán comprobaciones independientes.

| Fase | Implementación y gate de entrada | Evidencia exigida para salir | Rollback |
|---|---|---|---|
| **F0. Custodia** | Inventariar refs, índice, cambios, archivos no versionados y worktrees; partir del estado observado al iniciar | Nuevo bundle con refs actuales, respaldo separado del trabajo no comprometido y manifiesto SHA-256; restauración probada en directorio vacío | Conservar checkout original y respaldos anteriores |
| **F1. Reconciliación** | Con F0 aprobado, crear candidata desde el remoto actualizado; clasificar cada diferencia local como equivalente, superada, mejora exclusiva o conflicto | Las 23 rutas iniciales —más cualquier cambio posterior— tienen destino documentado; ninguna versión antigua sustituye capacidades remotas superiores; candidato funcional | Descartar únicamente la candidata propia; originales y respaldos permanecen |
| **F2. Entorno y diagnósticos** | Sobre candidata reconciliada, reparar Bundler, alinear Node y restaurar el diagnóstico de Jekyll | Instalación limpia, `bundle check`, diagnóstico y builds funcionan; discrepancia de versión y fallo `stringex` rechazan sus fixtures | Revertir el commit específico y restaurar configuración local respaldada |
| **F3. Dependencias y gates** | Con entorno estable, evaluar las cinco actualizaciones compatibles y consolidar validaciones locales/CI | Locks coherentes, suites y tres modos de build verdes; gates rechazan assets ausentes, contratos vacíos y presupuestos excedidos | Revertir cada actualización o gate por separado |
| **F4. Interfaz y rendimiento** | Con artefacto válido, medir baseline y candidatos acotados | Interacciones, accesibilidad y alternativas textuales verificadas; conservar sólo optimizaciones con mejora reproducible | Restaurar candidato anterior y confirmar recuperación |
| **F5. Consumidores y DEV.to** | Con candidata aprobada, preparar actualización del checkout operativo y controlar la sindicación | Hooks/servicio consumen los archivos previstos; pruebas demuestran cero creación y cero modificación de publicados | Restaurar configuración propia; detener escrituras DEV ante discrepancias |
| **F6. Producción** | Todos los gates requeridos aprobados y comparación final contra remotos | Ambos remotos convergen, CI y Pages verifican el SHA final, producción responde correctamente y DEV conserva el alcance autorizado | Revertir mediante nuevo commit, sin reescribir historia; verificar nuevamente despliegue |

### Decisiones técnicas de las fases

- **Custodia:** el bundle existente tiene integridad válida, pero no sustituye el respaldo actualizado ni contiene automáticamente cambios sin commit; probar ambas recuperaciones.
- **Reconciliación:** conservar en archivo recuperable las versiones locales superadas; integrar mejoras exclusivas sólo si pasan la misma rúbrica. Un conflicto semántico irresoluble se consulta.
- **Videos:** copiar ambos MP4, manifiestos, imágenes y evidencia a una carpeta versionada por fecha bajo el estado externo de 3cucharadas; comprobar restauración y referencias antes de retirarlos del árbol publicable.
- **Bundler:** instalar dependencias en una ubicación declarada y soportada; mantener `stringex` del remoto y preservar los anchors actuales.
- **Runtime:** unificar Node en **26.8.1**, incluyendo CI, `.nvmrc`, selección del runtime y checks; verificar los tarballs oficiales contra hashes fijados. Mantener inicialmente Ruby 3.3 en CI y 3.4 local como matriz explícita, con Bundler **4.0.3**.
- **Doctor:** añadir compatibilidad mínima y versionada para preparar Polyglot antes de la lectura diagnóstica; comprobar que no cambia URLs, idiomas ni HTML del build. No editar gems instaladas ni ocultar excepciones.
- **Dependencias:** evaluar `concurrent-ruby`, `csv`, `execjs`, `google-protobuf` y `sass-embedded` en commits separables; verificar compatibilidad con ambas versiones Ruby.
- **Limpieza:** usar `--strict` más estado Git limpio para el checkout operativo; reservar `--strict-local` para copias destinadas a archivo. Las dependencias ignoradas necesarias no se tratarán como corrupción.
- **Presupuestos:** mantener separados capacidad de Pages y transferencia al navegador; contar también chunks importados al medir gzip para impedir una mejora ficticia por repartir archivos.
- **Sass:** corregir primero usos deprecados propios; evitar una sustitución completa del tema como parte de este saneamiento.

## Herramientas y pruebas

| Capacidad | Activación y propósito |
|---|---|
| `3cucharadas-site` + `codigo-multilenguaje` | Builds, dependencias, scripts reproducibles y reversión |
| `auditoria-critica` | Aplicar restricciones, buscar contraejemplos y emitir el dictamen |
| Git, Bundler, npm y suites existentes | Integridad, recuperación, instalaciones limpias, compatibilidad y regresiones |
| `agent-browser` | Sesión aislada para interacción, capturas, accesibilidad y métricas; `PLAYWRIGHT_LOCAL` sólo ante fallo comprobado del primero |
| `systemd-monitoring` | Comprobar rutas y comportamiento del servicio de cadencia; distinguir ejecución correcta de deuda editorial detectada |
| APIs GitLab/GitHub/DEV.to y HTTP | Verificar commits, jobs, despliegue y estados reales; secretos mediante mecanismos existentes |
| `recall-context` y `quota-guard` | Recuperar decisiones cuando haya incertidumbre y comprobar margen al iniciar tareas largas |

Registrar una selección contextual de capacidades al iniciar la ejecución. No activar búsqueda bibliográfica, generación de imágenes, cambios de flota MCP ni otros proveedores: no resuelven una necesidad de este contrato.

Pruebas obligatorias:

- Recuperación desde bundle y respaldo de cambios; negativos por archivo omitido, hash alterado y manifiesto vacío.
- Instalación limpia y builds de producción, futuros y borradores; Vite antes de Jekyll, con verificación del artefacto.
- Suites existentes: baseline de **181 pruebas aprobadas y siete geoespaciales omitidas**; estas últimas permanecen explícitamente fuera de cobertura mientras no cambie ese subsistema.
- Fixture de diagnóstico con Polyglot y encabezados transliterados; fixture con conflicto real que el diagnóstico deba rechazar.
- Home ES/EN, post con matemáticas, post III, grafo y Catastro a 390 y 1280 px; teclado, tema, consola, enlaces, carga diferida y fallback sin WebGL.
- Cero errores JavaScript y recursos propios rotos en los recorridos; cero problemas graves de accesibilidad; resultados automáticos incompletos revisados.
- Preservar los targets de navegador existentes; Chromium no acreditará compatibilidad real con Safari 16 o Firefox 104.

Para rendimiento: comparar baseline y hasta dos candidatos con siete pares de mediciones, misma máquina, navegador, viewport, inputs RSS y caché controlada. Conservar una optimización sólo si mejora al menos 10% la mediana de la métrica objetivo, mejora en cinco de siete pares y no deteriora más de 5% las métricas secundarias. Son umbrales de decisión de este experimento, no garantías universales.

## Publicación controlada y cierre

- Preparar primero el resultado completo en aislamiento; actualizar el checkout compartido sólo después de comprobar que no recibió nuevos cambios sin custodia.
- Para esta release, introducir un modo de mantenimiento identificable en el commit que fuerce `--existing-drafts-only` en el workflow; conservar el comportamiento ordinario fuera de ese modo.
- Corregir la simulación actual: con ese modo no podrá anunciar creaciones; sin inventario remoto suficiente deberá declarar resultado no concluyente.
- Antes de cada escritura DEV, comprobar identidad y estado de borrador; guardar el contenido previo y rechazar cambios de estado concurrentes, destinos ambiguos o errores de API.
- Probar explícitamente borrador válido, artículo publicado, destino inexistente, duplicidad, 429 y ejecución repetida; ninguna recuperación podrá crear artículos.
- Publicar con pushes explícitos, sin fuerza; absorber el eventual commit de retorno del workflow y volver a comprobar convergencia de GitLab, GitHub y checkout.
- Verificar páginas ES/EN, canonical, feeds, assets críticos y recorridos interactivos en producción; cerrar sesiones y servidores de prueba.
- No enviar Telegram ni publicar en otras redes. La deuda editorial no se cancelará para conseguir un tablero verde.

Mantener `TODO_STATE` con `[x]`, `[~]`, `[ ]`, `[ghost]` y `[!]`. Todo hallazgo emergente se clasifica antes de actuar: incidental documentado, mejora dentro del alcance con gate propio, incidente diagnosticado o decisión material consultada.

El cierre tendrá las tres filas **implementado / parcial / no implementado**, métricas antes/después, evidencia negativa y positiva, y rollback comprobado. El veredicto será “óptimo factible entre los candidatos evaluados” únicamente si las mediciones lo sostienen; cualquier incumplimiento requerido bloqueará el cierre completo.

