# frozen_string_literal: true

# Envuelve las tablas del contenido editorial en un contenedor que asume el
# desplazamiento horizontal, y las clasifica por perfil para que el CSS pueda
# darles un `min-width` distinto.
#
# POR QUE EXISTE
#
# `table` recibe `display: block` (tema) y, por debajo de 64em, el propio sitio
# redeclara `display:block` + `overflow-x:auto` en main.scss:1476-1483. Ninguna
# regla le da `min-width`. Sin suelo, el algoritmo de tabla comprime cada columna
# hacia su `min-content` hasta caber siempre, asi que el `overflow-x` que ya
# existe NUNCA dispara: no hay desbordamiento porque la tabla se estruja.
#
# Medido en produccion el 2026-09-05 sobre el post III (Playwright, viewport real):
#
#   viewport 320 -> columna 288px, tabla mas alta 3.414px, celda de prosa 69px
#   viewport 390 -> columna 358px, tabla mas alta 2.237px, celda de prosa 67px
#   viewport 1280-> columna 636px, tabla mas alta 1.139px, celda de prosa 157px
#
# A 320px las 7 tablas de ese post suman 12.655px de una pagina de 32.786: el 39%
# del alto. Una fila media a 390px: cuatro celdas de 72/151/68/67px, las cuatro de
# 20 lineas. Envolver sin poner suelo no arregla nada; el suelo sin contenedor
# desbordaria el documento. Hacen falta las dos cosas, y por eso van juntas.
#
# POR QUE ESTE HOOK
#
# `:documents, :post_render` opera sobre `doc.output`, ya con layout. Se descarto
# `:posts, :post_convert` porque jekyll-feed emite `post.content` dentro de
# <content> --lo demuestra _plugins/feed_license_footer.rb:62-64, que inyecta
# justo ahi-- y los envoltorios contaminarian /feed.xml y /en/feed.xml.
#
# POR QUE REXML Y NO NOKOGIRI
#
# Nokogiri no es dependencia del proyecto: cero coincidencias en Gemfile.lock, y
# anadirla obliga a tocar el lockfile y a compilar nativo sobre el ruby:3.3 fijado
# por digest en CI. REXML es stdlib y ya se usa para parsear en
# scripts/verify_site_artifact.rb:294-304. Comprobado el 2026-09-05: parsea las 63
# tablas del sitio construido sin un solo fallo.
#
# El regex localiza los limites de cada tabla contando profundidad; quien entiende
# la estructura --columnas, longitud de celda, si ya esta envuelta-- es REXML. No
# se usa regex como parser, que es lo que el encargo prohibe.

require "rexml/document"

module TablaDesplazable
  CLASE = "tabla-desliza"

  # Una celda con mas de este numero de caracteres convierte la tabla en
  # narrativa. El umbral sale del inventario real de 62 tablas en 12 posts: las
  # numericas (CASEN, 7 columnas) no pasan de 25 caracteres por celda; las
  # narrativas (post III 188, bayes 393) lo superan con holgura. No es un numero
  # elegido a ojo: es el hueco que separa los dos perfiles que existen.
  UMBRAL_NARRATIVA = 60

  ETIQUETAS = {
    "es" => "Tabla desplazable horizontalmente",
    "en" => "Horizontally scrollable table"
  }.freeze

  module_function

  # Devuelve los rangos [inicio, fin) de cada <table> de primer nivel.
  # Cuenta profundidad para no romperse con tablas anidadas, aunque hoy no
  # existan: que no las haya hoy no es garantia de que no las haya manana.
  def rangos_de_tabla(html)
    rangos = []
    profundidad = 0
    inicio = nil
    html.to_enum(:scan, %r{<table\b|</table>}).each do
      m = Regexp.last_match
      if m[0].start_with?("<table")
        inicio = m.begin(0) if profundidad.zero?
        profundidad += 1
      else
        profundidad -= 1
        if profundidad.zero? && inicio
          rangos << [inicio, m.end(0)]
          inicio = nil
        end
      end
    end
    rangos
  end

  # Perfil segun la celda mas larga. REXML hace el trabajo: contar columnas a
  # ojo con un regex daria mal los colspan.
  def perfil(fragmento)
    doc = REXML::Document.new(fragmento)
    celdas = []
    # Texto visible de la celda, incluido el que va dentro de <code>, <a> o
    # <strong>: `e.text` solo devuelve el primer nodo de texto y se dejaria
    # fuera casi todo el contenido de una celda con marcado.
    longitud = lambda do |elemento|
      REXML::XPath.match(elemento, ".//text()").map { |t| t.value.to_s }.join.strip.length
    end
    doc.elements.each("//td") { |e| celdas << longitud.call(e) }
    doc.elements.each("//th") { |e| celdas << longitud.call(e) }
    max = celdas.max || 0

    # Columnas de la fila mas ancha, contando colspan. Se usa para escalar el
    # suelo: un suelo fijo dejaria una tabla de 3 columnas mas holgada que una
    # de 4 sin razon, y al reves.
    columnas = 0
    doc.elements.each("//tr") do |fila|
      n = 0
      fila.elements.each("th | td") { |c| n += (c.attributes["colspan"] || 1).to_i }
      columnas = n if n > columnas
    end

    [max > UMBRAL_NARRATIVA ? "narrativa" : "numerica", [columnas, 1].max]
  rescue REXML::ParseException
    # Una tabla que no parsea no se transforma. Falla cerrado: mejor una tabla
    # sin arreglar que una tabla rota.
    nil
  end

  def envolver(html, lang)
    return html unless html.is_a?(String)

    etiqueta = ETIQUETAS.fetch(lang.to_s, ETIQUETAS["es"])
    rangos = rangos_de_tabla(html)
    return html if rangos.empty?

    # De atras hacia adelante para que los offsets no se muevan al insertar.
    rangos.reverse_each do |(ini, fin)|
      fragmento = html[ini...fin]

      # Idempotencia estructural, no por contador: polyglot hace una pasada de
      # render por idioma. La pregunta correcta es si ESTA tabla ya tiene su
      # envoltorio, no cuantas llevo vistas.
      antes = html[0...ini]
      next if antes.rstrip.end_with?(%(class="#{CLASE}">))

      datos = perfil(fragmento)
      next if datos.nil?

      p, columnas = datos
      apertura = %(<div class="#{CLASE}" data-perfil="#{p}" data-columnas="#{columnas}" ) +
                 %(style="--columnas: #{columnas}" role="region" ) +
                 %(aria-label="#{etiqueta}" tabindex="0">)
      html = html[0...ini] + apertura + fragmento + "</div>" + html[fin..]
    end
    html
  end
end

Jekyll::Hooks.register :documents, :post_render do |doc|
  next unless doc.output.is_a?(String)
  next unless doc.collection&.label == "posts"

  doc.output = TablaDesplazable.envolver(doc.output, doc.data["lang"])
end
