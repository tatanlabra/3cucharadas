---
name: 3cucharadas Cuaderno de Evidencia
colors:
  background: "#faf7f0"
  on-background: "#26354c"
  surface: "#faf7f0"
  on-surface: "#26354c"
  surface-variant: "#f1ede4"
  on-surface-variant: "#4c596b"
  primary: "#176b7b"
  on-primary: "#ffffff"
  secondary: "#8a5a00"
  on-secondary: "#ffffff"
  error: "#a83b55"
  on-error: "#ffffff"
  outline: "#9c9588"
  background-dark: "#161616"
  on-background-dark: "#f2f5f8"
  surface-dark: "#161616"
  on-surface-dark: "#f2f5f8"
  surface-variant-dark: "#222222"
  on-surface-variant-dark: "#c4cbd3"
  primary-dark: "#64d8e9"
  secondary-dark: "#f1c75b"
  error-dark: "#f08ca3"
  outline-dark: "#9ca3ad"
typography:
  headline-lg:
    fontFamily: Fira Sans
    fontSize: 22px
    fontWeight: "700"
    lineHeight: 29px
  headline-md:
    fontFamily: Fira Sans
    fontSize: 18px
    fontWeight: "700"
    lineHeight: 25px
  body-md:
    fontFamily: Fira Sans
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 24px
  label-sm:
    fontFamily: Fira Sans
    fontSize: 15px
    fontWeight: "400"
    lineHeight: 20px
  data-strong:
    fontFamily: Fira Sans
    fontSize: 16px
    fontWeight: "700"
    lineHeight: 20px
rounded:
  sm: 2px
  DEFAULT: 4px
  full: 9999px
spacing:
  unit: 4px
  compact: 8px
  control: 16px
  panel: 24px
components:
  figure-editorial:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
  data-label:
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.label-sm}"
  data-strong:
    textColor: "{colors.on-surface}"
    typography: "{typography.data-strong}"
  uncertainty-note:
    backgroundColor: "{colors.surface-variant}"
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: "{spacing.control}"
  body-copy-dark:
    backgroundColor: "{colors.background-dark}"
    textColor: "{colors.on-background-dark}"
    typography: "{typography.body-md}"
  figure-editorial-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-surface-dark}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
  uncertainty-note-dark:
    backgroundColor: "{colors.surface-variant-dark}"
    textColor: "{colors.on-surface-variant-dark}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: "{spacing.control}"
  evidence-mark-dark:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.background-dark}"
    typography: "{typography.data-strong}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
  caution-mark-dark:
    backgroundColor: "{colors.secondary-dark}"
    textColor: "{colors.background-dark}"
    typography: "{typography.data-strong}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
  contradiction-mark-dark:
    backgroundColor: "{colors.error-dark}"
    textColor: "{colors.background-dark}"
    typography: "{typography.data-strong}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
  rule-dark:
    backgroundColor: "{colors.outline-dark}"
    textColor: "{colors.background-dark}"
    rounded: "{rounded.sm}"
    padding: "{spacing.compact}"
---

# 3cucharadas — Cuaderno de evidencia

## Brand & Style

Una visualización debe leerse como una página anotada del artículo, no como un tablero incrustado. La marca surge del ritmo editorial: evidencia principal, incertidumbre y límite de interpretación.

## Colors

El fondo conserva el papel cálido y el negro cálido del sitio. Teal identifica la evidencia principal; ocre identifica incertidumbre o cautela; magenta se reserva para contradicción o falla. Ninguna categoría depende solo del color.

## Typography

Fira Sans une figuras, tablas y prosa. Toda etiqueta informativa se renderiza a 15 px o más en escritorio y 16 px o más en móvil; cifras usan peso 700 y numerales tabulares.

## Layout & Spacing

Figuras y tablas comparten la medida de 620 px de la prosa. La composición es vertical, con rotulado directo y una retícula de 4 px; no se conserva un lienzo panorámico cuando obliga a reducir el texto.

## Elevation & Depth

La jerarquía usa espacio, filetes y cambios mínimos de superficie. No hay sombras decorativas ni una segunda tinta negra alrededor de las figuras.

## Shapes

Los radios no superan 4 px. Círculos, cuadrados, líneas continuas y achurados codifican series e incertidumbre además del color.

## Components

La figura editorial no repite en su interior el título ya presente en el relato o pie. Las tablas caben en la columna en escritorio; en móvil solo desplazan cuando el contenido no admite una reexpresión semántica accesible.

## Do’s and Don’ts

Usar rotulado directo, cifras tabulares, filetes sutiles y una visualización elegida por la pregunta. Evitar tarjetas para cada idea, leyendas flotantes, paletas arcoíris, gradientes, pictogramas decorativos y texto reducido para salvar una composición demasiado ancha.
