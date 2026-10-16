#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting Gunicorn..."
exec gunicorn -c gunicorn.conf.py app.main:app
