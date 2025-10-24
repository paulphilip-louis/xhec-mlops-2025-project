# MLFlow Integration with FastAPI Docker Image

This document describes the MLFlow integration that has been added to the Abalone Age Prediction FastAPI application.

## Overview

The FastAPI application now includes comprehensive MLFlow tracking capabilities for both training and inference operations. MLFlow provides experiment tracking, model registry, and model serving capabilities.

## Features Added

### 1. MLFlow Tracking Server
- **Automatic startup**: MLFlow tracking server starts automatically with the Docker container
- **SQLite backend**: Uses SQLite database for metadata storage
- **Local artifacts**: Stores model artifacts locally within the container
- **Web UI**: Accessible at `http://localhost:5000`

### 2. Training Tracking
- **Hyperparameters**: All training hyperparameters are logged
- **Metrics**: Training and validation metrics (MSE, R²) are tracked
- **Model artifacts**: Trained models are automatically registered in MLFlow
- **Training metadata**: Sample counts and model types are recorded

### 3. Inference Tracking
- **Prediction logging**: Individual predictions can be logged (optional)
- **Input features**: All input features are recorded as parameters
- **Model versioning**: Tracks which model version was used for predictions

### 4. Configuration Management
- **Environment variables**: MLFlow settings configurable via environment variables
- **Flexible URIs**: Support for different MLFlow tracking URIs
- **Enable/disable**: MLFlow tracking can be toggled on/off

## Architecture Changes

### New Files Added

#### `src/web_service/mlflow_utils.py`
Contains all MLFlow-related utility functions:
- `setup_mlflow()`: Initialize MLFlow configuration
- `log_training_run()`: Log training experiments
- `log_prediction()`: Log individual predictions
- `get_latest_model_version()`: Retrieve latest model version
- `load_model_from_mlflow()`: Load models from MLFlow registry

#### Updated Configuration (`src/web_service/app_config.py`)
Added MLFlow configuration parameters:
```python
# MLFlow configuration
mlflow_tracking_uri: str = "http://localhost:5000"
mlflow_experiment_name: str = "abalone_age_prediction"
mlflow_model_name: str = "abalone_model"
mlflow_enable_tracking: bool = True
```

### Modified Files

#### `src/web_service/main.py`
- Added MLFlow initialization on startup
- Enhanced `/train` endpoint with experiment tracking
- Enhanced `/predict` endpoint with optional prediction logging
- Added comprehensive error handling for MLFlow operations

#### `Dockerfile.app`
- Added MLFlow server dependencies
- Created MLFlow data directories
- Exposed port 5000 for MLFlow UI
- Set MLFlow environment variables

#### `bin/run_services.sh`
- Added MLFlow server startup
- Improved service orchestration
- Added graceful shutdown handling

## Usage

### Starting the Services

```bash
# Build the Docker image
docker build -f Dockerfile.app -t abalone-api-mlflow .

# Run the container
docker run -p 8000:8000 -p 5000:5000 abalone-api-mlflow
```

### Accessing the Services

- **FastAPI Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLFlow UI**: http://localhost:5000

### Training with MLFlow Tracking

```bash
# Train a model (automatically logged to MLFlow)
curl -X POST "http://localhost:8000/train" \
  -H "Content-Type: application/json" \
  -d '{
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "random_state": 42
  }'
```

### Making Predictions

```bash
# Make a prediction (optionally logged to MLFlow)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

## Environment Variables

You can customize MLFlow behavior using environment variables:

```bash
# MLFlow tracking URI
ABALONE_MLFLOW_TRACKING_URI=http://localhost:5000

# Experiment name
ABALONE_MLFLOW_EXPERIMENT_NAME=abalone_age_prediction

# Model registry name
ABALONE_MLFLOW_MODEL_NAME=abalone_model

# Enable/disable tracking
ABALONE_MLFLOW_ENABLE_TRACKING=true
```

## MLFlow UI Features

### Experiments View
- View all training runs
- Compare hyperparameters and metrics
- Sort and filter experiments
- Download artifacts

### Models Registry
- Browse registered models
- View model versions
- Promote models to different stages
- Model lineage tracking

### Runs Comparison
- Side-by-side comparison of runs
- Metrics visualization
- Parameter analysis
- Artifact comparison

## Data Persistence

### Docker Volume Mounting
To persist MLFlow data between container restarts:

```bash
docker run -p 8000:8000 -p 5000:5000 \
  -v $(pwd)/mlflow_data:/app/mlflow_data \
  abalone-api-mlflow
```

### External MLFlow Server
To use an external MLFlow server:

```bash
docker run -p 8000:8000 \
  -e ABALONE_MLFLOW_TRACKING_URI=http://external-mlflow:5000 \
  abalone-api-mlflow
```

## Monitoring and Logging

### Application Logs
The application provides detailed logging for MLFlow operations:
- Successful experiment logging
- Model registration status
- Error handling and fallbacks

### Health Checks
The `/health` endpoint includes MLFlow status information.

## Best Practices

### 1. Experiment Organization
- Use descriptive experiment names
- Tag runs with meaningful information
- Document hyperparameter choices

### 2. Model Management
- Register successful models
- Use model stages (Staging, Production)
- Version models systematically

### 3. Performance Considerations
- MLFlow logging is non-blocking
- Failed logging doesn't affect API functionality
- Configurable logging levels

## Troubleshooting

### Common Issues

#### MLFlow Server Not Starting
- Check port 5000 availability
- Verify SQLite database permissions
- Check Docker container logs

#### Tracking Not Working
- Verify `ABALONE_MLFLOW_ENABLE_TRACKING=true`
- Check MLFlow server connectivity
- Review application logs for errors

#### Model Registration Failures
- Ensure MLFlow server is accessible
- Check model artifacts directory permissions
- Verify experiment exists

### Debug Mode
Enable debug logging by setting:
```bash
export PYTHONPATH=/app
export MLFLOW_TRACKING_URI=http://localhost:5000
```

## Security Considerations

### Production Deployment
- Use authentication for MLFlow UI
- Secure MLFlow tracking URI
- Implement proper access controls
- Use HTTPS for external connections

### Data Privacy
- Be mindful of logging sensitive data
- Configure appropriate retention policies
- Implement data anonymization if needed

## Integration Benefits

1. **Experiment Reproducibility**: All training runs are tracked and reproducible
2. **Model Lineage**: Clear tracking of model versions and their performance
3. **Collaboration**: Team members can share and compare experiments
4. **Production Monitoring**: Track model performance in production
5. **Automated Workflows**: Enable CI/CD pipelines with MLFlow integration

## Next Steps

### Potential Enhancements
1. **Model Serving**: Use MLFlow model serving capabilities
2. **A/B Testing**: Implement model comparison frameworks
3. **Automated Retraining**: Trigger retraining based on performance metrics
4. **Advanced Metrics**: Add custom metrics and visualizations
5. **Integration with Cloud**: Deploy to cloud MLFlow services

This integration provides a solid foundation for MLOps practices and can be extended based on specific requirements.
