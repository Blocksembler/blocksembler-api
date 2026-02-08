#!/usr/bin/env bash
set -e

export BLOCKSEMBLER_DB_URI

echo "Starting container..."

if [[ "$DEBUG" == "true" || "$DEBUG" == "1" ]]; then
  echo "DEBUG=true --> Skipping Alembic migrations"
else
  echo "Running Alembic migrations..."
  if ! alembic upgrade head; then
    echo "Alembic migrations failed, exiting..."
    exit 1
  fi
  echo "Migrations completed..."
fi

echo "Starting application..."
exec "$@"