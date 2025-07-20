#!/bin/sh

# Aspetta che il DB sia pronto (usa pg_isready o simile)
until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  echo "Aspettando database..."
  sleep 2
done

# Applica le migration
alembic upgrade head

# Avvia l'app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload