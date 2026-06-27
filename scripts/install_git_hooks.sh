#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
source_hook="$repo_root/scripts/git-hooks/post-commit"
target_hook="$(git rev-parse --git-path hooks/post-commit)"

if [ ! -f "$source_hook" ]; then
  printf 'missing hook source: %s\n' "$source_hook" >&2
  exit 1
fi

mkdir -p "$(dirname "$target_hook")"

if [ -e "$target_hook" ] && ! cmp -s "$source_hook" "$target_hook"; then
  backup="$target_hook.backup-$(date +%Y%m%d%H%M%S)"
  cp "$target_hook" "$backup"
  printf 'backed up existing hook: %s\n' "$backup"
fi

install -m 0755 "$source_hook" "$target_hook"
printf 'installed hook: %s\n' "$target_hook"
