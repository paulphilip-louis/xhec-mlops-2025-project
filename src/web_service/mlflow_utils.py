"""MLFlow utilities for tracking experiments and models."""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from pathlib import Path
import logging
from typing import Optional, Dict, Any
from .app_config import config

logger = logging.getLogger(__name__)


def setup_mlflow():
    """Initialize MLFlow tracking configuration."""
    if config.mlflow_enable_tracking:
        try:
            mlflow.set_tracking_uri(config.mlflow_tracking_uri)
            
            # Create experiment if it doesn't exist
            try:
                experiment = mlflow.get_experiment_by_name(config.mlflow_experiment_name)
                if experiment is None:
                    mlflow.create_experiment(config.mlflow_experiment_name)
                    logger.info(f"Created MLFlow experiment: {config.mlflow_experiment_name}")
            except Exception as e:
                logger.warning(f"Could not create/access MLFlow experiment: {e}")
                
            mlflow.set_experiment(config.mlflow_experiment_name)
            logger.info(f"MLFlow tracking initialized with URI: {config.mlflow_tracking_uri}")
            
        except Exception as e:
            logger.error(f"Failed to initialize MLFlow: {e}")
            config.mlflow_enable_tracking = False


def log_training_run(
    model,
    hyperparameters: Dict[str, Any],
    metrics: Dict[str, float],
    training_samples: int,
    model_path: Optional[Path] = None
) -> Optional[str]:
    """Log a training run to MLFlow.
    
    Args:
        model: The trained model
        hyperparameters: Model hyperparameters
        metrics: Training metrics (e.g., train_score, test_score)
        training_samples: Number of training samples
        model_path: Path where the model is saved locally
        
    Returns:
        MLFlow run ID if successful, None otherwise
    """
    if not config.mlflow_enable_tracking:
        return None
        
    try:
        with mlflow.start_run() as run:
            # Log hyperparameters
            mlflow.log_params(hyperparameters)
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log additional info
            mlflow.log_param("training_samples", training_samples)
            mlflow.log_param("model_type", type(model).__name__)
            
            # Log the model
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=config.mlflow_model_name
            )
            
            # Log local model file if provided
            if model_path and model_path.exists():
                mlflow.log_artifact(str(model_path), "local_model")
                
            logger.info(f"Logged training run to MLFlow: {run.info.run_id}")
            return run.info.run_id
            
    except Exception as e:
        logger.error(f"Failed to log training run to MLFlow: {e}")
        return None


def log_prediction(
    input_features: Dict[str, Any],
    prediction: float,
    model_version: Optional[str] = None
) -> Optional[str]:
    """Log a prediction to MLFlow.
    
    Args:
        input_features: Input features used for prediction
        prediction: The prediction result
        model_version: Version of the model used
        
    Returns:
        MLFlow run ID if successful, None otherwise
    """
    if not config.mlflow_enable_tracking:
        return None
        
    try:
        with mlflow.start_run() as run:
            # Log input features as parameters
            for key, value in input_features.items():
                mlflow.log_param(f"input_{key}", value)
                
            # Log prediction as metric
            mlflow.log_metric("prediction", prediction)
            
            if model_version:
                mlflow.log_param("model_version", model_version)
                
            # Tag as inference run
            mlflow.set_tag("run_type", "inference")
            
            return run.info.run_id
            
    except Exception as e:
        logger.error(f"Failed to log prediction to MLFlow: {e}")
        return None


def get_latest_model_version() -> Optional[str]:
    """Get the latest version of the registered model.
    
    Returns:
        Latest model version string if available, None otherwise
    """
    if not config.mlflow_enable_tracking:
        return None
        
    try:
        client = MlflowClient()
        latest_version = client.get_latest_versions(
            config.mlflow_model_name,
            stages=["Production", "Staging", "None"]
        )
        
        if latest_version:
            return latest_version[0].version
            
    except Exception as e:
        logger.error(f"Failed to get latest model version: {e}")
        
    return None


def load_model_from_mlflow(version: Optional[str] = None):
    """Load model from MLFlow registry.
    
    Args:
        version: Specific version to load. If None, loads latest.
        
    Returns:
        Loaded model if successful, None otherwise
    """
    if not config.mlflow_enable_tracking:
        return None
        
    try:
        if version is None:
            version = get_latest_model_version()
            
        if version is None:
            logger.warning("No model version found in MLFlow registry")
            return None
            
        model_uri = f"models:/{config.mlflow_model_name}/{version}"
        model = mlflow.sklearn.load_model(model_uri)
        
        logger.info(f"Loaded model from MLFlow: {model_uri}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model from MLFlow: {e}")
        return None
