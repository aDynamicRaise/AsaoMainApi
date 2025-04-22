#!/bin/bash
set -e

# Ждем пока PostgreSQL будет готов принимать подключения
until pg_isready -U "$POSTGRES_USER"; do
  sleep 1
done

# Восстанавливаем дамп
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -f /docker-entrypoint-initdb.d/dump.sql

echo "Database dump restored successfully"