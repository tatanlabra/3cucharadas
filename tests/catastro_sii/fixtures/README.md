# Avalúos II: ancla de metadatos de `main`

`avaluos_ii_release_baseline.json` separa dos autoridades que antes se trataban como una sola:

- El `baseline.json` de `catastros_sii` conserva el corte histórico `10c1b7b` y los hashes de 781 archivos. No se modifica.
- `81c7449b` era `main` en GitLab y GitHub al verificarlo el 2026-10-02. Su front matter incorpora la fecha de revisión en ES/EN y los metadatos de audio en ES.

El test exige que ambos posts actuales igualen **íntegramente** el front matter de `81c7449b`. Además, fija el SHA-256 del baseline histórico y el delta exacto de front matter entre ambas revisiones; comprueba título, fecha original, idioma, `ref`, permalink y todas las referencias protegidas. Así se aceptan solo las adiciones ya versionadas, sin quitar la protección de los campos previos ni modificar el proyector ligado por hash a sus salidas.

Falsación observada: `project_residential_extension.py --check --baseline <baseline histórico>` terminó con código 1 por el front matter cambiado; el mismo `--check` con esta ancla terminó con código 0. `test_front_matter_tampering_fails_closed` altera el título solo en memoria y confirma el rechazo. Un nuevo cambio editorial de estos posts requiere actualizar deliberadamente esta ancla y repetir ambas pruebas; el estado de los remotos del 2026-10-02 no concede aprobación futura.
