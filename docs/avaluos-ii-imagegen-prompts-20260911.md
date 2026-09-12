# Avalúos II — hero y teaser

> **Sustituido el 12-09-2026.** La revisión humana determinó que esta primera dirección gris/teal no seguía la identidad Tokyo Night de las piezas IA ni los formatos editoriales del sitio. El par vigente, sus prompts y la evidencia están en [la corrección de título y sistema visual](avaluos-ii-title-visual-correction-20260912.md). Este documento se conserva como antecedente y no debe usarse como baseline.

Modo utilizado: herramienta integrada `image_gen`, una llamada por pieza. Ilustraciones conceptuales sin datos ni geografía real; las cifras y mapas del artículo mantienen sus fuentes independientes.

## Entregables y reproducción

- Hero: `assets/images/avaluos-ii/hero-catastro-residencial-v1-1942x809.png` y su versión WebP sin pérdida; generación nueva en 23,0 segundos.
- Teaser: `assets/images/avaluos-ii/teaser-catastro-residencial-v1-1672x941.png` y su versión WebP sin pérdida; derivación del hero en 27,4 segundos.
- Ambas salidas originales se conservaron en el destino de `image_gen` y se copiaron al repo. Dimensiones observadas, no garantías de una nueva ejecución.
- En ChatGPT web: usar el prompt del hero primero; luego adjuntar ese resultado al prompt del teaser. La referencia busca conservar la dirección de arte, pero una nueva ejecución puede producir otra imagen.
- Para reproducir la entrega local: mantener el arte generado y recodificar solo el formato con `magick entrada.png -define webp:lossless=true salida.webp`; verificar igualdad de píxeles como describe el informe. No se utilizó el CLI de generación de la skill.
- [Hashes y tamaños de los cuatro archivos](avaluos-ii-imagegen-assets-20260911.json), [verificación](avaluos-ii-editorial-consolidation-evidence.md) y [auditoría delegada](avaluos-ii-imagegen-diagnosis-20260911.md).

## Hero — prompt enviado

```text
Use case: stylized-concept.
Asset type: editorial hero for the bilingual Chilean data-journalism article "Avalúos II" on 3cucharadas. Generate one panoramic landscape image, approximately 2.4:1.
Primary request: an elegant conceptual architectural illustration about the gap between the physical residential city and its cadastral records, and the need to investigate that gap carefully.
Scene and subject: a restrained urban diorama on a dark charcoal ground, recognizably inspired by Chilean residential urban fabric without depicting any actual identifiable city or property. Low-rise homes and a few apartment buildings, subtle hillside terraces. Above part of the built fabric, one very thin translucent cadastral plane with fine parcel outlines is slightly offset from the buildings beneath. A few outlines remain unresolved, suggesting records to be checked rather than proven tax evasion. Make the relationship between tangible buildings and the incomplete abstract register immediately legible.
Style: premium architectural editorial illustration, precise and tactile, matte ceramic buildings, fine etched lines, controlled soft shadows, crisp large forms, understated contemporary financial-magazine art direction. Not a dashboard, infographic, blueprint screenshot or fantasy sci-fi city.
Composition: the actual Jekyll title is rendered by the website at the left. Keep the left 40 percent dark, calm and almost empty for readable white text; place the principal urban form in the right 60 percent. Allow safe margins and maintain meaning when cropped vertically for mobile. Avoid tiny busy decoration.
Palette: charcoal #10121D background, pale stone buildings, muted teal #55C4C0 cadastral lines, slate #98A8BD secondary surfaces, very sparse warm amber #F0B35B emphasis. Contemporary, restrained saturation.
Text: none. No letters, numerals, captions, logos, flags, seals, currency symbols or watermarks.
Constraints: this is clearly a conceptual illustration, not a real map or data visualization. No identifiable parcels, fake statistics, bar charts, accusatory imagery, money piles, officials, people, fences or stigmatizing depictions of informal settlements. No glowing cyberpunk or retro gradients.
```

## Teaser — prompt enviado con el hero como referencia local

```text
Use case: style-transfer.
Asset type: 16:9 landscape teaser and social preview for the same bilingual Avalúos II editorial article.
Input image: the provided image is the existing hero illustration and visual reference.
Change only composition and framing to create a compact teaser from this same architectural scene: bring a smaller cluster of its pale Chilean-inspired residential buildings and its translucent teal cadastral plane into the center; reduce empty space; the central relationship must be legible as a small 320-pixel thumbnail. Keep the whole principal cluster comfortably inside a central safe area so a slight social-card crop will preserve it. Request a 16:9 landscape canvas.
Preserve the charcoal #10121D background, matte pale stone, muted teal #55C4C0 linework, slate #98A8BD, sparse amber #F0B35B, precise premium architectural style, soft light, and restrained contemporary palette. Simplify peripheral structures rather than adding new narrative objects. Keep both tangible houses and the partially unresolved cadastral plane visibly distinct.
No title or any other text, letters, numerals, charts, symbols, logos, official seals, money, people, or watermarks. It remains a clearly conceptual illustration of a cadastral discrepancy to investigate, not an actual map or a claim that any identifiable property evades taxes.
```
