import pickle as pkl
import pandas as pd

TRAINSET_PATH = "data/abalone.csv"


def pickle_object(obj, filepath):
    """
    Save a Python object to a file using pickle.

    Args:
        obj: Any Python object (model, encoder, etc.)
        filepath: Path where to save the pickled object
    """
    with open(filepath, "wb") as f:
        pkl.dump(obj, f)


def load_data(datapath):
    df = pd.read_csv(datapath)
    return df
