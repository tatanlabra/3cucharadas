#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de difusion CUMPLIDA. No confundir con verify_distribution_readiness.rb,
# que pese a su nombre solo comprueba og:image, description, canonico y enlaces
# —es un gate de SEO—. Por eso el post III paso el pipeline entero sin que nadie
# notara que no era sindicable por ningun canal.
#
# Este gate hace la pregunta que faltaba: de los canales que el post DECLARA,
# cuales produjeron un artefacto verificable, y cuales llevan vencido su plazo.
#
# Fuente de verdad: _data/distribucion.yml, que esta versionado. El ledger del
# CLI de difusion vive fuera del repo y esta gitignorado, asi que en CI no
# existe: apoyarse en el haria un gate que en CI aprueba siempre.
#
# Plazos, de penta-agent/skills/publicacion-externa/references/checklists.md:
#   D2  hilo en Bluesky y Mastodon      (distribution.social: true)
#   D4  dev.to con canonico             (republish incluye `dev`)
#   D10 Medium                          (republish incluye `medium`)
#
# Uso:
#   ruby scripts/verify_distribution_done.rb            # falla si hay vencidos
#   ruby scripts/verify_distribution_done.rb --strict   # ademas falla por avisos
#   ruby scripts/verify_distribution_done.rb --ventana 30  # solo lo accionable hoy
#
# LA VENTANA, Y POR QUE NO ES UN INDULTO
#
# Sin `--ventana` el gate pregunta «de todo lo declarado, que falta»: hoy 7
# canales vencidos, algunos de hace 174 dias. Esa es la pregunta correcta para
# una auditoria y la INCORRECTA para un timer diario: un aviso que repite lo
# mismo cada manana durante medio ano se silencia, y un gate silenciado no
# interrumpe a nadie, que es el mismo fallo que no tenerlo.
#
# `--ventana N` acota los ERRORES a los posts de los ultimos N dias --lo que
# todavia se puede hacer a tiempo-- y sigue imprimiendo el atraso historico como
# aviso, con su cuenta. No lo esconde: lo baja de fatal a visible. El modo por
# defecto no cambia, y es el que va a CI.

require "date"
require "yaml"

ROOT = File.expand_path("..", __dir__)
STRICT = ARGV.include?("--strict")
VENTANA = begin
  i = ARGV.index("--ventana")
  i ? Integer(ARGV[i + 1]) : nil
end
HOY = (ENV["DISTRIBUCION_HOY"] ? Date.parse(ENV["DISTRIBUCION_HOY"]) : Date.today)

PLAZOS = { "social" => 2, "dev" => 4, "medium" => 10 }.freeze

errores = []
avisos = []
historicos = []

registro = begin
  path = File.join(ROOT, "_data", "distribucion.yml")
  File.file?(path) ? (YAML.safe_load_file(path, permitted_classes: [Date, Time]) || []) : []
end

def front_matter(path)
  raw = File.read(path)
  return nil unless raw.start_with?("---")

  fin = raw.index("\n---", 3)
  return nil unless fin

  YAML.safe_load(raw[4...fin], permitted_classes: [Date, Time]) || {}
rescue Psych::SyntaxError
  nil
end

def publicaciones_de(registro, slug)
  entrada = registro.find { |e| e.is_a?(Hash) && e["slug"] == slug }
  Array(entrada && entrada["publicaciones"]).select { |p| p.is_a?(Hash) }
end

# Un canal esta cumplido si dejo un artefacto identificable, no si alguien
# escribio su nombre: se exige la URL publicada, que es lo unico que prueba que
# el contenido existe fuera de este repositorio.
#
# CORRECCION 2026-09-05: bastaba con que existiera `devto_article_id`, y un
# borrador tiene id. `syndicate_devto.rb:304` crea toda entrada de dev.to con
# `estado: borrador` y NUNCA la cambia --publicar es una decision humana, alli--,
# asi que el gate daba por cumplido un canal cuyo articulo no ha visto nadie. El
# efecto era silencioso y creciente: cada borrador nuevo apagaba un pendiente
# real. Un borrador ahora no cuenta, y la unica forma de cerrar `dev` es publicar
# en dev.to y anotarlo aqui.
def cumplido?(pubs, plataformas)
  pubs.any? do |p|
    next false unless plataformas.include?(p["plataforma"].to_s)
    next false if p["estado"].to_s == "borrador"

    p["url_publicada"].to_s.strip != "" || p["devto_article_id"]
  end
end

posts = Dir.glob(File.join(ROOT, "_posts", "*.md")).sort
revisados = 0

posts.each do |path|
  front = front_matter(path)
  next unless front

  relativo = path.sub("#{ROOT}/", "")
  fecha = begin
    Date.parse(front["date"].to_s)
  rescue ArgumentError, TypeError
    nil
  end
  next unless fecha

  dias = (HOY - fecha).to_i
  distribution = front["distribution"]

  # Guarda contra el modo vacuo. Un post sin `distribution` no puede aprobar en
  # silencio: la lista vacia de canales haria que el bucle no iterara y el gate
  # saliera 0 sin comprobar nada. Los anteriores a que existiera la convencion
  # quedan como aviso; los nuevos, como error.
  unless distribution.is_a?(Hash)
    (dias > 30 ? avisos : errores) << "#{relativo}: no declara `distribution`; no se puede saber que canales le corresponden"
    next
  end

  slug = front["permalink"].to_s.chomp("/").split("/").last
  pubs = publicaciones_de(registro, slug)
  revisados += 1

  esperados = []
  esperados << "social" if distribution["social"]
  Array(distribution["republish"]).map { |t| t.to_s.downcase }.each do |canal|
    esperados << canal if PLAZOS.key?(canal)
  end

  esperados.each do |canal|
    plataformas = canal == "social" ? %w[mastodon bluesky] : [canal == "dev" ? "devto" : canal]
    next if cumplido?(pubs, plataformas)

    plazo = PLAZOS.fetch(canal)
    if dias > plazo
      linea = "#{relativo}: declara `#{canal}` y lleva #{dias} dias sin artefacto (plazo D#{plazo})"
      if VENTANA && dias > VENTANA
        historicos << linea
      else
        errores << linea
      end
    else
      avisos << "#{relativo}: `#{canal}` pendiente, D#{dias} de D#{plazo}"
    end
  end
end

historicos.uniq.each { |h| warn "- atraso historico (fuera de la ventana de #{VENTANA} dias): #{h}" }
avisos.uniq.each { |a| warn "- aviso: #{a}" }
errores.uniq.each { |e| warn "- #{e}" }

if !errores.empty?
  abort "Gate de difusion cumplida fallo (#{errores.uniq.length} canal(es) vencido(s) sin artefacto)"
elsif STRICT && !avisos.empty?
  abort "Gate de difusion cumplida fallo en modo --strict (#{avisos.uniq.length} aviso(s))"
end

resumen = "Gate de difusion cumplida OK: #{revisados} post(s) con canales declarados, " \
          "#{avisos.uniq.length} aviso(s)"
resumen += ", #{historicos.uniq.length} atraso(s) historico(s) fuera de la ventana" unless historicos.empty?
puts "#{resumen}."
