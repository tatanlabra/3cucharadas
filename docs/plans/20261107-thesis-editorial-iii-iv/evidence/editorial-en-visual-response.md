# Respuesta editorial EN: textos alternativos y pies de figura

PLAN_STATE v2: F3 adaptación EN congelada tras corrección visual; F4 build/QA pendiente del integrador.

HANDOFF-TRACE: Codex integrador → adaptador EN vía collaboration → siete pares de figuras cotejados con ES congelado.

- Figuras III 1/2 y anexos A1/A2, IV 1 y anexo A1/A2: revisé `alt` y `figcaption` contra los homólogos ES aprobados.
- III figura 1, `alt`: «similar» sustituye «balanced» para conservar el límite de comparabilidad SEP del ES.
- IV figura 1, `alt`: la escalera se describe como comparaciones ajustadas; IP/CFT es una diferencia condicionada al modelo y los intervalos de básica superior incluyen cero.
- IV anexo figura A1, `alt` y `figcaption`: D2 identifica episodios depurados; la composición observada no verifica el estado jurídico individual.
- Los demás `alt` y pies conservan el mismo hecho, unidad, período y límite del ES; no requirieron cambios.
- `ruby scripts/verify_thesis_post3.rb`: exit 0, `POST3_VALID lang=both`; advertencia `UNCOMMITTED_FILE_HASHES` conservada.
- `ruby scripts/verify_thesis_post4.rb`: exit 0, `THESIS_POST4_VERIFIED lang=both fixture=none`.
- `git diff --check`: exit 0. Requiere nuevo build para actualizar HTML renderizado; no ejecuté publicación, commit ni push.
