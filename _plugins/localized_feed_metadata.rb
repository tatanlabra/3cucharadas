# frozen_string_literal: true

require "cgi"

# jekyll-feed usa site.lang y page.url, pero jekyll-polyglot conserva esos
# valores globales al renderizar /en/feed.xml. Este hook corrige el contrato
# Atom con el idioma activo y reutiliza el enlace canónico ya localizado de
# cada entrada para su id y xml:base.
module LocalizedFeedMetadata
  module_function

  def root(site)
    "#{site.config.fetch("url")}#{site.config.fetch("baseurl", "")}".sub(%r{/$}, "")
  end

  def localized_path(path, lang, default_lang)
    normalized = "/#{path.to_s.sub(%r{^/}, "")}"
    return normalized if lang == default_lang || normalized.start_with?("/#{lang}/")

    "/#{lang}#{normalized}"
  end

  def rewrite_entries(xml, lang, default_lang, site_root)
    xml.gsub(%r{<entry\b.*?</entry>}m) do |entry|
      match = entry.match(%r{<link href="([^"]+)" rel="alternate" type="text/html"})
      next entry unless match

      href = match[1]
      if lang != default_lang && href.start_with?(site_root) && !href.start_with?("#{site_root}/#{lang}/")
        href = "#{site_root}#{localized_path(href.delete_prefix(site_root), lang, default_lang)}"
        entry = entry.sub(match[1], href)
      end
      escaped = CGI.escapeHTML(href)
      entry
        .sub(%r{<id>.*?</id>}m, "<id>#{escaped}</id>")
        .sub(/xml:base="[^"]*"/, "xml:base=\"#{escaped}\"")
    end
  end

  def rewrite(page)
    site = page.site
    lang = site.active_lang || site.config.fetch("default_lang", site.config.fetch("lang", "es"))
    default_lang = site.config.fetch("default_lang", "es")
    site_root = root(site)
    self_path = localized_path(page.url, lang, default_lang)
    self_url = "#{site_root}#{self_path}"
    home_path = lang == default_lang ? "/" : "/#{lang}/"
    home_url = "#{site_root}#{home_path}"
    description = site.data.dig("brand", lang, "description") || site.config["description"]

    xml = page.output.dup
    xml.sub!(/(<feed\b[^>]*\bxml:lang=")[^"]+("[^>]*>)/, "\\1#{lang}\\2")
    xml.sub!(%r{<link href="[^"]+" rel="self" type="application/atom\+xml"\s*/>},
             %(<link href="#{CGI.escapeHTML(self_url)}" rel="self" type="application/atom+xml" />))
    xml.sub!(%r{<link href="[^"]+" rel="alternate" type="text/html" hreflang="[^"]+"\s*/>},
             %(<link href="#{CGI.escapeHTML(home_url)}" rel="alternate" type="text/html" hreflang="#{lang}" />))
    xml.sub!(%r{<id>.*?</id>}m, "<id>#{CGI.escapeHTML(self_url)}</id>")
    xml.sub!(%r{<subtitle>.*?</subtitle>}m, "<subtitle>#{CGI.escapeHTML(description.to_s)}</subtitle>")
    page.output = rewrite_entries(xml, lang, default_lang, site_root)
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  next unless page.output&.include?('<feed xmlns="http://www.w3.org/2005/Atom"')

  LocalizedFeedMetadata.rewrite(page)
end
