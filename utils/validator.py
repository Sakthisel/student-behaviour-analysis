from schema.gd_schema import REQUIRED_COLUMNS


def validate_dataframe(df):

    missing_cols = []

    for col, default in REQUIRED_COLUMNS.items():
        if col not in df.columns:
            df[col] = default
            missing_cols.append(col)

    if missing_cols:
        print("\nMissing columns added automatically:")
        print(missing_cols)

    return df
