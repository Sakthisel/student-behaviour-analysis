import pandas as pd
import numpy as np
from ml.config import FEATURES, TARGET_COL
from ml.utils import make_label


def clean_data(df):
    pd.set_option("future.no_silent_downcasting", True)

    df = df.copy()
    df = df.replace(["-", "None", "nan", ""], np.nan)
    df = df.fillna(0)

    for col in FEATURES + [TARGET_COL]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["target"] = df[TARGET_COL].apply(make_label)

    return df
