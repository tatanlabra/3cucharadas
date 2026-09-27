# Contabilidad de hipótesis — post I de recreación de tesis

## Decisión editorial

El balance de 50 hipótesis se publica con sus cuatro desenlaces, no con un
atajo binario entre refutadas y sobrevivientes. Ese atajo borraría dos
categorías; el registro F4 primario permite ahora nombrarlas sin inventar una
partición.

## Evidencia disponible

- `tesis_mae_mejorada@e4c8d924691bf40763897fd61ad6df7459fab82c`,
  `audit/f4_divergence_adjudication.json`, blob Git
  `98654dc39e68ed4735aeb20f7deb1c277421e2ee`, SHA-256
  `b6b38eb4d6377333d8def1ad5044c844ffe530b460ac178814753550c9a37417`:
  50 filas y cuatro desenlaces mutuamente excluyentes al nivel de hipótesis:
  37 `REFUTADA`, 11 `SOSTENIDA`, 1 `PARCIAL` y 1
  `REFUTADA_PARA_ONCE_TERMINOS`.
- La última categoría conserva un matiz que la suma corta escondía: la
  hipótesis de divergencia queda refutada para once de catorce términos, pero
  dos varianzas y `l_simce` siguen divergentes; no se la puede convertir en
  una refutación simple sin perder información.
- El mismo commit, `audit/f5_judgment_registry.json`: 34 juicios sobre
  displays y claims: 15 calces correctos, 10 errores de 2014, cero errores
  conocidos en la salida canónica de 2026, un error a ambos lados, un calce
  heredado y siete límites o casos no adjudicables. Es otra unidad y no
  sustituye las 50 hipótesis F4.
- `audit/recreation_result_comparison_v2.json`, blob Git
  `ae578e1461865168270a8c48cb81cb82c7131589`, SHA-256
  `8bd336a3c443d95b8d08449b475fb688a71cfd7ffd2f584e2e37392d380827a2`:
  los nueve casos reabiertos terminan en 3 coincidencias, 2 diferencias y 4
  no comparables por diseño; los Cuadros 5–8 conservan una auditoría
  inferencial separada de la mera ejecución.

## Regla de mantenimiento

El total solo puede permanecer publicado si el verificador confirma hashes, 50
filas F4, 34 juicios F5 y los nueve estados terminales. Si cualquiera cambia, el
post vuelve a revisión técnica.
