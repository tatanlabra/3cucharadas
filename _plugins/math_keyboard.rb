# frozen_string_literal: true

# KaTeX display wrappers scroll horizontally on small screens. Give the
# generated wrapper a keyboard stop without rewriting MathML, TeX or feeds.
module MathKeyboard
  def self.decorate(html, lang)
    return html unless html.is_a?(String)
    label = lang.to_s.start_with?('en') ? 'Mathematical formula; horizontal scrolling' : 'Fórmula matemática; desplazamiento horizontal'
    html.gsub('<span class="katex-display">', %(<span class="katex-display" tabindex="0" role="region" aria-label="#{label}">))
  end
end

if defined?(Jekyll::Hooks)
  Jekyll::Hooks.register [:documents, :pages], :post_render do |document|
    document.output = MathKeyboard.decorate(document.output, document.data['lang'] || document.site.active_lang)
  end
end
