#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de coherencia entre el paquete de difusión y el post que difunde.
#
# POR QUÉ EXISTE
#
# El 2026-09-05 el autor reescribió el post III y se llevó por delante la tabla de
# métricas del experimento. El carrusel de LinkedIn, el copy y los mensajes de
# Mastodon y Bluesky seguían citando `38/2/0`, `recall@5 0,9635`, `MRR 0,9010` y
# latencias de `15,83 s` y `91,10 s`. Publicarlos habría afirmado en cinco redes
# cifras que el artículo enlazado ya no contiene: el lector que hiciera clic no
# habría encontrado ninguna.
#
# Nadie lo habría notado. El paquete de difusión no se construye desde el post: se
# escribe a mano una vez y se queda quieto mientras el post cambia debajo.
#
# QUÉ COMPRUEBA
#
# Que toda cifra que una pieza de difusión afirme aparezca también en el cuerpo del
# post. No al revés: el post puede tener cifras que la difusión no destaque.
#
# Se comparan cifras normalizadas —«16.955», «16,955» y «16955» son la misma— para
# que la convención decimal de cada idioma no produzca falsos rojos.
#
# QUE NO COMPRUEBA
#
# Un punto ciego declarado, no descubierto: una cifra escrita dentro de un
# encabezado Markdown de una pieza no se compara. Falsado el 2026-09-05 --se
# metio `recall@5 0,9635` en un `###` del hilo de X y el gate siguio verde-- y
# se acepta a cambio de que el recuento de caracteres de cada post pueda vivir
# ahi. Si algun dia un encabezado lleva texto publicable, esta exclusion deja de
# ser inocua y hay que revisarla.
#
# Tampoco comprueba afirmaciones que no sean numericas: una pieza puede prometer
# una seccion que el post ya no tiene y este gate no lo vera.
#
# Uso:
#   ruby scripts/verify_difusion_coherente.rb
#   ruby scripts/verify_difusion_coherente.rb <ref>

require "set"
require "yaml"

ROOT = File.expand_path("..", __dir__)

# Cifras que no son afirmaciones sobre el contenido: fechas, tamaños de lámina,
# años de una cita, versiones. Comprobarlas daría rojos que no significan nada.
IGNORAR = /\A(19|20)\d\d\z|\A0?\d\z|\A(1080|1350|1200|630|1600|900|640|360|280|300|500)\z/

def normaliza(cifra)
  cifra.gsub(/[.,\s]/, "")
end

def cifras(texto)
  texto.scan(/\d+(?:[.,]\d+)*/).map { |c| normaliza(c) }.reject { |c| c.match?(IGNORAR) }
end

def cuerpo_del_post(path)
  raw = File.read(path)
  partes = raw.split(/^---$/, 3)
  cuerpo = partes.length >= 3 ? partes[2] : raw
  # El `en_abstract` del front matter también es texto publicado, así que cuenta.
  # Los comentarios YAML no: son notas para quien edita, no llegan a la página.
  # Sin esta exclusión, una referencia del tipo `julia_feed.rb:60` en un comentario
  # se leía como una cifra afirmada por una version y no por la otra, y rompía la
  # paridad. Observado el 2026-09-05 sobre un comentario propio.
  front = (partes[1] || "").lines.reject { |l| l.strip.start_with?("#") }.join
  cuerpo + front
end

ref = ARGV.first || "multiagente-penta-agent-memoria-gobernada"

posts = Dir.glob(File.join(ROOT, "_posts", "*.md")).select do |p|
  File.read(p).include?(ref.sub(/-poc\z/, "")) || File.basename(p).include?(ref)
end
if posts.empty?
  puts "SKIP: ningún post coincide con `#{ref}`."
  exit 0
end
# El universo es la union de las dos versiones del post, y por si sola esa union
# tiene un agujero: si una version queda obsoleta respecto de la otra, sus cifras
# viejas dan cobertura a una pieza de difusion que ya no deberia citarlas.
#
# Medido el 2026-09-05 falsando este mismo gate: se devolvio `0,9635` al carrusel
# --una cifra que el autor habia retirado del espanol-- y el gate siguio verde,
# porque la traduccion inglesa aun no se habia rehecho y todavia la contenia.
#
# Por eso se comprueba tambien la PARIDAD entre idiomas. Las dos condiciones
# juntas no son vacuas: una version obsoleta se detecta aqui, y solo con las dos
# alineadas tiene sentido el universo comun.
por_post = posts.to_h { |p| [File.basename(p), cifras(cuerpo_del_post(p)).uniq.to_set] }
universo = por_post.values.reduce(:|) || Set.new

if por_post.length == 2
  a, b = por_post.keys
  solo_a = por_post[a] - por_post[b]
  solo_b = por_post[b] - por_post[a]
  unless solo_a.empty? && solo_b.empty?
    errores_paridad = []
    errores_paridad << "solo en #{a}: #{solo_a.to_a.sort.first(8).join(', ')}" unless solo_a.empty?
    errores_paridad << "solo en #{b}: #{solo_b.to_a.sort.first(8).join(', ')}" unless solo_b.empty?
    warn "- paridad ES/EN rota: una version cita cifras que la otra no"
    errores_paridad.each { |e| warn "    #{e}" }
    abort "Gate de coherencia de difusion fallo (las dos versiones del post no coinciden en cifras)"
  end
end

piezas = Dir.glob(File.join(ROOT, "difusion", "**", "#{ref}*")).select do |p|
  File.file?(p) && %w[.md .html].include?(File.extname(p))
end
if piezas.empty?
  puts "SKIP: no hay piezas de difusión para `#{ref}`."
  exit 0
end

errores = []
piezas.each do |pieza|
  texto = File.read(pieza)
  # En el HTML del carrusel, solo el contenido visible: el CSS está lleno de
  # números que no afirman nada.
  texto = texto.sub(/<style>.*?<\/style>/m, "") if pieza.end_with?(".html")
  if pieza.end_with?(".md")
    # Mismo criterio que el `<style>` de arriba y que los comentarios YAML del
    # post: se compara lo que se publica, no el andamiaje.
    #
    # Un bloque cercado lleva el comando que regenera la pieza, y un encabezado
    # lleva su etiqueta --«ES root», «Carrusel», «01 - imagen ... 245/280»--.
    # Ninguno de los dos sale a ninguna red. Sin esta exclusion, el recuento de
    # caracteres de un hilo de X se leia como una afirmacion sobre el post y
    # daba ocho rojos que no significaban nada.
    #
    # No se excluye nada mas. Se descarto la regla tentadora de mirar solo lo que
    # cuelga de un `###`: `copy-linkedin.md` y `targeting.md` no tienen ninguno,
    # su texto publicable vive bajo `##`, y con esa regla el gate se habria
    # quedado ciego justo en las dos piezas donde nadie lo habria notado.
    texto = texto.gsub(/^```.*?^```/m, "").lines.reject { |l| l.start_with?("#") }.join
  end
  huerfanas = cifras(texto).uniq.reject { |c| universo.include?(c) }
  next if huerfanas.empty?

  errores << "#{pieza.sub("#{ROOT}/", '')}: afirma #{huerfanas.length} cifra(s) que el post no contiene: #{huerfanas.first(8).join(', ')}"
end

errores.each { |e| warn "- #{e}" }
if errores.any?
  abort "Gate de coherencia de difusión falló (#{errores.length} pieza(s) desalineada(s))"
end
puts "Gate de coherencia de difusión OK: #{piezas.length} pieza(s) contra #{posts.length} post(s), " \
     "#{universo.length} cifra(s) en el universo."
