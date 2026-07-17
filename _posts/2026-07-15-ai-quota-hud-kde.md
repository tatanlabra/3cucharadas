---
layout: single
classes: [ai-quota-hud-post]
title: "Cuotas de IA en 3 cucharadas: un HUD para el panel de KDE"
subtitle: "Claude, Codex, Gemini y DeepSeek, antes de que alguno se declare fuera de servicio"
date: 2026-07-15 00:00:00 +0000
categories: [ia, productividad, desarrollo, kde]
tags: [kde, plasma, plasmoid, qml, python, systemd, mcp, claude-code, codex, gemini, deepseek, arch-linux, cuota, rate-limit, local-first]
description: "Un plasmoide local para KDE Plasma 6 que muestra la cuota disponible de Claude, Codex, Gemini y DeepSeek. Cómo funciona y qué ocurrió cuando Codex cambió sus ventanas de uso."
excerpt: "Cuatro agentes, cuatro formas de medir la cuota y un plasmoide para saber cuál todavía puede terminar el trabajo."
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
  og_image: /assets/images/ai-quota-hud/popup-hidpi.png
  og_image_alt: "Popup del plasmoide AI Quota HUD con cuatro indicadores circulares de cuota"
---

Actualmente ocupo Claude Code, Codex, Gemini (vía agy en CLI) y DeepSeek desde Arch Linux con KDE Plasma 6. Y como a muchos el problema está siendo saber cuál tiene cuota disponible, sobre todo en una tarea que ya tiene harto contexto, archivos revisados y hora de iteración.
{: .text-justify}

Así terminé armando un visor o HUD en el panel/barra de KDE: cuatro indicadores que muestran cuánto margen le queda a cada agente y cuándo debería reiniciarse. Sin otra pestaña, sin otro tablero y, sobre todo, sin sorprenderme que se acabó en medio del remate de una tarea o un `git rebase` 😱.
{: .text-justify}

## Primera cucharada: la semana-token

Cada proveedor inventó su propia forma de medir cuánto podemos usarlo.
{: .text-justify}

Claude habla en ventanas de horas y días. Codex presenta las ventanas disponibles para el plan. Gemini requiere una estimación local de solicitudes. DeepSeek, en cambio, habla en saldo monetario.
{: .text-justify}

Cuatro agentes, cuatro relojes y ninguna unidad común.
{: .text-justify}

La industria consiguió así algo bastante particular: convertir las **horas-token** y las **semanas-token** en unidades reales de planificación. Ya no basta con preguntarse cuánto demora una tarea. También hay que calcular si el agente alcanza a terminarla antes de quedar a la antigua :).
{: .text-justify}

En el panel lo reduje a cuatro anillos o donas. Uno casi lleno significa que el agente todavía tiene margen. Uno casi vacío significa que conviene agradecerle los servicios prestados y probar con el siguiente.
{: .text-justify}

{% include figure class="ai-quota-hud__donuts" popup=true image_path="/assets/images/ai-quota-hud/bar.png" alt="Barra compacta de AI Quota HUD en el panel de KDE Plasma, con cuatro indicadores circulares." caption="**Figura 1** — Vista compacta de AI Quota HUD en el panel de KDE Plasma. Los cuatro anillos resumen el margen disponible por agente. Fuente: captura propia con datos demostrativos." %}

Al pasar el cursor aparece el detalle de las ventanas y sus horas de reinicio:
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/tooltip.png" alt="Tooltip de AI Quota HUD con el resumen de cuota y reinicio por agente." caption="**Figura 2** — El tooltip despliega las ventanas y horas de reinicio sin abandonar la tarea activa. Fuente: captura propia con datos demostrativos." %}

Al abrir el plasmoide aparece el detalle completo de los cuatro agentes:
{: .text-justify}

<figure class="ai-quota-hud__video">
  <video autoplay loop muted playsinline controls preload="metadata" poster="/assets/images/ai-quota-hud/popup-hidpi.png" aria-label="Demostración de AI Quota HUD: barra de KDE, tooltip y popup con cuatro indicadores de cuota.">
    <source src="/assets/videos/ai-quota-hud-kde.webm" type="video/webm">
    Tu navegador no admite video WebM. Puedes <a href="/assets/videos/ai-quota-hud-kde.webm">abrir la demostración directamente</a>.
  </video>
  <figcaption><strong>Figura 3</strong> — Demostración de AI Quota HUD desde la barra de KDE hasta la vista detallada. Panel, tooltip y popup leen una única fuente local; los valores mostrados son demostrativos y no representan cuotas personales. Fuente: captura propia.</figcaption>
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

{% include figure popup=true image_path="/assets/images/ai-quota-hud/xkcd-303-compiling.png" alt="xkcd 303, Compiling: dos programadores juegan mientras esperan que termine la compilación." caption="**Figura 4** — *Compiling*, [xkcd n.º 303](https://xkcd.com/303/), de Randall Munroe. Antes la coartada era que el código estaba compilando; ahora puedo alegar que la cuota reinicia la próxima semana. Licencia [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)." %}
