# frozen_string_literal: true

require "minitest/autorun"
require "date"
require "digest"
require "open3"
require "tmpdir"
require "yaml"
require_relative "../scripts/jekyll_to_devto"

class JekyllToDevtoTest < Minitest::Test
  SITE_URL = "https://3cucharadas.cl"
  CANONICAL_URL = "#{SITE_URL}/en/example/"

  def transform(markdown, page: {})
    JekyllToDevto.transform(markdown, canonical_url: CANONICAL_URL, page: page).body
  end

  def test_absolutizes_relative_url_in_markdown_and_html
    source = <<~MARKDOWN
      [Post I]({{ '/first/' | relative_url }})
      [Relative]({{ 'relative/path/' | relative_url }})
      <a href="{{ '/map/' | relative_url }}">Map</a>
      <img src="{{ '/image.png' | relative_url }}"
           srcset="{{ '/small.png' | relative_url }} 640w, {{ '/large.png' | relative_url }} 1280w">
    MARKDOWN

    result = transform(source)

    assert_includes result, "[Post I](#{SITE_URL}/first/)"
    assert_includes result, "[Relative](#{SITE_URL}/relative/path/)"
    assert_includes result, %(href="#{SITE_URL}/map/")
    assert_includes result, %(src="#{SITE_URL}/image.png")
    assert_includes result, %(srcset="#{SITE_URL}/small.png 640w, #{SITE_URL}/large.png 1280w")
    refute_includes result, "relative_url"
  end

  # falsified_by: 2026-09-09. Con el codigo de HEAD (`git show HEAD:scripts/jekyll_to_devto.rb`)
  # este mismo cuerpo levanta `JekyllToDevto::TransformError: Liquid sin cierre cerca de:
  # "{% include figure popup=true image_path=..."`, porque `map_inline_code` partia la linea
  # por las comillas invertidas ANTES de que `transform_liquid` viera el tag, y le llegaba sin
  # su `%}`. Es lo que tumbo el job build_site del pipeline 2831523259 (2026-09-09 02:10) y el
  # workflow de dev.to 34302166528, sobre _posts/2026-07-15-ai-quota-hud-kde-en.md.
  def test_keeps_a_liquid_tag_whole_when_its_arguments_contain_inline_code
    source = <<~MARKDOWN
      {% include figure popup=true image_path="/assets/images/ai-quota-hud/tooltip-en.png" alt="Tooltip" caption="**Figure 2** — the `OFICIAL` badge next to the `LOCAL` one." %}
    MARKDOWN

    result = transform(source)

    assert_includes result, "![Tooltip](#{SITE_URL}/assets/images/ai-quota-hud/tooltip-en.png)"
    assert_includes result, "the `OFICIAL` badge next to the `LOCAL` one."
    refute_includes result, "{%"
    refute_includes result, "%}"
  end

  # falsified_by: 2026-09-09. Con el codigo de HEAD, `literal_block_start` usaba
  # /\{%[-]?\s*(katex|raw)\b[^%]*[-]?%\}/ y esa clase negada termina el tag en el primer `%`
  # de sus propios argumentos: el bloque no se detectaba y `{{ site.url }}` se expandia DENTRO
  # de un `raw`, que existe justo para impedirlo. Medido: antiguo -> "texto con
  # https://3cucharadas.cl literal"; nuevo -> "texto con {{ site.url }} literal".
  def test_detects_a_literal_block_whose_arguments_contain_a_percent_sign
    source = <<~MARKDOWN
      {% raw label="95% CI" %}
      texto con {{ site.url }} literal
      {% endraw %}
    MARKDOWN

    result = transform(source)

    assert_includes result, "texto con {{ site.url }} literal"
    refute_includes result, "texto con #{SITE_URL} literal"
  end

  def test_resolves_known_jekyll_variables_and_removes_unknown_outputs
    source = "{{ site.url }}{{ page.url }} {{ page.title }} {{ site.unknown }} {{ custom.value }}"
    result = transform(source, page: { "title" => "Example" })

    assert_equal "#{CANONICAL_URL} Example", result
  end

  def test_preserves_forem_liquid_and_code_literals
    source = <<~MARKDOWN
      {% embed https://example.com/demo %}
      {% link https://dev.to/example %}
      {% katex %} x^2 {% endkatex %}

      `{{ page.url | relative_url }}`

      ```liquid
      {{ site.url | relative_url }}
      {% include figure image_path="/literal.png" %}
      ```
    MARKDOWN

    assert_equal source.strip, transform(source)
  end

  def test_allowlist_keeps_required_and_generated_forem_tags
    required = %w[katex endkatex embed link youtube]

    assert_empty required - JekyllToDevto::FOREM_TAGS
    refute_includes JekyllToDevto::FOREM_TAGS, "include"
  end

  def test_converts_block_math_and_removes_kramdown_extensions
    source = <<~MARKDOWN
      $$
      x^2 + y^2 = z^2
      $$
      {: .text-justify}

      $$e^{i\\pi}+1=0$$
    MARKDOWN

    result = transform(source)

    assert_includes result, "{% katex %}\nx^2 + y^2 = z^2\n{% endkatex %}"
    assert_includes result, "{% katex %} e^{i\\pi}+1=0 {% endkatex %}"
    refute_includes result, "{: .text-justify}"
    refute_includes result, "$$"
  end

  def test_transforms_figure_include_even_when_caption_contains_percent
    source = <<~MARKDOWN
      {% include figure image_path="/chart.png" alt="Chart" caption="95% CI; marker %} quoted" %}
      {% include gallery caption="95% CI" %}
    MARKDOWN

    result = JekyllToDevto.transform(source, canonical_url: CANONICAL_URL)

    assert_includes result.body, "![Chart](#{SITE_URL}/chart.png)"
    assert_includes result.body, "95% CI; marker %} quoted"
    refute_includes result.body, "{% include"
    assert_includes result.warnings, "include Jekyll eliminado: gallery (sin id) no resuelta"
  end

  def test_final_validation_rejects_residual_liquid_outside_code
    error = assert_raises(JekyllToDevto::TransformError) do
      JekyllToDevto.validate!("Broken {{ page.url | relative_url }}")
    end

    assert_includes error.message, "relative_url"
    assert JekyllToDevto.validate!("`{{ page.url | relative_url }}`")
  end

  def test_rewrites_internal_svg_urls_to_explicit_devto_rasters
    source = <<~MARKDOWN
      <picture>
        <source srcset="/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.svg" type="image/svg+xml">
        <img src="/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en.svg" alt="Flow">
      </picture>
      [Full size](/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg)
    MARKDOWN

    result = transform(source)

    assert_includes result, "#{SITE_URL}/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp"
    assert_includes result, "#{SITE_URL}/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en-devto-1200x2172.png"
    assert_includes result, "#{SITE_URL}/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources-devto-1600x1169.png"
    assert_includes result, 'type="image/webp"'
    refute_match(/\.svg\b/i, result)
  end

  def test_fails_closed_when_an_internal_svg_has_no_raster_mapping
    error = assert_raises(JekyllToDevto::TransformError) do
      transform('<img src="/assets/images/missing-diagram.svg" alt="Missing">')
    end

    assert_includes error.message, "falta mapeo ráster DEV.to"
  end

  def test_final_validation_rejects_external_svg_references_outside_code
    error = assert_raises(JekyllToDevto::TransformError) do
      JekyllToDevto.validate!("![Diagram](https://example.com/diagram.svg)")
    end

    assert_includes error.message, "referencia SVG no portable"
    assert JekyllToDevto.validate!("`https://example.com/diagram.svg`")
  end

  def test_renders_devto_front_matter_as_an_explicit_publishable_draft
    document = JekyllToDevto.render_document(
      body: "Body",
      title: "Title",
      description: "Description",
      tags: %w[ruby jekyll],
      canonical_url: CANONICAL_URL,
      cover_image: "#{SITE_URL}/cover.png"
    )
    front = YAML.safe_load(document.split(/^---\s*$/, 3)[1])

    assert_equal CANONICAL_URL, front["canonical_url"]
    assert_equal false, front["published"]
    assert_equal "some_ai", front["ai_disclosure_level"]
    assert_equal "ruby, jekyll", front["tags"]
    assert_equal "#{SITE_URL}/cover.png", front["cover_image"]
  end

  def test_renders_remote_published_state_without_reverting_it
    document = JekyllToDevto.render_document(
      body: "Body",
      title: "Title",
      description: "Description",
      tags: %w[ruby jekyll],
      canonical_url: CANONICAL_URL,
      published: true,
      ai_disclosure_level: "no_ai"
    )
    front = YAML.safe_load(document.split(/^---\s*$/, 3)[1])

    assert_equal true, front["published"]
    assert_equal "no_ai", front["ai_disclosure_level"]
  end

  def test_rejects_more_than_four_tags_and_unknown_ai_disclosure
    error = assert_raises(JekyllToDevto::TransformError) do
      JekyllToDevto.render_document(
        body: "Body",
        title: "Title",
        description: "Description",
        tags: %w[one two three four five],
        canonical_url: CANONICAL_URL
      )
    end
    assert_includes error.message, "máximo 4 tags"

    error = assert_raises(JekyllToDevto::TransformError) do
      JekyllToDevto.render_document(
        body: "Body",
        title: "Title",
        description: "Description",
        tags: %w[one],
        canonical_url: CANONICAL_URL,
        ai_disclosure_level: "invented"
      )
    end
    assert_includes error.message, "ai_disclosure_level inválido"
  end

  def test_renders_forem_front_matter_as_single_line_quoted_scalars
    title = "Parser DEV: apostrophe's regression"
    description = "A long description: #{'portable text ' * 12}".strip
    document = JekyllToDevto.render_document(
      body: "Body",
      title: title,
      description: description,
      tags: %w[devto jekyll],
      canonical_url: CANONICAL_URL
    )
    front_text = document.split(/^---\s*$/, 3)[1]
    front = YAML.safe_load(front_text)

    assert_includes front_text, %(title: #{JSON.generate(title)})
    assert_includes front_text, %(description: #{JSON.generate(description)})
    refute_match(/^\s+portable text/, front_text)
    refute_match(/^[^:]+:\s*[>|]/, front_text)
    assert_equal title, front["title"]
    assert_equal description, front["description"]
  end

  def test_multiagent_post_ii_regression
    path = File.expand_path("../_posts/2026-07-23-multiagente-penta-agent-memoria-en.md", __dir__)
    source = File.read(path)
    front_text, body = source.split(/^---\s*$/, 3)[1, 2]
    front = YAML.safe_load(front_text, permitted_classes: [Date, Time])
    canonical_url = "#{SITE_URL}/en#{front.fetch('permalink')}"
    result = JekyllToDevto.transform(body, canonical_url: canonical_url, page: front).body

    assert_includes result, "[first post](#{SITE_URL}/ia/productividad/desarrollo/multiagente-penta-agent-modelos/)"
    assert_includes result, %(src="#{SITE_URL}/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en-devto-1200x2172.png")
    refute_match(/\.svg\b/i, result)
    refute_match(/\|\s*relative_url\b/, result)
    refute_match(/\{\{/, result)
    assert_includes result, "{% katex %}"
    assert_includes source, "relative_url"
    assert_equal source, File.read(path), "la transformación no debe reescribir el post canónico"
  end

  def test_casen_galleries_keep_all_six_images
    path = File.expand_path("../_posts/2026-03-15-casen2024-julia-waffles-politica-publica-en.md", __dir__)
    source = File.read(path)
    front_text, body = source.split(/^---\s*$/, 3)[1, 2]
    front = YAML.safe_load(front_text, permitted_classes: [Date, Time])
    canonical_url = "#{SITE_URL}/en#{front.fetch('permalink')}"
    result = JekyllToDevto.transform(body, canonical_url: canonical_url, page: front)

    gallery_paths = %w[
      waffle_educacion_educc.webp
      waffle_salud_s13.webp
      waffle_trabajo_ingresos_pobreza.webp
      regional_dotplot_educacion_educc.webp
      regional_dotplot_salud_s13.webp
      regional_dotplot_trabajo_ingresos_pobreza.webp
    ]
    gallery_paths.each do |filename|
      assert_includes result.body, "#{SITE_URL}/assets/images/casen2024-julia-waffles-politica-publica/#{filename}"
    end
    assert_empty result.warnings.grep(/gallery/)
    refute_includes result.body, "{% include gallery"
    assert_equal source, File.read(path), "la transformación no debe reescribir el post canónico"
  end

  def test_cli_exports_the_exact_derived_document_without_api_key
    path = File.expand_path("../_posts/2026-07-23-multiagente-penta-agent-memoria-en.md", __dir__)
    source = File.read(path)
    source_sha = Digest::SHA256.hexdigest(source)
    front_text, body = source.split(/^---\s*$/, 3)[1, 2]
    front = YAML.safe_load(front_text, permitted_classes: [Date, Time])
    canonical_url = "#{SITE_URL}/en#{front.fetch('permalink')}"
    slug = front.fetch("permalink").chomp("/").split("/").last
    tags = Array(front["devto_tags"] || front["tags"]).first(4).map do |tag|
      tag.to_s.downcase.gsub(/[^a-z0-9]/, "")
    end.reject(&:empty?)
    transformed = JekyllToDevto.transform(body, canonical_url: canonical_url, page: front)
    expected = JekyllToDevto.render_document(
      body: transformed.body,
      title: front.fetch("title"),
      description: front["description"],
      tags: tags,
      canonical_url: canonical_url,
      cover_image: JekyllToDevto.absolute_url(front.dig("header", "og_image"), SITE_URL, force_relative: true),
      published: false,
      ai_disclosure_level: "some_ai"
    )

    Dir.mktmpdir("devto-export") do |dir|
      script = File.expand_path("../scripts/syndicate_devto.rb", __dir__)
      stdout, stderr, status = Open3.capture3({ "DEV_TO_API_KEY" => nil }, "ruby", script, "--export-dir", dir)

      assert status.success?, "export falló: #{stdout}\n#{stderr}"
      assert_equal expected, File.read(File.join(dir, "#{slug}.md"))
      assert_equal 7, Dir.glob(File.join(dir, "*.md")).length
      Dir.glob(File.join(dir, "*.md")).each do |artifact|
        contents = File.read(artifact)
        front = YAML.safe_load(contents.split(/^---\s*$/, 3)[1])
        assert_equal false, front["published"], "published no explícito en #{File.basename(artifact)}"
        assert_equal "some_ai", front["ai_disclosure_level"], "AI disclosure ausente en #{File.basename(artifact)}"
        refute_match(/https?:\/\/[^\s"'<>)]*\.svg\b/i, contents, "SVG residual en #{File.basename(artifact)}")
      end
    end
    assert_equal source_sha, Digest::SHA256.file(path).hexdigest
  end
end
