#!/usr/bin/env ruby
# frozen_string_literal: true

# Fase 4.4 (archivo/handoffs/difusion/HANDOFF-2026-07-25-distribucion-3cucharadas.md):
# gate previo a distribuir un post externamente. Falla el build antes que la
# difusión, no después. Revisa, por cada post ES/EN construido:
#   - imagen social (og:image) real >= 1200px de ancho
#   - description presente y no vacía
#   - canónico único y absoluto
#   - enlaces internos del post resuelven a archivos reales del artefacto
#
# Sin dependencias nuevas: parsea encabezados WebP/PNG/JPEG a mano (misma
# filosofía que verify_site_artifact.rb, solo stdlib de Ruby). Ese parser vive
# ahora en scripts/lib/image_dimensions.rb, compartido con verify_visual_assets.rb.

require "cgi"
require_relative "lib/image_dimensions"

site_dir = File.expand_path(ARGV.fetch(0, "public"))
abort "Artifact directory does not exist: #{site_dir}" unless Dir.exist?(site_dir)

MIN_OG_IMAGE_WIDTH = 1200

def extract_meta(body, name)
  match = body.match(/<meta\s+name="#{Regexp.escape(name)}"\s+content="([^"]*)"/i) ||
          body.match(/<meta\s+content="([^"]*)"\s+name="#{Regexp.escape(name)}"/i)
  match && CGI.unescapeHTML(match[1])
end

def extract_og(body, property)
  match = body.match(/<meta\s+property="#{Regexp.escape(property)}"\s+content="([^"]*)"/i)
  match && CGI.unescapeHTML(match[1])
end

post_pages = Dir.glob(File.join(site_dir, "**", "index.html")).select do |path|
  relative = path.delete_prefix("#{site_dir}/")
  # Solo posts reales: excluye home, listados, tags/categorías y microsites ajenos.
  next false if relative == "index.html" || relative == "en/index.html"
  next false if relative.match?(%r{\A(en/)?(tags|categories|year-archive|search|sitemap|about)/})
  next false if relative.start_with?("catastro_sii_brecha/")

  body = File.read(path)
  body.include?('itemprop="datePublished"')
end

abort "No se encontraron páginas de post en #{site_dir}" if post_pages.empty?

failures = []

post_pages.each do |path|
  relative = path.delete_prefix("#{site_dir}/")
  body = File.read(path)

  # 1) Imagen social real >= 1200px de ancho.
  og_image = extract_og(body, "og:image")
  if og_image.nil? || og_image.empty?
    failures << "#{relative}: sin og:image"
  else
    image_relative = og_image.sub(%r{\Ahttps://3cucharadas\.cl}, "").sub(%r{\A/en(?=/)}, "").delete_prefix("/")
    image_path = File.join(site_dir, image_relative)
    width = image_width(image_path)
    if width.nil?
      failures << "#{relative}: no se pudo leer el ancho de #{image_relative} (og:image)"
    elsif width < MIN_OG_IMAGE_WIDTH
      failures << "#{relative}: og:image #{image_relative} tiene #{width}px, mínimo #{MIN_OG_IMAGE_WIDTH}px"
    end
  end

  # 2) description presente y no vacía.
  description = extract_meta(body, "description") || extract_og(body, "og:description")
  failures << "#{relative}: sin description" if description.nil? || description.strip.empty?

  # 3) Canónico único y absoluto.
  canonicals = body.scan(/<link\s+rel="canonical"\s+href="([^"]+)"/i).flatten
  if canonicals.empty?
    failures << "#{relative}: sin canonical"
  elsif canonicals.length > 1
    failures << "#{relative}: #{canonicals.length} canonicals duplicados"
  elsif !canonicals.first.start_with?("https://3cucharadas.cl/")
    failures << "#{relative}: canonical no es absoluto (#{canonicals.first})"
  end

  # 4) Enlaces internos del post resuelven a archivos reales.
  body.scan(/<a\s+[^>]*href="([^"]+)"/i).flatten.each do |raw_href|
    href = CGI.unescapeHTML(raw_href)
    href = href.sub(%r{\Ahttps://3cucharadas\.cl}, "")
    next unless href.start_with?("/")
    next if href.start_with?("//")

    target = href.split(/[?#]/, 2).first
    next if target.nil? || target.empty?

    target_path = File.join(site_dir, target.delete_prefix("/"))
    target_path = File.join(target_path, "index.html") if target.end_with?("/")
    failures << "#{relative}: enlace interno roto #{href}" unless File.file?(target_path) || File.file?("#{target_path}.html")
  end
end

unless failures.empty?
  failures.uniq.each { |f| warn "- #{f}" }
  abort "Gate de distribución falló (#{failures.uniq.length} problema(s) en #{post_pages.length} posts)"
end

puts "Gate de distribución OK: #{post_pages.length} posts verificados (imagen >=#{MIN_OG_IMAGE_WIDTH}px, description, canonical, enlaces internos)."
