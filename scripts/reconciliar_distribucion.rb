#!/usr/bin/env ruby
# frozen_string_literal: true

# Puente entre el ledger del CLI de difusion y `_data/distribucion.yml`.
#
# POR QUE EXISTE
#
# `verify_distribution_done.rb` exige, para dar un canal por cumplido, una URL
# publicada en `_data/distribucion.yml`. Y el CLI de difusion NO escribe ese
# fichero: deja su rastro en `difusion/state/ledger.jsonl`, que esta gitignorado.
# El circuito no cerraba solo. La consecuencia esta escrita en el propio YAML,
# en un comentario del 2026-08-31: la entrada de CASEN llevaba `publicaciones: []`
# desde julio pese a que el ledger registraba las dos redes desde el 24 de julio.
# Alguien lo reconcilio a mano, una vez, y el problema volvio.
#
# El ledger si tiene lo que hace falta: cada `network_published` trae `root_url`.
#
# QUE NO HACE
#
# No escribe por su cuenta en modo normal. `--check` compara y sale 1 si hay
# publicaciones en el ledger que el YAML no refleja; `--aplicar` las inserta.
#
# La insercion es TEXTUAL, no un round-trip de YAML. `_data/distribucion.yml`
# lleva comentarios que explican reconciliaciones pasadas --justamente la de
# agosto-- y un `YAML.dump` los borraria en silencio: el fichero quedaria
# formalmente igual y habria perdido la unica constancia de por que esa entrada
# se toco a mano.
#
# Uso:
#   ruby scripts/reconciliar_distribucion.rb --check
#   ruby scripts/reconciliar_distribucion.rb --aplicar

require "json"
require "yaml"
require "date"

ROOT = File.expand_path("..", __dir__)
YML = File.join(ROOT, "_data", "distribucion.yml")
LEDGER = File.join(ROOT, "difusion", "state", "ledger.jsonl")
APLICAR = ARGV.include?("--aplicar")

unless File.file?(LEDGER)
  # Sin ledger no se puede afirmar nada: en CI el fichero no existe por estar
  # gitignorado. Salir 0 aqui no es aprobar en vacio, porque quien decide sobre
  # lo publicado es verify_distribution_done.rb, no este puente.
  puts "SKIP: no hay #{LEDGER.sub("#{ROOT}/", '')} (esperado en CI, gitignorado)."
  exit 0
end

registro = begin
  YAML.safe_load_file(YML, permitted_classes: [Date, Time]) || []
rescue Psych::SyntaxError => e
  # Un YAML roto tiene que decir que esta roto, no vomitar una traza de Psych:
  # la traza manda a leer psych.rb y el problema esta en el fichero de datos.
  abort "No se pudo leer #{YML.sub("#{ROOT}/", '')}: #{e.message}"
end
por_ref = registro.to_h { |e| [e["ref_interno"].to_s, e] }
por_slug = registro.to_h { |e| [e["slug"].to_s, e] }

publicados = []
File.foreach(LEDGER) do |linea|
  fila = begin
    JSON.parse(linea)
  rescue JSON::ParserError
    next
  end
  next unless fila["event"] == "network_published"

  resultado = fila["result"] || {}
  url = resultado["root_url"].to_s
  next if url.empty?

  publicados << {
    ref: fila["ref"].to_s,
    red: fila["network"].to_s,
    url: url,
    reply_url: resultado["reply_url"].to_s,
    fecha: Date.parse(fila["timestamp"].to_s).to_s
  }
end

faltan = publicados.reject do |p|
  entrada = por_ref[p[:ref]] || por_slug[p[:ref]]
  next false if entrada.nil? # sin entrada no se puede insertar; se reporta aparte

  Array(entrada["publicaciones"]).any? { |x| x.is_a?(Hash) && x["url_publicada"].to_s == p[:url] }
end

sin_entrada = faltan.select { |p| por_ref[p[:ref]].nil? && por_slug[p[:ref]].nil? }
insertables = faltan - sin_entrada

sin_entrada.each do |p|
  warn "- #{p[:ref]}/#{p[:red]}: publicado el #{p[:fecha]} y no hay entrada con ese `slug` ni `ref_interno` en _data/distribucion.yml"
end

avisos_en_previo = publicados.reject { |p| p[:reply_url].empty? }.reject do |p|
  entrada = por_ref[p[:ref]] || por_slug[p[:ref]]
  entrada && Array(entrada["publicaciones"]).any? do |x|
    x.is_a?(Hash) && x["url_publicada"].to_s == p[:url] && x["url_publicada_en"].to_s != ""
  end
end

if insertables.empty? && sin_entrada.empty?
  avisos_en_previo.each do |p|
    warn "- aviso: #{p[:ref]}/#{p[:red]} tiene respuestas en el hilo y la entrada no declara `url_publicada_en` " \
         "(ultima respuesta: #{p[:reply_url]}); el ledger no dice de que idioma es cada post"
  end
  puts "Reconciliacion OK: #{publicados.length} publicacion(es) en el ledger, todas reflejadas en " \
       "_data/distribucion.yml#{avisos_en_previo.empty? ? '' : ", #{avisos_en_previo.length} aviso(s)"}."
  exit 0
end

insertables.each do |p|
  warn "- #{p[:ref]}/#{p[:red]}: publicado el #{p[:fecha]} y ausente de _data/distribucion.yml (#{p[:url]})"
end

# `url_publicada_en` NO se rellena sola, y no es un olvido.
#
# El ledger guarda `root_url` y `reply_url`, y nada mas: el `result` no dice de
# que idioma es cada post del hilo. En el hilo del post II --raiz ES, respuesta
# EN-- `reply_url` era efectivamente la version inglesa, y por eso la tentacion
# de mapearlos. Pero el hilo del post III lleva cuatro posts en Bluesky (raiz ES,
# respuesta ES, raiz EN, respuesta EN) y ahi `reply_url` es la ULTIMA respuesta,
# que no es la raiz inglesa. Escribir esa URL como `url_publicada_en` seria
# meter un dato falso en el registro que el gate usa como prueba.
#
# Se avisa y se deja a un humano.
avisos_en = publicados.reject { |p| p[:reply_url].empty? }.reject do |p|
  entrada = por_ref[p[:ref]] || por_slug[p[:ref]]
  entrada && Array(entrada["publicaciones"]).any? do |x|
    x.is_a?(Hash) && x["url_publicada"].to_s == p[:url] && x["url_publicada_en"].to_s != ""
  end
end
avisos_en.each do |p|
  warn "- aviso: #{p[:ref]}/#{p[:red]} tiene respuestas en el hilo y la entrada no declara `url_publicada_en`. " \
       "El ledger no dice de que idioma es cada post: completalo a mano (ultima respuesta: #{p[:reply_url]})"
end

unless APLICAR
  warn ""
  warn "Correr con --aplicar para insertarlas."
  abort "Reconciliacion pendiente (#{insertables.length + sin_entrada.length} publicacion(es))"
end

abort "Hay publicaciones sin entrada: creala a mano antes de --aplicar" unless sin_entrada.empty?

lineas = File.readlines(YML)
insertables.group_by { |p| (por_ref[p[:ref]] || por_slug[p[:ref]])["slug"] }.each do |slug, grupo|
  # Se ancla en la linea `publicaciones:` de ESE slug, no en la primera del
  # fichero: buscar la clave suelta insertaria todo en la primera entrada.
  i_slug = lineas.index { |l| l.start_with?("- slug: #{slug}") }
  raise "No se encontro el bloque de #{slug}" if i_slug.nil?

  i_pub = (i_slug...lineas.length).find do |i|
    lineas[i].start_with?("  publicaciones:") || (i > i_slug && lineas[i].start_with?("- slug: "))
  end
  raise "No se encontro `publicaciones:` dentro de #{slug}" if i_pub.nil? || lineas[i_pub].start_with?("- slug: ")

  bloque = grupo.flat_map do |p|
    ["  - plataforma: #{p[:red]}\n",
     "    fecha: #{p[:fecha]}\n",
     "    url_publicada: #{p[:url]}\n",
     "    resultado_30d:\n"]
  end
  # `publicaciones: []` es una lista vacia en linea; hay que abrirla antes de
  # colgarle elementos, o el YAML resultante no parsea.
  lineas[i_pub] = "  publicaciones:\n" if lineas[i_pub].strip == "publicaciones: []"
  lineas.insert(i_pub + 1, *bloque)
end

File.write(YML, lineas.join)
YAML.safe_load_file(YML, permitted_classes: [Date, Time]) # revienta si quedo mal formado
puts "Reconciliadas #{insertables.length} publicacion(es) en _data/distribucion.yml."
