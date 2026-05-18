<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=NLP%20ADVERSARIAL%20SENTIMENT%20ANALYSIS%20LAB&fontSize=26&fontColor=ffffff&animation=fadeIn" />

  <a href="https://github.com/Basmala-ElKady/NLP-Adversarial-Sentiment-Analysis">
    <img src="https://readme-typing-svg.demolab.com/?lines=NLP%20ADVERSARIAL%20BENCHMARK;ROBUSTNESS%20STRESS%20TESTING;ATTACK%20SIMULATION%20LAB;FULL%20PIPELINE%20INTEGRATION&font=Fira%20Code&center=true&width=600&height=50&color=36BCF7&vCenter=true&size=24" />
  </a>

  
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
    <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  </p>


</div>


A state-of-the-art interactive lab and evaluation pipeline for testing the robustness of sentiment analysis models against adversarial perturbations. This repository contains both a high-fidelity **evaluation benchmark** using TextAttack and a live, lightning-fast **React + FastAPI Web Application** featuring custom zero-dependency adversarial heuristics.

---

## Key Features

### Zero-Latency Model Initialization
The robust transformer model is eagerly preloaded into GPU/CPU memory during FastAPI startup, eliminating cold-start delays and enabling near-instant inference from the very first API request.

---

### Real-Time Adversarial Simulation Engine
Traditional adversarial frameworks such as TextAttack often require **30+ seconds** per attack generation.

To support a real-time interactive web experience, the platform implements lightweight local perturbation strategies inspired by state-of-the-art attacks:

| Original Attack | High-Speed Local Strategy |
|-----------------|--------------------------|
| TextFooler      | Context-aware synonym substitution |
| BAE             | Leetspeak transformation |
| DeepWordBug     | Character-level typo injection |
| PWWS            | Repeated-character perturbation |

These optimizations reduce attack latency to **under 1ms** while preserving realistic adversarial behavior.

---

### Advanced Evaluation & Benchmarking Pipeline
A dedicated CLI benchmarking framework enables large-scale robustness evaluation with detailed analytics including:

- Attack Success Rate (ASR)
- Accuracy degradation
- Confidence shift analysis
- Prediction stability tracking
- Robustness visualization reports

The evaluation engine automatically generates publication-style plots and metric reports using Matplotlib.

---

### Modern Interactive Frontend
The platform features a responsive glassmorphism-based UI with smooth micro-interactions powered by Framer Motion.

Users can:

- Run real-time sentiment inference
- Launch adversarial simulations interactively
- Visualize robustness degradation instantly
- Explore attack behavior through an intuitive dashboard


---

## Project Structure

```
NLP-Adversarial-Sentiment-Analysis/
├── backend/                     # FastAPI Application
│   ├── api/                     # HTTP router & validation schemas
│   ├── services/                # Core logic & attacks mapping
│   │   ├── attacks.py           # High-speed offline custom perturbations
│   │   └── attacker.py          # Wrapper routing requests safely
│   └── main.py                  # API entrance & startup pre-loading config
├── frontend/                    # Vite + React Client
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdversarialLab.jsx  # Interactive attack test sandbox
│   │   │   └── SentimentForm.jsx   # Live model sentiment predictor
│   │   ├── services/
│   │   │   └── api.js              # Axios configuration & routing
│   │   └── main.jsx
│   └── package.json
├── nlp/                         # Research & Model Hub
│   ├── models/
│   │   └── final_robust_model/  # Place trained robust model files here
│   └── src/                     # Evaluation engine
│       ├── model_loader.py      # Eager/lazy loading Singleton
│       ├── inference.py         # Sentiment classification service
│       └── attack_pipeline.py   # TextAttack recipe definitions
├── results/                     # Metric exports & visualizations
├── run_evaluation.py            # CLI benchmark testing script
├── requirements.txt             # Python requirements
└── README.md
```

---

##  Setup & Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** and **Node.js 16+** installed on your system.

### 2. Python Backend Setup
Initialize your environment and install dependencies:
```bash
# Clone the repository
git clone https://github.com/Basmala-ElKady/NLP-Adversarial-Sentiment-Analysis.git
cd NLP-Adversarial-Sentiment-Analysis

# Install python requirements
pip install -r requirements.txt
```

> [!TIP]
> The backend has been decoupled from the heavy `textattack` library on startup. You **do not** need to install `textattack` to run the FastAPI app or React frontend! 

### 3. Model Files
Ensure your trained model files (`model.safetensors`, `config.json`, `tokenizer.json`, etc.) are placed inside:
`nlp/models/final_robust_model/`

---

## Running the Lab

To get the full application running, open two terminal windows:

### Terminal A: Start the FastAPI Backend
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
*The terminal will display `[🚀] Pre-loading robust model on startup...` and ready classifications instantly on port 8000.*

### Terminal B: Start the React Frontend
```bash
cd frontend
npm install
npm run dev
```
*The app will compile and launch on `http://localhost:5173`.*

---

## Benchmarking & CLI Evaluation

To execute a comprehensive adversarial stress test over your dataset using heavy `TextAttack` recipes (TextFooler, BAE, PWWS, DeepWordBug):

```bash
# Run deep adversarial benchmark evaluation
python run_evaluation.py --attack deepwordbug --num_examples 100
```

> [!NOTE]
> Evaluation scripts will generate automatic visualizations (Accuracy vs Perturbation Rate, Model Confidence Distribution) inside the `results/plots/` folder and CSV sheets in `results/csv/`.

---

## Custom Attack Pipeline

To guarantee 100% reliability, the backend uses a tiered defense for synonym substitution (`TextFooler`):
```python
# TIER 1: Zero-latency high-speed local dictionary
LOCAL_SYNONYMS = { "good": "decent", "great": "excellent", "bad": "poor", ... }

# TIER 2: Offline WordNet fallback via NLTK corpus
# TIER 3: Typo injection fallback to ensure perturbation never fails or hangs
```
This multi-tier pipeline guarantees the server never freezes or crashes when performing perturbations.

---

## Contributing
Feel free to open issues or submit pull requests to enhance the adversarial resilience of this sentiment lab!
