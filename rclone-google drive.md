• Here are the basic CLI commands we used to copy a local file to Google Drive using rclone.

  # 1. Download rclone
  curl -L -o /tmp/rclone.zip https://downloads.rclone.org/rclone-current-linux-amd64.zip

  # 2. Unzip it
  unzip -q /tmp/rclone.zip -d /tmp

  # 3. Create an rclone Google Drive remote
  /tmp/rclone-v1.73.4-linux-amd64/rclone config create mydrive drive scope drive --config /tmp/rclone.conf

  That command opens an OAuth URL. Open it in your browser, approve Google Drive access, then continue.

  # 4. Copy a local file to a specific Google Drive folder by folder ID
  /tmp/rclone-v1.73.4-linux-amd64/rclone copyto \
    /path/to/local/file.md \
    mydrive:file.md \
    --drive-root-folder-id GOOGLE_DRIVE_FOLDER_ID \
    --config /tmp/rclone.conf \
    -v

  For your exact case:

  /tmp/rclone-v1.73.4-linux-amd64/rclone copyto \
    claude_trader.md \
    ibkrdrive:claude_trader.md \
    --drive-root-folder-id 1sFgQQukoK5Td4rWde7BNE9odCknJzME0 \
    --config /tmp/rclone.conf \
    -v

  Optional verification:

  /tmp/rclone-v1.73.4-linux-amd64/rclone lsf \
    ibkrdrive: \
    --drive-root-folder-id 1sFgQQukoK5Td4rWde7BNE9odCknJzME0 \
    --config /tmp/rclone.conf

  If you want the config to persist across sessions, omit --config /tmp/rclone.conf so rclone stores it in its default config location, usually:

  ~/.config/rclone/rclone.conf
