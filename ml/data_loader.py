import pandas as pd
from ml.config import DATA_PATH


def load_data(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    if df is None or df.empty:
        raise ValueError("Dataset is empty or not loaded correctly.")

    return df
