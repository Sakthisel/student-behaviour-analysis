import joblib
import pandas as pd
import os

from sklearn.preprocessing import LabelEncoder, StandardScaler
from ml.config.config import FEATURES, MODEL_DIR


def transform_features(df, save=True):

    os.makedirs(MODEL_DIR, exist_ok=True)

    X = df[FEATURES].copy()
    y = df["target"]

    encoders = {}

    for col in X.columns:
        if X[col].dtype == "object":
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

    scaler = StandardScaler()
    X_scaled_array = scaler.fit_transform(X)

    X_scaled = pd.DataFrame(X_scaled_array, columns=FEATURES)

    if save:
        joblib.dump(FEATURES, f"{MODEL_DIR}/features.pkl")
        joblib.dump(scaler, f"{MODEL_DIR}/scaler.pkl")
        joblib.dump(encoders, f"{MODEL_DIR}/encoders.pkl")

    return X_scaled, y, scaler, encoders
