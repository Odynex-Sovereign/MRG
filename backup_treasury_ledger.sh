#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit
set -o pipefail

# -----------------------------------------------------------------------------
# CONFIGURATION BOUNDS
# -----------------------------------------------------------------------------
BACKUP_DIR="${HOME}/mrg_backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/mrg_treasury_backup_${TIMESTAMP}.sql.gz"
LOG_FILE="${BACKUP_DIR}/backup_execution_audit.log"

# Target app environment credentials
APP_NAME="mrg"
DATABASE_SECRET_VAR="DATABASE_URL"

# Ensure target storage matrices exist locally
mkdir -p "${BACKUP_DIR}"

echo "[${TIMESTAMP}] 📡 Initializing automated cluster database extract loop..." | tee -a "${LOG_FILE}"

# 1. FETCH PRODUCTION ENCRYPTED CONNECTION STRINGS FROM CLUSTER SECRETS
DB_CONN_STR=$(fly secrets list -a "${APP_NAME}" --json | grep -v "Connecting" | jq -r '.[] | select(.Name=="'"${DATABASE_SECRET_VAR}"'") | .Value' 2>/dev/null || true)

# Sandbox proxy fallback if JSON pipelines are locked during maintenance checks
if [ -z "${DB_CONN_STR}" ]; then
    echo "[${TIMESTAMP}] ⚠️ Unable to fetch secret string programmatically via CLI json pipes. Attempting direct secret dump backup route..." | tee -a "${LOG_FILE}"
    # Alternative direct fallback dump method utilizing internal fly proxy tunneling bridges
    fly proxy 5432:5432 -a "${APP_NAME}-db" &
    PROXY_PID=$!
    sleep 3
    DB_CONN_STR="postgresql://postgres:your_db_password_here@localhost:5432/mrg_telemetry"
fi

# 2. EXECUTE HIGH-DENSITY AUDITABLE LEDGER DATA DUMP
echo "[${TIMESTAMP}] 💾 Fetching system treasury tables, balance histories, and yield indexes..." | tee -a "${LOG_FILE}"
if pg_dump "${DB_CONN_STR}" \
    --table=billing_vault \
    --table=structural_ledger_history \
    --table=high_frequency_yield_log \
    --table=insurance_compliance_registry \
    | gzip > "${BACKUP_FILE}"; then
    
    echo "[${TIMESTAMP}] ✅ Success! Production billing vault snapshot securely compressed at: ${BACKUP_FILE}" | tee -a "${LOG_FILE}"
else
    echo "[${TIMESTAMP}] ❌ Critical Error: Data extraction handshake loop aborted." | tee -a "${LOG_FILE}"
    if [ ! -z "${PROXY_PID}" ]; then kill "${PROXY_PID}"; fi
    exit 1
fi

# Kill proxy tunnels safely if spun up
if [ ! -z "${PROXY_PID}" ]; then kill "${PROXY_PID}"; fi

# 3. ENFORCE SECURE CONSERVATIVE FILE PROTECTION PERMISSIONS
chmod 600 "${BACKUP_FILE}"

# 4. PRUNE OLD SNAPS TO MAINTAIN BALANCED COLD STORAGE LIMITS (Retain last 14 days)
find "${BACKUP_DIR}" -type f -name "mrg_treasury_backup_*.sql.gz" -mtime +14 -exec rm {} \;
echo "[${TIMESTAMP}] 🧹 Pruning expired backup blocks. Ledger protection task complete." | tee -a "${LOG_FILE}"
