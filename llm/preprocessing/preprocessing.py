from llm.prompts.prompt_builder import build_prompt, build_target


def prepare_llm_dataset(data):
    processed = []

    for row in data:
        processed.append({
            "input_text": build_prompt(row),
            "target_text": build_target(row),
        })

    return processed
