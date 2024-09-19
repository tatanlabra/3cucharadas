source "https://rubygems.org"

# Gestión de versiones para Jekyll
gem 'jekyll', '~> 4.3'

# Tema
gem 'jekyll-theme-chirpy', '~> 7.0', '>= 7.0.1'
#gem 'minimal-mistakes-jekyll', '~> 4.26', '>= 4.26.2'

# Plugins esenciales para funcionalidad extendida y SEO
group :jekyll_plugins do
  gem 'jekyll-feed', '~> 0.17.0'
  gem "jekyll-seo-tag", "~> 2.8"
  gem 'jekyll-scholar', '~> 7.1', '>= 7.1.3'
  gem "jekyll-polyglot", "~> 1.8"
  gem "jekyll-toc", "~> 0.19"
  gem "jekyll-asciidoc", "~> 3.0"
  gem 'jekyll-responsive-image', '~> 1.6'
  gem "jekyll-sitemap"
  end

# Dependencias específicas de la plataforma para usuarios de Windows y JRuby
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo-data" # Proporciona datos de zonas horarias
  gem "wdm", "~> 0.1.1" # Watchdog para mejorar el rendimiento de Jekyll en Windows
end

# Permitir que Bundler maneje automáticamente todas las actualizaciones de gemas
gem "bundler", "~> 2.2"
gem "json"
gem "faraday-retry"