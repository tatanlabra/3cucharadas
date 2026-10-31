#!/usr/bin/env ruby
# frozen_string_literal: true

# Wrapper canónico hacia verify_draft_promotion.rb para mantener compatibilidad con
# invocaciones directas de verify_post_publication_readiness.rb.
load File.expand_path("verify_draft_promotion.rb", __dir__)
