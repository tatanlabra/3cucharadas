# Evidencia de cierre: difusión y gobernanza — 2026-09-06

Medición final: 2026-09-06 18:25, America/Santiago. SHA auditado:
`03cb4e472d50a0f1b2cba2c77081a4ff63936826`.

## Estado probado

| Superficie | Resultado medido |
|---|---|
| GitLab y GitHub `main` | Mismo SHA `03cb4e47` |
| GitLab pipeline `#226` | `build_site` y `pages` en `success` |
| GitHub DEV.to run `34057422194` | 7 actualizaciones OK; sin 429 |
| Producción | Avalúo, Multiagente II y portada WebP respondieron HTTP 200 |
| Build limpio completo | 1.121 archivos; 59.873.791 de 1.048.576.000 bytes |
| Readiness editorial | 18 posts con imagen, descripción, canonical y enlaces válidos |
| Transformación DEV.to | 17 tests; 142 aserciones; cero fallos |
| Gobernanza | 1.337 entradas; 61.917.784 bytes; cero violaciones |
| Git object store tras retirar el worktree de auditoría | `garbage: 0` |

La primera ejecución de `verify_site_artifact.rb` falló con `Vite manifest is
missing` porque se había construido solo Jekyll. Después de ejecutar los dos builds
Vite y reconstruir Jekyll en otro destino vacío, el mismo verificador pasó. Este
rojo/verde prueba el orden del pipeline; no se rebajó ningún gate.

## Deuda de difusión observada

La auditoría completa terminó con exit 1 por 11 salidas vencidas:

| Canal | Posts | Cantidad |
|---|---|---:|
| DEV.to EN | AI Quota, Multiagente II, Avalúo, Nushell | 4 |
| Medium EN | CASEN, AI Quota, Avalúo | 3 |
| Mastodon y Bluesky | Nushell en ES y EN, ambas redes | 4 |

Tres plazos aún no vencidos quedaron visibles: Multiagente III DEV D3/D4,
Nushell Medium D8/D10 y Multiagente III Medium D3/D10.

La API pública de DEV devolvió 200 para los IDs `4584590` y `4584570`, y 404 para
`4235233`, `4584571`, `4582774`, `4584596`, `4584688` y `4584581`. El último snapshot
autenticado disponible, generado a las 17:05, mostraba esos seis como borradores y
confirmaba que `4584581` duplicaba el avalúo. La sesión de cierre no tenía
`DEV_TO_API_KEY`; por tanto, el 404 actual demuestra ausencia pública, no existencia
actual del borrador.

## Estado de destinos por feed

| Destino | Evidencia | Pendiente real |
|---|---|---|
| Medium | Cinco refs en estado `listo`; modo manual | Importar, revisar canonical, publicar y registrar |
| Planet Python | AI Quota y Avalúo pasan el gate; `feed-python.xml` respondió 404 | Definir feed adecuado, validarlo y solicitar incorporación |
| JuliaBloggers | `feed-julia.xml` respondió 200 y contiene un item | Verificar ingestión externa |
| R-bloggers | Mejor candidato observado en 1/2 posts EN con tag R | Segundo artículo, feed R completo y backlink |

## Checkout compartido

El checkout operativo permaneció en `47234acd`, 10 commits detrás del remoto, para
no pisar trabajo concurrente. Su estado contenía 32 rutas:

| Clase | Rutas |
|---|---:|
| Modificadas e idénticas al remoto | 3 |
| Modificadas y diferentes del remoto | 11 |
| No versionadas, con ruta remota pero contenido diferente | 9 |
| No versionadas y ausentes del remoto | 9 |

Las nueve rutas nuevas pertenecen al piloto de captura de video y pesan 7.320.547
bytes. Su propio `TODO_STATE` deja pendientes la aprobación visual específica de la
variante y su eventual commit/push. No se eliminan ni se mezclan con este cierre.

El timer `difusion-cadencia.timer` estaba habilitado, con próxima corrida el
2026-09-07 a las 09:30. El servicio figuraba `failed` porque el gate devolvió 1:
systemd cargó la unit y ejecutó correctamente el contrato. El checkout compartido
reportó 3 categorías recientes; el SHA remoto reportó 5 plataformas/idiomas, lo que
demuestra la deriva operativa que debe resolverse antes de confiar en la próxima
cuenta.

## Orden de reanudación

1. Dar custodia a las 29 rutas divergentes o nuevas y reconciliar el checkout con `main`.
2. Repetir el gate de 30 días desde el checkout ya actualizado.
3. Publicar y registrar DEV.to y las cuatro salidas sociales de Nushell.
4. Procesar los cinco candidatos Medium según prioridad editorial.
5. Decidir el alta de Planet Python y verificar JuliaBloggers.
6. Revisar visualmente la variante de video antes de integrarla o archivarla fuera del repo.

Fuentes externas consultadas:

- https://dev.to/p/editor_guide
- https://developers.forem.com/api/
- https://github.com/python/planet/blob/main/config/config.ini
- https://www.r-bloggers.com/add-your-blog/
