/* Search behavior shared by the two language-specific Jekyll stores. */
var idx = lunr(function () {
  this.field("title");
  this.field("excerpt");
  this.field("categories");
  this.field("tags");
  this.ref("id");
  this.pipeline.remove(lunr.trimmer);

  for (var item in store) {
    this.add({
      title: store[item].title,
      excerpt: store[item].excerpt,
      categories: store[item].categories,
      tags: store[item].tags,
      id: item
    });
  }
});

// Sin jQuery (capa 2, fase A): el script corre al final del <body>, con el DOM listo.
(function () {
  var searchMain = document.getElementById("search-main");
  var toggle = document.querySelector(".search__toggle");
  var skipContent = document.getElementById("skip-content-link");
  var results = document.getElementById("results");
  var input = document.getElementById("search");

  function syncSearchState() {
    var open = searchMain.classList.contains("is--visible");
    toggle.setAttribute("aria-expanded", String(open));
    skipContent.setAttribute("href", open ? "#search-main" : "#main");
    if (!open && searchMain.contains(document.activeElement)) toggle.focus();
  }

  if (searchMain && toggle && skipContent) {
    new MutationObserver(syncSearchState).observe(searchMain, {
      attributes: true,
      attributeFilter: ["class"]
    });
    syncSearchState();
  }

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) { node.setAttribute(key, attrs[key]); });
    if (text !== undefined) node.textContent = text;
    return node;
  }

  if (!input || !results) return;
  input.addEventListener("input", function () {
    var query = input.value.toLowerCase().trim();
    results.textContent = "";
    if (!query) return;

    var matches = idx.query(function (search) {
      query.split(lunr.tokenizer.separator).forEach(function (term) {
        if (!term) return;
        search.term(term, { boost: 100 });
        if (query.lastIndexOf(" ") !== query.length - 1) {
          search.term(term, { usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING, boost: 10 });
        }
        search.term(term, { usePipeline: false, editDistance: 1, boost: 1 });
      });
    });

    // «1 resultado encontrado» / «5 resultados encontrados»: antes «resultado(s)».
    var label = matches.length === 1
      ? (results.dataset.resultsFoundOne || results.dataset.resultsFound)
      : results.dataset.resultsFound;
    results.appendChild(el("p", { "class": "results__found" }, matches.length + " " + label));

    matches.forEach(function (match) {
      var entry = store[match.ref];
      var article = el("article", { "class": "archive__item", itemscope: "", itemtype: "https://schema.org/CreativeWork" });
      var heading = el("h2", { "class": "archive__item-title", itemprop: "headline" });
      heading.appendChild(el("a", { href: entry.url, rel: "permalink" }, entry.title));
      article.appendChild(heading);
      if (entry.teaser) {
        var teaser = el("div", { "class": "archive__item-teaser" });
        teaser.appendChild(el("img", { src: entry.teaser, alt: "" }));
        article.appendChild(teaser);
      }
      article.appendChild(el("p", { "class": "archive__item-excerpt", itemprop: "description" },
        entry.excerpt.split(" ").slice(0, 20).join(" ") + "…"));
      var item = el("div", { "class": "list__item" });
      item.appendChild(article);
      results.appendChild(item);
    });
  });
})();
