# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Force the stdout and stderr streams to be unbuffered

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY ../../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY ../../.. .

# Copy and make entrypoint script executable
COPY build/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add the current directory to Python path
ENV PYTHONPATH=/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Use entrypoint script for proper signal handling
ENTRYPOINT ["/entrypoint.sh"]
