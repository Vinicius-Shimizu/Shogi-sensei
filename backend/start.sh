#!/bin/bash

set -e

echo "Running migrations..."

alembic upgrade head

echo "Starting application..."

# exec python3 -m src.exercise_generator
exec uvicorn src.server:app --host 0.0.0.0 --port 8000