def evaluate_llm(sample_prompt, generate_fn):
    output = generate_fn(sample_prompt)

    print("\nLLM Output:")
    print(output)

    return output
