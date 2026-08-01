# LinkedIn — Avalúo y vulnerabilidad en unidad vecinal

Carrusel: `avaluo-vulnerabilidad-carrusel.pdf` (6 láminas, 1080×1350).
Se regenera con `scripts/render-linkedin-carousel.sh difusion/linkedin/avaluo-vulnerabilidad-carrusel.html`.

## Copy

> Las tres primeras líneas son lo único que se ve antes del «ver más». Van sin
> preámbulo a propósito.

Crucé el avalúo fiscal de predios del SII con el índice de vulnerabilidad territorial del MDSF, a nivel de unidad vecinal.

Antes de llegar al cruce apareció algo que no esperaba: en varias comunas la cobertura de predios del catastro es baja y bastante discutible. Eso solo ya condiciona cualquier lectura posterior.

Y sobre el cruce mismo: la relación entre vulnerabilidad y avalúo depende de entre qué se divide. Por hogar y por persona casi se desvanece. Por metro cuadrado aparece con fuerza a nivel nacional, y se atenúa al mirar solo unidades mayoritariamente urbanas. A priori no es evidente por dónde está el problema.

Publiqué las dos cosas para que cada quien saque sus propias conclusiones:

→ El post, con el método completo, sus supuestos y sus límites declarados antes de mostrar cualquier color.
3cucharadas.cl/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/

→ El visor, para explorar comuna por comuna. Elige la tuya y revisa qué dice.
3cucharadas.cl/catastro_sii_brecha/

Los datos comunales están en Parquet con su diccionario. La lectura es descriptiva: describe territorios agregados, no identifica causas ni dice nada sobre las personas que viven ahí.

#DatosAbiertos #PoliticaPublica #Chile #GIS

## Notas de publicación

- **Enlaces en el cuerpo, no en el primer comentario.** El post no tiene enlace
  externo saliente que competir: ambas URLs son del mismo sitio y el objetivo es
  que la gente llegue, no maximizar impresiones.
- **El carrusel va como documento PDF**, no como imágenes sueltas: LinkedIn lo
  renderiza con paginador y cuenta el tiempo de lectura.
- **Cuatro hashtags**, al final. Más se lee a relleno.
- **No etiquetar instituciones** (SII, INE, MDSF). El post cuestiona la cobertura
  de un registro público; etiquetar al organismo convierte una lectura técnica en
  una interpelación, que no es el tono.

## Qué NO decir

- Que hay «una relación entre vulnerabilidad y avalúo» a secas. El hallazgo es que
  la relación **depende del denominador**: por hogar y por persona casi no existe.
  Afirmarla sin el matiz invita justo a la lectura que el post desarma.
- Cualquier cifra que no esté en el post. Las que aparecen en el carrusel
  —9.401.277, 271.150, 2,884%, 587,4 billones, 19,2%, 19,9%, 45,8%— están todas
  en el artículo y son verificables contra el Parquet publicado.
