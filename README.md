# NLP-Adversarial-Sentiment-Analysis 🚀

### Improving Sentiment Analysis Robustness through a Self-Evolving Adversarial Loop

## 📝 Project Overview
This project is inspired by **Stanford's CS224N (2024)**. Our goal is to address a critical flaw in modern NLP models: **Fragility**. While models like DistilBERT achieve high accuracy on standard datasets, they often fail when faced with minor text perturbations (typos, leetspeak, or code-switching).

We propose an innovative **Self-Evolving Framework** that doesn't just classify sentiment, but actively learns to defend itself against adversarial attacks.

## 💡 The Innovation: Self-Evolving Critic Loop
Unlike traditional sentiment classifiers, our approach implements a three-stage system:
1.  **The Adversary (Generator):** Automatically generates complex perturbations (morphological changes, symbols, and "Franco-Arabic" influence).
2.  **The Rationalizer (Stability Metric):** Measures how much the model's confidence "drops" when the input style changes while the meaning remains constant.
3.  **The Mentor-Student Loop:** Uses a "Mentor" (Reasoning logic) to teach the "Student" (Classifier) **why** a certain sentence is negative, focusing on the core meaning rather than the superficial word shape.

## 🏗️ Project Structure
- `baseline.py`: Initial implementation using DistilBERT on the SST-2 dataset.
- `perturbator.py`: (Under Development) Automated attack generation engine.
- `evaluator.py`: Stability metrics and error analysis tools.
- `requirements.txt`: Project dependencies for environment reproducibility.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PyTorch
- HuggingFace Transformers & Datasets

