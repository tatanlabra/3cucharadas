---
permalink: /terms/
title: "Términos y política de privacidad"
# Fuente en español. La inglesa es _pages/terms-en.md, con el MISMO permalink:
# es el patrón que ya usan about.md/about-en.md y year-archive.md/-en.md, y `lang`
# es lo único que impide que las dos fuentes colisionen en el mismo pase de
# Polyglot. Antes había un solo archivo en inglés que Polyglot publicaba en
# /terms/ y /en/terms/, así que la URL española servía texto inglés.
last_modified_at: 2026-08-08T00:00:00-04:00
lang: es
ref: terms
# Ya no lleva `noindex_langs: [en]`. Esa marca existía porque /en/terms/ era una
# copia byte a byte del original, no una traducción, y no debía competir por la
# indexación. Ahora hay dos textos reales, así que ambas variantes se indexan y
# `_pages/sitemap.xml` vuelve a declarar el par con su hreflang.
#
# El cuerpo venía de la plantilla de Minimal Mistakes y describía un sitio con
# Google AdSense y afiliados de Amazon. Nada de eso existe aquí —el gate de
# scripts/verify_site_artifact.rb aborta el build si aparece `adsbygoogle` o
# `pagead2.googlesyndication.com` en el artefacto—, así que esas secciones se
# retiran en lugar de traducirse: traducir una afirmación falsa la deja igual de
# falsa. Lo que sí ocurre en el sitio (GA4 con anonimización de IP y GoatCounter)
# se declara, porque una política que omite la analítica que sí corre es peor que
# la plantilla. No se agregan compromisos que el original no tenía.
toc: true
---

## Política de privacidad

La privacidad de quienes visitan este sitio es muy importante. Esta política describe qué información personal se recibe y se recolecta, y cómo se usa.

Ante todo: nunca compartiré tu dirección de correo ni ningún otro dato personal con nadie sin tu consentimiento directo.

### Archivos de registro

Como muchos otros sitios, este usa archivos de registro (*log files*) para conocer cuándo, desde dónde y con qué frecuencia llega el tráfico. La información de esos registros incluye:

* Direcciones IP
* Tipo de navegador
* Proveedor de acceso a internet (ISP)
* Fecha y hora
* Páginas de entrada y de salida
* Número de clics

Nada de esa información se vincula con datos que permitan identificarte.

### Cookies y balizas web

Al enviar un comentario se guardan en tu equipo cookies "de conveniencia" que sirven para que la próxima vez entres más rápido a [Disqus](https://disqus.com).

Los comentarios son de carga manual: Disqus no se contacta ni instala nada mientras no pulses el botón para cargarlos.

Si quieres desactivar las cookies, puedes hacerlo desde las opciones de tu navegador. Las instrucciones están en el sitio de cada navegador.

#### Google Analytics

Google Analytics es una herramienta de analítica web que uso para entender cómo se usa este sitio. Informa tendencias mediante cookies y balizas web, sin identificar visitantes individuales, y aquí está configurada para anonimizar la dirección IP. Puedes leer la [política de privacidad de Google Analytics](https://policies.google.com/technologies/partner-sites).

#### GoatCounter

En paralelo uso [GoatCounter](https://www.goatcounter.com), un contador de visitas que no usa cookies ni huella digital del navegador (*fingerprinting*).

## Publicidad y afiliados

Este sitio no tiene publicidad, ni programas de afiliados, ni ningún otro mecanismo por el que yo gane dinero con lo que publico aquí. Tampoco recibo compensación por recomendar herramientas o productos: lo que aparece en los artículos es lo que uso.

Igual que el resto del sitio, esta página está en construcción permanente. Si algo cambia, cambia también aquí.
