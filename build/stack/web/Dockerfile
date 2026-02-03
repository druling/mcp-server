# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ../../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY ../../.. .

# Add the current directory to Python path
ENV PYTHONPATH=/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]