# Revisión editorial completa III–IV: ocho fuentes ES/EN
Estado documental: LISTO. Origen Codex → Claude Code, CLI claude-bridge, modelo sonnet, 2026-11-08.
PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev15. D7/D10 verificados; P1/D8 reabiertos por figuras; D9 revisión adversarial activa; P4 publicación verificada pendiente.
HANDOFF-TRACE: Codex → Claude Code vía claude-bridge CLI, sonnet.

## Alcance estricto y obligatorio
La revisión anterior de figuras dio REQUEST_CHANGES y admitió NO revisar la prosa completa. El usuario pidió revisión adversarial de TODO. Tu unidad ahora es únicamente las OCHO fuentes textuales listadas en `inputs-before.json` de este directorio. Léelas COMPLETAS (sin limitarte al diff) y devuelve inventario de ocho rutas efectivamente revisadas. No revises gráficos/generadores/gates: otro pase resuelve sus defectos en paralelo. No edites archivos. No publiques.

## Decisiones y criterio
- Prosa adulta clara, sin etiquetas ELI5/en simple como estilo; hilo conductor, preámbulo con motivación/método crítico/conclusión principal, cierre con recapitulación/desafíos.
- Cuerpo principal conciso, anexos retienen evidencia y método. Verificar coherencia del traslado: mismo hecho y mismo límite, enlaces/identidad/permalink conservados. Chicago/Deusto es guía editorial, no excusa para inventar regla de blog ni exigir estilo APA.
- III: +9,11 histórico distinto a +5,29 en2016–19; cotas recientes[−1,15;10,98]inconclusas; receptor−3,35descriptivo.
- IV: abrir2009–2022/14cohortes;2016–19subventana de modelos; no extrapolar; −0,29 diferencia no tasa,CI[−2,64;2,06]; IP/CFT−2,09condicional vsDiD−2,59p0,28con12tratados; universidad+1,98CIcruzacero,no sustituciónidentificada; −13,24modelado vs−14,64bruto denominadoresdistintos; G1−12,26vs−0,26gruposreestimados,nodevenir mismosalumnos; D1−D2composición,nocertificaciónjurídica.
- Datos de cotejo disponibles en assets/data/tesis-post4/*.json y CSV de assets/images/tesis-post3/ y tesis-post4/. No recomputar ciencia ni inventar datos. Verificar ES/EN semánticamente, no solo números.
- Cambios gráficos se ejecutan en paralelo, fuentes textuales congeladas para esta revisión. La prosa IV ya añade CI2016–2019[−7,54;+2,25]enpanoramalongitudinal (existenteenbody/tabla).

## Salida
`REVIEW_VERDICT: APPROVE` o `REVIEW_VERDICT: REQUEST_CHANGES`. Hallazgos concretos archivo:línea, gravedad, corrección y evidencia; separar bloqueos de observaciones opcionales. Inventario8/8 y hashes si los comprobaste. Declarar límites sin presentar revisión parcial como completa. No aceptar consenso entreagentescomo evidencia. Cierre PLAN_STATE v2 / HANDOFF-TRACE: / MODEL-REPORT:. Los defects de figuras de la revisión previa quedan fuera de TU unidad, no impiden aprobar texto si texto cumple; el integrador exige ambas aprobaciones antes de publicar.
