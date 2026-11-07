#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Configuration variables
DB_HOST=${POSTGRES_HOST:-"postgres_db"}
DB_USER=${POSTGRES_USER:-"mrg_user"}
DB_NAME=${POSTGRES_DB:-"mrg_prod"}
BACKUP_DIR="/tmp/snapshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/mrg_${TIMESTAMP}.sql"
ENCRYPTED_FILE="${BACKUP_FILE}.enc"

mkdir -p "$BACKUP_DIR"

echo "[Backup Engine] Initializing table extraction payload sequence..."
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

echo "[Backup Engine] Encrypting structural output blocks using AES-256..."
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in "$BACKUP_FILE" \
  -out "$ENCRYPTED_FILE" \
  -pass env:BACKUP_ENCRYPTION_KEY

echo "[Backup Engine] Syncing encrypted transaction snapshots to Amazon S3 pool..."
# Requires aws-cli tools configured inside the runtime context
aws s3 cp "$ENCRYPTED_FILE" "s3://${AWS_BACKUP_BUCKET_NAME}/database/mrg_${TIMESTAMP}.sql.enc"

echo "[Backup Engine] Cleaning up temporary storage mounts..."
rm -f "$BACKUP_FILE" "$ENCRYPTED_FILE"

echo "[Backup Engine] Database backup state successfully archived and secured."
