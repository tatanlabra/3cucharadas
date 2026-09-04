# Activos visuales — «Multiagentes en 3 cucharadas III: una memoria que deja huellas»

Documento editorial de las piezas del post. Mismo rol que
`assets/images/avaluo-vulnerabilidad-unidad-vecinal/source/readme.md`: aquí vive el
razonamiento y los prompts; lo verificable vive en `_data/visuales/<slug>.yml`, que es
contra lo que corre `scripts/verify_visual_assets.rb`.

## La regla que manda sobre todas

**Ninguna imagen de este post puede contener un cerebro, una silueta humana pensante,
una nube de neuronas ni nada que sugiera una mente.**

No es preferencia estética. El post se titula «un mapa que no se hace pasar por una
mente» y su argumento central es que lo que hay es un registro de trabajo con
procedencia, no cognición. El teaser del Post II —que este post reemplaza en la serie—
es literalmente un cerebro holográfico. Repetirlo contradiría el texto en la primera
impresión, que es donde más pesa.

Lo que sí debe verse: **cuatro fuentes separadas por una frontera**, con flechas que
salen solo donde el contrato lo permite. Memoria, no mente. Permisos, no inteligencia.

## Continuidad con la serie

Referencias: `assets/images/teasers/teaser-multiagentes-memoria.webp` y
`teaser-multiagentes-vscode.webp`.

- Render isométrico 3D, cámara alta, ~30–35° de inclinación.
- Fondo azul muy oscuro, casi negro, con retícula tenue apenas insinuada.
- Objetos sobre plataformas flotantes con borde luminoso.
- Emisión cian y violeta; naranja/ámbar solo como acento puntual.
- Superficies mate. Nada de plástico brillante ni cromo.
- Sin gente real, sin logos, sin texto decorativo inventado.

## Paleta exacta

Son los colores del propio visor del post (`assets/src/memoria_gobernada/styles.scss`).
Usarlos, no colores «parecidos».

| Uso | Hex |
|---|---|
| Fondo | `#07070c` |
| Superficie / plataformas | `#0f1620` |
| Líneas y bordes | `#294155` |
| Texto claro / puntos brillantes | `#eef8fc` |
| Acento principal (cian) | `#37e7ff` |
| Acento secundario (magenta) | `#ff4fd8` |
| Acento terciario (verde ácido) | `#b8ff3c` |

Color por fuente, igual que en el visor: memoria operativa **cian**, correo personal
**magenta**, índice de tesis **verde ácido**, proyección pública **cian intenso**.

## Qué genera quién

| Pieza | Quién | Tamaño máster |
|---|---|---|
| Hero | ChatGPT (prompt 1) | 1672×941, o 1792×1024 y se recorta |
| Teaser | ChatGPT (prompt 2) | 1672×941 |
| OG social | reencuadre manual del hero, **no** un render nuevo | → 1200×630 |
| Carrusel LinkedIn | **no ChatGPT**: HTML + `scripts/render-linkedin-carousel.sh` | 1080×1350 ×6 |

El carrusel sale de HTML porque lleva cifras exactas que están verificadas contra
artefactos y tiene que ser regenerable. Una imagen generada con cifras dentro no se
corrige sin volver a generarla.

---

## PROMPT 1 — Hero

> Ilustración isométrica 3D, cámara elevada a unos 32 grados, fondo azul casi negro
> (#07070c) con una retícula técnica muy tenue apenas perceptible.
>
> La escena muestra cuatro plataformas flotantes SEPARADAS, dispuestas en arco, cada
> una con un borde luminoso de su propio color y un objeto encima:
>
> 1. Plataforma con borde cian brillante (#37e7ff): una pila ordenada de tarjetas de
>    datos translúcidas, apiladas y alineadas, cada una con una pequeña marca de
>    verificación luminosa en la esquina.
> 2. Plataforma con borde magenta (#ff4fd8): un sobre cerrado, opaco y sellado, dentro
>    de una cúpula de cristal esmerilado que impide ver su interior. Del sobre sale un
>    único hilo de luz muy fino.
> 3. Plataforma con borde verde ácido (#b8ff3c): un archivador de fichas técnicas con
>    etiquetas y códigos, no libros ni documentos legibles.
> 4. Plataforma central, más grande y más elevada, con borde cian intenso: una esfera de
>    malla geométrica abierta, hecha de nodos y aristas finas, translúcida, que se ve
>    claramente HUECA.
>
> Entre las tres plataformas laterales y la central corren flechas de luz delgadas y
> direccionales, todas apuntando hacia la esfera central. La flecha que sale del sobre
> magenta es notoriamente más fina y más tenue que las otras dos.
>
> Cruzando toda la escena en diagonal, por delante de las plataformas laterales y por
> detrás de la central, hay un plano vertical translúcido de vidrio azulado con un patrón
> hexagonal sutil: una membrana, una frontera. Las flechas la atraviesan por aberturas
> circulares nítidas, tres y solo tres, cada una del color de su flecha. El resto de la
> membrana es continuo y cerrado.
>
> Estilo: superficies mate, emisión de luz suave, niebla volumétrica leve en el suelo,
> partículas luminosas muy dispersas al fondo. Alto detalle, acabado editorial limpio,
> como una infografía técnica de producto. Sin personas, sin robots, sin rostros.
>
> Incluye estas cuatro etiquetas en español, en tipografía sans-serif geométrica, tamaño
> pequeño pero legible, color #eef8fc, una bajo cada plataforma y en este orden:
> MEMORIA DE TRABAJO · CORREO PERSONAL · ÍNDICE DE TESIS · PROYECCIÓN PÚBLICA
> Respeta las tildes: ÍNDICE lleva tilde en la I, PROYECCIÓN en la O.
> Ningún otro texto: sin título, sin cifras, sin firma.
>
> PROHIBIDO: cerebros, siluetas de cabeza humana, redes neuronales con forma orgánica,
> corazones, ojos, iconos genéricos de inteligencia artificial, logos de marcas reales,
> texto en inglés inventado, código legible falso.

**Por qué así.** La escena *es* el argumento del post: cuatro fuentes que no se mezclan,
una frontera que solo deja pasar lo que el contrato permite, y una proyección pública
hueca a propósito porque es derivada, no la cosa misma. El sobre sellado bajo cristal es
el correo: existe en el sistema y no sale de él.

**Variante EN** (misma escena, etiquetas traducidas):
`OPERATIONAL MEMORY · PERSONAL MAIL · THESIS INDEX · PUBLIC PROJECTION`

**No usar como teaser:** a tamaño tarjeta las cuatro etiquetas quedan ilegibles y la
membrana se lee como un artefacto.

---

## PROMPT 2 — Teaser (sin texto)

> Ilustración isométrica 3D, cámara elevada, fondo azul casi negro (#07070c).
>
> Una esfera de malla geométrica abierta y translúcida, hecha de nodos luminosos y
> aristas muy finas, flotando sobre una plataforma circular oscura con borde de luz cian
> (#37e7ff). La esfera es claramente hueca: se ven sus aristas del lado opuesto a través
> de ella.
>
> Tres nodos concretos de la malla brillan más que el resto, cada uno de un color
> distinto: uno cian (#37e7ff), uno magenta (#ff4fd8) y uno verde ácido (#b8ff3c). De
> cada uno de esos tres nodos desciende un hilo de luz hasta la plataforma, donde deja
> una HUELLA circular que sigue brillando débilmente, como una marca que permanece
> después del paso. Las huellas son de tres tamaños distintos.
>
> Alrededor, partículas de luz muy dispersas sobre el fondo oscuro, como un campo de
> estrellas lejano y tenue. Niebla volumétrica suave en la base de la plataforma.
>
> Composición centrada, con aire generoso alrededor del objeto: la esfera no debe ocupar
> más de un 55% del ancho del encuadre, porque la imagen se recortará a varias
> proporciones distintas.
>
> Estilo: superficies mate, emisión de luz suave, acabado editorial limpio, alto detalle.
>
> SIN TEXTO DE NINGÚN TIPO. Sin personas, sin robots.
>
> PROHIBIDO: cerebros, cabezas humanas, redes neuronales orgánicas, texto, números,
> logos, iconos genéricos de IA.

**Por qué sin texto.** El teaser se muestra a 640×360 en la portada, con el título ya en
HTML al lado. Cualquier tipografía dentro queda por debajo del umbral de legibilidad y
duplica lo que ya dice el titular. Es la conclusión que dejó escrita el post de avalúo
tras probarlo.

**Por qué las huellas.** Son el título del post: *una memoria que deja huellas*. Y el
aire alrededor es requisito técnico, no estético: esta imagen se recorta a 16:9 para el
teaser, a 1.91:1 para el og y potencialmente a 4:5 para redes.

---

## Qué se hace al recibir los PNG

1. Máster a `recursos/assets/3cucharadas/multiagente-penta-agent-memoria-gobernada/`
   (fuera del repo del sitio: pesan y el sitio sirve solo `.webp`).
2. Derivar: `hero-…-1600x900.webp`, `teaser-….webp` (1280×720), `teaser-…-640.webp`,
   `og-…-1200x630.webp` reencuadrado a mano desde el hero.
3. Escribir `_data/visuales/multiagente-penta-agent-memoria-gobernada.yml`.
4. `ruby scripts/verify_visual_assets.rb`.

## Restricción dura del pipeline

`scripts/verify_visual_assets.rb:22` fija `MIN_OG_IMAGE_WIDTH = 1200`. Si el og sale con
menos de 1200 px de ancho, **el build del sitio aborta**. No es un aviso.

## Reencuadre del og

Del hero 16:9 al og 1.91:1 se recorta altura, no ancho, y **a mano**. Un recorte centrado
ciego se come las etiquetas laterales, que son lo único que explica la escena. El encuadre
correcto conserva la esfera central completa, la membrana con sus tres aberturas, y al
menos dos etiquetas legibles. Se puede sacrificar la plataforma del extremo; la membrana
no. Comprobar que se entiende a 300 px de ancho, que es la miniatura real en el feed de
LinkedIn en móvil.
