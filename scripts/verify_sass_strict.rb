#!/usr/bin/env ruby
# frozen_string_literal: true

# Compila assets/css/main.scss sin silenciar ningún aviso de Sass y reprueba ante el
# primero (capa 2C, auditoría UX 2026-10-17).
#
# Por qué existe: _config.yml compila con `quiet_deps`, que calla los avisos de los
# archivos cargados por load path. Con la Sass del tema eso escondía 245 de 249 avisos
# (@import, funciones globales, if(), división con /, color). Tras migrar el tema a
# módulos el build no tiene ninguno, y este gate impide que vuelvan sin que nadie lo vea.
#
# El Liquid de main.scss se reduce a lo que hace hoy: `{{ 'ruta' | relative_url }}`
# → 'ruta' (baseurl vacío). Cualquier otro Liquid hace fallar el gate, a propósito.
require "sass-embedded"

root = File.expand_path("..", __dir__)
source = File.read(File.join(root, "assets/css/main.scss"), encoding: "utf-8")
body = source.sub(/\A---\n.*?\n---\n/m, "")
body = body.gsub(/\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}/) { Regexp.last_match(1) }
abort "verify_sass_strict: queda Liquid sin traducir en main.scss" if body.match?(/\{\{|\{%/)

warnings = []
logger = Object.new
logger.define_singleton_method(:warn) do |message, options = nil|
  type = options.respond_to?(:deprecation_type) ? options.deprecation_type : nil
  kind = type.nil? ? "warn" : (type.respond_to?(:id) ? type.id : type.to_s)
  where = options.respond_to?(:span) && options.span ? "#{options.span.url}:#{options.span.start.line + 1}" : "?"
  warnings << "#{kind} #{where}: #{message.lines.first.strip}"
end
logger.define_singleton_method(:debug) { |*| }

css = Sass.compile_string(body, load_paths: [File.join(root, "_sass")], style: :compressed,
                                quiet_deps: false, verbose: true, logger: logger).css
abort "verify_sass_strict: CSS vacío" if css.bytesize < 100_000
abort "verify_sass_strict: faltan los tokens del sitio" unless css.include?("--ui-paper")

if warnings.empty?
  puts "Sass estricto: 0 avisos, #{css.bytesize} bytes"
else
  warn "Sass estricto: #{warnings.size} avisos"
  warnings.first(10).each { |line| warn "  #{line}" }
  exit 1
end
