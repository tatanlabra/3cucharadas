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
# El ledger NO vive en el repositorio, y darlo por hecho hacia inutil todo este
# script: apuntaba a `difusion/state/ledger.jsonl`, que quedo congelado el
# 2026-07-24 con 2 publicaciones, mientras el CLI escribia en
# `~/.local/state/3cucharadas-difusion/ledger.jsonl`, que tenia 8. La
# reconciliacion salia «OK, todas reflejadas» sin haber mirado nada. Se detecto
# el 2026-09-05 al publicar el post III: el gate no se entero de la publicacion.
#
# Misma resolucion que `storage.py:20 default_state_dir()`: la variable de entorno
# manda, si no el directorio de estado del usuario. El del repositorio queda como
# ultimo recurso porque es lo que existe en CI, donde el otro no esta.
LEDGER = [
  ENV["CUCHARADAS_DIFUSION_STATE_DIR"] && File.join(ENV["CUCHARADAS_DIFUSION_STATE_DIR"], "ledger.jsonl"),
  File.join(Dir.home, ".local", "state", "3cucharadas-difusion", "ledger.jsonl"),
  File.join(ROOT, "difusion", "state", "ledger.jsonl"),
].compact.find { |p| File.file?(p) } || File.join(ROOT, "difusion", "state", "ledger.jsonl")
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

if insertables.empty? && sin_entrada.empty?
  puts "Reconciliacion OK: #{publicados.length} publicacion(es) en el ledger, todas reflejadas en _data/distribucion.yml."
  exit 0
end

insertables.each do |p|
  warn "- #{p[:ref]}/#{p[:red]}: publicado el #{p[:fecha]} y ausente de _data/distribucion.yml (#{p[:url]})"
end

# `url_publicada_en` SI se rellena, y antes no.
#
# La primera version de este script se nego a mapear `reply_url` a
# `url_publicada_en` razonando que el ledger no dice de que idioma es cada post
# del hilo, y suponiendo que el hilo podia llevar cuatro entradas. Se comprobo el
# 2026-09-05 leyendo el publicador: `networks.py` emite exactamente dos por red,
# `<red>_es` para la raiz y `<red>_en` para la respuesta --lineas 169-192 en
# Mastodon y 381-403 en Bluesky--, y `base_copy` es por idioma, asi que no existe
# el hilo de cuatro que motivo la cautela. `reply_url` es la version inglesa
# siempre. Dejarlo en manos de un humano era pedir trabajo manual por una duda
# que el codigo ya resolvia.


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
    linea = ["  - plataforma: #{p[:red]}\n",
             "    fecha: #{p[:fecha]}\n",
             "    url_publicada: #{p[:url]}\n"]
    linea << "    url_publicada_en: #{p[:reply_url]}\n" unless p[:reply_url].empty?
    linea << "    resultado_30d:\n"
    linea
  end
  # `publicaciones: []` es una lista vacia en linea; hay que abrirla antes de
  # colgarle elementos, o el YAML resultante no parsea.
  lineas[i_pub] = "  publicaciones:\n" if lineas[i_pub].strip == "publicaciones: []"
  lineas.insert(i_pub + 1, *bloque)
end

File.write(YML, lineas.join)
YAML.safe_load_file(YML, permitted_classes: [Date, Time]) # revienta si quedo mal formado
puts "Reconciliadas #{insertables.length} publicacion(es) en _data/distribucion.yml."
