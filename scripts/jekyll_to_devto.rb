#!/usr/bin/env ruby
# frozen_string_literal: true

require "cgi"
require "json"
require "shellwords"
require "uri"
require "yaml"
require_relative "lib/ai_disclosure"

# Transformación determinista del Markdown canónico de Jekyll al dialecto que
# acepta DEV.to. El fuente nunca se modifica: este módulo solo devuelve texto.
module JekyllToDevto
  SITE_URL = "https://3cucharadas.cl"
  ROOT = File.expand_path("..", __dir__)
  AI_DISCLOSURE_LEVELS = AiDisclosure::LEVELS
  DEFAULT_AI_DISCLOSURE_LEVEL = "not_disclosed"

  # DEV.to hace pasar los <img> externos por su optimizador. Ese proxy declara
  # WebP para un SVG de 3cucharadas.cl pero entrega los bytes SVG sin convertir,
  # por lo que el navegador lo descarta. El mapeo es explícito y verificable:
  # el post Jekyll conserva el vector y solo el artefacto DEV usa el ráster.
  DEVTO_RASTERS = {
    "/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.svg" =>
      "/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp",
    "/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.svg" =>
      "/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.webp",
    "/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en.svg" =>
      "/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en-devto-1200x2172.png",
    "/assets/images/structured-shell/fig-d2-shell-families-mobile-en.svg" =>
      "/assets/images/structured-shell/fig-d2-shell-families-mobile-en-devto-1080x2710.png",
    "/assets/images/structured-shell/fig-d2-shell-families-en.svg" =>
      "/assets/images/structured-shell/fig-d2-shell-families-en-devto-1600x1360.png",
    "/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg" =>
      "/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources-devto-1600x1169.png"
  }.freeze

  # Tags documentados por Forem y tags de bloque que DEV.to ya admite. La lista
  # es deliberadamente explícita: un tag Jekyll nuevo no debe cruzar por accidente.
  FOREM_TAGS = %w[
    blogcast codepen codesandbox details devcomment dotnetfiddle embed enddetails
    endkatex endquote github glitch instagram jsfiddle katex kotlin link nexttech
    podcast quote raw reddit endraw replit slideshare soundcloud speakerdeck spotify
    stackblitz stackery tag twitch twitter user vimeo wikipedia youtube
  ].freeze
  LITERAL_BLOCKS = %w[katex raw].freeze

  FENCE_OPEN = /\A {0,3}(`{3,}|~{3,})/.freeze
  KRAMDOWN_IAL = /[ \t]*\{:\s*[^}\n]+\}[ \t]*(?=\n|\z)/.freeze
  HTML_URL_ATTR = /\b(src|href|poster)=(['"])(.*?)\2/i.freeze
  HTML_SRCSET_ATTR = /\bsrcset=(['"])(.*?)\1/i.freeze
  VIDEO_FIGURE = %r{<figure[^>]*>\s*<video\b([^>]*)>.*?</video>\s*(<figcaption>(.*?)</figcaption>)?\s*</figure>}mi.freeze
  HTML_ATTR = /([\w:-]+)=(['"])(.*?)\2/.freeze

  class TransformError < StandardError; end

  Result = Struct.new(:body, :warnings, keyword_init: true)

  module_function

  def youtube_id_from_url(url)
    return nil unless url

    match = url.match(%r{(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([\w-]{11})})
    match && match[1]
  end

  def transform(body, site_url: SITE_URL, canonical_url:, page: {}, youtube_id: nil)
    warnings = []
    transformed = map_fenced_blocks(body) do |markdown|
      transform_unfenced(markdown, site_url:, canonical_url:, page:, youtube_id:, warnings:)
    end
    transformed = transformed.strip
    validate!(transformed)
    Result.new(body: transformed, warnings: warnings.uniq)
  end

  # El editor Markdown básico de DEV publica al cambiar `published: false` a
  # `true`. La generación local siempre parte como borrador; al actualizar por
  # API, el llamador debe pasar el estado remoto para no despublicar artículos.
  def render_document(body:, title:, description:, tags:, canonical_url:, cover_image: nil,
                      published: false, ai_disclosure_level: DEFAULT_AI_DISCLOSURE_LEVEL)
    tags = Array(tags)
    raise TransformError, "front matter DEV.to inválido: máximo 4 tags" if tags.length > 4
    unless [true, false].include?(published)
      raise TransformError, "front matter DEV.to inválido: published debe ser booleano"
    end
    unless AI_DISCLOSURE_LEVELS.include?(ai_disclosure_level)
      raise TransformError, "front matter DEV.to inválido: ai_disclosure_level inválido"
    end

    metadata = {
      "title" => title,
      "published" => published,
      "description" => description,
      "tags" => tags.join(", "),
      "canonical_url" => canonical_url,
      "cover_image" => cover_image,
      "ai_disclosure_level" => ai_disclosure_level
    }.compact
    # Forem acepta front matter, pero su parser rechaza algunas formas válidas
    # que Psych elige para textos largos (plegado `>-` y continuaciones). JSON
    # produce escalares entre comillas que también son YAML válido y mantiene
    # cada campo en una sola línea, sin heurísticas dependientes del contenido.
    yaml = metadata.map do |key, value|
      serialized = [true, false].include?(value) ? value.to_s : JSON.generate(value.to_s)
      "#{key}: #{serialized}"
    end.join("\n")
    document = "---\n#{yaml}\n---\n\n#{body.rstrip}\n"
    validate!(document)
    document
  end

  # Falla cerrado antes de cualquier llamada a la API. Los ejemplos Liquid en
  # cercos, spans de código y bloques raw/katex son literales y no cuentan.
  def validate!(markdown)
    problems = []
    each_validated_plain_segment(markdown) do |segment|
      problems << "filtro relative_url" if segment.match?(/\|\s*relative_url\b/)
      problems << "variable site.*" if segment.match?(/\{\{[-]?\s*site\./)
      problems << "variable page.*" if segment.match?(/\{\{[-]?\s*page\./)
      problems << "salida Liquid {{ ... }}" if segment.include?("{{")
      problems << "extensión Kramdown" if segment.match?(KRAMDOWN_IAL)
      if segment.match?(%r{(?:https?://[^\s"'<>)]*|/assets/[^\s"'<>)]*)\.svg(?:[?#][^\s"'<>)]*)?}i)
        problems << "referencia SVG no portable"
      end

      segment.scan(/\{%[-]?\s*([A-Za-z_][\w-]*)/) do |match|
        tag = match.first.downcase
        problems << "tag Liquid no permitido: #{tag}" unless FOREM_TAGS.include?(tag)
      end
    end
    return true if problems.empty?

    raise TransformError, "borrador DEV.to inválido: #{problems.uniq.join('; ')}"
  end

  def map_fenced_blocks(markdown)
    output = +""
    plain = +""
    fence = nil

    markdown.each_line do |line|
      if fence
        output << line
        fence = nil if closes_fence?(line, fence)
        next
      end

      match = line.match(FENCE_OPEN)
      if match
        output << yield(plain) unless plain.empty?
        plain.clear
        fence = match[1]
        output << line
      else
        plain << line
      end
    end

    output << yield(plain) unless plain.empty?
    output
  end

  def closes_fence?(line, fence)
    marker = Regexp.escape(fence[0])
    line.match?(/\A {0,3}#{marker}{#{fence.length},}[ \t]*\r?\n?\z/)
  end

  def transform_unfenced(markdown, site_url:, canonical_url:, page:, youtube_id:, warnings:)
    markdown = transform_video_figures(markdown, site_url:, canonical_url:, youtube_id:)
    output = +""
    in_math = false
    literal_block = nil

    markdown.each_line do |line|
      if literal_block
        output << line
        literal_block = nil if line.match?(/\{%[-]?\s*end#{Regexp.escape(literal_block)}\s*[-]?%\}/i)
        next
      end

      if (literal = literal_block_start(line))
        output << line
        literal_block = literal unless line.match?(/\{%[-]?\s*end#{Regexp.escape(literal)}\s*[-]?%\}/i)
        next
      end

      if in_math
        if line.match?(/^\s*\$\$\s*$/)
          output << "{% endkatex %}\n"
          in_math = false
        else
          output << line
        end
        next
      end

      if (same_line_math = line.match(/^\s*\$\$(.*?)\$\$\s*$/))
        output << "{% katex %} #{same_line_math[1].strip} {% endkatex %}\n"
      elsif line.match?(/^\s*\$\$\s*$/)
        output << "{% katex %}\n"
        in_math = true
      else
        output << map_inline_code(line) do |plain|
          transform_plain(plain, site_url:, canonical_url:, page:, warnings:)
        end
      end
    end

    raise TransformError, "bloque matemático $$ sin cierre" if in_math

    output
  end

  def literal_block_start(line)
    # NO se usa una clase negada [^%]* para los argumentos del tag: termina el tag
    # en el primer `%` de sus propios argumentos, asi que un `{% katex ... 95% ... %}`
    # no casa y el bloque literal no se detecta. Es el fallo de septiembre de 2026,
    # que quedo anotado como pariente y sin arreglar. find_liquid_close respeta las
    # comillas y devuelve el cierre real, sin suponer nada del contenido.
    match = line.match(/\{%[-]?\s*(katex|raw)\b/i)
    return nil unless match
    return nil unless find_liquid_close(line, match.end(0), "%}")

    match[1].downcase
  end

  # Rangos que ocupan las etiquetas Liquid ({{ ... }} y {% ... %}) en una linea.
  # Se recorre con el MISMO escaner que usa transform_liquid, para que los tramos
  # que aqui se protegen sean exactamente los que alli se consumen.
  def liquid_spans(text)
    spans = []
    cursor = 0

    while cursor < text.length
      output_start = text.index("{{", cursor)
      tag_start = text.index("{%", cursor)
      start = [output_start, tag_start].compact.min
      break unless start

      closer = start == output_start ? "}}" : "%}"
      finish = find_liquid_close(text, start + 2, closer)
      break unless finish

      spans << (start...(finish + closer.length))
      cursor = finish + closer.length
    end

    spans
  end

  # Primera comilla invertida en `from` o despues que NO caiga dentro de un tag Liquid.
  def next_inline_code_tick(text, from, spans)
    cursor = from

    while (tick = text.index("`", cursor))
      span = spans.find { |range| range.cover?(tick) }
      return tick unless span

      cursor = span.end
    end

    nil
  end

  def map_inline_code(text)
    output = +""
    cursor = 0
    # Una comilla invertida DENTRO de un tag Liquid no abre codigo en linea: el tag
    # es una unidad y hay que entregarlo entero a transform_liquid. Si se parte por
    # las comillas primero, a transform_liquid le llega `{% include figure ...` sin
    # su `%}` y revienta con "Liquid sin cierre". Medido el 2026-09-09 sobre
    # _posts/2026-07-15-ai-quota-hud-kde-en.md, con un caption que citaba `OFICIAL`.
    spans = liquid_spans(text)

    while (opening = next_inline_code_tick(text, cursor, spans))
      output << yield(text[cursor...opening])
      run = text[opening..].match(/\A`+/)[0]
      closing = text.index(run, opening + run.length)
      unless closing
        output << yield(text[opening..])
        return output
      end

      output << text[opening...(closing + run.length)]
      cursor = closing + run.length
    end

    output << yield(text[cursor..])
    output
  end

  def transform_plain(text, site_url:, canonical_url:, page:, warnings:)
    transformed = transform_liquid(text, site_url:, canonical_url:, page:, warnings:)
    transformed = transformed.gsub(KRAMDOWN_IAL, "")
    transformed = absolutize_html_attributes(transformed, site_url)
    transformed = rewrite_internal_svg_urls(transformed, site_url)
    transformed
  end

  def rewrite_internal_svg_urls(text, site_url)
    site_root = site_url.chomp("/")
    pattern = %r{(?:#{Regexp.escape(site_root)})?(?<path>/assets/[^\s"'<>),]+\.svg)(?<suffix>[?#][^\s"'<>),]*)?}i
    extensions = []
    transformed = text.gsub(pattern) do
      svg_path = Regexp.last_match(:path)
      suffix = Regexp.last_match(:suffix).to_s
      raster_path = DEVTO_RASTERS[svg_path]
      unless raster_path
        raise TransformError,
              "falta mapeo ráster DEV.to para #{svg_path}; ejecute scripts/generate_devto_rasters.sh"
      end

      local_raster = File.expand_path(raster_path.delete_prefix("/"), ROOT)
      unless local_raster.start_with?("#{File.join(ROOT, 'assets')}/") && File.file?(local_raster)
        raise TransformError,
              "falta ráster DEV.to #{raster_path}; ejecute scripts/generate_devto_rasters.sh"
      end

      extensions << File.extname(raster_path).downcase
      "#{site_root}#{raster_path}#{suffix}"
    end

    return transformed if extensions.empty?

    mime_types = extensions.uniq.map { |extension| extension == ".webp" ? "image/webp" : "image/png" }
    if mime_types.one?
      transformed.gsub(/\btype=(['"])image\/svg\+xml\1/i) do
        quote = Regexp.last_match(1)
        "type=#{quote}#{mime_types.first}#{quote}"
      end
    else
      transformed
    end
  end

  def transform_liquid(text, site_url:, canonical_url:, page:, warnings:)
    output = +""
    cursor = 0

    while cursor < text.length
      output_start = text.index("{{", cursor)
      tag_start = text.index("{%", cursor)
      start = [output_start, tag_start].compact.min
      unless start
        output << text[cursor..]
        break
      end

      output << text[cursor...start]
      is_output = start == output_start
      closer = is_output ? "}}" : "%}"
      finish = find_liquid_close(text, start + 2, closer)
      raise TransformError, "Liquid sin cierre cerca de: #{text[start, 80].inspect}" unless finish

      inner = text[(start + 2)...finish].sub(/\A-/, "").sub(/-\z/, "").strip
      output << if is_output
                  resolve_output(inner, site_url:, canonical_url:, page:, warnings:)
                else
                  transform_tag(inner, site_url:, canonical_url:, page:, warnings:)
                end
      cursor = finish + 2
    end

    output
  end

  def find_liquid_close(text, cursor, closer)
    quote = nil
    escaped = false

    while cursor < text.length
      char = text[cursor]
      if escaped
        escaped = false
      elsif char == "\\" && quote
        escaped = true
      elsif quote
        quote = nil if char == quote
      elsif char == "'" || char == '"'
        quote = char
      elsif text[cursor, closer.length] == closer
        return cursor
      end
      cursor += 1
    end

    nil
  end

  def resolve_output(expression, site_url:, canonical_url:, page:, warnings:)
    pipeline = split_outside_quotes(expression, "|")
    value = resolve_value(pipeline.shift.to_s.strip, site_url:, canonical_url:, page:)
    unless value
      warnings << "salida Liquid eliminada: #{expression}"
      return ""
    end

    pipeline.each do |raw_filter|
      name, raw_argument = split_filter(raw_filter)
      case name
      when "relative_url", "absolute_url"
        value = absolute_url(value, site_url, force_relative: true)
      when "append"
        value += resolve_value(raw_argument, site_url:, canonical_url:, page:).to_s
      when "prepend"
        value = resolve_value(raw_argument, site_url:, canonical_url:, page:).to_s + value
      when "strip"
        value = value.strip
      when "downcase"
        value = value.downcase
      when "upcase"
        value = value.upcase
      when "escape", "escape_once"
        value = CGI.escapeHTML(value)
      else
        warnings << "salida Liquid con filtro no soportado eliminada: #{expression}"
        return ""
      end
    end

    value
  end

  def resolve_value(token, site_url:, canonical_url:, page:)
    token = token.to_s.strip
    return token[1...-1].gsub(/\\(['"\\])/, "\\1") if quoted?(token)

    page_url = URI.parse(canonical_url).path
    values = {
      "site.url" => site_url,
      "site.baseurl" => "",
      "page.url" => page_url,
      "page.title" => page[:title] || page["title"],
      "page.description" => page[:description] || page["description"]
    }
    value = values[token]
    value.nil? ? nil : value.to_s
  rescue URI::InvalidURIError
    nil
  end

  def quoted?(token)
    token.length >= 2 && %w[' "].include?(token[0]) && token[-1] == token[0]
  end

  def split_outside_quotes(text, delimiter)
    parts = []
    current = +""
    quote = nil
    escaped = false

    text.each_char do |char|
      if escaped
        current << char
        escaped = false
      elsif char == "\\" && quote
        current << char
        escaped = true
      elsif quote
        current << char
        quote = nil if char == quote
      elsif char == "'" || char == '"'
        current << char
        quote = char
      elsif char == delimiter
        parts << current
        current = +""
      else
        current << char
      end
    end

    parts << current
    parts
  end

  def split_filter(raw_filter)
    pieces = split_outside_quotes(raw_filter, ":")
    [pieces.shift.to_s.strip.downcase, pieces.join(":").strip]
  end

  def transform_tag(inner, site_url:, canonical_url:, page:, warnings:)
    name, arguments = inner.split(/\s+/, 2)
    name = name.to_s.downcase

    return "{% #{inner} %}" if FOREM_TAGS.include?(name)

    if name == "include"
      include_name, include_arguments = arguments.to_s.split(/\s+/, 2)
      return transform_figure_include(include_arguments, site_url) if include_name == "figure"
      return transform_gallery_include(include_arguments, page, site_url, warnings) if include_name == "gallery"

      warnings << "include Jekyll eliminado: #{include_name}"
      return ""
    end

    return "```#{arguments.to_s.split.first}\n" if name == "highlight"
    return "```\n" if name == "endhighlight"

    warnings << "tag Liquid Jekyll eliminado: #{name}"
    ""
  end

  def transform_figure_include(arguments, site_url)
    attributes = Shellwords.shellsplit(arguments.to_s).filter_map do |token|
      key, value = token.split("=", 2)
      [key, value] if key && value
    end.to_h
    image = attributes["image_path"]
    alt = attributes.fetch("alt", "")
    caption = attributes["caption"]
    parts = []
    parts << "![#{alt}](#{absolute_url(image, site_url, force_relative: true)})" if image
    parts << caption if caption
    parts.join("\n\n")
  rescue ArgumentError
    ""
  end

  def transform_gallery_include(arguments, page, site_url, warnings)
    attributes = parse_include_attributes(arguments)
    gallery_id = attributes["id"]
    images = gallery_id && (page[gallery_id] || page[gallery_id.to_sym])
    unless images.is_a?(Array) && !images.empty?
      warnings << "include Jekyll eliminado: gallery #{gallery_id || '(sin id)'} no resuelta"
      return ""
    end

    parts = images.filter_map do |image|
      next unless image.is_a?(Hash)

      path = image["image_path"] || image[:image_path] || image["url"] || image[:url]
      next unless path

      alt = (image["alt"] || image[:alt] || "").to_s.gsub("]", "\\]")
      title = image["title"] || image[:title]
      markdown = "![#{alt}](#{absolute_url(path.to_s, site_url, force_relative: true)})"
      title ? "#{markdown}\n\n*#{title}*" : markdown
    end
    parts << attributes["caption"] if attributes["caption"]
    parts.join("\n\n")
  rescue ArgumentError
    warnings << "include Jekyll eliminado: gallery con atributos inválidos"
    ""
  end

  def parse_include_attributes(arguments)
    Shellwords.shellsplit(arguments.to_s).filter_map do |token|
      key, value = token.split("=", 2)
      [key, value] if key && value
    end.to_h
  end

  def transform_video_figures(markdown, site_url:, canonical_url:, youtube_id:)
    markdown.gsub(VIDEO_FIGURE) do
      caption = Regexp.last_match(3)
      attributes = Regexp.last_match(1).to_s.scan(HTML_ATTR).to_h { |key, _quote, value| [key, value] }
      poster = attributes["poster"]
      alt = attributes["aria-label"] || "Video demonstration"
      parts = []
      if youtube_id
        parts << "{% youtube #{youtube_id} %}"
      elsif poster
        poster_url = absolute_url(poster, site_url, force_relative: true)
        parts << "[![#{alt}](#{poster_url})](#{canonical_url})"
        parts << "*Watch the full video demo on [3cucharadas.cl](#{canonical_url}).*"
      end
      parts << caption if caption
      parts.join("\n\n")
    end
  end

  def absolutize_html_attributes(text, site_url)
    transformed = text.gsub(HTML_URL_ATTR) do
      name = Regexp.last_match(1)
      quote = Regexp.last_match(2)
      value = Regexp.last_match(3)
      "#{name}=#{quote}#{absolute_url(value, site_url)}#{quote}"
    end
    transformed.gsub(HTML_SRCSET_ATTR) do
      quote = Regexp.last_match(1)
      candidates = Regexp.last_match(2).split(",").map do |candidate|
        url, descriptor = candidate.strip.split(/\s+/, 2)
        [absolute_url(url, site_url), descriptor].compact.join(" ")
      end
      "srcset=#{quote}#{candidates.join(', ')}#{quote}"
    end
  end

  def absolute_url(value, site_url, force_relative: false)
    return value unless value
    return value if value.match?(%r{\A(?:https?:)?//}) || value.start_with?("#", "mailto:", "data:")

    return "#{site_url.chomp('/')}#{value}" if value.start_with?("/")
    return "#{site_url.chomp('/')}/#{value}" if force_relative

    value
  end

  def each_validated_plain_segment(markdown, &block)
    map_fenced_blocks(markdown) do |unfenced|
      without_literals = unfenced.gsub(/\{%[-]?\s*(katex|raw)\b.*?%\}.*?\{%[-]?\s*end\1\s*[-]?%\}/mi, "")
      without_literals.each_line do |line|
        map_inline_code(line) do |plain|
          block.call(plain)
          plain
        end
      end
      unfenced
    end
    nil
  end
end
