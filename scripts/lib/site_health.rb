# frozen_string_literal: true
require 'yaml'
require 'json'
require 'cgi'
require 'digest'

module SiteHealth
  PROFILES = %w[source local release].freeze
  PHASES = %w[F0 F1 F2 F3 F4 F5 F6].freeze
  def self.validate_contract(contract)
    raise 'invalid contract version' unless contract['version'] == 1
    raise 'empty invariants' unless contract['invariants'].is_a?(Array) && !contract['invariants'].empty?
    phases = contract.fetch('phases')
    raise 'incomplete phases' unless phases.map { |phase| phase['id'] } == PHASES
    phases.each do |phase|
      %w[objective invariants entry_gate exit_gate evidence falsified_by rollback].each do |field|
        raise "#{phase['id']}: empty #{field}" if Array(phase[field]).empty? || Array(phase[field]).any? { |v| v.to_s.strip.empty? }
      end
    end
    contract
  end

  def self.runtime_violations(root, contract)
    expected = contract.fetch('runtime')
    node = File.read(File.join(root, '.nvmrc')).strip
    package = JSON.parse(File.read(File.join(root, 'package.json')))
    lock = JSON.parse(File.read(File.join(root, 'package-lock.json')))
    ci = YAML.safe_load_file(File.join(root, '.gitlab-ci.yml'), aliases: true)
    gem_lock = File.read(File.join(root, 'Gemfile.lock'))
    errors = []
    errors << 'node .nvmrc/contract drift' unless node == expected.fetch('node')
    errors << 'node CI drift' unless ci.fetch('variables').fetch('NODE_VERSION') == node
    wanted = ">=#{node.split('.').first} <#{node.split('.').first.to_i + 1}"
    errors << 'node engines drift' unless package.dig('engines', 'node') == wanted
    errors << 'node lock engines drift' unless lock.dig('packages', '', 'engines', 'node') == wanted
    errors << 'bundler lock drift' unless gem_lock.match?(/BUNDLED WITH\s+#{Regexp.escape(expected.fetch('bundler'))}\s*\z/)
    install = ci.fetch('build_site').fetch('script').grep(String).find { |cmd| cmd.start_with?('gem install bundler') }
    errors << 'bundler CI drift' unless install == "gem install bundler -v #{expected.fetch('bundler')} -N"
    errors
  end

  def self.validate_workflows(root)
    files = Dir.glob(File.join(root, '.github/workflows/*.{yml,yaml}'))
    raise 'empty workflow inventory' if files.empty?
    files.each do |file|
      workflow = YAML.safe_load_file(file, aliases: true)
      raise "invalid workflow: #{file}" unless workflow.is_a?(Hash) && workflow['jobs'].is_a?(Hash) && !workflow['jobs'].empty?
    end
    files.length
  end

  def self.public_css_url(html)
    matches = html.scan(/href=["'](\/assets\/css\/main\.css(?:\?[^"'<>]*)?)["']/).flatten.uniq
    raise 'missing or ambiguous public stylesheet' unless matches.one?
    'https://3cucharadas.cl' + CGI.unescapeHTML(matches.first)
  end

  def self.catastro_asset_urls(html, root)
    %w[style.css app.js].to_h do |asset|
      matches = html.scan(/(?:href|src)=["'](#{Regexp.escape(asset)}(?:\?[^"'<>]*)?)["']/).flatten
      digest = Digest::SHA256.file(File.join(root, 'catastro_sii_brecha', asset)).hexdigest
      raise "missing, ambiguous or stale Catastro asset: #{asset}" unless matches == ["#{asset}?v=#{digest}"]
      [asset, 'https://3cucharadas.cl/catastro_sii_brecha/' + matches.first]
    end
  end
end
