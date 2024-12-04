import json
from transformers import pipeline
import torch


def load_prompts(file_path):
    """Load prompts from a JSONL file."""
    prompts = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():
                data = json.loads(line)
                prompts.append(data["prompt"])
    return prompts


def test_semcoder(prompt, generator):
    """Test a single prompt on SemCoder and return the result."""
    try:
        result = generator(prompt, max_length=2048, num_return_sequences=1, temperature=0.0)
        return result[0]["generated_text"]
    except Exception as e:
        print(f"Error testing prompt: {e}")
        return None


def main():
    # Initialize the SemCoder model pipeline
    print("Initializing SemCoder...")
    generator = pipeline(
        model="semcoder/semcoder_s_1030",
        task="text-generation",
        torch_dtype=torch.float16,
        device_map="auto",
    )
    print("SemCoder initialized successfully!")

    # Load the generated prompts
    prompt_file = "data/output.jsonl"  # Path to the JSONL file with generated prompts
    prompts = load_prompts(prompt_file)
    print(f"Loaded {len(prompts)} prompts for testing.")

    # Test each prompt and save the results
    results = []
    output_file = "data/test_results.jsonl"  # Path to save the results

    for idx, prompt in enumerate(prompts):
        print(f"Testing prompt {idx + 1}/{len(prompts)}...")
        result = test_semcoder(prompt, generator)
        if result:
            results.append({"prompt": prompt, "result": result})
        else:
            print(f"Prompt {idx + 1} failed.")

    # Save results to a JSONL file
    with open(output_file, "w") as file:
        for entry in results:
            file.write(json.dumps(entry) + "\n")

    print(f"Testing completed. Results saved to {output_file}.")


if __name__ == "__main__":
    main()