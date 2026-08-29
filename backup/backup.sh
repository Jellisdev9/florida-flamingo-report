#!/bin/sh
set -eu

BACKUP_INTERVAL_SECONDS="${BACKUP_INTERVAL_SECONDS:-86400}"

while true; do
  if [ -z "${BACKUP_BUCKET:-}" ]; then
    echo "$(date -Iseconds) BACKUP_BUCKET not set, skipping (expected in local dev)"
  else
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    FILE="/tmp/${DB_NAME}_${TIMESTAMP}.sql.gz"
    echo "$(date -Iseconds) starting backup -> ${FILE}"
    PGPASSWORD="$DB_PASSWORD" pg_dump -h db -U "$DB_USER" "$DB_NAME" | gzip > "$FILE"
    rclone copy "$FILE" "remote:${BACKUP_BUCKET}/${DB_NAME}/"
    rm -f "$FILE"
    echo "$(date -Iseconds) backup complete"
  fi
  sleep "$BACKUP_INTERVAL_SECONDS"
done
