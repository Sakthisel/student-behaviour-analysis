import os
import json
import pandas as pd

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.data_loader import load_data
from ml.preprocessing import clean_data

LABEL_MAP = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}


def generate_llm_data(output_path="llm/data/student_reports.jsonl"):
    # =============================
    # CREATE DIRECTORY
    # =============================
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # =============================
    # LOAD + CLEAN DATA
    # =============================
    df = load_data()
    df = clean_data(df)

    if df is None or df.empty:
        raise ValueError("Input dataframe is empty")

    # =============================
    # GENERATE DATASET
    # =============================
    with open(output_path, "w") as f:
        for _, row in df.iterrows():

            ml_label = LABEL_MAP.get(int(row["target"]), "LOW")

            # =============================
            # INPUT
            # =============================
            input_text = (
                f"Student ID: {int(row['student_id'])}\n"
                f"Attention Score: {row['attention_score']:.2f}\n"
                f"Engagement Score: {row['engagement_score']:.2f}\n"
                f"GD Score: {row['gd_score']:.2f}\n"
                f"ML Engagement: {ml_label}\n\n"
                "Analyze this student's performance."
            )

            # =============================
            # OUTPUT LOGIC
            # =============================
            if ml_label == "HIGH":
                level_text = "high engagement"
                behavior = "highly active and focused"
            elif ml_label == "MEDIUM":
                level_text = "moderate engagement"
                behavior = "moderately engaged with some active participation"
            else:
                level_text = "low predicted engagement"
                behavior = "less visibly engaged and need improvement"

            focus_text = (
                "good focus" if row["attention_score"] > 2 else "moderate focus"
            )

            performance_text = (
                "strong performance" if row["gd_score"] > 4 else "average performance"
            )

            # =============================
            # OUTPUT
            # =============================
            output_text = (
                f"The student shows {level_text} based on the ML classification. "
                f"The attention score of {row['attention_score']:.2f} indicates {focus_text}. "
                f"The overall group discussion performance is {row['gd_score']:.2f}, showing {performance_text}. "
                f"The student is {behavior}.\n\n"
                "Recommendation: Improve participation and maintain consistent attention during discussions."
            )

            # =============================
            # RECORD
            # =============================
            record = {
                "instruction": "Analyze student performance and generate a report.",
                "input": input_text,
                "output": output_text,
            }

            f.write(json.dumps(record) + "\n")

    print(f" LLM dataset created at: {output_path}")


# =============================
# RUN
# =============================
if __name__ == "__main__":
    generate_llm_data()
