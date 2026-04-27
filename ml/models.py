from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout


def get_ml_models():
    return {
        "RandomForest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=1,
        ),
        "SVM": SVC(
            kernel="rbf",
            C=2.0,
            probability=True,
            random_state=42,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="mlogloss",
            random_state=42,
            n_jobs=1,
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=100,
            learning_rate=0.05,
            num_leaves=7,
            min_child_samples=5,
            force_row_wise=True,
            verbose=-1,
            random_state=42,
            n_jobs=1,
        ),
    }


def build_lstm_model(seq_len, num_features):
    model = Sequential(
        [
            Input(shape=(seq_len, num_features)),
            LSTM(128, return_sequences=True),
            Dropout(0.3),
            LSTM(64),
            Dropout(0.3),
            Dense(64, activation="relu"),
            Dropout(0.2),
            Dense(3, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model
