# Caso agregado de tesis

Este experimento reutiliza la auditoría canónica de actividad temporal de la
reconstrucción de tesis. `export_fixture.py` reduce su salida a conteos anuales,
hash de fuente, invariantes y límites explícitos; no exporta microdatos ni
identificadores.

El A/B es una intervención: el control prohíbe Nushell y el tratamiento recibe
una política congelada que lo exige solo cuando corresponde. Son tres tareas,
dos brazos y cinco repeticiones. El resultado es descriptivo para este caso
real, no una estimación de rendimiento general ni una prueba de cierre
institucional.

```text
/opt/entornos/mamba312/bin/python export_fixture.py --tesis-root <tesis-root>
/opt/entornos/mamba312/bin/python -m unittest test_thesis_case.py
```
