from transformers import AutoConfig, AutoModelForSeq2SeqLM
from peft import LoraConfig, get_peft_model
from llm.config import PRE_TRAINED_MODEL


def load_base_model():
    config = AutoConfig.from_pretrained(PRE_TRAINED_MODEL)

    model = AutoModelForSeq2SeqLM.from_pretrained(
        PRE_TRAINED_MODEL,
        config=config
    )

    return model.to("cpu")


def apply_lora(model):
    lora_config = LoraConfig(
        r=4,
        lora_alpha=8,
        target_modules=["q", "v"],
        lora_dropout=0.05,
        bias="none",
        task_type="SEQ_2_SEQ_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    return model