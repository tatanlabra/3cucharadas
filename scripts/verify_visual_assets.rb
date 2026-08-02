#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de activos visuales. Corre sobre el ÁRBOL FUENTE (_posts/, assets/,
# _config.yml), no sobre el artefacto construido, así que puede ejecutarse antes
# de `jekyll build` y también como pre-commit local.
#
# Cubre dos cosas que ningún otro verificador del repo mira:
#
#   1. Que todo <img src> de un post resuelva a un archivo real (V9). Hoy una
#      imagen excluida del build pero referenciada desde un post sale rota a
#      producción y el CI pasa en verde.
#   2. Que los manifests _data/visuales/<slug>.yml se cumplan: dimensiones
#      declaradas == reales, cifras citadas presentes en el post, y coherencia
#      entre el estado de cada pieza y el `exclude` de _config.yml.
#
# V9 no depende de que exista manifest: funciona para todos los posts desde ya.
#
# Uso:
#   ruby scripts/verify_visual_assets.rb            # warnings no fallan
#   ruby scripts/verify_visual_assets.rb --strict   # warnings fallan

require "yaml"
require_relative "lib/image_dimensions"

ROOT = File.expand_path("..", __dir__)
STRICT = ARGV.include?("--strict")
MIN_OG_IMAGE_WIDTH = 1200
ROLES_CON_ALT = %w[hero figura og].freeze

errors = []
warnings = []

def rel(path)
  path.delete_prefix("#{ROOT}/")
end

# --- Carga del exclude de _config.yml -------------------------------------

config = YAML.safe_load_file(File.join(ROOT, "_config.yml"), permitted_classes: [Date, Time], aliases: true)
excludes = Array(config["exclude"]).map { |e| e.to_s.chomp("/") }

# Una ruta está excluida si coincide exactamente o cuelga de un prefijo excluido.
def excluded?(path, excludes)
  excludes.any? { |e| path == e || path.start_with?("#{e}/") }
end

# Quita separadores de miles y decimales para comparar cifras entre idiomas:
# "10.343.893" (ES) y "10,343,893" (EN) colapsan al mismo "10343893".
def normaliza_cifra(str)
  str.gsub(/[., \s]/, "")
end

# No reutiliza posts.py::_numbers() del paquete de difusión a propósito: aquel
# compara contra title+description (metadatos públicos) y su regex parte
# "10.343.893" en fragmentos. Acá el corpus es el cuerpo completo del post.
def cifra_presente?(cifra, cuerpo)
  return true if cuerpo.include?(cifra)

  objetivo = normaliza_cifra(cifra)
  return false if objetivo.empty?

  # Compara token completo, no subcadena: evita que "94" case dentro de "1945".
  cuerpo.scan(/\d[\d.,]*%?/).any? { |token| normaliza_cifra(token) == objetivo }
end

# --- Índice de referencias desde los posts --------------------------------

post_paths = Dir.glob(File.join(ROOT, "_posts", "*.md")).sort
abort "No se encontraron posts en _posts/" if post_paths.empty?

# ruta_de_asset => [[post_relativo, alt], ...]
referencias = Hash.new { |h, k| h[k] = [] }
post_bodies = {}

post_paths.each do |path|
  body = File.read(path)
  post_bodies[rel(path)] = body

  # <img src="..."> y srcset, con o sin filtro Liquid alrededor.
  tags = body.scan(/<img\s[^>]*>/i)
  tags.each do |tag|
    alt = tag[/\balt\s*=\s*"([^"]*)"/i, 1]
    srcs = tag.scan(/\b(?:src|srcset)\s*=\s*"([^"]*)"/i).flatten
    srcs.each do |raw|
      # Desenvuelve {{ '/ruta' | relative_url }} y limpia descriptores de srcset.
      raw.scan(%r{/assets/[^"'\s,|\}]+}).each do |asset|
        referencias[asset.delete_prefix("/")] << [rel(path), alt]
      end
    end
  end

  # Front matter: teaser y og_image.
  next unless body.start_with?("---")

  fm_raw = body.split(/^---\s*$/, 3)[1]
  next if fm_raw.nil?

  begin
    fm = YAML.safe_load(fm_raw, permitted_classes: [Date, Time], aliases: true)
  rescue StandardError
    next
  end
  header = fm.is_a?(Hash) ? fm["header"] : nil
  next unless header.is_a?(Hash)

  %w[teaser og_image overlay_image image].each do |key|
    value = header[key]
    next unless value.is_a?(String) && value.start_with?("/assets/")

    referencias[value.delete_prefix("/")] << [rel(path), nil]
  end
end

# --- V9: toda referencia resuelve a un archivo real ------------------------

referencias.each do |asset, usos|
  next if File.file?(File.join(ROOT, asset))

  usos.map(&:first).uniq.each do |post|
    errors << "V9 #{post}: referencia a #{asset}, que no existe en el repo"
  end
end

# --- Manifests -------------------------------------------------------------

manifest_paths = Dir.glob(File.join(ROOT, "_data", "visuales", "*.yml")).sort
slugs_con_manifest = manifest_paths.map { |p| File.basename(p, ".yml") }

manifest_paths.each do |manifest_path|
  manifest_rel = rel(manifest_path)
  manifest = YAML.safe_load_file(manifest_path, permitted_classes: [Date, Time], aliases: true)

  unless manifest.is_a?(Hash) && manifest["piezas"].is_a?(Array)
    errors << "#{manifest_rel}: no tiene una lista `piezas`"
    next
  end

  # Cuerpo de los posts declarados, para contrastar cifras.
  cuerpos = Array(manifest["posts"]).filter_map { |p| post_bodies[p] }
  if cuerpos.empty? && manifest["posts"]
    errors << "#{manifest_rel}: ningún post de `posts` existe en _posts/"
  end
  cuerpo_unido = cuerpos.join("\n")

  manifest["piezas"].each do |pieza|
    id = pieza["id"] || "(sin id)"
    etiqueta = "#{manifest_rel}[#{id}]"
    estado = pieza["estado"]
    archivo = pieza["archivo"]

    unless %w[publicable solo-difusion bloqueado].include?(estado)
      errors << "#{etiqueta}: estado inválido #{estado.inspect}"
      next
    end

    if archivo.nil?
      # Solo una pieza bloqueada puede no tener archivo: se eliminó del repo y
      # la entrada se conserva por el catálogo de errores.
      errors << "#{etiqueta}: sin `archivo` y no está bloqueada" unless estado == "bloqueado"
      next
    end

    ruta = File.join(ROOT, archivo)
    existe = File.file?(ruta)

    # V1: el archivo declarado existe (salvo pieza bloqueada ya eliminada).
    if !existe
      if estado == "bloqueado"
        next
      end
      errors << "V1 #{etiqueta}: #{archivo} no existe"
      next
    end

    # V2 y V3: dimensiones declaradas vs reales vs nombre.
    declarado_w = pieza["ancho"]
    declarado_h = pieza["alto"]
    reales = image_dimensions(ruta)

    if reales.nil?
      # SVG y formatos sin encabezado binario: no verificable, no es error.
      if declarado_w || declarado_h
        warnings << "V2 #{etiqueta}: declara dimensiones pero #{File.extname(archivo)} no es verificable; se ignoran"
      end
    elsif declarado_w.nil? || declarado_h.nil?
      warnings << "V2 #{etiqueta}: sin ancho/alto declarados (reales #{reales[0]}x#{reales[1]})"
    elsif [declarado_w, declarado_h] != reales
      errors << "V2 #{etiqueta}: declara #{declarado_w}x#{declarado_h} pero #{archivo} mide #{reales[0]}x#{reales[1]}"
    end

    # Anclado antes de la extensión: un nombre como
    # bivariado-clasificacion-4x2-1200x1685.webp lleva "4x2" en el nombre y las
    # dimensiones al final. Sin anclar, el "4x2" gana.
    if (m = File.basename(archivo).match(/(\d+)x(\d+)\.\w+\z/)) && declarado_w && declarado_h
      nombre = [m[1].to_i, m[2].to_i]
      if nombre != [declarado_w, declarado_h]
        errors << "V3 #{etiqueta}: el nombre dice #{nombre[0]}x#{nombre[1]} pero declara #{declarado_w}x#{declarado_h}"
      end
    end

    # V4: convención de nombres. Solo aviso, y solo para activos editoriales
    # colocados a mano: los generados desde los datos siguen el naming de su
    # pipeline (sankey-pipeline.webp, violin-denominadores.webp) y renombrarlos
    # en masa rompería los posts sin ganar nada.
    if pieza["origen"] != "datos" && File.extname(archivo) != ".svg" &&
       !File.basename(archivo).match?(/\d+x\d+\.\w+\z/)
      warnings << "V4 #{etiqueta}: #{File.basename(archivo)} no sigue la convención <nombre>-<ancho>x<alto>.<ext>"
    end

    usos = referencias[archivo] || []

    # V5: las cifras declaradas aparecen en el cuerpo del post.
    Array(pieza["cifras"]).each do |cifra|
      next if cuerpo_unido.empty?
      next if cifra_presente?(cifra, cuerpo_unido)

      errors << "V5 #{etiqueta}: la cifra #{cifra.inspect} no aparece en el cuerpo del post"
    end

    case estado
    when "publicable"
      # V7: una pieza publicable no puede estar excluida del build.
      if excluded?(archivo, excludes)
        errors << "V7 #{etiqueta}: es publicable pero #{archivo} está en el `exclude` de _config.yml"
      end

      # V11: og real >= 1200px de ancho.
      if pieza["rol"] == "og" && reales && reales[0] < MIN_OG_IMAGE_WIDTH
        errors << "V11 #{etiqueta}: og de #{reales[0]}px, mínimo #{MIN_OG_IMAGE_WIDTH}px"
      end

      # V12: alt no vacío en los roles que lo exigen.
      # Los .svg suelen ser el acompañante vectorial de un .webp que ya lleva el
      # alt en su <img>; exigirles alt propio duplicaría el texto.
      if ROLES_CON_ALT.include?(pieza["rol"]) && File.extname(archivo) != ".svg"
        alt = pieza["alt"]
        vacio = !alt.is_a?(Hash) || alt.values.all? { |v| v.to_s.strip.empty? }
        warnings << "V12 #{etiqueta}: rol #{pieza["rol"]} sin `alt`" if vacio
      end

      # V12b: el alt real del <img> en el post tampoco puede estar vacío.
      usos.each do |post, alt_real|
        next if alt_real.nil? # front matter, no lleva alt
        next unless alt_real.strip.empty?

        errors << "V12 #{post}: <img> de #{archivo} sin alt"
      end

    when "solo-difusion", "bloqueado"
      # V6: no puede estar referenciada desde ningún post.
      usos.map(&:first).uniq.each do |post|
        errors << "V6 #{etiqueta}: es #{estado} pero #{post} la referencia"
      end

      # V8: debe estar cubierta por el `exclude` de _config.yml.
      if existe && !excluded?(archivo, excludes)
        errors << "V8 #{etiqueta}: es #{estado} pero #{archivo} no está en el `exclude` de _config.yml"
      end
    end
  end

  # V10: teaser y og_image del front matter apuntan a piezas publicables.
  publicables = manifest["piezas"]
                .select { |p| p["estado"] == "publicable" && p["archivo"] }
                .map { |p| p["archivo"] }

  Array(manifest["posts"]).each do |post_rel|
    body = post_bodies[post_rel]
    next unless body&.start_with?("---")

    fm_raw = body.split(/^---\s*$/, 3)[1]
    next if fm_raw.nil?

    fm = begin
      YAML.safe_load(fm_raw, permitted_classes: [Date, Time], aliases: true)
    rescue StandardError
      nil
    end
    header = fm.is_a?(Hash) ? fm["header"] : nil
    next unless header.is_a?(Hash)

    %w[teaser og_image].each do |key|
      value = header[key]
      next unless value.is_a?(String) && value.start_with?("/assets/")

      asset = value.delete_prefix("/")
      next if publicables.include?(asset)

      errors << "V10 #{post_rel}: header.#{key} apunta a #{asset}, que no es una pieza publicable de #{manifest_rel}"
    end
  end
end

# --- V13: posts con carpeta de activos propia deberían tener manifest ------

Dir.glob(File.join(ROOT, "assets", "images", "*")).each do |dir|
  next unless File.directory?(dir)

  slug = File.basename(dir)
  # Carpetas de infraestructura del sitio, no activos de un post.
  next if %w[teasers home favicons 404].include?(slug)
  next if slugs_con_manifest.include?(slug)

  warnings << "V13 assets/images/#{slug}/ no tiene manifest en _data/visuales/"
end

# --- Salida ----------------------------------------------------------------

warnings.uniq.each { |w| warn "- aviso: #{w}" }
errors.uniq.each { |e| warn "- #{e}" }

if !errors.empty?
  abort "Gate de activos visuales falló (#{errors.uniq.length} problema(s))"
elsif STRICT && !warnings.empty?
  abort "Gate de activos visuales falló en modo --strict (#{warnings.uniq.length} aviso(s))"
end

referenciados = referencias.keys.length
puts "Gate de activos visuales OK: #{manifest_paths.length} manifest(s), " \
     "#{referenciados} activo(s) referenciados desde #{post_paths.length} posts, " \
     "#{warnings.uniq.length} aviso(s)."
