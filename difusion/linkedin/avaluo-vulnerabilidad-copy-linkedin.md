# LinkedIn — Avalúo y vulnerabilidad en unidad vecinal

**Formato: video nativo.** Se descartó el carrusel: LinkedIn no admite documento y
video en el mismo post, y el video muestra la herramienta en uso, que es lo que
convierte a un lector en usuario del visor.

| | |
|---|---|
| Video | `assets/videos/catastro-sii-visor.mp4` — 1920×1080, 39,5 s, sin audio |
| Póster | `assets/images/avaluo-vulnerabilidad-unidad-vecinal/poster-visor-1280x720.jpg` |

El carrusel de 6 láminas queda disponible en `avaluo-vulnerabilidad-carrusel.html`
por si más adelante conviene una segunda entrada sin video. Se regenera con
`scripts/render-linkedin-carousel.sh`.

## Copy

> A diferencia de Mastodon y Bluesky, en LinkedIn **no hay un post previo** de este
> artículo. El copy no puede arrancar con «luego lo llevé a un visor» como si
> continuara algo: tiene que sostenerse solo. Las tres primeras líneas son lo
> único visible antes del «ver más», así que van sin preámbulo.

Crucé el avalúo fiscal de predios del SII con el índice de vulnerabilidad territorial del MDSF, a nivel de unidad vecinal.

Antes de llegar al cruce apareció algo que no buscaba: en varias comunas la cobertura de predios del catastro, contrastada contra las viviendas del Censo 2024, es baja y bastante discutible. Eso por sí solo condiciona cualquier lectura posterior.

Sobre el cruce mismo, la conclusión es más sobria de lo que esperaba: la relación entre vulnerabilidad y avalúo depende de entre qué se divide. Por hogar y por persona casi se desvanece. Por metro cuadrado aparece con fuerza a nivel nacional, y se atenúa al mirar solo unidades mayoritariamente urbanas. A priori no es evidente por dónde está el problema.

Así que armé un visor para recorrer las 346 comunas y que cada quien mire la suya. En el video se ve el flujo completo: eliges una comuna en el gráfico de burbujas, bajas al mapa de unidades vecinales y exploras sus resultados.

→ El visor, para explorar comuna por comuna:
3cucharadas.cl/catastro_sii_brecha/

→ El post, con el método completo, sus supuestos y sus límites declarados antes de mostrar cualquier color:
3cucharadas.cl/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/

Los datos comunales están en Parquet con su diccionario. La lectura es descriptiva: describe territorios agregados, no identifica causas ni dice nada sobre las personas que viven ahí.

#DatosAbiertos #PolíticaPública #Chile #GIS

## Notas de publicación

- **El video va nativo, no como enlace a YouTube.** LinkedIn penaliza el enlace
  externo y el nativo reproduce en el feed con autoplay silenciado, que es
  exactamente para lo que sirve un video sin audio.
- **Enlaces en el cuerpo, no en el primer comentario.** Ambas URLs son del mismo
  sitio; el objetivo es que la gente llegue, no maximizar impresiones.
- **Cuatro hashtags al final.** Más se lee a relleno.
- **No etiquetar instituciones** (SII, INE, MDSF). El post cuestiona la cobertura
  de un registro público; etiquetar al organismo convierte una lectura técnica en
  una interpelación, que no es el tono.
- **Accesibilidad**: el video es silente y no lleva subtítulos, así que para un
  lector de pantalla no comunica nada. El párrafo que describe el flujo —«eliges
  una comuna, bajas al mapa, exploras»— cumple esa función y por eso está en el
  cuerpo y no solo implícito en la imagen.

## Qué NO decir

- Que hay «una relación entre vulnerabilidad y avalúo» a secas. El hallazgo es que
  la relación **depende del denominador**: por hogar y por persona casi no existe.
  Afirmarla sin el matiz invita justo a la lectura que el post desarma.
- Cualquier cifra que no esté en el post. LinkedIn no valida esto —a diferencia
  del pipeline de Mastodon y Bluesky, que rechaza números ausentes de los
  metadatos— así que acá la disciplina es manual.
