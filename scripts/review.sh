#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

timestamp="$(date +"%Y%m%d-%H%M%S")"
report_dir="$repo_root/review-reports"
mkdir -p "$report_dir"

report_file="$report_dir/$timestamp.txt"
latest_file="$report_dir/latest.txt"

{
  echo "useful-cli review report: $timestamp"
  echo "repo: $repo_root"
  echo

  echo "## git"
  if command -v git >/dev/null 2>&1; then
    git rev-parse --abbrev-ref HEAD 2>/dev/null | sed 's/^/branch: /' || true
    git rev-parse --short HEAD 2>/dev/null | sed 's/^/head: /' || true
    echo "status:"
    git status --porcelain || true
  else
    echo "git: not found"
  fi
  echo

  echo "## python"
  if command -v python3 >/dev/null 2>&1; then
    python3 -V || true
    if [ -d "leetcode" ]; then
      echo "compileall: leetcode/"
      python3 -m compileall -q leetcode || true
    fi
  elif command -v python >/dev/null 2>&1; then
    python -V || true
    if [ -d "leetcode" ]; then
      echo "compileall: leetcode/"
      python -m compileall -q leetcode || true
    fi
  else
    echo "python: not found (tried python3, python)"
  fi
  echo
} >"$report_file"

cp -f "$report_file" "$latest_file"
