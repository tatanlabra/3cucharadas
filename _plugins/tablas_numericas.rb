# frozen_string_literal: true

# Cifras alineadas en las tablas del contenido (auditoría UX 2026-10-17, decisión
# sobre el estilo de tablas).
#
# POR QUE EXISTE
#
# Medido en producción el 2026-10-17 sobre las 96 tablas de los 24 posts: 924
# celdas numéricas en 38 tablas, el 61 % alineadas a la izquierda y ninguna con
# cifras tabulares. Así, 2.300 queda sobre 13.707 con las unidades desfasadas y
# las magnitudes no se comparan de un vistazo. La guía experta coincide:
# Remshard y Queenborough (2023, Ecology and Evolution, doi:10.1002/ece3.10062),
# tras revisar más de 1.000 tablas de 43 revistas, recomiendan alinear a la
# derecha las columnas numéricas con una fuente de cifras tabulares, y Schwabish
# (Ten Guidelines for Creating Better Tables, SAGE 2021) dice lo mismo.
#
# Las tablas salen de Markdown escrito a mano y de generadores sellados con
# sha256 (Avalúos II, assets/data/avaluos-ii-extension/provenance.json). Marcar
# columna por columna en cada fuente no escala y rompe esos sellos. Este hook
# marca, ya renderizado, cada columna cuyas celdas son mayoritariamente cifras.
#
# QUE HACE
#
# En cada tabla sin colspan ni rowspan, una columna que no es la primera (la
# primera rotula las filas) es numérica si al menos 2 celdas del cuerpo, y al
# menos el 60 % de sus celdas no vacías, son una cifra. Esas celdas y su
# encabezado reciben la clase `num`; el CSS las alinea al final con cifras
# tabulares. Un `style="text-align"` puesto por el autor (`|---:|` o `|:---:|`)
# gana por cascada: el hook no lo pisa.
#
# Igual que tabla_desplazable.rb: REXML analiza y el regex solo ubica las
# etiquetas que se editan, en el mismo orden de documento. Una tabla que no
# parsea no se toca. Es idempotente: no duplica `num`.

require "rexml/document"

module TablasNumericas
  CLASE = "num"
  MINIMO_CELDAS = 2
  PROPORCION = 0.6

  # Una cifra en notación chilena o inglesa: signo, moneda, miles con punto o
  # coma, decimales, porcentaje o unidad corta, estrellas de significancia y
  # paréntesis de error estándar. Los intervalos se reconocen aparte para no
  # confundir la coma decimal con el separador inglés entre extremos.
  CIFRA = /\A[(\[]?\s*[−\-+±~≈<>≤≥]?\s*[$€£]?\s*\d[\d.,  ]*(?:\s?(?:%|‰|pp|p\.\s?p\.|DE|SD|pts?|x|×))?\s*[)\]]?\**\z/
  INTERVALO = /\A[\[(]\s*(.+?)\s*(?:;|,\s+|–|—|\bto\b|\ba\b)\s*(.+?)\s*[\])]\s*(?:pp|p\.\s?p\.|pts?)?\s*\z/i

  module_function

  def texto(elemento)
    REXML::XPath.match(elemento, ".//text()").map { |t| t.value.to_s }.join
      .gsub(/[[:space:]  ]+/, " ").strip
  end

  def cifra?(texto)
    return false if texto.empty?
    return true if CIFRA.match?(texto)

    intervalo = INTERVALO.match(texto)
    intervalo && intervalo.captures.all? { |extremo| CIFRA.match?(extremo) }
  end

  # Índices de columna numérica, o nil si la tabla no se debe tocar.
  def columnas_numericas(fragmento)
    doc = REXML::Document.new(fragmento)
    return nil if REXML::XPath.first(doc, "//*[@colspan or @rowspan]")

    filas = REXML::XPath.match(doc, "//tbody/tr")
    return [] if filas.empty?

    celdas = filas.map { |fila| fila.elements.to_a.select { |e| %w[td th].include?(e.name) }.map { |c| texto(c) } }
    ancho = celdas.map(&:size).max || 0
    (1...ancho).select do |col|
      valores = celdas.map { |fila| fila[col] }.compact.reject(&:empty?)
      numericas = valores.count { |v| cifra?(v) }
      numericas >= MINIMO_CELDAS && numericas >= PROPORCION * valores.size
    end
  rescue REXML::ParseException
    nil
  end

  def con_clase(apertura)
    return apertura if apertura.match?(/\bclass="[^"]*\b#{CLASE}\b/)

    if apertura.match?(/\bclass="/)
      apertura.sub(/\bclass="([^"]*)"/) { %(class="#{Regexp.last_match(1)} #{CLASE}") }
    else
      apertura.sub(/\A<(td|th)/) { %(<#{Regexp.last_match(1)} class="#{CLASE}") }
    end
  end

  def marcar_tabla(fragmento)
    columnas = columnas_numericas(fragmento)
    return fragmento if columnas.nil? || columnas.empty?

    fragmento.gsub(%r{<tr\b[^>]*>.*?</tr>}m) do |fila|
      indice = -1
      fila.gsub(/<(?:td|th)\b[^>]*>/) do |apertura|
        indice += 1
        columnas.include?(indice) ? con_clase(apertura) : apertura
      end
    end
  end

  def marcar(html)
    return html unless html.is_a?(String) && html.include?("<table")

    rangos = TablaDesplazable.rangos_de_tabla(html)
    rangos.reverse_each do |ini, fin|
      html = html[0...ini] + marcar_tabla(html[ini...fin]) + html[fin..]
    end
    html
  end
end

Jekyll::Hooks.register :documents, :post_render, priority: :low do |doc|
  next unless doc.output.is_a?(String)
  next unless doc.collection&.label == "posts"

  doc.output = TablasNumericas.marcar(doc.output)
end
