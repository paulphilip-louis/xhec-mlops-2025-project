# Dockerfile for Abalone Age Prediction API with MLFlow
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY src/ ./src/
COPY data/ ./data/
COPY simple_train.py ./
COPY bin/ ./bin/

# Create directories for model storage and MLFlow
RUN mkdir -p src/web_service/local_objects
RUN mkdir -p mlflow_data/mlruns
RUN mkdir -p mlflow_data/artifacts

# Make run script executable
RUN chmod +x bin/run_services.sh

# Set MLFlow environment variables
ENV MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow_data/mlflow.db
ENV MLFLOW_DEFAULT_ARTIFACT_ROOT=./mlflow_data/artifacts

# Expose ports (8000 for FastAPI, 5000 for MLFlow)
EXPOSE 8000 5000

# Health check for FastAPI
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the service
CMD ["./bin/run_services.sh"]
