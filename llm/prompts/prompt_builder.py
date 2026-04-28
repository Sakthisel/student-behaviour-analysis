def build_prompt(row):
    return f"""
    Instruction:
    {row["instruction"]}

    Input:
    {row["input"]}

    Response:
    """.strip()


def build_target(row):
    return row["output"]
