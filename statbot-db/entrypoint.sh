#!/bin/bash

set -euo pipefail

echo "Waiting for PostgreSQL..."

until pg_isready \
    -h "${DB_HOST}" \
    -p "${DB_PORT:-5432}" \
    -U "${DB_USERNAME}" \
    -d postgres
do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Creating ${DB_DATABASE} if necessary..."

# Export PGPASSWORD so psql and pg_isready can pick it up automatically
export PGPASSWORD="${DB_PASS}"

psql \
    -h "${DB_HOST}" \
    -p "${DB_PORT:-5432}" \
    -U "${DB_USERNAME}" \
    -d postgres \
    -v ON_ERROR_STOP=1 \
    -c "CREATE DATABASE ${DB_DATABASE};" \
    || true

echo "Downloading database backup..."

mkdir -p /tmp/statbot

mc alias set s3 "${S3_ENDPOINT}" "${S3_ACCESS_KEY}" "${S3_SECRET_KEY}"

mc cp \
    "s3/jonasmorin/diffusion/statbot_db/statbot.tar.gz" \
    /tmp/statbot/statbot.tar.gz

echo "Extracting database backup..."

tar -xvzf \
    /tmp/statbot/statbot.tar.gz \
    -C /tmp/statbot

echo "Restoring database..."

sed \
    -e 's|COPY|\\copy|g' \
    -e 's|\$\$PATH\$\$/||g' \
    /tmp/statbot/restore.sql \
    | psql \
        -h "${DB_HOST}" \
        -p "${DB_PORT:-5432}" \
        -U "${DB_USERNAME}" \
        -d "${DB_DATABASE}" \
        -v ON_ERROR_STOP=1

# Optional: If you need to set a default schema search path after restore
if [ -n "${DB_SCHEMA:-}" ]; then
    echo "Setting default search path to schema: ${DB_SCHEMA}"
    psql \
        -h "${DB_HOST}" \
        -p "${DB_PORT:-5432}" \
        -U "${DB_USERNAME}" \
        -d "${DB_DATABASE}" \
        -c "CREATE SCHEMA IF NOT EXISTS ${DB_SCHEMA};"
fi

echo "Database deployment completed successfully."