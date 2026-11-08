#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de auditoría pre-publicación para promover un borrador (_drafts/*.md) a post
# productivo (_posts/*.md) en 3cucharadas.
#
# Modos de uso:
#   ruby scripts/verify_draft_promotion.rb --fixture-red
#     Ejecuta el fixture negativo y devuelve exit 1 con el detalle de las violaciones
#     observadas (gates-falsables.md: "Un criterio no está validado hasta que se le ha
#     visto en rojo").
#
#   ruby scripts/verify_draft_promotion.rb --fixture
#     Ejecuta canario rojo + verde (self-test): verifica que cada violación material
#     dispare su fallo específico y que el caso sano pase en 0.
#
#   ruby scripts/verify_draft_promotion.rb [--draft-ready | --production] <archivo.md> [...]
#     - --draft-ready (por defecto para rutas en _drafts/): exige atribución válida en
#       _data/authors.yml (clabra), author_profile: true, ausencia de mathjax: true,
#       metadatos obligatorios (description, excerpt, ref, permalink, lang, ai_disclosure),
#       justificado tipográfico, sección ## Referencias, imágenes y videos locales con
#       width/height/alt/poster, enlaces internos existentes y reglas editoriales
#       2026-10-31+ (0 comillas « », 0 primera persona plural).
#     - --production (por defecto para rutas en _posts/): exige todo lo anterior más
#       paridad bilingüe ES/EN (mismo ref y permalink), visual_id, ficha en
#       _data/visuales/<visual_id>.yml con el post en la clave posts: y header completo
#       en heroes-v2/.

require "date"
require "yaml"
require_relative "verify_hero_disclosure"

module DraftPromotionCheck
  module_function

  EDITORIAL_CUTOFF_DATE = Date.new(2026, 10, 31)
  THESIS_JUSTIFIED_REFS = %w[costos-cierre-escolar-trayectorias cierre-escolar-educacion-superior-causal-ml].freeze
  REQUIRED_FRONT_KEYS = %w[
    layout title subtitle date categories tags description excerpt
    author lang ref permalink toc ai_disclosure
  ].freeze

  def split_front_matter(content)
    match = content.match(/\A---\s*\n(.*?\n)---\s*\n(.*)\z/m)
    return [nil, content, ["missing YAML front matter delimiters (---)"]] unless match

    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true)
    return [nil, match[2], ["front matter is not a YAML mapping"]] unless front.is_a?(Hash)

    [front, match[2], []]
  rescue Psych::Exception => e
    [nil, content, ["invalid YAML front matter: #{e.message}"]]
  end

  def load_authors(root)
    authors_path = File.join(root, "_data", "authors.yml")
    return {} unless File.file?(authors_path)

    YAML.safe_load_file(authors_path, permitted_classes: [Date, Time], aliases: true) || {}
  end

  def known_permalinks(root)
    @known_permalinks ||= begin
      set = {}
      Dir.glob(File.join(root, "{_posts,_pages,pages}/**/*.{md,html}")).each do |file|
        front, _, errs = split_front_matter(File.read(file))
        next unless errs.empty? && front.is_a?(Hash)

        perm = front["permalink"].to_s.strip
        set[perm] = true unless perm.empty?
      end
      set
    end
  end

  def parse_post_date(raw_date, path)
    return raw_date.to_date if raw_date.respond_to?(:to_date)

    str = raw_date.to_s.strip
    return Date.parse(str[0, 10]) if str.match?(/\A\d{4}-\d{2}-\d{2}/)

    base = File.basename(path.to_s)
    return Date.parse(base[0, 10]) if base.match?(/\A\d{4}-\d{2}-\d{2}/)

    nil
  rescue Date::Error
    nil
  end

  def strip_non_narrative(body)
    cleaned = body.dup
    cleaned.gsub!(/<!--.*?-->/m, "")
    cleaned.gsub!(/<style\b[^>]*>.*?<\/style>/im, "")
    cleaned.gsub!(/<script\b[^>]*>.*?<\/script>/im, "")
    cleaned.gsub!(/<pre\b[^>]*>.*?<\/pre>/im, "")
    cleaned.gsub!(/^```.*?^```/m, "")
    cleaned.gsub!(/`[^`]+`/, "")
    cleaned
  end

  def scoped_thesis_justification?(stylesheet)
    stylesheet.match?(
      /\.thesis-extension-post\.post3-evidence\s+\.page__content\s+p\s*\{\s*text-align:\s*justify;\s*hyphens:\s*auto;/
    )
  end

  def clean_liquid_url(raw)
    val = raw.to_s.strip
    if (m = val.match(/\{\{\s*['"]([^'"]+)['"]\s*\|\s*relative_url\s*\}\}/))
      return m[1]
    end
    val
  end

  def audit_content(content, root:, path: "memory.md", mode: :draft_ready, check_bilingual_pair: true)
    front, body, errors = split_front_matter(content)
    return errors unless front

    # 1. Campos obligatorios de frontmatter
    REQUIRED_FRONT_KEYS.each do |key|
      val = front[key]
      if val.nil? || (val.respond_to?(:empty?) && val.empty?)
        errors << "frontmatter.#{key}: missing or empty"
      end
    end

    permalink = front["permalink"].to_s.strip
    if !permalink.empty? && (!permalink.start_with?("/") || !permalink.end_with?("/"))
      errors << "frontmatter.permalink: must start and end with '/' (got '#{permalink}')"
    end

    # 2. Atribución de autor contra _data/authors.yml
    authors = load_authors(root)
    author_key = front["author"].to_s.strip
    if author_key.empty?
      errors << "frontmatter.author: missing"
    elsif !authors.key?(author_key)
      valid_keys = authors.keys.join(", ")
      errors << "frontmatter.author: '#{author_key}' not found in _data/authors.yml (expected: #{valid_keys})"
    end
    errors << "frontmatter.author_profile: must be true so author name and citation box render" unless front["author_profile"] == true

    # 3. Prohibición de MathJax (verify_site_artifact.rb falla si aparece MathJax)
    if front["mathjax"] == true
      errors << "frontmatter.mathjax: true is forbidden by verify_site_artifact.rb (use math: false or static KaTeX)"
    end
    errors << "body contains unrendered LaTeX $...$ with math: false" if front["math"] == false && strip_non_narrative(body).match?(/(?<!\\)\$[^\n$]+\$/)

    # 4. ai_disclosure válido
    begin
      AiDisclosure.resolve(front)
    rescue ArgumentError => e
      errors << "frontmatter.ai_disclosure: #{e.message}"
    end

    # 5. Reglas editoriales del corpus (aplicables desde 2026-10-31 o en modo draft_ready)
    post_date = parse_post_date(front["date"], path)
    enforce_2026_10_31_rules = (mode == :draft_ready) || (post_date && post_date >= EDITORIAL_CUTOFF_DATE)
    narrative = strip_non_narrative(body)

    if enforce_2026_10_31_rules
      # 5a. Comillas angulares prohibidas (« »)
      all_text = [front["title"], front["subtitle"], front["description"], front["excerpt"], narrative].compact.join("\n")
      if all_text.match?(/[«»]/)
        errors << "editorial: angular quotes (« ») are forbidden; use double quotes (\"\")"
      end

      # 5b. Primera persona plural autoral prohibida
      if narrative.match?(/\b(nosotros|nosotras|nuestro|nuestra|nuestros|nuestras)\b/i)
        errors << "editorial: first-person plural pronoun (nosotros/nuestro) detected; use first-person singular (yo/mi)"
      end

      # 5c. Justificado general; III–IV exigen regla CSS acotada que también
      # alcanza sus anexos. El gate de navegador comprueba el estilo efectivo.
      has_justify_css = body.match?(/text-align\s*:\s*justify/i)
      has_justify_kramdown = body.include?("{: .text-justify}")
      stylesheet = File.join(root, "assets/css/main.scss")
      thesis_post = THESIS_JUSTIFIED_REFS.include?(front["ref"])
      has_scoped_justify = thesis_post &&
        (%w[thesis-extension-post post3-evidence] - Array(front["classes"])).empty? &&
        File.file?(stylesheet) && scoped_thesis_justification?(File.read(stylesheet))
      if thesis_post && !has_scoped_justify
        errors << "layout: thesis III–IV require scoped paragraph justification and hyphens: auto"
      elsif !thesis_post && !(has_justify_css || has_justify_kramdown)
        errors << "layout: missing text justification (add text-align: justify in CSS or {: .text-justify})"
      end

      # 5d. Sección de Referencias y enlaces verificables en cada entrada
      ref_match = body.match(/^##\s+(Referencias|References)\b(.*)\z/im)
      if ref_match.nil?
        errors << "references: missing '## Referencias' or '## References' section"
      else
        ref_section = ref_match[2].gsub(/<style\b[^>]*>.*?<\/style>/im, "")
        # Desde el 2026-10-31 las entradas pueden ser notas kramdown `[^clave]: …`.
        ref_items = ref_section.lines.map(&:strip).select { |l| l.start_with?("- ") || l.match?(/\A\[\^[^\]]+\]:\s+\S/) || l.match?(/\A[A-ZÁÉÍÓÚÑÜ][a-záéíóúñüA-Z-]+,\s+.*\b(1[789]\d{2}|20\d{2})\b/) }
        if ref_items.empty?
          errors << "references: section '## Referencias' has no bibliography entries"
        else
          ref_items.each do |item|
            unless item.match?(%r{https?://[^\s)>]+})
              errors << "references: entry missing verifiable URL/DOI link: #{item[0, 80]}"
            end
          end
        end
      end
    end

    # 6. Imágenes y videos locales en el cuerpo: existencia + width/height/alt/poster
    body.scan(/<img\b[^>]*>/i).each do |img_tag|
      attrs = HeroDisclosureCheck.attributes(img_tag)
      src = clean_liquid_url(attrs["src"])
      next unless src.start_with?("/assets/")

      disk_path = File.join(root, src.delete_prefix("/"))
      errors << "image missing on disk: #{src}" unless File.file?(disk_path)
      errors << "image missing width/height attributes: #{src}" if attrs["width"].to_s.strip.empty? || attrs["height"].to_s.strip.empty?
      errors << "image missing alt text: #{src}" if attrs["alt"].to_s.strip.empty?
    end

    body.scan(/<video\b[^>]*>.*?<\/video>/im).each do |video_block|
      open_tag = video_block[/\A<video\b[^>]*>/i].to_s
      attrs = HeroDisclosureCheck.attributes(open_tag)
      poster = clean_liquid_url(attrs["poster"])
      errors << "video missing width/height attributes" if attrs["width"].to_s.strip.empty? || attrs["height"].to_s.strip.empty?
      errors << "video missing poster attribute" if poster.empty?
      if poster.start_with?("/assets/")
        disk_poster = File.join(root, poster.delete_prefix("/"))
        errors << "video poster missing on disk: #{poster}" unless File.file?(disk_poster)
      end
      video_block.scan(/<source\b[^>]*>/i).each do |src_tag|
        sattrs = HeroDisclosureCheck.attributes(src_tag)
        vsrc = clean_liquid_url(sattrs["src"])
        next unless vsrc.start_with?("/assets/")

        disk_vsrc = File.join(root, vsrc.delete_prefix("/"))
        errors << "video source missing on disk: #{vsrc}" unless File.file?(disk_vsrc)
      end
    end

    # 7. Enlaces internos en Markdown: verificar que apunten a permalinks o archivos reales
    permalinks = known_permalinks(root)
    narrative.scan(/\]\((\{\{\s*['"][^'"]+['"]\s*\|\s*relative_url\s*\}\}|\/[^)\s]+)\)/).flatten.each do |raw_target|
      target = clean_liquid_url(raw_target).sub(/[?#].*\z/, "")
      next unless target.start_with?("/")
      next if target.start_with?("/assets/")

      normalized = target.end_with?("/") ? target : "#{target}/"
      disk_candidate = File.join(root, target.delete_prefix("/"))
      unless permalinks.key?(normalized) || permalinks.key?(target) || File.exist?(disk_candidate)
        errors << "internal link target not found in site permalinks: #{target}"
      end
    end

    # 8. En modo producción (_posts/), verificar hero WebP, paridad bilingüe ES/EN y _data/visuales/<visual_id>.yml
    if mode == :production
      errors.concat(HeroDisclosureCheck.source_errors(front, root))

      if check_bilingual_pair && path.to_s.include?("/_posts/")
        ref = front["ref"].to_s.strip
        lang = front["lang"].to_s.strip
        other_lang = lang == "es" ? "en" : "es"
        pair_found = Dir.glob(File.join(root, "_posts", "*.md")).any? do |pfile|
          next false if File.expand_path(pfile) == File.expand_path(path)

          pfront, _, perrs = split_front_matter(File.read(pfile))
          perrs.empty? && pfront.is_a?(Hash) && pfront["ref"].to_s.strip == ref && pfront["lang"].to_s.strip == other_lang
        end
        unless pair_found
          errors << "bilingual parity: missing '#{other_lang}' counterpart in _posts/ with ref: #{ref} (required by verify_hero_disclosure.rb hreflang check)"
        end
      end
    end

    errors
  end

  def bad_fixture_markdown
    <<~MD
      ---
      layout: single
      title: "Título con «comillas angulares» prohibidas"
      subtitle: "Subtítulo de prueba"
      date: 2026-10-31 11:00:00 -0300
      categories: [ia-herramientas]
      tags: [cpu]
      author: "Ende"
      mathjax: true
      excerpt: "En este experimento nosotros probamos un comité."
      ---

      En este post nosotros medimos $p > 0,5$ sin justificar ni referencias y enlazamos a [ruta rota](/ruta/inexistente/parte-3/).
    MD
  end

  def run_fixture_red(root)
    bad_errors = audit_content(bad_fixture_markdown, root: root, path: "_drafts/2026-10-31-bad.md", mode: :draft_ready)
    warn "FAIL [fixture-red]: #{bad_errors.size} violation(s) caught as expected:"
    bad_errors.each { |e| warn "  - #{e}" }
    !bad_errors.empty?
  end

  def run_fixture_self_test(root)
    bad_errors = audit_content(bad_fixture_markdown, root: root, path: "_drafts/2026-10-31-bad.md", mode: :draft_ready)
    expected_substring_checks = [
      "frontmatter.description: missing or empty",
      "frontmatter.author: 'Ende' not found in _data/authors.yml",
      "frontmatter.author_profile: must be true",
      "frontmatter.mathjax: true is forbidden",
      "editorial: angular quotes (« ») are forbidden",
      "editorial: first-person plural pronoun",
      "layout: missing text justification",
      "references: missing '## Referencias' or '## References' section",
      "internal link target not found in site permalinks: /ruta/inexistente/parte-3/"
    ]

    missing_detections = expected_substring_checks.reject do |needle|
      bad_errors.any? { |err| err.include?(needle) }
    end

    unless missing_detections.empty?
      warn "FAIL [canary-red]: fixture did not trigger expected errors: #{missing_detections.join('; ')}"
      warn "Actual errors: #{bad_errors.inspect}"
      return false
    end

    good_md = <<~MD
      ---
      layout: single
      title: "Título válido con comillas dobles"
      subtitle: "Subtítulo válido en primera persona"
      date: 2026-10-31 11:00:00 -0300
      categories: [ia-herramientas]
      tags: [cpu]
      description: "Descripción breve y válida para SEO y redes sociales."
      excerpt: "En este experimento probé un clasificador en mi portátil."
      author: clabra
      author_profile: true
      lang: es
      ref: fixture-valido
      permalink: /ia-herramientas/fixture-valido/
      toc: true
      math: false
      ai_disclosure:
        level: some_ai
        components:
          text: assisted
      ---

      <style>
      .page__content > p { text-align: justify; }
      </style>

      En este experimento probé un clasificador con <code>p &gt; 0,5</code> en mi portátil.

      ## Referencias

      - Condorcet. 1785. [*Essai sur l'application de l'analyse*](https://archive.org/details/essaisurlapplica00cond). https://archive.org/details/essaisurlapplica00cond.
    MD

    good_errors = audit_content(good_md, root: root, path: "_drafts/2026-10-31-good.md", mode: :draft_ready)
    unless good_errors.empty?
      warn "FAIL [canary-green]: valid fixture produced unexpected errors: #{good_errors.inspect}"
      return false
    end

    stylesheet = File.read(File.join(root, "assets/css/main.scss"))
    altered = stylesheet.sub(
      /(\.thesis-extension-post\.post3-evidence\s+\.page__content\s+p\s*\{\s*text-align:\s*)justify;/,
      '\\1start;'
    )
    unless scoped_thesis_justification?(stylesheet) && altered != stylesheet &&
        !scoped_thesis_justification?(altered)
      warn "FAIL [canary-thesis-justify]: scoped CSS mutation did not turn the guard red"
      return false
    end

    puts "CANARY OK (red=9 violations caught + scoped CSS mutation, green=0 errors)"
    true
  end
end

if $PROGRAM_NAME == __FILE__ || File.basename($PROGRAM_NAME) == "verify_post_publication_readiness.rb"
  root = File.expand_path("..", __dir__)
  args = ARGV.dup

  if args.delete("--fixture-red")
    DraftPromotionCheck.run_fixture_red(root)
    exit 1
  end

  if args.delete("--fixture")
    exit(DraftPromotionCheck.run_fixture_self_test(root) ? 0 : 1)
  end

  explicit_mode = nil
  explicit_mode = :draft_ready if args.delete("--draft-ready")
  explicit_mode = :production if args.delete("--production")

  targets = args.empty? ? [File.join(root, "_posts/2026-10-31-multiagente-penta-agent-autopoiesis-parte-iv.md")] : args
  failures = 0

  targets.each do |target|
    full_path = File.expand_path(target, root)
    unless File.file?(full_path)
      warn "#{target}: file not found"
      failures += 1
      next
    end

    mode = explicit_mode || (full_path.include?("/_posts/") ? :production : :draft_ready)
    errs = DraftPromotionCheck.audit_content(File.read(full_path), root: root, path: full_path, mode: mode)
    if errs.empty?
      puts "OK [#{mode}]: #{File.basename(full_path)}"
    else
      warn "FAIL [#{mode}]: #{File.basename(full_path)}"
      errs.each { |e| warn "  - #{e}" }
      failures += 1
    end
  end

  exit(failures.zero? ? 0 : 1)
end
