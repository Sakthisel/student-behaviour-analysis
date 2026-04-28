from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq
from llm.config.config import OUTPUT_DIR, NUM_EPOCHS, LEARNING_RATE


def train_llm(model, tokenizer, tokenized_dataset):
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True
    )

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=LEARNING_RATE,
        max_grad_norm=0.5,
        save_strategy="epoch",
        logging_steps=1,
        report_to="none",
        remove_unused_columns=False,
        fp16=False,
        bf16=False,
        dataloader_pin_memory=False,
        dataloader_num_workers=0,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    trainer.train()

    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    return model
