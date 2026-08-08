---
layout: archive
title: "Sitemap"
permalink: /sitemap/
author_profile: false
---

{% assign active_lang = site.active_lang | default: page.lang | default: site.default_lang | default: "es" %}
{% if active_lang == "en" %}All the posts and pages published on this site.{% else %}Todas las publicaciones y páginas de este sitio.{% endif %}

{% comment %}
El bucle iteraba `site.pages` sin filtro, así que esta página enlazaba a
`/404.html`, `/robots.txt`, `/sitemap.xml`, la hoja de estilos y los índices de
Lunr. Eso le daba a Googlebot una ruta de descubrimiento hacia la 404 —que
responde 200— y hacia recursos que no son páginas.

El filtro es de forma, no una lista negra: una página de contenido tiene título
y URL "bonita" terminada en barra. Los feeds, los assets y la 404 terminan en
extensión; las páginas del paginador de jekyll-paginate heredan el front matter
de index.html, que no declara `title`, así que también quedan fuera. Se respetan
además `sitemap: false` y `noindex`, para no enlazar lo que le pedimos a Google
que ignore.

También se quitó el enlace al sitemap XML: robots.txt ya se lo anuncia a los
rastreadores, y desde una página indexable sólo servía para empujarlos hacia un
recurso que no es contenido.
{% endcomment %}

<h2>{% if active_lang == "en" %}Pages{% else %}Páginas{% endif %}</h2>
{% for post in site.pages %}
  {% assign url_tail = post.url | slice: -1 %}
  {% assign lang_noindex = false %}
  {% if post.noindex_langs contains active_lang %}{% assign lang_noindex = true %}{% endif %}
  {% if post.title and url_tail == "/" and post.sitemap != false and post.noindex != true and lang_noindex == false %}
    {% include archive-single.html %}
  {% endif %}
{% endfor %}

<h2>{% if active_lang == "en" %}Posts{% else %}Publicaciones{% endif %}</h2>
{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}

{% capture written_label %}'None'{% endcapture %}

{% for collection in site.collections %}
{% unless collection.output == false or collection.label == "posts" %}
  {% capture label %}{{ collection.label }}{% endcapture %}
  {% if label != written_label %}
  <h2>{{ label }}</h2>
  {% capture written_label %}{{ label }}{% endcapture %}
  {% endif %}
{% endunless %}
{% for post in collection.docs %}
  {% unless collection.output == false or collection.label == "posts" %}
  {% include archive-single.html %}
  {% endunless %}
{% endfor %}
{% endfor %}
