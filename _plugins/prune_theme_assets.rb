# frozen_string_literal: true

# Minimal Mistakes ships source assets alongside the compiled files used by the
# site. Keep only the browser-facing runtime bundle in the generated artifact.
Jekyll::Hooks.register :site, :post_read do |site|
  exact_paths = %w[
    assets/images/catppuccin_latte-skin-archive-large.png
    assets/images/catppuccin_mocha-skin-archive-large.png
    assets/js/_main.js
    assets/js/lunr/lunr-gr.js
    assets/js/lunr/lunr.js
    assets/js/main.min.js
    assets/js/main.min.js.map
  ].freeze

  path_prefixes = %w[
    assets/js/plugins/
    assets/js/vendor/
  ].freeze

  prunable_path = lambda do |relative_path|
    path = relative_path.delete_prefix("/")
    exact_paths.include?(path) || path_prefixes.any? { |prefix| path.start_with?(prefix) }
  end

  site.static_files.reject! { |static_file| prunable_path.call(static_file.relative_path) }

  # Theme files with YAML front matter (for example lunr-gr.js) are Pages,
  # not StaticFiles, so they must be removed from that collection as well.
  site.pages.reject! { |page| prunable_path.call(page.path) }

  # El main.scss de la gema. En español lo sombrea el del sitio, pero en la pasada
  # inglesa Polyglot excluye `assets` del sitio y el del tema reaparecía: se publicaba
  # /en/assets/css/main.css (72 KB, CSS por defecto del tema, ninguna página lo enlaza)
  # y era la fuente de los últimos avisos de @import del build. Capa 2C, 2026-10-17.
  theme_root = site.theme&.root
  if theme_root
    site.pages.reject! do |page|
      page.name == "main.scss" && page.instance_variable_get(:@base).to_s.start_with?(theme_root)
    end
  end
end
