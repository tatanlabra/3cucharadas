# frozen_string_literal: true

require "json"
require "minitest/autorun"
require "open3"
require "pathname"
require "tmpdir"
require "yaml"

ROOT = Pathname(__dir__).parent
SCRIPT = ROOT.join("scripts/verify_repo_governance.rb")

def fixture_config(root, owned: {})
  config = {
    "version" => 1,
    "limits" => {
      "github_large_object_review_bytes" => 10,
      "github_single_object_enforced_bytes" => 100,
      "github_repository_ondisk_recommended_bytes" => 10_000_000,
      "github_directory_entries_recommended" => 30,
      "github_directory_depth_recommended" => 10,
      "github_push_enforced_bytes" => 2_000,
      "gitlab_repository_bytes" => 10_000_000,
      "gitlab_push_bytes" => 5_000,
      "gitlab_pages_site_bytes" => 1_000
    },
    "forbidden_worktree_roots" => ["activos"],
    "tracked_forbidden_patterns" => ["public/**"],
    "local_residue_paths" => ["_site"],
    "owned_large_files" => owned,
    "falsified_by" => [{ "test" => "fixture", "observation" => "red/green observado por esta suite" }]
  }
  path = root.join("contract.yaml")
  path.write(config.to_yaml)
  path
end

def owner_record
  { "owner" => "fixture", "role" => "prueba", "retention" => "durante-la-prueba" }
end

def init_repo(root)
  Open3.capture3("git", "init", "-q", root.to_s)
  root.join("README.md").write("fixture\n")
  Open3.capture3("git", "-C", root.to_s, "add", "README.md")
  Open3.capture3(
    { "GIT_AUTHOR_NAME" => "Test", "GIT_AUTHOR_EMAIL" => "test@example.invalid",
      "GIT_COMMITTER_NAME" => "Test", "GIT_COMMITTER_EMAIL" => "test@example.invalid" },
    "git", "-C", root.to_s, "commit", "-qm", "fixture"
  )
end

def run_gate(root, config, *flags)
  stdout, stderr, status = Open3.capture3(
    "ruby", SCRIPT.to_s, "--root", root.to_s, "--config", config.to_s, "--strict", *flags
  )
  [JSON.parse(stdout), stderr, status]
end

describe "verify_repo_governance" do
  it "pasa con un archivo grande que tiene dueño explícito" do
    Dir.mktmpdir do |temporary|
      root = Pathname(temporary)
      init_repo(root)
      root.join("owned.bin").binwrite("x" * 12)
      Open3.capture3("git", "-C", root.to_s, "add", "owned.bin")
      config = fixture_config(root, owned: { "owned.bin" => owner_record })
      report, stderr, status = run_gate(root, config)
      assert status.success?, stderr
      assert_equal "pass", report.fetch("status")
    end
  end

  it "falla con un archivo grande sin dueño" do
    Dir.mktmpdir do |temporary|
      root = Pathname(temporary)
      init_repo(root)
      root.join("orphan.bin").binwrite("x" * 12)
      Open3.capture3("git", "-C", root.to_s, "add", "orphan.bin")
      config = fixture_config(root, owned: { "sentinel.bin" => owner_record })
      report, _stderr, status = run_gate(root, config)
      refute status.success?, "el gate no quedó rojo"
      assert report.fetch("violations").any? { |row| row.fetch("type") == "unowned_large_file" }, report.inspect
    end
  end

  it "falla si reaparece un worktree anidado aunque Git lo ignore" do
    Dir.mktmpdir do |temporary|
      root = Pathname(temporary)
      init_repo(root)
      root.join("activos/prueba/.git").mkpath
      config = fixture_config(root, owned: { "sentinel.bin" => owner_record })
      report, _stderr, status = run_gate(root, config)
      refute status.success?, "el gate no quedó rojo"
      types = report.fetch("violations").map { |row| row.fetch("type") }
      assert_includes types, "nested_git_metadata", report.inspect
      assert_includes types, "forbidden_worktree_root", report.inspect
    end
  end
end
