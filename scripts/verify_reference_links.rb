#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de enlaces de referencias científicas (decisión editorial del 2026-10-31).
#
# Toda entrada de referencias con DOI o id de arXiv debe:
#   - enlazar su DOI (o su página de arXiv) como destino de un enlace Markdown;
#   - enlazar a Google Scholar con la URL exacta del registro;
#   - enlazar al PDF del registro cuando el registro lo marca verificado;
#   - no enlazar ningún otro PDF que el registro no haya verificado.
# Una entrada es una línea bajo un encabezado de referencias o una definición `[^x]:`.
# Las citas del cuerpo no se evalúan aquí. El registro lo genera
# scripts/build_reference_links.py, que comprueba DOI ↔ título y PDF ↔ título.
#
# Uso: ruby scripts/verify_reference_links.rb [--registry R] [archivo.md ...]

require "yaml"

module ReferenceLinks
  REF_HEAD = /^\#{2,4}\s+(Referencias|References|Fuentes|Sources|Lectura complementaria|Further reading|Software y documentaci|Software and (technical )?documentation|Bibliograf|Bibliography)/i
  ANY_HEAD = /^\#{1,4}\s/
  DOI_URL = %r{https?://(?:dx\.)?doi\.org/(10\.\d{4,9}/(?:[^\s()>\]{}"'<]|\([^\s()>\]{}"'<]*\))+)}i
  ARXIV_URL = %r{https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?}i
  LINK = /\[([^\]]*)\]\(((?:[^()\s]|\([^()\s]*\))+)\)/
  SCHOLAR = "scholar.google.com/scholar_lookup"

  module_function

  def clean_doi(doi)
    doi.sub(/[.,;:]+\z/, "").strip
  end

  # Un PDF de arXiv junto a un DOI es la versión abierta de ese DOI, no otra
  # referencia (misma regla que build_reference_links.py).
  def identifiers(line)
    ids = line.scan(DOI_URL).flatten.map { |doi| "doi:#{clean_doi(doi).downcase}" }
    arxiv = line.to_enum(:scan, ARXIV_URL).map { Regexp.last_match }
    arxiv = arxiv.reject { |match| match[0].include?("/pdf/") } unless ids.empty?
    ids + arxiv.map { |match| "arxiv:#{match[1]}" }
  end

  def entries(text)
    ref_level = 0
    text.each_line.with_index(1).filter_map do |raw, number|
      line = raw.chomp
      if line.match?(ANY_HEAD)
        level = line[/\A#+/].length
        if line.match?(REF_HEAD)
          ref_level = level unless ref_level.positive? && level > ref_level
        elsif ref_level.zero? || level <= ref_level
          ref_level = 0
        end
      end
      next if line.start_with?("|")
      next unless ref_level.positive? || line.start_with?("[^")

      ids = identifiers(line).uniq
      # Una entrada que conserva su enlace a Scholar pero perdió el DOI sigue siendo
      # científica: sin esta guarda saldría del alcance del gate en silencio.
      next [number, line, []] if ids.empty? && line.include?(SCHOLAR)

      [number, line, ids] unless ids.empty?
    end
  end

  def words(text)
    text.unicode_normalize(:nfkd).encode("ASCII", undef: :replace, replace: "").downcase
        .scan(/[a-z0-9]+/).select { |word| word.length > 2 }.uniq
  end

  # Un texto de enlace es «el título» si comparte con el título oficial del registro
  # al menos 3 palabras (o todas, si el título oficial es más corto) y el 60 % de las
  # palabras del más corto de los dos.
  def title_label?(label, title)
    mine = words(label)
    official = words(title)
    return false if mine.empty? || official.empty?

    shared = (mine & official).length
    shared >= [3, official.length].min && shared >= 0.6 * [mine.length, official.length].min
  end

  def pdf_like?(label, url)
    label.strip.casecmp?("PDF") || url.match?(%r{\.pdf(\z|[?#])}i) || url.match?(%r{arxiv\.org/pdf/}i)
  end

  def check_entry(name, number, line, ids, registry, errors)
    where = "#{name}:#{number}"
    if ids.empty?
      errors << "#{where}: entrada con enlace a Scholar y sin DOI ni arXiv"
      return
    end
    if ids.length > 1
      errors << "#{where}: entrada con #{ids.length} identificadores (#{ids.join(', ')}); separar o elegir uno"
      return
    end
    entry = registry[ids.first]
    unless entry
      errors << "#{where}: #{ids.first} no está en el registro; correr scripts/build_reference_links.py"
      return
    end
    targets = line.scan(LINK)
    urls = targets.map(&:last)
    canonical = entry["kind"] == "doi" ? entry["doi_url"] : entry["arxiv_abs"]
    unless urls.any? { |url| url.casecmp?(canonical) }
      errors << "#{where}: falta el enlace #{entry['kind'] == 'doi' ? 'DOI' : 'arXiv'} #{canonical}"
    end
    if entry["scholar_url"] && !urls.include?(entry["scholar_url"])
      errors << "#{where}: falta el enlace a Scholar del registro"
    end
    if entry["pdf_verified"] && !urls.include?(entry["pdf_url"])
      errors << "#{where}: el registro tiene PDF verificado y la entrada no lo enlaza"
    end
    # El enlace cuyo texto es el título de la obra debe llevar al destino primario:
    # el PDF verificado o, si no hay, el DOI/arXiv. Sin esta regla bastaba con que
    # los destinos aparecieran en enlaces secundarios (hallazgo de Codex, 2026-10-31).
    primary = entry["pdf_verified"] ? entry["pdf_url"] : canonical
    titled = targets.select { |label, _url| title_label?(label, entry["title"].to_s) }
    errors << "#{where}: ningún enlace lleva el título de la obra (debe enlazar a #{primary})" if titled.empty?
    titled.each do |_label, url|
      next if url == primary

      errors << "#{where}: el título enlaza a #{url} y debe enlazar a #{primary}"
    end
    targets.each do |label, url|
      next unless pdf_like?(label, url)
      next if entry["pdf_verified"] && url == entry["pdf_url"]

      errors << "#{where}: PDF no verificado por el registro: #{url}"
    end
  end

  def run(files, registry_path)
    registry = YAML.safe_load_file(registry_path)
    raise "registro vacío: #{registry_path}" unless registry.is_a?(Hash) && !registry.empty?

    errors = []
    checked = 0
    files.each do |file|
      text = File.read(file, encoding: "UTF-8")
      entries(text).each do |number, line, ids|
        checked += 1
        check_entry(File.basename(file), number, line, ids, registry, errors)
      end
      # Todo identificador que el registro ubica en este post debe seguir en él: si
      # desapareció, se borró una referencia o el registro quedó viejo.
      present = entries(text).flat_map { |_number, _line, ids| ids }.uniq
      registry.each do |key, entry|
        next unless Array(entry["seen"]).include?(File.basename(file))
        next if present.include?(key)

        errors << "#{File.basename(file)}: #{key} figura en el registro y ya no está en el post; " \
                  "reponerlo o volver a correr scripts/build_reference_links.py"
      end
    end
    raise "ninguna entrada con DOI o arXiv evaluada: colección vacía o detección rota" if checked.zero?

    [checked, errors]
  end
end

if $PROGRAM_NAME == __FILE__
  registry = "_data/referencias_enlaces.yml"
  args = ARGV.dup
  if (index = args.index("--registry"))
    registry = args.delete_at(index + 1)
    args.delete_at(index)
  end
  annexes = [3, 4].product(["", "-en"]).map { |part, lang| "_pages/tesis-post#{part}-anexo-metodologico#{lang}.md" }
  files = args.empty? ? (Dir.glob("_posts/*.md") + annexes.select { |path| File.file?(path) }).sort : args
  begin
    checked, errors = ReferenceLinks.run(files, registry)
  rescue StandardError => e
    warn "REFERENCE_LINKS_ERROR #{e.message}"
    exit 2
  end
  if errors.empty?
    puts "REFERENCE_LINKS_VALID #{checked} entradas en #{files.length} archivos"
    exit 0
  end
  errors.each { |error| warn "REFERENCE_LINKS_INVALID #{error}" }
  warn "#{errors.length} errores en #{checked} entradas"
  exit 1
end
