import pandas as pd


def prepare_student_summary(data):
    if isinstance(data, pd.DataFrame):
        df = data.copy()
        if "ml_engagement" not in df.columns:
            raise ValueError("ml_engagement column missing. Run ML prediction first.")
        df_summary = (
            df.groupby("student_id")
            .agg(
                attention_score=("attention_score", "mean"),
                engagement_score=("engagement_score", "mean"),
                gd_score=("gd_score", "mean"),
                ml_engagement=(
                    "ml_engagement",
                    lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0],
                ),
            )
            .reset_index()
        )
        data_list = df_summary.round(2).to_dict(orient="records")
    elif isinstance(data, list):
        data_list = data
    else:
        raise TypeError("Input must be DataFrame or list of dicts")

    if not data_list:
        return []

    data_list = sorted(data_list, key=lambda x: x["gd_score"], reverse=True)

    return data_list
