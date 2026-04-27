import os
import joblib
import numpy as np

from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from ml.config import MODEL_DIR, FEATURES, SEQ_LEN
from ml.models import get_ml_models, build_lstm_model
from ml.evaluation import evaluate_model


def train_ml_models(X_train, X_test, y_train, y_test):
    os.makedirs(MODEL_DIR, exist_ok=True)

    models = get_ml_models()

    best_model = None
    best_name = None
    best_acc = 0
    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")

        model.fit(X_train, y_train)

        acc, _ = evaluate_model(model, X_test, y_test, name)
        results[name] = acc

        joblib.dump(model, f"{MODEL_DIR}/{name}.pkl")

        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    joblib.dump(best_model, f"{MODEL_DIR}/best_ml_model.pkl")
    joblib.dump(results, f"{MODEL_DIR}/ml_results.pkl")

    print("\nBest ML Model:", best_name)
    print("Best ML Accuracy:", best_acc)

    return best_name, best_acc, results


def create_lstm_sequences(df, seq_len=SEQ_LEN):
    X_seq = []
    y_seq = []

    for sid in df["student_id"].unique():
        sdf = df[df["student_id"] == sid].reset_index(drop=True)

        X_s = sdf[FEATURES].values.astype(np.float32)
        y_s = sdf["target"].values

        for i in range(len(sdf) - seq_len):
            X_seq.append(X_s[i : i + seq_len])
            y_seq.append(y_s[i + seq_len])

    return np.array(X_seq), np.array(y_seq)


def train_lstm_model(df):
    os.makedirs(MODEL_DIR, exist_ok=True)

    X_seq, y_seq = create_lstm_sequences(df)

    if len(X_seq) == 0:
        raise ValueError("Not enough rows for LSTM sequences. Reduce SEQ_LEN.")

    X_train, X_test, y_train, y_test = train_test_split(
        X_seq, y_seq, test_size=0.2, random_state=42, stratify=y_seq
    )

    y_train_cat = to_categorical(y_train, 3)
    y_test_cat = to_categorical(y_test, 3)

    model = build_lstm_model(SEQ_LEN, len(FEATURES))

    model.fit(
        X_train,
        y_train_cat,
        epochs=25,
        batch_size=16,
        validation_data=(X_test, y_test_cat),
        verbose=1,
    )

    model.save(f"{MODEL_DIR}/engagement_lstm_model.keras")

    y_pred = model.predict(X_test, verbose=0)
    y_pred_labels = np.argmax(y_pred, axis=1)
    y_true = np.argmax(y_test_cat, axis=1)

    print("\n==============================")
    print("LSTM Accuracy:", accuracy_score(y_true, y_pred_labels))
    print("==============================")

    print(
        classification_report(
            y_true,
            y_pred_labels,
            labels=[0, 1, 2],
            target_names=["LOW", "MEDIUM", "HIGH"],
            zero_division=0,
        )
    )

    return model
