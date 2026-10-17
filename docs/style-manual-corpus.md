# Matriz de estilo para los posts I y II

## Alcance y custodia

- Esta matriz aplica criterios editoriales al cuerpo, títulos, encabezados, números, puntuación y transiciones de los posts I y II.
- Las referencias bibliográficas conservan su formato actual; una migración bibliográfica completa queda fuera de este cierre.
- Los PDF y el corpus de búsqueda permanecen fuera del repositorio; no se versiona texto extraído de los manuales.
- Las reglas siguientes son paráfrasis operativas, no transcripciones de los manuales.

## Recibo de fuentes

| Alias | Edición | SHA-256 | Páginas PDF | Uso |
|---|---|---|---:|---|
| `CD-primary` | *Manual de estilo Chicago-Deusto*, edición digital adaptada al español, 2013 | `45d1908efedaf582c89c56494ae862736d252434bbf63c98294ee76ecebf7a34` | 979 | Autoridad principal para el español |
| `CD-scan` | *Manual de estilo Chicago-Deusto*, escaneo con OCR, 2013 | `437fb5d032cdc0ddff87ebd7121d45435ee26b6542119110ea39aee81ae5a38c` | 966 | Contraste visual; su paginación no es canónica |
| `CMOS18` | *The Chicago Manual of Style*, 18.ª edición, 2024 | `4b61b8f7cbf520b5c99f34cc7ef3c15dbb0eb7fbee82e0a082f276c8d66abd86` | 1.208 | Autoridad principal para el inglés |

## Reglas aplicadas

| Área | Referencia | Regla operativa para estos posts |
|---|---|---|
| Párrafos | `CD-primary` §§2.10–2.11, p. impresa 62 / PDF 83; `CMOS18` §§2.14–2.15, pp. 70–71 / PDF 92–93 | Cada párrafo desarrolla una unidad semántica; no se simula estructura con saltos manuales. La extensión breve es una decisión de voz del blog, no una regla atribuida a Chicago. |
| Títulos | `CD-primary` §§8.154–8.156, pp. 392–394 / PDF 413–415; `CMOS18` §§8.157–8.166, pp. 568–572 / PDF 590–594 | Se usa estilo oración y se conservan de forma consistente `(parte I)`, `(parte II)`, `(part I)` y `(part II)`. |
| Encabezados | `CD-primary` §6.14, p. 256 / PDF 277; `CMOS18` §2.87, p. 101 / PDF 123 y §6.14, p. 384 / PDF 406 | La jerarquía responde al significado, no al tamaño visual; no lleva punto final y conserva los signos de interrogación cuando corresponde. |
| Números | `CD-primary` §§9.2–9.7, pp. 414–416 / PDF 435–437; §§9.18–9.20, pp. 420–421 / PDF 441–442; §9.30, p. 424 / PDF 445; §9.55, p. 430 / PDF 451 | Resultados, años y porcentajes se expresan con cifras. En español se usan `3.800`, `5,9` y `20 %`; en inglés, `3,800`, `5.9` y `20%`. La marca «3 Cucharadas» conserva su grafía. |
| Puntuación | `CD-primary` §§6.16–6.18, p. 257 / PDF 278; §6.25, p. 260 / PDF 281; §6.42, p. 265 / PDF 286; §§6.50 y 6.55, pp. 267 y 269 / PDF 288 y 290; §6.78, p. 275 / PDF 296 | Los conectores e incisos se puntúan por su función; los dos puntos siguen una introducción completa y la raya se reserva para una relación que la justifique. |
| Transiciones | `CD-primary` §§5.121–5.138, pp. 234–238 / PDF 255–259; `CMOS18` §5.209, p. 302 / PDF 324 y §§5.249–5.251, pp. 316–317 / PDF 338–339 | Las series mantienen paralelismo y los puentes nombran la pregunta pendiente; se evitan conectores mecánicos y repetidos. |
| Registro bilingüe | `CD-primary` prefacio, pp. XIII–XV / PDF 14–16; §§5.139–5.143, pp. 239–240 / PDF 260–261; §§5.148–5.152, pp. 247–248 / PDF 268–269; `CMOS18` §§5.255–5.267, pp. 371–376 / PDF 393–398 y §§11.1–11.14, pp. 674–680 / PDF 696–702 | Se traduce la intención y el estado epistémico, no la sintaxis. SLEP y SAE se definen en la primera aparición y personas o territorios no se reducen a etiquetas. El registro inglés es híbrido institucional: conserva ortografía británica de forma deliberada y aplica Chicago a estructura, puntuación y uso editorial, sin convertir la ortografía estadounidense por defecto en una exigencia. |

## Aplicación verificable

- El Post I conserva la primera persona responsable, distingue hallazgo, explicación y límite, y avanza de la reconstrucción a su uso público.
- El Post II elimina transiciones de bitácora, mantiene paralelos los resultados iniciales y hace visible la pregunta que conduce a cada cucharada.
- Las versiones en español e inglés mantienen el mismo universo, período, magnitudes y cautela causal, aunque varíen su ritmo y léxico.

## Consulta privada del corpus

- `scripts/style_manual_corpus.py` crea un corpus consultable desde PDF locales y prefiere Docling, con `pdftotext` como fallback declarado.
- La salida contiene texto protegido por derecho de autor: debe quedar fuera del repositorio y de `_site`.
- Cada fragmento conserva archivo, hash de origen y páginas cuando el extractor las entrega; una página ausente se registra como `null`.

```bash
python3 scripts/style_manual_corpus.py build \
  --source-dir "$STYLE_MANUAL_DIR" \
  --output-dir /tmp/3cucharadas-style-manual-corpus

python3 scripts/style_manual_corpus.py search \
  --corpus /tmp/3cucharadas-style-manual-corpus/chunks.jsonl \
  --query "tablas notas fuentes tamaño tipografía"
```

El corpus localiza reglas; no convierte una coincidencia léxica en una decisión editorial. El constructor rechaza salidas dentro del repositorio.
