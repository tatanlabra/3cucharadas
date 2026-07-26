# frozen_string_literal: true

require "cgi"

# Fase 3 (auditoria-2026-07-25): agrega licencia CC BY 4.0 al feed principal
# (site.feed / /feed.xml y /en/feed.xml) — a nivel de <feed> y por <entry> —
# más un footer con la URL canónica dentro del propio HTML del <content>,
# para que viaje con el texto si un agregador republica solo eso sin
# conservar los metadatos Atom. Es una decisión consciente frente a
# mantener el feed completo (ver auditoría §9): compensa exposición a
# raspadores con atribución explícita.
#
# No reemplaza el generador de jekyll-feed ni el hook de este mismo
# directorio (localized_feed_metadata.rb): opera igual que él, como hook
# `:pages, :post_render` sobre el HTML ya renderizado, para no reimplementar
# el paso doble de jekyll-polyglot (una pasada por idioma). Es idempotente
# frente al orden de ejecución entre ambos hooks: recalcula la URL
# localizada de cada entrada con `LocalizedFeedMetadata.localized_path` en
# vez de asumir que el otro hook ya corrió antes.
module FeedLicenseFooter
  module_function

  LICENSE_URL_ES = "https://creativecommons.org/licenses/by/4.0/deed.es"
  LICENSE_URL_EN = "https://creativecommons.org/licenses/by/4.0/"
  RIGHTS_TEXT = "CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/"

  def add_feed_rights(xml)
    return xml if xml =~ %r{</subtitle>.*?<rights>}m

    xml.sub(%r{(</subtitle>)}, "\\1<rights>#{CGI.escapeHTML(RIGHTS_TEXT)}</rights>")
  end

  def footer_html(url, lang)
    if lang == "en"
      %(<hr /><p>Originally published at <a href="#{url}">#{url}</a>. ) +
        %(Licensed under <a href="#{LICENSE_URL_EN}">CC BY 4.0</a>.</p>)
    else
      %(<hr /><p>Publicado originalmente en <a href="#{url}">#{url}</a>. ) +
        %(Licencia <a href="#{LICENSE_URL_ES}">CC BY 4.0</a>.</p>)
    end
  end

  def canonical_entry_url(entry, lang, default_lang, site)
    href_match = entry.match(%r{<link href="([^"]+)" rel="alternate" type="text/html"})
    return nil unless href_match

    root = LocalizedFeedMetadata.root(site)
    href = CGI.unescapeHTML(href_match[1])
    path = href.start_with?(root) ? href.delete_prefix(root) : href
    "#{root}#{LocalizedFeedMetadata.localized_path(path, lang, default_lang)}"
  end

  def add_entry_extras(xml, default_lang, site)
    xml.gsub(%r{<entry\b.*?</entry>}m) do |entry|
      next entry if entry.include?("<rights>")

      lang_match = entry.match(/xml:lang="([^"]+)"/)
      lang = lang_match ? lang_match[1] : default_lang
      entry = entry.sub(%r{(</id>)}, "\\1<rights>#{CGI.escapeHTML(RIGHTS_TEXT)}</rights>")

      url = canonical_entry_url(entry, lang, default_lang, site)
      if url && entry.include?("]]></content>")
        footer = footer_html(url, lang)
        entry = entry.sub("]]></content>", "#{footer}]]></content>")
      end
      entry
    end
  end

  def rewrite(page)
    default_lang = page.site.config.fetch("default_lang", "es")
    xml = page.output.dup
    xml = add_feed_rights(xml)
    xml = add_entry_extras(xml, default_lang, page.site)
    page.output = xml
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  next unless page.output&.include?('<feed xmlns="http://www.w3.org/2005/Atom"')

  FeedLicenseFooter.rewrite(page)
end
