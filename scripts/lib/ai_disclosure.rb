# frozen_string_literal: true
require 'uri'

# Canonical declaration for source checks and offline DEV exports. A global
# declaration never invents the component history or a human review.
module AiDisclosure
  LEVELS = %w[no_ai some_ai fully_autonomous not_disclosed].freeze
  COMPONENTS = {'text' => %w[assisted human generated unknown], 'hero' => %w[generated human unknown]}.freeze
  module_function

  def resolve(front)
    canonical = front['ai_disclosure']
    legacy = front['devto_ai_disclosure_level']
    if front.key?('ai_disclosure')
      raise ArgumentError, 'ai_disclosure must be a mapping with level' unless canonical.is_a?(Hash) && canonical.key?('level')
      level = canonical['level']
      if front.key?('devto_ai_disclosure_level') && legacy != level
        raise ArgumentError, 'ai_disclosure.level conflicts with devto_ai_disclosure_level'
      end
    else
      level = front.key?('devto_ai_disclosure_level') ? legacy : 'not_disclosed'
      canonical = {}
    end
    raise ArgumentError, "invalid ai_disclosure.level: #{level.inspect}" unless LEVELS.include?(level)
    components = canonical.fetch('components', {})
    raise ArgumentError, 'ai_disclosure.components must be a mapping' unless components.is_a?(Hash)
    raise ArgumentError, 'unknown disclosure component' unless (components.keys - COMPONENTS.keys).empty?
    normalized = COMPONENTS.to_h do |component, levels|
      value = components.fetch(component, 'unknown')
      raise ArgumentError, "invalid #{component}: #{value.inspect}" unless levels.include?(value)
      [component, value]
    end
    if level == 'no_ai' && normalized.values.any? { |v| %w[generated assisted].include?(v) }
      raise ArgumentError, 'no_ai contradicts AI component'
    end
    if level == 'fully_autonomous' && normalized.values.any? { |v| %w[human assisted].include?(v) }
      raise ArgumentError, 'fully_autonomous contradicts human component'
    end
    validate_public_link!(canonical['evidence_url']) if canonical.key?('evidence_url')
    {'level' => level, 'components' => normalized, 'explicit' => front.key?('ai_disclosure') || front.key?('devto_ai_disclosure_level')}
  end

  def validate_public_link!(value)
    uri = URI.parse(value.to_s)
    unless uri.is_a?(URI::HTTPS) && uri.host && !uri.userinfo && !uri.query
      raise ArgumentError, 'evidence_url must be a public HTTPS URL without credentials or query parameters'
    end
    true
  rescue URI::InvalidURIError
    raise ArgumentError, 'invalid evidence_url'
  end
end
