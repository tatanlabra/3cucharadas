#!/usr/bin/env ruby
# frozen_string_literal: true

require "find"
require "json"
require "open3"
require "optparse"
require "pathname"
require "set"
require "yaml"

options = {
  root: Pathname.pwd,
  config: nil,
  strict: false,
  strict_local: false
}

OptionParser.new do |parser|
  parser.banner = "Usage: verify_repo_governance.rb [options]"
  parser.on("--root PATH") { |value| options[:root] = Pathname(value) }
  parser.on("--config PATH") { |value| options[:config] = Pathname(value) }
  parser.on("--strict") { options[:strict] = true }
  parser.on("--strict-local") do
    options[:strict] = true
    options[:strict_local] = true
  end
end.parse!

root = options[:root].expand_path
config_path = (options[:config] || root.join("docs/contracts/repo-governance.yaml")).expand_path

def git!(root, *arguments)
  output, status = Open3.capture2e("git", "-C", root.to_s, *arguments)
  raise "git #{arguments.join(' ')} falló: #{output.strip}" unless status.success?

  output
end

def tree_stats(path)
  bytes = 0
  entries = 0
  Find.find(path.to_s) do |entry|
    next if entry == path.to_s

    stat = File.lstat(entry)
    entries += 1
    bytes += stat.size unless stat.directory?
  rescue Errno::ENOENT
    next
  end
  { "path" => path.to_s, "bytes" => bytes, "entries" => entries }
end

config = YAML.safe_load(config_path.read, permitted_classes: [], aliases: false)
required = %w[limits forbidden_worktree_roots tracked_forbidden_patterns local_residue_paths owned_large_files falsified_by]
missing = required.reject { |key| config.key?(key) }
raise "Contrato incompleto: faltan #{missing.join(', ')}" unless missing.empty?
raise "Contrato vacuo: owned_large_files no puede estar vacío" if config.fetch("owned_large_files").empty?
raise "Contrato vacuo: falsified_by no puede estar vacío" if config.fetch("falsified_by").empty?
owner_fields = %w[owner role retention]
invalid_owners = config.fetch("owned_large_files").filter_map do |path, metadata|
  path unless metadata.is_a?(Hash) && owner_fields.all? { |field| metadata[field].to_s.strip != "" }
end
raise "Dueños incompletos para: #{invalid_owners.join(', ')}" unless invalid_owners.empty?

limits = config.fetch("limits")
tracked = git!(root, "ls-files", "-z").split("\0").reject(&:empty?)
tracked_rows = tracked.filter_map do |relative|
  path = root.join(relative)
  next unless path.exist? || path.symlink?

  { "path" => relative, "bytes" => path.lstat.size }
end

review_bytes = Integer(limits.fetch("github_large_object_review_bytes"))
hard_bytes = Integer(limits.fetch("github_single_object_enforced_bytes"))
large_rows = tracked_rows.select { |row| row.fetch("bytes") > review_bytes }.sort_by { |row| -row.fetch("bytes") }
owners = config.fetch("owned_large_files")
unowned_large = large_rows.reject { |row| owners.key?(row.fetch("path")) }
oversized = tracked_rows.select { |row| row.fetch("bytes") > hard_bytes }

flags = File::FNM_PATHNAME | File::FNM_EXTGLOB
tracked_forbidden = tracked.select do |relative|
  config.fetch("tracked_forbidden_patterns").any? { |pattern| File.fnmatch?(pattern, relative, flags) }
end

nested_git = []
Find.find(root.to_s) do |entry|
  path = Pathname(entry)
  if path == root.join(".git")
    Find.prune if path.directory?
    next
  end
  if path.basename.to_s == ".git"
    nested_git << path.relative_path_from(root).to_s
    Find.prune if path.directory?
    next
  end
  Find.prune if path.directory? && path.basename.to_s == "node_modules"
end

forbidden_roots = config.fetch("forbidden_worktree_roots").filter_map do |relative|
  path = root.join(relative)
  next unless path.exist? && (path.file? || path.children.any?)

  relative
end

local_residue = config.fetch("local_residue_paths").flat_map do |pattern|
  Dir.glob(root.join(pattern).to_s, File::FNM_EXTGLOB).sort
end.uniq.map { |path| tree_stats(Pathname(path)) }

children = Hash.new { |hash, key| hash[key] = Set.new }
max_depth = 0
tracked.each do |relative|
  parts = relative.split("/")
  max_depth = [max_depth, parts.length].max
  parts.each_index do |index|
    parent = parts[0...index].join("/")
    children[parent] << parts[index]
  end
end
widest_dir, widest_entries = children.max_by { |_directory, entries| entries.length } || ["", Set.new]

violations = []
violations << { "type" => "unowned_large_file", "paths" => unowned_large.map { |row| row.fetch("path") } } unless unowned_large.empty?
violations << { "type" => "github_single_object_limit", "paths" => oversized.map { |row| row.fetch("path") } } unless oversized.empty?
violations << { "type" => "tracked_generated_path", "paths" => tracked_forbidden } unless tracked_forbidden.empty?
violations << { "type" => "nested_git_metadata", "paths" => nested_git } unless nested_git.empty?
violations << { "type" => "forbidden_worktree_root", "paths" => forbidden_roots } unless forbidden_roots.empty?
if widest_entries.length > Integer(limits.fetch("github_directory_entries_recommended"))
  violations << { "type" => "directory_width", "path" => widest_dir, "entries" => widest_entries.length }
end
if max_depth > Integer(limits.fetch("github_directory_depth_recommended"))
  violations << { "type" => "directory_depth", "depth" => max_depth }
end
if options[:strict_local] && !local_residue.empty?
  violations << { "type" => "local_residue", "paths" => local_residue.map { |row| row.fetch("path") } }
end

count_objects = git!(root, "count-objects", "-v").lines.to_h do |line|
  key, value = line.strip.split(": ", 2)
  [key, value]
end
git_store_bytes = (Integer(count_objects.fetch("size", "0")) + Integer(count_objects.fetch("size-pack", "0"))) * 1024
git_store_limit = [
  Integer(limits.fetch("github_repository_ondisk_recommended_bytes")),
  Integer(limits.fetch("gitlab_repository_bytes"))
].min
if git_store_bytes > git_store_limit
  violations << { "type" => "git_object_store_limit", "bytes" => git_store_bytes, "limit" => git_store_limit }
end
worktrees = git!(root, "worktree", "list", "--porcelain").lines.filter_map do |line|
  line.delete_prefix("worktree ").strip if line.start_with?("worktree ")
end

report = {
  "schema_version" => 1,
  "status" => violations.empty? ? "pass" : "fail",
  "root" => root.to_s,
  "contract" => config_path.relative_path_from(root).to_s,
  "tracked" => {
    "entries" => tracked_rows.length,
    "worktree_bytes" => tracked_rows.sum { |row| row.fetch("bytes") },
    "large_review_threshold_bytes" => review_bytes,
    "large_files" => large_rows,
    "widest_directory" => widest_dir,
    "widest_directory_entries" => widest_entries.length,
    "maximum_depth" => max_depth
  },
  "git_object_store" => count_objects.merge("bytes" => git_store_bytes, "limit_bytes" => git_store_limit),
  "worktrees" => worktrees,
  "local_residue" => local_residue,
  "violations" => violations
}

puts JSON.pretty_generate(report)
exit(options[:strict] && !violations.empty? ? 1 : 0)
