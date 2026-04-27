from pathlib import Path
from functools import lru_cache

import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
from llm.config import PRE_TRAINED_MODEL, OUTPUT_DIR


def _tokenizer_path(use_lora: bool) -> str:
    if use_lora and Path(OUTPUT_DIR).exists():
        return OUTPUT_DIR
    return PRE_TRAINED_MODEL


@lru_cache(maxsize=2)
def load_model(use_lora=True):
    device = "cpu"

    tokenizer_source = _tokenizer_path(use_lora)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_source)

    config = AutoConfig.from_pretrained(PRE_TRAINED_MODEL)

    base_model = AutoModelForSeq2SeqLM.from_pretrained(PRE_TRAINED_MODEL, config=config)

    if use_lora and Path(OUTPUT_DIR).exists():
        model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)
    else:
        model = base_model

    if model.config.pad_token_id is None:
        model.config.pad_token_id = tokenizer.eos_token_id

    model.to(device)
    model.eval()

    return model, tokenizer, device


def generate_report(input_text, use_lora=True):
    model, tokenizer, device = load_model(use_lora)

    prompt = (
        "You are an expert classroom analytics AI. Analyze the following student performance data "
        "and return a structured report exactly in the format shown below.\n\n"
        f"INPUT:\n{input_text}\n\n"
        "OUTPUT FORMAT:\n"
        "LLM OUTPUT:\n"
        " Okay, let's analyze this student performance data and generate the requested output.\n\n"
        "**TOP PERFORMER:**\n\n"
        "*   **Student ID:** [ID]\n"
        "*   **Reason:** [Reason]\n\n"
        "**RANKING:**\n\n"
        "1.  Student ID: [ID] - [Score]\n"
        "2.  Student ID: [ID] - [Score]\n"
        "3.  Student ID: [ID] - [Score]\n\n"
        "**INDIVIDUAL REPORTS:**\n\n"
        "*   **Student ID:** [ID]\n"
        "    *   Attention: [Score]\n"
        "    *   Engagement: [Score]\n"
        "    *   Performance (GD): [Score]\n"
        "    *   ML Insight: [Text]\n"
        "    *   Strength: [Text]\n"
        "    *   Weakness: [Text]\n"
        "    *   Recommendation: [Text]\n\n"
        "**FINAL SUMMARY:**\n\n"
        "[Summary text]"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding="max_length",
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=280,
            min_new_tokens=80,
            num_beams=2,
            early_stopping=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            do_sample=False,
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    if text.startswith(prompt):
        text = text[len(prompt) :].strip()

    if not text:
        return "No report generated."

    return text
