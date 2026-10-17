# Recibo de falsificación observado

Fecha: 2026-10-17T18:05:01-03:00

| Gate | Perturbación | Exit | Señal observada |
|---|---|---:|---|
| AC-F0 | Contrato con `plan_contract_version` inválida | 2 | `plan_contract.py solo acepta plan_contract_version: 1` |
| AC-F1 | Distancia obsoleta del caso autoral | 1 | `CONTRACT_PROBE_EXPECTED_REJECTION author-case-old-distance` |
| AC-F1 | Portabilidad byte a byte promovida entre hosts | 1 | `CONTRACT_PROBE_EXPECTED_REJECTION cross-host-byte-identity-promoted` |
| AC-F2 | Reinyección de Lo Prado, distancia exacta en el cuerpo y regresión a seis puntos en anexo EN | 1 | Tres `EXPECTED_FAIL`: caso retirado, fuga de distancia y anexo bilingüe obsoleto |
| AC-F3 | Reinyección de casos sistemáticos en el visor principal | 1 | `EXPECTED_FAIL` y `el visor principal conserva casos sistemáticos retirados` |
| AC-F4 | Overflow documental inyectado | 1 | `EXPECTED_FAIL` y `document-overflow` |

Cada comando se ejecutó sin tubería; los códigos corresponden al proceso probado.
