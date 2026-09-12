#!/usr/bin/env ruby
# frozen_string_literal: true

# Puente entre el ledger del CLI de difusion y `_data/distribucion.yml`.
#
# POR QUE EXISTE
#
# `verify_distribution_done.rb` exige, para dar un canal por cumplido, una URL
# publicada en `_data/distribucion.yml`. Y el CLI de difusion NO escribe ese
# fichero: deja su rastro en el ledger XDG del usuario, fuera del repositorio.
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
require "optparse"

options = {}
OptionParser.new do |o|
  o.on("--check") {}
  o.on("--aplicar") { options[:aplicar] = true }
  o.on("--ref REF") { |ref| options[:ref] = ref }
end.parse!

ROOT = File.expand_path(ENV.fetch("DISTRIBUCION_ROOT", File.expand_path("..", __dir__)))
YML = File.join(ROOT, "_data", "distribucion.yml")
# El ledger NO vive en el repositorio, y darlo por hecho hacia inutil todo este
# script: apuntaba a `difusion/state/ledger.jsonl`, que quedo congelado el
# 2026-07-24 con 2 publicaciones, mientras el CLI escribia en
# `~/.local/state/3cucharadas-difusion/ledger.jsonl`, que tenia 8. La
# reconciliacion salia «OK, todas reflejadas» sin haber mirado nada. Se detecto
# el 2026-09-05 al publicar el post III: el gate no se entero de la publicacion.
#
# Misma resolucion que `storage.py:20 default_state_dir()`: la variable de entorno
# manda, si no el directorio de estado del usuario. No se permite recurrir a un
# ledger distinto cuando el solicitado no existe: ocultaría una precondición rota.
LEDGER = File.join(File.expand_path(ENV.fetch("CUCHARADAS_DIFUSION_STATE_DIR",
  File.join(Dir.home, ".local", "state", "3cucharadas-difusion"))), "ledger.jsonl")
APLICAR = options[:aplicar]

unless File.file?(LEDGER)
  abort "No hay ledger para reconciliar el ref solicitado" if options[:ref] || APLICAR
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

vigentes = {}
File.foreach(LEDGER) do |linea|
  fila = begin
    JSON.parse(linea)
  rescue JSON::ParserError
    abort "Ledger inválido: no se puede reconciliar omitiendo eventos corruptos"
  end
  next if options[:ref] && fila["ref"] != options[:ref]
  key = [fila["ref"], fila["network"]]
  if fila["event"] == "network_rolled_back"
    vigentes.delete(key)
    next
  end
  next unless fila["event"] == "network_published"

  resultado = fila["result"] || {}
  url = resultado["root_url"].to_s
  next if url.empty?

  vigentes[key] = {
    ref: fila["ref"].to_s,
    red: fila["network"].to_s,
    url: url,
    reply_url: resultado["reply_url"].to_s,
    fecha: Date.parse(fila["timestamp"].to_s).to_s
  }
end
publicados = vigentes.values
abort "No hay publicaciones vigentes para el ref solicitado" if options[:ref] && publicados.empty?

faltan = publicados.reject do |p|
  entrada = por_ref[p[:ref]] || por_slug[p[:ref]]
  next false if entrada.nil? # sin entrada no se puede insertar; se reporta aparte

  Array(entrada["publicaciones"]).any? do |x|
    x.is_a?(Hash) && x["plataforma"] == p[:red] && x["url_publicada"].to_s == p[:url] &&
      (p[:reply_url].empty? || x["url_publicada_en"].to_s == p[:reply_url])
  end
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
    entrada = por_ref[p[:ref]] || por_slug[p[:ref]]
    existente = Array(entrada["publicaciones"]).find { |x| x.is_a?(Hash) && x["plataforma"] == p[:red] }
    if existente
      # Completar la respuesta EN sin duplicar plataforma ni borrar comentarios.
      raise "Conflicto de URL en #{slug}/#{p[:red]}" unless existente["url_publicada"].to_s == p[:url] && existente["url_publicada_en"].to_s.empty?
      stop = ((i_slug + 1)...lineas.length).find { |i| lineas[i].start_with?("- slug: ") } || lineas.length
      i_red = ((i_pub + 1)...stop).find { |i| lineas[i].strip == "- plataforma: #{p[:red]}" }
      raise "No se encontró la plataforma #{p[:red]}" unless i_red
      i_url = ((i_red + 1)...stop).find { |i| lineas[i].strip.start_with?("url_publicada:") }
      raise "No se encontró la URL de #{p[:red]}" unless i_url
      lineas.insert(i_url + 1, "    url_publicada_en: #{p[:reply_url]}\n")
      next []
    end
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

contenido = lineas.join
YAML.safe_load(contenido, permitted_classes: [Date, Time]) # validar ANTES de escribir
temporal = "#{YML}.#{Process.pid}.tmp"
File.write(temporal, contenido)
File.rename(temporal, YML)
puts "Reconciliadas #{insertables.length} publicacion(es) en _data/distribucion.yml."
