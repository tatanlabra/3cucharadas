---
name: 3cucharadas Data Visuals Baseline
colors:
  background: "#faf7f0"
  on-background: "#26354c"
  surface: "#fffaf0"
  on-surface: "#26354c"
  surface-variant: "#fffaf0"
  on-surface-variant: "#526176"
  primary: "#176b7b"
  on-primary: "#ffffff"
  secondary: "#6755c4"
  on-secondary: "#ffffff"
  error: "#a83b55"
  on-error: "#ffffff"
  outline: "#cbd3d9"
typography:
  headline-lg:
    fontFamily: Fira Sans
    fontSize: 24px
    fontWeight: "700"
    lineHeight: 32px
  body-md:
    fontFamily: Fira Sans
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 24px
  label-sm:
    fontFamily: Fira Sans
    fontSize: 12px
    fontWeight: "400"
    lineHeight: 16px
rounded:
  sm: 8px
  DEFAULT: 12px
  full: 9999px
spacing:
  unit: 8px
  compact: 8px
  control: 16px
  panel: 24px
components:
  figure-panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.DEFAULT}"
    padding: "{spacing.compact}"
  data-label:
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.label-sm}"
---

# 3cucharadas Data Visuals Baseline

## Brand & Style

Línea base observada del Post III: paneles tipo tablero, seis colores categóricos y lienzos 16:9 que se reducen dentro de la columna editorial.

## Colors

El teal, el violeta, el magenta, el ocre y dos colores adicionales compiten por atención; claro y oscuro se resuelven en el snapshot DTCG separado.

## Typography

Fira Sans conserva continuidad con el sitio. Las etiquetas nominales de 12 a 14 px pierden legibilidad al reducir el SVG de 1.600 px a la columna de lectura.

## Layout & Spacing

Las figuras usan composición panorámica y paneles internos; las tablas pueden alcanzar 748 px dentro de una columna de 620 px.

## Elevation & Depth

El panel exterior usa borde, radio de 12 px y sombra; las capas internas vuelven a usar cajas y superficies.

## Shapes

Predominan rectángulos redondeados y tarjetas. Las formas también diferencian algunas series, pero no gobiernan la composición.

## Components

La figura se trata como un panel autónomo y la etiqueta como texto auxiliar pequeño.
