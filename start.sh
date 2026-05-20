#!/bin/bash

echo "Waiting database..."

sleep 5

echo "Running migrations..."

alembic upgrade head

echo "Starting application..."

python3 src/exercise_generator.py