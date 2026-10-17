# frozen_string_literal: true

# Agrega srcset/sizes a las <img> cuyo src tiene variantes en _data/image_variants.json
# (C3, auditoría UX 2026-10-17). Las variantes las genera scripts/build_image_variants.py.
#
# Actúa sobre el HTML ya renderizado, así cubre por igual las figuras escritas a mano
# en los posts, el include `figure` y los carruseles, sin tocar el contenido. No toca
# una <img> que ya traiga srcset, ni el enlace de zoom (`a.image-popup`), que sigue
# apuntando al original. El contrato tests/test_ux_transversal_contract.py
# (imagenes-responsivas) reprueba si una figura declarada se publica sin su srcset.
module ResponsiveImages
  IMG = /<img\b[^>]*>/m.freeze

  def self.attribute(tag, name)
    tag[/\s#{name}="([^"]*)"/, 1]
  end

  def self.rewrite(html, data, baseurl)
    images = data["images"] || {}
    return html if images.empty?

    html.gsub(IMG) do |tag|
      next tag if tag.include?(" srcset=")

      src = attribute(tag, "src").to_s.sub(/\A#{Regexp.escape(baseurl)}/, "").sub(/\?.*\z/, "")
      entry = images[src]
      next tag unless entry

      candidates = entry["variants"].map { |v| "#{baseurl}#{v['src']} #{v['w']}w" }
      candidates << "#{baseurl}#{src} #{entry['w']}w"
      tag.sub(/<img\b/, %(<img srcset="#{candidates.join(', ')}" sizes="#{data['sizes']}"))
    end
  end
end

Jekyll::Hooks.register [:posts, :pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  data = doc.site.data["image_variants"]
  next unless data

  doc.output = ResponsiveImages.rewrite(doc.output, data, doc.site.config["baseurl"].to_s)
end
