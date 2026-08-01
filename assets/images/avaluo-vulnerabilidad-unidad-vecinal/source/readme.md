> **Dónde están los PNG máster.** Ya no viven acá. Pesaban 13,9 MB y versionarlos
> en el repo del sitio los dejaba para siempre en el historial de git sin que
> ninguna página los use: el sitio sirve sólo los derivados `.webp`.
>
> Se movieron a, siguiendo la gobernanza del workspace (`recursos/` = assets
> externos, ver `gobernanza/README.md`):
>
> ```
> /home/ende/Descargas/programaciones/recursos/assets/3cucharadas/avaluo-vulnerabilidad-unidad-vecinal/
> ```
>
> Este documento se queda en el repo porque describe qué es cada imagen, dónde va
> y qué advertencias tiene — eso sí vale versionarlo.

---

Se generaron siete imágenes únicas. La ubicación propuesta sigue la estructura real del post: presentación de la pregunta, construcción del universo espacial y cruce entre avalúo y vulnerabilidad.

Las rutas sandbox: sirven para descargarlas desde esta conversación. Codex o Claude Code no las verán automáticamente en tu equipo: deben copiarse al repositorio y renombrarse.

1. Hero editorial principal

Archivo actual:

infografía_de_avalúo_y_vulnerabilidad_territorial.png

Medidas: 1672 × 941 px
Relación: aproximadamente 16:9
Nombre recomendado:

hero-avaluo-vulnerabilidad-1672x941.png

Uso:

Imagen principal al comienzo del artículo.
Puede implementarse como header.image, overlay_image o figura inmediatamente debajo del encabezado, según el contrato real del tema Jekyll.
Resume el argumento completo: mismo numerador, tres denominadores y tres mapas.
Contiene las cifras 9,4 M, 19,9% y 45,8%.

Derivados recomendados:

hero-avaluo-vulnerabilidad-1600x900.webp
og-avaluo-vulnerabilidad-1200x630.webp

El og_image debe obtenerse mediante reencuadre manual, no con un recorte ciego, para no cortar el titular ni la figura de la derecha.

No usar como teaser pequeño de la portada: al reducirse a una tarjeta, sus textos se vuelven demasiado pequeños.

2. Teaser limpio, sin texto

Archivo actual:

cargando_energía_en_mosaicos_start_of_caption.png

Medidas: 1672 × 941 px
Relación: aproximadamente 16:9
Nombre recomendado:

teaser-avaluo-vulnerabilidad-sin-texto-1672x941.png

Uso principal:

Imagen de la tarjeta del post en la portada.
header.teaser.
Miniatura en listados por categoría o etiqueta.
Fondo visual para una llamada a explorar el visor.
Alternativa para contextos donde el título ya aparece como HTML.

Derivados recomendados:

teaser-avaluo-vulnerabilidad-640x360.webp
teaser-avaluo-vulnerabilidad-1280x720.webp

Esta es probablemente la imagen más adecuada para reemplazar la captura actual de la portada. Al no llevar texto incrustado, el título del post seguirá siendo legible y no habrá duplicación visual.

3. Imagen social con titular y estadísticas

Archivo actual:

mapa_neón_de_avalúos_y_vulnerabilidad.png

Medidas: 1122 × 1402 px
Relación: aproximadamente 4:5
Nombre recomendado:

social-avaluo-vulnerabilidad-estadisticas-1122x1402.png

Uso:

Publicación de imagen única en LinkedIn.
Mastodon y Bluesky.
Teaser vertical para difusión del artículo.
Eventualmente segunda lámina de un carrusel.

Incluye:

«Cambie el denominador, cambie el mapa».
El numerador fijo.
Los tres denominadores.
9,4 M predios únicos.
19,9% permanece en el mismo cuartil.
45,8% cambia dos o más cuartiles.

Derivado estándar recomendado:

social-avaluo-vulnerabilidad-1080x1350.png

Conviene conservarla en PNG para subirla directamente a las plataformas, sin convertirla a WebP.

4. Portada del carrusel

Archivo actual:

mapa_de_datos_en_flujo_neón.png

Medidas: 1122 × 1402 px
Relación: aproximadamente 4:5
Nombre recomendado:

carousel-cover-avaluo-vulnerabilidad-1122x1402.png

Uso:

Primera página de un carrusel PDF de LinkedIn.
Portada vertical para una secuencia explicativa.
Miniatura de un video vertical o demostración del visor.

Es más limpia que la imagen social anterior: presenta el título, la idea del numerador fijo y los tres denominadores, pero no incluye la fila de estadísticas.

Derivado recomendado:

carousel-01-portada-avaluo-vulnerabilidad-1080x1350.png

No es necesario insertarla dentro del artículo. Su función es principalmente de distribución.

5. Figura conceptual: un numerador, tres historias

Archivo actual:

infografía_neón_un_numerador_tres_historias.png

Medidas: 1448 × 1086 px
Relación: 4:3
Nombre recomendado:

figura-numerador-tres-denominadores-1448x1086.png

Ubicación recomendada en el post:

Inmediatamente después de la tabla de la sección «Pregunta», donde se explican:

avalúo por hogar;
avalúo por persona;
avalúo por metro cuadrado.

Puede ir antes del párrafo que comienza con:

«La respuesta corta: por hogar y por persona casi no hay relación…»

Función editorial:

Mostrar de manera directa que el avalúo fiscal total permanece fijo, mientras la pregunta y el patrón territorial cambian.

Derivado web recomendado:

figura-numerador-tres-denominadores-1200x900.webp

Alt sugerido:

Un mismo avalúo fiscal total se divide por hogares, personas y metros cuadrados, produciendo tres patrones territoriales distintos.
6. Figura del pipeline espacial

Archivo actual:

infografía_neón_del_universo_espacial.png

Medidas: 1448 × 1086 px
Relación: 4:3
Nombre recomendado:

figura-pipeline-universo-espacial-1448x1086.png

Ubicación recomendada:

En «Cucharada 1: construir el numerador sin cerrar la fuga», cerca de la actual Figura 1.

Representa:

10.343.893 registros originales.
942.616 duplicados.
9.401.277 predios únicos.
9.130.127 que tocan al menos una UV.
271.150 que no tocan ninguna UV.
Fuga de 2,884%.

Decisión de implementación:

No conviene mostrar simultáneamente esta imagen y el Sankey actual si ambos cuentan exactamente el mismo proceso. El agente debe escoger una de estas alternativas:

Mantener el SVG actual como figura analítica canónica y usar esta nueva imagen como lámina del carrusel.
Sustituir la figura actual por esta infografía, después de verificar manualmente todos los números y textos.
Usarla como apertura visual de la Cucharada 1 y conservar el SVG sólo como detalle técnico desplegable.

Para credibilidad metodológica, el SVG original tiene ventaja por ser vectorial y probablemente generado directamente desde los datos.

Alt sugerido:

Flujo desde 10.343.893 registros originales hasta 9.401.277 predios únicos, de los cuales 9.130.127 intersectan alguna unidad vecinal y 271.150 quedan fuera.

Pie obligatorio:

Debe conservar la advertencia del post: tocar al menos una UV no significa que el predio haya sido asignado completamente.

7. Figura bivariada: avalúo y vulnerabilidad

Archivo actual:

cruce_de_avalúo_y_vulnerabilidad_territoriales.png

Medidas: 1448 × 1086 px
Relación: 4:3
Nombre recomendado:

figura-bivariado-avaluo-vulnerabilidad-1448x1086.png

Ubicación prevista:

Al comienzo de «Cucharada 2: cuartiles, bivariado y denominadores», después de explicar el contrato de clasificación 4×2.

Estado: no debe publicarse sin correcciones.

Problemas detectados:

Dice «CATÁSTRO»; debe decir «CATASTRO».
Expande IGVUST como «Índice Geográfico de Vulnerabilidad Urbana y Social Territorial». En el artículo se define como Índice Global de Vulnerabilidad Socioterritorial.
La matriz aparece visualmente como cuatro columnas de vulnerabilidad por dos filas de avalúo. El post describe cuatro filas IGVUST por dos columnas de avalúo. Es la misma combinación matemática, pero el agente debe alinear la orientación con la leyenda efectiva del visor.
Los pequeños mapas son ilustrativos, no geometrías ni resultados reales. El pie debe llamarla esquema conceptual, no mapa de resultados.
Debe verificarse la dirección de los cuartiles y de la escala IGVUST contra el procesamiento real antes de conservar las etiquetas «baja» y «alta».

Alt sugerido después de corregirla:

Esquema conceptual de una clasificación bivariada que cruza niveles de vulnerabilidad territorial con avalúo fiscal por metro cuadrado.
Estructura recomendada dentro del repositorio
assets/
└── images/
    └── avaluo-vulnerabilidad-unidad-vecinal/
        ├── hero-avaluo-vulnerabilidad-1600x900.webp
        ├── teaser-avaluo-vulnerabilidad-640x360.webp
        ├── teaser-avaluo-vulnerabilidad-1280x720.webp
        ├── og-avaluo-vulnerabilidad-1200x630.webp
        ├── figures/
        │   ├── numerador-tres-denominadores-1200x900.webp
        │   ├── pipeline-universo-espacial-1200x900.webp
        │   └── bivariado-avaluo-vulnerabilidad-1200x900.webp
        ├── social/
        │   ├── teaser-estadisticas-1080x1350.png
        │   └── carousel-01-portada-1080x1350.png
        └── source/
            ├── hero-avaluo-vulnerabilidad-1672x941.png
            ├── teaser-sin-texto-1672x941.png
            ├── numerador-tres-denominadores-1448x1086.png
            ├── pipeline-universo-espacial-1448x1086.png
            ├── bivariado-avaluo-vulnerabilidad-1448x1086.png
            ├── social-estadisticas-1122x1402.png
            └── carousel-portada-1122x1402.png
Orden de implementación de mayor utilidad
Usar la imagen sin texto como nuevo teaser de la portada.
Incorporar el hero principal al inicio del artículo.
Generar el og_image de 1200 × 630 desde el hero.
Insertar «Un mismo numerador, tres historias» después de la tabla de denominadores.
Resolver si la imagen del pipeline sustituye o complementa el Sankey actual.
Corregir y recién entonces incorporar la figura bivariada.
Mantener las dos imágenes 4:5 exclusivamente como activos de distribución.
Archivos que el agente debe ignorar
/mnt/data/imagegen.png: es una copia byte a byte del hero principal.
/mnt/data/image(2).png: es la captura de la portada que adjuntaste, no una imagen generada para el post.