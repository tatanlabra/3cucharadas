{% assign indexed_posts = site.posts | where: "lang", include.lang | where_exp: "post", "post.search != false" | where_exp: "post", "post.hidden != true" %}
var store = [
{% for post in indexed_posts %}
  {% assign teaser = post.header.teaser | default: site.teaser %}
  {% assign localized_url = post.url %}
  {% if include.lang != site.default_lang %}
    {% assign localized_url = '/' | append: include.lang | append: post.url %}
  {% endif %}
  {
    "title": {{ post.title | jsonify }},
    "excerpt": {{ post.content | newline_to_br | replace: "<br />", " " | replace: "</p>", " " | replace: "</h1>", " " | replace: "</h2>", " " | replace: "</h3>", " " | replace: "</h4>", " " | replace: "</h5>", " " | replace: "</h6>", " " | strip_html | strip_newlines | jsonify }},
    "categories": {{ post.categories | jsonify }},
    "tags": {{ post.tags | jsonify }},
    "url": {{ localized_url | relative_url | jsonify }},
    "teaser": {{ teaser | relative_url | jsonify }},
    "lang": {{ include.lang | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{% endfor %}
];
