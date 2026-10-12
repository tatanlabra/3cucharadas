# F22 — custodia del puente científico

Fecha: 2026-10-12. Estado: commit científico bloqueado; implementación local validada.

## Experimento limpio

| Control | Resultado |
|---|---|
| Base | Worktree separado desde `38a31d79272f8a1c10d34113a862c241a69d3a27`. |
| Parche | Ocho archivos: registro y programa editorial, módulo, tests, dos audits y dos reportes. |
| Post canónico | Symlink aislado al candidato limpio del blog para conservar la topología del workspace. |
| Ruff y `git diff --cached --check` | Exit 0. |
| Claims | 21 pasan y uno falla; el primer faltante es `audit/article_h3_performance_trajectory.json`. |
| Freeze | 17 pasan y uno falla por observación Git obsoleta. |
| Validadores | Claims exit 2 por evidencia ausente; freeze exit 2 por observación Git no portable. |

## Clausura faltante

El registro vigente requiere ocho artefactos que no existen en la base Git limpia:

- `audit/article_h1_model_diagnostics.json`
- `audit/article_h1_temporal_calibration_joint_bootstrap.json`
- `audit/article_h1_temporal_validation.json`
- `audit/article_h2_robustness.json`
- `audit/article_h3_composition_trajectory.json`
- `audit/article_h3_joint_trajectory.json`
- `audit/article_h3_performance_trajectory.json`
- `audit/article_post2_research_closeout.json`

## Decisión

- No se creó un commit parcial que solo pase en el árbol vivo.
- Incorporar los ocho JSON sin sus generadores, fuentes y contratos produciría apariencia de reproducibilidad, no reproducibilidad.
- La matriz pública, el blog y H1 permanecen válidos: usan la evidencia actual y sus límites, no afirman que el artículo futuro esté cerrado.
- E-46 se desbloquea cuando se adjudique una revisión científica coherente con esos artefactos y su procedencia.
