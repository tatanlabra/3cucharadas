#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
silent_hook="$repo_root/scripts/git-hooks/post-commit"
diffusion_hook="$repo_root/scripts/git-hooks/post-commit-difusion"
target_hook="$(git rev-parse --git-path hooks/post-commit)"

for source_hook in "$silent_hook" "$diffusion_hook"; do
  if [ ! -f "$source_hook" ]; then
    printf 'missing hook source: %s\n' "$source_hook" >&2
    exit 1
  fi
done

mkdir -p "$(dirname "$target_hook")"
temporary_hook="$(mktemp "${target_hook}.tmp.XXXXXX")"
trap 'rm -f "$temporary_hook"' EXIT
cat > "$temporary_hook" <<'SH'
#!/usr/bin/env bash
set -u
root="$(git rev-parse --show-toplevel)"
"$root/scripts/git-hooks/post-commit" || true
"$root/scripts/git-hooks/post-commit-difusion" || true
exit 0
SH

if [ -e "$target_hook" ] && cmp -s "$temporary_hook" "$target_hook"; then
  printf 'hook chain already installed: %s\n' "$target_hook"
else
  if [ -e "$target_hook" ]; then
    backup="$target_hook.backup-$(date +%Y%m%d%H%M%S)"
    cp "$target_hook" "$backup"
    printf 'backed up existing hook: %s\n' "$backup"
  fi
  install -m 0755 "$temporary_hook" "$target_hook"
  printf 'installed hook chain: %s\n' "$target_hook"
fi

# pre-push: frena secretos antes de que el push salga hacia GitLab y GitHub (ver el hook).
push_source="$repo_root/scripts/git-hooks/pre-push"
push_target="$(git rev-parse --git-path hooks/pre-push)"
if [ ! -f "$push_source" ]; then
  printf 'missing hook source: %s\n' "$push_source" >&2
  exit 1
fi
if [ -e "$push_target" ] && cmp -s "$push_source" "$push_target"; then
  printf 'pre-push already installed: %s\n' "$push_target"
else
  if [ -e "$push_target" ]; then
    backup="$push_target.backup-$(date +%Y%m%d%H%M%S)"
    cp "$push_target" "$backup"
    printf 'backed up existing hook: %s\n' "$backup"
  fi
  install -m 0755 "$push_source" "$push_target"
  printf 'installed pre-push: %s\n' "$push_target"
fi
