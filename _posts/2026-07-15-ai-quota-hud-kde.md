---
layout: single
classes: [ai-quota-hud-post]
title: "Cuotas de IA en 3 cucharadas: un HUD para el panel de KDE"
subtitle: "Claude, Codex, Gemini y DeepSeek, antes de que alguno se declare fuera de servicio"
date: 2026-07-15 00:00:00 +0000
categories: [ia, productividad, desarrollo, kde]
tags: [kde, plasma, plasmoid, qml, python, systemd, mcp, claude-code, codex, gemini, deepseek, arch-linux, cuota, rate-limit, local-first]
description: "Un plasmoide local para KDE Plasma 6 que muestra la cuota disponible de Claude, Codex, Gemini y DeepSeek. Cómo funciona y qué ocurrió cuando Codex cambió sus ventanas de uso."
excerpt: "Cinco agentes, cinco formas de medir la cuota y un plasmoide para saber cuál todavía puede terminar el trabajo."
author: clabra
lang: es
ref: ai-quota-hud-kde
permalink: /ia/productividad/ai-quota-hud-kde/
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-ai-quota-hud.webp
  og_image: /assets/images/ai-quota-hud/popup-og-1200.webp
  og_image_alt: "Vista detallada del plasmoide AI Quota HUD con cinco indicadores circulares de cuota"
---

Actualmente ocupo Claude Code, Codex, Gemini (vía agy en CLI) y DeepSeek desde Arch Linux con KDE Plasma 6. Y como a muchos el problema está siendo saber cuál tiene cuota disponible, sobre todo en una tarea que ya tiene harto contexto, archivos revisados y hora de iteración.
{: .text-justify}

Así terminé armando un visor o HUD en el panel/barra de KDE: cinco indicadores que muestran cuánto margen le queda a cada agente y cuándo debería reiniciarse. Sin otra pestaña, sin otro tablero y, sobre todo, sin sorprenderme que se acabó en medio del remate de una tarea o un `git rebase` 😱.
{: .text-justify}

## Primera cucharada: la semana-token

Cada proveedor inventó su propia forma de medir cuánto podemos usarlo.
{: .text-justify}

Claude habla en ventanas de horas y días. Codex presenta las ventanas disponibles para el plan. Gemini requiere una estimación local de solicitudes. Copilot cuenta solicitudes premium con corte de calendario. DeepSeek, en cambio, habla en saldo monetario.
{: .text-justify}

Cinco agentes, cinco relojes y ninguna unidad común.
{: .text-justify}

La industria consiguió así algo bastante particular: convertir las **horas-token** y las **semanas-token** en unidades reales de planificación. Ya no basta con preguntarse cuánto demora una tarea. También hay que calcular si el agente alcanza a terminarla antes de quedar a la antigua :).
{: .text-justify}

En el panel lo reduje a cinco anillos o donas. Uno casi lleno significa que el agente todavía tiene margen. Uno casi vacío significa que conviene agradecerle los servicios prestados y probar con el siguiente.
{: .text-justify}

{% include figure class="ai-quota-hud__donuts" popup=true image_path="/assets/images/ai-quota-hud/bar.png" alt="Barra compacta de AI Quota HUD en el panel de KDE Plasma, con cinco indicadores circulares." caption="**Figura 1** — Vista compacta de AI Quota HUD en el panel de KDE Plasma. Los cinco anillos resumen el margen disponible por agente. El arco de color es lo que queda libre y las marcas blancas exteriores cuentan los días hasta el reinicio. Fuente: captura propia con datos ficticios." %}

Al pasar el cursor sobre una dona aparece el detalle de ese agente: sus ventanas y sus horas de reinicio.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/tooltip.png" alt="Visor emergente de AI Quota HUD mostrando las cuatro ventanas de cuota de Antigravity y Gemini, cada una con su porcentaje libre y su hora de reinicio." caption="**Figura 2** — El visor emergente despliega las ventanas del agente señalado sin abandonar la tarea activa. Antigravity lleva dos cuotas semanales independientes, con relojes distintos: una para los modelos de Google y otra para los de terceros. La insignia dice de dónde viene cada cifra: OFICIAL si la reporta el proveedor, LOCAL si es un conteo propio. Fuente: captura propia con datos ficticios." %}

Al hacer clic se abre la vista detallada, con los cinco agentes arriba y las ventanas del que se elija debajo.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/popup-hidpi.png" alt="Vista detallada de AI Quota HUD: fila de cinco selectores con el porcentaje libre de cada agente y, debajo, las cuatro ventanas de Claude con su porcentaje, procedencia y hora de reinicio." caption="**Figura 3** — Vista detallada. Arriba, los cinco agentes con su margen más ajustado; abajo, las ventanas del que se elija. Cada línea dice cuánto queda, cuándo renueva y de dónde sale la cifra. Fuente: captura propia con datos ficticios." %}

<figure class="ai-quota-hud__video">
  <video width="1472" height="1152" autoplay loop muted playsinline controls preload="metadata" poster="/assets/images/ai-quota-hud/demo-poster-1472x1152.webp" aria-label="Demostración de AI Quota HUD: la barra en el panel de KDE, el visor emergente al señalar un agente, y la vista detallada con la fila de selectores cambiando de agente.">
    <source src="/assets/videos/ai-quota-hud-demo-1472x1152.webm" type="video/webm">
    Tu navegador no admite video WebM. Puedes <a href="/assets/videos/ai-quota-hud-demo-1472x1152.webm">abrir la demostración directamente</a>.
  </video>
  <figcaption><strong>Figura 4</strong> — Recorrido desde la barra del panel hasta la vista detallada, con la fila de selectores pasando por Codex, Antigravity y DeepSeek. Los valores son ficticios y no representan cuotas personales. Fuente: secuencia renderizada con la misma sonda que verifica las pruebas, fotograma a fotograma y con el reloj fijo, así que se puede volver a generar idéntica.</figcaption>
</figure>

## Segunda cucharada: el dato manda, no el orden

La primera versión funcionó bien durante semanas. Codex entregaba dos ventanas: una corta, de cinco horas, y otra semanal.
{: .text-justify}

Mi código las interpretaba por posición:
{: .text-justify}

1. La primera ventana o anillo exterior era la de cinco horas.
2. La segunda era la semanal.

Era sencillo, hasta que Codex cambió el esquema.
{: .text-justify}

Un día el widget mostró un 5 % disponible en la supuesta ventana de «5 h», pero con un reinicio programado para seis días después. Incluso para una empresa tecnológica, cinco horas que duran casi una semana parecían demasiada innovación.
{: .text-justify}

La respuesta cruda contenía una sola ventana:
{: .text-justify}

```text
604800 segundos
```

Eso equivale a siete días.
{: .text-justify}

Codex había dejado de informar la ventana corta, pero mi código seguía llamando «5 h» a cualquier cosa que apareciera primero. Al mismo tiempo, la antigua ventana semanal permanecía congelada en la caché, porque la lógica de «conservar el último valor bueno» no sabía distinguir entre una consulta fallida y una ventana que había dejado de existir. 👻
{: .text-justify}

La corrección tuvo dos partes.
{: .text-justify}

Primero, cada ventana dejó de identificarse por su posición y pasó a identificarse por su duración real. Una duración breve corresponde a una sesión; una duración extendida, a una ventana semanal o equivalente.
{: .text-justify}

Segundo, el monitor ahora distingue entre:
{: .text-justify}

- **una consulta que falló**, caso en que conserva temporalmente el dato anterior y lo marca como caché;
- **una consulta válida que ya no contiene una ventana**, caso en que elimina esa ventana del estado vigente.

La interfaz también dejó de suponer que todos los agentes tienen la misma estructura. Si llegan dos ventanas, dibuja una dona doble. Si llega una, dibuja un solo anillo. El dato define la interfaz, no al revés.
{: .text-justify}

La moraleja es pequeña, pero bastante general: **si el proveedor entrega la duración, esa es la identidad del dato; la posición en un arreglo es apenas una coincidencia temporal.**
{: .text-justify}

## Tercera cucharada: local, útil y poco universal

Este proyecto no pretende ser una aplicación multiplataforma.
{: .text-justify}

Lo construí para un entorno muy parecido al mío:
{: .text-justify}

- Arch Linux;
- KDE Plasma 6;
- `systemd --user`;
- Python;
- Bash;
- QML;
- las sesiones y credenciales locales de las herramientas que ya utilizo.

Probablemente pueda adaptarse a otras distribuciones con Plasma 6. No prometo que funcione sin cambios en GNOME, Plasma 5, Windows o macOS. Tampoco abstraje cada posible método de autenticación. Es una herramienta para mi escritorio que decidí ordenar y publicar, no un intento de resolver todas las combinaciones posibles de sistemas operativos, proveedores y planes.
{: .text-justify}

Por dentro, el recorrido es corto:
{: .text-justify}

```text
                 systemd --user timer
                          │
                    cada cinco minutos
                          ▼
 helpers/*.sh ──► monitor en Python ──► status.json
                                                │
                                 ┌──────────────┴──────────────┐
                                 ▼                             ▼
                         plasmoide QML                    servidor MCP
                   panel · tooltip · popup          consulta antes de delegar
```

Los *helpers* son el único componente que toca credenciales. Entregan JSON saneado, sin tokens de autenticación ni contenido de conversaciones.
{: .text-justify}

El monitor en Python consulta, valida y fusiona la información. Si aparece un `timeout`, una credencial expirada o un error `429`, conserva el último valor conocido y lo marca como caché.
{: .text-justify}

El temporizador de `systemd` ejecuta la actualización cada cinco minutos. El plasmoide no consulta directamente a los proveedores; solo lee un archivo local con permisos `0600`. Así evito provocar un *rate limit* por consultar demasiado el *rate limit*, que sería una forma especialmente elegante de cerrar el círculo. 🫠
{: .text-justify}

El mismo `status.json` puede ser leído por un servidor MCP. De este modo, un agente puede preguntar qué proveedor tiene cuota antes de delegar una tarea. La barra del escritorio y el orquestador reciben exactamente el mismo estado.
{: .text-justify}

## Cierre

El repositorio está publicado con licencia MIT. Está pensado para KDE Plasma 6, no requiere `sudo` y se instala en las rutas locales del usuario:
{: .text-justify}

```bash
git clone https://github.com/tatanlabra/ai-quota-kde.git
cd ai-quota-kde
scripts/install-user.sh
ai-quota-monitor doctor
```

[Ver el repositorio en GitHub](https://github.com/tatanlabra/ai-quota-kde){: .btn .btn--primary}

No crea más cuota, no negocia mejores planes y no elimina la semana-token. Solo evita descubrir, a mitad de una tarea, que el agente elegido se fue a descansar sediento de cuota adicional 🤑.
{: .text-justify}

Es una cucharada pequeña de soberanía sobre mi propio flujo: saber cuánto queda, cuándo reinicia y a quién conviene pasarle el trabajo.
{: .text-justify}

## Actualización del 8 de septiembre de 2026

El HUD cambió lo suficiente como para que las capturas de julio ya no lo
representaran. Lo que se ve arriba en las figuras 1 a 3 es el estado de hoy; el
video de la figura 4 sigue siendo de julio y se conserva porque el recorrido
—panel, visor emergente, vista detallada— no ha cambiado, aunque el diseño sí.
{: .text-justify}

Qué es distinto:
{: .text-justify}

- **Cinco agentes en vez de cuatro.** Se sumó Copilot, que cuenta solicitudes premium con corte de calendario. El texto del post decía «cuatro» en siete lugares y quedó corregido.
- **Otro visor emergente.** Antes resumía los cinco agentes en una lista apretada. Ahora muestra el detalle del agente sobre el que está el cursor, con una insignia por línea que dice si la cifra la reporta el proveedor (`OFICIAL`) o es un conteo local (`LOCAL`).
- **Otra vista al hacer clic.** Los cinco agentes pasaron a una fila de selectores con su margen más ajustado, y debajo van las ventanas del que se elija. Antes eran cinco columnas simultáneas que no cabían.
- **Trazo y logotipos un punto más grandes.** El arco de cuota pasó de 0,055 a 0,060 del diámetro y los logotipos crecieron un 3 %, medido en ejecución. La apertura central se recuperó apretando la separación entre anillos, porque ensanchar el trazo la encogía.
- **La interfaz está traducida.** Las cadenas fuente pasaron a inglés y el español vive en un catálogo `gettext`, así que el widget habla el idioma del escritorio.

Y dos cosas que aparecieron justo al preparar estas capturas, que valen más que
las capturas mismas:
{: .text-justify}

- Las fechas salían en inglés en un escritorio en español. `Qt.formatDate` con un formato escrito a mano usa el locale C, no el del sistema: con todo lo demás ya traducido, seguía diciendo «Sat 12 Sep» donde correspondía «sáb 12 sept». Medido con `QLocale("es_CL")` sobre la misma fecha.
- Cuatro etiquetas las escribía el recolector en español y llegaban a pantalla sin pasar por el catálogo, así que en un escritorio en inglés se leían en español entre cadenas traducidas.

Las capturas se generan con un script del repositorio, no a mano, y de ahí
salen las tres figuras nuevas:
{: .text-justify}

```bash
scripts/capture_previews.sh build/previews es 3
```

Renderiza las tres vistas sin abrir ventana, con el mismo componente que
verifican las pruebas, y a la escala que se le pida —3× para estas—. Los datos
salen de `ai-quota-monitor sample`, que escribe un informe ficticio en un
directorio temporal: la caché real no se lee ni se toca, y cada línea del render
queda rotulada como dato ficticio. Por eso las cifras de las figuras no son mis
cuotas, y por eso se pueden volver a generar idénticas. Eso sí, necesita GPU, y
la actualización de más abajo cuenta por qué.
{: .text-justify}

## Actualización del 9 de septiembre de 2026

Las figuras 1 a 3 se volvieron a generar por una razón concreta: **los logotipos
salían en negro**. El widget en el panel siempre estuvo bien; lo que estaba mal era
el script de capturas.
{: .text-justify}

El componente de Kirigami que recolorea un SVG monocromo lo hace con un material de
GPU, y el renderizador por software no tiene equivalente para ese material: dibuja
la silueta y se salta el color. El script renderizaba por software, así que cuatro
de los cinco logotipos aparecían negros —el de Codex, blanco— y en el popup
quedaban casi invisibles, oscuro sobre oscuro. El quinto, Gemini, se veía bien
porque nunca se pretendió teñirlo: conserva el azul de su propio archivo.
{: .text-justify}

Lo que más me interesa de este fallo es por qué las 93 pruebas seguían verdes. Una
silueta negra tiene exactamente la misma anchura, la misma altura y la misma
apertura que una teñida, así que ningún invariante de geometría podía verlo: la
ausencia de una comprobación de color *era* la razón de que pasara inadvertido. Y
estaba anotado desde el 6 de septiembre en el propio repositorio —«el renderizado
por software no muestra fielmente los colores de máscara»—, dos días antes de que un
commit cambiara el flujo a offscreen y publicara el defecto.
{: .text-justify}

Medido: la barra tenía 1452 píxeles opacos exactamente negros y 299 exactamente
blancos; el popup, 2597 y 6. Ahora tiene cero de cada uno y los cuatro logotipos
enmascarados aparecen en su acento. Hay una prueba nueva que mira el color del píxel
dentro del disco central de cada dona y exige que el color dominante sea el acento de
ese proveedor, con Gemini como control negativo: si Gemini casara con los dos, la
medición estaría mirando el anillo y no el logotipo. Se salta explícitamente si la
máquina no tiene GPU, y nunca aprueba por no medir nada.
{: .text-justify}

Una vuelta de tuerca que no esperaba: de las tres formas de renderizar por GPU, las
dos obvias exigen mapear una ventana, y **una pantalla bloqueada deja de
presentarla**. Los mismos comandos que funcionaron por la tarde se colgaban una hora
después con la sesión bloqueada, esperando un fotograma que nadie iba a pintar. La
vía que sí sirve no abre ventana en absoluto. Y al cambiar de plataforma apareció otra
sorpresa: la nueva deducía el DPI del monitor real en vez de usar 96, y con eso el
tooltip crecía 24 píxeles sin que cambiara una línea de código. Ahora el DPI va fijo,
así que la geometría no depende del monitor de la máquina que capture.
{: .text-justify}

Y los logotipos crecieron un 5,3 %, que es todo el margen que queda: la esquina de su
recuadro toca ya la circunferencia del hueco central. La comprobación que garantizaba
esa contención estaba anulada por un techo silencioso que recortaba cualquier valor
mayor que 1 sin avisar —un valor de 1,10 salía verde—; quitarlo la devolvió al
servicio.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/xkcd-303-compiling.png" alt="xkcd 303, Compiling: dos programadores juegan mientras esperan que termine la compilación." caption="**Figura 5** — *Compiling*, [xkcd n.º 303](https://xkcd.com/303/), de Randall Munroe. Antes la coartada era que el código estaba compilando; ahora puedo alegar que la cuota reinicia la próxima semana. Licencia [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)." %}
