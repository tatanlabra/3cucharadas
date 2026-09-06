# frozen_string_literal: true

# Polyglot prepares languages in Site#process, but Jekyll's doctor calls
# reset/read/generate directly. Prepare only the uninitialized case; ordinary
# multilingual builds have already prepared before reset and are unchanged.
Jekyll::Hooks.register :site, :after_reset do |site|
  if site.respond_to?(:prepare) && site.respond_to?(:languages) && site.languages.nil?
    site.prepare
  end
end
