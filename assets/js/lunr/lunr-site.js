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

$(function () {
  var searchMain = document.getElementById("search-main");
  var toggle = document.querySelector(".search__toggle");
  var skipContent = document.getElementById("skip-content-link");
  var results = $("#results");

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

  $("input#search").on("input", function () {
    var query = $(this).val().toLowerCase().trim();
    results.empty();
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

    $("<p>", { "class": "results__found" })
      .text(matches.length + " " + results.data("results-found"))
      .appendTo(results);

    matches.forEach(function (match) {
      var entry = store[match.ref];
      var article = $("<article>", { "class": "archive__item", itemscope: "", itemtype: "https://schema.org/CreativeWork" });
      var heading = $("<h2>", { "class": "archive__item-title", itemprop: "headline" });
      $("<a>", { href: entry.url, rel: "permalink" }).text(entry.title).appendTo(heading);
      heading.appendTo(article);
      if (entry.teaser) {
        $("<div>", { "class": "archive__item-teaser" })
          .append($("<img>", { src: entry.teaser, alt: "" }))
          .appendTo(article);
      }
      $("<p>", { "class": "archive__item-excerpt", itemprop: "description" })
        .text(entry.excerpt.split(" ").slice(0, 20).join(" ") + "…")
        .appendTo(article);
      $("<div>", { "class": "list__item" }).append(article).appendTo(results);
    });
  });
});
