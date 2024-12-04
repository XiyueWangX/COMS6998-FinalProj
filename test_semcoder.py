import json
from transformers import pipeline
import torch
import os


def load_prompts(file_path):
    """Load prompts with metadata from a JSONL file."""
    prompts = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():
                data = json.loads(line)
                prompts.append(data)  # Load the full dictionary including tag and encoding
    return prompts


def test_semcoder(prompt_text, generator):
    """Test a single prompt on SemCoder and return the result."""
    try:
        result = generator(prompt_text, max_length=2048, num_return_sequences=1, temperature=0.0)
        return result[0]["generated_text"]
    except Exception as e:
        print(f"Error testing prompt: {e}")
        return None


def save_individual_result(idx, prompt_data, result, output_dir):
    """Save individual results to separate files, including metadata."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"result_{idx + 1}.json")
    with open(output_path, "w") as file:
        json.dump(
            {
                "tag": prompt_data.get("tag"),
                "encoding": prompt_data.get("encoding"),
                "prompt": prompt_data.get("prompt"),
                "result": result,
            },
            file,
            indent=4,
        )
    print(f"Saved result for prompt {idx + 1} to {output_path}")


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
    prompt_file = "data/prompts.jsonl"  # Path to the JSONL file with generated prompts
    prompts = load_prompts(prompt_file)
    print(f"Loaded {len(prompts)} prompts for testing.")

    # Test each prompt and save the results
    results = []
    output_file = "data/test_results.jsonl"  # Path to save the aggregated results
    individual_output_dir = "data/individual_results"  # Directory to save individual result files

    for idx, prompt_data in enumerate(prompts):
        prompt_text = prompt_data.get("prompt", "")
        print(f"Testing prompt {idx + 1}/{len(prompts)} (Tag: {prompt_data.get('tag')}, Encoding: {prompt_data.get('encoding')})...")
        result = test_semcoder(prompt_text, generator)
        if result:
            results.append({
                "tag": prompt_data.get("tag"),
                "encoding": prompt_data.get("encoding"),
                "prompt": prompt_text,
                "result": result,
            })
            # Save individual result
            save_individual_result(idx, prompt_data, result, individual_output_dir)
        else:
            print(f"Prompt {idx + 1} failed.")

    # Save aggregated results to a JSONL file
    with open(output_file, "w") as file:
        for entry in results:
            file.write(json.dumps(entry) + "\n")

    print(f"Testing completed. Aggregated results saved to {output_file}.")


if __name__ == "__main__":
    main()
