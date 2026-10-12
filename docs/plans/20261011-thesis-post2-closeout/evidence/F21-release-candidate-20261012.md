# F21 — candidato limpio para H1

Fecha: 2026-10-12. Estado: listo para revisión humana; sin push ni despliegue.

## Custodia

| Control | Evidencia |
|---|---|
| Base remota | GitLab y GitHub `main` observados en `b2957178560013987e3d45d535f093b3aef70997`. |
| Historia | Worktree nuevo desde `origin/main`; no hereda el commit histórico con metadatos Tailnet. |
| Alcance | 71 rutas del paquete Post II; cuatro SVG no rastreados de Rancagua/La Reina excluidos. |
| Dependencias | Gems y módulos Node locales ya instalados; no hubo descarga ni incorporación al índice. |
| Acciones externas | Ningún push, despliegue público ni difusión. |

## Rojo → verde del gate limpio

| Observación | Exit | Corrección |
|---|---:|---|
| Autodetección desde `/tmp` buscó la tesis bajo `/tmp/incubadora`. | 2 | Declarar `THESIS_WORKSPACE_ROOT` y `THESIS_RESEARCH_ROOT`. |
| El worktree no heredó cuatro gems del bundle local. | 1 | Usar `BUNDLE_PATH` del checkout canónico; no descargar. |
| El artefacto no tenía el manifiesto Vite ignorado. | 1 | El preview genera catastro, Post II y memoria gobernada antes de Jekyll. |
| La ruta al binario Vite no resolvía imports ESM. | 1 | Enlazar temporalmente `node_modules` ya instalado; el enlace queda ignorado. |
| Gate integral sobre el candidato final. | 0 | Freeze → claims → semántica → Vite → Jekyll → artefacto → navegador. |

## Resultado medido

| Gate | Resultado |
|---|---|
| Freeze científico | Válido: 58 artefactos, 15 claims, aprobación humana `NOT_GRANTED`, R-007 `OPEN`. |
| Claims | `ARTICLE_PRODUCT_CLAIMS_CURRENT_WITH_BLOCKERS`; exit 0. |
| Semántica | `PASS`; solo avisos blandos de longitud ES/EN. |
| Vite | Tres bundles construidos con Node 26 y Vite 8.2.2. |
| Jekyll | Build de producción exit 0; avisos de `@import` Sass no bloqueantes. |
| Artefacto | 70.884.482 bytes y 1.506 entradas; exit 0. |
| Navegador | 24/24 páginas, 12/12 SVG y 2/2 fallbacks; cero fallos. |

## Límite del cierre

- El candidato acredita aptitud local y reproducibilidad en este equipo; no acredita estado público.
- La longitud supera la meta blanda de 2.500 palabras, pero no viola el contrato editorial revisado.
- Los chunks Vite grandes y la deprecación Sass son deuda técnica no bloqueante para Post II.
- H1, push, despliegue, paridad pública y difusión requieren decisiones posteriores separadas.
