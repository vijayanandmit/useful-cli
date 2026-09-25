#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
uid="$(id -u)"

label="com.vijay.usefulcli.review"
plist_dir="$HOME/Library/LaunchAgents"
plist_path="$plist_dir/$label.plist"

interval_seconds="${REVIEW_INTERVAL_SECONDS:-86400}"
stdout_log="$HOME/Library/Logs/useful-cli-review.out.log"
stderr_log="$HOME/Library/Logs/useful-cli-review.err.log"

mkdir -p "$plist_dir"

cat >"$plist_path" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>$label</string>

    <key>ProgramArguments</key>
    <array>
      <string>$repo_root/scripts/review.sh</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$repo_root</string>

    <key>RunAtLoad</key>
    <true/>

    <key>StartInterval</key>
    <integer>$interval_seconds</integer>

    <key>StandardOutPath</key>
    <string>$stdout_log</string>
    <key>StandardErrorPath</key>
    <string>$stderr_log</string>
  </dict>
</plist>
PLIST

chmod 0644 "$plist_path"

launchctl bootout "gui/$uid" "$plist_path" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$uid" "$plist_path"
launchctl enable "gui/$uid/$label" >/dev/null 2>&1 || true
launchctl kickstart -k "gui/$uid/$label" >/dev/null 2>&1 || true

echo "Installed: $plist_path"
echo "Runs every ${interval_seconds}s and at load."
echo "Latest report: $repo_root/review-reports/latest.txt"
