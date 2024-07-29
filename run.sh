#!/bin/bash

# Stop the script on any error
set -e

# Optional: Delete older .pyc files
# find . -type d \( -name env -o -name venv \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Export environment variable for Flask
export FLASK_APP=core/server.py

# Uncomment these lines if you need to run migrations
# echo "Running Flask migrations..."
# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run the Flask server with Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn -c gunicorn_config.py core.server:app
