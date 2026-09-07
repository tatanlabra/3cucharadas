# Contrato de saneamiento — evidencia viva

## TODO_STATE v1

| Fase | Estado | Evidencia / siguiente gate |
|---|---|---|
| F0 Custodia | [x] | 1.325 archivos, bundle completo, restore y tres negativos rechazados |
| F1 Reconciliación | [x] | Base 75f80d72 + historia f91498b7; archivo externo verificado; gobernanza verde |
| F2 Entorno | [x] | Instalación aislada: 52 gems; doctor reparado; 5 tests/38 aserciones, stringex rojo/verde y paridad HTML ES/EN; runtime 2/9 |
| F3 Dependencias/gates | [x] | Cinco actualizaciones conservadoras; contrato local y tres builds verdes |
| F4 Interfaz/rendimiento | [x] | 22 combinaciones de la candidata, revisión completa de incompletos, interacción/fallback y ensayo controlado; ver suplemento de validación |
| F4.1 Paleta nocturna | [x] | Teal tenue, contraste 10,83:1, tema claro y teclado conservados |
| F4.2–4.4 Accesibilidad emergente | [x] | Paginación, fórmulas móviles y roles Catastro: fallo observado y recuperación |
| F5 Consumidores/DEV | [~] | 7 publicados/0 borradores verificados; no-op probado con CLI real y negativos; falta corroborar ese no-op en el workflow de la release |
| F6 Producción | [~] | Baseline 5052233b ya desplegado; suplemento local aprobado, pendiente convergencia y comprobación de la nueva release |

## Custodia y reconciliación

Respaldo privado: `3cucharadas/git-backups/site-health-20260906T221857Z` bajo
`XDG_STATE_HOME` (por defecto `~/.local/state`). Contiene `refs.bundle`, índice,
patch sin stage, estado NUL, snapshot íntegro y manifiesto SHA-256. La restauración
bare pasó `git fsck`; los 1.325 archivos restaurados coinciden. Los controles
manifest vacío, hash alterado y archivo ausente fallaron; el válido volvió a pasar.

Las 23 rutas pendientes se preservan íntegramente en ese snapshot. El baseline
remoto probado gobierna la candidata; no se reaplican versiones anteriores de sus
correcciones. Inventario original: `worktree-comparison.json` en la auditoría
`3cucharadas-audit-fgDYyv` y `status.z` en el respaldo durable.

| Rutas locales | Disposición y razón |
|---|---|
| scripts/notify_telegram_commit.py | Idéntica al remoto; absorbida |
| scripts/syndicate_devto.rb; scripts/jekyll_to_devto.rb; tests/test_jekyll_to_devto.rb | Versiones anteriores archivadas; remoto añade selección de borradores, rasterización, preflight y pruebas |
| scripts/verify_distribution_done.rb | Anterior archivada; remoto distingue plataforma/idioma y contratos ausentes |
| scripts/notify_telegram_publication.py; tests/test_notify_telegram_publication.py | Anteriores archivadas; remoto comprueba ambos espejos |
| .gitlab-ci.yml; .github/workflows/devto-syndication.yml | Anteriores archivadas; remoto conserva gates estrictos y modo de borradores existentes |
| scripts/install_git_hooks.sh; scripts/git-hooks/post-commit; scripts/git-hooks/README.md | Anteriores archivadas; remoto conserva instalación idempotente y commits silenciosos |
| difusion/README.md; difusion/config/destinos.yml; difusion/linkedin/multiagente-penta-agent-memoria-gobernada-targeting.md | Anteriores archivadas; baseline remoto preservado sin ejecutar canales |
| docs/distribucion.md; docs/publishing.md; systemd/user/difusion-cadencia.service | Anteriores archivadas; remoto documenta auditoría programada y ambos remotos |
| docs/flujo-difusion.md; docs/diagrams/flujo-difusion.d2; docs/diagrams/flujo-difusion.svg; docs/diagrams/flujo-difusion-mobile.d2; docs/diagrams/flujo-difusion-mobile.svg | Anteriores archivadas; se conserva la documentación remota consistente con sus scripts |

El commit de video queda en la ascendencia de la candidata mediante merge. Ningún
archivo pendiente se borra del checkout operativo antes de revalidar su snapshot.

## Archivo de videos

Decisión humana: archivo externo trazable de ambos videos aprobados, sin insertarlos
en posts ni publicarlos. Ubicación: `3cucharadas/source-masters/penta-rag-video-20260906`
bajo `XDG_STATE_HOME`. Nueve archivos copiados y verificados: seis entregables,
dos documentos históricos y la receta ejecutable. Su `manifest.json` contiene
paths, tamaños, hashes, commit de procedencia, responsable, función y retención.

| MP4 | SHA-256 |
|---|---|
| Piloto, 2.764.701 bytes | `4d1b33173e0ca3eb52b3624f8b4d0cb3132c7e5af7484cd941ca1d43bc561c9e` |
| Variante, 3.661.510 bytes | `5aecef774b0a0adae3993b42bef2f5a7ec020bc49c309c352c55ae2321783efd` |

Los seis entregables se retiran únicamente de la candidata publicable después de
verificar la copia. Se recuperan desde ese archivo, el respaldo F0 o el commit
`f91498b7`. Responsable: editorial-multiagente. Retención: hasta reemplazo explícito
y restauración comprobada. Los documentos de captura permanecen como historia;
sus enlaces originales se resuelven restaurando el paquete completo del archivo.

## Validación local y contraejemplos

La candidata integra el remoto 75f80d72 y conserva f91498b7 en su ascendencia.
Antes de actualizar el checkout operativo se repitió el cotejo de sus 1.325 hashes:
`PASS unchanged live snapshot`. Los 23 paths quedaron además en el stash
`site-health-20260906: original pending work preserved; see F0 backup`.
`main` avanzó por fast-forward; no se aplicó encima el contenido antiguo del stash.

| Superficie | Evidencia observada |
|---|---|
| Entorno operativo | Instalación frozen en vendor/bundle; bundle check y doctor exit 0; Node 26.8.1, Bundler 4.0.3, Ruby 3.4.10 |
| Gems | concurrent-ruby 1.3.8, csv 3.3.6, execjs 2.10.2, google-protobuf 4.36.1, sass-embedded 1.104.0; un commit por actualización conservadora |
| Presupuesto transitivo | 131.980/153.600 bytes gzip, dos archivos; import dinámico sobredimensionado, manifiesto vacío e import ausente rechazados |
| Tipos | Nueva prueba detectó TS7016 por declaración ausente; d.mts añadido, TypeScript volvió a verde sin bajar exigencia |
| Suite | 194 pruebas únicas ejecutadas en el checkout operativo; siete geoespaciales omitidas; dos nuevas regresiones YAML/CSS pasan además |
| Builds | Producción, future y drafts; comprobación de artefactos y readiness verdes |
| Seguridad consultada | npm audit: cero vulnerabilidades; API Dependabot: cero alertas abiertas |
| Git operativo | fsck y gobernanza verdes; count-objects garbage=0; checkout limpio, dependencias ignoradas permitidas |
| Hooks | Cadena anterior respaldada; primera instalación actualiza, segunda informa already installed; commits no notifican Telegram |
| systemd | Symlink al checkout operativo, WorkingDirectory correcto, ExecStart --ventana 30; daemon-reload sin iniciar publicación |

Ejecución en `/tmp/3c-health-run-LCLqKQ`: `recovery/local.json` acredita la suite
verde anterior a la última corrección ARIA; `pre-release/report.json` repitió
pruebas y builds sobre 27069d2b, pero salió 1: ambos remotos seguían en 75f80d72
y no había pipeline del candidato. Esto demuestra que HTTP 200 del sitio viejo
no basta para aprobar producción. El informe final debe repetirse tras el push.

## Interfaz: mejora acotada, no perfección

**Suplemento que reemplaza el cierre provisional de F4:**
[validación completa](site-health-validation-20260906.md). Las cifras y límites
de las primeras pruebas se conservan debajo como historia, no como prueba suficiente
del contrato completo.

`browser/matrix.json`: portada ES/EN, avalúo, Nushell y post III × 1280/390 px ×
claro/nocturno. Las 20 combinaciones finales no detectaron violaciones axe
WCAG A/AA. Hubo dos fallos reales corregidos: enlace deshabilitado sin nombre y
fórmulas anchas sin acceso de teclado. La fórmula móvil se enfocó y ArrowRight
produjo scrollLeft=40. El HTML MathML y los feeds no se reescriben.

Catastro: selección Atacama/Caldera y vista agregada operativas, documento de
390 px sin overflow. Axe detectó regiones nombradas sin rol; se corrigieron los
14 contenedores con el mismo patrón, incluidos paneles inicialmente ocultos.
`catastro-a11y-recovery.json` registra cero violaciones y dos revisiones pendientes
del motor automático. No se certificó la descarga de geometría externa en esta
sesión limitada a localhost. El grafo 3D separado dio cero violaciones automáticas;
una sesión con WebGL desactivado mostró las ocho familias en su fallback.

Bloquear `theme-toggle.js` hizo que toggleWorks=false; desbloquearlo y recargar
restauró toggleWorks=true. Los recursos externos estuvieron bloqueados; su ausencia
en capturas no se imputa a regresión de CSS. La revisión no equivale a WCAG integral
ni a pruebas con lectores de pantalla. Ver el informe específico de paleta.

Siete pares exploratorios, orden alternado: LCP mediano baseline 120 ms y candidata
124 ms; CLS mediano 0,36 en ambas. No hubo mejora de 10% ni cinco pares favorables.
Además, no se fijaron caché/red/reloj con rigor de promoción: estas mediciones NO
acreditan rendimiento de producción. No se retuvo una optimización de velocidad;
la paleta se acepta por contraste y continuidad visual, no por velocidad. El CLS
observado tampoco permite afirmar que el rendimiento sea óptimo: queda como
línea de investigación separada con ensayo controlado antes de cambiar arquitectura.

## DEV y deuda editorial

**Actualización posterior:** la persona usuaria autorizó depurar y luego publicar.
Se eliminó sólo el duplicado idéntico 4584581, se conservó el ID del ledger y se
publicaron los cinco borradores restantes. Panel y API pública verificados:
7 publicados, 0 borradores; cuerpos intactos. La decisión ya no está pendiente.
Ver [evidencia y nuevas URLs](devto-publication-20260906.md). Los párrafos siguientes
conservan el incidente anterior a esa autorización, no el estado actual.

Modo de mantenimiento: sólo drafts existentes, canonical único, relectura antes
del PUT, rechazo de estados cambiantes y parada ante 429. Cuatro pruebas y 23
aserciones pasan; rechazan destino ausente/publicado/duplicado/modificado y verifican
custodia cifrada recuperable. `--existing-drafts-only --dry-run` salió 2, porque
una simulación sin API no demuestra estado remoto. Contrato y recuperación en
`docs/contracts/devto-draft-maintenance.md`.

La ejecución autenticada se detuvo **antes de todo PUT/POST** por canonical
duplicado `https://3cucharadas.cl/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/`.
No se generó custodia remota porque el preflight global precede a cualquier escritura.
Run bloqueado: https://github.com/tatanlabra/3cucharadas/actions/runs/34065651595 .
No se elige ni elimina un duplicado sin decisión humana. Tampoco se actualizan
silenciosamente los otros borradores después del fallo. Pregunta nativa emitida:
pausar DEV, omitir Avalúo o elegir un ID tras revisión. Sin respuesta aún.

El consumidor `--ventana 30` sigue rojo por cinco compromisos reales vencidos:
Nushell Mastodon ES/EN, Bluesky ES/EN y DEV EN. La deuda histórica se informa aparte.
No se modifican publicaciones ni fechas para conseguir verde y no se envía Telegram.

## Producción e incidentes de implementación

GitLab recibió por SSH los mismos commits que GitHub, sin force. El primer intento
HTTPS de escritura GitLab no tenía credencial y no modificó el remoto; se utilizó
después su URL SSH canónica sin cambiar configuración ni secretos.

El workflow inicial de esta implementación fue rechazado por YAML: el `:` del
trailer estaba dentro de una expresión sin comillas externas. Fue un fallo propio,
no de DEV. Se reprodujo con Psych, se corrigió y se agregó un gate de todos los
workflows con fixture rojo/verde. La corrida siguiente sí llegó al inventario
autenticado y se detuvo correctamente por duplicados.

El pipeline https://gitlab.com/tatanlabra/3cucharadas/-/pipelines/2824859252
publicó df3d67bd; build_site y pages exitosos. El CSS que enlaza el HTML público
(`/assets/css/main.css?v=1788735697`) coincide byte a byte con el build local:
`daee7bc59122690338d3600367554b82c66404b3a102320b2566635a2b29627d`.
La comprobación inicial consultaba la URL sin versión y dio falsa alarma por su
caché de cuatro horas; el gate ahora resuelve la URL desde el HTML público y exige
una sola referencia. Los fixtures rechazan referencia ausente o ambigua. No hubo
purga ni cambios de Cloudflare. Falta ejecutar el informe final sobre el commit
que incorpora esta propia evidencia.

## Alcance del juicio

La transcripción del plan aprobado está en
`docs/contracts/site-health-approved-plan.md`. La continuación detectó una
declaración prematura de F4 completa: 49 checks técnicos PASS no acreditan por sí
solos todas las obligaciones manuales del plan. Se conserva la evidencia anterior
y se reabre la fase hasta completar ensayo controlado y revisión de incompletos.

La nueva fixture F2 refutó inicialmente otra premisa: GFM genera
`prueba-ágil` / `niño-y-acción`, no sus equivalentes ASCII, aun con
`transliterated_header_ids: true`. El camino Kramdown sí usa `stringex`. Se prueba
su ausencia mediante `Gem::LoadError` y recuperación con la gema disponible, y
se congela por separado la igualdad del HTML GFM en ambas URLs ES/EN con y sin
el hook. No se cambian anchors ni gems instaladas para satisfacer una expectativa
equivocada. Ejecutar `ruby tests/test_polyglot_doctor.rb`; `bundle exec ruby` no
es el runner de estas pruebas: `minitest` está en el entorno de test, no en Gemfile.

Inventario DEV suplementario autenticado y **sólo lectura**:
https://github.com/tatanlabra/3cucharadas/actions/runs/34066653342 . Confirmó dos
borradores para Avalúo (`4584596` y `4584581`, ambos `published=false`). No fue un
falso positivo causado por un publicado. La rama diagnóstica
`maintenance/devto-inventory-20260906` fuerza `DEVTO_INVENTORY_ONLY=1` y **no debe
fusionarse sin retirar esa configuración exclusivamente diagnóstica**. Pruebas:
3 casos, 17 aserciones, sólo dos GET y rechazo de toda escritura, 429 y falta de
credencial. Cero escrituras reales; la decisión humana sigue pendiente.

Autorrevisión de Codex; no revisión entre proveedores. El usuario añadió después
un subagente para F4.1, con propiedad exclusiva de la hoja de estilos y sin
autoridad de publicación. MCP selector evaluado, pero
el registro automático informó `MCP observation unavailable`. Ningún canal externo
se activa por esa selección. Deuda editorial y cobertura geoespacial se informan
separadas de salud técnica; no se cambian sus criterios para obtener verde.
