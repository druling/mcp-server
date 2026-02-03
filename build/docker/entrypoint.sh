#!/bin/bash

# Enable exit on error
set -e

# Function to handle shutdown signals
shutdown() {
    echo "Received shutdown signal, gracefully stopping uvicorn..."
    if [ ! -z "$UVICORN_PID" ]; then
        kill -TERM "$UVICORN_PID"
        wait "$UVICORN_PID"
    fi
    echo "Application stopped gracefully"
    exit 0
}

# Trap SIGTERM and SIGINT signals
trap shutdown SIGTERM SIGINT

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Store the PID of uvicorn process
UVICORN_PID=$!

# Wait for the process to complete
wait "$UVICORN_PID"
