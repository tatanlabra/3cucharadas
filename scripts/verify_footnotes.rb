#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de notas al pie kramdown (2026-10-31).
#
# Las citas de los posts llevan al pie con notas `[^clave]`. kramdown descarta en
# silencio la definición que nadie cita, deja como texto literal la marca sin
# definición y no avisa de nada: el post se publica con una referencia menos. Este
# gate lo comprueba en dos niveles por cada post con notas:
#   1. fuente: cada definición se cita y cada marca tiene definición; claves únicas;
#   2. render: kramdown (GFM, como _config.yml) produce exactamente tantas notas como
#      definiciones, sin marcas literales `[^` sobrevivientes en el HTML.
# Con --site DIR compara además contra el HTML del build: el número de <li> en
# .footnotes de cada página publicada debe coincidir con las definiciones del post.
#
# Uso: bundle exec ruby scripts/verify_footnotes.rb [--site _site] [archivo.md ...]

require "kramdown"
require "kramdown-parser-gfm"
require "yaml"

module Footnotes
  DEF = /^\[\^([^\]\s]+)\]:\s*\S/
  MARK = /\[\^([^\]\s]+)\](?!:)/

  module_function

  def split_front(text)
    match = text.match(/\A---\s*\n(.*?)\n---\s*\n/m)
    return [{}, text] unless match

    [YAML.safe_load(match[1], permitted_classes: [Date, Time]) || {}, text[match.end(0)..]]
  end

  # Quita lo que kramdown no debe ver: Liquid, bloques de código y código en línea.
  def prose(body)
    body.gsub(/^(```|~~~).*?^\1/m, "")
        .gsub(/\{%-?.*?-?%\}/m, "")
        .gsub(/\{\{.*?\}\}/m, "x")
  end

  def check(path)
    errors = []
    _front, body = split_front(File.read(path, encoding: "UTF-8"))
    text = prose(body)
    definitions = text.scan(DEF).flatten
    return [0, errors] if definitions.empty? && text !~ MARK

    without_code = text.gsub(/`[^`\n]*`/, "")
    marks = without_code.lines.reject { |line| line.match?(DEF) }.join.scan(MARK).flatten
    name = File.basename(path)
    duplicates = definitions.tally.select { |_key, count| count > 1 }.keys
    errors << "#{name}: definición duplicada: #{duplicates.join(', ')}" unless duplicates.empty?
    orphans = definitions.uniq - marks
    errors << "#{name}: definición sin cita (kramdown la descarta): #{orphans.join(', ')}" unless orphans.empty?
    missing = marks.uniq - definitions
    errors << "#{name}: marca sin definición (queda como texto): #{missing.join(', ')}" unless missing.empty?

    html = Kramdown::Document.new(text, input: "GFM", auto_ids: true, footnote_nr: 1, hard_wrap: false).to_html
    rendered = html[/<div class="footnotes".*?<\/div>/m].to_s.scan(/<li id="fn:/).length
    if rendered != definitions.uniq.length
      errors << "#{name}: kramdown rinde #{rendered} notas y la fuente define #{definitions.uniq.length}"
    end
    leftovers = html.gsub(/<code>.*?<\/code>/m, "").scan(/\[\^[^\]\s]+\]/)
    errors << "#{name}: marcas literales en el HTML: #{leftovers.uniq.join(', ')}" unless leftovers.empty?
    [definitions.uniq.length, errors]
  end

  def site_page(site, front)
    permalink = front["permalink"].to_s
    return nil if permalink.empty?

    File.join(site, permalink.sub(%r{\A/}, ""), "index.html").sub(%r{/+index\.html\z}, "/index.html")
  end

  def check_site(path, site, expected)
    front, = split_front(File.read(path, encoding: "UTF-8"))
    page = site_page(site, front)
    return ["#{File.basename(path)}: sin permalink para comparar con el build"] unless page
    return ["#{File.basename(path)}: no existe #{page} en el build"] unless File.file?(page)

    html = File.read(page, encoding: "UTF-8")
    count = html[/<div class="footnotes".*?<\/div>/m].to_s.scan(/<li id="fn:/).length
    count == expected ? [] : ["#{File.basename(path)}: el build publica #{count} notas y la fuente define #{expected}"]
  end
end

if $PROGRAM_NAME == __FILE__
  args = ARGV.dup
  site = nil
  if (index = args.index("--site"))
    site = args.delete_at(index + 1)
    args.delete_at(index)
  end
  files = args.empty? ? Dir.glob("_posts/*.md").sort : args
  errors = []
  posts = 0
  notes = 0
  files.each do |file|
    count, file_errors = Footnotes.check(file)
    errors.concat(file_errors)
    next if count.zero?

    posts += 1
    notes += count
    errors.concat(Footnotes.check_site(file, site, count)) if site
  end
  if posts.zero?
    warn "FOOTNOTES_ERROR ningún post con notas: colección vacía o detección rota"
    exit 2
  end
  if errors.empty?
    puts "FOOTNOTES_VALID #{notes} notas en #{posts} posts#{site ? " (fuente y build)" : ''}"
    exit 0
  end
  errors.each { |error| warn "FOOTNOTES_INVALID #{error}" }
  exit 1
end
