from datasets import Dataset

from llm.data_loader import load_llm_data
from llm.generate_dataset import generate_llm_data
from llm.preprocessing import prepare_llm_dataset
from llm.tokenizer import load_tokenizer, tokenize_dataset
from llm.model_loader import load_base_model, apply_lora
from llm.training import train_llm


def main():
    print("\nGenerate LLM data...")
    raw_data = generate_llm_data()

    print("\nLoading LLM data...")
    raw_data = load_llm_data()

    print("\nPreparing prompts...")
    processed_data = prepare_llm_dataset(raw_data)

    dataset = Dataset.from_list(processed_data)

    print("\nLoading tokenizer...")
    tokenizer = load_tokenizer()

    print("\nTokenizing dataset...")
    tokenized_dataset = tokenize_dataset(dataset, tokenizer)

    print("\nLoading base model...")
    base_model = load_base_model()

    print("\nApplying LoRA...")
    model = apply_lora(base_model)

    print("\nFine-tuning LLM...")
    train_llm(model, tokenizer, tokenized_dataset)

    print("\nLLM fine-tuning completed successfully.")

    # =============================
    # INFERENCE (AFTER TRAINING)
    # =============================
    print("\nTesting trained LLM...")

    from llm.inference import generate_report

    input_text = """Student ID: 1
    Attention Score: 2.00
    Engagement Score: 2.00
    GD Score: 4.00
    ML Engagement: LOW

    Analyze this student's performance."""

    print("Base model:")
    print(generate_report(input_text, use_lora=False))

    print("\nLoRA model:")
    print(generate_report(input_text, use_lora=True))


if __name__ == "__main__":
    main()
