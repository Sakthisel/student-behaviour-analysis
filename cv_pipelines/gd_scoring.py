import pandas as pd
from config import CSV_PATHS
from ml.utils import make_label


def compute_scores(df):
    df.fillna(0, inplace=True)

    # =============================
    # SAFE GETTER
    # =============================
    def get(row, col, default=0):
        return row[col] if col in row and pd.notna(row[col]) else default

    # =============================
    # ATTENTION SCORE
    # =============================
    def attention_score(row):
        score = 0

        looking_object = get(row, "joint_visual_attention", "N")

        if looking_object in ["L", "B"]:
            score += 2

        if get(row, "looking_other_student", 0) == 1:
            score += 1

        if get(row, "looking_away", 1) == 1:
            score -= 2

        return score

    df["attention_score"] = df.apply(attention_score, axis=1)

    # =============================
    # ENGAGEMENT SCORE
    # =============================
    def engagement_score(row):
        score = 0

        score += 2 * get(row, "positive", 0)
        score -= get(row, "negative", 0)
        score -= get(row, "bored", 0)

        score += get(row, "fiddling", 0)
        score += get(row, "lean_towards", 0)

        return score

    df["engagement_score"] = df.apply(engagement_score, axis=1)

    # =============================
    # FINAL GD SCORE
    # =============================
    df["gd_score"] = df["attention_score"] + df["engagement_score"]

    df["target"] = df["engagement_score"].apply(make_label)

    # =============================
    # STUDENT LEVEL SUMMARY
    # =============================
    summary = (
        df.groupby("student_id")
        .agg(
            {
                "attention_score": "mean",
                "engagement_score": "mean",
                "gd_score": "mean",
                "target": lambda x: x.mode()[0],
            }
        )
        .reset_index()
    )

    summary = summary.sort_values("gd_score", ascending=False)

    # =============================
    # SAVE OUTPUTS
    # =============================
    df.to_csv(CSV_PATHS["final"], index=False)
    summary.to_csv(CSV_PATHS["summary"], index=False)

    print("\nGD Scoring Completed")

    print("\nTOP PERFORMER:")
    print(summary.head(1))

    print("\nSTUDENT RANKING:")
    print(summary)

    return df, summary
