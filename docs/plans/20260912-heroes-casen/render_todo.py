#!/usr/bin/env python3
"""Render the human progress view from the contract, never from remembered status."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
contract = json.loads((root / 'contract.json').read_text())
labels = {'P0':'Fuentes e inventario congelados','D1':'CASEN reproducible y protección de tipos R',
          'U1':'Hero y transparencia IA compartidos','H1':'Familias visuales, metadatos y tarjetas móviles',
          'V0':'Figuras fiscales Python y tipografía portátil','G1':'Revisión documental y respaldo DeepSeek',
          'D2':'Revisión científica independiente Claude','V1':'Figura CASEN y datos verificables',
          'E1':'Relato bilingüe e integración','R1':'Revisión adversarial del candidato',
          'Q1':'QA final y commits locales'}
states = {'verified':'[x]', 'pending':'[ ]', 'in_progress':'[~]', 'partial':'[~]', 'blocked':'[ghost]', 'incident':'[!]'}
lines = ['# Avance verificable — héroes, CASEN y figuras', '',
         'Derivado de contract.json. El verificador exige criterios cubiertos, dependencias y hashes vigentes. Sin push ni publicación.', '',
         '| Tarea | Estado | Entrega | Evidencia |', '|---|---|---|---|']
for task in contract['tasks']:
    state = states[task['status']]
    assert state == contract['todo_state'][task['id']]
    evidence = task.get('evidence')
    link = f'[Recibo]({evidence})' if evidence and task['status'] == 'verified' else 'Pendiente de aceptación vigente'
    lines.append(f"| {task['id']} | {state} {task['status']} | {labels[task['id']]} | {link} |")
lines += ['', 'G1 es complementaria. Su fallo o informe recuperado no cuenta como revisión externa aprobada; véase [disposición](evidence/G1/disposition.md).', '',
          'El verificador original aceptaba 27 casos prohibidos reproducidos. La corrección satisface 49 casos: 6 aceptaciones válidas y 43 rechazos. [Evidencia](evidence/contract-assurance/receipt.json). Esto verifica enlaces e integridad; no sustituye la revisión científica ni visual.']
(root / 'TODO.md').write_text('\n'.join(lines) + '\n')
