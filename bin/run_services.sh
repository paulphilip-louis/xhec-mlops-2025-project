#!/bin/bash

# Script to run the Abalone Age Prediction API service with MLFlow

echo "🦪 Starting Abalone Age Prediction API Service with MLFlow..."
echo "============================================================="

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Check if model exists, if not train one
if [ ! -f "src/web_service/local_objects/model.pkl" ]; then
    echo "⚠️  Model not found! Training a new model..."
    python simple_train.py
    if [ $? -eq 0 ]; then
        echo "✅ Model trained successfully!"
    else
        echo "❌ Model training failed!"
        exit 1
    fi
fi

# Start MLFlow tracking server in background
echo "🔬 Starting MLFlow tracking server on port 5000..."
mlflow server \
    --backend-store-uri sqlite:///mlflow_data/mlflow.db \
    --default-artifact-root ./mlflow_data/artifacts \
    --host 0.0.0.0 \
    --port 5000 &

# Wait a moment for MLFlow to start
sleep 3

# Start the FastAPI server
echo "🚀 Starting FastAPI server on port 8000..."
echo ""
echo "🌐 Service URLs:"
echo "   📖 API Documentation: http://localhost:8000/docs"
echo "   🏠 API Home Page: http://localhost:8000/"
echo "   🔬 MLFlow UI: http://localhost:5000/"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start FastAPI server (this will run in foreground)
uvicorn src.web_service.main:app --host 0.0.0.0 --port 8000
