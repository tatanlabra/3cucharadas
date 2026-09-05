#!/usr/bin/env ruby
# frozen_string_literal: true

# Productor del campo `resultado_30d` de `_data/distribucion.yml`.
#
# POR QUE EXISTE
#
# El campo estaba en cada publicacion y SIEMPRE vacio. No era un dato pendiente
# de llegar: nadie lo escribia y nadie lo leia --buscado en todo el repositorio el
# 2026-09-05, solo aparecia aqui y en `docs/distribucion.md`, que lo describe--.
# Un campo asi miente por omision el dia que alguien lea el null como «no hubo
# alcance» en vez de «no se midio nunca».
#
# Se decidio darle productor en vez de retirarlo porque el dato es alcanzable:
# `reconciliar_distribucion.rb` ya deja `url_publicada` en el registro, y las dos
# redes exponen sus contadores publicos SIN autenticacion. Comprobado el
# 2026-09-05 contra las publicaciones reales:
#   GET mastodon.social/api/v1/statuses/<id>              -> favourites/reblogs/replies
#   GET public.api.bsky.app/xrpc/app.bsky.feed.getPosts   -> like/repost/reply/quote
# La de Bluesky exige el DID, no el handle: con el handle en la URI devuelve
# «Internal Server Error», que es por lo que hace falta resolverlo antes.
#
# QUE NO HACE, Y ES DELIBERADO
#
# - **No es un gate y no corre en CI.** Sale a la red, y una comprobacion que
#   gasta un servicio de terceros en cada corrida es justo lo que este workspace
#   ya pago una vez. Se invoca a mano o desde un timer.
# - **Solo consulta lo que cumplio 30 dias y aun no tiene medicion.** Una
#   publicacion de hoy no se toca; una ya medida tampoco. Sin `--forzar` no
#   repite una consulta.
# - **Solo Mastodon y Bluesky.** dev.to, Medium y LinkedIn no dan contadores
#   publicos sin autenticacion. Sus entradas quedan con el campo vacio y el
#   informe lo dice, en vez de rellenarlas con un cero que parece una medicion.
# - **Mide la raiz del hilo, no la respuesta.** El hilo es raiz ES + respuesta EN
#   (`networks.py`), y sumar las dos daria un numero que no corresponde a ninguna
#   audiencia. La URL de la respuesta queda en `url_publicada_en` para quien
#   quiera mirarla.
#
# La escritura es TEXTUAL, no un round-trip de YAML: el fichero lleva comentarios
# que explican reconciliaciones pasadas y `YAML.dump` los borraria en silencio.
#
# Uso:
#   ruby scripts/resultado_30d.rb --check     # que hay pendiente de medir
#   ruby scripts/resultado_30d.rb --aplicar   # consulta y escribe
#   ruby scripts/resultado_30d.rb --aplicar --forzar   # remide lo ya medido

require "date"
require "json"
require "net/http"
require "uri"
require "yaml"

ROOT = File.expand_path("..", __dir__)
YML = File.join(ROOT, "_data", "distribucion.yml")
APLICAR = ARGV.include?("--aplicar")
FORZAR = ARGV.include?("--forzar")
DIAS = 30
HOY = ENV["RESULTADO_30D_HOY"] ? Date.parse(ENV["RESULTADO_30D_HOY"]) : Date.today
MEDIBLES = %w[mastodon bluesky].freeze

def http_json(url)
  res = Net::HTTP.get_response(URI(url))
  return nil unless res.is_a?(Net::HTTPSuccess)

  JSON.parse(res.body)
rescue StandardError
  nil
end

def metricas_mastodon(url)
  # La URL publicada es https://<instancia>/@<usuario>/<id>; el id es el ultimo tramo.
  u = URI(url)
  id = u.path.split("/").last
  datos = http_json("https://#{u.host}/api/v1/statuses/#{id}")
  return nil unless datos

  { "favoritos" => datos["favourites_count"], "difusiones" => datos["reblogs_count"],
    "respuestas" => datos["replies_count"] }
end

def metricas_bluesky(url)
  # https://bsky.app/profile/<handle>/post/<rkey>. La AppView publica exige el DID.
  partes = URI(url).path.split("/")
  handle = partes[2]
  rkey = partes[4]
  return nil if handle.nil? || rkey.nil?

  did = http_json("https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=#{handle}")
  return nil unless did && did["did"]

  uri = "at://#{did['did']}/app.bsky.feed.post/#{rkey}"
  datos = http_json("https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?uris=#{URI.encode_www_form_component(uri)}")
  post = datos && datos["posts"] && datos["posts"].first
  return nil unless post

  { "favoritos" => post["likeCount"], "difusiones" => post["repostCount"],
    "respuestas" => post["replyCount"] }
end

registro = begin
  YAML.safe_load_file(YML, permitted_classes: [Date, Time]) || []
rescue Psych::SyntaxError => e
  abort "No se pudo leer #{YML.sub("#{ROOT}/", '')}: #{e.message}"
end

pendientes = []
no_medibles = []
inmaduras = []

registro.each do |entrada|
  Array(entrada["publicaciones"]).each do |pub|
    next unless pub.is_a?(Hash)

    plataforma = pub["plataforma"].to_s
    url = pub["url_publicada"].to_s
    fecha = begin
      Date.parse(pub["fecha"].to_s)
    rescue ArgumentError, TypeError
      nil
    end
    next if fecha.nil? || url.empty?

    dias = (HOY - fecha).to_i
    unless MEDIBLES.include?(plataforma)
      no_medibles << "#{entrada['slug']}/#{plataforma}"
      next
    end
    if dias < DIAS
      inmaduras << "#{entrada['slug']}/#{plataforma}: D#{dias} de D#{DIAS}"
      next
    end
    next if pub["resultado_30d"] && !FORZAR

    pendientes << { slug: entrada["slug"], red: plataforma, url: url, dias: dias }
  end
end

inmaduras.each { |i| puts "- aun no cumple 30 dias: #{i}" }
no_medibles.uniq.each { |n| puts "- sin contador publico sin autenticacion, queda vacio: #{n}" }

if pendientes.empty?
  puts "resultado_30d: nada que medir (#{inmaduras.length} inmadura(s), #{no_medibles.uniq.length} sin API publica)."
  exit 0
end

pendientes.each { |p| puts "- por medir: #{p[:slug]}/#{p[:red]} (D#{p[:dias]}) #{p[:url]}" }

unless APLICAR
  puts ""
  puts "Correr con --aplicar para consultar y escribir. Sale a la red: no es un gate."
  exit 0
end

lineas = File.readlines(YML)
escritas = 0
fallidas = []

pendientes.each do |p|
  m = p[:red] == "mastodon" ? metricas_mastodon(p[:url]) : metricas_bluesky(p[:url])
  if m.nil?
    fallidas << "#{p[:slug]}/#{p[:red]}: la API no respondio o cambio de forma"
    next
  end

  # Se ancla en la linea de la URL, que es unica en el fichero, y se reescribe el
  # `resultado_30d:` que la sigue dentro de su mismo bloque de publicacion.
  i_url = lineas.index { |l| l.include?("url_publicada: #{p[:url]}") }
  if i_url.nil?
    fallidas << "#{p[:slug]}/#{p[:red]}: no se encontro su linea `url_publicada`"
    next
  end
  i_res = (i_url...[i_url + 6, lineas.length].min).find { |i| lineas[i].strip.start_with?("resultado_30d:") }
  if i_res.nil?
    fallidas << "#{p[:slug]}/#{p[:red]}: no hay `resultado_30d:` en su bloque"
    next
  end

  valor = "{favoritos: #{m['favoritos']}, difusiones: #{m['difusiones']}, " \
          "respuestas: #{m['respuestas']}, medido: #{HOY}, dias: #{p[:dias]}}"
  lineas[i_res] = "    resultado_30d: #{valor}\n"
  escritas += 1
  puts "  #{p[:slug]}/#{p[:red]}: #{valor}"
end

if escritas.positive?
  File.write(YML, lineas.join)
  YAML.safe_load_file(YML, permitted_classes: [Date, Time]) # revienta si quedo mal formado
end

fallidas.each { |f| warn "- #{f}" }
puts "resultado_30d: #{escritas} medicion(es) escrita(s), #{fallidas.length} fallida(s)."
exit(fallidas.empty? ? 0 : 1)
