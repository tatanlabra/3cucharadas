# F20 — apoyo a la decisión y puente científico

Fecha: 2026-10-12. Estado: implementación local en revisión independiente.

## Separación epistémica

| Clase | Aplicación | Límite |
|---|---|---|
| HECHO | El Post II describe eventos, matrículas, muestras, distancias y alcance institucional documentado. | No identifica destinos individuales ni efectos de cerrar, abrir o cambiar administración. |
| DEDUCCIÓN | Si una señal admite explicaciones rivales y no construye contrafactual, no autoriza una decisión automática ni una atribución causal. | Depende de que las premisas y restricciones declaradas sigan siendo verdaderas. |
| INDUCCIÓN | Los patrones repetidos orientan diagnóstico dentro de la población y período observados. | No se generalizan a otra red o territorio sin soporte y período explícitos. |
| ABDUCCIÓN | Menor matrícula puede ser compatible con demografía, transferencias, movilidad, competencia o anticipación administrativa. | La explicación preferida debe discriminarse con datos adicionales y descartarse si contradice su patrón temporal o territorial. |
| HIPÓTESIS | La cadena insumos–actividades–productos–resultados–impacto organiza una evaluación futura. | El post no acredita que la cadena funcione ni que produzca aprendizaje o equidad. |

## Decisiones implementadas

- La regla pública es `observación → diagnóstico → decisión`, no `observación → cierre`.
- SLEP queda limitado a su propia red; otros sostenedores a sus establecimientos; MINEDUC/DEP a observación y apoyo sistémico.
- La matriz exige evidencia adicional antes de validar evento, diagnosticar matrícula, planificar transición o evaluar resultados.
- Se muestran falso positivo, falso negativo e IVE-SINAE como indicador escolar agregado, no pobreza individual.
- El registro de claims usa esquema 2 y añade AP-037–AP-040 con uso permitido/prohibido, evidencia, nivel de resultado y destino científico.
- DEC-REL-007 conserva separados el artículo H1-H3, la pieza MR1-MR4 y una futura evaluación de política.
- AP-017 queda `PUBLICATION_PENDING`; una URL local o un build no prueba publicación.

## Rojo → verde

| Superficie | Rojo observado | Verde observado |
|---|---|---|
| Ruta canónica del Post II | `scripts/254_validate_article_claims.py --validate`, exit 2 por ruta del 17 de septiembre. | Registro y derivados sincronizados al 11 de octubre, exit 0. |
| Reglas epistémicas | Diez tests deliberadamente inválidos: inferencias sin soporte, etapa omitida, prohibiciones ausentes, destino incorrecto, publicación sin recibo y descarte genérico; 10 failed, exit 1. | `tests/test_article_claim_register.py`: 22 passed, exit 0. |
| Uso público del blog | Siete canarios de matriz, actor SLEP en ES/EN, IVE, ranking y salvaguarda causal: `EXPECTED_FAIL`, exit 1. | Gate completo ES/EN: `PASS`, exit 0. |
| Freeze científico | Validación posterior al cambio: exit 2 por hash obsoleto. | 18 pruebas, diez probes negativos, Ruff y validación: exit 0/2 según contrato; hash vigente `3a519f16…`. |
| Artefacto visual | Primer intento: socket local denegado por sandbox, `EPERM`, exit 1 después de build verde. | Mismo gate con socket acotado: Jekyll, 70.906.162 bytes, 1.510 entradas, 24/24 páginas, 12/12 SVG y 2/2 fallbacks, exit 0. |

## Fuentes institucionales

- [Ley 21.040](https://www.bcn.cl/leychile/navegar?idNorma=1111237): cobertura y continuidad de trayectorias dentro del territorio y establecimientos bajo dependencia del SLEP.
- [Plan Anual Local 2026](https://dep.gob.cl/pal-2026/): planificación de apoyo técnico, infraestructura, personal, cursos y matrícula.
- Ambas fuentes delimitan funciones; no demuestran superioridad de una modalidad ni autorizan una decisión sobre una escuela específica.

## Revisión independiente E-41

- Claude Opus 5.5 emitió `REQUEST_CHANGES`: 0 altos, 3 medios, 6 bajos y 2 menores.
- Se aceptaron M1–M3 y B1–B6: cobertura territorial, precisión MINEDUC/DEP/PAL, cinco niveles de teoría de cambio, alternativa de calidad percibida y gates de estructura/paridad.
- AP-040 pasó a `DEFERRED_FUTURE_PRODUCT`; AP-017 no puede pasar a `PUBLICATION_VERIFIED` sin URL canónica HTTP 200, fecha y hash de fuente.
- La respuesta original queda en `archivo/handoffs/.originals/response.retXGU.txt`, SHA-256 `172cb0b7720656f96f0b091a83620c0a11c58c6633a6050d7bdfa339257671eb`.
- La rerevisión estrecha confirmó seis de siete remediaciones y reabrió R1–R2; respuesta bajo custodia en `response.rk1A6T.txt`, SHA-256 `e8f0c470d58d29114da4779d580343b026ad17b68cf41bd9ae635024aac0bba5`.
- La revisión siguiente confirmó R2 y volvió a falsar R1: el audit había sido generado antes del freeze y retenía su hash anterior; respuesta `response.UX1ntB.txt`, SHA-256 `9ee2377c12b88406ed499db983f1e8642b36129a2cfa7598a8b53a50003a9d5e`.
- R1 quedó cerrado en el orden convergente `freeze → article claims`: primero se observó `254 --validate` rojo exit 2, después el audit regenerado y ambos validadores salieron 0.
- R2 quedó cerrado con fragmentos obligatorios ES/EN, prohibición `commune_wide_slep_authority` en todo claim de alcance SLEP y canarios específicos observados rojos.
- La microrevisión final reprodujo 37 hashes de evidencia, 20 hashes del contrato, claims y freeze en exit 0 y emitió `APPROVE`; respuesta `response.E2R5gt.txt`, SHA-256 `80f2f95b8ebdbb9f023b0ccd3f95f1750559f011324fedaff3437bd8fb9e0058`.
- El gate de preview ejecuta ahora `freeze --validate` y después `article claims --validate` sobre el mismo candidato, antes del gate Jekyll.

## Cierre del plan

| Estado | Resultado |
|---|---|
| Implementado | E-38–E-42 y E-45: matriz bilingüe, claims esquema 2, revisión independiente, candidato limpio y H1 portable. |
| Parcial | H1 espera aprobación humana; E-46 mantiene el puente científico sin commit hasta adjudicar ocho evidencias y sus generadores. |
| No implementado | Push, despliegue, paridad pública y difusión. |
