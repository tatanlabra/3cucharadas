#!/usr/bin/env ruby
# frozen_string_literal: true

# Numeric consistency only, not semantic equivalence or publication verification.
# Explicit scope is required: REF or --all-declared (metadata-backed packages).
# Legacy ref-prefixed MD/HTML remain supported. Headings and fenced code in
# social Markdown are editorial scaffolding, excluded as in the historical gate.
require "set"
require "yaml"
require "json"
require "date"
require "bigdecimal"
require "optparse"

module DiffusionCoherence
  # Historical exclusions: dates, single-digit counts and common media sizes.
  # These limits are reported; this gate never proves every numeric claim.
  IGNORE = /\A(?:19|20)\d\d\z|\A0?\d\z|\A(?:1080|1350|1200|630|1600|900|640|360|280|300|500)\z/
  ADMIN = /\A(?:00-metadata|README|QA|AUDITORIA)(?:\.|\z)/i
  # Explicit historical filename alias; post lookup always uses its exact ref.
  LEGACY_PIECE_NAMES = { "multiagente-penta-agent-memoria-gobernada-poc" => "multiagente-penta-agent-memoria-gobernada" }.freeze
  EXTENSIONS = %w[.md .html .txt .json].freeze

  def self.front_and_body(path)
    raw = File.read(path)
    match = raw.match(/\A---\s*\n(.*?)^---\s*$\n?/m)
    return [{}, raw] unless match
    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: false) || {}
    raise "front matter inválido: #{path}" unless front.is_a?(Hash)
    [front, raw[match.end(0)..]]
  end

  def self.number(token, lang = nil)
    token = token.gsub(/[\u00a0\u202f ]/, "")
    # Version-like tokens remain literal: 4.5.3 is not decimal 453.
    return "literal:#{token}" if token.count(".") > 1 && !token.include?(",") && !token.match?(/\A\d{1,3}(?:\.\d{3})+\z/)
    return "literal:#{token}" if token.count(",") > 1 && !token.include?(".") && !token.match?(/\A\d{1,3}(?:,\d{3})+\z/)
    decimal = lang.to_s.start_with?("es") ? "," : lang.to_s.start_with?("en") ? "." : nil
    if token.match?(/\A0[.,]\d+\z/)
      separator = token[1]
      puts "NORMALIZE decimal #{token} (#{lang})" if decimal && separator != decimal
      decimal = separator
    end
    if token.include?(".") && token.include?(",")
      decimal ||= token.rindex(".") > token.rindex(",") ? "." : ","
    elsif token.match?(/[.,]/)
      separator = token.include?(",") ? "," : "."
      # Locale-free bilingual Markdown: 0.xxx is decimal; repeated groups of
      # three are thousands. Explicit language disambiguates 1.234 vs 1,234.
      decimal ||= if token.match?(/\A0[.,]/) || !token.match?(/\A\d{1,3}(?:[.,]\d{3})+\z/)
                    separator
                  end
    end
    if decimal && token.include?(decimal == "." ? "," : ".")
      grouping = decimal == "." ? "," : "."
      integer = token.split(decimal).first
      if integer.include?(grouping) && !integer.match?(/\A\d{1,3}(?:#{Regexp.escape(grouping)}\d{3})+\z/)
        raise "separador incompatible con idioma #{lang}: #{token}"
      end
    end
    clean = token.gsub(/[.,]/) { |s| s == decimal ? "." : "" }
    BigDecimal(clean).to_s("F").sub(/\.0+\z/, "").sub(/(\.\d*?)0+\z/, '\\1')
  end

  def self.numbers(text, lang = nil)
    # TeX decimal braces are punctuation, not distinct numeric tokens.
    text = text.gsub(/\{([.,])\}/, '\\1').gsub(%r{https?://[^\s<>]+}, "")
    # RSS 2.0 is a version identifier, not a Spanish decimal. Normalize its
    # two-component form to the existing literal-version branch so parity is
    # still checked without imposing a locale separator on the protocol name.
    text = text.gsub(/\bRSS\s+(\d+)\.(\d+)\b/i, '\\1.\\2.0')
    text.scan(/\d+(?:[.,]\d+)*(?:[\u00a0\u202f]\d{3})*/).map { |n| number(n, lang) }
        .reject { |n| n.match?(IGNORE) }.to_set
  end

  def self.copy_parts(path, lang)
    text = File.read(path)
    raise "copy vacío: #{path}" if text.strip.empty?
    if File.basename(path) == "reddit-target.md"
      labels = ["TÍTULO PROVISIONAL", "URL PROPUESTA", "PRIMER COMENTARIO PROPUESTO"]
      sections = labels.map do |label|
        match = text.match(/^#{Regexp.escape(label)}:\s*\n(.*?)(?=^[A-ZÁÉÍÓÚÑ ][A-ZÁÉÍÓÚÑ ]+:\s*$|\z)/m)
        raise "sección publicable ausente: #{label} en #{path}" unless match
        raise "sección publicable vacía: #{label} en #{path}" if match[1].strip.empty?
        match[1]
      end
      puts "EXTRACTION #{path}: título, URL y primer comentario; reglas y recordatorios son notas operativas"
      return [[sections.join("\n"), nil]]
    end
    if path.end_with?(".json")
      data = JSON.parse(text)
      # Current social.json contract: localized public copy, not metadata values.
      unless data.is_a?(Hash) && !data.empty? && data.keys.all? { |k| %w[es en].include?(k) } && data.values.all? { |v| v.is_a?(String) && !v.strip.empty? }
        raise "JSON de copy no reconocido: #{path}; declarar extracción antes de afirmar cobertura"
      end
      return data.map { |locale, copy| [copy, locale] }
    end
    if path.end_with?(".html")
      text = text.gsub(/<(style|script)\b[^>]*>.*?<\/\1>/m, "").gsub(/<[^>]+>/, " ")
    elsif path.end_with?(".md")
      _, text = front_and_body(path)
      text = text.gsub(/^```.*?^```[^\n]*$/m, "").lines.reject { |line| line.start_with?("#") }.join
    end
    raise "copy extraído vacío: #{path}" if text.strip.empty?
    [[text, path.end_with?(".txt") ? lang : nil]]
  end

  # Only explicit time expressions qualify for ms -> seconds rounding. No
  # tolerance is applied to arbitrary numbers, taxes or decimal rates. Matching
  # numeric sets does not assign values to claims, subjects or causal mechanisms.
  def self.milliseconds(text, lang)
    text.gsub("*", "").scan(/(\d+(?:[.,]\d+)*)\s*ms\b/).map { |item| BigDecimal(number(item.first, lang)) }
  end

  def self.rounded_seconds(text, lang, source_ms)
    text.gsub("*", "").scan(/(\d+(?:[.,]\d+)?)(?:\s*(?:a|to|→|and|y|–|-)\s*(\d+(?:[.,]\d+)?))?\s*(?:s|seconds?|segundos?)\b/).flatten.compact.filter_map do |token|
      value = number(token, lang)
      # Precision belongs to the written token: 6,20 asks for two decimal
      # places even though its canonical numeric value is 6.2.
      precision = token[/[.,](\d+)\z/, 1]&.length
      next unless precision
      origin = source_ms.find { |ms| (ms / 1000).round(precision) == BigDecimal(value) }
      if origin
        puts "EQUIVALENCE #{origin.to_s('F')} ms -> #{value} s (#{precision} decimales)"
        value
      end
    end.to_set
  end

  def self.check(root, ref)
    raise "ref inválida" unless ref.match?(/\A[a-zA-Z0-9_-]+\z/)
    posts = Dir.glob(File.join(root, "_posts", "*.md")).filter_map do |path|
      front, body = front_and_body(path)
      [path, front, body] if front["ref"] == ref
    end
    raise "sin cobertura: ningún post con ref exacta #{ref}" if posts.empty?
    puts "REF #{ref}"
    values = posts.map do |path, front, body|
      puts "SOURCE #{path.delete_prefix(root + '/')} lang=#{front['lang']}"
      public_front = %w[title subtitle excerpt description entorno].filter_map { |key| front[key] }.join("\n")
      numbers(body + "\n" + public_front, front["lang"]) | numbers(front.fetch("en_abstract", "").to_s, "en")
    end
    package = File.join(root, "difusion", "paquetes", ref)
    lang = "es"
    metadata = Dir.glob(File.join(package, "00-metadata.{json,yaml,yml}"))
    raise "metadata duplicada para #{ref}" if metadata.size > 1
    unless metadata.empty?
      data = metadata.first.end_with?(".json") ? JSON.parse(File.read(metadata.first)) : YAML.safe_load_file(metadata.first, permitted_classes: [Date, Time], aliases: false)
      raise "metadata inválida para #{ref}" unless data.is_a?(Hash)
      lang = data.fetch("language", "es")
    end
    basename = LEGACY_PIECE_NAMES.fetch(ref, ref)
    legacy = Dir.glob(File.join(root, "difusion", "**", "#{basename}-*")) + Dir.glob(File.join(root, "difusion", "**", "#{basename}.*"))
    # Historical artifacts are MD/HTML; state JSON is a ledger, never public copy.
    legacy.select! { |path| %w[.md .html].include?(File.extname(path)) }
    pieces = Dir.glob(File.join(package, "*")) + legacy
    pieces = pieces.uniq.select { |path| File.file?(path) && EXTENSIONS.include?(File.extname(path)) && !File.basename(path).match?(ADMIN) }.sort
    raise "sin cobertura: no hay piezas para #{ref}" if pieces.empty?
    errors = []
    values.drop(1).each_with_index do |set, index|
      difference = (values[0] - set) | (set - values[0])
      errors << "paridad entre #{File.basename(posts[0][0])} y #{File.basename(posts[index + 1][0])}: #{difference.to_a.sort.first(12).join(', ')}" unless difference.empty?
    end
    universe = values.reduce(:|)
    source_ms = posts.flat_map { |_path, front, body| milliseconds(body, front["lang"]) }
    pieces.each do |path|
      puts "COPY #{path.delete_prefix(root + '/')}"
      orphaned = copy_parts(path, lang).flat_map do |copy, locale|
        (numbers(copy, locale) - universe - rounded_seconds(copy, locale, source_ms)).to_a
      end.uniq
      errors << "#{path.delete_prefix(root + '/')}: cifras ausentes del post: #{orphaned.first(12).join(', ')}" unless orphaned.empty?
    end
    errors.each { |error| warn "- #{error}" }
    puts "COVERAGE #{ref}: #{posts.size} posts, #{pieces.size} piezas, #{universe.size} cifras; excluye años, cifras enteras de un dígito, tamaños comunes y encabezados/código de copy Markdown"
    errors.empty?
  end

  def self.run(args)
    options = { root: File.expand_path("..", __dir__) }
    OptionParser.new do |parser|
      parser.on("--root PATH") { |value| options[:root] = File.expand_path(value) }
      parser.on("--all-declared") { options[:all] = true }
    end.parse!(args)
    raise "indicar REF o --all-declared, no ambos" unless (options[:all] && args.empty?) || (!options[:all] && args.length == 1)
    refs = if options[:all]
             Dir.glob(File.join(options[:root], "difusion", "paquetes", "*", "00-metadata.{json,yaml,yml}")).map { |path| File.basename(File.dirname(path)) }.uniq.sort
           else
             args
           end
    raise "sin cobertura: no hay paquetes declarados" if refs.empty?
    results = refs.map do |ref|
      begin
        check(options[:root], ref)
      rescue StandardError => error
        warn "FAIL #{ref}: #{error.message}"
        false
      end
    end
    puts "#{results.all? ? 'PASS' : 'FAIL'}: coherencia numérica; #{refs.size} ref(s) explícitas"
    results.all? ? 0 : 1
  rescue StandardError => error
    warn "FAIL: #{error.message}"
    1
  end
end

exit DiffusionCoherence.run(ARGV) if $PROGRAM_NAME == __FILE__
