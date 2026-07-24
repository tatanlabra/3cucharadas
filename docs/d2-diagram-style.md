# D2 diagram style

Receta reusable para diagramas D2 editoriales en `3cucharadas`, basada en la figura de memoria validable del post multiagente II.

## Render

Usar ELK con tema oscuro y espaciado intermedio:

```bash
DEBUG=0 d2 --theme=200 --layout=elk --elk-nodeNodeBetweenLayers=20 --elk-edgeNodeBetweenLayers=12 --pad=6 input.d2 output.svg
```

Parametros clave:

- `--theme=200`: base oscura tipo mauve, consistente con la paleta nocturna del sitio.
- `--layout=elk`: mejor para cajas horizontales y flechas limpias que `dagre` en estos flujos.
- `--elk-nodeNodeBetweenLayers=20`: flechas visibles sin exceso de aire vertical.
- `--elk-edgeNodeBetweenLayers=12`: separacion suficiente entre bordes, nodos y etiquetas.
- `--pad=6`: margen exterior ajustado para que el SVG no parezca una tarjeta inflada.

## Tipografia

- Cajas: `style.font-size: 11`.
- Etiquetas de flechas: `style.font-size: 9`.
- Color principal de texto: `#f8f8f2`.
- Color de etiquetas de flecha: `#cdd6f4`.

## Paleta

```d2
classes: {
  input: {
    style.fill: "#282a36"
    style.stroke: "#8be9fd"
    style.stroke-width: 2
    style.font-color: "#f8f8f2"
    style.font-size: 11
  }
  process: {
    style.fill: "#303446"
    style.stroke: "#bd93f9"
    style.stroke-width: 2
    style.font-color: "#f8f8f2"
    style.font-size: 11
  }
  canonical: {
    style.fill: "#263f35"
    style.stroke: "#50fa7b"
    style.stroke-width: 2
    style.font-color: "#f8f8f2"
    style.font-size: 11
  }
  derived: {
    style.fill: "#3f3328"
    style.stroke: "#ffb86c"
    style.stroke-width: 2
    style.font-color: "#f8f8f2"
    style.font-size: 11
  }
  output: {
    style.fill: "#392b3f"
    style.stroke: "#ff79c6"
    style.stroke-width: 2
    style.font-color: "#f8f8f2"
    style.font-size: 11
  }
}
```

## Composicion

- Usar `direction: down`.
- Preferir cajas horizontales: titulo y detalle en una linea si cabe.
- Evitar mas de dos lineas por nodo; usar `/` y `;` para comprimir relaciones.
- Mantener las flechas con texto solo cuando aporta semantica, no en cada transicion.
- Para flujos de 7 a 9 nodos, una salida cercana a `421x742` queda balanceada.

## Insercion en posts

Usar una clase especifica para no afectar figuras globales:

```html
<figure class="align-center memory-flow-figure">
  <img src="{{ '/assets/images/.../diagrama.svg' | relative_url }}" alt="..." loading="lazy" decoding="async">
  <figcaption><strong>Figura 1</strong> — Leyenda. Nota: aclaracion metodologica breve.</figcaption>
</figure>
```

CSS recomendado:

```scss
.memory-flow-figure img {
  width: min(70%, 42rem);
  max-width: 100%;
}

@media (max-width: 47.99em) {
  .memory-flow-figure img {
    width: 100%;
  }
}
```

## Revision rapida

```bash
rsvg-convert output.svg -o /tmp/d2-preview.png
```

Comprobar:

- fondo oscuro embebido en el SVG;
- texto legible en modo claro y nocturno;
- cajas sin texto cortado ni solapado;
- flechas suficientemente largas para entender la secuencia;
- figura al 70% aproximado en desktop y a 100% en movil.
