#!/usr/bin/env bash

# Formulate standard production execution environment paths
export AWS_ACCESS_KEY_ID=$(cat /run/secrets/AWS_ACCESS_KEY_ID 2>/dev/null || echo "$AWS_ACCESS_KEY_ID")
export AWS_SECRET_ACCESS_KEY=$(cat /run/secrets/AWS_SECRET_ACCESS_KEY 2>/dev/null || echo "$AWS_SECRET_ACCESS_KEY")
export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-"us-east-1"}

# Execute the primary encryption backup data transfer workflow utility
/bin/bash /app/scripts/backup_db.sh >> /var/log/mrg_backup_cron.log 2>&1
