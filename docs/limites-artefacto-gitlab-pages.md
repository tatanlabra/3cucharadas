# Límites verificables del artefacto de GitLab Pages

Fecha de comprobación: 2026-09-06.

## Restricciones efectivas

| Superficie | Límite publicado | Magnitud que se debe medir |
|---|---:|---|
| Sitio GitLab Pages | 1000 MiB | Suma de bytes del árbol desplegado |
| Archivo de artefactos del job | 1000 MiB | Tamaño final de `artifacts.zip` |
| Entradas de un sitio Pages | 200.000 | Archivos, directorios y enlaces simbólicos |

- `1000 MiB` equivale a `1.048.576.000` bytes; no a 1.000.000.000 bytes.
- La [configuración pública de GitLab.com](https://gitlab.com/help/instance_configuration#size-limits) declara 1000 MiB para el artefacto del job y para Pages.
- La [documentación de administración de Pages](https://docs.gitlab.com/administration/pages/#set-global-maximum-size-of-each-gitlab-pages-site) define el límite del sitio y las 200.000 entradas.
- La [documentación de artefactos](https://docs.gitlab.com/ci/jobs/job_artifacts/#set-the-maximum-artifacts-size) aclara que el límite se aplica al archivo final, no a cada archivo individual.
- La API pública del proyecto devolvió `max_artifacts_size: null`; por tanto, no hay un override de proyecto observable y se usa el límite de GitLab.com.

## Medición local antes del push

`scripts/verify_site_artifact.rb` calcula bytes y entradas directamente sobre `public/`.
El gate usa los límites reales anteriores y permite overrides cuando GitLab cambie:

```bash
ruby scripts/verify_site_artifact.rb public
SITE_ARTIFACT_MAX_BYTES=1048576000 SITE_ARTIFACT_MAX_ENTRIES=200000 \
  ruby scripts/verify_site_artifact.rb public
```

- `SITE_BASE_ARTIFACT_MAX_BYTES` conserva la posibilidad de fijar un presupuesto interno, pero queda desactivado por defecto.
- `CATASTRO_SITE_MAX_BYTES` permite fijar un techo específico si aparece una restricción real; por defecto hereda los 1.000 MiB de Pages y reemplaza el antiguo hard stop local de 60 MB.
- Los presupuestos de releases históricos se conservan como evidencia y se marcan con alcance histórico; no reemplazan este límite operativo.
- No se debe comparar `du -sh` con el límite: redondea y puede contar bloques asignados en vez de bytes lógicos.
- El margen de Pages se calcula como `1 - bytes_public/1048576000`.
- El margen de entradas se calcula como `1 - entradas_public/200000`.

## Medición exacta después del pipeline

La compresión depende del runner. Para el límite del job, la medida exacta es
`artifacts_file.size` de la API una vez que terminó el pipeline:

```bash
GITLAB_PROJECT_ID=57339918
GITLAB_PIPELINE_ID="$(curl -fsS \
  "https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/pipelines?ref=main&status=success&per_page=1" \
  | jq -r '.[0].id')"
curl -fsS \
  "https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/pipelines/${GITLAB_PIPELINE_ID}/jobs?per_page=100" \
  | jq '[.[] | select(.name == "build_site" or .name == "pages") | {id, name, size: .artifacts_file.size}]'
```

- El último pipeline exitoso anterior a este cambio, `2824519126`, produjo un ZIP de `39.858.951` bytes.
- El build local de este cambio produjo `59.850.844` bytes y `1.249` entradas sin comprimir.
- Las cuatro imágenes PNG derivadas para DEV.to suman `415.108` bytes.
- El consumo observado es 5,71 % del límite Pages por bytes y 0,62 % por entradas; el ZIP anterior consumió 3,80 % del límite de artefactos.

## Falsabilidad observada

| Criterio | Perturbación | Rojo observado | Recuperación verde |
|---|---|---|---|
| Bytes Pages | `SITE_ARTIFACT_MAX_BYTES=1` | `Artifact exceeds 1 bytes: 59850844`, exit 1 | `59850844/1048576000`, exit 0 |
| Entradas Pages | `SITE_ARTIFACT_MAX_ENTRIES=1` | `Artifact exceeds 1 entries: 1249`, exit 1 | `1249/200000`, exit 0 |
| Bytes Catastro | `CATASTRO_SITE_MAX_BYTES=1` | `Catastro SII Brecha exceeds 1 bytes: 12054913`, exit 1 | hereda `1048576000`, exit 0 |

El valor operativo debe ser el máximo de esas tres proporciones. Un fallo real se
diagnostica por la dimensión que lo produce: `413 Request Entity Too Large` para el
ZIP, rechazo de Pages por tamaño o entradas, cuota de almacenamiento del namespace,
espacio del runner, tiempo de build o rendimiento medido en el navegador. Esas señales
no se sustituyen por un umbral local arbitrario.
