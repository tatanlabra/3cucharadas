#!/usr/bin/env ruby
# frozen_string_literal: true

require "cgi"
require "find"
require "json"

site_dir = File.expand_path(ARGV.fetch(0, "public"))
# KaTeX CSS and its self-hosted WOFF2 font set are part of the public artifact.
max_bytes = Integer(ENV.fetch("SITE_ARTIFACT_MAX_BYTES", "22000000"))
draft_fixture_mode = ENV["VERIFY_MATH_DRAFTS"] == "1"

abort "Artifact directory does not exist: #{site_dir}" unless Dir.exist?(site_dir)

required_files = %w[
  assets/css/main.css
  assets/js/main.min.js
  assets/js/theme-toggle.js
  assets/js/lunr/lunr-en.js
  assets/js/lunr/lunr-store.js
  assets/js/lunr/lunr.min.js
  assets/vendor/katex/0.17.0/katex.css
  assets/images/clabra2026-320.webp
  assets/images/teasers/teaser-ai-quota-hud-640.webp
  assets/images/teasers/teaser-bayes-hiperparametros-640.webp
  assets/images/teasers/teaser-casen-2024-640.webp
  assets/images/teasers/teaser-multiagentes-vscode-640.webp
  assets/images/teasers/teaser-rss-soberania-digital-640.webp
].freeze

pruned_files = %w[
  assets/images/catppuccin_latte-skin-archive-large.png
  assets/images/catppuccin_mocha-skin-archive-large.png
  assets/images/favicons/favicon.svg
  assets/js/_main.js
  assets/js/lunr/lunr-gr.js
  assets/js/lunr/lunr.js
  assets/js/main.min.js.map
  assets/js/plugins/gumshoe.js
  assets/js/vendor/jquery/jquery-3.6.0.js
].freeze

required_files.each do |relative|
  abort "Required runtime asset is missing: #{relative}" unless File.file?(File.join(site_dir, relative))
end

microsite = "catastro_sii_brecha"
microsite_dir = File.join(site_dir, microsite)
if Dir.exist?(microsite_dir)
  %w[index.html metodologia.html style.css app.js assets/map-config.js assets/site-ui.js data/manifest.json data/comunas.json data/regiones.json data/quality.json data/metricas_comunales.parquet].each do |relative|
    abort "Catastro SII Brecha asset is missing: #{relative}" unless File.file?(File.join(microsite_dir, relative))
  end
  abort "Catastro SII Brecha was localized under /en" if Dir.exist?(File.join(site_dir, "en", microsite))
  abort "Catastro SII Brecha lacks density cells" unless Dir.glob(File.join(microsite_dir, "data", "comunas", "*.json")).length == 346
  parcels_manifest_path = File.join(microsite_dir, "data", "capas_prediales", "manifest.json")
  abort "Catastro SII Brecha parcel-layer manifest is missing" unless File.file?(parcels_manifest_path)
  parcels_manifest = JSON.parse(File.read(parcels_manifest_path))
  abort "Catastro SII Brecha parcel-layer format is invalid" unless parcels_manifest["format"] == "mvt-directory"
  parcels_manifest.fetch("regions", {}).each do |region, layer|
    next unless layer["available"]

    abort "Catastro SII Brecha #{region} parcel layer has invalid format" unless layer["format"] == "mvt-directory"
    %w[tiles metadata].each do |field|
      value = layer[field].to_s
      abort "Catastro SII Brecha #{region} parcel layer has unsafe #{field}" if value.empty? || value.start_with?("/") || value.include?("..")
    end
    metadata_path = File.join(microsite_dir, "data", "capas_prediales", layer.fetch("metadata"))
    abort "Catastro SII Brecha #{region} parcel metadata is missing" unless File.file?(metadata_path)
    metadata = JSON.parse(File.read(metadata_path))
    embedded = JSON.parse(metadata.fetch("json"))
    vector_layer = embedded.fetch("vector_layers").first
    abort "Catastro SII Brecha #{region} parcel layer name is invalid" unless metadata["name"] == "predios_h" && vector_layer["id"] == "predios_h"
    abort "Catastro SII Brecha #{region} parcel fields are not minimized" unless vector_layer.fetch("fields").keys == ["dc_cod_destino"]
  end
  index = File.read(File.join(microsite_dir, "index.html"))
  abort "Catastro SII Brecha canonical URL is missing" unless index.include?("https://3cucharadas.cl/catastro_sii_brecha/")
  abort "Catastro SII Brecha unexpectedly exposes a configured MapTiler key" if index.match?(/maptiler[^<]{0,80}key=[A-Za-z0-9_-]{12,}/i)
  microsite_bytes = 0
  Find.find(microsite_dir) { |entry| microsite_bytes += File.size(entry) if File.file?(entry) }
  abort "Catastro SII Brecha exceeds 60 MB: #{microsite_bytes}" if microsite_bytes > 60_000_000
end

pruned_files.each do |relative|
  abort "Pruned asset is present: #{relative}" if File.exist?(File.join(site_dir, relative))
end

source_maps = Dir.glob(File.join(site_dir, "**", "*.map"))
abort "Source maps are public: #{source_maps.join(', ')}" unless source_maps.empty?

missing_references = []
extract_references = lambda do |body|
  values = body.scan(/\b(?:src|href|poster|content)=["']([^"']+)["']/i).flatten
  values.concat(body.scan(/\bsrcset=["']([^"']+)["']/i).flatten.flat_map { |srcset| srcset.split(",").map { |entry| entry.strip.split(/\s+/, 2).first } })
  values
end

Dir.glob(File.join(site_dir, "**", "*.{html,css}")).each do |document|
  extract_references.call(File.read(document)).each do |raw_value|
    value = CGI.unescapeHTML(raw_value)
    value = value.sub(%r{\Ahttps://3cucharadas\.cl}, "")
    next unless value.match?(%r{\A/(?:assets/|favicon\.ico)})

    relative = value.split(/[?#]/, 2).first.delete_prefix("/")
    missing_references << [document.delete_prefix("#{site_dir}/"), relative] unless File.file?(File.join(site_dir, relative))
  end
end

unless missing_references.empty?
  if draft_fixture_mode
    warn "Ignoring internal asset references from unrelated drafts in fixture mode"
  else
    missing_references.uniq.each { |document, relative| warn "Missing #{relative} referenced by #{document}" }
    abort "Rendered internal asset references are broken"
  end
end

katex_css = File.join(site_dir, "assets/vendor/katex/0.17.0/katex.css")
katex_font_paths = File.read(katex_css).scan(/url\(fonts\/([^\)]+)\)/).flatten.uniq
abort "KaTeX CSS does not reference versioned fonts" if katex_font_paths.empty?

katex_font_paths.each do |font|
  relative = File.join("assets/vendor/katex/0.17.0/fonts", font)
  abort "KaTeX font is missing: #{relative}" unless File.file?(File.join(site_dir, relative))
end

rendered_html = Dir.glob(File.join(site_dir, "**", "*.html"))
forbidden_runtime = {
  "window.MathJax" => "MathJax",
  "cdn.jsdelivr.net/npm/mathjax" => "MathJax",
  "pagead2.googlesyndication.com" => "AdSense",
  "adsbygoogle" => "AdSense"
}.freeze

forbidden_runtime.each do |needle, label|
  offender = rendered_html.find { |document| File.read(document).include?(needle) }
  abort "#{label} remains in rendered output: #{offender.delete_prefix("#{site_dir}/")}" if offender
end

unless draft_fixture_mode
  home = File.read(File.join(site_dir, "index.html"))
  abort "Home LCP card is not eager" unless home.include?('loading="eager"') && home.include?('fetchpriority="high"')
  abort "Home responsive teaser sources are absent" unless home.match?(/srcset=["'][^"']*teaser-[^"']+-640\.webp/)
  abort "Spanish home brand description is stale" unless home.include?("Datos abiertos, estadísticas, MLOps, curiosidades, economía aplicada y políticas sociales, con código reproducible.")

  home_en_path = File.join(site_dir, "en", "index.html")
  abort "English home is missing" unless File.file?(home_en_path)
  home_en = File.read(home_en_path)
  abort "English home brand description is stale" unless home_en.include?("Open data, statistics, MLOps, curiosities, applied economics, and social policy, with reproducible code.")

  hud_titles = {
    "ia/productividad/ai-quota-hud-kde/index.html" => "Cuotas de IA en 3 cucharadas: un HUD para el panel de KDE",
    "en/ia/productividad/ai-quota-hud-kde/index.html" => "AI quotas in three spoonfuls: a HUD for the KDE panel"
  }.freeze

  hud_titles.each do |relative, title|
    path = File.join(site_dir, relative)
    abort "HUD page is missing: #{relative}" unless File.file?(path)
    abort "HUD title is stale: #{relative}" unless File.read(path).include?(title)
  end

  math_documents = %w[
    mlops/bayes-hiperparametros/index.html
    en/mlops/bayes-hiperparametros/index.html
    datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/index.html
    en/datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/index.html
    feed.xml
    en/feed.xml
  ].freeze
  raw_tex_delimiters = ["$$", "\\(", "\\)", "\\[", "\\]"].freeze

  math_documents.each do |relative|
    path = File.join(site_dir, relative)
    abort "Static math document is missing: #{relative}" unless File.file?(path)

    body = File.read(path)
    abort "KaTeX HTML is missing: #{relative}" unless body.include?('class="katex"')
    abort "MathML is missing: #{relative}" unless body.include?("<math")
    abort "KaTeX render error is present: #{relative}" if body.include?("katex-error")
    delimiter = raw_tex_delimiters.find { |marker| body.include?(marker) }
    abort "Raw TeX delimiter #{delimiter.inspect} remains: #{relative}" if delimiter
  end
end

if draft_fixture_mode
  math_drafts = {
    "informatics/prueba-webfonts-katex/index.html" => ['class="nf"', "", "⠿"],
    "r/bioinformatics/biology/prueba-webfonts2/index.html" => ["→", "⇄", "ﬁ"]
  }.freeze

  math_drafts.each do |relative, required_symbols|
    path = File.join(site_dir, relative)
    abort "Math draft fixture is missing: #{relative}" unless File.file?(path)

    body = File.read(path)
    abort "KaTeX HTML is missing from draft: #{relative}" unless body.include?('class="katex"')
    abort "MathML is missing from draft: #{relative}" unless body.include?("<math")
    abort "KaTeX render error is present in draft: #{relative}" if body.include?("katex-error")
    missing_symbol = required_symbols.find { |symbol| !body.include?(symbol) }
    abort "Draft symbol is missing (#{missing_symbol.inspect}): #{relative}" if missing_symbol
  end
end

artifact_bytes = 0
Find.find(site_dir) { |entry| artifact_bytes += File.size(entry) if File.file?(entry) }
unless draft_fixture_mode
  microsite_bytes = 0
  Find.find(microsite_dir) { |entry| microsite_bytes += File.size(entry) if File.file?(entry) } if Dir.exist?(microsite_dir)
  base_artifact_bytes = artifact_bytes - microsite_bytes
  abort "Artifact outside Catastro SII Brecha exceeds #{max_bytes} bytes: #{base_artifact_bytes}" if base_artifact_bytes > max_bytes
end

puts "Artifact verification passed: #{artifact_bytes} bytes"
