import sys
import traceback
import time

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

from llm.inference.gemini import generate_report
from ml.models.prediction import predict_batch
from cv_pipelines.main import cv_pipelines


# =============================
# MAIN
# =============================
if __name__ == "__main__":

    start_time = time.time()

    df = cv_pipelines()

    try:
        # =============================
        # REQUIRED COLUMN CHECK
        # =============================
        required_cols = [
            "student_id",
            "attention_score",
            "engagement_score",
            "gd_score",
        ]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns from scoring: {missing}")

        # =============================
        # CREATE TARGET
        # =============================
        df["target"] = df["engagement_score"].apply(
            lambda x: 0 if x <= 2 else 1 if x <= 4 else 2
        )

        # =============================
        # ML PREDICTION
        # =============================
        print("\nRunning ML engagement prediction...")

        df = predict_batch(df)

        if "ml_engagement" not in df.columns:
            raise ValueError("ML prediction failed: ml_engagement not found")

        print("ML prediction completed")

        # =============================
        # SAMPLE OUTPUT
        # =============================
        print("\nML Predictions (sample):")

        print(
            df[
                [
                    "student_id",
                    "attention_score",
                    "engagement_score",
                    "gd_score",
                    "ml_engagement",
                ]
            ].head(10)
        )

        # =============================
        # ACCURACY CHECK
        # =============================
        label_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

        if "target" in df.columns and "ml_engagement" in df.columns:

            # =============================
            # SAFE CONVERSION
            # =============================
            y_true = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int)

            y_pred = (
                df["ml_engagement"].astype(str).map(label_map).fillna(-1).astype(int)
            )

            mask = y_pred != -1
            y_true = y_true[mask]
            y_pred = y_pred[mask]

            acc = accuracy_score(y_true, y_pred)

            print("\nML MODEL EVALUATION")
            print(f"Accuracy: {acc:.4f}\n")

            print(classification_report(y_true, y_pred))

        else:
            print("\nMissing required columns → skipping accuracy")

        # =============================
        # LLM EVALUATION
        # =============================
        print("\nRunning LLM evaluation...")
        df_sorted = df.sort_values("gd_score", ascending=False)

        report = generate_report(df_sorted)

        print("\nLLM OUTPUT:\n", report)

    except Exception as e:
        print(f"\nPost-processing error: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    # =============================
    # DONE
    # =============================
    total_time = round(time.time() - start_time, 2)
    print(f"\nFinished Successfully in {total_time}s", flush=True)
