#!/usr/bin/env ruby
# frozen_string_literal: true

# Sindicación automatizada a dev.to para posts EN que declaran
# `distribution.republish: [dev]`; `sindicar: true` se acepta solo como alias
# heredado. Los artículos nuevos se crean como borrador. Los ya registrados se
# actualizan sin enviar `published`, por lo que conservan su estado remoto.
# El id se guarda en _data/distribucion.yml para actualizar sin duplicar.
#
# Fusible: sin DEV_TO_API_KEY configurado, no hace nada. Así el workflow
# puede existir y correr sin que nadie active la sindicación real hasta que
# el secreto se configure deliberadamente en GitHub.
#
# DEVTO_DRY_RUN=1 simula sin llamar a la API ni escribir _data/distribucion.yml.

require "net/http"
require "json"
require "yaml"
require "date"

api_key = ENV["DEV_TO_API_KEY"]
if api_key.nil? || api_key.strip.empty?
  puts "DEV_TO_API_KEY no configurado; nada que sindicar."
  exit 0
end

site_root = File.expand_path("..", __dir__)
posts_dir = File.join(site_root, "_posts")
distribucion_path = File.join(site_root, "_data", "distribucion.yml")
dry_run = ENV["DEVTO_DRY_RUN"] == "1"

def parse_front_matter(path)
  text = File.read(path)
  return [{}, ""] unless text.start_with?("---\n")

  parts = text.split(/^---\s*$/, 3)
  return [{}, text] if parts.length < 3

  [YAML.safe_load(parts[1], permitted_classes: [Date, Time]) || {}, parts[2].strip]
end

FIGURE_TAG = /\{%-?\s*include\s+figure\s+([^%]*?)-?%\}/.freeze
ATTR = /(\w+)="([^"]*)"/.freeze
KRAMDOWN_IAL = /\n?\{:\s*\.[\w-]+(?:\s+\.[\w-]+)*\s*\}\n?/.freeze
RELATIVE_ASSET_ATTR = /(src|poster|href)="(\/[^"]+)"/.freeze
VIDEO_FIGURE = %r{<figure[^>]*>\s*<video\b([^>]*)>.*?</video>\s*(<figcaption>(.*?)</figcaption>)?\s*</figure>}m.freeze

# dev.to rechaza cualquier `{% include %}` (lo desactivan por seguridad: 422
# "Liquid#include tag is disabled"). El tema usa `{% include figure ... %}`
# para imágenes con caption/lightbox en casi todos los posts — se convierte a
# markdown plano. Cualquier otro include desconocido se elimina (con aviso),
# en vez de dejar que rompa la llamada entera a la API.
#
# Además: {: .clase} (Kramdown IAL, ej. `{: .text-justify}`) queda como texto
# literal para dev.to — se elimina. Y cualquier atributo src/poster/href con
# ruta relativa al sitio (ej. el <video> autoalojado) se resuelve a absoluta,
# porque dev.to renderiza el cuerpo fuera del contexto del sitio.
def youtube_id_from_url(url)
  return nil unless url

  match = url.match(%r{(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([\w-]{11})})
  match && match[1]
end

def sanitize_body_for_devto(body, site_url, canonical_url, youtube_id: nil)
  warnings = []
  sanitized = body.gsub(FIGURE_TAG) do
    attrs = Regexp.last_match(1).to_s.scan(ATTR).to_h
    image = attrs["image_path"]
    alt = attrs["alt"] || ""
    caption = attrs["caption"]
    image_url = image ? "#{site_url}#{image}" : nil
    parts = []
    parts << "![#{alt}](#{image_url})" if image_url
    parts << caption if caption
    parts.join("\n\n")
  end

  # dev.to elimina <video>/<source> por seguridad y solo deja el texto de
  # respaldo huérfano ("your browser does not support..."), sin el elemento
  # que ese texto describe. Si hay devto_video_url (YouTube), se embebe de
  # verdad con el tag Liquid propio de dev.to; si no, se cae al poster como
  # imagen enlazada al post original, en vez de dejar ese fragmento roto.
  sanitized = sanitized.gsub(VIDEO_FIGURE) do
    caption = Regexp.last_match(3)
    video_attrs = Regexp.last_match(1).to_s.scan(ATTR).to_h
    poster = video_attrs["poster"]
    alt = video_attrs["aria-label"] || "Video demonstration"
    poster_url = poster ? (poster.start_with?("/") ? "#{site_url}#{poster}" : poster) : nil
    parts = []
    if youtube_id
      parts << "{% youtube #{youtube_id} %}"
    elsif poster_url
      parts << "[![#{alt}](#{poster_url})](#{canonical_url})"
      parts << "*Watch the full video demo on [3cucharadas.cl](#{canonical_url}).*"
    end
    parts << caption if caption
    parts.join("\n\n")
  end

    # `[^%]*` cortaba el tag en el primer porcentaje de sus argumentos, asi que un
    # `{% include gallery ... caption="... 95% CIs ..." %}` sobrevivia entero y
    # dev.to lo rechazaba con «422 Liquid#include tag is disabled». Medido el
    # 2026-09-05 sobre CASEN: la primera galeria se limpiaba y la segunda no, y la
    # comprobacion que hice para descartarlo tenia el mismo fallo que el codigo.
  sanitized = sanitized.gsub(/\{%-?\s*include\s+([^\s%]+).*?-?%\}/m) do
    warnings << Regexp.last_match(1)
    ""
  end

  sanitized = sanitized.gsub(KRAMDOWN_IAL, "\n")
  sanitized = sanitized.gsub(RELATIVE_ASSET_ATTR) { "#{Regexp.last_match(1)}=\"#{site_url}#{Regexp.last_match(2)}\"" }

  [sanitized, warnings.uniq]
end

# Dias desde la publicacion dentro de los cuales un post puede CREARSE en dev.to
# sin intervencion explicita. Mas alla, hace falta --backlog.
VENTANA_SINDICACION_DIAS = Integer(ENV.fetch("DEVTO_VENTANA_DIAS", "21"))
# Segundos entre escrituras (crear o actualizar). Medido el 2026-09-05: cuatro creaciones seguidas
# dieron 429 en tres de ellas.
PAUSA_ESCRITURA = Integer(ENV.fetch("DEVTO_PAUSA_ESCRITURA", "35"))
BACKLOG = ARGV.include?("--backlog") || ENV["DEVTO_BACKLOG"] == "1"

def slug_from_permalink(permalink)
  permalink.to_s.chomp("/").split("/").last
end

eligible = Dir.glob(File.join(posts_dir, "*-en.md")).filter_map do |path|
  front, body = parse_front_matter(path)
  # Contrato unico de sindicacion: `distribution.republish`. Es el mismo que ya
  # gobiernan el feed (_plugins/julia_feed.rb:60) y el catalogo de destinos.
  # Antes esta ruta usaba `sindicar` + `valor_seo`, un segundo vocabulario que
  # nadie cruzaba con el primero: un post podia salir en el feed y no por la API,
  # o quedar fuera de los dos sin que nada avisara. Paso exactamente eso con los
  # posts II y III de la serie multiagente.
  # `sindicar` se acepta como alias en desuso para no romper los posts que ya lo
  # declaran; no se exige, y `valor_seo` deja de decidir nada.
  republish = Array(front.dig("distribution", "republish")).map { |t| t.to_s.downcase }
  next unless republish.include?("dev") || front["sindicar"] == true
  next unless front["permalink"]

  # Compuerta de rezago. Unificar el contrato dejo elegibles a posts que llevaban
  # meses declarando `republish: [dev]` sin haber pasado nunca por la API: al
  # medirlo, `casen2024` (marzo) y `avaluo` (julio) aparecieron como "crearia".
  # Sindicarlos hoy los publicaria con fecha de hoy y competirian con lo reciente.
  # Se crean solo los posts dentro de la ventana; los viejos exigen --backlog,
  # que es un acto deliberado. Actualizar un articulo YA existente no se frena:
  # eso mantiene sincronizado lo que ya vive en dev.to.
  fecha_post = begin
    Date.parse(front["date"].to_s)
  rescue ArgumentError, TypeError
    nil
  end
  antiguedad = fecha_post ? (Date.today - fecha_post).to_i : nil
  rezagado = antiguedad && antiguedad > VENTANA_SINDICACION_DIAS

  url_canonica = "https://3cucharadas.cl/en#{front['permalink']}"
  youtube_id = youtube_id_from_url(front["devto_video_url"])
  sanitized_body, unhandled_includes = sanitize_body_for_devto(body, "https://3cucharadas.cl", url_canonica, youtube_id: youtube_id)
  unless unhandled_includes.empty?
    warn "#{File.basename(path)}: include(s) sin manejar, eliminados del cuerpo enviado a dev.to: #{unhandled_includes.join(', ')}"
  end

  og_image = front.dig("header", "og_image")

  {
    rezagado: rezagado,
    antiguedad: antiguedad,
    slug: slug_from_permalink(front["permalink"]),
    ref_interno: front["ref"] || slug_from_permalink(front["permalink"]),
    url_canonica: url_canonica,
    titulo_usado: front.fetch("title"),
    body_markdown: sanitized_body,
    description: front["description"],
    cover_image: og_image ? "https://3cucharadas.cl#{og_image}" : nil,
    tags: (front["devto_tags"] || front["tags"] || []).first(4).map { |t| t.to_s.downcase.gsub(/[^a-z0-9]/, "") }.reject(&:empty?)
  }
end

if eligible.empty?
  puts "Ningun post declara `distribution.republish: [dev]`. Nada que hacer."
  exit 0
end

def devto_request(api_key, method, path, payload = nil)
  uri = URI("https://dev.to/api#{path}")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  request = method.new(uri)
  request["api-key"] = api_key
  request["content-type"] = "application/json"
  request.body = payload.to_json if payload
  response = http.request(request)
  body = begin
    JSON.parse(response.body)
  rescue JSON::ParserError, TypeError
    {}
  end
  [response.code.to_i, body]
end

# Psych no preserva comentarios en un round-trip load -> to_yaml, y este script
# reescribe el fichero entero. Ya se llevo por delante tres lineas que explicaban
# por que el Post II tenia publicaciones registradas a mano (c9dcdac7). El dato
# sobrevivia; la razon no, y sin la razon nadie sabe si esas URLs son verificadas.
#
# Cada bloque de comentarios se ancla a la primera linea no vacia que lo sigue, y
# se reinserta despues del volcado. Si el ancla desaparecio, el comentario no se
# inventa un sitio: se avisa por stderr y se pierde de forma visible.
def capturar_comentarios(path)
  return [] unless File.file?(path)

  bloques = []
  actual = []
  File.readlines(path, chomp: true).each do |linea|
    if linea.strip.start_with?("#")
      actual << linea
    elsif actual.any?
      bloques << { comentario: actual, ancla: linea } unless linea.strip.empty?
      actual = [] unless linea.strip.empty?
    end
  end
  bloques
end

def restaurar_comentarios(texto, bloques)
  return texto if bloques.empty?

  lineas = texto.split("\n", -1)
  bloques.reverse_each do |bloque|
    indice = lineas.index(bloque[:ancla])
    if indice.nil?
      warn "comentario perdido: su ancla ya no existe -> #{bloque[:ancla].strip}"
      next
    end
    lineas.insert(indice, *bloque[:comentario])
  end
  lineas.join("\n")
end

comentarios = capturar_comentarios(distribucion_path)
entries = File.file?(distribucion_path) ? (YAML.safe_load_file(distribucion_path, permitted_classes: [Date, Time]) || []) : []
changed = false
fallos = []
llamadas = 0

eligible.each do |post|
  entry = entries.find { |e| e["slug"] == post[:slug] }
  unless entry
    entry = {
      "slug" => post[:slug],
      "ref_interno" => post[:ref_interno],
      "url_canonica" => post[:url_canonica],
      "titulo_usado" => post[:titulo_usado],
      "publicaciones" => []
    }
    entries << entry
  end
  entry["publicaciones"] ||= []
  devto_pub = entry["publicaciones"].find { |p| p["plataforma"] == "devto" }

  existente = devto_pub && devto_pub["devto_article_id"]

  # `published` viaja SOLO al crear. Enviarlo en el PUT despublicaba el articulo
  # en cada corrida: como el workflow se dispara con cualquier push de un
  # `-en.md`, un articulo ya publicado en dev.to volvia a borrador sin que nadie
  # lo pidiera. Quedo registrado en 021fb543, que revirtio una correccion manual.
  # Quien decide publicar en dev.to es la persona, alli; este script no opina.
  article = {
    title: post[:titulo_usado],
    body_markdown: post[:body_markdown],
    canonical_url: post[:url_canonica],
    description: post[:description],
    main_image: post[:cover_image],
    tags: post[:tags]
  }
  article[:published] = false unless existente
  payload = { article: article.compact }

  # Un post rezagado no se CREA sin --backlog; si ya existe, sí se actualiza.
  if post[:rezagado] && !existente && !BACKLOG
    puts "#{post[:slug]}: omitido, #{post[:antiguedad]} dias desde su publicacion (ventana: #{VENTANA_SINDICACION_DIAS}). Use --backlog para crearlo igual."
    next
  end

  if dry_run
    action = existente ? "actualizaría" : "crearía"
    # El tamano del cuerpo va en la linea porque «actualizaria» no distingue un
    # articulo completo de uno vacio, y un borrador que llega vacio a dev.to se ve
    # igual de «OK» en el log del workflow que uno correcto.
    puts "[dry-run] #{post[:slug]}: #{action} borrador en dev.to " \
         "(#{post[:body_markdown].length} car de cuerpo, #{post[:url_canonica]})"
    next
  end

  if existente
    sleep(PAUSA_ESCRITURA) unless llamadas.zero?
    llamadas += 1
    code, body = devto_request(api_key, Net::HTTP::Put, "/articles/#{devto_pub['devto_article_id']}", payload)
  else
    # dev.to limita las escrituras, creacion y actualizacion por igual: el
    # 2026-09-05 se midieron 429 tambien en updates, no solo al crear. Con
    # `--backlog` se crean varios seguidos. El 2026-09-05 tres de cuatro
    # creaciones murieron con 429 en la misma corrida, y el workflow lo reporto
    # como `success`. Se espacian; la primera no espera.
    sleep(PAUSA_ESCRITURA) unless llamadas.zero?
    llamadas += 1
    code, body = devto_request(api_key, Net::HTTP::Post, "/articles", payload)
  end

  ok = code.between?(200, 299)
  detalle = ok ? "OK" : "FALLÓ (#{code}#{body.is_a?(Hash) && body['error'] ? ": #{body['error']}" : ''})"
  puts "#{post[:slug]}: #{devto_pub ? 'actualización' : 'creación'} dev.to #{detalle}"
  unless ok
    fallos << "#{post[:slug]}: #{code}#{body.is_a?(Hash) && body['error'] ? " #{body['error']}" : ''}"
    next
  end

  devto_pub ||= { "plataforma" => "devto" }
  devto_pub["fecha"] ||= Date.today.to_s
  devto_pub["devto_article_id"] = body["id"]
  devto_pub["url_publicada"] = body["url"]
  # `||=`, no `=`: si alguien marco el articulo como publicado, esta corrida no
  # tiene forma de saberlo mejor que quien lo marco.
  devto_pub["estado"] ||= "borrador"
  entry["publicaciones"] << devto_pub unless entry["publicaciones"].include?(devto_pub)
  changed = true
end

if dry_run
  puts "[dry-run] #{eligible.length} post(s) elegibles, ninguna llamada real realizada."
else
  File.write(distribucion_path, restaurar_comentarios(entries.to_yaml, comentarios)) if changed
  puts "Listo. #{eligible.length} post(s) elegibles procesados."
end

# Salir 0 con creaciones caidas es lo que dejo el workflow en verde mientras tres
# de cuatro articulos no se creaban. Un fallo que no interrumpe a nadie no es un
# fallo detectado.
unless fallos.empty?
  warn "\nFallaron #{fallos.length} llamada(s) a dev.to:"
  fallos.each { |f| warn "  - #{f}" }
  exit 1
end
