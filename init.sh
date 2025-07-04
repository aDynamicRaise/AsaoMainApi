#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER IF NOT EXISTS ${DB_USER} WITH PASSWORD '${DB_PASS}';
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOSQL