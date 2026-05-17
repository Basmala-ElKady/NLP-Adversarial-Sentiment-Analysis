import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Model Paths
MODEL_DIR = BASE_DIR / "models" / "final_robust_model"

# Results Paths
RESULTS_DIR = BASE_DIR / "results"
CSV_DIR = RESULTS_DIR / "csv"
JSON_DIR = RESULTS_DIR / "json"
PLOTS_DIR = RESULTS_DIR / "plots"
REPORTS_DIR = RESULTS_DIR / "reports"

# Ensure directories exist
for d in [MODEL_DIR, CSV_DIR, JSON_DIR, PLOTS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Training/Eval Constants
MAX_LENGTH = 128
BATCH_SIZE = 32

# Attack Recipes
SUPPORTED_ATTACKS = ["textfooler", "pwws", "deepwordbug", "bae"]
