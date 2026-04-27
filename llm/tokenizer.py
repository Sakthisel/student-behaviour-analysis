from transformers import AutoTokenizer
from llm.config import PRE_TRAINED_MODEL


def load_tokenizer():
    return AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL)


def tokenize_dataset(dataset, tokenizer):
    def tokenize_fn(example):
        model_inputs = tokenizer(
            example["input_text"],
            max_length=512,
            truncation=True,
            padding="max_length",
        )

        labels = tokenizer(
            text_target=example["target_text"],
            max_length=256,
            truncation=True,
            padding="max_length",
        )

        model_inputs["labels"] = [
            token if token != tokenizer.pad_token_id else -100
            for token in labels["input_ids"]
        ]

        return model_inputs

    return dataset.map(tokenize_fn, remove_columns=dataset.column_names)
