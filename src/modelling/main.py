# This module is the training flow: it reads the data, preprocesses it, trains a model and saves it.

import argparse
from src.modelling.utils import load_data
from src.modelling.preprocessing import encode_sex, splitting_data
from src.modelling.training import train
from pathlib import Path


def main(trainset_path: Path = Path("data/abalone.csv")) -> None:
    """Train a model using the data at the given path and save the model (pickle)."""
    # Read data
    print("Loading data...")
    df = load_data(trainset_path)
    # Preprocess data
    print("Preprocessing data...")
    df = encode_sex(df)
    print("Splitting data...")
    X_train, _, y_train, _ = splitting_data(df)
    # (Optional) Pickle encoder if need be

    # Train model
    print("Training the model...")
    train(X_train, y_train, savepath="src/web_service/local_objects")
    # Pickle model --> The model should be saved in pkl format the `src/web_service/local_objects` folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument(
        "--trainset_path",
        type=str,
        default="data/abalone.csv",
        help="Path to the training set (default: data/abalone.csv)",
    )
    args = parser.parse_args()
    main(Path(args.trainset_path))
