import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "Sex_encoded",
    "Length",
    "Diameter",
    "Height",
    "Whole weight",
    "Shucked weight",
    "Viscera weight",
    "Shell weight",
]
TARGET_COLUMN = ["Rings"]


def encode_sex(df: pd.DataFrame) -> pd.DataFrame:
    label_encoder = LabelEncoder()
    df["Sex_encoded"] = label_encoder.fit_transform(df["Sex"])
    return df.drop(["Sex"], axis=1)


def splitting_data(df: pd.DataFrame) -> pd.DataFrame:
    y = df[TARGET_COLUMN]
    X = df.drop(TARGET_COLUMN, axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test
