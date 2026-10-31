#!/usr/bin/env ruby
# frozen_string_literal: true

# Verifica los enlaces de uno o más posts de Jekyll.
#
# - Internos (/ruta/ o {{ '/ruta/' | relative_url }}): deben existir en el sitio
#   construido (--site, por defecto _site).
# - Externos (http/https): se consultan por red con --external. Un 404/410 o un
#   fallo de DNS es ROTO; un 401/403/429/5xx o un timeout es NO CONCLUYENTE,
#   nunca verde.
# - Repositorios de GitHub/GitLab/Codeberg: si el texto del enlace no comparte
#   ningún término con el nombre del repositorio, se marca NOMBRE_DISTINTO.
#
# Salida: 0 sin rotos; 1 con al menos un roto; 2 con --strict y algún no
# concluyente o nombre distinto. --json escribe el reporte completo.

require "cgi"
require "json"
require "net/http"
require "openssl"
require "optparse"
require "set"
require "uri"

class PostLinkChecker
  LINK_RE = /\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)/.freeze
  HREF_RE = /\b(?:href|src)="([^"]+)"/.freeze
  LIQUID_URL_RE = /\{\{\s*['"]([^'"]+)['"]\s*\|\s*(?:relative_url|absolute_url)\s*\}\}/.freeze
  CODE_HOSTS = %w[github.com gitlab.com codeberg.org].freeze
  INCONCLUSIVE_STATUS = [401, 403, 405, 408, 429].freeze

  Result = Struct.new(:file, :line, :text, :url, :kind, :status, :detail, keyword_init: true)

  def initialize(site:, external:, timeout:)
    @site = site
    @external = external
    @timeout = timeout
    @cache = {}
  end

  def check_files(paths)
    paths.flat_map { |path| check_file(path) }
  end

  def check_file(path)
    body = File.read(path, encoding: "UTF-8")
    front = body[/\A---\n.*?\n---\n/m].to_s
    offset = front.count("\n")
    body = body.delete_prefix(front) # front matter fuera, numeración intacta
    results = []
    in_fence = false
    body.each_line.with_index(offset + 1) do |line, number|
      in_fence = !in_fence if line.lstrip.start_with?("```")
      next if in_fence

      expanded = line.gsub(LIQUID_URL_RE) { Regexp.last_match(1) }
      seen = Set.new
      expanded.scan(LINK_RE) do |text, url|
        seen << url
        results << classify(path, number, text, url)
      end
      expanded.scan(HREF_RE) do |(url)|
        next if seen.include?(url)

        results << classify(path, number, "", url)
      end
    end
    results.compact
  end

  private

  def classify(file, line, text, raw_url)
    url = CGI.unescapeHTML(raw_url.strip)
    return nil if url.empty? || url.start_with?("#", "mailto:", "tel:", "data:", "{{")

    base = { file: file, line: line, text: text.strip, url: url }
    if url.start_with?("http://", "https://")
      external_result(base)
    elsif url.start_with?("/")
      internal_result(base)
    else
      Result.new(**base, kind: "relative", status: "NO_CONCLUYENTE", detail: "ruta relativa no resoluble")
    end
  end

  def internal_result(base)
    path = URI.decode_www_form_component(base[:url].split(/[?#]/).first)
    candidates = [path, File.join(path, "index.html"), "#{path.chomp('/')}.html"]
    found = candidates.any? { |candidate| File.file?(File.join(@site, candidate)) }
    status = found ? "OK" : "ROTO"
    Result.new(**base, kind: "internal", status: status, detail: found ? nil : "no existe en #{@site}")
  end

  def external_result(base)
    uri = URI.parse(base[:url])
    name_status = repository_name_status(uri, base[:text])
    unless @external
      return Result.new(**base, kind: "external", status: name_status || "NO_VERIFICADO",
                                detail: "sin --external")
    end

    status, detail = @cache[base[:url]] ||= fetch(uri)
    status = name_status if status == "OK" && name_status
    Result.new(**base, kind: "external", status: status, detail: detail)
  rescue URI::InvalidURIError => e
    Result.new(**base, kind: "external", status: "ROTO", detail: "URL inválida: #{e.message}")
  end

  def repository_name_status(uri, text)
    return nil unless CODE_HOSTS.include?(uri.host)

    segments = uri.path.split("/").reject(&:empty?)
    return nil if segments.length < 2 || text.to_s.strip.empty?

    repo_terms = terms(segments[1])
    text_terms = terms(text)
    return nil if repo_terms.empty? || text_terms.empty?

    shared = repo_terms & text_terms
    partial = repo_terms.any? { |r| text_terms.any? { |t| r.include?(t) || t.include?(r) } }
    shared.empty? && !partial ? "NOMBRE_DISTINTO" : nil
  end

  def terms(value)
    value.to_s.downcase.gsub(/[`*_]/, "").split(/[^a-z0-9]+/).reject { |t| t.length < 2 }
  end

  def fetch(uri, redirects = 5)
    response = request(uri, Net::HTTP::Head)
    response = request(uri, Net::HTTP::Get) if [403, 405, 501].include?(response.code.to_i)
    code = response.code.to_i
    if (300..399).cover?(code) && response["location"] && redirects.positive?
      return fetch(URI.join(uri.to_s, response["location"]), redirects - 1)
    end
    return ["OK", "HTTP #{code}"] if (200..299).cover?(code)
    return ["ROTO", "HTTP #{code}"] if [404, 410].include?(code)
    return ["NO_CONCLUYENTE", "HTTP #{code}"] if INCONCLUSIVE_STATUS.include?(code) || code >= 500

    ["NO_CONCLUYENTE", "HTTP #{code}"]
  rescue SocketError, Resolv::ResolvError => e
    ["ROTO", "DNS: #{e.class}"]
  rescue Net::OpenTimeout, Net::ReadTimeout, Errno::ECONNRESET, Errno::ECONNREFUSED,
         OpenSSL::SSL::SSLError, EOFError => e
    ["NO_CONCLUYENTE", e.class.name]
  end

  def request(uri, klass)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = uri.scheme == "https"
    http.open_timeout = @timeout
    http.read_timeout = @timeout
    req = klass.new(uri.request_uri)
    req["User-Agent"] = "3cucharadas-link-check/1.0 (+https://3cucharadas.cl)"
    req["Accept"] = "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8"
    http.request(req)
  end
end

options = { site: "_site", external: false, timeout: 15, strict: false, json: nil }
OptionParser.new do |opts|
  opts.banner = "uso: verify_post_links.rb [opciones] POST..."
  opts.on("--site DIR", "sitio construido para enlaces internos") { |v| options[:site] = v }
  opts.on("--external", "consultar enlaces externos por red") { options[:external] = true }
  opts.on("--timeout N", Integer, "timeout por petición") { |v| options[:timeout] = v }
  opts.on("--strict", "no concluyentes y nombres distintos salen 2") { options[:strict] = true }
  opts.on("--json PATH", "reporte JSON") { |v| options[:json] = v }
end.parse!

abort("uso: verify_post_links.rb [opciones] POST...") if ARGV.empty?
missing = ARGV.reject { |path| File.file?(path) }
abort("no existe: #{missing.join(', ')}") unless missing.empty?
abort("sitio no construido: #{options[:site]}") unless Dir.exist?(options[:site])

checker = PostLinkChecker.new(site: options[:site], external: options[:external], timeout: options[:timeout])
results = checker.check_files(ARGV)
abort("ningún enlace encontrado en #{ARGV.join(', ')}: el gate no comprobó nada") if results.empty?

counts = results.group_by(&:status).transform_values(&:size)
results.reject { |r| r.status == "OK" }.each do |r|
  puts "#{r.status}\t#{r.file}:#{r.line}\t#{r.url}\t#{r.detail}"
end
puts "RESUMEN #{results.size} enlaces: #{counts.sort.map { |k, v| "#{k}=#{v}" }.join(' ')}"
if options[:json]
  File.write(options[:json], JSON.pretty_generate(
    { "checked" => results.size, "counts" => counts, "results" => results.map(&:to_h) }
  ) + "\n")
end

exit 1 if counts.fetch("ROTO", 0).positive?
exit 2 if options[:strict] && (counts.keys - ["OK"]).any?
exit 0
