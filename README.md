# Adversarial Prompt Generator Framework

## Overview
This project provides a modular framework for generating adversarial prompts targeting vulnerabilities in Code Language Models (Code LMs). It combines a curated library of templates with multiple encoding techniques to systematically create and evaluate prompts that test the robustness of Code LMs.

### Files
- **data/templates.jsonl**: 
  Contains a set of predefined prompt templates, each tagged with a specific vulnerability type (e.g., injection, encoding, rule-based manipulation). These templates form the backbone of the adversarial testing framework.
  
- **prompt_generator.py**: 
  The main script that integrates user-provided malicious input with the templates. It applies multiple encoding techniques to create diverse adversarial prompts and writes the results to an output file.

- **data/output.jsonl**: 
  The file where generated adversarial prompts are saved. Each line contains a JSON object representing one prompt.

- **README.md**:
  Provides an overview of the project, a disclaimer, and instructions on how to run the code.

## Disclaimer
This project is intended solely for academic and research purposes to evaluate the safety and robustness of language models. Misuse of the framework for illegal or unethical purposes is strictly prohibited. The authors are not responsible for any consequences arising from the improper use of this tool.

## How to Run
1. Ensure you have Python installed on your machine.
2. Clone or download the repository.
3. Open a terminal or command prompt and navigate to the project directory.
4. Run the following command:
   ```bash
   python prompt_generator.py
5.	Enter your malicious input when prompted. The script will process the input, generate adversarial prompts using the templates and encodings, and save the output to `data/output.jsonl`.
