# Política experimental de Nushell

Aplica Nushell de forma selectiva cuando un JSON exige varias transformaciones
estructuradas: validar invariantes, filtrar, ordenar, agregar y reducir una
respuesta. Para ese caso usa `nu -n -c` y termina en `to json`.

No uses Nushell para leer Parquet, extraer un único campo, buscar texto ni para
explicar un límite conceptual. Para esas tareas usa Python/DuckDB, `jq`/`rg` o
responde directamente. No cambies archivos.
