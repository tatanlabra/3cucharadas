# frozen_string_literal: true

# Una sola región enfocable por tabla (U25, auditoría UX 2026-10-17).
#
# Los generadores de Avalúos II (scripts/catastro_sii/*.py) envuelven cada tabla en
# un <div role="region" tabindex="0"> con desplazamiento propio, y después
# tabla_desplazable.rb la envuelve otra vez en .tabla-desliza, también región y
# también enfocable. Resultado: dos paradas de tabulación y dos regiones anunciadas
# para la misma tabla, una con la etiqueta buena (la leyenda) y otra con una
# genérica («Tabla desplazable horizontalmente 3»).
#
# No se corrigen los generadores: sus salidas y su propio código están sellados con
# sha256 en assets/data/avaluos-ii-extension/provenance.json, y regenerarlos exige
# datos que no viven en este repo. Este hook actúa sobre el HTML ya renderizado,
# después de tabla_desplazable.rb (prioridad baja = corre al final):
#
#   - la región externa deja de serlo: sin role, tabindex, aria-label ni scroll;
#   - su etiqueta descriptiva pasa a la región del plugin, que es la que desplaza;
#   - el envoltorio intermedio `width:max-content` pierde ese estilo, que forzaba
#     la tabla a su ancho máximo aunque cupiera partiendo encabezados.
#
# Y en todo el sitio: una región del plugin con etiqueta genérica («Tabla desplazable
# horizontalmente N») cuya tabla tiene <caption> pasa a llamarse como la leyenda.
#
# Es idempotente: tras la primera pasada la región externa ya no tiene role.
module RegionUnica
  GENERICA = %r{
    <div\ class="tabla-desliza"(?<antes>[^>]*?)\baria-label="(?:Tabla\ desplazable\ horizontalmente|Horizontally\ scrollable\ table)[^"]*"(?<despues>[^>]*)>
    (?<tabla>\s*<table\b[^>]*>\s*<caption>(?<leyenda>.*?)</caption>)
  }mx

  ANIDADA = %r{
    <div\b(?<externos>[^>]*\brole="region"[^>]*)>
    (?<entre>(?:\s*<div\b[^>]*>)*\s*)
    <div\ class="tabla-desliza"(?<internos>[^>]*)>
  }mx

  module_function

  def normalizar(html)
    return html unless html.is_a?(String) && html.include?('class="tabla-desliza"')

    html = html.gsub(ANIDADA) do
      externos = Regexp.last_match[:externos]
      entre = Regexp.last_match[:entre]
      internos = Regexp.last_match[:internos]
      next Regexp.last_match[0] unless externos.include?('tabindex="0"')

      etiqueta = externos[/\baria-label="([^"]*)"/, 1]
      externos = externos.gsub(/\s(?:role|tabindex|aria-label)="[^"]*"/, "")
      externos = externos.gsub(/\sstyle="[^"]*overflow[^"]*"/, "")
      entre = entre.gsub(/\sstyle="width:max-content;min-width:100%"/, "")
      internos = internos.sub(/\baria-label="[^"]*"/, %(aria-label="#{etiqueta}")) if etiqueta && !etiqueta.empty?
      %(<div#{externos}>#{entre}<div class="tabla-desliza"#{internos}>)
    end

    html.gsub(GENERICA) do
      m = Regexp.last_match
      leyenda = m[:leyenda].gsub(/<[^>]+>/, "").gsub(/\s+/, " ").strip.gsub('"', "&quot;")
      next m[0] if leyenda.empty?

      %(<div class="tabla-desliza"#{m[:antes]}aria-label="#{leyenda}"#{m[:despues]}>#{m[:tabla]})
    end
  end
end

Jekyll::Hooks.register [:documents, :pages], :post_render, priority: :low do |doc|
  next unless doc.output.is_a?(String)

  doc.output = RegionUnica.normalizar(doc.output)
end
