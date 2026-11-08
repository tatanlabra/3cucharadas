#!/usr/bin/env ruby
# frozen_string_literal: true

# Compatibility entry point for source-health and CI. Both series share one
# source-bound scientific contract; language-only mode cannot bypass it.
require "open3"
require "pathname"
root = Pathname(__dir__).parent
args = ARGV.dup
contract = nil
lang = nil
until args.empty?
  flag = args.shift
  value = args.shift
  unless %w[--contract --lang].include?(flag) && value
    warn "POST3_USAGE_ERROR: invalid argument #{flag}"
    exit 2
  end
  flag == "--contract" ? contract = value : lang = value
end
unless lang.nil? || %w[es en].include?(lang)
  warn "POST3_USAGE_ERROR: invalid language #{lang}"
  exit 2
end
command = ["python3", root.join("scripts/verify_thesis_scientific_reset.py").to_s, "--root", root.to_s]
command.concat(["--contract", contract]) if contract
output, status = Open3.capture2e({"PYTHONDONTWRITEBYTECODE" => "1"}, *command, chdir: root.to_s)
if status.success?
  puts "POST3_VALID scientific_reset_v2 lang=#{lang || 'both'}"
else
  warn "POST3_INVALID: #{output.strip}"
end
exit(status.exitstatus || 1)
