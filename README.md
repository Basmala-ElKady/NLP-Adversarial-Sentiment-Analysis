# NLP Adversarial Sentiment Analysis

A production-ready pipeline for performing inference and adversarial attacks on a robust sentiment analysis model.

## Features
- **Inference Only:** No model retraining. Centralized model loading.
- **Adversarial Evaluation:** Uses TextAttack to generate perturbations (TextFooler, PWWS, DeepWordBug, BAE).
- **Visualization & Metrics:** Computes attack success rate (ASR), accuracy, and confidence changes.
- **Backend API:** FastAPI endpoints for `/predict` and `/attack`.
- **Cross-Platform:** Works on Windows, Linux, and Google Colab.

## Project Structure
```
project/
├── models/
│   └── final_robust_model/      # Put your trained model here
├── notebooks/                   # Jupyter notebooks
├── backend/                     # FastAPI backend
│   ├── api/
│   ├── services/
│   ├── utils/
│   └── main.py
├── frontend/                    # React frontend (if applicable)
├── results/                     # Evaluation results
│   ├── csv/
│   ├── json/
│   ├── plots/
│   └── reports/
├── src/                         # Core Python modules
│   ├── config.py
│   ├── model_loader.py
│   ├── inference.py
│   ├── attack_pipeline.py
│   ├── evaluation.py
│   ├── visualization.py
│   └── helpers.py
├── requirements.txt
└── README.md
```

## Setup & Installation

1. **Install Requirements:**
```bash
pip install -r requirements.txt
```

2. **Project Restructuring (Important!):**
If you have just pulled this code, you may need to move your `nlp/models/final_robust_model` to `models/final_robust_model` and clean up the old directory structure. You can automatically restructure your folder by running the included python script:
```bash
python restructure.py
```

## Running the Backend

The model is loaded once on startup via `src.model_loader`.

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints
- **GET `/`**: Health check.
- **POST `/predict`**: Predict sentiment of the given text.
- **POST `/attack`**: Perform adversarial attack on the given text.

## Local / Colab Usage

You can use the `src` modules directly in any notebook or script.
Make sure to set your Python Path to include the project root, or run your notebooks directly from the `notebooks/` folder.
