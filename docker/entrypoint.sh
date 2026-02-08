#!/usr/bin/env bash
set -e

export BLOCKSEMBLER_DB_URI

echo "Starting container..."

if [[ "$DEBUG" == "true" || "$DEBUG" == "1" ]]; then
  echo "DEBUG=true --> Skipping Alembic migrations"
else
  echo "Running Alembic migrations..."
  alembic upgrade head
  echo "Migrations completed..."
fi

echo "Starting application..."
exec "$@"