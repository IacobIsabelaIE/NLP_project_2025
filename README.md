# 🧠 NLP Project 2025

This repository contains the implementation and evaluation setup for **NLP Project 2025**, focused on using **prompt engineering techniques** to perform **knowledge base construction** with large language models (LLMs). The work is developed as part of the **LM-KBC Challenge @ ISWC 2025**.

---

## 🌿 Branch Overview

- **`main`** — Contains experiments based on **persona-style prompting**.
- **`double-cot-prompt-experiments`** — Contains experiments using **double prompting + Chain-of-Thought (CoT)** reasoning.
- **`few_shot_branch`** — Focuses on **few-shot prompting** strategies for improving model predictions.

---

## ⚙️ Running the Experiments

### 🧪 Generating Predictions

To generate predictions:

1. Open the notebook: `notebooks/model_experimentation.ipynb`.
2. Run all the cells sequentially.
3. Save the generated results in a JSONL file (e.g., `few_shot_prompt8.jsonl`).

---

### 📊 Evaluating the Predictions

To evaluate your predictions against the ground truth, run the following command:

```bash
python evaluate.py -g data/val.jsonl -p <generated_file.jsonl> -o <output_metrics.txt>
