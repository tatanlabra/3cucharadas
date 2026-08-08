# Gemfile — 3cucharadas (build local)
source "https://rubygems.org"

# Core
gem "jekyll", "~> 4.4"              # 4.4.1 a enero 2025
gem "webrick", "~> 1.9", group: :development  # necesario para `jekyll serve` en Ruby 3+

# Tema
gem "minimal-mistakes-jekyll", "~> 4.28"      # 4.28.0

# Plugins recomendados por el tema
group :jekyll_plugins do
  gem "jekyll-include-cache", "~> 0.2"        # requerido por Minimal Mistakes
  gem "jekyll-feed", "~> 0.17"
  # jekyll-sitemap RETIRADO. El sitio tiene su propio `_pages/sitemap.xml`, que es
  # multilingüe y emite `xhtml:link rel="alternate" hreflang`; el de la gema no
  # sabe de Polyglot. Estaba desactivado en la lista `plugins:` de `_config.yml`,
  # pero eso no bastaba: Jekyll carga el grupo `:jekyll_plugins` ENTERO, al margen
  # de esa lista. Sólo se mantenía callado porque `_pages/sitemap.xml` ya ocupaba
  # la ruta `/sitemap.xml`; en el pase EN, donde esa ruta queda libre, sí se
  # colaba y publicaba `/en/sitemap.xml` y un `/en/robots.txt` truncado.
  gem "jekyll-paginate", "~> 1.1"
  gem "kramdown-parser-gfm", "~> 1.1"
  gem "kramdown-math-katex", "~> 1.0"
  gem "jekyll-polyglot", "~> 1.9"             # multi-idioma ES/EN (build local + CI)
end
