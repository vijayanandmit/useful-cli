#!/usr/bin/env bash
set -euo pipefail

uid="$(id -u)"
label="com.vijay.usefulcli.review"
plist_path="$HOME/Library/LaunchAgents/$label.plist"

if [ -f "$plist_path" ]; then
  launchctl bootout "gui/$uid" "$plist_path" >/dev/null 2>&1 || true
  rm -f "$plist_path"
  echo "Removed: $plist_path"
else
  echo "Not installed: $plist_path"
fi
