#!/usr/bin/env ruby
# frozen_string_literal: true

# Sindicación automatizada a dev.to para posts EN que declaran
# `distribution.republish: [dev]`; `sindicar: true` se acepta solo como alias
# heredado. Los artículos nuevos se crean como borrador. Los ya registrados se
# actualizan sin enviar `published` como atributo JSON y con el estado remoto
# reflejado en el front matter, por lo que conservan ese estado.
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
require "fileutils"
require "optparse"
require_relative "jekyll_to_devto"
require_relative "lib/devto_draft_policy"

options = {
  backlog: ENV["DEVTO_BACKLOG"] == "1",
  dry_run: ENV["DEVTO_DRY_RUN"] == "1",
  existing_drafts_only: ENV["DEVTO_EXISTING_DRAFTS_ONLY"] == "1",
  export_dir: nil
}
OptionParser.new do |parser|
  parser.banner = "Uso: ruby scripts/syndicate_devto.rb [opciones]"
  parser.on("--backlog", "Permite crear borradores fuera de la ventana") { options[:backlog] = true }
  parser.on("--dry-run", "Simula sin escribir ni llamar a DEV.to") { options[:dry_run] = true }
  parser.on("--existing-drafts-only", "Actualiza borradores remotos existentes; no crea ni toca publicados") do
    options[:existing_drafts_only] = true
  end
  parser.on("--export-dir DIR", "Exporta el Markdown DEV.to derivado y termina") do |dir|
    options[:export_dir] = dir
  end
end.parse!

unless ARGV.empty?
  warn "Argumentos no reconocidos: #{ARGV.join(' ')}"
  exit 2
end

api_key = ENV["DEV_TO_API_KEY"]
site_root = File.expand_path("..", __dir__)
posts_dir = File.join(site_root, "_posts")
distribucion_path = File.join(site_root, "_data", "distribucion.yml")
dry_run = options[:dry_run]

def parse_front_matter(path)
  text = File.read(path)
  return [{}, ""] unless text.start_with?("---\n")

  parts = text.split(/^---\s*$/, 3)
  return [{}, text] if parts.length < 3

  [YAML.safe_load(parts[1], permitted_classes: [Date, Time]) || {}, parts[2].strip]
end

# Dias desde la publicacion dentro de los cuales un post puede CREARSE en dev.to
# sin intervencion explicita. Mas alla, hace falta --backlog.
VENTANA_SINDICACION_DIAS = Integer(ENV.fetch("DEVTO_VENTANA_DIAS", "21"))
# Segundos entre escrituras (crear o actualizar). Medido el 2026-09-05: cuatro creaciones seguidas
# dieron 429 en tres de ellas.
PAUSA_ESCRITURA = Integer(ENV.fetch("DEVTO_PAUSA_ESCRITURA", "35"))
backlog = options[:backlog]

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
  og_image = front.dig("header", "og_image")
  cover_image = og_image ? JekyllToDevto.absolute_url(og_image, JekyllToDevto::SITE_URL, force_relative: true) : nil
  tags = (front["devto_tags"] || front["tags"] || []).first(4).map do |tag|
    tag.to_s.downcase.gsub(/[^a-z0-9]/, "")
  end.reject(&:empty?)
  transformed = JekyllToDevto.transform(
    body,
    canonical_url: url_canonica,
    page: front,
    youtube_id: JekyllToDevto.youtube_id_from_url(front["devto_video_url"])
  )
  transformed.warnings.each { |warning| warn "#{File.basename(path)}: #{warning}" }
  ai_disclosure_level = AiDisclosure.resolve(front).fetch("level")
  devto_document = JekyllToDevto.render_document(
    body: transformed.body,
    title: front.fetch("title"),
    description: front["description"],
    tags: tags,
    canonical_url: url_canonica,
    cover_image: cover_image,
    published: false,
    ai_disclosure_level: ai_disclosure_level
  )

  {
    rezagado: rezagado,
    antiguedad: antiguedad,
    slug: slug_from_permalink(front["permalink"]),
    ref_interno: front["ref"] || slug_from_permalink(front["permalink"]),
    url_canonica: url_canonica,
    titulo_usado: front.fetch("title"),
    body_markdown: devto_document,
    transformed_body: transformed.body,
    description: front["description"],
    cover_image: cover_image,
    tags: tags,
    ai_disclosure_level: ai_disclosure_level
  }
end

if eligible.empty?
  puts "Ningun post declara `distribution.republish: [dev]`. Nada que hacer."
  exit 0
end

if options[:export_dir]
  export_dir = File.expand_path(options[:export_dir])
  FileUtils.mkdir_p(export_dir)
  eligible.each do |post|
    File.write(File.join(export_dir, "#{post[:slug]}.md"), post[:body_markdown])
  end
  puts "Exportados #{eligible.length} borradores DEV.to reproducibles en #{export_dir}."
  exit 0
end

if !dry_run && (api_key.nil? || api_key.strip.empty?)
  puts "DEV_TO_API_KEY no configurado; nada que sindicar."
  exit(options[:existing_drafts_only] ? 2 : 0)
end

if dry_run && options[:existing_drafts_only]
  warn "NO_CONCLUYENTE: dry-run no consulta DEV; no permite afirmar qué borradores existen. Use --export-dir para revisar contenido sin API."
  exit 2
end

def devto_request(api_key, method, path, payload = nil)
  uri = URI("https://dev.to/api#{path}")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  http.open_timeout = 10
  http.read_timeout = 30
  request = method.new(uri)
  request["api-key"] = api_key
  request["accept"] = "application/vnd.forem.api-v1+json"
  request["user-agent"] = "3cucharadas-devto-syndication/1.0"
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

def devto_remote_articles(api_key)
  %w[published unpublished].flat_map do |state|
    code, body = devto_request(
      api_key,
      Net::HTTP::Get,
      "/articles/me/#{state}?per_page=1000"
    )
    unless code.between?(200, 299) && body.is_a?(Array) && body.length < 1000
      error = body.is_a?(Hash) ? body["error"] : nil
      raise JekyllToDevto::TransformError,
            "no se pudo leer el estado remoto DEV.to (#{state}: #{code}#{error ? ": #{error}" : ''})"
    end

    body.map { |article| article.merge("published" => state == "published") }
  end
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
remote_articles = if dry_run
                    []
                  else
                    begin
                      devto_remote_articles(api_key)
                    rescue JekyllToDevto::TransformError => e
                      warn e.message
                      exit 1
                    end
                  end
remote_by_id = remote_articles.to_h { |article| [article.fetch("id").to_i, article] }
remote_by_canonical = remote_articles.group_by { |article| article["canonical_url"] }
remote_drafts_by_canonical = remote_articles.reject { |article| article["published"] }
                                           .group_by { |article| article["canonical_url"] }
if options[:existing_drafts_only]
  begin
    # Preflight the whole inventory before the first write; never partially
    # update an ambiguous set or mistake an empty inventory for success.
    selected = eligible.flat_map { |post| DevtoDraftPolicy.select(remote_articles, post[:url_canonica]) }
    if selected.empty?
      # An authenticated, complete published inventory is a verified no-op,
      # not a successful empty lookup. Preserve fail-closed behavior for any
      # missing, duplicate, malformed or unknown-state canonical.
      all_published = eligible.all? do |post|
        matches = remote_articles.select { |article| article['canonical_url'] == post[:url_canonica] }
        matches.one? && matches.first['published'] == true &&
          matches.first['id'].is_a?(Integer) && matches.first['id'].positive?
      end
      raise DevtoDraftPolicy::Violation, 'no drafts and incomplete published inventory' unless all_published

      puts "NO_OP: #{eligible.length} canonical(es) verificados publicados; 0 borradores, 0 escrituras"
      exit 0
    end
    backup_dir = ENV.fetch("DEVTO_BACKUP_DIR") { raise DevtoDraftPolicy::Violation, 'DEVTO_BACKUP_DIR required for maintenance' }
    DevtoDraftPolicy.backup!(selected, backup_dir, api_key)
    puts "Custodia cifrada: #{selected.length} borrador(es); ids #{selected.map { |a| a.fetch('id') }.join(', ')}"
  rescue DevtoDraftPolicy::Violation, SystemCallError => e
    warn e.message
    exit 1
  end
end
halt_writes = false

eligible.each do |post|
  break if halt_writes
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

  if dry_run
    action = existente ? "actualizaría" : "crearía"
    # El tamano del cuerpo va en la linea porque «actualizaria» no distingue un
    # articulo completo de uno vacio, y un borrador que llega vacio a dev.to se ve
    # igual de «OK» en el log del workflow que uno correcto.
    puts "[dry-run] #{post[:slug]}: #{action} borrador en dev.to " \
         "(#{post[:body_markdown].length} car de cuerpo, #{post[:url_canonica]})"
    next
  end

  targets = if options[:existing_drafts_only]
              remote_drafts_by_canonical.fetch(post[:url_canonica], [])
            elsif existente
              remote = remote_by_id[existente.to_i]
              if remote.nil?
                fallos << "#{post[:slug]}: id registrado #{existente} no existe en la cuenta DEV.to"
                []
              else
                [remote]
              end
            elsif remote_by_canonical.key?(post[:url_canonica])
              matches = remote_by_canonical.fetch(post[:url_canonica])
              if matches.one?
                [matches.first]
              else
                ids = matches.map { |article| article.fetch("id") }.join(", ")
                fallos << "#{post[:slug]}: canonical duplicado en DEV.to (ids: #{ids})"
                []
              end
            else
              [nil]
            end

  if options[:existing_drafts_only] && targets.empty?
    puts "#{post[:slug]}: omitido, no tiene borrador remoto existente."
    next
  end

  # Un post rezagado no se CREA sin --backlog; si ya existe, sí se actualiza.
  if post[:rezagado] && targets == [nil] && !backlog
    puts "#{post[:slug]}: omitido, #{post[:antiguedad]} dias desde su publicacion (ventana: #{VENTANA_SINDICACION_DIAS}). Use --backlog para crearlo igual."
    next
  end

  targets.each do |target|
    target_id = target && target.fetch("id").to_i
    published = target ? target.fetch("published") : false
    devto_document = JekyllToDevto.render_document(
      body: post[:transformed_body],
      title: post[:titulo_usado],
      description: post[:description],
      tags: post[:tags],
      canonical_url: post[:url_canonica],
      cover_image: post[:cover_image],
      published: published,
      ai_disclosure_level: post[:ai_disclosure_level]
    )

    # `published` viaja como atributo JSON solo al crear. En un PUT, el front
    # matter refleja el estado leído en la misma corrida y el atributo se omite:
    # la actualización no puede decidir publicar ni despublicar por su cuenta.
    article = {
      title: post[:titulo_usado],
      body_markdown: devto_document,
      canonical_url: post[:url_canonica],
      description: post[:description],
      main_image: post[:cover_image],
      tags: post[:tags],
      ai_disclosure_level: post[:ai_disclosure_level]
    }
    article[:published] = false unless target
    payload = { article: article.compact }

    if options[:existing_drafts_only] && target && target['body_markdown'] == devto_document && target['title'] == post[:titulo_usado]
      puts "#{post[:slug]}: borrador ##{target_id} ya coincide; sin PUT."
      next
    end

    sleep(PAUSA_ESCRITURA) unless llamadas.zero?
    llamadas += 1
    if options[:existing_drafts_only]
      begin
        code, body = DevtoDraftPolicy.update!(
          target, current: devto_remote_articles(api_key), payload: payload,
          writer: ->(id, guarded_payload) { devto_request(api_key, Net::HTTP::Put, "/articles/#{id}", guarded_payload) }
        )
      rescue DevtoDraftPolicy::Violation, JekyllToDevto::TransformError, Timeout::Error, IOError, SystemCallError => e
        fallos << "#{post[:slug]}: #{e.message}"
        halt_writes = true
        break
      end
    elsif target
      code, body = devto_request(api_key, Net::HTTP::Put, "/articles/#{target_id}", payload)
    else
      # DEV limita creaciones y actualizaciones por igual; la pausa se aplica a
      # toda escritura para que un 429 sea fallo visible y no pérdida silenciosa.
      code, body = devto_request(api_key, Net::HTTP::Post, "/articles", payload)
    end

    ok = code.between?(200, 299)
    detalle = ok ? "OK" : "FALLÓ (#{code}#{body.is_a?(Hash) && body['error'] ? ": #{body['error']}" : ''})"
    puts "#{post[:slug]}: #{target ? "actualización ##{target_id}" : 'creación'} dev.to #{detalle}"
    unless ok
      fallos << "#{post[:slug]}: #{code}#{body.is_a?(Hash) && body['error'] ? " #{body['error']}" : ''}"
      halt_writes = true if code == 429
      next
    end

    # Un duplicado remoto se actualiza para retirar contenido viejo, pero no
    # reemplaza la identidad que ya gobierna _data/distribucion.yml.
    if !target || existente.nil? || target_id == existente.to_i
      devto_pub ||= { "plataforma" => "devto" }
      devto_pub["fecha"] ||= Date.today.to_s
      devto_pub["devto_article_id"] = body["id"]
      devto_pub["url_publicada"] = body["url"]
      devto_pub["estado"] = published ? "publicado" : "borrador"
      entry["publicaciones"] << devto_pub unless entry["publicaciones"].include?(devto_pub)
      changed = true
    end
  end
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
