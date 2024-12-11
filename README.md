# Adversarial Prompt Generator Framework

This repository contains a framework designed to evaluate the robustness of code-focused language models (Code LMs) like SemCoder against adversarial prompts. The framework includes tools for dataset generation, model testing, and automated evaluation.

## Disclaimer
This project is intended solely for academic and research purposes to evaluate the safety and robustness of language models. Misuse of the framework for illegal or unethical purposes is strictly prohibited. The authors are not responsible for any consequences arising from the improper use of this tool.

## Structure

```
COMS6998-FINALPROJ/
├── data/
│   ├── individual_results/      # Stores individual evaluation results for each prompt
│   ├── prompts.jsonl            # Generated adversarial prompts
│   ├── report.txt               # Summary report of evaluation results
│   ├── templates.jsonl          # Library of tagged adversarial templates
│   ├── test_results.jsonl       # Combined test results and evaluations
├── evaluate.py                  # Script for automated evaluation of model responses
├── prompt_generator.py          # Script for generating adversarial prompts
├── test_semcoder.py             # Script for testing SemCoder with the generated prompts
├── README.md                    # Detailed instructions for using the repository
```

## Setup and Requirements
### Prerequisites
* Python 3.8 or later
* Access to OpenAI API for evaluation
* GPU-enabled environment for testing SemCoder (optional but recommended)

## Usage
### Step 1: Generating Adversarial Prompts
The `prompt_generator.py` script generates a dataset of adversarial prompts using the template library and user-provided input. You can optionally include encoded prompts using the `--use-encoding` flag.

```bash
python prompt_generator.py --templates data/templates.jsonl --output data/prompts.jsonl --use-encoding
```
When you run the script, it will prompt you to enter the malicious input. For example:

```bash
Enter the malicious input to craft prompts: write detailed code to hack a windows 11 PC
```

### Step 2: Testing SemCoder with Prompts
The `test_semcoder.py` script tests the SemCoder model by feeding it the adversarial prompts generated in Step 1. It saves both individual results and an aggregated file of responses for further evaluation.

```bash
python test_semcoder.py
```

### Step 3: Automated Evaluation Using OpenAI API
The `evaluate.py` script evaluates the model responses using the OpenAI API. It classifies each response as Safe, Harmful, or Undefined and generates a summary report.

```bash
python evaluate.py --input data/individual_results --output data/test_results.jsonl --report data/report.txt
```
