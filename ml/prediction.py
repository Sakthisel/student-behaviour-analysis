import os
import joblib
import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model
from ml.config import MODEL_DIR, FEATURES, LABEL_MAP, SEQ_LEN


def prepare_ml_input(df):
    features = joblib.load(f"{MODEL_DIR}/features.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")

    encoders_path = f"{MODEL_DIR}/encoders.pkl"
    encoders = joblib.load(encoders_path) if os.path.exists(encoders_path) else {}

    X = df.copy()
    X = X.replace(["-", "None", "nan", ""], np.nan)

    for feature in features:
        if feature not in X.columns:
            X[feature] = 0

    X = X[features]

    for col, le in encoders.items():
        if col in X.columns:
            X[col] = X[col].astype(str)
            mask = X[col].isin(le.classes_)
            X.loc[mask, col] = le.transform(X.loc[mask, col])
            X.loc[~mask, col] = -1

    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    X_scaled = scaler.transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=features)

    return X_scaled


def predict_batch(df, model_name="best_ml_model"):
    if isinstance(df, tuple):
        df = df[0]

    if df is None or df.empty:
        raise ValueError("Input dataframe is empty or None")

    output_df = df.copy()

    model = joblib.load(f"{MODEL_DIR}/{model_name}.pkl")
    X = prepare_ml_input(output_df)

    preds = model.predict(X).astype(int)

    output_df["ml_engagement"] = [LABEL_MAP.get(int(pred), "UNKNOWN") for pred in preds]

    return output_df


def predict_all_ml_models(sample_dict):
    predictions = {}

    for model_name in ["RandomForest", "SVM", "XGBoost", "LightGBM"]:
        model_path = f"{MODEL_DIR}/{model_name}.pkl"

        if os.path.exists(model_path):
            sample_df = pd.DataFrame([sample_dict])
            result_df = predict_batch(sample_df, model_name)
            predictions[model_name] = result_df["ml_engagement"].iloc[0]

    return predictions


def predict_lstm(sample_dict):
    model = load_model(f"{MODEL_DIR}/engagement_lstm_model.keras")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")

    x = pd.DataFrame([sample_dict])

    for feature in FEATURES:
        if feature not in x.columns:
            x[feature] = 0

    x = x[FEATURES]
    x = x.apply(pd.to_numeric, errors="coerce").fillna(0)

    x_scaled = scaler.transform(x)

    x_seq = np.repeat(x_scaled.reshape(1, 1, len(FEATURES)), SEQ_LEN, axis=1)

    pred = model.predict(x_seq, verbose=0)
    pred_class = int(np.argmax(pred, axis=1)[0])

    return LABEL_MAP.get(pred_class, "UNKNOWN")


def predict_hybrid(sample_dict):
    return {
        "all_ml_models": predict_all_ml_models(sample_dict),
        "lstm": predict_lstm(sample_dict),
    }
