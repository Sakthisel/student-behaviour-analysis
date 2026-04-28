from pathlib import Path
import sys

import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import CSV_PATHS
from utils.validation import validate_dataframe


def combine():
    # =============================
    # LOAD
    # =============================
    gaze = pd.read_csv(CSV_PATHS["gaze"])
    gesture = pd.read_csv(CSV_PATHS["gesture"])
    pose = pd.read_csv(CSV_PATHS["pose"])
    emotion = pd.read_csv(CSV_PATHS["emotion"])

    # =============================
    # MERGE
    # =============================
    df = gaze.merge(gesture, on=["frame", "student_id"], how="outer")
    df = df.merge(pose, on=["frame", "student_id"], how="outer")
    df = df.merge(emotion, on=["frame", "student_id"], how="outer")

    print("\nColumns after merge:")
    print(df.columns.tolist())

    # =============================
    # Duplicates Check
    # =============================
    def resolve_column(df, col):
        if f"{col}_x" in df.columns and f"{col}_y" in df.columns:
            df[col] = df[f"{col}_x"].combine_first(df[f"{col}_y"])
            df.drop([f"{col}_x", f"{col}_y"], axis=1, inplace=True)
        elif f"{col}_x" in df.columns:
            df.rename(columns={f"{col}_x": col}, inplace=True)
        elif f"{col}_y" in df.columns:
            df.rename(columns={f"{col}_y": col}, inplace=True)

    cols_to_fix = [
        "joint_visual_attention",
        "individual_attention",
        "looking_other_student",
        "looking_away",
        "head_nod_shake",
    ]

    for col in cols_to_fix:
        resolve_column(df, col)

    # =============================
    # Validate structure
    # =============================
    df = validate_dataframe(df)

    # =============================
    # Fill missing safely
    # =============================
    df = df.fillna(
        {
            "joint_visual_attention": "N",
            "individual_attention": 0.0,
            "looking_other_student": 0.0,
            "looking_away": 1.0,
            "head_nod_shake": 0.0,
            "confidence": 0.5,
            "fiddling": 0.0,
            "lean": 0.0,
            "lean_x": 0.0,
            "lean_y": 0.0,
            "lean_towards": 0.0,
            "lean_away": 0.0,
            "positive": 0.0,
            "negative": 0.0,
            "bored": 0.0,
            "confusion": 0.0,
        }
    )

    # =============================
    # Correct datatypes
    # =============================
    float_cols = [
        "individual_attention",
        "looking_other_student",
        "looking_away",
        "head_nod_shake",
        "confidence",
        "fiddling",
        "lean_x",
        "lean_y",
        "lean_towards",
        "lean_away",
        "positive",
        "negative",
        "bored",
        "confusion",
    ]

    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].astype(float)

    # =============================
    # Derive pose safely
    # =============================
    def derive_pose(row):
        if row.get("lean", 0) == 1 or row.get("lean_towards", 0) == 1:
            return "forward"
        elif row.get("lean", 0) == -1 or row.get("lean_away", 0) == 1:
            return "backward"
        return "neutral"

    df["pose"] = df.apply(derive_pose, axis=1)

    # =============================
    # Improved scoring
    # =============================
    df["attention_score"] = (
        0.4 * (1 - df["looking_away"]) + 0.3 * df["individual_attention"]
    ) * 3

    df["engagement_score"] = (
        0.4 * df["looking_other_student"]
        + 0.3 * df["head_nod_shake"]
        + 0.3 * (1 - df["fiddling"])
    ) * 3

    df["behavior_score"] = (
        0.5 * df["confidence"]
        + 0.3 * df["positive"]
        - 0.2 * (df["negative"] + df["bored"] + df["confusion"])
    )

    df["behavior_score"] = np.clip(df["behavior_score"], 0, 1) * 4

    df["gd_score"] = (
        df["attention_score"] + df["engagement_score"] + df["behavior_score"]
    )

    # =============================
    # Normalize scores
    # =============================
    df["gd_score"] = df["gd_score"].clip(0, 10)

    # =============================
    # SORT
    # =============================
    df = df.sort_values(by=["frame", "student_id"]).reset_index(drop=True)

    # =============================
    # SAVE
    # =============================
    df.to_csv(CSV_PATHS["final"], index=False)

    print("\nFINAL CSV READY (CLEAN + ML SAFE)")
    print(df.head())

    return df
