#!/usr/bin/env ruby
# frozen_string_literal: true

# Fase 4.3 (archivo/handoffs/difusion/HANDOFF-2026-07-25-distribucion-3cucharadas.md):
# sindicación automatizada a dev.to, solo para posts marcados `sindicar: true`
# con `valor_seo: bajo|medio` en el front matter EN. Publica siempre como
# borrador (published: false) — nunca lo hace público. Guarda el id remoto
# en _data/distribucion.yml (mismo esquema que usa Fase 3, reutilizado, no
# duplicado) para permitir actualizaciones y evitar duplicados.
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

  sanitized = sanitized.gsub(/\{%-?\s*include\s+([^\s%]+)[^%]*-?%\}/) do
    warnings << Regexp.last_match(1)
    ""
  end

  sanitized = sanitized.gsub(KRAMDOWN_IAL, "\n")
  sanitized = sanitized.gsub(RELATIVE_ASSET_ATTR) { "#{Regexp.last_match(1)}=\"#{site_url}#{Regexp.last_match(2)}\"" }

  [sanitized, warnings.uniq]
end

def slug_from_permalink(permalink)
  permalink.to_s.chomp("/").split("/").last
end

eligible = Dir.glob(File.join(posts_dir, "*-en.md")).filter_map do |path|
  front, body = parse_front_matter(path)
  next unless front["sindicar"] == true
  next unless %w[bajo medio].include?(front["valor_seo"])
  next unless front["permalink"]

  url_canonica = "https://3cucharadas.cl/en#{front['permalink']}"
  youtube_id = youtube_id_from_url(front["devto_video_url"])
  sanitized_body, unhandled_includes = sanitize_body_for_devto(body, "https://3cucharadas.cl", url_canonica, youtube_id: youtube_id)
  unless unhandled_includes.empty?
    warn "#{File.basename(path)}: include(s) sin manejar, eliminados del cuerpo enviado a dev.to: #{unhandled_includes.join(', ')}"
  end

  og_image = front.dig("header", "og_image")

  {
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
  puts "Sin posts marcados sindicar:true + valor_seo:bajo|medio. Nada que hacer."
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

entries = File.file?(distribucion_path) ? (YAML.safe_load_file(distribucion_path, permitted_classes: [Date, Time]) || []) : []
changed = false

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

  payload = {
    article: {
      title: post[:titulo_usado],
      body_markdown: post[:body_markdown],
      published: false,
      canonical_url: post[:url_canonica],
      description: post[:description],
      main_image: post[:cover_image],
      tags: post[:tags]
    }.compact
  }

  if dry_run
    action = devto_pub && devto_pub["devto_article_id"] ? "actualizaría" : "crearía"
    puts "[dry-run] #{post[:slug]}: #{action} borrador en dev.to (#{post[:url_canonica]})"
    next
  end

  if devto_pub && devto_pub["devto_article_id"]
    code, body = devto_request(api_key, Net::HTTP::Put, "/articles/#{devto_pub['devto_article_id']}", payload)
  else
    code, body = devto_request(api_key, Net::HTTP::Post, "/articles", payload)
  end

  ok = code.between?(200, 299)
  puts "#{post[:slug]}: #{devto_pub ? 'actualización' : 'creación'} dev.to #{ok ? 'OK' : "FALLÓ (#{code})"}"
  next unless ok

  devto_pub ||= { "plataforma" => "devto" }
  devto_pub["fecha"] ||= Date.today.to_s
  devto_pub["devto_article_id"] = body["id"]
  devto_pub["url_publicada"] = body["url"]
  devto_pub["estado"] = "borrador"
  entry["publicaciones"] << devto_pub unless entry["publicaciones"].include?(devto_pub)
  changed = true
end

if dry_run
  puts "[dry-run] #{eligible.length} post(s) elegibles, ninguna llamada real realizada."
else
  File.write(distribucion_path, entries.to_yaml) if changed
  puts "Listo. #{eligible.length} post(s) elegibles procesados."
end
