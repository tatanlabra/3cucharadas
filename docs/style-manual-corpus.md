# Corpus local de manuales de estilo

- `scripts/style_manual_corpus.py` crea un corpus privado y consultable desde PDF locales.
- `auto` intenta Docling primero y declara en el manifiesto si debió usar `pdftotext`.
- La salida contiene texto protegido por derecho de autor: se genera fuera de `_site` y no se versiona.
- Cada fragmento conserva archivo, hash de origen y páginas cuando el extractor las entrega.

```bash
python3 scripts/style_manual_corpus.py build \
  --source-dir "$STYLE_MANUAL_DIR" \
  --output-dir /tmp/3cucharadas-style-manual-corpus

python3 scripts/style_manual_corpus.py search \
  --corpus /tmp/3cucharadas-style-manual-corpus/chunks.jsonl \
  --query "tablas notas fuentes tamaño tipografía"
```

El corpus ayuda a localizar reglas; no convierte una coincidencia léxica en una decisión editorial. Toda regla aplicada debe citar manual y páginas, distinguir el original inglés de la adaptación Chicago-Deusto y conservar la evidencia contraria.

El constructor rechaza cualquier salida ubicada dentro del repositorio. Si Docling no conserva páginas en su exportación Markdown, el corpus registra esos campos como `null` en vez de inventar una página 1.
