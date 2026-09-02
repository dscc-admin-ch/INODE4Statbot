#!/bin/bash

set -euo pipefail

echo "Waiting for PostgreSQL..."

until pg_isready \
    -h "${PGHOST}" \
    -U "${PGUSER}" \
    -d postgres
do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Creating statbotdb if necessary..."

psql \
    -h "${PGHOST}" \
    -U "${PGUSER}" \
    -d postgres \
    -v ON_ERROR_STOP=1 \
    -c "CREATE DATABASE statbotdb;" \
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
        -h "${PGHOST}" \
        -U "${PGUSER}" \
        -d statbotdb \
        -v ON_ERROR_STOP=1

echo "Database deployment completed successfully."
