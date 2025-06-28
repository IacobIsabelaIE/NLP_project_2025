# 🧠 NLP Project 2025

This repository contains the implementation and evaluation setup for the **NLP Project 2025**, focused on using **prompt engineering techniques** to perform **knowledge base construction** with large language models (LLMs), specifically for the **LM-KBC Challenge @ ISWC 2025**.

---

## 📂 Branch: `few-shot-branch`

This branch contains experiments and evaluations related to the **few-shot prompting** technique.

##🧪 Evaluation Instructions

To evaluate your model predictions against the ground truth, use the `evaluate.py` script with the following command:

```bash
python evaluate.py -g data/val.jsonl -p <generated_file.jsonl> -o <output_metrics.txt>

.................
