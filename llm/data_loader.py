import json
from llm.config import DATA_PATH


def load_llm_data(data_path=DATA_PATH):
    data = []

    with open(data_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            data.append(json.loads(line))

    if not data:
        raise ValueError("LLM training data is empty.")

    return data